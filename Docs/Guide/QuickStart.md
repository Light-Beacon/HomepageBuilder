# 快速上手
## 一、准备工作
### 1. 安装 Python
主页构建器所需 Python 版本为 3.9+

### 2. 下载 HomepageBuilder 源码
你可以通过 GitHub Releases 或 Git Clone 下载构建器的源码 

#### 通过 Release
1. 打开 [HomepageBuilder 的最新发布版](https://github.com/Light-Beacon/HomepageBuilder/releases/latest)
2. 下载 Source code 文件（如果不知道下哪个好就下 zip）
3. 解压下载的文件到想存放的位置下

#### 通过 Git Clone
1. 在存放位置处运行 `git clone https://github.com/Light-Beacon/HomepageBuilder.git .`

### 3. 安装依赖
#### 基础依赖
运行在文件夹以下命令以安装依赖
```bash
pip3 install -r requirements.txt
```
#### 服务器依赖
如果你需要使用构建器部署服务器，你需要额外安装服务器的依赖
```bash
pip3 install -r server_requirements.txt
```
## 二、构建主页
### 1. 获取主页工程模版
点击该[链接](https://github.com/Light-Beacon/HomepageProjectTemplate/archive/refs/heads/main.zip)下载工程文件模版并解压

### 2. 构建第一个主页
运行以下命令
```bash
python3 <构建器main.py的绝对路径> build <工程文件夹下Project.yml文件的绝对路径> <主页生成文件的绝对路径>
```

主页生成文件的绝对路径是你主页文件放在那里，一般是 PCL 可执行文件所在目录的 PCL 文件夹内的 Custom.xaml

### 3. 启动 PCL 查看主页
若你生成于PCL文件夹的 Custom.xaml，这时启动 PCL，将自定义主页选择本地文件，就可以看到主页啦！

## 三、添加卡片
