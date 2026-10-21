"""
数据库层包
==========
作用：把 db_manager 和各个数据模型统一导出，
其他模块只要 `from src.database import xxx` 即可使用。
"""
from src.database.db_manager import db_manager
from src.database.models import (
    ClipboardItem,
    FileIndex,
    ReminderItem,
    ScheduleItem,
    TaskItem,
)

__all__ = [
    "db_manager",
    "ClipboardItem",
    "TaskItem",
    "FileIndex",
    "ScheduleItem",
    "ReminderItem",
]
