import ctypes
import os.path
import shutil
import sys
import tkinter.messagebox
from codecs import ignore_errors

if __name__ == '__main__':
    a = ctypes.windll.shell32.IsUserAnAdmin()
    if not a:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)
    用户bool=tkinter.messagebox.askyesno("真的要删除我吗","确认开始删除")
    路径=os.getcwd()
    if 用户bool== True:
        shutil.rmtree(路径,ignore_errors=True)

    else:
        pass


