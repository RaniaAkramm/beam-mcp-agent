import os
import uvicorn
from fastmcp import FastMCP
from dotenv import load_dotenv
import modal

# 1. تحميل إعدادات البيئة من ملف .env (أو متغيرات النظام في Railway)
load_dotenv()

# 2. تهيئة تطبيق FastMCP
mcp = FastMCP("BeamMCP-Agent")

# 3. الأدوات (Tools)
@mcp.tool()
def process_file(file_path: str) -> str:
    """إرسال ملف إلى Modal للمعالجة"""
    try:
        # ملاحظة: تأكد أن اسم التطبيق والدالة موجودان في حساب Modal الخاص بك
        # f = modal.Function.lookup("اسم_تطبيقك_على_modal", "اسم_الدالة")
        # result = f.remote(file_path)
        
        return f"تم الاتصال بـ Modal بنجاح، جاري معالجة الملف: {file_path}"
    except Exception as e:
        return f"خطأ في الاتصال بـ Modal: {str(e)}"

@mcp.tool()
def get_task_result(task_id: str) -> str:
    """الاستعلام عن حالة المهمة"""
    return f"جاري التحقق من حالة المهمة في Modal: {task_id}"

@mcp.tool()
def list_recent_tasks() -> str:
    """عرض سجل المهام الأخيرة"""
    return "لا توجد مهام حالياً في السجل."

# 4. نقطة الدخول لتشغيل الخادم
if __name__ == "__main__":
    # الحصول على المنفذ من نظام Railway أو استخدام 8080 افتراضياً
    port = int(os.environ.get("PORT", 8080))
    # تشغيل الخادم باستخدام Uvicorn ليكون متوافقاً مع بروتوكول HTTP/WebSockets
    uvicorn.run(mcp.app, host="0.0.0.0", port=port)
