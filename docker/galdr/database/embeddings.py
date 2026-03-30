"""
Embedding generator using OpenAI text-embedding-3-small model.
"""
import os
from openai import OpenAI
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Generate embeddings using OpenAI's text-embedding-3-small model.

    Produces 1536-dimensional vectors for semantic search.
    """

    MODEL = "text-embedding-3-small"
    DIMENSIONS = 1536

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the embedding generator.

        Args:
            api_key: OpenAI API key. If None, uses OPENAI_API_KEY env var.

        Raises:
            ValueError: If no API key provided or found in environment
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Provide as argument or set OPENAI_API_KEY env var."
            )

        self.client = OpenAI(api_key=self.api_key)
        logger.info(f"EmbeddingGenerator initialized with model: {self.MODEL}")

    def generate(self, text: str) -> List[float]:
        """
        Generate embedding for a single text string.

        Args:
            text: The text to embed

        Returns:
            List of 1536 floats representing the embedding vector

        Raises:
            Exception: If API call fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            response = self.client.embeddings.create(
                model=self.MODEL,
                input=text.strip()
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated {len(embedding)}-dim embedding for text ({len(text)} chars)")
            return embedding
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise

    def to_pg_vector(self, embedding: List[float]) -> str:
        """
        Convert embedding list to PostgreSQL vector string format.

        Args:
            embedding: List of floats from generate()

        Returns:
            String in format '[0.1,0.2,...]' for PostgreSQL vector casting
        """
        return '[' + ','.join(map(str, embedding)) + ']'

    def generate_pg_vector(self, text: str) -> str:
        """
        Convenience method: generate embedding and convert to pg vector format.

        Args:
            text: The text to embed

        Returns:
            PostgreSQL vector string ready for use in queries
        """
        embedding = self.generate(text)
        return self.to_pg_vector(embedding)

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in a single API call.

        More efficient than calling generate() multiple times.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (each is List[float] of length 1536)
        """
        if not texts:
            return []

        cleaned_texts = [t.strip() for t in texts if t and t.strip()]
        if not cleaned_texts:
            return []

        try:
            response = self.client.embeddings.create(
                model=self.MODEL,
                input=cleaned_texts
            )
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"Generated {len(embeddings)} embeddings in batch")
            return embeddings
        except Exception as e:
            logger.error(f"Batch embedding generation failed: {e}")
            raise
