# Medicine & Symptoms Information Assistant

This project is an AI-powered Healthcare Medicine & Symptoms Information Assistant built using Retrieval-Augmented Generation (RAG).
Users can upload medical PDFs (e.g., lab reports, discharge summaries, or drug information sheets), and the system extracts text, creates embeddings, and stores them in ChromaDB. When a user asks a question, the system performs semantic retrieval and uses a local LLM to generate a concise, factual answer based strictly on the retrieved chunks.

Key Features

📄 PDF Upload & Processing

🧠 Embeddings + Vector Database (ChromaDB)

🔍 RAG-based semantic search

💬 Natural language Q&A using LLM

📚 Source-cited answers (no hallucination)

⚠️ Medical safety: No diagnosis or advice

Tech Stack

Python, Streamlit, SentenceTransformers, ChromaDB, LangChain (optional), Ollama (LLM)

What it Demonstrates

GenAI integration

Prompt engineering

Retrieval pipelines

LLM safety and grounding

Real-world healthcare document handling
