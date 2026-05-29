import os
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastmcp import FastMCP
from dotenv import load_dotenv

# =========================
# ENV
# =========================
load_dotenv()
API_KEY = os.getenv("API_KEY", "beam-123456")

# =========================
# MCP SERVER
# =========================
mcp = FastMCP("BeamMCP-Agent")

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
# LIFESPAN (المهم للإصلاح)
# =========================
mcp_app = mcp.http_app()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_app.router.lifespan_context(app):
        yield

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="BeamMCP SaaS", lifespan=lifespan)

# =========================
# API KEY MIDDLEWARE (مصحح)
# =========================
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    path = request.url.path
    # حماية /mcp فقط ما عدا health check
    if path.startswith("/mcp") and path != "/mcp/health":
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

# =========================
# MCP MOUNT
# =========================
app.mount("/mcp", mcp_app)

# =========================
# DASHBOARD
# =========================
@app.get("/dashboard")
async def dashboard():
    return {
        "name": "BeamMCP SaaS",
        "status": "running",
        "tools": ["search_domain", "analyze_text", "generate_report"]
    }

# =========================
# HOME PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>BeamMCP</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #03060d;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .card {
                border: 1px solid #00ff88;
                padding: 40px;
                border-radius: 12px;
                background: rgba(0,255,136,0.05);
            }
            h1 { color: #00ff88; margin-bottom: 10px; }
            p { color: #aaa; }
            a { color: #00c2ff; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 BeamMCP is Running</h1>
            <p>MCP Server + AI Tools + SaaS Platform</p>
            <p><a href="/dashboard">Open Dashboard</a></p>
        </div>
    </body>
    </html>
    """

# =========================
# START
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
