from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever as BaseVectorStoreRetriever
from chatbot_clone.data.chunker import TextChunk


class VectorStoreRetriever:
    """Wrapper for VectorStoreRetriever to provide backward compatibility"""

    def __init__(self, base_retriever: BaseVectorStoreRetriever):
        self._retriever = base_retriever

    def get_relevant_documents(self, query: str):
        """Get relevant documents for a query (backward compatible method)"""
        return self._retriever.invoke(query)

    def __getattr__(self, name):
        """Delegate other attributes to the base retriever"""
        return getattr(self._retriever, name)


class VectorStoreManager:
    """Manages Chroma vector store for RAG retrieval"""

    def __init__(
        self,
        persist_directory: str,
        embedding_model: str = "BAAI/bge-m3",
        embedding_function=None,
    ) -> None:
        """Initialize vector store with persistence.

        Args:
            persist_directory: Directory to persist Chroma data.
            embedding_model: HuggingFace model name for embeddings (default: BAAI/bge-m3).
            embedding_function: Optional custom embedding function (useful for testing).
        """
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model

        if embedding_function is not None:
            self.embedding_function = embedding_function
        else:
            from langchain_huggingface import HuggingFaceEmbeddings
            self.embedding_function = HuggingFaceEmbeddings(
                model_name=embedding_model,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )

        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            collection_name="chatbot_chunks",
            embedding_function=self.embedding_function,
        )

    def add_chunks(self, chunks: list[TextChunk]) -> None:
        """Add text chunks to vector store.

        If a chunk has `metadata["context_prefix"]`, the embedding is computed
        from ``context_prefix + "\\n" + text`` so that the vector captures
        conversational context.  The stored document text remains the original
        ``chunk.text`` (without the prefix) so the LLM sees clean dialogue.
        """
        if not chunks:
            return

        # Build embedding texts (with context prefix when available)
        embed_texts: list[str] = []
        store_texts: list[str] = []
        metadatas: list[dict] = []

        for chunk in chunks:
            prefix = chunk.metadata.get("context_prefix", "")
            if prefix:
                embed_texts.append(f"{prefix}\n{chunk.text}")
            else:
                embed_texts.append(chunk.text)
            store_texts.append(chunk.text)
            metadatas.append(chunk.metadata)

        # Compute embeddings from context-enriched text
        embeddings = self.embedding_function.embed_documents(embed_texts)

        # Store with original text + precomputed embeddings
        self.vectorstore.add_texts(
            texts=store_texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def similarity_search_with_scores(
        self,
        query: str,
        k: int = 5,
    ) -> list[tuple]:
        """Search for similar documents and return (Document, score) pairs.

        Scores are relevance scores in [0, 1] where 1 is most similar.
        """
        return self.vectorstore.similarity_search_with_relevance_scores(
            query, k=k,
        )

    def get_retriever(self, k: int = 5) -> VectorStoreRetriever:
        """Get a retriever for semantic search"""
        base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        return VectorStoreRetriever(base_retriever)
