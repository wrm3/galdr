"""
Database client with connection pooling for PostgreSQL (galdr).
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from typing import Generator, Optional
import logging

logger = logging.getLogger(__name__)


class _PoolConnection:
    """Wraps a psycopg2 connection so `with db.get_connection() as conn:` returns it to the pool."""

    def __init__(self, pool: SimpleConnectionPool):
        self._pool = pool
        self._conn = pool.getconn()

    def __enter__(self):
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._conn.rollback()
        self._pool.putconn(self._conn)
        return False

    def cursor(self, *args, **kwargs):
        return self._conn.cursor(*args, **kwargs)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()


class RAGDatabase:
    """
    Database client with connection pooling for PostgreSQL.

    Uses SimpleConnectionPool for efficient connection management.
    All queries return RealDictCursor results for easy JSON serialization.
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize database connection pool.

        Args:
            config: Configuration dictionary with PostgreSQL credentials.
                   If None, loads from environment variables.
        """
        self.config = config or {}
        self.pool: Optional[SimpleConnectionPool] = None
        self._init_pool()

    def _build_connection_string(self) -> str:
        """Build PostgreSQL connection string from config or environment."""
        conn_str = self.config.get('postgres_connection_string') or os.getenv('POSTGRES_CONNECTION_STRING')
        if conn_str:
            return conn_str

        host = self.config.get('postgres_host') or os.getenv('POSTGRES_HOST')
        port = self.config.get('postgres_port') or os.getenv('POSTGRES_PORT', '5432')
        database = self.config.get('postgres_db') or self.config.get('postgres_database') or os.getenv('POSTGRES_DB') or os.getenv('POSTGRES_DATABASE', 'knowledge_base')
        user = self.config.get('postgres_user') or os.getenv('POSTGRES_USER', 'postgres')
        password = self.config.get('postgres_password') or os.getenv('POSTGRES_PASSWORD')

        if not all([host, password]):
            raise ValueError("Missing required database connection parameters (host, password)")

        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def _init_pool(self):
        """Initialize the connection pool."""
        try:
            dsn = self._build_connection_string()
            self.pool = SimpleConnectionPool(
                minconn=2,
                maxconn=20,
                dsn=dsn,
                connect_timeout=10,
                options='-c statement_timeout=30000'  # 30 second query timeout
            )
            logger.info("Database connection pool initialized successfully")
        except psycopg2.Error as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            raise

    def get_connection(self):
        """Get a pool-aware connection context manager. Always use with `with`."""
        if not self.pool:
            raise RuntimeError("Connection pool not initialized")
        return _PoolConnection(self.pool)

    def release_connection(self, conn):
        """Return a connection to the pool."""
        if self.pool:
            raw = conn._conn if isinstance(conn, _PoolConnection) else conn
            self.pool.putconn(raw)

    @contextmanager
    def get_cursor(self, cursor_factory=RealDictCursor) -> Generator:
        """
        Context manager for database cursor with automatic cleanup.

        Args:
            cursor_factory: Cursor factory class (default: RealDictCursor)

        Yields:
            Database cursor
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=cursor_factory) as cursor:
                yield cursor
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            self.release_connection(conn)

    def execute_query(self, sql: str, params: tuple = None) -> list:
        """
        Execute a query and return all results.

        Args:
            sql: SQL query string
            params: Query parameters (optional)

        Returns:
            List of dictionaries (RealDictCursor rows)
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute_one(self, sql: str, params: tuple = None) -> Optional[dict]:
        """
        Execute a query and return a single result.

        Args:
            sql: SQL query string
            params: Query parameters (optional)

        Returns:
            Single dictionary or None
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def test_connection(self) -> bool:
        """
        Test database connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = self.execute_one("SELECT 1 as test")
            return result is not None and result.get('test') == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def close(self):
        """Close all connections in the pool."""
        if self.pool:
            self.pool.closeall()
            self.pool = None
            logger.info("Database connection pool closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes pool."""
        self.close()
        return False
