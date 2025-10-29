import ctypes
import subprocess
import sys
import tkinter.messagebox
import winreg

if __name__ == '__main__':

     a=ctypes.windll.shell32.IsUserAnAdmin()
     if not a:
          ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
          sys.exit(0)
     try:
          with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\NET Framework Setup\NDP\v9.0',0,winreg.KEY_READ):
               print("已经存在net9 Desktop Runtime")
               subprocess.run(['start',""],shell=True,check=True)

     except Exception as e:
          print("不存在net9 Desktop Runtime")
          结果=tkinter.messagebox.askokcancel("无法检测到dotnet9环境","您没有安装dotnet9 Desktop Runtime 是否安装dotnet9")
          if 结果:
                subprocess.run(['start','/wait',"./dotnet9.exe"],shell=True,check=True)
                subprocess.run(['xiaoxing安装程序.exe'], shell=True)

          else:
               sys.exit(1)