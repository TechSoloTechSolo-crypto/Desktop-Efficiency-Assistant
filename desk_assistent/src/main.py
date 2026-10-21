"""
桌面效率助手 - 程序入口
======================
这是整个程序的"大门"，从这里开始运行。

运行方式（在项目根目录下执行）：
    python -m src.main

为什么要用 `python -m src.main` 而不是直接 `python src/main.py`？
    因为项目里用了 `from src.xxx import ...` 这种"绝对导入"，
    用 `-m` 方式运行时，项目根目录会被加入 Python 路径，才能正确找到 src 包。
"""
import sys  # 用来返回退出码给操作系统

from src.app import run  # 从 app.py 导入启动函数


def main() -> None:
    """主函数：调用 run() 并把退出码传给操作系统。"""
    sys.exit(run())


# 下面这行的意思是：只有当这个文件被"直接运行"时才执行 main()
# 如果它被别的文件 import，则不会执行（避免 import 时意外启动程序）
if __name__ == "__main__":
    main()
