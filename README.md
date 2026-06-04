# ✨ AI Video Assistant

Welcome to the **AI Video Assistant**, a powerful, premium application designed to transform long, unstructured videos into actionable insights! Whether you are processing a YouTube link or a local video/audio file, this tool automatically transcribes, summarizes, and extracts key data—all presented in a beautiful, modern Streamlit dashboard. 

You can even chat dynamically with the video's content using our built-in RAG (Retrieval-Augmented Generation) pipeline!

---

## 🌟 Features

- 🎥 **Dual Input Sources**: Simply paste a YouTube URL or upload a local video/audio file (`.mp4`, `.mkv`, `.mp3`, etc.).
- 📝 **Local Transcription**: Powered by OpenAI's Whisper model for highly accurate speech-to-text.
- 🧠 **Deep AI Processing**: Uses LangChain and Mistral AI to generate:
  - Smart Video Titles
  - Comprehensive AI Summaries
  - Extracted Action Items (Checklist)
  - Key Decisions (Chronological Timeline)
  - Open Questions (Tags)
- 💬 **Interactive RAG Chat**: Ask specific questions about the video content in a ChatGPT-style conversational interface.
- 🎨 **Premium UI**: A sleek, dark-themed dashboard featuring glassmorphism design, smooth animations, and detailed metrics built with Streamlit.

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.10** or higher
- **FFmpeg**: Required by `yt-dlp` and `pydub` for audio extraction and slicing. 
  - *Windows*: Can be installed via `winget install -e --id Gyan.FFmpeg`
  - *Mac*: `brew install ffmpeg`
  - *Linux*: `sudo apt install ffmpeg`

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sushhh05/AI_Video_Assistant.git
   cd AI_Video_Assistant
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # Mac/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Create a `.env` file in the root directory of the project and add your API keys. You will need a Mistral AI API key for the summarization and chat features.
   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

---

## 💻 Usage

To launch the beautiful web interface, simply run the Streamlit app:

```bash
streamlit run app.py
```

This will automatically open your default web browser to `http://localhost:8501`. 

### How to use the app:
1. **Input**: Paste a YouTube link or upload a file in the top section.
2. **Analyze**: Click the "Analyze Content" button. Go grab a coffee ☕ while the AI downloads, transcribes, and analyzes the video.
3. **Review**: Browse your generated Dashboard metrics, summaries, action items, and view the full searchable transcript.
4. **Chat**: Scroll down to the Chat section and ask the AI specific questions like *"What were the exact metrics discussed regarding Q3 sales?"*

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (with custom HTML/CSS for styling)
- **Transcription**: [Whisper](https://github.com/openai/whisper) (Local)
- **LLM Engine**: [Mistral AI](https://mistral.ai/)
- **Framework**: [LangChain](https://python.langchain.com/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Embeddings**: SentenceTransformers (HuggingFace)
- **Media Processing**: yt-dlp & FFmpeg

---

## 📄 License
This project is open-source and available under the MIT License.
