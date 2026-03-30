"""
Oracle Database Utility Functions

Shared utilities for oracle_query and oracle_execute plugins.
Handles connection management, DSN construction, SQL classification,
Oracle data type conversion, error categorization, and parameter validation.

Ported from galdr_oracle standalone server into galdr_docker plugin system.
"""
import logging
import os
import re
import math
import base64
import glob
from datetime import datetime, date, time as time_type, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any, Tuple

import sqlparse

logger = logging.getLogger(__name__)

# ============================================================
# ORACLE THICK MODE INITIALIZATION
# ============================================================
# Must be called once before any oracledb.connect() calls.
# Thick mode enables Network Encryption, Data Integrity, and
# advanced Oracle Net features via the Instant Client libraries.

_oracle_thick_initialized = False


def ensure_thick_mode():
    """Initialize Oracle thick mode (idempotent).

    Searches for Instant Client in common Docker and local paths.
    Raises on failure since thick mode is required for Network Encryption.
    """
    global _oracle_thick_initialized
    if _oracle_thick_initialized:
        return True

    import oracledb

    # Candidate paths: explicit ORACLE_HOME, well-known Docker paths, then no-arg fallback
    candidate_dirs = []
    oracle_home = os.environ.get("ORACLE_HOME")
    if oracle_home:
        candidate_dirs.append(oracle_home)
    # Docker paths (versioned dir or stable symlink)
    candidate_dirs += glob.glob("/opt/oracle/instantclient_*")
    candidate_dirs.append("/opt/oracle/instantclient")

    last_error = None
    for lib_dir in candidate_dirs:
        if not os.path.isdir(lib_dir):
            continue
        try:
            oracledb.init_oracle_client(lib_dir=lib_dir)
            _oracle_thick_initialized = True
            logger.info(f"Oracle thick mode initialized (lib_dir={lib_dir})")
            return True
        except Exception as e:
            last_error = e
            logger.debug(f"Thick mode init failed with {lib_dir}: {e}")
            continue

    # Last resort: no lib_dir, let oracledb search LD_LIBRARY_PATH / ldconfig
    try:
        oracledb.init_oracle_client()
        _oracle_thick_initialized = True
        logger.info("Oracle thick mode initialized (system library path)")
        return True
    except Exception as e:
        last_error = e

    # If we get here, thick mode failed entirely
    logger.error(f"Oracle thick mode FAILED - all paths exhausted: {last_error}")
    _oracle_thick_initialized = True  # Don't retry every call
    return False


# ============================================================
# CONFIGURATION
# ============================================================

def get_oracle_config(config: dict, is_write: bool = False) -> dict:
    """
    Extract Oracle connection config from the galdr config dict.

    Uses ORACLE_SRC_* for read and ORACLE_TGT_* for write operations.
    Falls back to ORACLE_* prefix if SRC/TGT not set.
    """
    if is_write:
        return {
            'host': config.get('oracle_tgt_host') or config.get('oracle_host', 'localhost'),
            'port': int(config.get('oracle_tgt_port') or config.get('oracle_port', 1521)),
            'username': config.get('oracle_tgt_user') or config.get('oracle_user', ''),
            'password': config.get('oracle_tgt_password') or config.get('oracle_password', ''),
            'service_name': config.get('oracle_tgt_service') or config.get('oracle_service', ''),
        }
    else:
        return {
            'host': config.get('oracle_src_host') or config.get('oracle_host', 'localhost'),
            'port': int(config.get('oracle_src_port') or config.get('oracle_port', 1521)),
            'username': config.get('oracle_src_user') or config.get('oracle_user', ''),
            'password': config.get('oracle_src_password') or config.get('oracle_password', ''),
            'service_name': config.get('oracle_src_service') or config.get('oracle_service', ''),
        }


# ============================================================
# CONNECTION MANAGEMENT
# ============================================================

def construct_oracle_dsn(host: str, port: int, service_name: str = None) -> str:
    """Construct an Oracle DSN string: host:port/service_name."""
    if not host or not isinstance(port, int):
        raise ValueError("Host and port are required for Oracle DSN construction")
    if service_name:
        return f"{host}:{port}/{service_name}"
    return f"{host}:{port}"


def validate_oracle_dsn(dsn: str) -> dict:
    """Validate an Oracle DSN string format."""
    if not dsn or not isinstance(dsn, str):
        return {"is_valid": False, "error": "DSN must be a non-empty string", "dsn_type": "INVALID"}
    if ":" not in dsn:
        return {"is_valid": False, "error": "DSN must contain at least host:port format", "dsn_type": "INVALID"}

    parts = dsn.split(":")
    if len(parts) < 2:
        return {"is_valid": False, "error": "DSN must contain at least host:port format", "dsn_type": "INVALID"}

    host = parts[0]
    try:
        port = int(parts[1].split("/")[0])
    except ValueError:
        return {"is_valid": False, "error": "Port must be a valid integer", "dsn_type": "INVALID"}

    if "/" in dsn:
        service_part = dsn.split("/", 1)[1]
        dsn_type = "SERVICE_NAME" if service_part else "SERVICE_NAME_EMPTY"
        return {"is_valid": True, "error": None, "dsn_type": dsn_type,
                "host": host, "port": port, "service_name": service_part or None}
    elif len(parts) == 3:
        sid = parts[2]
        if not sid:
            return {"is_valid": False, "error": "SID cannot be empty when using SID format", "dsn_type": "INVALID"}
        return {"is_valid": True, "error": None, "dsn_type": "SID", "host": host, "port": port, "sid": sid}
    elif len(parts) == 2:
        return {"is_valid": True, "error": None, "dsn_type": "BASIC", "host": host, "port": port}
    else:
        return {"is_valid": False, "error": "Invalid DSN format", "dsn_type": "INVALID"}


def validate_connection_parameters(host, port, username, password, service_name) -> Optional[str]:
    """Validate Oracle connection parameters. Returns error string or None."""
    if not host or not host.strip():
        return "Oracle host cannot be empty"
    if len(host.strip()) > 255:
        return "Oracle host name is too long (max 255 characters)"
    if not isinstance(port, int):
        return "Port must be an integer"
    if port < 1 or port > 65535:
        return "Port must be between 1 and 65535"
    if not username or not username.strip():
        return "Oracle username cannot be empty"
    if len(username) > 128:
        return "Oracle username is too long (max 128 characters)"
    if password and len(password) > 256:
        return "Oracle password is too long (max 256 characters)"
    if service_name and len(service_name) > 128:
        return "Oracle service name is too long (max 128 characters)"
    return None


def create_oracle_connection(host, port, username, password, service_name=None, connection_timeout=30):
    """
    Create an Oracle database connection using oracledb in thick mode.
    Thick mode uses Oracle Instant Client libraries for Network Encryption,
    Data Integrity, and advanced Oracle Net features.
    Returns an oracledb.Connection object.
    """
    import oracledb

    # Ensure thick mode is initialized (idempotent)
    ensure_thick_mode()

    dsn = construct_oracle_dsn(host, port, service_name)
    validation = validate_oracle_dsn(dsn)
    if not validation["is_valid"]:
        raise ValueError(f"Invalid Oracle DSN: {validation['error']}")

    logger.info(f"Connecting to Oracle at {dsn} (type: {validation['dsn_type']}, thick mode)")

    try:
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        connection.autocommit = True

        # Verify connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM dual")
        cursor.fetchone()
        cursor.close()
        logger.info(f"Oracle connection verified (DSN type: {validation['dsn_type']})")
        return connection

    except oracledb.Error as e:
        raise ConnectionError(f"Oracle connection failed: {e}")
    except Exception as e:
        raise ConnectionError(f"Unexpected connection error: {e}")


# ============================================================
# SQL CLASSIFICATION & VALIDATION
# ============================================================

_READ_ONLY_KEYWORDS = {'SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN', 'WITH'}
_MODIFICATION_KEYWORDS = {'INSERT', 'UPDATE', 'DELETE', 'REPLACE', 'CREATE', 'ALTER',
                          'DROP', 'TRUNCATE', 'CALL'}


def classify_sql_command(sql: str) -> dict:
    """Classify a SQL command to determine its operation type."""
    try:
        if not sql or not sql.strip():
            return {'command_type': 'UNKNOWN', 'primary_keyword': None,
                    'is_read_only': False, 'is_modification': False,
                    'detected_operations': [], 'error': 'Empty SQL query'}

        parsed_statements = sqlparse.parse(sql.strip())
        if not parsed_statements:
            return {'command_type': 'UNKNOWN', 'primary_keyword': None,
                    'is_read_only': False, 'is_modification': False,
                    'detected_operations': [], 'error': 'Unable to parse SQL'}

        detected_operations = []
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'REPLACE', 'CREATE',
                        'ALTER', 'DROP', 'TRUNCATE', 'SHOW', 'DESCRIBE', 'EXPLAIN',
                        'WITH', 'CALL', 'GRANT', 'REVOKE']

        for statement in parsed_statements:
            if not statement.tokens:
                continue
            first_keyword = None
            for token in statement.tokens:
                if token.ttype is sqlparse.tokens.Keyword:
                    first_keyword = str(token).upper().strip()
                    break
                elif str(token).strip() and token.ttype not in (
                        sqlparse.tokens.Whitespace, sqlparse.tokens.Comment.Single,
                        sqlparse.tokens.Comment.Multiline):
                    token_str = str(token).upper().strip()
                    for kw in sql_keywords:
                        if token_str.startswith(kw):
                            first_keyword = kw
                            break
                    if first_keyword:
                        break

            if not first_keyword:
                cleaned = str(statement).strip().upper()
                for line in cleaned.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('/*') and not line.startswith('--'):
                        words = line.split()
                        if words:
                            pot = words[0]
                            if pot == 'DESC':
                                first_keyword = 'DESCRIBE'
                            elif pot in sql_keywords:
                                first_keyword = pot
                        break

            if first_keyword:
                detected_operations.append(first_keyword)

        if not detected_operations:
            return {'command_type': 'UNKNOWN', 'primary_keyword': None,
                    'is_read_only': False, 'is_modification': False,
                    'detected_operations': [], 'error': 'No SQL keywords detected'}

        primary_keyword = detected_operations[0]

        if len(detected_operations) > 1:
            all_ro = all(k.upper() in _READ_ONLY_KEYWORDS for k in detected_operations)
            any_mod = any(k.upper() in _MODIFICATION_KEYWORDS for k in detected_operations)
            if all_ro:
                return {'command_type': 'READ', 'primary_keyword': primary_keyword,
                        'is_read_only': True, 'is_modification': False,
                        'detected_operations': detected_operations, 'error': None}
            else:
                return {'command_type': 'MULTI', 'primary_keyword': primary_keyword,
                        'is_read_only': False, 'is_modification': any_mod,
                        'detected_operations': detected_operations, 'error': None}

        is_ro = primary_keyword.upper() in _READ_ONLY_KEYWORDS
        is_mod = primary_keyword.upper() in _MODIFICATION_KEYWORDS

        if is_ro:
            cmd_type = 'READ'
        elif primary_keyword in ('GRANT', 'REVOKE'):
            cmd_type = 'DCL'
            is_mod = True
        elif primary_keyword in ('CREATE', 'ALTER', 'DROP', 'TRUNCATE'):
            cmd_type = 'DDL'
            is_mod = True
        elif primary_keyword in ('INSERT', 'UPDATE', 'DELETE', 'REPLACE'):
            cmd_type = 'WRITE'
            is_mod = True
        elif is_mod:
            cmd_type = 'WRITE'
        else:
            cmd_type = 'UNKNOWN'

        return {'command_type': cmd_type, 'primary_keyword': primary_keyword,
                'is_read_only': is_ro, 'is_modification': is_mod,
                'detected_operations': detected_operations, 'error': None}

    except Exception as e:
        return {'command_type': 'UNKNOWN', 'primary_keyword': None,
                'is_read_only': False, 'is_modification': False,
                'detected_operations': [], 'error': f"Classification error: {e}"}


def validate_sql_for_read_only(sql: str) -> dict:
    """Validate that SQL contains only read-only operations."""
    classification = classify_sql_command(sql)

    if classification.get('error') and classification['command_type'] == 'UNKNOWN':
        return {'is_valid': False, 'error_message': classification['error'],
                'classification': classification}

    if classification['is_read_only']:
        return {'is_valid': True, 'error_message': None, 'classification': classification}

    pk = classification.get('primary_keyword', 'UNKNOWN')
    blocked_msg = (f"SECURITY: {pk} operations are not allowed in the read-only oracle_query tool. "
                   f"Use the oracle_execute tool for data modification operations.")
    return {'is_valid': False, 'error_message': blocked_msg, 'classification': classification}


# ============================================================
# ORACLE DATA TYPE CONVERSION
# ============================================================

def convert_oracle_value(value):
    """Convert Oracle data types to JSON-compatible types with type metadata."""
    if value is None:
        return None

    # LOB types
    if hasattr(value, 'read'):
        try:
            if hasattr(value, 'size') and value.size() == 0:
                return None
            lob_content = value.read()
            if isinstance(lob_content, bytes):
                return {"type": "BLOB", "data": base64.b64encode(lob_content).decode('ascii'),
                        "size": len(lob_content)}
            else:
                return {"type": "CLOB", "data": str(lob_content), "size": len(str(lob_content))}
        except Exception as e:
            return {"type": "LOB_ERROR", "error": f"Failed to read LOB: {e}"}

    if isinstance(value, datetime):
        if value.tzinfo is not None:
            return {"type": "TIMESTAMP_TZ", "value": value.isoformat(),
                    "timezone": str(value.tzinfo)}
        return {"type": "TIMESTAMP", "value": value.isoformat()}

    if isinstance(value, date):
        return {"type": "DATE", "value": value.isoformat()}

    if isinstance(value, time_type):
        return {"type": "TIME", "value": str(value)}

    if isinstance(value, Decimal):
        sign, digits, exponent = value.as_tuple()
        return {"type": "NUMBER", "value": str(value),
                "precision": len(digits), "scale": -exponent if exponent < 0 else 0,
                "is_integer": exponent >= 0}

    if isinstance(value, timedelta):
        return {"type": "INTERVAL_DS", "days": value.days, "seconds": value.seconds,
                "microseconds": value.microseconds, "total_seconds": value.total_seconds(),
                "iso_format": str(value)}

    if isinstance(value, bytes):
        try:
            decoded = value.decode('utf-8')
            if decoded and sum(c.isprintable() or c.isspace() for c in decoded) / len(decoded) > 0.8:
                return {"type": "RAW_TEXT", "value": decoded, "original_bytes_length": len(value)}
        except UnicodeDecodeError:
            pass
        return {"type": "RAW_BINARY", "value": base64.b64encode(value).decode('ascii'),
                "bytes_length": len(value)}

    if isinstance(value, bool):
        return {"type": "BOOLEAN", "value": value}

    if isinstance(value, int):
        return {"type": "NUMBER_INT", "value": value, "possible_boolean": value in (0, 1)}

    if isinstance(value, float):
        if math.isnan(value):
            return {"type": "NUMBER_FLOAT", "value": None, "special": "NaN"}
        if math.isinf(value):
            return {"type": "NUMBER_FLOAT", "value": None,
                    "special": "Infinity" if value > 0 else "-Infinity"}
        return {"type": "NUMBER_FLOAT", "value": value}

    if isinstance(value, str):
        return {"type": "STRING", "value": value, "length": len(value)}

    return {"type": f"UNKNOWN_{type(value).__name__}", "value": str(value),
            "python_type": type(value).__name__}


def convert_oracle_value_simple(value):
    """Convert Oracle data types to simple JSON-compatible values (no type metadata)."""
    if value is None:
        return None
    if hasattr(value, 'read'):
        try:
            content = value.read()
            return content.decode('utf-8') if isinstance(content, bytes) else str(content)
        except Exception:
            return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, time_type):
        return str(value)
    if isinstance(value, Decimal):
        return float(value) if value != value.to_integral_value() else int(value)
    if isinstance(value, timedelta):
        return value.total_seconds()
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return base64.b64encode(value).decode('ascii')
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, str)):
        return value
    return str(value)


def convert_oracle_row(row_dict: dict, detailed_types: bool = True) -> dict:
    """Convert all values in an Oracle result row dictionary."""
    if not row_dict:
        return row_dict
    fn = convert_oracle_value if detailed_types else convert_oracle_value_simple
    return {col: fn(val) for col, val in row_dict.items()}


# ============================================================
# CURSOR RESULT HANDLING
# ============================================================

def detect_oracle_column_types(cursor) -> dict:
    """Extract column type information from Oracle cursor description."""
    if not cursor.description:
        return {}
    column_types = {}
    for desc in cursor.description:
        name = desc[0]
        type_code = desc[1] if len(desc) > 1 else None
        precision = desc[4] if len(desc) > 4 else None
        scale = desc[5] if len(desc) > 5 else None
        column_types[name] = {
            "type_code": type_code, "precision": precision, "scale": scale,
            "oracle_type_name": get_oracle_type_name(type_code, precision, scale)
        }
    return column_types


_ORACLE_TYPE_MAP = {
    1: "VARCHAR2", 2: "NUMBER", 8: "LONG", 11: "ROWID", 12: "DATE",
    23: "RAW", 24: "LONG RAW", 96: "CHAR", 112: "CLOB", 113: "BLOB",
    114: "BFILE", 180: "TIMESTAMP", 181: "TIMESTAMP WITH TIME ZONE",
    182: "INTERVAL YEAR TO MONTH", 183: "INTERVAL DAY TO SECOND",
    231: "TIMESTAMP WITH LOCAL TIME ZONE"
}


def get_oracle_type_name(type_code, precision=None, scale=None) -> str:
    """Convert Oracle type code to human-readable name."""
    base = _ORACLE_TYPE_MAP.get(type_code, f"UNKNOWN_TYPE_{type_code}")
    if type_code == 2 and precision is not None:
        if scale is not None and scale > 0:
            return f"NUMBER({precision},{scale})"
        elif precision > 0:
            return f"NUMBER({precision})"
        return "NUMBER"
    return base


def handle_oracle_cursor_conversion(cursor, use_detailed_types: bool = True) -> dict:
    """Convert Oracle cursor results with comprehensive type handling."""
    try:
        column_types = detect_oracle_column_types(cursor)
        column_names = [d[0] for d in cursor.description] if cursor.description else []
        raw = cursor.fetchall()
        rows = []
        for row_tuple in raw:
            if column_names and len(row_tuple) == len(column_names):
                row_dict = dict(zip(column_names, row_tuple))
            else:
                row_dict = {f"col_{i}": v for i, v in enumerate(row_tuple)}
            rows.append(convert_oracle_row(row_dict, detailed_types=use_detailed_types))
        return {"rows": rows, "row_count": len(rows), "columns": column_names,
                "column_types": column_types,
                "conversion_mode": "detailed" if use_detailed_types else "simple"}
    except Exception as e:
        try:
            raw = cursor.fetchall()
            column_names = [d[0] for d in cursor.description] if cursor.description else []
            rows = []
            for row_tuple in raw:
                if column_names and len(row_tuple) == len(column_names):
                    rd = dict(zip(column_names, row_tuple))
                else:
                    rd = {f"col_{i}": v for i, v in enumerate(row_tuple)}
                rows.append(convert_oracle_row(rd, detailed_types=False))
            return {"rows": rows, "row_count": len(rows), "columns": column_names,
                    "conversion_error": f"Advanced conversion failed: {e}",
                    "conversion_mode": "fallback_simple"}
        except Exception as fb:
            return {"rows": [], "row_count": 0, "columns": [],
                    "conversion_error": f"All conversion attempts failed: {fb}",
                    "conversion_mode": "failed"}


def convert_oracle_to_mysql_format(cursor) -> dict:
    """Convert Oracle cursor results to simple list-of-dicts format."""
    try:
        column_names = [d[0] for d in cursor.description] if cursor.description else []
        raw = cursor.fetchall()
        rows = []
        for row_tuple in raw:
            rd = {}
            for i, val in enumerate(row_tuple):
                col = column_names[i] if i < len(column_names) else f"col_{i}"
                rd[col] = convert_oracle_value_simple(val)
            rows.append(rd)
        return {"rows": rows, "row_count": len(rows), "columns": column_names}
    except Exception as e:
        return {"rows": [], "row_count": 0, "columns": [],
                "conversion_error": f"Conversion failed: {e}"}


# ============================================================
# ERROR HANDLING
# ============================================================

def categorize_oracle_error(error) -> Tuple[str, str]:
    """Categorize Oracle errors and return (category, user_message)."""
    import oracledb

    error_msg = str(error).lower()
    oracle_error_code = getattr(error, 'code', None)
    if oracle_error_code is None:
        m = re.search(r'ora-(\d+)', error_msg)
        if m:
            oracle_error_code = int(m.group(1))

    # Connection errors
    code_map = {
        12541: ("CONNECTION", "Oracle TNS: No listener. The Oracle service is not running or accessible."),
        12514: ("CONNECTION", "Oracle TNS: Listener does not know of the service. Check service name."),
        12545: ("CONNECTION", "Oracle TNS: Host or service does not exist. Verify hostname and service."),
        12170: ("TIMEOUT", "Oracle TNS: Connection timeout. Check network and firewall."),
        12504: ("CONNECTION", "Oracle TNS: Service name not provided to listener."),
        12505: ("CONNECTION", "Oracle TNS: Unknown SID. Check SID or use service name."),
        12154: ("CONNECTION", "Oracle TNS: Could not resolve connect identifier."),
        1017: ("AUTHENTICATION", "Oracle: Invalid username or password."),
        28000: ("AUTHENTICATION", "Oracle: Account is locked."),
        28001: ("AUTHENTICATION", "Oracle: Password has expired."),
        900: ("SYNTAX", "Oracle ORA-00900: Invalid SQL statement."),
        942: ("SCHEMA", "Oracle ORA-00942: Table or view does not exist."),
        904: ("SCHEMA", "Oracle ORA-00904: Invalid column name."),
        936: ("SYNTAX", "Oracle ORA-00936: Missing expression."),
        933: ("SYNTAX", "Oracle ORA-00933: SQL command not properly ended."),
        1722: ("DATA", "Oracle ORA-01722: Invalid number format."),
        1: ("DATA", "Oracle ORA-00001: Unique constraint violated."),
        2291: ("DATA", "Oracle ORA-02291: Foreign key constraint violated."),
        2292: ("DATA", "Oracle ORA-02292: Cannot delete parent record - child records exist."),
        12899: ("DATA", "Oracle ORA-12899: Value too large for column."),
        1031: ("PERMISSION", "Oracle ORA-01031: Insufficient privileges."),
        600: ("SERVER", "Oracle ORA-00600: Internal error. Contact DBA."),
        7445: ("SERVER", "Oracle ORA-07445: Exception encountered. Contact DBA."),
    }

    if oracle_error_code and oracle_error_code in code_map:
        return code_map[oracle_error_code]

    if isinstance(error, oracledb.InterfaceError) or "connection refused" in error_msg:
        return "CONNECTION", "Cannot connect to Oracle server. Check if the service is running."
    if "timeout" in error_msg or "timed out" in error_msg:
        return "TIMEOUT", "Connection to Oracle server timed out."
    if "access denied" in error_msg:
        return "AUTHENTICATION", "Oracle authentication failed."

    if oracle_error_code:
        return "ORACLE_ERROR", f"Oracle ORA-{oracle_error_code:05d}: {error}"
    return "UNKNOWN", f"Oracle error: {error}"


# ============================================================
# PARAMETER VALIDATION
# ============================================================

def count_sql_placeholders(sql: str) -> int:
    """Count ? placeholders in SQL, excluding those inside quotes."""
    in_sq = False
    in_dq = False
    count = 0
    i = 0
    while i < len(sql):
        ch = sql[i]
        if i < len(sql) - 1 and ch == '\\':
            i += 2
            continue
        if ch == "'" and not in_dq:
            in_sq = not in_sq
        elif ch == '"' and not in_sq:
            in_dq = not in_dq
        elif ch == '?' and not in_sq and not in_dq:
            count += 1
        i += 1
    return count


def convert_query_parameter(value, position):
    """Convert and validate a single query parameter for Oracle binding."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, int):
        limit = 10**38 - 1
        if value < -limit or value > limit:
            raise ValueError(f"Parameter {position}: Integer exceeds Oracle NUMBER range (±10^38-1)")
        return value
    if isinstance(value, float):
        if math.isnan(value):
            raise ValueError(f"Parameter {position}: NaN not supported in Oracle NUMBER")
        if math.isinf(value):
            raise ValueError(f"Parameter {position}: Infinity not supported in Oracle NUMBER")
        return value
    if isinstance(value, Decimal):
        if len(value.as_tuple().digits) > 38:
            raise ValueError(f"Parameter {position}: Decimal precision exceeds Oracle limit (38)")
        return value
    if isinstance(value, (datetime, date)):
        return value
    if isinstance(value, time_type):
        return value.isoformat()
    if isinstance(value, timedelta):
        return value
    if isinstance(value, bytes):
        return value
    if isinstance(value, dict):
        import json
        return json.dumps(value, default=str, ensure_ascii=False)
    if hasattr(value, 'hex') and hasattr(value, 'version'):  # UUID
        return str(value)
    if hasattr(value, 'value') and hasattr(value, 'name'):  # Enum
        return convert_query_parameter(value.value, position)

    raise ValueError(f"Parameter {position}: Unsupported type: {type(value).__name__}")


def validate_and_convert_parameters(sql: str, vals) -> Tuple[Any, Optional[str]]:
    """Validate and convert query parameters for Oracle binding."""
    if vals is None:
        vals = []

    has_positional = '?' in sql
    named_params_in_sql = re.findall(r':(\w+)', sql)
    has_named = len(named_params_in_sql) > 0

    if has_positional and has_named:
        return None, "Cannot mix positional (?) and named (:name) parameters"

    # Bulk (list of dicts)
    if isinstance(vals, list) and vals and isinstance(vals[0], dict):
        return _validate_bulk(sql, vals)
    # Named (dict)
    if isinstance(vals, dict):
        if not has_named:
            return None, "Named parameters provided but no :name bind variables found"
        return _validate_named(sql, vals)
    # Positional (list)
    if isinstance(vals, list):
        if has_named:
            return None, "Positional parameters provided but named :name bind variables found"
        return _validate_positional(sql, vals)

    return None, f"Invalid parameter format: expected list or dict, got {type(vals).__name__}"


def _validate_positional(sql, vals):
    pc = count_sql_placeholders(sql)
    if pc != len(vals):
        return None, f"Parameter count mismatch: SQL has {pc} placeholders but {len(vals)} provided"
    converted = []
    for i, p in enumerate(vals):
        try:
            converted.append(convert_query_parameter(p, i))
        except ValueError as e:
            return None, f"Parameter {i+1} error: {e}"
    return converted, None


def _validate_named(sql, vals):
    named = set(re.findall(r':(\w+)', sql))
    missing = named - set(vals.keys())
    if missing:
        return None, f"Missing required parameters: {', '.join(sorted(missing))}"
    converted = {}
    for name in named:
        if name in vals:
            try:
                converted[name] = convert_query_parameter(vals[name], f":{name}")
            except ValueError as e:
                return None, f"Parameter ':{name}' error: {e}"
    return converted, None


def _validate_bulk(sql, vals):
    if not vals:
        return [], None
    if not isinstance(vals[0], dict):
        return None, f"Bulk params must be list of dicts, row 0 is {type(vals[0]).__name__}"
    expected = set(vals[0].keys())
    converted_rows = []
    for idx, row in enumerate(vals):
        if not isinstance(row, dict):
            return None, f"Row {idx} must be dict, got {type(row).__name__}"
        if set(row.keys()) != expected:
            return None, f"Row {idx} parameter mismatch vs row 0"
        cr = {}
        for name, value in row.items():
            try:
                cr[name] = convert_query_parameter(value, f"row {idx} :{name}")
            except ValueError as e:
                return None, f"Row {idx} ':{name}' error: {e}"
        converted_rows.append(cr)
    return converted_rows, None
