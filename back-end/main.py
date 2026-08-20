from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from pdfparser import extract_text


app = FastAPI(
    title="Research Paper Digest API",
    description="Backend API for the Research Paper Digest Tool",
    version="1.0.0",
)


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PAPER_PATH = DATA_DIR / "paper.txt"


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Research Paper Digest API is running",
    }


@app.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    pdf_path = DATA_DIR / file.filename

    try:
        contents = await file.read()
        pdf_path.write_bytes(contents)

        text = extract_text(str(pdf_path))

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF.",
            )

        PAPER_PATH.write_text(text, encoding="utf-8")

        return {
            "status": "success",
            "filename": file.filename,
            "characters": len(text),
            "message": "PDF uploaded and text extracted successfully.",
        }

    finally:
        if pdf_path.exists():
            pdf_path.unlink()


@app.get("/paper")
def get_paper():
    if not PAPER_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="No paper is currently loaded.",
        )

    text = PAPER_PATH.read_text(encoding="utf-8")

    return {
        "status": "success",
        "characters": len(text),
        "text": text,
    }