import pypdf

def load_pdf(file_path):
    """
    Extracts text from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of a specified size with overlap.
    
    Args:
        text (str): The text to chunk.
        chunk_size (int): The maximum size of each chunk (in characters).
        overlap (int): The number of characters to overlap between chunks.
        
    Returns:
        list: A list of text chunks.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
        
    return chunks
