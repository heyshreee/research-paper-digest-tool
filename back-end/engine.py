from pathlib import Path

from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    VectorStoreIndex,
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from prompts import DIGEST_PROMPT, QUESTION_PROMPT


# ============================================================
# PATHS
# ============================================================

DATA_DIR = Path("data")
PAPER_PATH = DATA_DIR / "paper.txt"


# ============================================================
# MODEL CONFIGURATION
# ============================================================

Settings.llm = Ollama(
    model="llama3.2",
    base_url="http://127.0.0.1:11434",
    request_timeout=120.0,
    context_window=8192,
)

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
)


# ============================================================
# ENGINE STATE
# ============================================================

index = None
query_engine = None


# ============================================================
# LOAD PAPER
# ============================================================

def load_paper():
    """
    Load the currently extracted paper and build its vector index.
    """

    global index, query_engine

    if not PAPER_PATH.exists():
        raise FileNotFoundError("No paper is currently loaded.")

    documents = SimpleDirectoryReader(
        input_files=[str(PAPER_PATH)]
    ).load_data()

    index = VectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine(
        similarity_top_k=5,
    )


# ============================================================
# GENERATE DIGEST
# ============================================================

def generate_digest() -> str:
    """
    Generate a concise research-paper digest.
    """

    if query_engine is None:
        load_paper()

    response = query_engine.query(DIGEST_PROMPT)

    return str(response)


# ============================================================
# QUESTION ANSWERING
# ============================================================

def answer_question(question: str) -> str:
    """
    Answer a question using the loaded research paper.
    """

    if query_engine is None:
        load_paper()

    prompt = QUESTION_PROMPT.format(
        question=question
    )

    response = query_engine.query(prompt)

    return str(response)


# ============================================================
# CLEAR ENGINE
# ============================================================

def clear_engine():
    """
    Clear the currently loaded index.
    """

    global index, query_engine

    index = None
    query_engine = None