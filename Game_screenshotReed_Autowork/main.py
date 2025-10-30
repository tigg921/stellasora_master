import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from core import MumuScreenshot, IconDetector, Showdetector, Tapscreen, Autorecruitment, StartGame
#import easyocr

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游戏截图识别程序")
        self.setGeometry(100, 100, 600, 400)

        self.screenshot_tool = MumuScreenshot()
        self.tapscreen_tool = Tapscreen()
        self.autorecruitment_tool = Autorecruitment()
        self.start_game_tool = StartGame()
        #template_path = os.path.join(os.path.dirname(__file__), "templates", "button_template.png")
        #self.detector = IconDetector(template_path)
        self.display = Showdetector(output_dir="test")
        #self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)

        self.last_detected_x = None
        self.last_detected_y = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("点击按钮进行截图和识别", self)


        self.capture_button = QPushButton("启动游戏", self)
        self.capture_button.clicked.connect(self.start_game)
        layout.addWidget(self.capture_button)

       

        layout.addWidget(self.label)
        self.capture_button = QPushButton("自动公招", self)
        self.capture_button.clicked.connect(self.auto_Public_Recruitment)
        layout.addWidget(self.capture_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def start_game(self):
        try:
            self.label.setText("正在启动游戏...")
            self.start_game_tool.run()
            self.label.setText("游戏启动完成")
              
        except Exception as e:
            self.label.setText(f"程序出错: {str(e)}")
    
    def tap_screen(self):
            
            try:
                self.label.setText("正在点击...")
               
                self.tapscreen_tool.tap_screen(self.last_detected_x, self.last_detected_y)
                self.label.setText(f"已点击按钮: ({self.last_detected_x}, {self.last_detected_y})")
            except Exception as e:
                self.label.setText(f"点击失败: {str(e)}")
        
    def auto_Public_Recruitment(self):
        try:
            self.label.setText("正在执行自动公招...")
            self.autorecruitment_tool.run()
            self.label.setText("自动公招执行完成")
        except Exception as e:
            self.label.setText(f"自动公招失败: {str(e)}")
        
     


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()