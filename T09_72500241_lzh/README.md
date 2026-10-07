# T09 · 训练自己的 YOLO

提交说明见 [T09_72500241_lzh.md](T09_72500241_lzh.md)。

## 文件位置

- 代码/train.py：复现训练、验证与配置检查。
- data.yaml：数据配置，nc=1，names 为 fire_extinguisher。
- 截图/T09_训练曲线.png、截图/T09_终端.png：真实训练曲线与验证指标。
- 记录/args.yaml、记录/results.csv：原始 50 轮训练记录。
- 记录/检查结果.md、记录/验证日志.txt、记录/检查数据.json：2026-10-07 已完成的实际检查。

记录/下的旧 README、旧提交说明和日志保留整理前路径，使用当前文件夹时以本 README 和当前提交说明为准。

## 完整包运行

在解压后的 T09_72500241_lzh 目录打开 PowerShell：

```powershell
python .\代码\train.py --check-only
python .\代码\train.py --eval
```

需要再次训练时才运行：

```powershell
python .\代码\train.py --epochs 50 --imgsz 320
```

脚本将 data.yaml 中的相对数据路径转换成绝对路径，完整包移动后仍可按本说明使用；训练输出保存到 runs/，不覆盖原始记录。若直接使用 yolo 命令行，请将所用 data.yaml 的 path 改为数据集绝对路径。

## GitHub 版与完整包

GitHub 地址：https://github.com/i13232641813-coder/rc-hw-72500241-lzh。

GitHub 不含模型、完整数据或 ZIP 附件。完整材料位于桌面：

`C:\Users\Austin\Desktop\rc_72500241_lzh\T09_72500241_lzh`

完整包包含 demo_dataset/、best.pt、last.pt、yolov8n.pt、训练输出/train-2。提交收集表时附 T09_72500241_lzh.zip，或填写自己创建的真实网盘链接。

在仓库根目录验证桌面提交模型：

```powershell
python .\T09_72500241_lzh\代码\train.py --eval --dataset "C:\Users\Austin\Desktop\rc_72500241_lzh\T09_72500241_lzh\demo_dataset" --weights "C:\Users\Austin\Desktop\rc_72500241_lzh\T09_72500241_lzh\best.pt"
```

原始记录为 50 轮、imgsz=320；实测 best.pt 的 mAP50=0.986688，mAP50-95=0.749153。课程参考权重 demo_dataset/open_source_best.pt 不作为本次训练的提交模型。
