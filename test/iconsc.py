from PIL import Image
import os


def change_image_color(input_folder, output_folder, target_color):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中所有PNG文件的列表
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    for input_file in input_files:
        # 构建输入和输出文件的完整路径
        input_path = os.path.join(input_folder, input_file)
        output_path = os.path.join(output_folder, input_file)

        # 打开图像
        image = Image.open(input_path)

        # 将图像转换为RGBA模式（如果不是的话）
        image = image.convert('RGBA')

        # 获取图像的像素数据
        data = image.getdata()

        # 创建一个新的像素列表，将目标颜色应用到每个像素
        new_data = []
        for item in data:
            # 判断当前像素是否为透明
            if item[3] > 0:
                # 将RGB部分替换为目标颜色
                new_data.append(
                    (target_color[0], target_color[1], target_color[2], item[3]))
            else:
                # 保持透明像素不变
                new_data.append(item)

        # 创建一个新的图像对象，将修改后的像素数据应用到其中
        new_image = Image.new('RGBA', image.size)
        new_image.putdata(new_data)

        # 保存新图像
        new_image.save(output_path)


# 示例使用：将“png”文件夹下的所有非透明像素的颜色改为红色 (255, 0, 0)
# change_image_color('res/icons', 'res/icons_c', (0, 0, 255))
