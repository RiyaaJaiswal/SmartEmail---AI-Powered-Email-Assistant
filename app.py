import gradio as gr
import os
import tempfile
from backend import SmartEmailProcessor

# Initialize the processor
processor = SmartEmailProcessor()

def process_files_and_query(files, query):
    if not files:
        return "Please upload at least one file."
    
    if not query.strip():
        return "Please enter a query."
    
    try:
        # Clear previous data
        processor.all_chunks = []
        processor.faiss_index = None
        processor.chunk_embeddings = None
        
        # Process uploaded files
        for file in files:
            file_path = file.name
            chunks = processor.load_and_chunk_document(file_path)
            print(f"Processed {file_path}: {len(chunks)} chunks")
        
        # Build FAISS index
        processor.build_faiss_index()
        
        # Search for relevant chunks
        retrieved_chunks = processor.search_documents(query, k=3)
        
        # Generate response
        response = processor.generate_response(query, retrieved_chunks)
        
        return response
    
    except Exception as e:
        return f"Error processing files: {str(e)}"

def create_interface():
    with gr.Blocks(title="SmartEmail - AI-Powered Email Assistant") as interface:
        gr.Markdown("# 📧 SmartEmail - AI-Powered Email Assistant")
        gr.Markdown("Upload your documents (PDF, DOCX, TXT) and ask questions about their content!")
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input = gr.File(
                    label="Upload Documents",
                    file_count="multiple",
                    file_types=[".pdf", ".docx", ".txt"]
                )
                query_input = gr.Textbox(
                    label="Your Query",
                    placeholder="e.g., Summarize the main points from the uploaded documents",
                    lines=3
                )
                submit_btn = gr.Button("Process & Generate Response", variant="primary")
            
            with gr.Column(scale=2):
                output = gr.Textbox(
                    label="AI Response",
                    lines=15,
                    max_lines=20
                )
        
        # Examples
        gr.Markdown("## Example Queries:")
        examples = [
            "Summarize the main points from the uploaded documents",
            "What are the key action items mentioned?",
            "Who are the main stakeholders discussed?",
            "What are the deadlines mentioned in the documents?",
            "Generate a brief summary of the client communication"
        ]
        
        for example in examples:
            gr.Markdown(f"• {example}")
        
        submit_btn.click(
            fn=process_files_and_query,
            inputs=[file_input, query_input],
            outputs=output
        )
    
    return interface

if __name__ == "__main__":
    import os
    interface = create_interface()
    port = int(os.environ.get("PORT", 7860))
    interface.launch(server_name="0.0.0.0", server_port=port, share=False)

