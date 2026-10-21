"""
课表模块 UI
==========
显示课程列表。
"""
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.services import schedule_service

# 把数字 1-7 映射成中文星期名
DAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


class ScheduleWidget(QWidget):
    """课表面板。"""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()
        self.refresh()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.refresh_btn)

    def refresh(self) -> None:
        """加载并显示所有课程。"""
        self.list_widget.clear()
        for item in schedule_service.list_all():
            day = DAY_NAMES[item.day_of_week - 1]  # 1→周一，所以索引要 -1
            self.list_widget.addItem(
                QListWidgetItem(
                    f"{day} {item.start_time}-{item.end_time} "
                    f"{item.course_name} @ {item.location}"
                )
            )
