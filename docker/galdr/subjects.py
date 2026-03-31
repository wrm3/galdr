"""
Subject Manager for Multi-Database RAG System.

Manages different subject databases (work_knowledge, ai_coding, etc.)
allowing content to be organized into separate knowledge bases.
"""
import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


@dataclass
class Subject:
    """Represents a subject (knowledge domain) with its database configuration."""
    id: str
    display_name: str
    description: str
    database: str
    aliases: List[str] = field(default_factory=list)
    is_default: bool = False

    def matches(self, query: str) -> bool:
        """Check if a query string matches this subject's id or aliases."""
        query_lower = query.lower().strip()
        if query_lower == self.id.lower():
            return True
        return any(alias.lower() == query_lower for alias in self.aliases)


class SubjectManager:
    """
    Manages multiple subject databases for the RAG system.

    Provides:
    - Subject lookup by ID or alias
    - Database connection management per subject
    - Subject CRUD operations
    - Persistence to subjects.json
    """

    CONFIG_FILE = "subjects.json"

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize SubjectManager.

        Args:
            config_path: Path to subjects.json. If None, uses default location
                        (same directory as this module).
        """
        self.config_path = config_path or Path(__file__).parent / self.CONFIG_FILE
        self._subjects: Dict[str, Subject] = {}
        self._connection_config: Dict[str, Any] = {}
        self._connections: Dict[str, Any] = {}  # Cache for database connections

        self._load_config()
        logger.info(f"SubjectManager initialized with {len(self._subjects)} subjects")

    def _load_config(self) -> None:
        """Load subjects configuration from JSON file."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            self._create_default_config()
            return

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Load connection configuration
            self._connection_config = data.get('connection', {})

            # Load subjects
            subjects_data = data.get('subjects', {})
            for subject_id, subject_info in subjects_data.items():
                self._subjects[subject_id] = Subject(
                    id=subject_id,
                    display_name=subject_info.get('display_name', subject_id),
                    description=subject_info.get('description', ''),
                    database=subject_info.get('database', f'rag_{subject_id}'),
                    aliases=subject_info.get('aliases', []),
                    is_default=subject_info.get('is_default', False)
                )

            logger.info(f"Loaded {len(self._subjects)} subjects from {self.config_path}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse subjects.json: {e}")
            raise ValueError(f"Invalid subjects.json: {e}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def _create_default_config(self) -> None:
        """Create a default configuration file."""
        default_config = {
            "subjects": {
                "work_knowledge": {
                    "display_name": "Work Knowledge",
                    "description": "Work-related documents, processes, and standards",
                    "database": os.getenv("POSTGRES_DB", "knowledge_base"),
                    "aliases": ["work", "wk", "docs"],
                    "is_default": True
                }
            },
            "connection": {
                "host": os.getenv("POSTGRES_HOST", "localhost"),
                "port": int(os.getenv("POSTGRES_PORT", "5432")),
                "user": os.getenv("POSTGRES_USER", "knowledge_base"),
                "password": os.getenv("POSTGRES_PASSWORD", "knowledge_base")
            }
        }

        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)

        # Load the default config
        self._connection_config = default_config['connection']
        for subject_id, subject_info in default_config['subjects'].items():
            self._subjects[subject_id] = Subject(
                id=subject_id,
                display_name=subject_info['display_name'],
                description=subject_info['description'],
                database=subject_info['database'],
                aliases=subject_info.get('aliases', []),
                is_default=subject_info.get('is_default', False)
            )

        logger.info(f"Created default config at {self.config_path}")

    def _save_config(self) -> None:
        """Save current configuration to JSON file."""
        subjects_data = {}
        for subject_id, subject in self._subjects.items():
            subject_dict = {
                'display_name': subject.display_name,
                'description': subject.description,
                'database': subject.database,
                'aliases': subject.aliases
            }
            if subject.is_default:
                subject_dict['is_default'] = True
            subjects_data[subject_id] = subject_dict

        config = {
            'subjects': subjects_data,
            'connection': self._connection_config
        }

        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)

        logger.info(f"Saved config to {self.config_path}")

    # ========================================
    # Subject Query Methods
    # ========================================

    def list_subjects(self) -> List[Subject]:
        """Get all available subjects."""
        return list(self._subjects.values())

    def get_subject(self, identifier: str) -> Optional[Subject]:
        """Get a subject by ID or alias."""
        if identifier in self._subjects:
            return self._subjects[identifier]

        for subject in self._subjects.values():
            if subject.matches(identifier):
                return subject

        return None

    def get_default_subject(self) -> Optional[Subject]:
        """Get the default subject."""
        for subject in self._subjects.values():
            if subject.is_default:
                return subject

        if self._subjects:
            return next(iter(self._subjects.values()))

        return None

    def resolve_subject(self, identifier: Optional[str] = None) -> Subject:
        """Resolve a subject identifier to a Subject object."""
        if identifier:
            subject = self.get_subject(identifier)
            if subject:
                return subject
            logger.warning(f"Subject '{identifier}' not found, using default")

        default = self.get_default_subject()
        if not default:
            raise ValueError("No subjects configured")

        return default

    # ========================================
    # Subject CRUD Methods
    # ========================================

    def create_subject(
        self,
        subject_id: str,
        display_name: str,
        description: str = "",
        aliases: Optional[List[str]] = None,
        is_default: bool = False,
        create_database: bool = True
    ) -> Subject:
        """Create a new subject and optionally its database."""
        if subject_id in self._subjects:
            raise ValueError(f"Subject '{subject_id}' already exists")

        database_name = f"rag_{subject_id}"

        subject = Subject(
            id=subject_id,
            display_name=display_name,
            description=description,
            database=database_name,
            aliases=aliases or [],
            is_default=is_default
        )

        if is_default:
            for s in self._subjects.values():
                s.is_default = False

        if create_database:
            self._create_database(database_name)

        self._subjects[subject_id] = subject
        self._save_config()

        logger.info(f"Created subject: {subject_id} (database: {database_name})")
        return subject

    def delete_subject(self, subject_id: str, drop_database: bool = False) -> bool:
        """Delete a subject from configuration."""
        if subject_id not in self._subjects:
            return False

        subject = self._subjects[subject_id]

        if subject_id in self._connections:
            try:
                self._connections[subject_id].close()
            except Exception:
                pass
            del self._connections[subject_id]

        if drop_database:
            self._drop_database(subject.database)

        del self._subjects[subject_id]
        self._save_config()

        logger.info(f"Deleted subject: {subject_id}")
        return True

    def update_subject(
        self,
        subject_id: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        is_default: Optional[bool] = None
    ) -> Optional[Subject]:
        """Update an existing subject."""
        if subject_id not in self._subjects:
            return None

        subject = self._subjects[subject_id]

        if display_name is not None:
            subject.display_name = display_name
        if description is not None:
            subject.description = description
        if aliases is not None:
            subject.aliases = aliases
        if is_default is not None:
            if is_default:
                for s in self._subjects.values():
                    s.is_default = False
            subject.is_default = is_default

        self._save_config()
        logger.info(f"Updated subject: {subject_id}")
        return subject

    # ========================================
    # Database Connection Methods
    # ========================================

    def get_connection_config(self, subject: Optional[Subject] = None) -> Dict[str, Any]:
        """Get database connection configuration for a subject."""
        if subject is None:
            subject = self.get_default_subject()

        return {
            'host': self._connection_config.get('host') or os.getenv('POSTGRES_HOST', 'localhost'),
            'port': self._connection_config.get('port') or int(os.getenv('POSTGRES_PORT', '5432')),
            'user': self._connection_config.get('user') or os.getenv('POSTGRES_USER', 'knowledge_base'),
            'password': self._connection_config.get('password') or os.getenv('POSTGRES_PASSWORD', 'knowledge_base'),
            'database': subject.database if subject else os.getenv('POSTGRES_DB', 'knowledge_base')
        }

    def get_connection(self, subject_identifier: Optional[str] = None):
        """Get a database connection for a specific subject."""
        subject = self.resolve_subject(subject_identifier)

        if subject.id in self._connections:
            conn = self._connections[subject.id]
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                return conn
            except Exception:
                del self._connections[subject.id]

        config = self.get_connection_config(subject)
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )

        self._connections[subject.id] = conn
        logger.info(f"Created connection to subject: {subject.id}")
        return conn

    def _create_database(self, database_name: str) -> None:
        """Create a new PostgreSQL database with pgvector extension."""
        cfg = self.get_connection_config()
        conn = psycopg2.connect(
            host=cfg['host'],
            port=cfg['port'],
            user=cfg['user'],
            password=cfg['password'],
            database='postgres'
        )
        conn.autocommit = True

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (database_name,)
                )
                if cur.fetchone():
                    logger.info(f"Database {database_name} already exists")
                else:
                    cur.execute(f'CREATE DATABASE "{database_name}"')
                    logger.info(f"Created database: {database_name}")
        finally:
            conn.close()

        new_conn = psycopg2.connect(
            host=cfg['host'],
            port=cfg['port'],
            user=cfg['user'],
            password=cfg['password'],
            database=database_name
        )
        new_conn.autocommit = True

        try:
            with new_conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
                logger.info(f"Enabled pgvector in {database_name}")

                self._apply_schema(cur)
                logger.info(f"Applied schema to {database_name}")
        finally:
            new_conn.close()

    def _apply_schema(self, cursor) -> None:
        """Apply the RAG schema to a database."""
        schema_sql = """
        CREATE TABLE IF NOT EXISTS sources (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source_type VARCHAR(50) NOT NULL,
            source_id VARCHAR(500) NOT NULL,
            title VARCHAR(1000),
            description TEXT,
            author VARCHAR(500),
            url TEXT,
            duration_seconds INTEGER,
            published_at TIMESTAMP WITH TIME ZONE,
            metadata JSONB DEFAULT '{}',
            status VARCHAR(50) DEFAULT 'pending',
            error_message TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(source_type, source_id)
        );

        CREATE TABLE IF NOT EXISTS content_chunks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
            chunk_type VARCHAR(50) DEFAULT 'text',
            chunk_index INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            start_time FLOAT,
            end_time FLOAT,
            metadata JSONB DEFAULT '{}',
            embedding VECTOR(1536),
            word_count INTEGER,
            char_count INTEGER,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(source_type);
        CREATE INDEX IF NOT EXISTS idx_sources_status ON sources(status);
        CREATE INDEX IF NOT EXISTS idx_chunks_source ON content_chunks(source_id);
        CREATE INDEX IF NOT EXISTS idx_chunks_type ON content_chunks(chunk_type);

        CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw
        ON content_chunks
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
        """
        cursor.execute(schema_sql)

    def _drop_database(self, database_name: str) -> None:
        """Drop a PostgreSQL database (DANGEROUS!)."""
        cfg = self.get_connection_config()
        conn = psycopg2.connect(
            host=cfg['host'],
            port=cfg['port'],
            user=cfg['user'],
            password=cfg['password'],
            database='postgres'
        )
        conn.autocommit = True

        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = %s
                    AND pid <> pg_backend_pid()
                """, (database_name,))

                cur.execute(f'DROP DATABASE IF EXISTS "{database_name}"')
                logger.warning(f"Dropped database: {database_name}")
        finally:
            conn.close()

    # ========================================
    # Utility Methods
    # ========================================

    def close_all_connections(self) -> None:
        """Close all cached database connections."""
        for subject_id, conn in list(self._connections.items()):
            try:
                conn.close()
                logger.info(f"Closed connection to {subject_id}")
            except Exception:
                pass
        self._connections.clear()

    @property
    def db_connection_config(self) -> Dict[str, Any]:
        """Get the base database connection configuration."""
        return self._connection_config.copy()

    @property
    def default_subject_id(self) -> Optional[str]:
        """Get the ID of the default subject."""
        default = self.get_default_subject()
        return default.id if default else None

    def to_dict(self) -> Dict[str, Any]:
        """Convert subjects to a dictionary for JSON serialization."""
        return {
            'subjects': [
                {
                    'id': s.id,
                    'display_name': s.display_name,
                    'description': s.description,
                    'database': s.database,
                    'aliases': s.aliases,
                    'is_default': s.is_default
                }
                for s in self._subjects.values()
            ],
            'default_subject': self.get_default_subject().id if self.get_default_subject() else None
        }

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes all connections."""
        self.close_all_connections()
        return False
