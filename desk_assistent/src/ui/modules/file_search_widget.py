"""
文件检索模块 UI
===============
提供搜索框和结果列表。
"""
from PySide6.QtWidgets import (
    QLineEdit,        # 单行输入框
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.services import file_search_service


class FileSearchWidget(QWidget):
    """文件检索面板。"""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入文件名关键词...")  # 灰色提示文字
        # 按回车键也触发搜索
        self.search_input.returnPressed.connect(self._do_search)

        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.clicked.connect(self._do_search)

        # 结果列表
        self.result_list = QListWidget()

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.result_list)

    def _do_search(self) -> None:
        """执行搜索，把结果显示到列表。"""
        keyword = self.search_input.text().strip()  # 去掉首尾空格
        self.result_list.clear()
        if not keyword:
            return  # 关键词为空就不搜
        for f in file_search_service.search(keyword):
            self.result_list.addItem(QListWidgetItem(f.file_path))
