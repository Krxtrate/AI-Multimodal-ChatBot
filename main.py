from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from pypdf import PdfReader
from dotenv import load_dotenv

from huggingface_hub import InferenceClient

import requests
import base64
import os

from io import BytesIO
from typing import List

load_dotenv()


# =====================================================
# APP SETUP
# =====================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_text = ""

# =====================================================
# IMAGE GENERATION CLIENT
# =====================================================

hf_client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)


# =====================================================
# MODELS
# =====================================================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ImageRequest(BaseModel):
    prompt: str


# =====================================================
# ROUTES
# =====================================================

@app.get("/")
def home():
    return {
        "message": "AI Assistant Running"
    }


# =====================================================
# CHAT
# =====================================================

@app.post("/generate")
def generate(chat: ChatRequest):

    global document_text

    conversation = ""

    if not chat.messages:
        return {
            "output": "No message received."
        }

    # -----------------------------------
    # SYSTEM PROMPT
    # -----------------------------------

    conversation = """
    SYSTEM INSTRUCTION:

    You are a helpful AI assistant.

    You can:
    - Answer questions
    - Help with programming
    - Explain concepts
    - Read uploaded PDFs
    - Generate creative content
    - Engage in conversation

    Answer clearly and professionally.
    """
    # -----------------------------------
    # OPTIONAL PDF CONTEXT
    # -----------------------------------

    if document_text:

        conversation += f"""

        UPLOADED DOCUMENT:

        {document_text[:2500]}

        If the user's question refers to the uploaded document,
        use this information.

        """

    # -----------------------------------
    # CHAT MEMORY
    # -----------------------------------

    for msg in chat.messages[-10:]:

        if msg.role == "user":

            conversation += (
                f"<|user|>\n"
                f"{msg.content}\n"
            )

        else:

            conversation += (
                f"<|assistant|>\n"
                f"{msg.content}\n"
            )

    conversation += "<|assistant|>\n"

    # -----------------------------------
    # OLLAMA
    # -----------------------------------

    payload = {
        "model": "llama3.1:8b",
        "prompt": conversation,
        "stream": False,
        "options": {
            "num_predict": 350,
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            return {
                "output": "The AI service is currently unavailable."
            }

    except requests.exceptions.RequestException:
        return {
            "output": "The AI service is currently unavailable."
        }
        
    result = response.json()

    return {
        "output": result["response"]
    }


# =====================================================
# PDF UPLOAD
# =====================================================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    global document_text

    reader = PdfReader(file.file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    document_text = text

    print("\n===== PDF UPLOADED =====")
    print(f"Characters: {len(text)}")
    print("========================\n")

    return {
        "message": "Document uploaded successfully",
        "pdf_length": len(text),
        "pdf_preview": text[:500]
    }


# =====================================================
# IMAGE GENERATION
# =====================================================

@app.post("/generate-image")
def generate_image(data: ImageRequest):

    try:
        image = hf_client.text_to_image(
            data.prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )

    except Exception:
        return {
            "image": None,
            "error": "Image generation failed."
        }

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return {
        "image": image_base64
    }