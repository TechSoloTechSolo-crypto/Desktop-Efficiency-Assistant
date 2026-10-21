"""
任务清单模块 UI
===============
显示任务列表，刷新查看。
"""
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.services import task_service


class TaskWidget(QWidget):
    """任务清单面板。"""

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
        """加载并显示所有任务。"""
        self.list_widget.clear()
        for task in task_service.list_all():
            # ✓ 已完成，○ 未完成；[P1/P2/P3] 表示优先级
            mark = "✓" if task.is_completed else "○"
            self.list_widget.addItem(
                QListWidgetItem(f"{mark} [P{task.priority}] {task.title}")
            )
