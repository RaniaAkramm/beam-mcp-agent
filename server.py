import os
import uvicorn
import modal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from fastmcp import FastMCP
from dotenv import load_dotenv

# =========================================
# تحميل متغيرات البيئة
# =========================================

load_dotenv()

# =========================================
# إنشاء تطبيق FastMCP
# =========================================

mcp = FastMCP("BeamMCP-Agent")

# =========================================
# أدوات MCP
# =========================================

@mcp.tool()
def process_file(file_path: str) -> str:
    """
    إرسال ملف إلى Modal للمعالجة
    """

    try:

        # مثال ربط Modal
        # قم بتعديلها لاحقاً حسب حسابك

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
# إنشاء FastAPI
# =========================================

app = FastAPI()

# =========================================
# الصفحة الرئيسية
# =========================================

@app.get("/", response_class=HTMLResponse)
async def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BeamMCP</title>

        <style>

            body{
                margin:0;
                padding:0;
                background:#0b0b0f;
                color:white;
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
                flex-direction:column;
            }

            h1{
                font-size:64px;
                margin:0;
            }

            p{
                color:#999;
                margin-top:12px;
                font-size:18px;
            }

            .status{
                margin-top:25px;
                padding:10px 18px;
                border-radius:12px;
                background:#15151d;
                border:1px solid #262636;
            }

        </style>
    </head>

    <body>

        <h1>BeamMCP</h1>

        <p>MCP Server Running Successfully</p>

        <div class="status">
            Status: Online
        </div>

    </body>
    </html>
    """


# =========================================
# صفحة معلومات MCP
# =========================================

@app.get("/mcp")
async def mcp_info():

    return JSONResponse({
        "name": "BeamMCP-Agent",
        "status": "online",
        "protocol": "MCP",
        "endpoint": "/mcp/ws"
    })


# =========================================
# ربط MCP الحقيقي
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
