from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from pdfparser import extract_text
from engine import (
    load_paper,
    clear_engine,
    generate_digest,
    answer_question,
)


app = FastAPI(
    title="Research Paper Digest API",
    description="Backend API for the Research Paper Digest Tool",
    version="1.0.0",
)


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PAPER_PATH = DATA_DIR / "paper.txt"


# ============================================================
# REQUEST MODELS
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Research Paper Digest API is running",
    }


# ============================================================
# UPLOAD PDF
# ============================================================

@app.post("/upload")
async def upload_paper(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF.",
        )

    pdf_path = DATA_DIR / file.filename

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty.",
            )

        pdf_path.write_bytes(contents)

        text = extract_text(str(pdf_path))

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF.",
            )

        PAPER_PATH.write_text(
            text,
            encoding="utf-8",
        )

        load_paper()

        return {
            "status": "success",
            "filename": file.filename,
            "characters": len(text),
            "message": "PDF uploaded and processed successfully.",
        }

    finally:

        if pdf_path.exists():
            pdf_path.unlink()


# ============================================================
# GET CURRENT PAPER
# ============================================================

@app.get("/paper")
def get_paper():

    if not PAPER_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="No paper is currently loaded.",
        )

    text = PAPER_PATH.read_text(
        encoding="utf-8"
    )

    return {
        "status": "success",
        "characters": len(text),
        "text": text,
    }


# ============================================================
# DELETE CURRENT PAPER
# ============================================================

@app.delete("/paper")
def delete_paper():

    if not PAPER_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="No paper is currently loaded.",
        )

    PAPER_PATH.unlink()

    clear_engine()

    return {
        "status": "success",
        "message": "Current paper deleted successfully.",
    }


# ============================================================
# GENERATE DIGEST
# ============================================================

@app.get("/digest")
def get_digest():

    if not PAPER_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="No paper is currently loaded.",
        )

    try:

        digest = generate_digest()

        return {
            "status": "success",
            "digest": digest,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate digest: {str(e)}",
        )


# ============================================================
# ASK QUESTION
# ============================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    if not PAPER_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="No paper is currently loaded.",
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        answer = answer_question(
            request.question
        )

        return {
            "status": "success",
            "question": request.question,
            "answer": answer,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {str(e)}",
        )