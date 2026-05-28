import os
import uvicorn

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
from dotenv import load_dotenv

# =========================
# إعداد البيئة
# =========================
load_dotenv()

API_KEY = os.getenv("API_KEY", "beam-123456")

# =========================
# FastAPI
# =========================
app = FastAPI(title="BeamMCP SaaS")

# =========================
# حماية API Key
# =========================
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)

    return await call_next(request)

# =========================
# MCP Server
# =========================
mcp = FastMCP("BeamMCP-Agent")

# =========================
# الأدوات (TOOLS)
# =========================

@mcp.tool()
def search_domain(domain: str) -> dict:
    return {
        "domain": domain,
        "available": True,
        "price": "$12"
    }


@mcp.tool()
def analyze_text(text: str) -> dict:
    return {
        "length": len(text),
        "summary": text[:50]
    }


@mcp.tool()
def generate_report(name: str) -> dict:
    return {
        "project": name,
        "status": "generated",
        "score": 90
    }

# =========================
# MCP endpoint الصحيح
# =========================
mcp_app = mcp.http_app()
app.mount("/mcp", mcp_app)

# =========================
# Dashboard
# =========================
@app.get("/dashboard")
async def dashboard():
    return {
        "name": "BeamMCP SaaS",
        "status": "running",
        "tools": 3
    }

# =========================
# Home
# =========================
@app.get("/")
async def home():
    return {"message": "BeamMCP is running"}

# =========================
# تشغيل السيرفر
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
