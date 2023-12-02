# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/11/30
# @File Name: read_config.py
from ruamel.yaml import YAML


def read_config():
    """
    读取配置文件并返回读取到的内容同
    :return: api_settings, key_settings, client_settings, software_settings  ->  0, 1, 2, 3
    """
    config_file = 'config.yml'
    with open(f'./{config_file}', 'r', encoding='utf-8') as conf:
        config = YAML().load(conf.read())
        api_settings = config['api-settings']
        key_settings = config['key-settings']
        client_settings = config['client-settings']
        software_settings = config['software-settings']
    return api_settings, key_settings, client_settings, software_settings
