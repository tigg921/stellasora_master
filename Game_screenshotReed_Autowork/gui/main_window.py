from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from core import MumuScreenshot, IconDetector, Showdetector
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游戏截图识别程序")
        self.setGeometry(100, 100, 800, 600)

        self.screenshot_tool = MumuScreenshot()
        self.detector = IconDetector("templates/button_template.png")
        self.display = Showdetector(output_dir="test")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("启动游戏")
        layout.addWidget(self.label)

        self.capture_button = QPushButton("截取屏幕")
        self.capture_button.clicked.connect(self.capture_and_detect)
        layout.addWidget(self.capture_button)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def capture_and_detect(self):
        try:
            screenshot = self.screenshot_tool.capture()
            (x, y), confidence = self.detector.find_icon(screenshot)

            if x is not None:
                h, w = self.detector.template.shape[:2]
                top_left = (x - w // 2, y - h // 2)
                bottom_right = (x + w // 2, y + h // 2)

                self.display.show_image_with_rectangle(screenshot, top_left, bottom_right)

                # Update the displayed image
                height, width, channel = screenshot.shape
                bytes_per_line = 3 * width
                q_img = QPixmap.fromImage(QImage(screenshot.data, width, height, bytes_per_line, QImage.Format_RGB888))
                self.image_label.setPixmap(q_img)
            else:
                self.label.setText(f"未找到按钮 (最高置信度: {confidence:.2f})")
        except Exception as e:
            self.label.setText(f"程序出错: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())