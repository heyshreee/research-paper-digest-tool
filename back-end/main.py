from fastapi import FastAPI

app = FastAPI(
    title="Research Paper Digest API",
    description="Backend API for the Research Paper Digest Tool",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Research Paper Digest API is running"
    }