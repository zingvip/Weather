# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/11/30
# @File Name: image_save.py
import os
from datetime import datetime
from lib.logger import Logger


class ImagesSave:
    def __init__(self, image_folder, image_counter, settings):
        self.image_folder = image_folder
        self.image_counter = image_counter
        self.settings = settings

    def clear_images(self):
        if os.path.exists(self.image_folder):
            for file in os.listdir(self.image_folder):
                file_path = os.path.join(self.image_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def save_as_image(self, central_widget):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f'{self.image_folder}/fig_{current_time}.png'
        screenshot = central_widget.grab()
        screenshot.save(image_filename)
        self.image_counter += 1
        inums = self.settings[3]['imagenum']
        if self.image_counter > inums:
            old_images = sorted(os.listdir(self.image_folder))
            oldest_image = os.path.join(self.image_folder, old_images[0])
            if os.path.exists(oldest_image):
                os.remove(oldest_image)
            self.image_counter -= 1
        Logger.info(f'图片已经保存为 fig_{current_time}.png')
