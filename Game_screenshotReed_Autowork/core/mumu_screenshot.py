import subprocess
import cv2
import numpy as np
import os
from pathlib import Path

class MumuScreenshot:
    def __init__(self, adb_path=None, default_instance=1):
        self.adb_path = str(Path(adb_path or r"D:\Program Files\Netease\MuMu Player 12\shell\adb.exe"))
        self.default_instance = default_instance
        
        if not os.path.exists(self.adb_path):
            raise FileNotFoundError(f"未找到ADB工具，请检查路径: {self.adb_path}")

    def capture(self, instance_num=None, save_path=None):
        port = 7554 + (instance_num or self.default_instance)
        
        try:
            subprocess.run(
                f'"{self.adb_path}" connect 127.0.0.1:{port}',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            result = subprocess.run(
                f'"{self.adb_path}" -s 127.0.0.1:{port} exec-out screencap -p',
                shell=True,
                capture_output=True,
                check=True
            )
            
            img_array = np.frombuffer(result.stdout, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("截图数据解析失败")
                
            if save_path:
                save_path = str(Path(save_path))
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                if not cv2.imwrite(save_path, img):
                    raise RuntimeError(f"无法保存图像到: {save_path}")
            
            return img
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('gbk', errors='ignore') or e.stdout.decode('gbk', errors='ignore')
            raise RuntimeError(f"ADB命令执行失败: {error_msg}") from e
        except Exception as e:
            raise RuntimeError(f"截图过程中发生错误: {str(e)}") from e

default_screenshot = MumuScreenshot()