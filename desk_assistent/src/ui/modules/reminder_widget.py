"""
消息提醒模块 UI
===============
显示提醒列表。
"""
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.services import reminder_service


class ReminderWidget(QWidget):
    """消息提醒面板。"""

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
        """加载并显示所有提醒。"""
        self.list_widget.clear()
        for item in reminder_service.list_all():
            state = "已提醒" if item.is_triggered else "待提醒"
            self.list_widget.addItem(
                QListWidgetItem(f"[{state}] {item.title}")
            )
