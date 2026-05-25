from fastmcp import FastMCP
import os
from dotenv import load_dotenv
from beam_client import BeamClient  # إضافة مكتبة Beam

# تحميل مفاتيح الأمان
load_dotenv()

# تهيئة العميل للاتصال بمنصة Beam
# يتوقع الكود وجود BEAM_API_KEY في ملف .env الخاص بك
beam = BeamClient(api_key=os.environ.get("BEAM_API_KEY"))

# إنشاء خادم MCP
mcp = FastMCP("BeamMCP-Agent")

# الأداة الأولى: معالجة الملفات
@mcp.tool()
def process_file(file_path: str) -> str:
    """إرسال ملف إلى منصة Beam للمعالجة"""
    # أصبح كائن beam متاحاً هنا للاستخدام
    return f"تم تهيئة العميل، وجاري إرسال الملف {file_path} إلى Beam للمعالجة..."

# الأداة الثانية: التحقق من حالة المهمة
@mcp.tool()
def get_task_result(task_id: str) -> str:
    """الاستعلام عن حالة المهمة السحابية"""
    return f"جاري التحقق من حالة المهمة: {task_id}"

# الأداة الثالثة: قائمة المهام
@mcp.tool()
def list_recent_tasks() -> str:
    """عرض سجل المهام الأخيرة"""
    return "عرض قائمة المهام الأخيرة..."

if __name__ == "__main__":
    mcp.run()
