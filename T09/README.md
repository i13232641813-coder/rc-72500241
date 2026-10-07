# T09 · 训练自己的 YOLO

学号：72500241；姓名：廖卓涵。

## 已有训练结果

使用课程示例灭火器数据集（205 张训练、52 张验证），从 yolov8n.pt 迁移学习，训练 50 轮，图片尺寸 320。实际训练使用 YOLO 命令行；`代码/train.py` 是之后按这些参数补充的复现入口。

原训练命令（当时在课程 `08_训练自己的YOLO` 目录执行）：

```powershell
yolo detect train data=demo_dataset/data.yaml model=..\assets\yolov8n.pt epochs=50 imgsz=320
```

`args.yaml` 保留原始记录，因此其中的旧电脑路径不代表当前提交包路径。原始训练记录在 `results.csv`、`results.png`；已有 best.pt 验证截图的 mAP50 为 0.987、mAP50-95 为 0.749。

## 查看材料

- `T09_72500241_廖卓涵.md`：提交说明。
- `代码/train.py`：训练、验证和配置检查入口。
- `data.yaml`：数据配置，显式包含 nc=1。
- `截图/T09_results.png`：50 轮训练曲线。
- `截图/T09_终端.png`：真实验证命令及 mAP 指标截图（原 download.png）。
- `检查结果.md`、`验证日志.txt`：2026-10-07 重新检查的记录。

## 完整提交包与 GitHub 的区别

完整包位于桌面 `线上自学作业_72500241_廖卓涵/T09_72500241_廖卓涵`。该文件夹内包含 `demo_dataset/`、`best.pt`、`last.pt` 和复现用的 `yolov8n.pt`，随其他材料一起打包交到课程作业收集表。

GitHub 目录只保留代码、配置、说明、截图和小体积训练记录，不含数据集和 .pt 权重。查看仓库材料的助教需要同时取得完整提交包。若改用网盘交大文件，应在提交说明里补实际分享链接。

## 在完整提交文件夹运行

在这个文件夹打开 PowerShell，先检查配置与文件配对：

```powershell
python .\代码\train.py --check-only
```

仅重新验证现有模型：

```powershell
python .\代码\train.py --eval
```

需要重新训练时才运行下面这条；会产生新的结果文件夹：

```powershell
python .\代码\train.py --epochs 50 --imgsz 320
```

需要已安装 Python、ultralytics 及其依赖。默认 CPU、batch=16、workers=0；原始训练参数完整保存在 args.yaml，设备与软件版本不同可能产生不同结果。生成结果在当前提交包的 `runs/` 内，原有结果文件不覆盖。

## 在仓库 T09 目录运行

仓库缺少大文件，因此需明确给出桌面数据集及本地权重：

```powershell
python .\代码\train.py --check-only --dataset "C:\Users\Austin\Desktop\线上自学作业_72500241_廖卓涵\T09_72500241_廖卓涵\demo_dataset"
python .\代码\train.py --eval --dataset "C:\Users\Austin\Desktop\线上自学作业_72500241_廖卓涵\T09_72500241_廖卓涵\demo_dataset" --weights "C:\Users\Austin\Desktop\线上自学作业_72500241_廖卓涵\T09_72500241_廖卓涵\best.pt"
```

移动完整包后，使用随附 train.py 会自动按 data.yaml 所在位置解析路径。若直接使用 `yolo detect train/val` 命令，请先把所用 data.yaml 的 path 改为解压后 demo_dataset 的绝对路径。
