# SmartEmail - AI-Powered Email Assistant

SmartEmail is an intelligent assistant that uses Retrieval-Augmented Generation (RAG) to summarize or respond to emails, using user-uploaded files as context.

## 🌟 Features

- **Document Processing**: Supports PDF, DOCX, and TXT file uploads
- **Semantic Search**: Uses vector embeddings for intelligent content retrieval
- **AI-Powered Responses**: Leverages open-source LLMs for generating summaries and responses
- **User-Friendly Interface**: Clean Gradio-based web interface
- **Free & Open Source**: Uses only open-source tools and models
- **Cross-Platform**: Works on Windows, Mac, and Linux

## 🛠 Tech Stack

- **Frontend**: Gradio
- **Document Processing**: PyMuPDF, docx2txt
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **LLM**: google/flan-t5-base (Hugging Face Transformers)

## 🚀 Quick Start (Windows)

### Option 1: Run Locally on Windows

1. **Clone the repository:**
```cmd
git clone <repository-url>
cd SmartEmail
```

2. **Create a virtual environment:**
```cmd
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```cmd
pip install -r requirements.txt
```

4. **Start the application:**
```cmd
python app.py
```

5. **Open your browser:** Navigate to `http://localhost:7860`


## 📝 Usage

1. **Upload Documents**: Drag and drop or click to upload PDF, DOCX, or TXT files
2. **Enter Query**: Type your question in the text box
3. **Get AI Response**: Click "Process & Generate Response"

## 💡 Example Queries

- "Summarize the main points from the uploaded documents"
- "What are the key action items mentioned?"
- "Who are the main stakeholders discussed?"
- "What are the deadlines mentioned in the documents?"
- "Generate a brief summary of the client communication"

## 🔧 How It Works

1. **Document Chunking**: Uploaded documents are broken into 400-600 token chunks
2. **Embedding Generation**: Chunks are converted to vectors using sentence-transformers
3. **Vector Storage**: Embeddings are stored and indexed in FAISS
4. **Semantic Search**: User queries are converted to vectors and matched against stored chunks
5. **Response Generation**: Retrieved chunks provide context for the LLM to generate responses

## 📁 Project Structure

```
SmartEmail/
├── app.py              # Main Gradio application
├── backend.py          # Core processing logic
├── start.py            # Cloud deployment entry point
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── README.md          # This file
├── test_documents/    # Sample test documents
└── Dockerfile         # Container deployment (optional)
```

## ⚙️ System Requirements

- **Python**: 3.8+ (3.11 recommended)
- **RAM**: 4GB+ (for model loading)
- **Storage**: 2GB+ (for models and dependencies)
- **Internet**: Required for initial model downloads

## 🌐 Deployment Options

### Cloud Platforms (Windows-friendly):
- **Render** (Recommended - Free tier available)
- **Railway** (Easy deployment)
- **Heroku** (Popular choice)
- **Google Cloud Run** (Scalable)
- **AWS App Runner** (Enterprise)

### Local Development:
- **Windows 10/11** with Python 3.8+
- **WSL2** (Windows Subsystem for Linux)
- **Docker Desktop** (Container deployment)

## 🔒 Security & Privacy

- All processing happens on the server (no data sent to external APIs)
- Documents are processed in memory (not permanently stored)
- Open-source models ensure transparency
- No tracking or analytics

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🆘 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with details about your problem
3. Include your operating system and Python version

---

**Made with ❤️ for the open-source community**

