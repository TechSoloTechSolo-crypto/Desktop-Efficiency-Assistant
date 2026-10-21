"""
数据模型定义
============
作用：用 dataclass 定义项目里的"数据长什么样"。
dataclass 是 Python 3.7+ 的语法糖，帮我们自动生成 __init__、__repr__ 等方法，
不用手写一堆样板代码。

比如一条任务，它有标题、描述、优先级、截止时间…… 这些字段就在 TaskItem 里定义。
"""
from dataclasses import dataclass, field  # dataclass 装饰器；field 用来给字段设置默认值
from datetime import datetime             # 日期时间类型
from typing import Optional               # Optional[X] 表示"可以是 X，也可以是 None"


@dataclass
class ClipboardItem:
    """一条剪贴板历史记录。"""
    id: Optional[int] = None        # 记录编号（数据库自增，新建时为 None）
    content_type: str = "text"      # 内容类型：text(文本) / image(图片) / file(文件)
    content: str = ""               # 剪贴板内容
    created_at: datetime = field(default_factory=datetime.now)  # 创建时间，默认"现在"
    is_pinned: bool = False         # 是否被"钉住"（置顶收藏）


@dataclass
class TaskItem:
    """一条任务清单项。"""
    id: Optional[int] = None
    title: str = ""                 # 任务标题
    description: str = ""           # 任务描述（详细内容）
    priority: int = 2               # 优先级：1高 / 2中 / 3低
    due_time: Optional[datetime] = None  # 截止时间（可以没有）
    is_completed: bool = False      # 是否已完成
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class FileIndex:
    """一条文件索引记录（用于文件检索）。"""
    id: Optional[int] = None
    file_path: str = ""             # 文件完整路径
    file_name: str = ""             # 文件名
    file_type: str = ""             # 文件扩展名（如 .docx）
    last_modified: Optional[datetime] = None  # 最后修改时间


@dataclass
class ScheduleItem:
    """一条课表记录。"""
    id: Optional[int] = None
    course_name: str = ""           # 课程名称
    day_of_week: int = 1            # 星期几：1=周一 ... 7=周日
    start_time: str = ""            # 开始时间，格式 "HH:MM"
    end_time: str = ""              # 结束时间
    location: str = ""              # 上课地点
    week_start: int = 1             # 起始周
    week_end: int = 16              # 结束周


@dataclass
class ReminderItem:
    """一条消息提醒。"""
    id: Optional[int] = None
    title: str = ""                 # 提醒标题
    content: str = ""               # 提醒内容
    remind_time: Optional[datetime] = None  # 提醒时间
    is_triggered: bool = False      # 是否已触发（提醒过了）
    created_at: datetime = field(default_factory=datetime.now)
