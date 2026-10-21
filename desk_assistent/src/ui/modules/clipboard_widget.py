"""
剪贴板历史模块 UI
=================
这是剪贴板功能的"界面"。
目前是骨架：显示历史记录列表 + 刷新按钮。
真实功能（监听剪贴板、搜索、收藏等）后续补充。
"""
# QListWidget 是列表控件，QPushButton 是按钮，QVBoxLayout 是垂直布局
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.services import clipboard_service  # 调用业务逻辑层，不直接碰数据库


class ClipboardWidget(QWidget):
    """剪贴板历史记录面板。"""

    def __init__(self) -> None:
        super().__init__()            # 必须先调用父类 QWidget 的初始化
        self._init_ui()               # 搭建界面
        self.refresh()                # 首次加载数据

    def _init_ui(self) -> None:
        """搭建界面控件。"""
        layout = QVBoxLayout(self)    # 垂直布局：从上到下排列
        self.list_widget = QListWidget()  # 用来显示剪贴板记录的列表
        self.refresh_btn = QPushButton("刷新")
        # 点击刷新按钮 → 调用 refresh 方法重新加载数据
        self.refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(self.list_widget)  # 列表加进布局
        layout.addWidget(self.refresh_btn)  # 按钮加进布局

    def refresh(self) -> None:
        """从数据库读取剪贴板记录并显示到列表里。"""
        self.list_widget.clear()              # 先清空列表
        for item in clipboard_service.list_all():
            # ★ 表示已钉住，□ 表示未钉住；内容太长只显示前 40 个字符
            text = f"[{'★' if item.is_pinned else ' '}] {item.content[:40]}"
            self.list_widget.addItem(QListWidgetItem(text))
