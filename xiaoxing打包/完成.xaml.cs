using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace xiaoxing打包
{
    public partial class 完成 : Page
    {
        private readonly Frame _frame;
        public 完成(Frame frame )
        {
            _frame = frame;
            InitializeComponent();
            
        }

        private void 完成安装(object sender, RoutedEventArgs e)
        {

            Environment.Exit( 0 );
        }
    }
}
