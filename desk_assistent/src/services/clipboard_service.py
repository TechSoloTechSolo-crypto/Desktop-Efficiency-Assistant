"""
剪贴板历史服务
==============
作用：封装剪贴板记录的"增删改查"（CRUD）。
UI 层不直接操作数据库，而是调用这里的方法，这样职责清晰、好维护。
"""
from datetime import datetime   # 用来生成当前时间
from typing import List         # 类型标注：返回列表

from src.config import TABLE_CLIPBOARD
from src.database import ClipboardItem, db_manager
from src.utils.logger import logger


class ClipboardService:
    """剪贴板历史记录的增删改查。"""

    def add(self, content: str, content_type: str = "text") -> int:
        """
        新增一条剪贴板记录。

        参数：
            content      : 剪贴板内容
            content_type : 内容类型，默认 text
        返回：
            int : 新记录的 id
        """
        # 用 with 拿到数据库连接，执行 INSERT
        with db_manager.get_connection() as conn:
            # ? 是参数占位符，防止 SQL 注入，也避免字符串里有引号导致语法错误
            cur = conn.execute(
                f"INSERT INTO {TABLE_CLIPBOARD} (content_type, content, created_at) "
                "VALUES (?, ?, ?)",
                (content_type, content, datetime.now().isoformat(timespec="seconds")),
            )
            item_id = cur.lastrowid  # lastrowid 拿到刚插入记录的自增 id
        logger.debug("新增剪贴板记录 #%d", item_id)
        return item_id

    def list_all(self, limit: int = 100) -> List[ClipboardItem]:
        """
        查询所有剪贴板记录。

        参数：
            limit: 最多返回多少条，默认 100
        返回：
            List[ClipboardItem]: 记录列表，置顶的在前，然后按时间倒序
        """
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                f"SELECT * FROM {TABLE_CLIPBOARD} ORDER BY is_pinned DESC, created_at DESC LIMIT ?",
                (limit,),  # 注意：即使只有一个参数，也要写成元组 (limit,)
            ).fetchall()
        # 把数据库行转成 ClipboardItem 对象
        # dict(r) 把 Row 转成字典，** 解包传给 dataclass 构造函数
        return [ClipboardItem(**dict(r)) for r in rows]

    def delete(self, item_id: int) -> None:
        """根据 id 删除一条剪贴板记录。"""
        with db_manager.get_connection() as conn:
            conn.execute(f"DELETE FROM {TABLE_CLIPBOARD} WHERE id = ?", (item_id,))
        logger.debug("删除剪贴板记录 #%d", item_id)

    def toggle_pin(self, item_id: int) -> None:
        """切换某条记录的"钉住"状态（钉 ↔ 不钉）。"""
        with db_manager.get_connection() as conn:
            # 1 - is_pinned：原来是 0 变 1，原来是 1 变 0
            conn.execute(
                f"UPDATE {TABLE_CLIPBOARD} SET is_pinned = 1 - is_pinned WHERE id = ?",
                (item_id,),
            )


# 创建全局单例，其他地方直接 from src.services import clipboard_service
clipboard_service = ClipboardService()
