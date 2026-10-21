"""
SQLite 数据库连接管理与建表
==========================
作用：
  1. 第一次使用时自动创建数据库文件和所有表
  2. 提供"获取数据库连接"的统一入口

为什么用 SQLite？
  它是"文件型数据库"，整个数据库就是一个 .db 文件，不需要单独装数据库服务器，
  非常适合桌面小工具。Python 自带 sqlite3 模块，开箱即用。
"""
import sqlite3                            # Python 内置的 SQLite 操作库
from contextlib import contextmanager     # 用来写"上下文管理器"（配合 with 使用）
from typing import Iterator               # 类型标注：表示返回一个迭代器

from src.config import (
    DB_PATH,
    TABLE_CLIPBOARD,
    TABLE_FILE_INDEX,
    TABLE_REMINDER,
    TABLE_SCHEDULE,
    TABLE_TASK,
)
from src.utils.logger import logger


class DatabaseManager:
    """数据库管理器：负责建表与连接。"""

    def __init__(self, db_path: str = str(DB_PATH)) -> None:
        """
        初始化时保存数据库路径，并立即创建表。

        参数：
            db_path: 数据库文件路径，默认用配置里的路径。
                     留个参数是为了方便测试时传入临时数据库。
        """
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self) -> None:
        """
        创建所有数据表（如果它们还不存在的话）。

        IF NOT EXISTS 的含义：表已存在就跳过，不会报错，所以每次启动都能安全调用。
        """
        # with 语句会自动调用 get_connection() 拿到连接，结束后自动 commit + 关闭
        with self.get_connection() as conn:
            # executescript 可以一次执行多条 SQL 语句（用分号分隔）
            conn.executescript(f"""
            -- 剪贴板历史表
            CREATE TABLE IF NOT EXISTS {TABLE_CLIPBOARD} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- 主键，自增
                content_type TEXT NOT NULL DEFAULT 'text',
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,                -- 时间存成字符串（ISO 格式）
                is_pinned INTEGER NOT NULL DEFAULT 0     -- SQLite 没有布尔型，用 0/1 表示
            );

            -- 任务清单表
            CREATE TABLE IF NOT EXISTS {TABLE_TASK} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority INTEGER NOT NULL DEFAULT 2,
                due_time TEXT,                            -- 可以为空
                is_completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );

            -- 文件索引表
            CREATE TABLE IF NOT EXISTS {TABLE_FILE_INDEX} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,            -- 路径唯一，避免重复索引
                file_name TEXT NOT NULL,
                file_type TEXT DEFAULT '',
                last_modified TEXT
            );

            -- 课表
            CREATE TABLE IF NOT EXISTS {TABLE_SCHEDULE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                day_of_week INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                location TEXT DEFAULT '',
                week_start INTEGER NOT NULL DEFAULT 1,
                week_end INTEGER NOT NULL DEFAULT 16
            );

            -- 消息提醒表
            CREATE TABLE IF NOT EXISTS {TABLE_REMINDER} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT DEFAULT '',
                remind_time TEXT,
                is_triggered INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            """)
        logger.info("数据库表结构已就绪: %s", DB_PATH)

    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """
        获取数据库连接的上下文管理器。

        用法：
            with db_manager.get_connection() as conn:
                conn.execute("...")

        好处：
            - 正常执行完自动 commit（提交）
            - 出错自动 rollback（回滚）
            - 无论如何都会 close（关闭连接）
            - row_factory = sqlite3.Row 让查询结果可以用列名访问
        """
        conn = sqlite3.connect(self.db_path)   # 连接（或创建）数据库
        conn.row_factory = sqlite3.Row         # 让查询结果像字典一样用 r["列名"] 访问
        try:
            yield conn                         # 把连接交给 with 里的代码使用
            conn.commit()                      # 正常结束 → 提交
        except Exception:
            conn.rollback()                     # 出异常 → 回滚（撤销未提交的改动）
            raise                              # 继续把异常抛出去
        finally:
            conn.close()                       # 最后一定关闭连接


# 创建一个全局单例，其他地方直接 `from src.database import db_manager` 就能用
db_manager = DatabaseManager()
