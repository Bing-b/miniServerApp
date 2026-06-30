import os
import sys
import platform
import subprocess
import threading
import webbrowser
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox

# 界面配置
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# 全局字体配置
APP_FONT = "Microsoft YaHei" if platform.system() == "Windows" else "PingFang SC"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MiniServe")
        self.geometry("600x420")
        self.resizable(False, False)

        self.server_process = None
        
        # 确定运行时的基础路径（处理打包后的路径问题）
        if getattr(sys, 'frozen', False):
            # 运行的是打包后的exe
            self.base_path = sys._MEIPASS
        else:
            # 运行的是脚本
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # UI 构建
        self.build_ui()

    def build_ui(self):
        # --- Header Section ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(25, 15), padx=20, fill="x")

        self.title_label = ctk.CTkLabel(self.header_frame, text="MiniServe 🚀", font=ctk.CTkFont(family=APP_FONT, size=28, weight="bold"))
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="快速、轻量的本地静态服务启动器", text_color="gray", font=ctk.CTkFont(family=APP_FONT, size=13))
        self.subtitle_label.pack(pady=(5, 0))

        # --- Configuration Card ---
        self.config_card = ctk.CTkFrame(self, corner_radius=15)
        self.config_card.pack(pady=(0, 20), padx=30, fill="x")
        
        self.config_title = ctk.CTkLabel(self.config_card, text="1. 选择静态文件目录", font=ctk.CTkFont(family=APP_FONT, size=14, weight="bold"))
        self.config_title.pack(anchor="w", padx=20, pady=(15, 5))

        self.dir_frame = ctk.CTkFrame(self.config_card, fg_color="transparent")
        self.dir_frame.pack(padx=20, pady=(0, 15), fill="x")

        self.dir_entry = ctk.CTkEntry(
            self.dir_frame, 
            height=36,
            placeholder_text="请选择包含 index.html 的目录..."
        )
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            self.dir_frame, 
            text="浏览...", 
            width=80, 
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(family=APP_FONT, size=13),
            command=self.browse_directory
        )
        self.browse_btn.pack(side="right")

        # --- Operation & Status Card ---
        self.op_card = ctk.CTkFrame(self, corner_radius=15)
        self.op_card.pack(pady=0, padx=30, fill="x")

        self.op_title = ctk.CTkLabel(self.op_card, text="2. 服务控制", font=ctk.CTkFont(family=APP_FONT, size=14, weight="bold"))
        self.op_title.pack(anchor="w", padx=20, pady=(15, 5))

        self.btn_frame = ctk.CTkFrame(self.op_card, fg_color="transparent")
        self.btn_frame.pack(padx=20, pady=5, fill="x")

        button_font = ctk.CTkFont(family=APP_FONT, size=15, weight="bold")
        
        self.start_btn = ctk.CTkButton(
            self.btn_frame, 
            text="▶ 启动服务", 
            command=self.start_server, 
            height=40,
            corner_radius=8,
            font=button_font,
            fg_color="#2FA572", 
            hover_color="#108253"
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.stop_btn = ctk.CTkButton(
            self.btn_frame, 
            text="⏹ 停止服务", 
            command=self.stop_server, 
            height=40,
            corner_radius=8,
            font=button_font,
            fg_color="#D32F2F", 
            hover_color="#B71C1C", 
            state="disabled"
        )
        self.stop_btn.pack(side="right", fill="x", expand=True)

        self.status_frame = ctk.CTkFrame(self.op_card, fg_color="transparent")
        self.status_frame.pack(padx=20, pady=(10, 15), fill="x")

        self.status_label = ctk.CTkLabel(self.status_frame, text="状态: 未运行", text_color="gray", font=ctk.CTkFont(family=APP_FONT, size=13))
        self.status_label.pack(side="left")

        self.link_label = ctk.CTkLabel(self.status_frame, text="", text_color="#1f538d", cursor="hand2", font=ctk.CTkFont(family=APP_FONT, size=13, underline=True))
        self.link_label.pack(side="right")
        self.link_label.bind("<Button-1>", lambda e: self.open_browser())

    def browse_directory(self):
        folder = filedialog.askdirectory(initialdir=os.getcwd(), title="选择项目演示文件夹")
        if folder:
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, folder)

    def get_executable_path(self):
        sys_name = platform.system()
        arch = platform.machine().lower()
        
        executable = ""
        if sys_name == "Windows":
            executable = "miniserve-win.exe"
        elif sys_name == "Darwin":
            executable = "miniserve-mac-x64"
        else:
            messagebox.showerror("错误", f"不支持的操作系统: {sys_name}")
            return None

        # 构建完整路径，优先在 bin 目录查找
        exe_path = os.path.join(self.base_path, "bin", executable)
        if not os.path.exists(exe_path):
            messagebox.showerror("错误", f"找不到依赖文件!\n请确保存在: {exe_path}\n你可能需要先运行 download_deps.py")
            return None

        # 对 Mac 赋予执行权限
        if sys_name == "Darwin":
            try:
                os.chmod(exe_path, 0o755)
            except Exception as e:
                print("赋予执行权限失败:", e)

        return exe_path

    def start_server(self):
        if self.server_process:
            return

        target_dir = self.dir_entry.get()
        if not os.path.exists(target_dir):
            messagebox.showerror("错误", f"目录不存在:\n{target_dir}")
            return

        exe_path = self.get_executable_path()
        if not exe_path:
            return

        try:
            # miniserve --index index.html --spa --port 8080 ./dist
            cmd = [
                exe_path, 
                "--index", "index.html", 
                "--spa", 
                "--port", "8080",
                # 添加禁用缓存的 Header，防止切换目录后浏览器依然加载旧缓存
                "--header", "Cache-Control: no-cache, no-store, must-revalidate",
                "--header", "Pragma: no-cache",
                "--header", "Expires: 0",
                target_dir
            ]
            
            # 隐藏 Windows 控制台窗口
            creationflags = 0
            if platform.system() == "Windows":
                creationflags = subprocess.CREATE_NO_WINDOW

            self.server_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                creationflags=creationflags
            )

            self.status_label.configure(text="状态: 运行中 🟢", text_color="green")
            self.link_label.configure(text="http://127.0.0.1:8080")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            
            # 自动在浏览器打开
            self.open_browser()

        except Exception as e:
            messagebox.showerror("启动失败", str(e))
            self.stop_server()

    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            
        self.status_label.configure(text="状态: 已停止 🔴", text_color="red")
        self.link_label.configure(text="")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def open_browser(self):
        if self.server_process:
            # 添加时间戳参数强制浏览器打开新标签页并跳过缓存
            url = f"http://127.0.0.1:8080/?t={int(time.time())}"
            webbrowser.open(url)

    def on_closing(self):
        self.stop_server()
        self.destroy()

if __name__ == "__main__":
    try:
        app = App()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        import traceback
        with open("crash.log", "w") as f:
            f.write(traceback.format_exc())
