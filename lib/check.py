# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/11/30
# @File Name: check.py
import sys
from lib.logger import Logger
from lib.language import Language
from lib.read_config import read_config
_code = [90, 105, 110, 103]
settings = read_config()
language = Language()


def check_config():
    author = settings[3]['author']
    if author == (''.join(chr(value) for value in _code)):
        return True
    else:
        return False


def setting():
    for api in settings[0].values():
        if not api:
            Logger.critical('api-settings 有未填写项目')
            sys.exit(1)
    for key in settings[1].values():
        if not key:
            Logger.critical('key-settings 有未填写项目')
            sys.exit(1)
    for client in settings[2].values():
        if not client:
            Logger.critical('client-settings 有未填写项目')
            sys.exit(1)
    for software in settings[3].values():
        if not software:
            Logger.critical('software-settings 有未填写项目')
            sys.exit(1)
