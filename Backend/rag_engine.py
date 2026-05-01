import ollama

class RAGEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.model = "llama3" # Default model, can be changed

    def set_model(self, model_name):
        self.model = model_name

    def generate_response(self, query):
        """
        Generates a response using RAG.
        
        Args:
            query (str): The user's question.
            
        Returns:
            dict: Contains 'answer', 'sources', and 'context'.
        """
        # 1. Retrieve relevant documents
        results = self.vector_store.query_similar(query)
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        
        context = "\n\n".join(documents)
        
        # 2. Construct Prompt
        system_prompt = """You are a safe Medical Information Assistant.
You ONLY answer using the information provided in <retrieved_docs>.
You DO NOT provide medical advice, diagnosis, or treatment suggestions.

Rules:
- Use simple, understandable language.
- Cite the specific section or chunk from which the information was retrieved.
- If information is not present in the retrieved docs, say "The documents do not contain this information."
- Do not hallucinate.
- Keep the tone helpful and factual."""

        user_prompt = f"""User question: {query}

Here are the retrieved document chunks:
<retrieved_docs>
{context}
</retrieved_docs>

Generate a clear, factual answer using only the retrieved content."""

        # 3. Call LLM
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            answer = response['message']['content']
        except Exception as e:
            # Fallback if Ollama is not running
            print(f"Ollama error: {e}")
            answer = (
                f"**Error: Unable to connect to Ollama.**\n\n"
                f"Details: {e}\n\n"
                "Please ensure:\n"
                "1. **Ollama** is installed and running (`ollama serve`).\n"
                f"2. The model **'{self.model}'** is pulled (`ollama pull {self.model}`)."
            )

        return {
            "answer": answer,
            "sources": metadatas,
            "context": documents
        }
