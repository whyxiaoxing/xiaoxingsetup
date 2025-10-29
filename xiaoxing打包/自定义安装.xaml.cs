using System.IO;
using System.Windows;
using System.Windows.Controls;

namespace xiaoxing打包
{
    public partial class 自定义安装 : Page
    {
        private readonly Frame _frame;
        public 自定义安装(Frame frame)
        {
            this.DataContext = 基础数据接口.接口MVVM;
            InitializeComponent();
            _frame = frame;
        }

        private void 获取路径(object sender, RoutedEventArgs e)
        {

            Microsoft.Win32.OpenFolderDialog 文件句柄对象 = new();

            文件句柄对象.Multiselect = false;
            文件句柄对象.Title = "选择安装目录";
            bool? 获取_bool = 文件句柄对象.ShowDialog();
            if (获取_bool == true)
            {
                基础数据接口.接口MVVM.M程序路径 = 文件句柄对象.FolderName;
                基础数据接口.接口.EXE位置 = 基础数据接口.接口MVVM.M程序路径 + @"/QQWX自动轰炸.exe";

            }
            else
            {
                MessageBox.Show("没有选择路径或者选择空的路径", $"函数获取错误");

            }

        }

        private void 上一步(object sender, RoutedEventArgs e)
        {
            var main = (MainWindow)Application.Current.MainWindow;
            main.Frame控件.Content = null;
            main.主界面.Visibility = Visibility.Visible;

        }
        private void 安装信息(object sender , RoutedEventArgs e ) {

            string edge位置 = @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe";
            if (File.Exists(edge位置))
            {
                System.Diagnostics.Process.Start(edge位置, 基础数据接口.接口.当前目录+"/安装信息.html");
            }
            else
            {
                MessageBox.Show($"esge默认位置{edge位置} 不存在在", "文件不存在");
                
            }

        }
        private  动画? 动画实例;
        private void 开始安装(object sender, RoutedEventArgs e)
        {
             if (动画实例 == null){
                动画实例 = new 动画(_frame);
            }
            _frame.Content = 动画实例;
            自定义安装xaml.Visibility = Visibility.Collapsed;

        }
    }
}
