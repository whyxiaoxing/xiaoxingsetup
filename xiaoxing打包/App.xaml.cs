using System.Windows;
using System.Windows.Media.Imaging;

namespace xiaoxing打包;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public static class 基础数据接口
{
    
    public static xiaoxing打包.基础数据 接口 = new xiaoxing打包.基础数据();
    public static xiaoxing打包.MVVM数据库 接口MVVM = new MVVM数据库(); 
}


public partial class App : Application
{


    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
       
        Task.Run(() => { 初始化过程(); });
    }

    static void 初始化过程() {

        基础数据接口.接口.当前目录 = System.IO.Directory.GetCurrentDirectory();
        long 大小 = 可用函数.统计安装所需空间(基础数据接口.接口.当前目录 + "/安装主体");
        double MB大小 = (double)大小 / (1024 * 1024);
        基础数据接口.接口MVVM.M需要磁盘空间 = MB大小.ToString("F2") + "MB";

        //基础数据修改位置
        基础数据接口.接口.EXE位置 = 基础数据接口.接口MVVM.M程序路径 + @"/QQWX自动轰炸.exe";
        基础数据接口.接口._7zexe位置 = 基础数据接口.接口.当前目录 + @"\7z\7z.exe";
        基础数据接口.接口.解压文件7z = 基础数据接口.接口.当前目录 + @"\test.7z";
}
    

    

    


}


