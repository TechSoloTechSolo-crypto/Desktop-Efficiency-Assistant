"""
任务清单服务
============
封装任务的增删改查逻辑。
"""
from datetime import datetime
from typing import List, Optional

from src.config import TABLE_TASK
from src.database import TaskItem, db_manager
from src.utils.logger import logger


class TaskService:
    """任务清单的增删改查。"""

    def add(self, title: str, description: str = "", priority: int = 2,
            due_time: Optional[datetime] = None) -> int:
        """
        新增一个任务。

        参数：
            title       : 任务标题（必填）
            description : 任务描述
            priority    : 优先级 1高/2中/3低
            due_time    : 截止时间（可以没有）
        """
        with db_manager.get_connection() as conn:
            # 如果有截止时间就转成字符串存，没有就存 None
            due_str = due_time.isoformat(timespec="seconds") if due_time else None
            cur = conn.execute(
                f"INSERT INTO {TABLE_TASK} (title, description, priority, due_time, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (title, description, priority, due_str,
                 datetime.now().isoformat(timespec="seconds")),
            )
            task_id = cur.lastrowid
        logger.debug("新增任务 #%d", task_id)
        return task_id

    def list_all(self, only_pending: bool = False) -> List[TaskItem]:
        """
        查询所有任务。

        参数：
            only_pending: True 时只返回未完成的任务
        返回：
            按优先级升序、创建时间倒序排列的任务列表
        """
        sql = f"SELECT * FROM {TABLE_TASK}"
        if only_pending:
            sql += " WHERE is_completed = 0"
        sql += " ORDER BY priority ASC, created_at DESC"
        with db_manager.get_connection() as conn:
            rows = conn.execute(sql).fetchall()
        return [TaskItem(**dict(r)) for r in rows]

    def toggle_complete(self, task_id: int) -> None:
        """切换任务的"完成"状态。"""
        with db_manager.get_connection() as conn:
            conn.execute(
                f"UPDATE {TABLE_TASK} SET is_completed = 1 - is_completed WHERE id = ?",
                (task_id,),
            )

    def delete(self, task_id: int) -> None:
        """删除一个任务。"""
        with db_manager.get_connection() as conn:
            conn.execute(f"DELETE FROM {TABLE_TASK} WHERE id = ?", (task_id,))


task_service = TaskService()
