import subprocess
import cv2
import numpy as np
import os
from pathlib import Path

class Tapscreen:
    def tap_screen(self, x=0, y=0, instance_num=None):
        adb_path = str(Path(r"D:\Program Files\Netease\MuMu Player 12\shell\adb.exe"))
        port = 7554 + (instance_num or 1)
        
        try:
            subprocess.run(
                f'"{adb_path}" -s 127.0.0.1:{port} shell input tap {x} {y}',
                shell=True,
                check=True
            )
            print(f"已在坐标({x}, {y})执行点击")
            return True
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('gbk', errors='ignore') or e.stdout.decode('gbk', errors='ignore')
            raise RuntimeError(f"点击失败: {error_msg}") from e
        
default_screenshot = Tapscreen()