"""
文件检索服务
============
负责：扫描指定目录建立文件索引，以及按关键词搜索文件。
"""
from datetime import datetime
from pathlib import Path       # 处理文件路径的标准库
from typing import List

from src.config import TABLE_FILE_INDEX
from src.database import FileIndex, db_manager
from src.utils.logger import logger


class FileSearchService:
    """文件索引与检索。"""

    def index_directory(self, directory: str, extensions: List[str] = None) -> int:
        """
        扫描指定目录，把文件信息存入索引表。

        参数：
            directory  : 要扫描的目录路径
            extensions : 只索引这些后缀的文件，默认索引常见文档和代码文件
        返回：
            int: 新增或更新的文件条数
        """
        if extensions is None:
            extensions = [".txt", ".docx", ".xlsx", ".pdf", ".py", ".md"]

        count = 0
        # rglob("*") 递归遍历目录下所有文件和子目录
        for path in Path(directory).rglob("*"):
            # 只处理文件（跳过目录），且后缀在白名单里
            if not path.is_file() or path.suffix.lower() not in extensions:
                continue
            try:
                # 把文件的最后修改时间转成字符串
                mtime = datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")
            except OSError:
                mtime = None  # 读取失败就存空

            # INSERT OR REPLACE：如果路径已存在就更新，不存在就插入
            with db_manager.get_connection() as conn:
                conn.execute(
                    f"INSERT OR REPLACE INTO {TABLE_FILE_INDEX} "
                    "(file_path, file_name, file_type, last_modified) VALUES (?, ?, ?, ?)",
                    (str(path), path.name, path.suffix.lower(), mtime),
                )
            count += 1

        logger.info("索引目录完成，新增/更新 %d 条", count)
        return count

    def search(self, keyword: str, limit: int = 50) -> List[FileIndex]:
        """
        按文件名关键词搜索。

        参数：
            keyword: 搜索关键词
            limit  : 最多返回多少条
        """
        with db_manager.get_connection() as conn:
            # LIKE 模糊匹配，% 表示任意字符，所以 %关键词% 表示"包含关键词"
            rows = conn.execute(
                f"SELECT * FROM {TABLE_FILE_INDEX} WHERE file_name LIKE ? LIMIT ?",
                (f"%{keyword}%", limit),
            ).fetchall()
        return [FileIndex(**dict(r)) for r in rows]


file_search_service = FileSearchService()
