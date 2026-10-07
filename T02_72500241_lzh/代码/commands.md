`pwd`：现实操作目前所在的目录
`ls`：列出你的全部文件夹
`cd`：用于切换目录，搭配不同符号可以从不同方向切换`cd ..`（上一级）、`cd ~`（回家）、`cd -`（回上一次） 
`mkdir`：在电脑再建一个新目录
`cp`：copy复制
cp a.txt b/              # 目标已存在目录 → 塞进去，保持原名
cp a.txt c.txt           # 目标不存在 → 复制并重命名
cp -r dir1 dir2          # 递归；dir2 存在则变成 dir2/dir1/
cp -r dir1/. dir2/       # 把内容平铺进已有 dir2（含隐藏文件）
cp -i a.txt b/           # 覆盖前问一句，输入 n 则放弃（实测保住了原文件）
cp -n a.txt b/           # 永不覆盖，已存在就静默跳过
cp -u a.txt b/           # 只在源比目标新时才复制，否则无声跳过
cp -v a.txt b/           # 显示过程：'a.txt' -> 'b/a.txt'
cp -p a.txt b/           # 保留原时间戳（普通 cp 会重置成"现在"）
cp -a dir1 dir2          # 归档，≈ -rp 全保留，备份目录首选
cp --backup=numbered a.txt b/   # 覆盖时自动留 a.txt.~1~，不丢旧版
cp -t b/ a.txt c.txt     # 目标目录写前面，配合 find/xargs 很好用
cp a.txt b.txt c.txt d/  # 多文件，目标必须是目录
`mv`：移动或者改名，`mv old.py new.py`（把old.py 改名为 new.py）
`rm`:删除对应的目录内容`rm a.txt`、`rm -rf dir/`
`cat`：查看文件内容
`grep`：搜索文件中的关键字，`grep -n error log.txt`（）
`find`：寻找文件  `find . -name "*.py"` 
`sudo`：以管理员身份执行 `sudo apt install git` 
`chmod`：改权限  `chmod +x run.sh`（变成可执行） 
`df` ：看磁盘空间  `df -h` 
`ping`：测网络通不通 | `ping -c 4 baidu.com` 
`tar`：打包/解压 `tar -xzf a.tar.gz` 