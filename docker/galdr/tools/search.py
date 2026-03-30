"""
rag_search tool - Semantic search over universal knowledge base.

Searches the unified content_chunks table which contains:
- Webpage content
- PDF documents
- Any ingested text content
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def rag_search(
    db,
    embedding_generator,
    query: str,
    limit: int = 5,
    source_type: Optional[str] = None,
    source_id: Optional[str] = None,
    chunk_type: Optional[str] = None,
    min_similarity: float = 0.0
) -> dict:
    """
    Search the universal knowledge base using semantic similarity.

    Uses OpenAI text-embedding-3-small to generate query embedding,
    then performs cosine similarity search against content_chunks
    using pgvector.

    Args:
        db: RAGDatabase instance
        embedding_generator: EmbeddingGenerator instance
        query: Natural language search query
        limit: Maximum results to return (1-50, default: 5)
        source_type: Filter by source type - 'webpage', 'document', etc. (optional)
        source_id: Filter to specific source ID (optional)
        chunk_type: Filter by type: 'text', 'code', 'heading', 'list', etc. (optional)
        min_similarity: Minimum similarity threshold 0.0-1.0 (default: 0.0)

    Returns:
        Dictionary with:
        - success: bool
        - query: str (original query)
        - result_count: int
        - filters_applied: dict
        - results: list of matching chunks with source metadata
    """
    # Validate parameters
    limit = max(1, min(50, limit))
    min_similarity = max(0.0, min(1.0, min_similarity))

    if not query or not query.strip():
        return {
            "success": False,
            "error": "Query cannot be empty",
            "query": query
        }

    query = query.strip()

    try:
        # Step 1: Generate query embedding
        logger.info(f"Generating embedding for query: '{query[:50]}...'")
        query_embedding = embedding_generator.generate(query)
        embedding_str = embedding_generator.to_pg_vector(query_embedding)

        # Step 2: Build SQL query for unified schema
        sql = """
            SELECT
                c.id::text as chunk_id,
                c.chunk_text,
                c.chunk_type,
                c.chunk_index,
                c.position_start,
                c.position_end,
                c.position_metadata,
                c.word_count,
                c.has_code,
                c.has_table,
                c.has_image,
                s.id::text as source_db_id,
                s.source_type,
                s.source_id,
                s.title as source_title,
                s.author,
                s.url,
                s.description as source_description,
                s.metadata as source_metadata,
                1 - (c.embedding <=> %s::vector) AS similarity
            FROM content_chunks c
            JOIN sources s ON c.source_id = s.id
            WHERE c.embedding IS NOT NULL
        """
        params = [embedding_str]

        # Add optional filters
        if source_type:
            sql += " AND s.source_type = %s"
            params.append(source_type.lower())

        if source_id:
            sql += " AND s.source_id = %s"
            params.append(source_id)

        if chunk_type:
            valid_types = {'text', 'code', 'heading', 'list', 'table', 'transcript', 'diagram', 'mixed'}
            if chunk_type.lower() in valid_types:
                sql += " AND c.chunk_type = %s"
                params.append(chunk_type.lower())

        if min_similarity > 0:
            sql += " AND (1 - (c.embedding <=> %s::vector)) >= %s"
            params.extend([embedding_str, min_similarity])

        # Order by similarity (closest first) and limit
        sql += """
            ORDER BY c.embedding <=> %s::vector
            LIMIT %s
        """
        params.extend([embedding_str, limit])

        # Step 3: Execute query
        logger.debug(f"Executing search query with {len(params)} parameters")
        with db.get_cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        # Step 4: Format results
        results = []
        for row in rows:
            result = {
                "chunk_id": row['chunk_id'],
                "chunk_text": row['chunk_text'],
                "chunk_type": row['chunk_type'],
                "chunk_index": row['chunk_index'],
                "similarity": round(float(row['similarity']), 4),
                "source_type": row['source_type'],
                "source_id": row['source_id'],
                "source_title": row['source_title'],
                "author": row['author'],
                "url": row['url'],
                "word_count": row['word_count'],
                "has_code": row['has_code'],
                "has_table": row['has_table'],
                "has_image": row['has_image'],
            }

            # Add position info if available
            if row['position_start'] is not None:
                result["position_start"] = float(row['position_start'])
            if row['position_end'] is not None:
                result["position_end"] = float(row['position_end'])

            # Add source metadata if present
            if row['source_metadata']:
                result["source_metadata"] = row['source_metadata']

            results.append(result)

        logger.info(f"rag_search: query='{query[:30]}...' returned {len(results)} results")

        return {
            "success": True,
            "query": query,
            "result_count": len(results),
            "filters_applied": {
                "source_type": source_type,
                "source_id": source_id,
                "chunk_type": chunk_type,
                "min_similarity": min_similarity,
                "limit": limit
            },
            "results": results
        }

    except Exception as e:
        logger.error(f"rag_search failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "query": query
        }
