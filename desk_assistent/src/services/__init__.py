"""
业务逻辑服务层包
================
把五个模块的 service 单例统一导出，
UI 层只要 `from src.services import xxx_service` 即可使用。
"""
from src.services.clipboard_service import clipboard_service
from src.services.file_search_service import file_search_service
from src.services.reminder_service import reminder_service
from src.services.schedule_service import schedule_service
from src.services.task_service import task_service

__all__ = [
    "clipboard_service",
    "task_service",
    "file_search_service",
    "schedule_service",
    "reminder_service",
]
