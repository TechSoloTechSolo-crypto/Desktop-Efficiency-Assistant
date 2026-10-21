"""
QApplication 初始化与主循环
==========================
作用：真正"把窗口跑起来"的地方。
一个 PySide6 程序的标准启动流程：
    1. 创建 QApplication（整个 GUI 程序的"总管家"，只能有一个）
    2. 创建并显示主窗口
    3. 调用 app.exec() 进入事件循环（等待用户点击、输入等操作）
"""
import sys  # 用来拿到命令行参数 sys.argv，并在结束时返回退出码

from PySide6.QtWidgets import QApplication  # Qt 的应用程序对象

from src.config import APP_NAME, ORGANIZATION_NAME   # 应用名、组织名
from src.ui.main_window import FloatingMainWindow     # 悬浮工具条主窗体
from src.utils.logger import logger                   # 日志


def run() -> int:
    """
    启动应用并进入事件循环。

    返回值：
        int：程序退出码（0 表示正常退出）
    """
    logger.info("启动 %s", APP_NAME)

    # 第 1 步：创建 QApplication，必须传入命令行参数（Qt 会解析一些自己的参数）
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)            # 设置应用名（系统会用到）
    app.setOrganizationName(ORGANIZATION_NAME)  # 设置组织名

    # 第 2 步：创建主窗口并显示
    window = FloatingMainWindow()
    window.show()

    # 第 3 步：进入事件循环，程序会一直运行直到窗口被关闭
    # exec() 会阻塞在这里，直到程序退出，返回退出码
    return app.exec()
