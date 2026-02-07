# 🔮 Mystic YouTube Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain)](https://langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge)](https://groq.com/)



https://github.com/user-attachments/assets/a4db58b9-4afd-476d-aaf1-a516564184f0


**Mystic Assistant** is a AI companion built directly into the YouTube sidebar. Using  **Retrieval-Augmented Generation (RAG)**, it "reads" video transcripts in real-time, allowing you to have deep conversations, generate summaries, and extract insights from any video without leaving the page.

---

## ✨ Key Features

* **🧠 Hybrid Multi-Retriever:** Merges `FAISS` (Semantic/Dense) and `BM25` (Keyword/Sparse) search for pinpoint accuracy.
* **⚡ Flashrank Reranking:** Implements a cross-encoder reranking layer to ensure the LLM receives only the most relevant context.
* **💬 Contextual Memory:** A history-aware pipeline that understands pronouns and follow-up questions (e.g., *"Who is he?"*).
* **🌙 Modern Dark UI:** A sleek, YouTube-integrated dark mode side panel built with Manifest V3.
* **🚀 Ultra-Fast Inference:** Powered by **Llama 3.3 70B** via Groq for sub-second responses.
* **📜 Smart Transcript Logic:** Automatically handles manual uploads and auto-generated English captions.

---

## 🛠️ Tech Stack

### Backend (Python)
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Orchestration:** [LangChain](https://python.langchain.com/) (LCEL)
- **Embeddings:** `all-MiniLM-L6-v2` (HuggingFace)
- **Vector DB:** [FAISS](https://github.com/facebookresearch/faiss)
- **Extraction:** `yt-dlp` for VTT transcript processing

### Frontend (Chrome Extension)
- **API:** Manifest V3 (SidePanel API)
- **Styling:** CSS3 (Modern Dark Theme)
- **Logic:** Native JavaScript (Fetch & Service Workers)

---

## 📂 Project Structure

```text
mystic-youtube-assistant/
├── main.py              # FastAPI server & API endpoints
├── backend.py           # Core RAG logic & LangChain pipeline
├── .env                 # API keys (Secrets)
├── downloads/           # Temporary transcript storage
└── extension/           # Chrome Extension folder
    ├── manifest.json    # Extension config
    ├── sidepanel.html   # Main UI
    ├── style.css        # Dark mode styles
    └── sidepanel.js     # Frontend logic
```

🚀 Installation & Setup
1. Backend Configuration

Ensure you have Python 3.9+ installed.

Bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/mystic-youtube-assistant.git](https://github.com/YOUR_USERNAME/mystic-youtube-assistant.git)
cd mystic-youtube-assistant

# Install dependencies
pip install fastapi uvicorn langchain langchain-community langchain-groq \
            langchain-huggingface faiss-cpu flashrank yt-dlp python-dotenv
2. Set API Keys

Create a .env file in the root directory:

Bash
GROQ_API_KEY=your_groq_api_key_here
3. Load the Extension

Open Chrome and go to chrome://extensions/.

Turn on Developer Mode (top right).

Click Load unpacked and select the /extension folder from this project.

🎮 How to Use
Start the server:

Bash
python main.py
Open any YouTube video in Chrome.

Click the Mystic Assistant icon in your extension bar.

The side panel will open. Ask anything about the video!
