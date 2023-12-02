import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtGui, QtCore


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建一个包含文本的标签
        label = QLabel('Hello, PyQt5!', central_widget)
        label.setAlignment(QtCore.Qt.AlignCenter)

        # 将标签添加到布局
        layout = QVBoxLayout(central_widget)
        layout.addWidget(label)

        # 设置主窗口的布局
        central_widget.setLayout(layout)

    def save_as_image(self):
        # 获取窗口内容的截图
        image = QImage(self.centralWidget().size(), QImage.Format_ARGB32)
        painter = QtGui.QPainter(image)
        self.centralWidget().render(painter)
        painter.end()

        # 保存截图为图片文件
        image.save('screenshot.png')
        print('Screenshot saved as screenshot.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    # 在这里调用保存为图片的函数
    mainWindow.save_as_image()

    sys.exit(app.exec_())
