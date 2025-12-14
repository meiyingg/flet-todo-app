# Advanced Todo Manager

一个功能强大的待办事项管理应用，使用Python和Flet框架开发。

## 功能特性

- ✅ 任务管理（添加、编辑、删除、完成）
- 🎯 优先级设置（高、中、低）
- 📁 分类管理
- 🔍 搜索功能
- 📊 统计面板
- 💾 数据导出
- 📱 跨平台支持

## 自动构建APK（GitHub Actions）

1. 推送代码到GitHub
2. 进入仓库的 **Actions** 标签
3. 点击 **Build Android APK** → **Run workflow**
4. 等待构建完成（约5-10分钟）
5. 下载生成的APK文件

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).