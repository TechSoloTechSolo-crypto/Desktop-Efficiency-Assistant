"""
悬浮工具条主窗体
================
这是整个程序的主界面，一个常驻桌面的悬浮小窗口。

特性：
  - 无边框（没有标题栏和关闭按钮，自己画一个）
  - 置顶（永远显示在其他窗口上面）
  - 可拖拽（鼠标按住窗口任意位置拖动）
  - 顶部一排按钮切换五大功能模块
"""
from PySide6.QtCore import QPoint, Qt   # QPoint 表示一个点；Qt 里有各种常量
from PySide6.QtGui import QMouseEvent    # 鼠标事件
from PySide6.QtWidgets import (
    QApplication,       # 应用对象，用来退出程序
    QHBoxLayout,        # 水平布局（从左到右）
    QLabel,             # 文本标签
    QPushButton,
    QStackedWidget,     # 堆叠布局：同一位置放多个页面，一次只显示一个
    QVBoxLayout,        # 垂直布局
    QWidget,            # 所有控件的基类
)

from src.config import APP_NAME, FLOAT_WINDOW_HEIGHT, FLOAT_WINDOW_WIDTH
from src.ui.modules import (
    ClipboardWidget,
    FileSearchWidget,
    ReminderWidget,
    ScheduleWidget,
    TaskWidget,
)

# 五大模块的名称，顺序要和下面 stack.addWidget 的顺序一致
MODULE_NAMES = ["剪贴板", "任务", "文件检索", "课表", "提醒"]


class FloatingMainWindow(QWidget):
    """悬浮工具条主窗体。"""

    def __init__(self) -> None:
        super().__init__()
        self._drag_pos: QPoint | None = None  # 记录鼠标按下时的位置，用于拖拽
        self._init_window()   # 设置窗口属性
        self._init_ui()       # 搭建界面

    def _init_window(self) -> None:
        """设置窗口的基本属性。"""
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(FLOAT_WINDOW_WIDTH, FLOAT_WINDOW_HEIGHT)  # 固定大小
        # setWindowFlags 设置窗口标志：
        #   FramelessWindowHint → 无边框
        #   WindowStaysOnTopHint → 永远置顶
        #   Tool → 不在任务栏显示图标
        # 多个标志用 | （按位或）组合
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

    def _init_ui(self) -> None:
        """搭建界面：标题栏 + 导航按钮 + 模块内容区。"""
        # 最外层用垂直布局，从上到下依次放：标题栏、导航、内容
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)  # 四周留 8 像素边距
        root.setSpacing(6)                   # 子元素之间间距 6 像素

        # ===== 标题栏（水平布局）=====
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel(APP_NAME)
        title_label.setStyleSheet("font-weight: bold; padding: 2px;")  # 加粗
        title_bar.addWidget(title_label)
        title_bar.addStretch()  # 弹簧：把后面的按钮推到右边
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        # 点击 ✕ → 退出整个应用
        close_btn.clicked.connect(QApplication.instance().quit)
        title_bar.addWidget(close_btn)
        root.addLayout(title_bar)

        # ===== 模块切换按钮（水平布局）=====
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(4)
        self.nav_buttons: list[QPushButton] = []
        for name in MODULE_NAMES:
            btn = QPushButton(name)
            btn.setCheckable(True)  # 可选中状态（选中后保持高亮）
            # 点击按钮 → 切换到对应模块
            # lambda 里的 n=name 是为了"捕获当前循环的 name"，避免闭包坑
            btn.clicked.connect(lambda checked, n=name: self._switch_module(n))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        root.addLayout(nav_layout)

        # ===== 模块内容区（堆叠布局）=====
        # QStackedWidget 像一叠卡片，一次只显示最上面那张
        self.stack = QStackedWidget()
        self.stack.addWidget(ClipboardWidget())    # 第 0 页
        self.stack.addWidget(TaskWidget())         # 第 1 页
        self.stack.addWidget(FileSearchWidget())   # 第 2 页
        self.stack.addWidget(ScheduleWidget())     # 第 3 页
        self.stack.addWidget(ReminderWidget())     # 第 4 页
        root.addWidget(self.stack)

        # 默认选中第一个模块
        self.nav_buttons[0].setChecked(True)

    def _switch_module(self, name: str) -> None:
        """
        切换到指定模块。

        逻辑：根据模块名找到它在列表中的索引，
        然后让 stack 显示对应页面，并更新按钮的选中状态。
        """
        index = MODULE_NAMES.index(name)
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)  # 只有当前模块的按钮是选中状态

    # ===== 下面三个方法实现"无边框窗口的拖拽" =====
    # 因为去掉了系统标题栏，所以要自己处理鼠标拖拽逻辑。

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """鼠标按下时记录位置。"""
        if event.button() == Qt.LeftButton:
            # globalPosition() 是鼠标在屏幕上的绝对位置
            # frameGeometry().topLeft() 是窗口左上角在屏幕上的位置
            # 两者相减 = 鼠标相对于窗口左上角的偏移量，拖动时保持这个偏移不变
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """鼠标移动时，如果按住左键就拖动窗口。"""
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            # 新的窗口位置 = 鼠标当前位置 - 之前记录的偏移量
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """鼠标松开时清除拖拽状态。"""
        self._drag_pos = None
