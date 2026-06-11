# 🤖 AI Multimodal Assistant

An intelligent multimodal AI assistant built using **React**, **FastAPI**, **Ollama**, and **Hugging Face**.

This project combines conversational AI, PDF document understanding, and AI-powered image generation into a single modern web application.

---

## ✨ Features

### 💬 Intelligent Chat

* Natural language conversations
* Context-aware responses
* Conversation memory
* Coding assistance
* Technical explanations
* General-purpose AI assistant

### 📄 PDF Analysis

* Upload PDF documents
* Extract text automatically
* Ask questions about uploaded documents
* Summarize document content
* Retrieve information from PDFs

### 🎨 AI Image Generation

* Generate images from text prompts
* Powered by FLUX.1 Schnell
* Fast image creation
* Download generated images

### ⚡ Modern Interface

* Responsive React frontend
* Real-time chat experience
* Clean and intuitive UI
* Message history
* File upload support

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* Axios
* CSS

### Backend

* FastAPI
* Python
* Pydantic

### AI Models

* Llama 3.1 (Ollama)
* FLUX.1 Schnell (Hugging Face)

### Additional Libraries

* PyPDF
* Hugging Face Hub
* Python Dotenv

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Multimodal-Assistant.git
cd AI-Multimodal-Assistant
```

### Backend Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
HF_TOKEN=your_huggingface_token
```

Start Backend:

```bash
uvicorn main:app --reload
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## 📷 Screenshots

Add screenshots of:

* Chat Interface
* PDF Upload
* Image Generation
* AI Responses

---

## 🔮 Future Improvements

* Voice Assistant
* Speech-to-Text
* Multiple AI Models
* Chat History Storage
* Authentication System
* Cloud Deployment
* RAG Knowledge Base Integration

---

## 📄 License

This project is open-source and available under the MIT License.

---

### Made with ❤️ using React, FastAPI, Ollama, and Hugging Face
