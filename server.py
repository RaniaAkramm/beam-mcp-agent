import os
import uvicorn
import modal

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from fastmcp import FastMCP
from dotenv import load_dotenv

# =========================================
# تحميل متغيرات البيئة
# =========================================

load_dotenv()

# =========================================
# إنشاء FastAPI
# =========================================

app = FastAPI()

# =========================================
# إنشاء MCP
# =========================================

mcp = FastMCP("BeamMCP-Agent")

# =========================================
# MCP Tools
# =========================================

@mcp.tool()
def process_file(file_path: str) -> str:
    """
    إرسال ملف إلى Modal للمعالجة
    """

    try:

        # مثال ربط Modal
        # عدلها لاحقاً حسب حسابك

        # f = modal.Function.lookup(
        #     "your-modal-app",
        #     "process_file"
        # )

        # result = f.remote(file_path)

        return f"تم إرسال الملف إلى Modal بنجاح: {file_path}"

    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بـ Modal: {str(e)}"


@mcp.tool()
def get_task_result(task_id: str) -> str:
    """
    الاستعلام عن حالة المهمة
    """

    try:
        return f"جاري التحقق من المهمة: {task_id}"

    except Exception as e:
        return f"خطأ: {str(e)}"


@mcp.tool()
def list_recent_tasks() -> str:
    """
    عرض المهام الأخيرة
    """

    try:
        return "لا توجد مهام حالياً."

    except Exception as e:
        return f"خطأ: {str(e)}"


# =========================================
# الصفحة الرئيسية
# =========================================

@app.get("/")
async def home():

    return FileResponse("index.html")


# =========================================
# صفحة معلومات MCP
# =========================================

@app.get("/mcp")
async def mcp_info():

    return JSONResponse({
        "name": "BeamMCP-Agent",
        "status": "online",
        "protocol": "MCP",
        "endpoint": "/mcp/ws",
        "website": "https://BeamMCP.com"
    })


# =========================================
# MCP الحقيقي
# =========================================

mcp_app = mcp.http_app()

app.mount("/mcp/ws", mcp_app)

# =========================================
# تشغيل السيرفر
# =========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
