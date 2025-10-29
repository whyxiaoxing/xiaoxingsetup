using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace xiaoxing打包;


public partial class 动画 : Page
{
    private readonly Frame _frame;
    BitmapImage 图片1 = new BitmapImage(new Uri("pack://application:,,,/pic/showend1.png"));
    BitmapImage 图片2 = new BitmapImage(new Uri("pack://application:,,,/pic/showend2.png"));
    BitmapImage 图片3 = new BitmapImage(new Uri("pack://application:,,,/pic/showend3.png"));
    public 动画(Frame frame)
    {
        InitializeComponent();
        _frame = frame;
        _7zexe  解压7zexe= new _7zexe();
        Task.Run(() => { 图片更新(1); });
        Task.Run(async () =>
        {
            await 解压7zexe._7zexerunAsync();
        })
    .ContinueWith(t =>
    {

        _frame.Dispatcher.Invoke(() =>
        {

            if (基础数据_静态.循环bool == false)
            {
                完成 完成_实例 = new 完成(_frame);
                _frame.Content = 完成_实例;
                动画xaml.Visibility = Visibility.Collapsed;

            }
            else { MessageBox.Show("错误，不是falese", "look"); }
        });
    }, TaskScheduler.FromCurrentSynchronizationContext()); //需要回归主线程 执行
        Task.Run(() =>
        {
            if (基础数据接口.接口MVVM.M快捷键事件)
            {
                可用函数.创建快捷方式();
            }
        });


    }

    private async Task 图片更新(int 次数)
    {
       
        while (基础数据_静态.循环bool ==true)
        {   
            Application.Current.Dispatcher.Invoke(() =>
            {
                if (次数 == 1)
                {
                    图片显示xaml.Source = 图片1;
                   
                }
                else if (次数 == 2)
                {
                    图片显示xaml.Source = 图片2;
                   
                }
                else if (次数 == 3)
                {
                    图片显示xaml.Source = 图片3;
                   
                }
                else
                {
                    次数 = 1;
                    图片显示xaml.Source = 图片1;
                    
                }
                
            });
            await Task.Delay(3000);
            次数++;
            
        }
     }
}
