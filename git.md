# Git 学习笔记

- git status：查看文件修改状态。
- git add 文件名：将文件修改加入暂存区。
- git commit -m "说明"：保存一次版本记录。
- git log --oneline：查看简洁的提交记录。
- git remote -v：查看远程仓库地址。
- git push：上传本地提交。

我遇到的问题：
浏览器能打开 GitHub，但 Git 上传连接超时。

解决方法：
上传时通过 http.proxy 指定 Clash 的代理地址。
