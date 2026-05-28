import os
import uvicorn
from fastmcp import FastMCP
from dotenv import load_dotenv
import modal

# تم إضافة المكتبات التالية لدعم صفحة الويب
from fastapi import FastAPI
from fastapi.responses import FileResponse

# تحميل متغيرات البيئة
load_dotenv()

# إنشاء تطبيق FastMCP (كودك الأصلي)
mcp = FastMCP("BeamMCP-Agent")

# =========================
# Tools (كودك الأصلي كما هو)
# =========================

@mcp.tool()
def process_file(file_path: str) -> str:
    """إرسال ملف إلى Modal للمعالجة"""
    try:
        return f"تم إرسال الملف إلى Modal بنجاح: {file_path}"
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال بـ Modal: {str(e)}"

@mcp.tool()
def get_task_result(task_id: str) -> str:
    """الاستعلام عن حالة المهمة"""
    try:
        return f"جاري التحقق من المهمة: {task_id}"
    except Exception as e:
        return f"خطأ: {str(e)}"

@mcp.tool()
def list_recent_tasks() -> str:
    """عرض المهام الأخيرة"""
    try:
        return "لا توجد مهام حالياً."
    except Exception as e:
        return f"خطأ: {str(e)}"

# =========================
# تعديل لتقديم صفحة الويب
# =========================

# إنشاء تطبيق FastAPI
app = FastAPI()

# مسار لجلب ملف index.html
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# ربط الـ MCP بتطبيق الويب
app.mount("/mcp", mcp.app)

# =========================
# تشغيل السيرفر
# =========================

if __name__ == "__main__":
    # منفذ Railway
    port = int(os.environ.get("PORT", 8080))

    # تشغيل السيرفر باستخدام FastAPI
    uvicorn.run(app, host="0.0.0.0", port=port)
