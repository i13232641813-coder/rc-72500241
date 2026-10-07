"""T09 复现入口：根据原 CLI 的 50 轮、320 尺寸配置补充。"""
import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def resolve_data(config_path, dataset_override=None):
    """把配置里的相对路径转换为绝对路径，方便移动提交文件夹。"""
    config_path = Path(config_path).expanduser().resolve()
    if not config_path.is_file():
        raise FileNotFoundError(f"找不到数据配置：{config_path}")
    config = yaml.safe_load(config_path.read_text(encoding="utf-8-sig"))
    if not isinstance(config, dict):
        raise ValueError("data.yaml 必须是包含 train、val、nc、names 的配置。")
    for key in ("train", "val", "nc", "names"):
        if key not in config:
            raise ValueError(f"data.yaml 缺少 {key}")
    if config["nc"] != 1 or config["names"] not in (
        {0: "fire_extinguisher"}, ["fire_extinguisher"]
    ):
        raise ValueError("本提交数据集应为一个类别：0 = fire_extinguisher。")
    if dataset_override:
        dataset = Path(dataset_override).expanduser().resolve()
    else:
        dataset = Path(config.get("path", ".")).expanduser()
        if not dataset.is_absolute():
            dataset = config_path.parent / dataset
        dataset = dataset.resolve()
    config["path"] = str(dataset)
    for split in ("train", "val"):
        expected = f"images/{split}"
        if str(config[split]).replace("\\", "/") != expected:
            raise ValueError(f"本提交 {split} 路径应为 {expected}")
        images_dir = dataset / "images" / split
        labels_dir = dataset / "labels" / split
        extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        if not images_dir.is_dir() or not labels_dir.is_dir():
            raise FileNotFoundError(f"缺少目录：{images_dir} 或 {labels_dir}")
        images = [p for p in images_dir.iterdir() if p.suffix.lower() in extensions]
        labels = list(labels_dir.glob("*.txt"))
        if not images or not labels:
            raise ValueError(f"{split} 图片或标签目录为空。")
        if len(images) != len(labels) or {p.stem for p in images} != {p.stem for p in labels}:
            raise ValueError(f"{split} 图片和标签没有逐个同名配对。")
        if split == "train" and len(images) < 30:
            raise ValueError("训练图片不足 30 张。")
        print(f"{split}: images={len(images)}, labels={len(labels)}")
    return config


def main():
    parser = argparse.ArgumentParser(description="T09 训练、验证或检查配置")
    parser.add_argument("--data", type=Path, default=ROOT / "data.yaml")
    parser.add_argument("--dataset", type=Path, help="覆盖数据集目录；仓库版可指向桌面数据集")
    parser.add_argument("--weights", type=Path, help="本地权重文件；训练默认 yolov8n.pt，验证默认 best.pt")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=320)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default="cpu", help="默认 CPU；有可用 CUDA 环境可设 0")
    parser.add_argument("--name", default=None, help="结果文件夹名称")
    parser.add_argument("--eval", action="store_true", help="仅验证 best.pt，不重新训练")
    parser.add_argument("--check-only", action="store_true", help="仅检查配置、目录和文件配对")
    args = parser.parse_args()
    try:
        config = resolve_data(args.data, args.dataset)
        if args.check_only:
            print("配置和文件配对检查通过；此模式不检查模型指标。")
            return
        weights = args.weights or ROOT / ("best.pt" if args.eval else "yolov8n.pt")
        weights = weights.expanduser().resolve()
        if not weights.is_file():
            raise FileNotFoundError(f"找不到本地权重：{weights}。请用 --weights 指定已有文件。")
        if args.epochs < 1 or args.imgsz < 1 or args.batch < 1:
            raise ValueError("epochs、imgsz、batch 必须为正整数。")
        # 保留转换后的配置，Ultralytics 直接读取绝对数据路径。
        runs = ROOT / "runs"
        runs.mkdir(exist_ok=True)
        resolved_path = runs / "data_resolved.yaml"
        resolved_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
        from ultralytics import YOLO
        model = YOLO(str(weights))
        options = dict(data=str(resolved_path), imgsz=args.imgsz, batch=args.batch,
                       device=args.device, workers=0, project=str(runs), exist_ok=False)
        if args.eval:
            model.val(name=args.name or "t09_validation", **options)
        else:
            model.train(epochs=args.epochs, name=args.name or "t09_reproduce", **options)
    except (FileNotFoundError, ValueError) as error:
        parser.exit(1, f"无法继续：{error}\n")


if __name__ == "__main__":
    main()
