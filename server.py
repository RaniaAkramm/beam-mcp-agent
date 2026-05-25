from fastmcp import FastMCP
import os
from dotenv import load_dotenv
from beam_client import BeamClient 

# تحميل إعدادات البيئة
load_dotenv()

# تهيئة العميل (سيستخدم المفتاح من النظام فور توفره)
beam = BeamClient(api_key=os.environ.get("BEAM_API_KEY"))

# إنشاء خادم MCP
mcp = FastMCP("BeamMCP-Agent")

@mcp.tool()
def process_file(file_path: str) -> str:
    """إرسال ملف إلى منصة Beam للمعالجة"""
    # هذا الكود سيقوم بالاتصال الفعلي لاحقاً
    return f"جاري التجهيز لإرسال الملف {file_path} إلى منصة Beam..."

@mcp.tool()
def get_task_result(task_id: str) -> str:
    """الاستعلام عن حالة المهمة"""
    return f"جاري التحقق من حالة المهمة: {task_id}"

@mcp.tool()
def list_recent_tasks() -> str:
    """عرض سجل المهام الأخيرة"""
    return "لا توجد مهام حالياً."

if __name__ == "__main__":
    mcp.run()
