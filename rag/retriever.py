from chatbot_clone.vectorstore.manager import VectorStoreManager


class RAGRetriever:
    """Retrieves relevant context for user query"""

    def __init__(
        self,
        vectorstore_manager: VectorStoreManager,
        top_k: int = 5,
        similarity_threshold: float = 0.0,
    ) -> None:
        """Initialize retriever with vector store.

        Args:
            vectorstore_manager: Vector store to search.
            top_k: Maximum number of results to return.
            similarity_threshold: Minimum relevance score in [0, 1].
                Results below this score are discarded.  Default 0.0
                means no filtering (return all top_k results).
        """
        self.vectorstore_manager = vectorstore_manager
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(self, query: str) -> list[str]:
        """Retrieve relevant text chunks for query.

        Uses similarity_search_with_scores when a threshold is set,
        otherwise falls back to the simple retriever.
        """
        if self.similarity_threshold > 0:
            scored = self.vectorstore_manager.similarity_search_with_scores(
                query, k=self.top_k,
            )
            return [
                doc.page_content
                for doc, score in scored
                if score >= self.similarity_threshold
            ]

        retriever = self.vectorstore_manager.get_retriever(k=self.top_k)
        documents = retriever.invoke(query)
        return [doc.page_content for doc in documents]
