using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace xiaoxing打包;

public partial class MainWindow : Window
{
    
    public MainWindow()
    {
        InitializeComponent();
        this.Closing += 基础数据接口.接口.退出事件;
       
    }

    private void 协议事件(object sender, MouseButtonEventArgs e)
    {
        string edge位置 = @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe";
        if (File.Exists(edge位置))
        {
            System.Diagnostics.Process.Start(edge位置, 基础数据接口.接口.当前目录+ @"\readme.html");

        }
        else
        {
            MessageBox.Show( $"esge默认位置{edge位置} 不存在在", "文件不存在");

        }
        
       

    }
    private 自定义安装? _自定义安装页面实例;
    private void 自定义安装( object sendr ,MouseButtonEventArgs e ){

        if (_自定义安装页面实例 == null)
        {
            _自定义安装页面实例 = new 自定义安装(Frame控件);
        }

        Frame控件.Content = _自定义安装页面实例;
        主界面.Visibility = Visibility.Collapsed;

    }
    private void 一键安装(object sender, MouseButtonEventArgs e){

      
          动画 动画实例 = new 动画(Frame控件);
        
        Frame控件.Content = 动画实例;
       主界面.Visibility = Visibility.Collapsed;

    }


}