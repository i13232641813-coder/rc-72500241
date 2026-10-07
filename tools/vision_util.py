# -*- coding: utf-8 -*-
"""
vision_util —— 本教案所有模块共用的视觉小工具

提供 5 类能力：
  1. 中文路径安全的 imread / imwrite（Windows 上 cv2 原生读写会失败）
  2. setup()：强制 stdout 为 UTF-8，解决控制台中文乱码
  3. find_asset()：素材定位（教案 assets/ → ~/rc_ws/assets/ → assets/videos / images）
  4. FrameSource：统一帧源抽象，摄像头 / 视频文件只差一个参数
  5. EMA 滤波 + FPS 统计（M10 闭环要用到）

用法：
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
    from vision_util import setup, imread, find_asset, FrameSource
"""
import os
import sys
import time

import cv2
import numpy as np

# ---------------------------------------------------------------- 基础设置

def setup():
    """脚本开头调用一次，让控制台中文不乱码。"""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def imread(path):
    """读取图片，支持中文路径。读不到返回 None。"""
    if not path or not os.path.exists(path):
        return None
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img


def imwrite(path, img):
    """写入图片，支持中文路径。自动创建父目录。"""
    d = os.path.dirname(os.path.abspath(path))
    if d:
        os.makedirs(d, exist_ok=True)
    ext = "." + path.rsplit(".", 1)[-1]
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise IOError("imwrite 失败: " + path)
    with open(path, "wb") as f:
        f.write(buf.tobytes())
    return True


# ---------------------------------------------------------------- 素材定位

def _asset_roots():
    """候选素材根目录，按这个顺序找（不读任何环境变量）：

        ① 教案 assets/          —— 随附素材都在这里，放这里一定找得到
        ② ~/rc_ws/assets/       —— 你自己的素材（可选）
        ③ assets/videos/        —— 你自己录的视频（可选）
        ④ assets/images/
    """
    here = os.path.dirname(os.path.abspath(__file__))       # .../线上自学教案/tools
    base = os.path.dirname(here)                            # .../线上自学教案
    home = os.path.expanduser("~")
    roots = [
        os.path.join(base, "assets"),
        os.path.join(home, "rc_ws", "assets"),
        os.path.join(base, "assets", "videos"),
        os.path.join(base, "assets", "images"),
    ]
    return [r for r in roots if r and os.path.isdir(r)]


def find_asset(name):
    """按文件名找素材，找不到返回 None。
    例：find_asset("quiz_01.png") / find_asset("bus.jpg") / find_asset("ball.mp4")
    """
    for root in _asset_roots():
        p = os.path.join(root, name)
        if os.path.exists(p):
            return p
    return None


def asset_roots_report():
    """返回当前生效的素材搜索路径（排障用）。"""
    return _asset_roots()


# ---------------------------------------------------------------- 帧源抽象

class FrameSource:
    """统一帧源：摄像头 / 视频文件 / 图片序列。

    cap = FrameSource(0)                  # 笔记本摄像头
    cap = FrameSource("assets/ball.mp4")  # 素材视频（线上无摄像头时使用）
    while True:
        ok, frame = cap.read()
        if not ok:
            break
    print(cap.fps)
    """

    def __init__(self, source=0, loop=False):
        self.is_camera = isinstance(source, int) or (isinstance(source, str) and source.isdigit())
        self.src = int(source) if self.is_camera else source
        self.loop = loop
        self.cap = cv2.VideoCapture(self.src)
        self.opened = self.cap.isOpened()
        self.index = 0

    def read(self):
        ok, frame = self.cap.read()
        if not ok and self.loop and not self.is_camera:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self.cap.read()
        if ok:
            self.index += 1
        return ok, frame

    @property
    def fps(self):
        f = self.cap.get(cv2.CAP_PROP_FPS)
        return f if f and f > 1 else 30.0

    def release(self):
        self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.release()


# ---------------------------------------------------------------- 滤波 / 计时

class EMA:
    """一阶低通（指数滑动平均）。alpha 越小越平滑、越迟钝。

    f = EMA(alpha=0.3)
    f.update(10.0)   -> 10.0
    f.update(20.0)   -> 13.0
    """

    def __init__(self, alpha=0.3, init=None):
        self.alpha = float(alpha)
        self.value = init

    def update(self, x):
        if x is None:
            return self.value
        if self.value is None:
            self.value = float(x)
        else:
            self.value = self.alpha * float(x) + (1 - self.alpha) * self.value
        return self.value

    def reset(self, v=None):
        self.value = v


class FPSMeter:
    """简易 FPS 统计。每帧 tick()，读 .fps 取当前帧率。"""

    def __init__(self):
        self.t0 = time.time()
        self.n = 0
        self.fps = 0.0

    def tick(self):
        self.n += 1
        dt = time.time() - self.t0
        if dt >= 0.5:
            self.fps = self.n / dt
            self.n = 0
            self.t0 = time.time()
        return self.fps


# ---------------------------------------------------------------- 绘图小工具

def draw_point(img, cx, cy, color=(0, 0, 255), r=5, text=None):
    """在图上画质心十字 + 圆点，可选文字标注。返回新图（不改动原图）。"""
    out = img.copy()
    h, w = out.shape[:2]
    cx, cy = int(cx), int(cy)
    cv2.drawMarker(out, (cx, cy), color, cv2.MARKER_CROSS, 24, 2)
    cv2.circle(out, (cx, cy), r, color, -1)
    if text:
        tx = min(cx + 10, w - 120)
        ty = max(cy - 10, 20)
        cv2.putText(out, str(text), (tx, ty), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, color, 2, cv2.LINE_AA)
    return out


def draw_roi(img, x0, y0, x1, y1, color=(0, 255, 0), thickness=2):
    """画 ROI 框。"""
    out = img.copy()
    cv2.rectangle(out, (int(x0), int(y0)), (int(x1), int(y1)), color, thickness)
    return out


def put_hud(img, lines, org=(10, 26)):
    """左上角叠加多行文字（FPS / 状态用）。"""
    out = img.copy()
    for i, t in enumerate(lines):
        y = org[1] + i * 24
        cv2.putText(out, str(t), (org[0], y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 255, 255), 2, cv2.LINE_AA)
    return out
