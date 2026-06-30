import os
import sys
import platform
import subprocess
import threading
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox

# 界面配置
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MiniServe")
        self.geometry("500x350")
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
        # 标题
        self.title_label = ctk.CTkLabel(self, text="MiniServe 极简启动器", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # 目录选择区域
        self.dir_frame = ctk.CTkFrame(self)
        self.dir_frame.pack(pady=10, padx=20, fill="x")

        self.dir_label = ctk.CTkLabel(self.dir_frame, text="目标文件夹:")
        self.dir_label.pack(side="left", padx=(10, 5), pady=10)

        self.dir_entry = ctk.CTkEntry(
            self.dir_frame, 
            width=220,
            placeholder_text="请选择 dist 文件夹..."
        )
        self.dir_entry.pack(side="left", padx=5)

        self.browse_btn = ctk.CTkButton(
            self.dir_frame, 
            text="浏览...", 
            width=80, 
            height=32,
            corner_radius=16,
            font=ctk.CTkFont(size=13),
            command=self.browse_directory
        )
        self.browse_btn.pack(side="left", padx=(5, 10))

        # 状态区域
        self.status_label = ctk.CTkLabel(self, text="状态: 未运行", text_color="gray", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=(10, 5))

        self.link_label = ctk.CTkLabel(self, text="", text_color="#1f538d", cursor="hand2", font=ctk.CTkFont(size=14, underline=True))
        self.link_label.pack(pady=5)
        self.link_label.bind("<Button-1>", lambda e: self.open_browser())

        # 按钮区域
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        button_font = ctk.CTkFont(size=16, weight="bold")
        
        self.start_btn = ctk.CTkButton(
            self.btn_frame, 
            text="🚀 启动服务", 
            command=self.start_server, 
            width=140,
            height=40,
            corner_radius=20,
            font=button_font,
            fg_color="#2FA572", 
            hover_color="#108253"
        )
        self.start_btn.pack(side="left", padx=15)

        self.stop_btn = ctk.CTkButton(
            self.btn_frame, 
            text="⏹ 停止服务", 
            command=self.stop_server, 
            width=140,
            height=40,
            corner_radius=20,
            font=button_font,
            fg_color="#D32F2F", 
            hover_color="#B71C1C", 
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=15)

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
            cmd = [exe_path, "--index", "index.html", "--spa", "--port", "8080", target_dir]
            
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
            webbrowser.open("http://127.0.0.1:8080")

    def on_closing(self):
        self.stop_server()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
