# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/11/30
# @File Name: get_weather.py
import requests
from lib.logger import Logger
from lib.language import Language
import json
language = Language()


class WeatherAPI:
    def __init__(self, key, settings):
        self.key = key
        self.settings = settings

    def get_weather_realtime_info(self, city_id):
        Logger.info(f'{language["wait_seconds"]}')
        url_rel = self.settings[0]['url_rel']
        api_url_rel = f"{url_rel}location={city_id}&key={self.key}"
        try:
            response = requests.get(api_url_rel)
            data = response.json()
            with open('out/json/get_weather_realtime_info.json', 'w') as file:
                json.dump(data, file)
            if data.get('code') == '200':
                Logger.info(f'{language["get_real_weather_successfully"]}')
                return data.get('now', {})
            else:
                Logger.critical('获取实时天气失败')
        except requests.exceptions.RequestException as e:
            Logger.critical('请求异常')
            return []

    def get_weather_forecast_info(self, city_id):
        Logger.info(f'{language["wait_seconds"]}')
        url_day = self.settings[0]['url_day']
        api_url_day = f"{url_day}location={city_id}&key={self.key}"
        try:
            response = requests.get(api_url_day)
            data = response.json()
            with open('out/json/get_weather_forecast_info.json', 'w') as file:
                json.dump(data, file)
            if data.get('code') == '200':
                Logger.info(f'{language["get_fore_weather_successfully"]}')
                return data.get('daily', {})
            else:
                Logger.critical('获取天气预测失败')
        except requests.exceptions.RequestException as e:
            Logger.critical('请求异常')
            return []

    def get_weather_24h_info(self, city_id):
        Logger.info(f'{language["wait_seconds"]}')
        url_24h = self.settings[0]['url_24h']
        api_url_24h = f"{url_24h}location={city_id}&key={self.key}"
        try:
            response = requests.get(api_url_24h)
            data = response.json()
            with open('out/json/get_weather_24h_info.json', 'w') as file:
                json.dump(data, file)
            if data.get('code') == '200':
                Logger.info(f'{language["get_24h_weather_successfully"]}')
                return data.get('hourly', {})
            else:
                Logger.critical('获取天气曲线失败')
        except requests.exceptions.RequestException as e:
            Logger.critical('请求异常')
            return []
