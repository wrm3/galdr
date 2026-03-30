"""
Oracle Read-Only Query Tool Plugin

Execute read-only SQL queries (SELECT, SHOW, DESCRIBE, EXPLAIN) on an Oracle database.
Blocks all data-modification operations.

Ported from galdr_oracle standalone MCP server.
"""
import logging
from typing import Optional, List, Any

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "oracle_query"

TOOL_DESCRIPTION = (
    "Execute read-only SQL queries on an Oracle database. "
    "Supports SELECT, SHOW, DESCRIBE, EXPLAIN, and WITH (CTEs). "
    "Blocks INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, and other modification operations. "
    "Supports parameterized queries with ? placeholders or :name bind variables. "
    "All connection parameters (host, username, password, service_name) MUST be supplied per call. "
    "Returns rows, column names, column types, and row count."
)

TOOL_PARAMS = {
    "sql": "Oracle SQL query (SELECT, SHOW, DESCRIBE, EXPLAIN only)",
    "host": "Oracle hostname (REQUIRED)",
    "port": "Oracle port (default 1521)",
    "username": "Oracle username (REQUIRED)",
    "password": "Oracle password (REQUIRED)",
    "service_name": "Oracle service name (REQUIRED)",
    "vals": "Query parameters as list (positional) or dict (named) (optional)",
}

logger = logging.getLogger(__name__)

# ============================================================
# PLUGIN IMPLEMENTATION
# ============================================================

_config = None


def setup(context: dict):
    """Called once during plugin loading."""
    global _config
    _config = context.get('config', {})


async def execute(
    sql: str,
    host: str = None,
    port: int = None,
    username: str = None,
    password: str = None,
    service_name: str = None,
    vals: Optional[List[Any]] = None,
    context: dict = None
) -> dict:
    """Execute a read-only Oracle SQL query."""
    from galdr.tools.oracle_utils import (
        get_oracle_config, validate_connection_parameters,
        validate_sql_for_read_only, validate_and_convert_parameters,
        create_oracle_connection, handle_oracle_cursor_conversion,
        categorize_oracle_error
    )

    # All connection params supplied per-call (no env defaults)
    port = port or 1521

    response = {"success": False, "results": None, "error": None}
    connection = None
    cursor = None

    try:
        # Validate input
        if not sql or not sql.strip():
            response["error"] = "SQL query cannot be empty"
            response["error_category"] = "VALIDATION"
            return response

        if len(sql) > 1048576:
            response["error"] = "SQL query is too long (max 1MB)"
            response["error_category"] = "VALIDATION"
            return response

        # Security: read-only validation
        validation = validate_sql_for_read_only(sql)
        if not validation['is_valid']:
            response["error"] = validation['error_message']
            response["error_category"] = "SECURITY"
            return response

        # Validate connection params
        param_err = validate_connection_parameters(host, port, username, password, service_name)
        if param_err:
            response["error"] = param_err
            response["error_category"] = "VALIDATION"
            return response

        # Validate query parameters
        if vals is not None or '?' in sql:
            converted, param_err = validate_and_convert_parameters(sql, vals)
            if param_err:
                response["error"] = param_err
                response["error_category"] = "PARAMETER"
                return response
            vals = converted

        # Connect
        try:
            connection = create_oracle_connection(host, port, username, password, service_name)
        except (ValueError, ConnectionError) as e:
            response["error"] = str(e)
            response["error_category"] = "CONNECTION"
            return response

        cursor = connection.cursor()

        # Execute
        if vals:
            cursor.execute(sql, vals)
        else:
            cursor.execute(sql)

        # Convert results
        conversion = handle_oracle_cursor_conversion(cursor, use_detailed_types=True)
        response["results"] = {
            "rows": conversion["rows"],
            "row_count": conversion["row_count"],
            "columns": conversion["columns"],
            "column_types": conversion.get("column_types", {}),
            "conversion_mode": conversion.get("conversion_mode", "detailed"),
            "tool_used": "oracle_query (read-only)"
        }
        if "conversion_error" in conversion:
            response["results"]["conversion_warning"] = conversion["conversion_error"]

        response["success"] = True
        logger.info(f"oracle_query returned {conversion['row_count']} rows")

    except Exception as e:
        try:
            import oracledb
            if isinstance(e, oracledb.Error):
                cat, msg = categorize_oracle_error(e)
                response["error"] = msg
                response["error_category"] = cat
            else:
                raise
        except ImportError:
            raise
        except Exception:
            response["error"] = f"Unexpected error: {type(e).__name__}: {e}"
            response["error_category"] = "UNKNOWN"

    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if connection:
            try:
                connection.close()
            except Exception:
                pass

    return response
