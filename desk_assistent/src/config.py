"""
全局配置文件
============
作用：把整个项目里会反复用到的"常量"集中放在这里，方便统一修改。
比如数据库存在哪、窗口多大、各个表叫什么名字……
其他文件需要这些值时，只要 `from src.config import XXX` 即可。
"""
import os  # 操作系统接口，用来读取环境变量
from pathlib import Path  # Path 是比字符串更方便的"路径"类型


# ===== 路径相关 =====

# 项目根目录：当前这个 config.py 在 src/ 下，
# parent 是上一级（项目根），resolve() 转成绝对路径。
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# 数据存储目录：默认放在项目下的 data/ 文件夹。
# 也支持通过环境变量 DESK_ASSISTENT_DATA 自定义位置（方便打包后使用）。
DATA_DIR: Path = Path(os.environ.get("DESK_ASSISTENT_DATA", PROJECT_ROOT / "data"))
# mkdir 创建目录，parents=True 表示上级目录不存在也一起建，exist_ok=True 表示已存在不报错。
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite 数据库文件的完整路径
DB_PATH: Path = DATA_DIR / "desk_assistent.db"

# 日志文件路径（程序运行时的"日记"）
LOG_PATH: Path = DATA_DIR / "desk_assistent.log"


# ===== 应用基本信息 =====

APP_NAME: str = "桌面效率助手"          # 应用名称，会显示在窗口标题等地方
APP_VERSION: str = "0.1.0"              # 版本号
ORGANIZATION_NAME: str = "G06"          # 组织/小组名


# ===== 悬浮窗默认参数 =====

FLOAT_WINDOW_WIDTH: int = 400           # 悬浮工具条宽度（像素）
FLOAT_WINDOW_HEIGHT: int = 600          # 悬浮工具条高度（像素）
FLOAT_WINDOW_OPACITY: float = 0.95      # 透明度（0~1，1 为完全不透明）


# ===== 数据库表名 =====
# 把表名定义成常量，避免在代码里到处写字符串，写错了不好查。
TABLE_CLIPBOARD: str = "clipboard_history"   # 剪贴板历史表
TABLE_TASK: str = "tasks"                    # 任务清单表
TABLE_FILE_INDEX: str = "file_index"         # 文件索引表
TABLE_SCHEDULE: str = "schedule"             # 课表
TABLE_REMINDER: str = "reminders"            # 提醒表
