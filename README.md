# MiniServe 极简启动器 (项目演示工具包)

MiniServe 是一个基于 `customtkinter` 和 `miniserve` 的跨平台 (Windows/macOS) 本地静态文件服务器图形界面工具。它的主要目标是帮助开发者或演示人员快速选择包含前端静态文件 (如 `dist` 目录) 的文件夹，并一键启动一个本地 Web 服务，方便进行项目演示或本地测试。

## ✨ 特性

- **跨平台支持**: 支持 Windows 和 macOS 系统。
- **现代化 UI**: 使用 `customtkinter` 构建的极简且现代化的深色/浅色自适应界面。
- **一键服务**: 自动检测并运行对应平台的 `miniserve` 引擎。
- **SPA 支持**: 默认开启 `--spa` 模式并自动指向 `index.html`，完美支持 Vue / React 等单页应用。
- **便捷操作**: 一键启动与停止，启动后自动在系统默认浏览器中打开页面。

## 🚀 如何使用

1. 确保安装了相关依赖 (`pip install -r requirements.txt`)。
2. 确保 `bin/` 目录下有对应平台的 `miniserve` 可执行文件 (`miniserve-win.exe` 或 `miniserve-mac-x64`)。
3. 运行主程序 `python main.py`。
4. 在图形界面中点击 **“浏览...”**，选择你要提供服务的静态文件目录 (例如 Vue/React 构建生成的 `dist` 目录)。
5. 点击 **“🚀 启动服务”**。
6. 服务将在 `http://127.0.0.1:8080` 启动，应用会自动打开你的默认浏览器。
7. 演示完成后，点击 **“⏹ 停止服务”**。

## 📦 构建与打包

项目附带了 `build_win.bat` 等脚本用于打包为独立的可执行文件。你可以通过 PyInstaller 将其打包发布，无需目标机器安装 Python 环境。
