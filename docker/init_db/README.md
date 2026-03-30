# Database Initialization Scripts

This directory contains SQL scripts that are automatically executed when the PostgreSQL container starts for the first time.

## Execution Order

Scripts are executed in alphabetical order:

| Script | Purpose |
|--------|---------|
| `01_extensions.sql` | Enable pgvector, uuid-ossp, pg_trgm extensions |
| `02_schema.sql` | Create tables, indexes, views, and functions |
| `03_multi_subject.sql` | Multi-subject database support and default subjects |
| `04_grants.sql` | Permission grants and final verification |

## Tables Created

### `sources`
Stores metadata for all content types (webpages, PDFs, documents, etc.)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| source_type | TEXT | 'webpage', 'pdf', 'document', etc. |
| source_id | TEXT | Unique ID within type |
| title | TEXT | Content title |
| content_full | TEXT | Full extracted text |
| metadata | JSONB | Type-specific metadata |
| status | TEXT | 'pending', 'completed', 'failed' |

### `content_chunks`
Stores text chunks with embeddings for semantic search

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| source_id | UUID | Reference to sources |
| chunk_text | TEXT | The text chunk |
| chunk_index | INT | Order within source |
| embedding | VECTOR(1536) | OpenAI embedding |
| position_start/end | DECIMAL | Position in source |

### `subjects`
Registry of knowledge domains/subjects

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | Subject identifier |
| name | TEXT | Display name |
| database_name | TEXT | PostgreSQL database name |
| is_default | BOOLEAN | Default subject flag |

## Default Subjects

Two subjects are created by default:

1. **work_knowledge** (default) - Work-related documents and standards
2. **ai_coding** - Technical documentation and AI/ML resources

## Indexes

### HNSW Index for Semantic Search
```sql
CREATE INDEX idx_content_chunks_embedding ON content_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

This uses HNSW (Hierarchical Navigable Small World) indexing which provides:
- O(log n) search complexity
- Better recall than IVFFlat
- No need to train on data

## Functions

### `search_similar(query_embedding, match_count, threshold)`
Semantic search helper that returns similar chunks

```sql
SELECT * FROM search_similar(
    '[0.1, 0.2, ...]'::vector,  -- query embedding
    10,                          -- max results
    0.7                          -- similarity threshold
);
```

### `create_subject_database(id, name, description)`
Register a new subject

```sql
SELECT create_subject_database('my_subject', 'My Subject', 'Description');
```

### `set_default_subject(id)`
Change the default subject

```sql
SELECT set_default_subject('ai_coding');
```

## Manual Execution

If you need to run these scripts manually:

```bash
# Connect to the database
docker exec -it galdr_postgres psql -U galdr -d rag_knowledge

# Run a script
\i /docker-entrypoint-initdb.d/02_schema.sql
```

## Resetting the Database

To completely reset and reinitialize:

```bash
# Stop containers and remove volumes
docker-compose down -v

# Start fresh (init scripts will run again)
docker-compose up -d
```

## Troubleshooting

### Extensions not found
Ensure you're using the `pgvector/pgvector:pg16` image which has pgvector pre-installed.

### Permission denied
The scripts grant PUBLIC access. If you need stricter permissions, modify `04_grants.sql`.

### Schema already exists
Scripts use `IF NOT EXISTS` so they're safe to run multiple times.
