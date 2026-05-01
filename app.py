import streamlit as st
import os
import tempfile
from backend.pdf_processor import load_pdf, chunk_text
from backend.vector_store import VectorStore
from backend.rag_engine import RAGEngine

# Page Config
st.set_page_config(page_title="Medicine Info Assistant", layout="wide")

# Title and Description
st.title("🏥 Medicine & Symptoms Information Assistant")
st.markdown("""
This is a **safe, factual healthcare information system** using RAG.
Upload a medical PDF (e.g., drug info sheet) and ask questions.
**Disclaimer:** This tool does NOT provide medical advice or diagnosis.
""")

# Initialize Backend Components
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = VectorStore()
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = RAGEngine(st.session_state.vector_store)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar: PDF Upload
with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload a Medical PDF", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                # Save uploaded file to temp
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Extract and Chunk
                text = load_pdf(tmp_path)
                chunks = chunk_text(text)
                
                # Add to Vector Store
                metadata = [{"source": uploaded_file.name} for _ in chunks]
                st.session_state.vector_store.add_documents(chunks, metadata)
                
                st.success(f"Processed {len(chunks)} chunks from {uploaded_file.name}!")
                os.remove(tmp_path)

    st.markdown("---")
    with st.expander("⚙️ Settings"):
        # Dynamic Model Selection
        try:
            import ollama
            models_info = ollama.list()
            
            # Handle different response structures (object vs dict)
            model_names = []
            if hasattr(models_info, 'models'):
                for m in models_info.models:
                    if hasattr(m, 'model'):
                        model_names.append(m.model)
                    elif isinstance(m, dict) and 'name' in m:
                        model_names.append(m['name'])
                    elif isinstance(m, dict) and 'model' in m:
                        model_names.append(m['model'])
            elif isinstance(models_info, dict) and 'models' in models_info:
                 for m in models_info['models']:
                    if isinstance(m, dict) and 'name' in m:
                        model_names.append(m['name'])
                    elif isinstance(m, dict) and 'model' in m:
                        model_names.append(m['model'])
        except Exception as e:
            print(f"Could not connect to Ollama: {e}") # Log to console instead of UI
            model_names = []

        if model_names:
            model_name = st.selectbox("Select LLM Model", model_names)
            if st.button("Update Model"):
                st.session_state.rag_engine.set_model(model_name)
                st.success(f"Model set to {model_name}")
        else:
            # Fallback for manual entry if connection fails or no models found
            st.warning("Could not automatically list models (check console).")
            model_name = st.text_input("Enter Model Name Manually", value="llama3")
            if st.button("Update Model"):
                st.session_state.rag_engine.set_model(model_name)
                st.success(f"Model set to {model_name}")

# Main Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the medicine..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    # Check if any documents have been processed
    if st.session_state.vector_store.collection.count() == 0:
        response_text = "⚠️ **No documents found!** Please upload and process a PDF in the sidebar first."
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing documents..."):
                response = st.session_state.rag_engine.generate_response(prompt)
                answer = response['answer']
                
                # Append sources to answer for display
                if response['context']:
                    answer += "\n\n**Sources:**"
                    for i, (doc, meta) in enumerate(zip(response['context'], response['sources'])):
                        answer += f"\n- **{meta['source']}**: {doc[:100]}..." # Show snippet
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
