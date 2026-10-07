# -*- coding: utf-8 -*-
"""
T08 YOLO 推理 —— 作业骨架（学生版）

目标：学会加载模型、跑推理、把结果解析成"能用的数据"。
训练是 M08 的事，这里只用官方预训练权重 yolov8n.pt（80 类通用目标）。

自检（本教案不含自动校验脚本）：跑一遍 assets/bus.jpg，看能不能检出 person 与 bus
"""
from typing import Dict, List, Tuple

import numpy as np


# ---------------------------------------------------------------- 1
def load_model(weight_path: str):
    """加载 YOLO 模型并返回模型对象。

    from ultralytics import YOLO
    return YOLO(weight_path)
    """
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    from ultralytics import YOLO
    return YOLO(weight_path)
    raise NotImplementedError("TODO: from ultralytics import YOLO")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 2
def detect_objects(model, img, conf: float = 0.25) -> List[Tuple[str, float, Tuple[int, int, int, int]]]:
    """对一张 BGR 图跑推理，返回检测列表。

    返回格式: [(类别名, 置信度, (x1, y1, x2, y2)), ...]
    按置信度从高到低排序。

    提示：
        results = model.predict(source=img, conf=conf, verbose=False)
        r = results[0]
        boxes = r.boxes
        - boxes.cls  是类别 id 的 tensor
        - boxes.conf 是置信度
        - boxes.xyxy 是左上角/右下角坐标
        - r.names    是 {id: 类别名} 的字典
    """
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    results = model.predict(source=img, conf=conf, verbose=False)
    r = results[0]
    boxes = r.boxes
    results=[]
    for b in boxes:
        cls_id=int(b.cls[0])
        conf=float(b.conf[0])
        name=r.names[cls_id]
        x1,y1,x2,y2=map(int,b.xyxy[0])
        results.append((name,conf,(x1,y1,x2,y2)))
    results.sort(key=lambda x: x[1], reverse=True)
    return results
    raise NotImplementedError("TODO: model.predict -> 解析 boxes -> 排序")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 3
def count_by_class(dets: List[Tuple[str, float, Tuple[int, int, int, int]]]) -> Dict[str, int]:
    """按类别名计数：{"person": 4, "bus": 1}"""
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    count={}
    for c,conf,box in dets:
        count[c]=count.get(c,0)+1
    return count
    raise NotImplementedError("TODO")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 4
def max_conf_target(dets, name: str):
    """返回指定类别中置信度最高的那一条；没有该类返回 None。"""
    # ↓↓↓ 在这里写你的代码 ↓↓↓
    best=None
    for det in dets:
        c,conf,box=det
        if c==name:
            if best is None or conf>best[1]:
                best=det
    return best
    raise NotImplementedError("TODO")
    # ↑↑↑ 你的代码写在这里 ↑↑↑


# ---------------------------------------------------------------- 5
def draw_dets(img, dets, copy_img: bool = True) -> "np.ndarray":
    """把检测结果画到图上：绿框 + 顶部文字 "name conf"。

    返回画好的图；copy_img=True 时不改动原图。
    """
    import cv2
    # ↓↓↓ 在这里写你的代码 ↓↓↓

    if copy_img:
        copy=img.copy()
    else:
        copy=img
    for c,conf,box in dets:
        (x1,y1,x2,y2)=box
        cv2.rectangle(copy,(x1,y1),(x2,y2),(0,255,0),2)
        lable=f"{c}{conf:.2f}"
        text_y=max(20,y1-8)
        cv2.putText(copy,lable,(x1, text_y),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 0),2,)
    return copy
    raise NotImplementedError("TODO: cv2.rectangle + cv2.putText")
    # ↑↑↑ 你的代码写在这里 ↑↑↑
