import fitz  # PyMuPDF
import docx2txt
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class SmartEmailProcessor:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2', llm_model_name='google/flan-t5-base'):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        self.llm_model = AutoModelForSeq2SeqLM.from_pretrained(llm_model_name)
        self.all_chunks = []
        self.faiss_index = None
        self.chunk_embeddings = None

    def _extract_text_from_pdf(self, file_path):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def _extract_text_from_docx(self, file_path):
        return docx2txt.process(file_path)

    def _extract_text_from_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_and_chunk_document(self, file_path, chunk_size=500, overlap=50):
        file_extension = os.path.splitext(file_path)[1].lower()
        text = ""
        if file_extension == '.pdf':
            text = self._extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = self._extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = self._extract_text_from_txt(file_path)
        else:
            raise ValueError("Unsupported file type.")
        
        chunks = self.chunk_text(text, chunk_size, overlap)
        self.all_chunks.extend(chunks)
        return chunks

    def chunk_text(self, text, chunk_size=500, overlap=50):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def generate_embeddings(self, texts):
        return self.embedding_model.encode(texts, show_progress_bar=True)

    def build_faiss_index(self):
        if not self.all_chunks:
            print("No chunks to build index from.")
            return
        
        self.chunk_embeddings = self.generate_embeddings(self.all_chunks)
        dimension = self.chunk_embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(self.chunk_embeddings)
        print("FAISS index built.")

    def search_documents(self, query, k=5):
        if self.faiss_index is None:
            print("FAISS index not built. Please load documents and build the index first.")
            return []

        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.faiss_index.search(query_embedding, k)
        
        retrieved_chunks = []
        for idx in indices[0]:
            if 0 <= idx < len(self.all_chunks):
                retrieved_chunks.append(self.all_chunks[idx])
        return retrieved_chunks

    def generate_response(self, query, retrieved_content):
        context = "".join(retrieved_content)
        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        
        inputs = self.tokenizer(prompt, return_tensors='pt', max_length=512, truncation=True)
        outputs = self.llm_model.generate(inputs.input_ids, max_new_tokens=200, num_beams=5, early_stopping=True)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

if __name__ == '__main__':
    processor = SmartEmailProcessor()
    
    # Create dummy files for testing
    dummy_txt_content = """This is a test document. It contains some information about SmartEmail. SmartEmail is an intelligent assistant that uses Retrieval-Augmented Generation (RAG) to summarize or respond to emails. It supports uploading files like PDFs, text files, and DOCX files. The system performs semantic search over their content using vector embeddings. An open-source LLM is used to generate responses or summaries. Document chunking breaks uploaded documents into clean 400-600 token chunks. These chunks are then converted into vectors using a Sentence Transformer model. FAISS is used for storing and querying these vector embeddings. When a user query is received, it's converted to a vector, and FAISS retrieves the top relevant chunks. Finally, a prompt is constructed dynamically, and a Hugging Face model generates a fluent, useful output."""
    with open('test.txt', 'w') as f:
        f.write(dummy_txt_content)

    # Load and process a document
    chunks = processor.load_and_chunk_document('test.txt')
    print(f"Number of chunks: {len(chunks)}")
    
    processor.build_faiss_index()
    
    query = "What is SmartEmail and what does it do?"
    retrieved_chunks = processor.search_documents(query)
    print(f"Retrieved chunks for '{query}': {retrieved_chunks}")

    response = processor.generate_response(query, retrieved_chunks)
    print(f"Generated response: {response}")

    # Clean up dummy file
    os.remove('test.txt')

