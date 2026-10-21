"""
消息提醒服务
============
封装提醒的增删改查，以及"检查是否有到点提醒"。
"""
from datetime import datetime
from typing import List, Optional

from src.config import TABLE_REMINDER
from src.database import ReminderItem, db_manager
from src.utils.logger import logger


class ReminderService:
    """消息提醒的增删改查与触发检查。"""

    def add(self, title: str, content: str = "",
            remind_time: Optional[datetime] = None) -> int:
        """
        新增一条提醒。

        参数：
            title      : 提醒标题
            content    : 提醒内容
            remind_time: 提醒时间（到点会触发）
        """
        with db_manager.get_connection() as conn:
            time_str = remind_time.isoformat(timespec="seconds") if remind_time else None
            cur = conn.execute(
                f"INSERT INTO {TABLE_REMINDER} (title, content, remind_time, created_at) "
                "VALUES (?, ?, ?, ?)",
                (title, content, time_str,
                 datetime.now().isoformat(timespec="seconds")),
            )
            item_id = cur.lastrowid
        logger.debug("新增提醒 #%d", item_id)
        return item_id

    def list_pending(self) -> List[ReminderItem]:
        """
        查询所有"到点且还没触发"的提醒。

        逻辑：
            - 还没触发过（is_triggered = 0）
            - 有提醒时间
            - 提醒时间 <= 当前时间
        """
        now = datetime.now().isoformat(timespec="seconds")
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                f"SELECT * FROM {TABLE_REMINDER} "
                "WHERE is_triggered = 0 AND remind_time IS NOT NULL AND remind_time <= ? "
                "ORDER BY remind_time",
                (now,),
            ).fetchall()
        return [ReminderItem(**dict(r)) for r in rows]

    def mark_triggered(self, item_id: int) -> None:
        """把某条提醒标记为"已触发"，避免重复提醒。"""
        with db_manager.get_connection() as conn:
            conn.execute(
                f"UPDATE {TABLE_REMINDER} SET is_triggered = 1 WHERE id = ?",
                (item_id,),
            )

    def list_all(self) -> List[ReminderItem]:
        """查询所有提醒，按创建时间倒序。"""
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                f"SELECT * FROM {TABLE_REMINDER} ORDER BY created_at DESC"
            ).fetchall()
        return [ReminderItem(**dict(r)) for r in rows]


reminder_service = ReminderService()
