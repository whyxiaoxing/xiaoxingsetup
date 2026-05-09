import asyncio
import os
import shutil
import subprocess
import sys
import threading
import tkinter
import tkinter.ttk as ttk
from pyshortcuts import make_shortcut
from pathlib import Path
from tkinter import Toplevel, scrolledtext, PhotoImage, filedialog, messagebox, StringVar, IntVar
from typing import Optional
from PIL import Image, ImageTk
import json

class AppPath:
    @staticmethod
    def root_dir() -> Path:
        if getattr(sys, "frozen", False):
            return Path(__file__).resolve().parent

        return Path(__file__).resolve().parent

    @staticmethod
    def data_path(relative_path: str) -> Path:
        return AppPath.root_dir() / relative_path

_TKROOTnouser=tkinter.Tk()
class 函数:
    def __init__(self) :
        self.最大线程数量=6
        self.解压日志:StringVar=tkinter.StringVar(value=" ")
        self.文件数量:IntVar=tkinter.IntVar(value=0)
        self.已经解压数量:IntVar=tkinter.IntVar(value=0)

    def _主线程执行(self, 回调):
        tk_root = getattr(self, "TKRoot", None)
        if tk_root is None:
            回调()
            return
        tk_root.after(0, 回调)

    def _设置变量(self, 变量, 内容) -> None:
        self._主线程执行(lambda: 变量.set(内容))

    def _增加已经解压数量(self) -> None:
        def 更新数量() -> None:
            self.已经解压数量.set(self.已经解压数量.get() + 1)

        self._主线程执行(更新数量)

    def 读取协议内容(self,txt位置:str)->str:
        try:
            with open(txt位置, 'r', encoding='utf-8') as f:
                内容=f.read()
                return 内容
        except Exception as e:
            raise e

    async def 解压逻辑(self,文件夹路径:Path,指定解压目录:Path):

        解压文件: list[Path] = []
        for 模式 in ["*.7z", "*.zip"]:解压文件.extend([f for f in 文件夹路径.glob(模式) if f.is_file()])

        if len(解压文件) == 0:
            raise RuntimeError(" 解压发生错误: 指定的7z文件不存在 ")

        self._设置变量(self.文件数量, len(解压文件))
        self._设置变量(self.已经解压数量, 0)

        if not 指定解压目录.exists():
            指定解压目录.mkdir(parents=True, exist_ok=True)

        并发限制=asyncio.Semaphore(self.最大线程数量)

        任务内容: list[asyncio.Task] = [asyncio.create_task(self.__7z解压(_a, 指定解压目录, 并发限制))for _a in 解压文件]

        已完成任务, 未完成任务 = await asyncio.wait(任务内容,return_when=asyncio.FIRST_EXCEPTION)
        错误内容: list[str] = []

        for 任务 in 已完成任务:
            try:
                任务.result()
            except Exception as exception:
                错误内容.append(str(exception))

        if 错误内容:
            for 任务 in 未完成任务:
                任务.cancel()

            await asyncio.gather(*未完成任务, return_exceptions=True)
            raise RuntimeError("\n".join(错误内容))

    async def __7z解压(
            self,
            解压文件: Path,
            解压目录路径: Path,
            并发限制: asyncio.Semaphore
    ):
        解压进程: asyncio.subprocess.Process | None = None

        async with 并发限制:
            self._设置变量(self.解压日志, f"开始解压: {解压文件.name}")

            try:
                解压进程 = await asyncio.create_subprocess_exec(
                    str(AppPath.data_path(r"./data/7z/7z.exe")),
                    "x",
                    str(解压文件),
                    f"-o{str(解压目录路径)}",
                    "-aoa",
                    "-scrc",
                    "-ssc",
                    "-y",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                标准输出任务 = asyncio.create_task(self.__日志读取(解压文件.name,解压进程.stdout, "输出" ) )
                错误输出任务 = asyncio.create_task(self.__日志读取(解压文件.name,解压进程.stderr,"错误"))
                返回码: int = await 解压进程.wait()

                await 标准输出任务
                await 错误输出任务

                if 返回码 != 0:
                    self._设置变量(self.解压日志, f"解压失败: {解压文件.name}, 返回码: {返回码}")
                    raise RuntimeError(f"{解压文件.name} 解压失败, 返回码: {返回码}")

                self._设置变量(self.解压日志, f"解压完成: {解压文件.name}")
                self._增加已经解压数量()

            except asyncio.CancelledError:
                self._设置变量(self.解压日志, f"正在终止解压: {解压文件.name}")

                if 解压进程 is not None:
                    if 解压进程.returncode is None:
                        解压进程.terminate()

                        try:
                            await asyncio.wait_for(解压进程.wait(),timeout=3)

                        except asyncio.TimeoutError:
                            解压进程.kill()
                            await 解压进程.wait()
                raise

    async  def __日志读取(self,文件名: str,输出管道,输出类型: str):
        if 输出管道 is None:
            return

        while True:
            原始行数据 = await 输出管道.readline()

            if 原始行数据 == b"":
                break

            日志行: str = 原始行数据.decode(
                "utf-8",
                errors="replace"
            ).rstrip()

            if 日志行 != "":
                self._设置变量(self.解压日志, f"[{文件名}][{输出类型}] {日志行}")

    def 加载图片(self,路径:str)->PhotoImage:
        完整路径 = str((Path(__file__).resolve().parent / 路径).resolve())
        ico=Image.open(完整路径)
        ico=ico.resize((32,32),Image.Resampling.LANCZOS)
        图片对象 = ImageTk.PhotoImage(ico, master=getattr(self, "TKRoot", None))

        return 图片对象

    def 返回安装路径(self, 中文路径支持: bool) -> str:
        安装路径 = filedialog.askdirectory(
            title="请选择安装路径",
            mustexist=True
        )

        if 安装路径 is None or 安装路径 == "":
            return ""

        安装路径 = os.path.abspath(安装路径)

        if not 中文路径支持:
            try:
                安装路径.encode("ascii")
            except UnicodeEncodeError:
                messagebox.showerror(
                    "路径错误",
                    "当前程序不支持中文路径，请选择不包含中文的安装路径。"
                )
                return ""

        return 安装路径

    async def 删除安装内容(self,路径:Path)-> list[tuple[str, str]]:
        if not 路径.exists():
            return []
        无法删除文件的信息:list[tuple[str, str]] = []

        def 错误文件(function, path, exc_info) -> None:
            无法删除文件的信息.append((str(path), str(exc_info[1])))

        try:
            await asyncio.to_thread(shutil.rmtree, 路径, ignore_errors=False,onerror=错误文件)
        except Exception as exception:
            无法删除文件的信息.append((str(路径), str(exception)))

        return 无法删除文件的信息

    def 创建快捷方式(self,安装目录,程序名称):
        完整路径=安装目录+"\\"+程序名称
        make_shortcut(
            script=完整路径,
            name=程序名称,
            desktop=True,
            startmenu=False,
            terminal=False,
            icon=完整路径
        )
        self._设置变量(self.解压日志,"已经创建快捷方式")

    def 记录安装位置(self,安装目录):
        json路径 = os.path.join(安装目录, "Uninstall.json")
        数据 = {
            "InstallPath": 安装目录
        }
        os.makedirs(安装目录, exist_ok=True)

        with open(json路径, "w", encoding="utf-8") as 文件:
            json.dump(数据, 文件, ensure_ascii=False, indent=4)
        self._设置变量(self.解压日志,"已经创建卸载卸载内容")

    def 安装前检查(self,tk:tkinter.Tk) -> bool:
        try:
            检测结果 = subprocess.run(
                ["dotnet", "--list-runtimes"],
                capture_output=True,
                text=True,
                shell=False,
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if 检测结果.returncode == 0:
                if "Microsoft.WindowsDesktop.App 9." in 检测结果.stdout or "Microsoft.NETCore.App 9" in 检测结果.stdout:
                    return True
                else:
                    raise
        except:
            结果 = tkinter.messagebox.askokcancel("无法检测到dotnet9环境","您没有安装 dotnet9 Desktop Runtime，是否安装 dotnet9？")
            if not 结果: return False

            安装程序路径 = AppPath.data_path(r"data/dotnet/dotnet9.exe")

            try:
                安装进程 = subprocess.Popen([str(安装程序路径)],shell=False)

                while True:
                    try:
                        返回码 = 安装进程.wait(timeout=0.1)
                        break
                    except subprocess.TimeoutExpired:
                        tk.update()

                if 返回码 != 0:
                    raise RuntimeError(str(返回码))

            except Exception as e:
                tkinter.messagebox.showerror(
                    "安装失败",
                    f"dotnet9 安装程序启动失败:\n{e}"
                )
                return False

        return True




class TK设置(函数):
    def __init__(self) -> None:
        super().__init__()
        self.TKRoot = _TKROOTnouser
        self.窗口大小: Optional[str]="400x100"
        self.窗口名称: Optional[str]="xiaoxing安装程序"
        self.安装程序名称: Optional[str]="xiaoxing.exe"
        self.图片: Optional[ImageTk.PhotoImage]=None
        self.__协议位置:str=str(AppPath.data_path(r"./data/安装协议/安装协议.txt"))

        self.__默认安装路径:StringVar=tkinter.StringVar(value=r"D:/xiaoxing")
        self.__安装路径是否可以有中文:bool=False


        self.__是否同意协议 = tkinter.BooleanVar(value=True)



    def __TK窗口(self):

        窗口宽度文本, 窗口高度文本 = self.窗口大小.split("x")
        窗口宽度 = int(窗口宽度文本)
        窗口高度 = int(窗口高度文本)
        屏幕宽度 = self.TKRoot.winfo_screenwidth()
        屏幕高度 = self.TKRoot.winfo_screenheight()

        窗口x = (屏幕宽度 - 窗口宽度) // 2
        窗口y = (屏幕高度 - 窗口高度) // 2


        self.TKRoot.iconbitmap(AppPath.data_path("./data/素材/APPico.ico"))
        self.TKRoot.title(self.窗口名称)
        self.TKRoot.geometry(f"{窗口宽度}x{窗口高度}+{窗口x}+{窗口y}")
        self.TKRoot.resizable(False, False)

        self.TKRoot.update_idletasks()

        self.主窗口x = self.TKRoot.winfo_x()
        self.主窗口y = self.TKRoot.winfo_y()
        self.主窗口宽度 = self.TKRoot.winfo_width()

        按钮样式 = ttk.Style()
        按钮样式.configure(
            "下一步.TButton",
            font=("Microsoft YaHei", 12, "bold"),
            foreground="black",
            padding=(10, 5)
        )
        按钮样式.configure(
            "选择文件夹.TButton",
            font=("Microsoft YaHei", 12, "bold"),
            foreground="black",
            padding=(10, 5)
        )

    def __打开安装协议(self):
        文本内容=self.读取协议内容(self.__协议位置)
        top = Toplevel(self.TKRoot)
        top.title("软件安装协议,请认真阅读")
        top.geometry("600x450")
        top.grab_set()

        文本区域= scrolledtext.ScrolledText(top, wrap=tkinter.WORD, font=("Consolas", 10))
        文本区域.pack(expand=True, fill="both", padx=10, pady=10)

        文本区域.insert(tkinter.END, 文本内容)
        文本区域.config(state="disabled")

        def 释放并关闭() -> None:
            self.__是否同意协议.set(value=True)
            top.grab_release()
            top.destroy()

        def 直接关闭() -> None:
            top.grab_release()
            top.destroy()

        btn_close = tkinter.Button(
            top,
            text="我已阅读并同意",
            command=释放并关闭,
            width=18
        )
        btn_close.pack(pady=10)

        top.protocol("WM_DELETE_WINDOW", 直接关闭)

    def __协议显示(self):
        容器 = ttk.Frame(self.TKRoot)
        容器.pack(fill="x", padx=1)

        第一行容器 = ttk.Frame(容器)
        第一行容器.pack(fill="x")

        第二行容器 = ttk.Frame(容器)
        第二行容器.pack(fill="x")
        self.图片 = self.加载图片(str(AppPath.data_path("./data/素材/感叹号.ico")))
        显示图标=ttk.Label(第一行容器,image=self.图片,takefocus=False)
        显示图标.image = self.图片

        def 同意状态变化(*args):
            下一步.configure(
                state="normal" if self.__是否同意协议.get() else "disabled"
            )


        def 下一步内容():
            self.__销毁界面内容(容器)
            self.__用户选择安装路径()

        self.__是否同意协议.trace_add("write", 同意状态变化)


        自定义字体  = ("Microsoft YaHei", 10,"bold")
        显示文字   = ttk.Label(第一行容器,text="已认真阅读本协议,并同意",font=自定义字体)
        同意选择   = ttk.Checkbutton(第一行容器,text="同意",variable=self.__是否同意协议,takefocus=False)
        下一步    = ttk.Button(第二行容器,text="下一步",style="下一步.TButton",command=下一步内容 ,takefocus=False)
        查看协议   = ttk.Button(第一行容器,text="查看协议",command=self.__打开安装协议,takefocus=False)

        显示图标.pack(side="left", padx=(10, 8),pady=5)
        显示文字.pack(side="left", padx=(6, 10),pady=5)
        同意选择.pack(side="left",pady=5)
        下一步.pack(side="left", padx=110, pady=1)
        查看协议.pack(side="left", padx=(10,0), pady=5)
        同意状态变化()

    def __销毁界面内容(self,销毁对象:ttk.Frame):
        self.图片=None
        销毁对象.grab_release()
        销毁对象.destroy()

    def __用户选择安装路径(self):
        容器=ttk.Frame(self.TKRoot)
        容器.pack(fill="x", padx=2)

        第一行容器 = ttk.Frame(容器)
        第一行容器.pack(fill="x")

        第二行容器 = ttk.Frame(容器)
        第二行容器.pack(fill="x")

        self.图片=self.加载图片(str(AppPath.data_path("./data/素材/文件夹.ico")))

        def a():
            b=self.返回安装路径(self.__安装路径是否可以有中文)
            if b =="" or b is None:
                return
            self.__默认安装路径.set(value=b)

        def 下一步内容():
            子窗口.destroy()
            self.__销毁界面内容(容器)
            self.__安装过程()



        子窗口=tkinter.Toplevel(self.TKRoot)
        子窗口.geometry(f"{400}x{100}+{self.主窗口x + self.主窗口宽度}+{self.主窗口y}")
        子窗口.resizable(False, False)
        子窗口.transient(self.TKRoot)
        子窗口.protocol("WM_DELETE_WINDOW", lambda: None)

        更改选择 = ttk.Button(master=第一行容器, text="更改安装路径", style="选择文件夹.TButton",takefocus=False, command=a)
        图片 = ttk.Label(master=第一行容器, image=self.图片, takefocus=False)
        图片.image = self.图片
        路径显示=ttk.Label(master=子窗口,textvariable=self.__默认安装路径,anchor="nw",justify="left",wraplength=390,font=("Microsoft YaHei", 10))
        下一步 = ttk.Button(第二行容器, text="下一步", style="下一步.TButton",command=下一步内容, takefocus=False)

        图片.pack(side="left", padx=(50, 150),pady=5)
        更改选择.pack(side="left", padx=(6, 10),pady=5)
        路径显示.place(x=0,y=0,width=400,height=75)
        下一步.pack(side="left", padx=110, pady=1)

    def __安装过程(self):
        容器 = ttk.Frame(self.TKRoot)
        容器.pack(fill="x", padx=5)

        第一行容器 = ttk.Frame(容器)
        第一行容器.pack(fill="x")

        子窗口 = tkinter.Toplevel(self.TKRoot)
        子窗口.geometry(f"{400}x{100}+{self.主窗口x + self.主窗口宽度}+{self.主窗口y}")
        子窗口.resizable(False, False)
        子窗口.transient(self.TKRoot)
        子窗口.protocol("WM_DELETE_WINDOW", lambda: None)

        字体=("Microsoft YaHei", 15,"bold")
        字体2=("Microsoft YaHei", 10)

        日志=ttk.Label(master=子窗口,textvariable=self.解压日志,anchor="nw",justify="left",wraplength=390,takefocus=False)
        已经解压数量=ttk.Label(master=第一行容器,textvariable=self.已经解压数量,takefocus=False,font=字体2)
        未解压数量=ttk.Label(master=第一行容器,textvariable=self.文件数量,takefocus=False,font=字体2)
        文字1= ttk.Label(master=第一行容器,text="未解压数量:",takefocus=False,font=字体)
        文字2= ttk.Label(master=第一行容器,text="已解压数量:",takefocus=False,font=字体)

        日志.place(x=0,y=0,width=395,height=85)
        文字1.pack(side="left", padx=(2,5), pady=20)
        未解压数量.pack(side="left", padx=5, pady=20)
        文字2.pack(side="left", padx=(50,2), pady=20)
        已经解压数量.pack(side="left", padx=5, pady=20)

        def 安装完成() -> None:
            子窗口.destroy()
            self.__销毁界面内容(容器)
            self.__解压成功()

        def 后台安装程序(安装路径: str,程序名称) -> None:
            try:
                asyncio.run(self.解压逻辑(AppPath.data_path(r"./data"), Path(安装路径)))
                self.创建快捷方式(安装路径,程序名称)
                self.记录安装位置(安装路径)
            except BaseException as 错误:
                self._主线程执行(lambda 错误=错误: self.__处理安装错误(错误))
                return

            self._主线程执行(安装完成)

        threading.Thread(
            target=后台安装程序,
            args=(self.__默认安装路径.get(),self.安装程序名称),
            daemon=True
        ).start()


    def __解压成功(self):

        成功文字 = ttk.Label(self.TKRoot,text="解压成功",font=("Microsoft YaHei", 14, "bold"),)
        关闭按钮 = ttk.Button(self.TKRoot,text="关闭安装",command=self.TKRoot.destroy,takefocus=False)

        成功文字.pack(padx=20,pady=(5, 5),anchor="center")
        关闭按钮.pack(padx=20,pady=(5, 5),anchor="center")

    def __安装失败(self,路径:Path):
        删除失败信息=  asyncio.run(self.删除安装内容(路径))

        未删除数量=len(删除失败信息)
        if 未删除数量 == 0 : return
        文件名称 = ",".join(Path(path).name for path, _ in 删除失败信息[:100])
        messagebox.showinfo(f"删除{未删除数量}个文件失败",文件名称)

    def __处理安装错误(self,错误:BaseException):
        messagebox.showerror("安装错误",str(错误),icon="error")
        for a in self.TKRoot.winfo_children():
            a.destroy()
        清理资源文字=ttk.Label(self.TKRoot,text="正在清理安装资源",font=("Microsoft YaHei", 16, "bold"),takefocus=False)
        清理资源文字.pack(padx=20,pady=(5, 5),anchor="center")
        self.__安装失败(Path(self.__默认安装路径.get()))

        self.TKRoot.destroy()




    def 主线安装(self):
        # 设置窗体
        try:
            self.TKRoot.withdraw()
            if not self.安装前检查(self.TKRoot):
                self.TKRoot.destroy()
                return
            self.TKRoot.deiconify()
            self.__TK窗口()
            self.__协议显示()
            self.TKRoot.mainloop()

        except BaseException as e:
            self.__处理安装错误(e)



if __name__=="__main__":
    资源 = TK设置()

    资源.主线安装()
