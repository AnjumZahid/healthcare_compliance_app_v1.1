# backend/main.py
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # suppress TF INFO & WARNING logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # disable oneDNN custom ops (optional)

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import asyncio, shutil, threading, json
from typing import List, Union
from contextlib import asynccontextmanager

from graphs.compliance_graph import graph_app
from state.chat_state import ChatState
from services.start_server import start_fda_server
from config.settings import PDF_DIR, BASE_DIR, IMAGE_DIR


# --- Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("🚀 Starting FDA MCP server...")
    thread = threading.Thread(target=start_fda_server, daemon=True)
    thread.start()
    print("✅ FDA MCP server started in background.")
    yield
    print("🛑 Shutting down backend...")


# --- FastAPI App ---
app = FastAPI(lifespan=lifespan)

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Endpoint ---
@app.post("/process/")
async def process_data(
    file: Union[UploadFile, List[UploadFile]],  # ✅ single OR multiple PDFs
    image: UploadFile,
    raw_medicine_text: str = Form(...),
    raw_manual_questions: str = Form("[]"),
):
    # --- Create upload folders if missing ---
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

    pdf_paths = []

    # ✅ Handle single or multiple PDF uploads
    if isinstance(file, list):
        for f in file:
            pdf_path = os.path.join(PDF_DIR, f.filename)
            with open(pdf_path, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)
            pdf_paths.append(pdf_path)
    else:
        pdf_path = os.path.join(PDF_DIR, file.filename)
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        pdf_paths.append(pdf_path)

    # ✅ Save image
    img_path = os.path.join(IMAGE_DIR, image.filename)
    with open(img_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # ✅ Parse manual doctor questions
    try:
        manual_qs_list = json.loads(raw_manual_questions)
    except Exception:
        manual_qs_list = []

    # ✅ Build initial state
    initial_state = ChatState(
        pdf_hist_path=pdf_paths,  # ✅ always a list now
        image_path=img_path,
        raw_medicine_text=raw_medicine_text,
        raw_manual_questions=manual_qs_list,
    )

    # ✅ Run LangGraph pipeline
    result = await graph_app.ainvoke(initial_state)

    all_questions = []
    cq_json = result.get("compliance_questions_json", {})
    if isinstance(cq_json, dict):
        for _, qs in cq_json.items():
            all_questions.extend(qs)

    return {
        # "questions": result.get("compliance_questions_json", {}),
        "questions": all_questions,  # ✅ flat list now
        "context": result.get("retrieved_chunks", ""),
        "image_text": result.get("cv_model_text", ""),
        "compliance_query": result.get("compliance_prompt", ""),
        "compliance_answer": result.get("compliance_answer", ""),
    }
