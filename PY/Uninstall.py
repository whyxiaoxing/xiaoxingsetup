import asyncio
import json
from pathlib import Path
import threading
import tkinter
from tkinter import messagebox


最大并发数量 = 10


async def 删除路径(路径: Path, 无法删除列表: list[str], 并发限制: asyncio.Semaphore) -> None:
    if 路径.is_dir() and not 路径.is_symlink():
        try:
            子路径列表 = list(路径.iterdir())
        except Exception:
            无法删除列表.append(路径.name)
            return

        子任务 = [
            asyncio.create_task(删除路径(子路径, 无法删除列表, 并发限制))
            for 子路径 in 子路径列表
        ]

        if 子任务:
            await asyncio.gather(*子任务)

        async with 并发限制:
            try:
                await asyncio.to_thread(路径.rmdir)
            except Exception:
                无法删除列表.append(路径.name)
        return

    async with 并发限制:
        try:
            await asyncio.to_thread(路径.unlink)
        except Exception:
            无法删除列表.append(路径.name)


async def 删除安装内容(安装路径: Path) -> list[str]:
    无法删除列表: list[str] = []
    并发限制 = asyncio.Semaphore(最大并发数量)

    删除任务 = [
        asyncio.create_task(删除路径(子路径, 无法删除列表, 并发限制))
        for 子路径 in 安装路径.iterdir()
    ]

    if 删除任务:
        await asyncio.gather(*删除任务)

    return 无法删除列表


def main() -> None:
    当前目录 = Path(__file__).resolve().parent

    with open(当前目录 / "Uninstall.json", "r", encoding="utf-8") as 文件:
        安装路径 = Path(json.load(文件)["InstallPath"])

    root = tkinter.Tk()
    root.withdraw()

    if not messagebox.askyesno("卸载", "是否删除该程序？"):
        root.destroy()
        return

    def 卸载完成(无法删除列表: list[str]) -> None:
        if 无法删除列表:
            messagebox.showinfo("无法删除", "\n".join(无法删除列表))

        messagebox.showinfo("卸载完成", "卸载完成")
        root.destroy()

    def 后台卸载() -> None:
        无法删除列表 = asyncio.run(删除安装内容(安装路径))
        root.after(0, 卸载完成, 无法删除列表)

    threading.Thread(target=后台卸载, args=(), daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    main()
