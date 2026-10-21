"""
课表服务
========
封装课表的增删改查。
"""
from typing import List

from src.config import TABLE_SCHEDULE
from src.database import ScheduleItem, db_manager
from src.utils.logger import logger


class ScheduleService:
    """课表的增删改查。"""

    def add(self, course_name: str, day_of_week: int, start_time: str,
            end_time: str, location: str = "", week_start: int = 1,
            week_end: int = 16) -> int:
        """
        新增一门课。

        参数：
            course_name : 课程名
            day_of_week : 星期几（1-7）
            start_time  : 开始时间 "HH:MM"
            end_time    : 结束时间 "HH:MM"
            location    : 上课地点
            week_start  : 起始周
            week_end    : 结束周
        """
        with db_manager.get_connection() as conn:
            cur = conn.execute(
                f"INSERT INTO {TABLE_SCHEDULE} "
                "(course_name, day_of_week, start_time, end_time, location, week_start, week_end) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (course_name, day_of_week, start_time, end_time, location,
                 week_start, week_end),
            )
            item_id = cur.lastrowid
        logger.debug("新增课表 #%d", item_id)
        return item_id

    def list_all(self) -> List[ScheduleItem]:
        """查询所有课程，按星期和时间排序。"""
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                f"SELECT * FROM {TABLE_SCHEDULE} ORDER BY day_of_week, start_time"
            ).fetchall()
        return [ScheduleItem(**dict(r)) for r in rows]

    def get_by_day(self, day_of_week: int) -> List[ScheduleItem]:
        """查询某一天（星期几）的所有课程。"""
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                f"SELECT * FROM {TABLE_SCHEDULE} WHERE day_of_week = ? ORDER BY start_time",
                (day_of_week,),
            ).fetchall()
        return [ScheduleItem(**dict(r)) for r in rows]

    def delete(self, item_id: int) -> None:
        """删除一条课表记录。"""
        with db_manager.get_connection() as conn:
            conn.execute(f"DELETE FROM {TABLE_SCHEDULE} WHERE id = ?", (item_id,))


schedule_service = ScheduleService()
