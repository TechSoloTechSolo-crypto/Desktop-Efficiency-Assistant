"""
五大功能模块 UI 包
=================
统一导出五个模块的 Widget，方便主窗体 import。
"""
from src.ui.modules.clipboard_widget import ClipboardWidget
from src.ui.modules.file_search_widget import FileSearchWidget
from src.ui.modules.reminder_widget import ReminderWidget
from src.ui.modules.schedule_widget import ScheduleWidget
from src.ui.modules.task_widget import TaskWidget

__all__ = [
    "ClipboardWidget",
    "TaskWidget",
    "FileSearchWidget",
    "ScheduleWidget",
    "ReminderWidget",
]
