# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/11/30
# @File Name: logger.py

from colorlog import ColoredFormatter
from lib.read_config import read_config
import logging.handlers
import time

level = read_config()[2]['level']

date_format = '%H:%M:%S'
info_format_console = '%(log_color)s[%(asctime)s] |%(filename)s[%(lineno)-3s] |%(levelname)-8s |%(message)s'
info_format_file = '[%(asctime)s] |%(filename)s[%(funcName)sline:%(lineno)d] |%(levelname)-8s |%(message)s'
formatter = ColoredFormatter(fmt=info_format_console,
                             datefmt=date_format,
                             reset=True,
                             log_colors={
                                 'DEBUG': 'light_purple',
                                 'INFO': 'light_cyan',
                                 'WARNING': 'yellow',
                                 'ERROR': 'red',
                                 'CRITICAL': 'red,bold_red'})
formatter_file = logging.Formatter(fmt=info_format_file,
                                   datefmt=date_format)

Logger = logging.getLogger('MainLogger')

if level == 'DEBUG':
    Logger.setLevel(logging.DEBUG)
elif level == 'INFO':
    Logger.setLevel(logging.INFO)
elif level == 'WARNING':
    Logger.setLevel(logging.WARNING)
elif level == 'ERROR':
    Logger.setLevel(logging.ERROR)
elif level == 'CRITICAL':
    Logger.setLevel(logging.CRITICAL)
else:
    Logger.setLevel(logging.DEBUG)

ConsoleLogger = logging.StreamHandler()  # 输出到终端
ConsoleLogger.setFormatter(formatter)
log_name = time.strftime('%Y-%m-%d#%H')  # 一小时内使用的日志文件都是同一个
FileLogger = logging.handlers.RotatingFileHandler(filename=f'./logs/{log_name}.log',
                                                  maxBytes=102400,
                                                  backupCount=5)  # 每个日志文件最大102400字节(100Kb)
FileLogger.setFormatter(formatter_file)
Logger.addHandler(ConsoleLogger)
Logger.addHandler(FileLogger)
