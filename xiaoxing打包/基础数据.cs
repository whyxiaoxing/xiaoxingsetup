using System.IO;
using System.Windows;
using System.Windows.Media.Imaging;
using CommunityToolkit.Mvvm.ComponentModel;
using IWshRuntimeLibrary;

namespace xiaoxing打包;


// 使用 CommunityToolkit.Mvvm的数据绑定
public partial class MVVM数据库 : ObservableObject{

    [ObservableProperty]
    private string? _m程序路径= @"D:\whyxiaoxing\QQWXbiubiubiu";
    [ObservableProperty]
    private string? _m需要磁盘空间="0MB";
    [ObservableProperty]
    private bool _m快捷键事件=true;
    
   



}

public class 基础数据

{  //以下变量我放在App.xaml.cs处赋予初始变量
    public string? 当前目录 = "";
    public string? EXE位置;
    public string? _7zexe位置;
    public string? 解压文件7z;




    public void 退出事件(object sender, System.ComponentModel.CancelEventArgs e)
    {
        MessageBoxResult resutl = System.Windows.MessageBox.Show("真的要退出安装吗？", "程序提示", MessageBoxButton.OKCancel);

        if (resutl == MessageBoxResult.Cancel)
        {

            e.Cancel = true;
        }
        else
        {

            GC.Collect();
            Application.Current.Shutdown();
        }


    }

}
public static class 基础数据_静态{

    public static BitmapImage? 图片1;
    public static BitmapImage? 图片2;
    public static BitmapImage? 图片3;
    public static volatile bool 循环bool = true;
}

public static class 可用函数{

    public static long 统计安装所需空间(string path)
    {
        if (!Directory.Exists(path)) return 0;

        long size = 0;
        foreach (var file in Directory.EnumerateFiles(path))
        {
            size += new FileInfo(file).Length;
        }
        foreach (var dir in Directory.EnumerateDirectories(path))
        {


            size += 统计安装所需空间(dir);
        }
        return size;
    }

    public static void 创建快捷方式(){
        string desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
        WshShell shell = new WshShell();
        IWshShortcut shortcut = (IWshShortcut)shell.CreateShortcut(desktopPath+@"\小星.lnk");
        shortcut.TargetPath = 基础数据接口.接口.EXE位置;
        shortcut.Description = "小星启动快捷键"; 
        shortcut.IconLocation = 基础数据接口.接口.EXE位置;
        shortcut.WorkingDirectory = 基础数据接口.接口MVVM.M程序路径;
        shortcut.Save();

    }

}
