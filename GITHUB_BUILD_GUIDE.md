# 如何使用GitHub Actions云构建APK

## 步骤1：创建GitHub仓库

1. 访问 https://github.com/new
2. 仓库名称：`flet-todo-app`（或任意名称）
3. 选择 **Public** 或 **Private**
4. 点击 **Create repository**

## 步骤2：推送代码到GitHub

在 `todo_app` 目录执行：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit with GitHub Actions"

# 关联远程仓库（替换成你的仓库地址）
git remote add origin https://github.com/你的用户名/flet-todo-app.git

# 推送到GitHub
git push -u origin main
```

如果遇到分支名称问题，运行：
```bash
git branch -M main
git push -u origin main
```

## 步骤3：触发自动构建

1. 打开你的GitHub仓库页面
2. 点击顶部 **Actions** 标签
3. 你会看到 **Build Android APK** 工作流
4. 点击右侧 **Run workflow** 按钮
5. 选择分支（默认main），点击绿色 **Run workflow** 按钮

## 步骤4：等待构建

- ⏱️ 构建时间：约5-10分钟
- 📊 可以实时查看构建进度和日志
- ✅ 成功后显示绿色对勾

## 步骤5：下载APK

1. 构建完成后，在工作流页面向下滚动
2. 找到 **Artifacts** 部分
3. 点击 **todo-app-release** 下载ZIP文件
4. 解压得到 `app-release.apk`

## 步骤6：安装到手机

1. 将APK传输到Android手机（通过USB、云盘、邮件等）
2. 在手机上打开APK文件
3. 允许"从未知来源安装应用"
4. 点击安装

## 注意事项

- ✅ GitHub Actions对公开仓库完全免费
- ✅ 私有仓库每月有免费额度（2000分钟）
- ✅ 每次推送代码会自动触发构建
- ✅ 可以手动触发构建（Run workflow按钮）

## 下次构建

直接推送代码即可：
```bash
git add .
git commit -m "Update app"
git push
```

或者在GitHub页面点击 **Run workflow** 手动触发。
