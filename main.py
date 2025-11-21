# main.py
import time
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

# ========================= Logging =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Azure AI Foundry Chat API for Power BI")

# ========================= CORS =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ========================= Azure AI Foundry Config =========================
# ⚠️ For safety, put this in an environment variable in real use.
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6InJ0c0ZULWItN0x1WTdEVlllU05LY0lKN1ZuYyIsImtpZCI6InJ0c0ZULWItN0x1WTdEVlllU05LY0lKN1ZuYyJ9.eyJhdWQiOiJodHRwczovL2FpLmF6dXJlLmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2IzNTJhYzBmLTEzMDctNGI1MC04ZjVkLWM5ZGE5ODM5NTM4Ny8iLCJpYXQiOjE3NjM3MTQ0NzUsIm5iZiI6MTc2MzcxNDQ3NSwiZXhwIjoxNzYzNzE5NTkzLCJhY3IiOiIxIiwiYWlvIjoiQVVRQXUvOGFBQUFBeW9NOWROZnpqTy8vNmpvU0FQNllGQlh6NWtnTmZmZFdSL1JUbWlOVUVEbndJYllJaStxR3lpMkk2eE5PcDBBY2N4ZUxicER2UEhkM1FuQWdHTVZmeEE9PSIsImFtciI6WyJwd2QiXSwiYXBwaWQiOiIwNGIwNzc5NS04ZGRiLTQ2MWEtYmJlZS0wMmY5ZTFiZjdiNDYiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IlBhbmRleSIsImdpdmVuX25hbWUiOiJBYmhheSIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjExNC43OS4xMzUuOTMiLCJuYW1lIjoiQWJoYXkgUGFuZGV5Iiwib2lkIjoiMjAwMTM3MmYtYTJjZC00NzQ0LWIzYTItOTNkM2Y4NTA0ZDEzIiwicHVpZCI6IjEwMDMyMDA1NDY4MTU5RkYiLCJwd2RfdXJsIjoiaHR0cHM6Ly9nby5taWNyb3NvZnQuY29tL2Z3bGluay8_bGlua2lkPTIyMjQxOTgiLCJyaCI6IjEuQVVrQUQ2eFNzd2NUVUV1UFhjbmFtRGxUaDE5dnBoamYyeGRNbmRjV05IRXFuTDR0QVR4SkFBLiIsInNjcCI6InVzZXJfaW1wZXJzb25hdGlvbiIsInNpZCI6IjAwYWE5ZmM5LTg4YTQtOTAxNS1hMDM4LTkwYTA1NjdmMDIxOCIsInN1YiI6IlpFcWd4cjNvTXBPMkdpZ0RGQU1LVnl5NDliUHBBcDhlM3E2TDZyMnBHNm8iLCJ0aWQiOiJiMzUyYWMwZi0xMzA3LTRiNTAtOGY1ZC1jOWRhOTgzOTUzODciLCJ1bmlxdWVfbmFtZSI6ImFiaGF5LnBhbmRleUByYmh1aW4ub25taWNyb3NvZnQuY29tIiwidXBuIjoiYWJoYXkucGFuZGV5QHJiaHVpbi5vbm1pY3Jvc29mdC5jb20iLCJ1dGkiOiJmdkVmQTFta0kwdWNDRm90cmJvVkFBIiwidmVyIjoiMS4wIiwieG1zX2FjdF9mY3QiOiI1IDMiLCJ4bXNfZnRkIjoiMGR0SDNrMl8yZEVJb09laDBOU1ZUSGdJLVlwUkdXSGhGLUpYcnZnUzkwY0JZWE5wWVhOdmRYUm9aV0Z6ZEMxa2MyMXoiLCJ4bXNfaWRyZWwiOiIxIDEwIiwieG1zX3N1Yl9mY3QiOiIzIDgifQ.nhaeayHX_M2aBnZvZPtt55BKOCKSI6FPIcUHj20f34xKUmEY9mRwlugjiEiPXCBtS0KzzSkIYmRHme3u6DSsm4wpoq7aDLRTRsrew_-sFAgb3qJ_oMhlqGWBKpWiXrbRr47SsR4ddQ8DChoOHQfwwEfU3ST8Y2L0q94S_PKNzdznAcGxMsq5003WJGo4dc0WM89vpNkxTfMN9g1cmBqMPxAdNofCngYBsLnSEeOcmBw3erNIq1isDmfHA9rSJsS8d3pnVC-AruimUN8jy_Poz3tVTr8z7liLqgDXHEEEXGKJ-m5Du22LKWEYTp8XPgdPdwAOvurnEHAGIZTl-aCS5A"
ENDPOINT     = "https://rbhu-foundry-2.services.ai.azure.com"
PROJECT_NAME = "rbhu-foundry"
AGENT_ID     = "asst_3x7W3aW4wyU7zQjGyJMZtuxM"
API_VERSION  = "2025-05-01"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

BASE_URL = f"{ENDPOINT}/api/projects/{PROJECT_NAME}/threads"

# ========================= Pydantic Models =========================
class ChatRequest(BaseModel):
    userQuery: str
    context: Optional[str] = None
    userId: Optional[str] = None

class ChatResponse(BaseModel):
    # This is what the Power BI visual expects
    answer: str


# ========================= Helper Functions =========================
def create_thread() -> str:
    url = f"{BASE_URL}?api-version={API_VERSION}"
    response = requests.post(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()["id"]

def send_message(thread_id: str, content: str):
    url = f"{BASE_URL}/{thread_id}/messages?api-version={API_VERSION}"
    payload = {"role": "user", "content": content}
    response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()

def start_run(thread_id: str) -> str:
    url = f"{BASE_URL}/{thread_id}/runs?api-version={API_VERSION}"
    payload = {"assistant_id": AGENT_ID}
    response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["id"]

def poll_run(thread_id: str, run_id: str, max_wait_seconds: int = 60):
    url = f"{BASE_URL}/{thread_id}/runs/{run_id}?api-version={API_VERSION}"
    start_time = time.time()

    while True:
        if time.time() - start_time > max_wait_seconds:
            raise TimeoutError("Agent took too long to respond")

        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        status = data.get("status")

        if status in ["completed", "failed", "cancelled", "expired"]:
            if status != "completed":
                error_msg = data.get("error", {}).get("message", "Unknown error")
                raise RuntimeError(f"Agent run failed: {status} - {error_msg}")
            return

        time.sleep(1.5)

def get_latest_reply(thread_id: str) -> str:
    url = f"{BASE_URL}/{thread_id}/messages?api-version={API_VERSION}"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    messages = response.json().get("data", [])

    # Get the latest assistant message, not the first
    for msg in messages:
        if msg.get("role") == "assistant":
            content_blocks = msg.get("content", [])
            if content_blocks:
                # Adjust this depending on Foundry's exact schema
                block0 = content_blocks[0]
                if "text" in block0 and "value" in block0["text"]:
                    return block0["text"]["value"]

    return "No response from agent."

# ========================= Endpoints =========================
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "Azure AI Foundry Chat API",
        "ready": True
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_query = request.userQuery.strip()
    if not user_query:
        raise HTTPException(
            status_code=400,
            detail="userQuery is required and cannot be empty"
        )

    logger.info(f"Received query from userId={request.userId or 'anonymous'}: {user_query}")

    try:
        thread_id = create_thread()
        send_message(thread_id, user_query)
        run_id = start_run(thread_id)
        poll_run(thread_id, run_id, max_wait_seconds=90)
        agent_reply = get_latest_reply(thread_id)

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error talking to Foundry: {e}")
        raise HTTPException(status_code=502, detail="Failed to connect to AI agent")
    except TimeoutError:
        logger.warning("Agent timed out")
        raise HTTPException(status_code=504, detail="Agent took too long to respond")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    # This "answer" field is exactly what the visual uses
    return ChatResponse(answer=agent_reply)


# ========================= Run Server =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
