# xiaoxing打包APP

- 基于C#的WPF
- 附带py脚本检测工具
- 支持安装时候基本功能，

## 目录结构

```xiaoxingsetup
├── pic
│   ├── 1.ico
│   │   
│   ├── 图片资源
├── _7zexe.cs //7z解压
├── 动画.xaml.cs //解压时候动画以及解压过程
├── 基础数据.cs //程序数据位置
├── 自定义安装.cs //自定义安装界面
```

## 数据部分

> > 基础数据.cs 内部包含了80%以上的数据位置，需要可以自定义修改变量
> > 可以自定义背景图片，以及icon
> > 可以往 ``` public partial class MVVM数据库 : ObservableObject ``` 内添加数据，绑定至xaml部分

## 后续

> > 该程序仅维护两个版本
> > 下一个版本主要目标是加入updata功能，以及优化安装流程

## 开发人员

>>> whyxiaoxing
>>>
