import requests
from config import API_BASE_URL


def health_check():
    try:
        resp = requests.get(f"{API_BASE_URL}/health", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def upload_pdf(file_obj):
    try:
        resp = requests.post(
            f"{API_BASE_URL}/upload",
            files={"file": (file_obj.name, file_obj, "application/pdf")},
            timeout=120,
        )
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def get_paper():
    try:
        resp = requests.get(f"{API_BASE_URL}/paper", timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def get_digest():
    try:
        resp = requests.get(f"{API_BASE_URL}/digest", timeout=120)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def ask_question(question):
    try:
        resp = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": question},
            timeout=120,
        )
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def clear_paper():
    try:
        resp = requests.delete(f"{API_BASE_URL}/paper", timeout=10)
        return resp.status_code == 200
    except Exception:
        return False
