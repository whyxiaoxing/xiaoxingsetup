# XIAOXING 安装程序 

## 文件介绍

| 文件名 | 作用 |
| --- | --- |
| 打包文件.py | 主要程序负责安装 |
| Uninstall.py | 卸载程序 |
| data 目录 | 存放数据文件  |

---
data 目录下方解压的7z文件
dotnet 是安装前检查的必要运行时文件

--- 
- 使用办法
1. 先运行使用pip 命令安装必要的包
> `pip3 install -r Packaeg.txt `
2. 先更改`打包文件.py` 内的两个类的`init` 的数据
3. 先使用pyinstaller 编译uninstall.py
4. 运行打包指令
   
