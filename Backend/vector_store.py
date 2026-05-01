import chromadb
from sentence_transformers import SentenceTransformer
import uuid

class VectorStore:
    def __init__(self, collection_name="medicine_docs"):
        self.client = chromadb.Client()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, chunks, metadata=None):
        """
        Adds text chunks to the vector store.
        
        Args:
            chunks (list): List of text chunks.
            metadata (list): List of metadata dictionaries corresponding to chunks.
        """
        if not chunks:
            return

        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        embeddings = self.embedding_model.encode(chunks).tolist()
        
        if metadata is None:
            metadata = [{"source": "unknown"} for _ in range(len(chunks))]
            
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata,
            ids=ids
        )

    def query_similar(self, query, n_results=5):
        """
        Retrieves relevant chunks for a given query.
        
        Args:
            query (str): The user query.
            n_results (int): Number of results to return.
            
        Returns:
            dict: Query results containing documents and metadatas.
        """
        query_embedding = self.embedding_model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results
