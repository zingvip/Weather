# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/11/30
# @File Name: language.py

from ruamel.yaml import YAML
import json


def Language():
    """
    读取配置文件中的语言选项并返回相对因的语言文件的读取结果
    :return:
    """
    with open('./config.yml', 'r', encoding='utf-8') as lang:
        config = YAML().load(lang.read())
        language_sel = config['client-settings']['language']
        if language_sel not in ['zh_cn', 'en_us']:
            language_sel = 'zh_cn'

    # 打开语言json文件
    with open(f'./res/lang/{language_sel}.json', 'r', encoding='utf-8') as lang_f:
        language = json.loads(lang_f.read())

    return language
