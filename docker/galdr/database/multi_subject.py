"""
Multi-Subject Database Client.

Provides a database interface that can dynamically switch between
different subject databases based on the subject parameter.
"""
import logging
from contextlib import contextmanager
from typing import Optional, Generator, Any

from psycopg2.extras import RealDictCursor

from ..subjects import SubjectManager, Subject

logger = logging.getLogger(__name__)


class MultiSubjectDatabase:
    """
    Database client that supports multiple subject databases.

    Wraps SubjectManager and provides a RAGDatabase-compatible interface
    that routes queries to the appropriate subject database.

    Usage:
        db = MultiSubjectDatabase(subject_manager)

        # Use default subject
        result = db.execute_query("SELECT * FROM sources")

        # Use specific subject
        result = db.execute_query("SELECT * FROM sources", subject='ai_coding')

        # Or use context manager style
        with db.for_subject('ai_coding') as ai_db:
            result = ai_db.execute_query("SELECT * FROM sources")
    """

    def __init__(self, subject_manager: SubjectManager):
        """
        Initialize MultiSubjectDatabase.

        Args:
            subject_manager: SubjectManager instance for connection management
        """
        self.subject_manager = subject_manager
        self._current_subject: Optional[str] = None
        logger.info("MultiSubjectDatabase initialized")

    def _get_connection(self, subject: Optional[str] = None):
        """Get database connection for a subject."""
        subject_id = subject or self._current_subject
        return self.subject_manager.get_connection(subject_id)

    @contextmanager
    def for_subject(self, subject: str) -> Generator['MultiSubjectDatabase', None, None]:
        """
        Context manager for operations on a specific subject.

        Args:
            subject: Subject ID or alias

        Yields:
            Self with current subject set
        """
        old_subject = self._current_subject
        self._current_subject = subject
        try:
            yield self
        finally:
            self._current_subject = old_subject

    @contextmanager
    def get_cursor(
        self,
        cursor_factory=RealDictCursor,
        subject: Optional[str] = None
    ) -> Generator:
        """
        Context manager for database cursor with automatic cleanup.

        Args:
            cursor_factory: Cursor factory class (default: RealDictCursor)
            subject: Subject ID or alias (uses current/default if None)

        Yields:
            Database cursor
        """
        conn = self._get_connection(subject)
        try:
            with conn.cursor(cursor_factory=cursor_factory) as cursor:
                yield cursor
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise

    def execute_query(
        self,
        sql: str,
        params: tuple = None,
        subject: Optional[str] = None
    ) -> list:
        """
        Execute a query and return all results.

        Args:
            sql: SQL query string
            params: Query parameters (optional)
            subject: Subject ID or alias (uses current/default if None)

        Returns:
            List of dictionaries (RealDictCursor rows)
        """
        with self.get_cursor(subject=subject) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute_one(
        self,
        sql: str,
        params: tuple = None,
        subject: Optional[str] = None
    ) -> Optional[dict]:
        """
        Execute a query and return a single result.

        Args:
            sql: SQL query string
            params: Query parameters (optional)
            subject: Subject ID or alias (uses current/default if None)

        Returns:
            Single dictionary or None
        """
        with self.get_cursor(subject=subject) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def test_connection(self, subject: Optional[str] = None) -> bool:
        """
        Test database connection for a subject.

        Args:
            subject: Subject ID or alias (uses current/default if None)

        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = self.execute_one("SELECT 1 as test", subject=subject)
            return result is not None and result.get('test') == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def close(self):
        """Close all database connections."""
        self.subject_manager.close_all_connections()
        logger.info("MultiSubjectDatabase connections closed")

    def get_current_subject(self) -> Optional[Subject]:
        """Get the current or default subject."""
        if self._current_subject:
            return self.subject_manager.get_subject(self._current_subject)
        return self.subject_manager.get_default_subject()

    def list_subjects(self):
        """Get all available subjects."""
        return self.subject_manager.list_subjects()

    def resolve_subject(self, identifier: Optional[str] = None) -> Subject:
        """Resolve a subject identifier to a Subject object."""
        return self.subject_manager.resolve_subject(identifier or self._current_subject)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes connections."""
        self.close()
        return False


class SubjectAwareDBWrapper:
    """
    Wrapper that adds a fixed subject to a MultiSubjectDatabase.

    This allows passing a subject-specific database to tools
    that expect the standard db interface.
    """

    def __init__(self, multi_db: MultiSubjectDatabase, subject: str):
        """
        Initialize wrapper.

        Args:
            multi_db: MultiSubjectDatabase instance
            subject: Subject ID or alias to use for all operations
        """
        self._db = multi_db
        self._subject = subject

    @contextmanager
    def get_cursor(self, cursor_factory=RealDictCursor) -> Generator:
        """Get cursor for the wrapped subject."""
        with self._db.get_cursor(cursor_factory=cursor_factory, subject=self._subject) as cursor:
            yield cursor

    def execute_query(self, sql: str, params: tuple = None) -> list:
        """Execute query on the wrapped subject."""
        return self._db.execute_query(sql, params, subject=self._subject)

    def execute_one(self, sql: str, params: tuple = None) -> Optional[dict]:
        """Execute single-result query on the wrapped subject."""
        return self._db.execute_one(sql, params, subject=self._subject)

    def test_connection(self) -> bool:
        """Test connection for the wrapped subject."""
        return self._db.test_connection(subject=self._subject)

    def close(self):
        """Close is a no-op for wrapper (main db manages connections)."""
        pass

    @property
    def subject(self) -> str:
        """Get the wrapped subject identifier."""
        return self._subject
