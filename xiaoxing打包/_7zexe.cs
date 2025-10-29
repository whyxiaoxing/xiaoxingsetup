using System.Diagnostics;
using System.Windows;

namespace xiaoxing打包;

public class _7zexe
{
    public async Task _7zexerunAsync()
    {
       
        string 解压命令 = $"x \"{基础数据接口.接口.解压文件7z}\" -o\"{基础数据接口.接口MVVM.M程序路径}\" -y";

        ProcessStartInfo Infomessage = new ProcessStartInfo
        {

            FileName = 基础数据接口.接口._7zexe位置,
            Arguments = 解压命令,
            RedirectStandardOutput = false,   
            RedirectStandardError = false,
            UseShellExecute = false,
            CreateNoWindow = true
        };
        using (Process p_ = Process.Start(Infomessage))
        {
            p_.WaitForExit();
            switch (p_.ExitCode)
            {
                case 0:
                    break;
                case 1:
                    MessageBox.Show("警告：部分文件可能被锁定或 CRC 校验不匹配", "警告",
                                    MessageBoxButton.OK, MessageBoxImage.Warning);
                                    
                    break;

                case 2:
                    MessageBox.Show("致命错误：程序错误请反馈开发者", "7z解压错误",
                                    MessageBoxButton.OK, MessageBoxImage.Error);
                                    强制退出();
                    break;

                case 7:
                    MessageBox.Show("命令行错误：程序错误请反馈开发者", "7z解压错误",
                                    MessageBoxButton.OK, MessageBoxImage.Error);
                                    强制退出();
                    break;

                case 8:
                    MessageBox.Show("内存不足：7-Zip 申请内存失败", "7z解压错误",
                                    MessageBoxButton.OK, MessageBoxImage.Error);
                                    强制退出();
                    break;

                case 255:
                    MessageBox.Show("用户中断：操作已被手动取消", "提示",
                                    MessageBoxButton.OK, MessageBoxImage.Information);
                                    强制退出();
                    break;

                default:
                    MessageBox.Show($"未知返回码：{p_.ExitCode}", "7z解压错误",
                                    MessageBoxButton.OK, MessageBoxImage.Error);
                                    强制退出();
                    break;
            }

        }
        await Task.Delay(6000);
        基础数据_静态.循环bool = false; 
       

    }

    void 强制退出(){
       GC.Collect();
       Environment.Exit(1);


    }
}
