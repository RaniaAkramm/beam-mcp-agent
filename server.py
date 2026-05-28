import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastmcp import FastMCP

from dotenv import load_dotenv

# =========================================
# Load environment
# =========================================
load_dotenv()

# =========================================
# FastAPI app
# =========================================
app = FastAPI(title="BeamMCP")

# =========================================
# MCP server
# =========================================
mcp = FastMCP("BeamMCP-Agent")

# =========================================
# TOOLS
# =========================================

@mcp.tool()
def process_file(file_path: str) -> str:
    return f"تم معالجة الملف: {file_path}"


@mcp.tool()
def get_task_result(task_id: str) -> str:
    return f"حالة المهمة: {task_id}"


@mcp.tool()
def list_recent_tasks() -> str:
    return "لا توجد مهام حالياً"


# =========================================
# MCP mount (IMPORTANT FIX)
# =========================================

mcp_app = mcp.http_app()

# ❌ كان /mcp/ws (خطأ)
# ✔ الصحيح /mcp
app.mount("/mcp", mcp_app)


# =========================================
# Info endpoint (optional)
# =========================================

@app.get("/mcp/info")
async def mcp_info():
    return JSONResponse({
        "name": "BeamMCP-Agent",
        "status": "online",
        "protocol": "mcp-streamable-http",
        "endpoint": "/mcp",
        "website": "https://BeamMCP.com"
    })


# =========================================
# Home page (optional)
# =========================================

@app.get("/")
async def home():
    return {"message": "BeamMCP is running"}


# =========================================
# Run server
# =========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
