# -*- coding: utf-8 -*-
"""T07 自检：默认测四色图片；加 --source 0 或视频路径，继续测基础追踪。

本脚本调用你已有的函数，不修改 hw_track_live.py 或 hw_vision.py。
四色真值来自课程 gen_images.py 的 patterns()；视频命中按非 None 统计。
"""
import argparse
import json
import math
from pathlib import Path
import sys
import time

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
from hw_track_live import detect_color

COLORS = ("red", "blue", "green", "yellow")
# 绿三角的质心是三个顶点坐标的平均值，不是外接框中心。
EXPECTED = {
    "red": (480.0, 270.0),
    "blue": (1470.0, 270.0),
    "green": (480.0, (810.0 + 560.0 + 560.0) / 3.0),
    "yellow": (1440.0, 800.0),
}
DRAW_COLORS = {"red": (0, 0, 255), "blue": (255, 0, 0),
               "green": (0, 150, 0), "yellow": (0, 150, 180)}


def read_image(path):
    if not path.is_file():
        raise FileNotFoundError(f"找不到图片：{path}")
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"图片无法读取：{path}")
    return image


def save_image(path, image):
    # imencode + tofile 支持 Windows 中文路径。
    ok, data = cv2.imencode(".png", image)
    if not ok:
        raise ValueError(f"图片保存失败：{path}")
    data.tofile(path)


def check_patterns(path, repeats, output, say):
    image = read_image(path)
    if image.shape[:2] != (1080, 1920):
        raise ValueError("请使用课程原版 1920×1080 的 patterns.png；本脚本的真值对应这张图。")
    marked = image.copy()
    records = []
    say("=== 进阶：四色质心与检测速度（静态图片） ===")
    say(f"图片：{path}")
    say(f"每种颜色计时 {repeats} 次；不含图片读取、画图和显示时间。")
    for color in COLORS:
        # 先预热，减少首次调用对速度的影响。
        for _ in range(3):
            detect_color(image, color)
        start = time.perf_counter()
        centers = [detect_color(image, color) for _ in range(repeats)]
        elapsed = time.perf_counter() - start
        fps = repeats / elapsed
        expected = EXPECTED[color]
        errors = [math.hypot(float(c[0]) - expected[0], float(c[1]) - expected[1])
                  for c in centers if c is not None]
        complete = len(errors) == repeats
        max_error = max(errors) if errors else None
        passed = complete and max_error <= 15 and fps >= 15
        center = centers[-1]
        record = dict(color=color, expected=list(expected), center=list(center) if center is not None else None,
                      successful_calls=len(errors), calls=repeats, max_error_px=max_error,
                      detection_fps=fps, passed=bool(passed))
        records.append(record)
        center_text = "None" if center is None else f"({center[0]:.2f}, {center[1]:.2f})"
        error_text = "无结果" if max_error is None else f"{max_error:.2f} px"
        say(f"{color:6s} 中心={center_text}  真值=({expected[0]:.2f}, {expected[1]:.2f})"
            f"  最大误差={error_text}  检测 FPS={fps:.1f}  {'PASS' if passed else 'FAIL'}")
        if center is not None:
            point = (round(center[0]), round(center[1]))
            cv2.circle(marked, point, 10, (0, 0, 0), 2)
            cv2.drawMarker(marked, point, (0, 0, 0), cv2.MARKER_CROSS, 30, 2)
            cv2.putText(marked, f"{color} {center_text} FPS {fps:.1f}",
                        (point[0] - 220, point[1] + 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, DRAW_COLORS[color], 2)
    cv2.putText(marked, "T07 STATIC COLOR CHECK - NOT A LIVE TRACKING SCREENSHOT",
                (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    save_image(output / "T07_patterns_check.png", marked)
    passed = all(record["passed"] for record in records)
    say(f"进阶图片自检：{'PASS' if passed else 'FAIL'}")
    say("此项验证四色检测函数；不自动证明按键切换、断流重连或实时显示。")
    return dict(passed=passed, results=records, image=str(path), measurement="detection_only")


def check_video(source_text, limit, output, show, say):
    from hw_vision import detect_red_circle
    source = int(source_text) if source_text.isdecimal() else source_text
    if isinstance(source, str) and not source.startswith(("http://", "https://", "rtsp://")):
        source = str(Path(source).expanduser().resolve())
        if not Path(source).is_file():
            raise FileNotFoundError(f"找不到视频文件：{source}")
    say("=== 基础：视频帧数、检测命中率与实际处理 FPS ===")
    say(f"视频源：{source}；最多处理 {limit} 帧。")
    say("命中表示 detect_red_circle 返回非 None；请使用包含红色圆形目标的视频。")
    cap = cv2.VideoCapture(source)
    frames = hits = 0
    last_frame = last_center = None
    window_open = False
    start = None
    try:
        if not cap.isOpened():
            raise RuntimeError("视频源打不开。检查摄像头占用、视频路径或手机网络地址。")
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        start = time.perf_counter()
        while frames < limit:
            ok, frame = cap.read()
            if not ok:
                break
            frames += 1
            center = detect_red_circle(frame)
            if center is not None:
                hits += 1
            last_frame, last_center = frame, center
            if show:
                preview = frame.copy()
                if center is not None:
                    point = (round(center[0]), round(center[1]))
                    cv2.drawMarker(preview, point, (0, 255, 0), cv2.MARKER_CROSS, 20, 2)
                    cv2.circle(preview, point, 5, (0, 255, 0), 2)
                live_fps = frames / (time.perf_counter() - start)
                cv2.putText(preview, f"Tracking: red  frames: {frames}  FPS: {live_fps:.1f}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.imshow("T07 Basic Check", preview)
                window_open = True
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        elapsed = time.perf_counter() - start
    finally:
        cap.release()
        if window_open:
            cv2.destroyWindow("T07 Basic Check")
    rate = hits / frames if frames else 0.0
    fps = frames / elapsed if elapsed > 0 else 0.0
    passed = frames >= 30 and rate >= 0.70 and fps >= 10
    say(f"处理帧数：{frames}；命中帧数：{hits}；命中率：{rate * 100:.1f}%；FPS：{fps:.1f}")
    say(f"基础自检：{'PASS' if passed else 'FAIL'}（要求 ≥30 帧、≥70%、≥10 FPS）")
    if last_frame is not None:
        marked = last_frame.copy()
        if last_center is not None:
            point = (round(last_center[0]), round(last_center[1]))
            cv2.circle(marked, point, 5, (0, 255, 0), 2)
            cv2.drawMarker(marked, point, (0, 255, 0), cv2.MARKER_CROSS, 20, 2)
        cv2.putText(marked, f"BASIC CHECK: frames={frames} hits={hits} hit={rate*100:.1f}% FPS={fps:.1f}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        save_image(output / "T07_basic_last_frame.png", marked)
    return dict(source=str(source), frames=frames, hits=hits, hit_rate=rate,
                processing_fps=fps, passed=passed, includes_display_time=show)


def main():
    parser = argparse.ArgumentParser(description="T07 自检：四色图片 + 可选视频统计")
    parser.add_argument("--image", type=Path, default=TASK / "素材" / "patterns.png")
    parser.add_argument("--source", help="0=电脑摄像头；也可填写视频路径或网络视频 URL")
    parser.add_argument("--frames", type=int, default=60)
    parser.add_argument("--repeats", type=int, default=30)
    parser.add_argument("--show", action="store_true", help="视频统计时显示窗口，q 提前结束")
    parser.add_argument("--output", type=Path, default=TASK / "自检结果")
    args = parser.parse_args()
    if args.frames < 30 or args.repeats < 1:
        parser.error("--frames 至少为 30，--repeats 必须大于 0。")
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    lines = []
    def say(message):
        print(message)
        lines.append(message)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    results = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "basic": {"status": "NOT_RUN"}}
    code = 0
    try:
        results["advanced"] = check_patterns(args.image.expanduser().resolve(), args.repeats, output, say)
        if not results["advanced"]["passed"]:
            code = 1
        if args.source is not None:
            results["basic"] = check_video(args.source, args.frames, output, args.show, say)
            if not results["basic"]["passed"]:
                code = 1
        else:
            say("基础视频自检：未运行。加 --source 0 或 --source 视频路径后才能得到帧数与命中率。")
    except (OSError, RuntimeError, ValueError, cv2.error) as error:
        say(f"检查中止：{error}")
        results["error"] = str(error)
        code = 1
    finally:
        say(f"结果保存目录：{output}")
        (output / f"T07_check_{stamp}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (output / f"T07_check_{stamp}.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
