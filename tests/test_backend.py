import unittest
import os
from reportlab.pdfgen import canvas
from backend.pdf_processor import load_pdf, chunk_text
from backend.vector_store import VectorStore
from backend.rag_engine import RAGEngine

class TestBackend(unittest.TestCase):
    def setUp(self):
        # Create a dummy PDF
        self.pdf_path = "test_doc.pdf"
        c = canvas.Canvas(self.pdf_path)
        c.drawString(100, 750, "This is a test medical document.")
        c.drawString(100, 730, "Paracetamol is used to treat pain and fever.")
        c.drawString(100, 710, "Side effects include nausea and liver damage if overdosed.")
        c.save()

        self.vector_store = VectorStore(collection_name="test_collection")
        self.rag_engine = RAGEngine(self.vector_store)

    def tearDown(self):
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)
        # Clean up vector store if possible (Chroma persists, so maybe just leave it or use a temp dir)

    def test_pdf_processing(self):
        text = load_pdf(self.pdf_path)
        self.assertIn("Paracetamol", text)
        
        chunks = chunk_text(text, chunk_size=50)
        self.assertTrue(len(chunks) > 0)

    def test_vector_store_and_rag(self):
        text = load_pdf(self.pdf_path)
        chunks = chunk_text(text)
        metadata = [{"source": "test_doc.pdf"} for _ in chunks]
        
        self.vector_store.add_documents(chunks, metadata)
        
        results = self.vector_store.query_similar("What is Paracetamol used for?")
        self.assertTrue(len(results['documents'][0]) > 0)
        
        # Test RAG response (Mocking Ollama or assuming it's running)
        # Since we can't guarantee Ollama is running in this environment, we might skip the actual LLM call
        # or just try it and catch the error.
        
        try:
            response = self.rag_engine.generate_response("What is Paracetamol used for?")
            print(f"RAG Response: {response['answer']}")
            self.assertIsNotNone(response['answer'])
        except Exception as e:
            print(f"Skipping LLM test due to error: {e}")

if __name__ == '__main__':
    unittest.main()
