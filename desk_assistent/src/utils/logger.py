"""
日志工具模块
============
作用：让程序在运行时能"记日记"，方便出问题时排查。
日志会同时输出到两个地方：
  1. 控制台（运行程序时看到的黑色窗口）
  2. 文件（data/desk_assistent.log，程序关掉后仍保留）
"""
import logging                       # Python 标准日志库
import sys                           # 用来拿到标准输出（控制台）
from logging.handlers import RotatingFileHandler  # 文件日志：文件太大自动轮转

from src.config import LOG_PATH      # 从配置里拿日志文件路径


def setup_logger(name: str = "desk_assistent", level: int = logging.INFO) -> logging.Logger:
    """
    配置并返回一个 logger 对象。

    参数：
        name : 日志的名字（可以理解为这条日志属于谁）
        level: 日志级别，INFO 表示记录"一般信息"及以上（还包括 WARNING、ERROR）

    为什么加 if 判断？
        因为这个函数可能被多次调用，如果不判断，每次都会重复添加"输出渠道"，
        导致同一条日志被打印好几遍。
    """
    logger = logging.getLogger(name)   # 拿到（或新建）一个名为 name 的 logger
    if logger.handlers:                # 如果已经配置过输出渠道，就直接返回
        return logger

    logger.setLevel(level)             # 设置日志级别

    # 定义日志的显示格式：时间 [级别] 名字: 消息内容
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",   # 时间格式：年-月-日 时:分:秒
    )

    # 渠道 1：输出到控制台（sys.stdout 就是控制台）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 渠道 2：输出到文件
    # maxBytes=2MB：单个日志文件最大 2MB；backupCount=5：最多保留 5 个旧文件
    # 超过大小后，旧文件会重命名为 .log.1、.log.2……自动轮转，避免日志无限变大
    file_handler = RotatingFileHandler(
        LOG_PATH, maxBytes=2 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# 创建一个全局可用的 logger，其他文件只要 `from src.utils.logger import logger` 就能用
logger = setup_logger()
