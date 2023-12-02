# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/11/30
# @File Name: gui_weather.py
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QMenu, QAction, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QDateTime, QDate
from PyQt5.QtGui import QIcon, QPixmap, QFont
import os
import base64
from datetime import datetime
import pyqtgraph as pg
from pyqtgraph import TextItem
from res.images_data import ico_base64
from lib.read_config import read_config
from lib.logger import Logger
from lib.language import Language
from lib.check import check_config, setting
from core.get_weather import WeatherAPI
from lib.files_zip import zip_folder
from lib.images_save import ImagesSave

language = Language()
city_data = {'九龙城区': '101320102', '香港岛': '101320101', '新界区': '101320103', '北京市': '101010400',
             '合肥市': '101220101', '庐阳区': '101220108', '蜀山区': '101220109', '桐城市': '101220609',
             '沈阳市': '101070101'}  # Add more cities as needed


class WeatherGUI(QMainWindow):
    def __init__(self):
        super(WeatherGUI, self).__init__()
        # 加载图标
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ico_base64))
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        self.settings = read_config()
        self.key = self.settings[1]['key']
        self.api = WeatherAPI(self.key, self.settings)
        self.image_counter = 0
        self.image_folder = 'out/images'
        self.image_saver = ImagesSave(
            self.image_folder, self.image_counter, self.settings)
        zip_folder_path = 'out/zip'
        zip_folder(self.image_folder, zip_folder_path, 20)
        self.clear_images()
        self.time_update = self.settings[3]['time_update']
        self.time_saim = self.settings[3]['time_saim']
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 布局
        main_layout = QVBoxLayout()
        # 标签和下拉框（城市选择）
        top_layout = QHBoxLayout()
        self.icon_label_realtime = QLabel()
        self.icon_label_realtime.setAlignment(Qt.AlignLeft)
        # top_layout.setSpacing(40)
        self.weather_text_realtime = QLabel()
        self.weather_text_realtime.setFont(QFont("Arial", 26, QFont.Bold))
        self.weather_text_realtime.setAlignment(Qt.AlignCenter)

        self.city_combo = QComboBox(self)
        self.city_combo.setFont(QFont("Arial", 18, QFont.Bold))
        self.city_combo.addItems(city_data.keys())

        top_layout.addWidget(self.icon_label_realtime)
        top_layout.addWidget(self.weather_text_realtime)
        top_layout.addWidget(self.city_combo)

        date_btu_layout = QHBoxLayout()
        self.datetime_label = QLabel(self)
        self.datetime_label.setAlignment(Qt.AlignLeft)
        self.datetime_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.update_datetime()
        # 查询按钮
        self.btn = QPushButton('获取数据', self)
        self.btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.btn.clicked.connect(self.update_weather_data)
        date_btu_layout.addWidget(self.datetime_label)
        date_btu_layout.addWidget(self.btn)

        # 天气图标布局
        day_icon_layout = QHBoxLayout()
        night_icon_layout = QHBoxLayout()

        # 日期标签布局
        self.date_label_layout = QHBoxLayout()
        self.temp_max_layout = QHBoxLayout()
        self.temp_min_layout = QHBoxLayout()

        # 添加到主布局
        main_layout.addLayout(top_layout)
        main_layout.addLayout(date_btu_layout)
        # 添加日期标签布局到主布局
        main_layout.addLayout(self.date_label_layout)
        # 添加天气图标布局到主布局
        main_layout.addLayout(day_icon_layout)
        main_layout.addLayout(night_icon_layout)
        main_layout.addLayout(self.temp_max_layout)
        main_layout.addLayout(self.temp_min_layout)

        # 设置主窗口的布局
        # self.setLayout(main_layout)
        central_widget.setLayout(main_layout)
        # 设置窗口属性
        self.setWindowTitle('天气预报')
        self.setFixedSize(385, 520)
        # self.setGeometry(300, 300, 385, 520)

        # 添加每日和每夜图标的标签
        self.icon_labels_day = []
        self.icon_labels_night = []

        for _ in range(7):
            date_label = QLabel()
            date_label.setAlignment(Qt.AlignCenter)
            self.date_label_layout.addWidget(date_label)

            label_day = QLabel()
            label_day.setFixedSize(40, 40)
            label_day.setAlignment(Qt.AlignCenter)
            label_night = QLabel()
            label_night.setFixedSize(40, 40)
            label_night.setAlignment(Qt.AlignCenter)
            self.icon_labels_day.append(label_day)
            self.icon_labels_night.append(label_night)
            day_icon_layout.addWidget(label_day)
            night_icon_layout.addWidget(label_night)

            temp_max = QLabel()
            temp_max.setAlignment(Qt.AlignCenter)
            self.temp_max_layout.addWidget(temp_max)
            temp_min = QLabel()
            temp_min.setAlignment(Qt.AlignCenter)
            self.temp_min_layout.addWidget(temp_min)

        self.plot_widget = pg.PlotWidget(self)
        main_layout.addWidget(self.plot_widget)
        self.plot_widget.getAxis('left').hide()
        self.plot_widget.getAxis('bottom').hide()

        self.datetime_timer = QTimer(self)
        self.datetime_timer.timeout.connect(self.update_datetime)
        self.datetime_timer.start(1000)  # Update every sec

        # Set up a QTimer for automatic updates
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_weather_data)
        self.update_timer.start(self.time_update)  # 10 minutes in milliseconds

        # 设置定时器，每隔3秒保存一次图片
        self.save_image_timer = QTimer(self)
        self.save_image_timer.timeout.connect(self.save_as_image)
        self.save_image_timer.start(self.time_saim)  # 2min

        # 添加右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("MM-dd hh:mm:ss")
        # Get the day of the week
        current_day = QDate.longDayName(current_datetime.date().dayOfWeek())
        current_day = current_day.replace('星期', '周')
        self.datetime_label.setText(f"{current_day} {formatted_datetime}")

    def update_weather_data(self):
        self.city_id, selected_city_name = self.get_cityid()
        Logger.info(f'当前地区:{selected_city_name}')
        self.get_weather_realtime()
        self.get_weather_forecast()
        self.get_weather_24h()
        Logger.info(f'{language["10min_update"]}')

    def show_weather_icon(self, weather_icon_label, icon_path, size=50):
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaledToWidth(size, Qt.SmoothTransformation)
        weather_icon_label.setPixmap(pixmap)
        weather_icon_label.setScaledContents(True)
        weather_icon_label.setMaximumSize(size, size)  # 设置最大尺寸

    def get_cityid(self):
        selected_city_name = self.city_combo.currentText()
        city_id = city_data.get(selected_city_name)
        return city_id, selected_city_name

    def get_weather_realtime(self):
        now = self.api.get_weather_realtime_info(self.city_id)
        temperature = now.get("temp")
        weather_text = now.get("text")
        weather_icon = now.get("icon")
        self.show_weather_icon(
            self.icon_label_realtime, f'res/icons/{weather_icon}.png', size=50)
        self.weather_text_realtime.setText(
            f"{weather_text} {temperature}°C")

    def get_weather_forecast(self):
        self.clear_weather_info()
        forecast_data = self.api.get_weather_forecast_info(self.city_id)
        # Only consider the next 7 days
        for i, forecast in enumerate(forecast_data[:7]):
            date = forecast.get('fxDate', '')
            date_object = datetime.strptime(date, '%Y-%m-%d')
            day_of_week = date_object.strftime('%A')
            day_of_week = day_of_week.replace('星期', '周')
            temp_max = forecast.get('tempMax', '')
            temp_min = forecast.get('tempMin', '')
            # Display day and night icons for each day with the date
            icon_code_day = forecast.get('iconDay', '')
            icon_path_day = os.path.join(
                'res/icons', f'{icon_code_day}.png')
            self.show_weather_icon(
                self.icon_labels_day[i], icon_path_day, 40)
            icon_code_night = forecast.get('iconNight', '')
            icon_path_night = os.path.join(
                'res/icons', f'{icon_code_night}.png')
            self.show_weather_icon(
                self.icon_labels_night[i], icon_path_night, 40)
            # Set the date labels above each column
            date_label = self.date_label_layout.itemAt(i).widget()
            if i == 0:
                date_label.setText('今天')
            else:
                date_label.setText(day_of_week)
            temp_max_label = self.temp_max_layout.itemAt(i).widget()
            temp_max_label.setText(f"↑{temp_max}°C")
            temp_min_label = self.temp_min_layout.itemAt(i).widget()
            temp_min_label.setText(f"↓{temp_min}°C")

    def get_weather_24h(self):
        self.clear_weather_info()
        hourly_data = self.api.get_weather_24h_info(self.city_id)
        # print(hourly_data)
        temperatures = [float(hour['temp']) for hour in hourly_data]
        times = [hour['fxTime'] for hour in hourly_data]
        # Display only the next 6 hours
        temperatures = temperatures[:6]
        times = times[:6]
        pen = pg.mkPen(color=(255, 255, 0), width=2)
        brush = pg.mkBrush(color=(21, 76, 119))  # RGB颜色为R21G76B119
        # 计算温度的平均值
        average_temperature = sum(temperatures) / len(temperatures)
        # 根据平均温度确定fill_level的值
        fill_level = -20 if average_temperature < 0 else -5
        self.plot_widget.plot(y=temperatures, pen=pen,
                              fillLevel=fill_level, fillBrush=brush)
        # Set background color
        background_color = (0, 147, 226)  # RGB values for R0G147B226
        self.plot_widget.setBackground(background_color)
        self.plot_widget.getAxis('left').hide()
        self.plot_widget.getAxis('bottom').show()
        # Add temperature labels at each data point
        for i in range(len(times)):
            temp_label = TextItem(f"{temperatures[i]:.1f}°", color=(
                255, 255, 255), anchor=(0.5, 0.9))
            temp_label.setPos(i, temperatures[i])
            temp_label.setRotation(0)
            self.plot_widget.addItem(temp_label)
        # Format x-axis labels as dates
        x_axis = self.plot_widget.getAxis('bottom')
        # x_axis.setStyle(tickLength=2)
        x_axis.setPen(pg.mkPen(color=(255, 255, 255), width=2))
        # self.plot_widget.showGrid(True, True)
        x_axis.setTextPen(color=(255, 255, 255))
        # Format x-axis labels dynamically based on current time
        current_hour = datetime.now().hour
        is_afternoon = current_hour >= 12
        if is_afternoon:
            x_axis.setTicks([[(i, self.format_time_afternoon(times[i]))
                            for i in range(len(times))]])
        else:
            x_axis.setTicks([[(i, self.format_time_morning(times[i]))
                            for i in range(len(times))]])

    def format_time_afternoon(self, timestamp):
        # Convert timestamp to datetime object
        dt_object = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M%z')
        # Format datetime object to desired string
        formatted_time = dt_object.strftime('下午%I点')
        return formatted_time.replace('下午0', '下午')

    def format_time_morning(self, timestamp):
        # Convert timestamp to datetime object
        dt_object = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M%z')
        # Format datetime object to desired string
        formatted_time = dt_object.strftime('上午%I点')
        return formatted_time.replace('上午0', '上午')

    def clear_weather_info(self):
        # Clear the plotted data in the PlotWidget
        self.plot_widget.clear()

    def mouseDoubleClickEvent(self, event):
        # 切换窗口的透明状态
        if self.isWindowOpaque():
            self.setWindowOpacity(0.5)  # 设置透明度为50%
        else:
            self.setWindowOpacity(1.0)  # 恢复到完全不透明
        event.accept()  # 接受双击事件

    def isWindowOpaque(self):
        # 判断窗口是否完全不透明
        return self.windowOpacity() == 1.0

    def show_context_menu(self, event):
        context_menu = QMenu(self)
        show_author_action = QAction("作者", self)
        show_author_action.triggered.connect(self.show_author_info)
        context_menu.addAction(show_author_action)
        context_menu.exec_(self.mapToGlobal(event))

    def show_author_info(self):
        info = self.settings[2]['info']
        if info == 'Zing':
            author_info = """
            作者:Zing YE
            版本:V2.2.1
            邮箱:Zingvip@163.com
            香港理工大学 机电工程学院
            """
        else:
            author_info = """ Test"""
        QMessageBox.information(self, "作者信息", author_info)

    def clear_images(self):
        # 调用 ImagesSave 类的 clear_images 方法
        self.image_saver.clear_images()

    def save_as_image(self):
        # 调用 ImagesSave 类的 save_as_image 方法
        self.image_saver.save_as_image(self.centralWidget())


def main_gui():
    Logger.info(f'{language["statement_1"]}')
    Logger.info(f'{language["statement_2"]}')
    Logger.info(f'{language["statement_3"]}')
    if check_config():
        setting()
        Logger.info(f'{language["statement_4"]}')
        app = QApplication(sys.argv)
        weather_app = WeatherGUI()
        weather_app.show()
        # weather_app.save_as_image()
        sys.exit(app.exec_())
    else:
        Logger.info(f'{language["config_not_filled"]}')
