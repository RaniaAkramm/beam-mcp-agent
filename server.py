import os
import uvicorn

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
# FASTAPI APP
# =========================
app = FastAPI(title="BeamMCP SaaS")

# =========================
# API KEY PROTECTION (MCP ONLY)
# =========================
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

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
# MCP ENDPOINT
# =========================
mcp_app = mcp.http_app()
app.mount("/mcp", mcp_app)

# =========================
# DASHBOARD (JSON)
# =========================
@app.get("/dashboard")
async def dashboard():
    return {
        "name": "BeamMCP SaaS",
        "status": "running",
        "tools": 3
    }

# =========================
# HOME PAGE (HTML FIX - IMPORTANT)
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
            h1 {
                color: #00ff88;
                margin-bottom: 10px;
            }
            p {
                color: #aaa;
            }
            a {
                color: #00c2ff;
                text-decoration: none;
            }
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
# START SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
