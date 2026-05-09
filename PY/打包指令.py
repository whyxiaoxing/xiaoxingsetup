import subprocess


使用conda = False

项目目录 = r"D:\pycode\study"

venv激活脚本 = r"D:\pycode\study\.venv\Scripts\activate.bat"

conda激活脚本 = r"D:\Anaconda3\Scripts\activate.bat"
conda环境名 = "YOLO"

pyinstaller命令 = (
    r'pyinstaller --noconsole -F --clean '
    r'--icon "D:\pycode\study\1.ico" '
    r'--add-data "data;data" '
    r'--runtime-tmpdir ./ '
    r'"打包文件.py"'
)

if 使用conda:
    命令 = rf'call "{conda激活脚本}" "{conda环境名}" && {pyinstaller命令}'
else:
    命令 = rf'call "{venv激活脚本}" && {pyinstaller命令}'

subprocess.run(
    命令,
    cwd=项目目录,
    shell=True,
    check=True
)