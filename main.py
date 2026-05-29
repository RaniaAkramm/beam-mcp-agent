import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY", "beam-123456")

mcp = FastMCP("BeamMCP-Agent")

@mcp.tool()
def search_domain(domain: str) -> dict:
    return {"domain": domain, "available": True, "price": "$12"}

@mcp.tool()
def analyze_text(text: str) -> dict:
    return {"length": len(text), "summary": text[:50]}

@mcp.tool()
def generate_report(name: str) -> dict:
    return {"project": name, "status": "generated", "score": 90}

app = FastAPI(title="BeamMCP SaaS")

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

app.mount("/mcp", mcp.http_app())

@app.get("/dashboard")
async def dashboard():
    return {"name": "BeamMCP", "status": "running", "tools": 3}

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>BeamMCP</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: #03060d;
                color: #fff;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .hero {
                text-align: center;
                padding: 60px 20px;
            }
            h1 { font-size: 48px; color: #00ff88; margin-bottom: 16px; }
            .subtitle { font-size: 20px; color: #aaa; margin-bottom: 40px; }
            .btn {
                background: #00ff88;
                color: #000;
                padding: 14px 32px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
                margin: 8px;
                display: inline-block;
            }
            .btn-outline {
                background: transparent;
                color: #00ff88;
                border: 2px solid #00ff88;
                padding: 12px 32px;
                border-radius: 8px;
                text-decoration: none;
                font-size: 16px;
                margin: 8px;
                display: inline-block;
            }
            .features {
                display: flex;
                gap: 24px;
                margin-top: 60px;
                flex-wrap: wrap;
                justify-content: center;
                padding: 0 20px;
            }
            .card {
                border: 1px solid #00ff8833;
                padding: 32px;
                border-radius: 12px;
                background: rgba(0,255,136,0.03);
                width: 260px;
                text-align: center;
            }
            .card h3 { color: #00ff88; margin-bottom: 12px; font-size: 18px; }
            .card p { color: #666; font-size: 14px; line-height: 1.6; }
            .icon { font-size: 36px; margin-bottom: 16px; }
        </style>
    </head>
    <body>
        <div class="hero">
            <h1>⚡ BeamMCP</h1>
            <p class="subtitle">AI-Powered MCP Server & SaaS Platform</p>
            <a href="/dashboard" class="btn">Open Dashboard</a>
            <a href="/mcp" class="btn-outline">MCP Endpoint</a>
        </div>
        <div class="features">
            <div class="card">
                <div class="icon">🔍</div>
                <h3>Domain Search</h3>
                <p>Search and analyze domain availability instantly.</p>
            </div>
            <div class="card">
                <div class="icon">📊</div>
                <h3>Text Analysis</h3>
                <p>Analyze and summarize any text with AI tools.</p>
            </div>
            <div class="card">
                <div class="icon">📋</div>
                <h3>Report Generator</h3>
                <p>Generate detailed project reports automatically.</p>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
