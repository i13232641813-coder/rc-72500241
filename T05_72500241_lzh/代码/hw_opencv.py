# -*- coding: utf-8 -*-
"""
T05 OpenCV 基础 —— 作业骨架（学生版）

6 个函数，全部是后面做视觉的"日常操作"。
自检（本教案不含自动校验脚本）：自己写几行 print 调用这六个函数，看输出对不对

注意：
  - 图像是 numpy 数组，shape = (高, 宽, 3)，下标顺序是 [y, x] 不是 [x, y]
  - OpenCV 读进来是 BGR 不是 RGB
"""
import os
from typing import List, Optional, Tuple

import cv2
import numpy as np


# ---------------------------------------------------------------- 1
def load_image(path: str):
    """读入一张图片（BGR），失败返回 None。直接用 cv2.imread 即可。"""
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    img=cv2.imread(path)
    if img is None:
        return None
    return img
    raise NotImplementedError("TODO: cv2.imread")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 2
def to_gray(img: "np.ndarray") -> "np.ndarray":
    """BGR 转灰度图，返回单通道图。"""
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray
    raise NotImplementedError("TODO: cv2.cvtColor + COLOR_BGR2GRAY")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 3
def crop_roi(img: "np.ndarray", x: int, y: int, w: int, h: int) -> "np.ndarray":
    """裁剪矩形区域。注意 numpy 是 [y:y+h, x:x+w]。"""
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    roi=img[y:y+h,x:x+w]
    return roi
    raise NotImplementedError("TODO: 切片，先 y 后 x")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 4
def resize_keep(img: "np.ndarray", max_side: int = 640):
    """等比例缩放：让长边等于 max_side，短边按比例。返回缩放后的图。

    640x480 且 max_side=320 -> 320x240
    """
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    if img.shape[0]>img.shape[1]:
        small=cv2.resize(img,(img.shape[1]*max_side//img.shape[0],max_side))
    else:
        small=cv2.resize(img,(max_side,img.shape[0]*max_side//img.shape[1]))
    return small
    raise NotImplementedError("TODO: 算比例 -> cv2.resize")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 5
def draw_marker(img: "np.ndarray", cx: float, cy: float,
                text: Optional[str] = None) -> "np.ndarray":
    """在图上画质心：红色圆点(r=5) + 十字，可选在右侧写文字。
    返回新图，不要改动传入的原图（先 copy）。
    """
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    img2=img.copy()
    circle=cv2.circle(img2,(round(cx),round(cy)),5,(0,0,255),-1)
    if text is not None:
        text=cv2.putText(img2,text,(round(cx)+10,round(cy)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
    cross=cv2.drawMarker(img2,(round(cx),round(cy)),(0,0,255),cv2.MARKER_CROSS,20,2)
    return img2
    raise NotImplementedError("TODO: copy -> cv2.circle / drawMarker / putText")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 6
def read_frames(source, n: int = 10) -> List["np.ndarray"]:
    """读取帧序列的前 n 帧。

    source 可以是：
      - 摄像头编号（整数，如 0）
      - 视频文件路径（字符串）
    返回帧的 list（读不到就返回已读到的部分）。记得 release。
    """
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    cap=cv2.VideoCapture(source)
    frames=[]
    while len(frames) < n:
        ok,frame=cap.read()
        if not ok:
            break
        frames.append(frame)
    cap.release()
    return frames
    raise NotImplementedError("TODO: VideoCapture + 循环 read + release")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 7（选做）
def mask_centroid(mask: "np.ndarray") -> Optional[Tuple[float, float]]:
    """求二值掩膜中白色区域的质心 (cx, cy)；全黑（没有白色）返回 None。

    提示：cv2.moments(mask)，m00 为 0 表示没有白色像素。
    """
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    moments=cv2.moments(mask)
    if moments["m00"]==0:
        return None
    cx=moments["m10"]/moments["m00"]
    cy=moments["m01"]/moments["m00"]
    return (cx,cy)
    raise NotImplementedError("TODO: cv2.moments")
    # ↑↑↑ 你的代码写在这里 ↑↑↑
