# 从 0 开始教你构建主页
## 准备工作
### 安装 Python
主页构建器所需 Python 版本为 3.9+
### 下载 HomepageBuilder 源码
你可以通过 GitHub Releases 或 Git Clone 下载构建器的源码 
#### 通过 Release
1. 打开 [HomepageBuilder 的最新发布版](https://github.com/Light-Beacon/HomepageBuilder/releases/latest)
2. 下载 Source code 文件（如果不知道下哪个好就下 zip）
3. 解压下载的文件到想存放的位置下
#### 通过 Git Clone
1. 在存放位置处运行 `git clone https://github.com/Light-Beacon/HomepageBuilder.git`
### 安装依赖
运行在文件夹以下命令以安装依赖
```bash
pip install -r requirements.txt
```
## 创建工程
### 主页工程的构成
构建器认为一个主页页面是由若干个卡片叠放而成的。所以简单来说构建器只会做这样一套流程：

1. 找到页面需要的卡片
2. 生成卡片的 XAML 代码
3. 按顺序将 XAML 代码堆在一起

所以对于一个主页来说，我们只需要交给它两样东西：**卡片信息** 和 **页面所拥有的卡片**。再多一项辅助生成的资源文件，就是整个工程文件夹的内容。

### 创建工程文件夹
工程文件夹根文件夹的内容一般有四个：

* Libraries - 卡片库文件夹 - *用来储存卡片信息*
* Pages - 页面文件夹 - *用来存储页面信息*
* Resource - 资源包文件夹
* Project.yml - 工程的描述文件

我们先找一个文件夹创建这些东西来继续我们的教程
### 编辑 Project.yml
`Project.yml` 有两个作用：告诉主页构建器工程路径，给主页构建器提供关于工程的必要信息

目前该文件只有两个有效键值：
```YAML
version: 0.9.0 # 这个工程对应的构建器版本
defult_page: DefultPage # 默认构建的页面
```
`version` 在当前版本没有任何作用，但必须填写

`defult_page` 告诉构建器在不指定页面名称的情况下默认输出哪个页面的代码

现在讲示例代码复制进文件里，或者你也可以按照你的需求更改

### 创建根卡片库
让我们进入到 Libraries 文件夹，创建一个名为`__LIBRARY__.yml`的文件，这个文件标识这个文件夹是一个主页构建器卡片库，其内容提供一些用于构建的参数
之后我们来编辑这个文件，将下面的代码写入文件
```YAML
name: rootLibrary # 卡片库的名称，你可以随意更改
fill: # 这些内容在进阶教程会有讲解，现在照做就好。 
   templates:
    - MarkdownCard
```
下面我们在这个文件夹里创建一个卡片文件 `HelloWorld.md`
``` Markdown
# 我的第一张卡片
## EXAMPLE
> 越过长城，走向世界！

* Hello World!
* Bonjour Le Monde!
* Ciao Mondo！
```
这些是这张卡片的内容，目前新闻主页构建器兼容 Markdown 部分语法，你在这里写的东西将会在最终的构建成果中有所体现

好了卡片库我们就先改到这里
### 创建第一个页面
我们进入工程文件的 `Pages` 文件夹，创建一个 `DefultPage.yml` 文件，文件内容为：
```
name: DefultPage # 页面名称，如果你之前在 Project.yml 中改过默认页面请按照实际情况命名
cards:
 - HelloWorld # 就是刚才文件的名字
```
这个文件表示 `DefultPage` 这个页面中存在一个名称为 `HelloWorld` 的卡片
## 构建主页
现在我们在解压后的目录下运行
```bash
python3 main.py -o <Project.yml的路径> -w <输出文件路径>
```
*⚠️ 注意： 这个仅仅是当前版本写法 之后会更改*

闪过一堆东西后你能在输出文件夹看到输出文件，将其改成 `Custom.xaml` 放进 PCL 文件夹就能用了