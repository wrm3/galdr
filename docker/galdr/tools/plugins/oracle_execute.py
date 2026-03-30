"""
Oracle Execute (Write) Tool Plugin

Execute any SQL operation on an Oracle database including INSERT, UPDATE, DELETE,
CREATE, ALTER, DROP, and PL/SQL blocks.

WARNING: This tool can modify, create, or delete data and database structures.

Ported from galdr_oracle standalone MCP server.
"""
import logging
from typing import Optional, List, Any

# ============================================================
# PLUGIN METADATA (Required)
# ============================================================

TOOL_NAME = "oracle_execute"

TOOL_DESCRIPTION = (
    "Execute any SQL on an Oracle database including data modification (INSERT, UPDATE, DELETE), "
    "DDL (CREATE, ALTER, DROP, TRUNCATE), DCL (GRANT, REVOKE), and PL/SQL blocks. "
    "WARNING: This tool can modify data and schema. Use with caution. "
    "Supports parameterized queries with ? placeholders, :name bind variables, and bulk operations. "
    "All connection parameters (host, username, password, service_name) MUST be supplied per call. "
    "Returns rows_affected for DML/DDL, or result set for SELECT queries."
)

TOOL_PARAMS = {
    "sql": "Oracle SQL statement (any operation allowed)",
    "host": "Oracle hostname (REQUIRED)",
    "port": "Oracle port (default 1521)",
    "username": "Oracle username (REQUIRED)",
    "password": "Oracle password (REQUIRED)",
    "service_name": "Oracle service name (REQUIRED)",
    "vals": "Parameters: list (positional), dict (named), or list-of-dicts (bulk) (optional)",
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
    """Execute an Oracle SQL statement (modification-enabled)."""
    from galdr.tools.oracle_utils import (
        get_oracle_config, validate_connection_parameters,
        classify_sql_command, validate_and_convert_parameters,
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
            response["error"] = "SQL statement cannot be empty"
            response["error_category"] = "VALIDATION"
            return response

        if len(sql) > 1048576:
            response["error"] = "SQL statement is too long (max 1MB)"
            response["error_category"] = "VALIDATION"
            return response

        # Classify for logging
        classification = classify_sql_command(sql)
        query_type = classification.get('primary_keyword', 'UNKNOWN')
        logger.info(f"oracle_execute: {classification['command_type']} - {query_type}")

        # Validate connection params
        param_err = validate_connection_parameters(host, port, username, password, service_name)
        if param_err:
            response["error"] = param_err
            response["error_category"] = "VALIDATION"
            return response

        # Validate query parameters
        if vals is not None or '?' in sql or ':' in sql:
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
            if isinstance(vals, list) and vals and isinstance(vals[0], dict):
                logger.info(f"Executing bulk operation with {len(vals)} rows")
                cursor.executemany(sql, vals)
            else:
                cursor.execute(sql, vals)
        else:
            cursor.execute(sql)

        # Format results
        if query_type in ('SELECT', 'WITH') or (
                query_type == 'UNKNOWN' and sql.strip().upper().startswith('SELECT')):
            try:
                conversion = handle_oracle_cursor_conversion(cursor, use_detailed_types=True)
                response["results"] = {
                    "query_type": "SELECT",
                    "rows": conversion["rows"],
                    "row_count": conversion["row_count"],
                    "columns": conversion["columns"],
                    "column_types": conversion.get("column_types", {}),
                    "tool_used": "oracle_execute (modification-enabled)"
                }
            except Exception:
                response["results"] = {
                    "query_type": "SELECT",
                    "rows_affected": cursor.rowcount,
                    "message": "Query executed (result conversion failed)",
                    "tool_used": "oracle_execute (modification-enabled)"
                }
        else:
            rows_affected = cursor.rowcount if cursor.rowcount >= 0 else 0
            response["results"] = {
                "query_type": query_type,
                "operation_type": classification.get('command_type', 'UNKNOWN'),
                "rows_affected": rows_affected,
                "message": f"{query_type} operation completed successfully",
                "tool_used": "oracle_execute (modification-enabled)"
            }
            logger.info(f"oracle_execute {query_type} affected {rows_affected} rows")

        response["success"] = True

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
