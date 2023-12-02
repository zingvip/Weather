# -- coding:utf-8 --
# @Author: Zing_YE zingvip@163.com
# @Development Tool: vscode
# @Create Time: 2023/12/01
# @File Name: files_zip.py
import zipfile
import os
import glob
from lib.logger import Logger


def zip_folder(folder_path, zip_folder_path):
    # 获取文件夹中的所有文件和子文件夹
    all_files = []
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            all_files.append(file_path)
    if not all_files:
        Logger.info(f'当前文件夹是空的')
        return
    # 获取文件夹中最后一个文件的路径
    last_file_path = max(all_files, key=os.path.getmtime)
    # 获取最后一个文件的不带后缀的名字
    last_file_name = os.path.splitext(os.path.basename(last_file_path))[0]
    # 构建最终的压缩文件路径
    zip_file_path_final = os.path.join(
        zip_folder_path, last_file_name + '.zip')
    # 创建一个 ZipFile 对象，用于写入压缩文件
    with zipfile.ZipFile(zip_file_path_final, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件夹中的所有文件和子文件夹
        for file_path in all_files:
            # 构建文件在压缩文件中的相对路径
            relative_path = os.path.relpath(file_path, folder_path)
            # 将文件添加到压缩文件中
            zipf.write(file_path, relative_path)


# 示例用法
# folder_to_zip = 'out/images'
# zip_folder_path = 'out/zip'
# zip_folder(folder_to_zip, zip_folder_path)
def zip_folder(folder_path, zip_folder_path, max_zip_files=20):
    # 获取文件夹中的所有文件和子文件夹
    all_files = []
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            all_files.append(file_path)

    if not all_files:
        Logger.info(f'当前文件夹是空的')
        return

    # 获取文件夹中最后一个文件的路径
    last_file_path = max(all_files, key=os.path.getmtime)
    # 获取最后一个文件的不带后缀的名字
    last_file_name = os.path.splitext(os.path.basename(last_file_path))[0]
    # 构建最终的压缩文件路径
    zip_file_path_final = os.path.join(
        zip_folder_path, last_file_name + '.zip')

    # 创建一个 ZipFile 对象，用于写入压缩文件
    with zipfile.ZipFile(zip_file_path_final, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件夹中的所有文件和子文件夹
        for file_path in all_files:
            # 构建文件在压缩文件中的相对路径
            relative_path = os.path.relpath(file_path, folder_path)
            # 将文件添加到压缩文件中
            zipf.write(file_path, relative_path)

    # 删除最老的文件，保留最新的max_zip_files个压缩包
    existing_zips = glob.glob(os.path.join(zip_folder_path, '*.zip'))
    if len(existing_zips) > max_zip_files:
        oldest_zips = sorted(existing_zips, key=os.path.getctime)[
            :len(existing_zips) - max_zip_files]
        for old_zip in oldest_zips:
            os.remove(old_zip)
