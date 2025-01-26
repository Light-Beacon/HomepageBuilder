快速上手
=================
安装
----------------
1. 安装 python 3.10 以上版本
2. 下载代码 
   
   * 最新版: https://github.com/Light-Beacon/HomepageBuilder/releases/latest
   * 正式版: https://github.com/Light-Beacon/HomepageBuilder/releases
  
3. 解压
4. 安装，在解压的目录中使用终端，运行:
   
.. code-block:: shell
    
    pip install .


创建工程
----------------
在空目录下执行以下命令创建一个初始工程

.. code-block:: shell

    builder initproject

启动
----------------
构建模式
~~~~~~~~~~~~~~~~
在工程文件夹运行以下命令来构建主页

.. code-block:: shell

    builder build


构建器会将生成的主页放入文件夹中的 `output.xaml`，你也可以使用参数改变生成位置。

常用可选参数
****************

* **-p**, **--page <page>**: 指定所要生成的页面
* **-a**, **--all-page**: 生成所有页面
* **--project <path>**: 工程文件绝对路径
* **--output-path <path>**: 指定输出文件位置
* **--dry-run**: 不生成输出文件


服务器模式
~~~~~~~~~~~~~~~~
构建器支持作为服务器运行，自动构建并返回页面 xaml 代码，且支持主页版本号。

Flask
****************

在测试环境中，你可以直接在工程文件夹下运行以下命令来启动 Flask 服务器。

.. code-block:: shell

    builder server

可选参数
++++++++++++++++

* **-p**, **--port <port>**: 监听端口号
* **--project <path>**: 工程文件绝对路径

.. IMPORTANT::
    不建议在生产环境中使用 Flask 服务器，若在生产环境中使用建议使用下方 Gunicorn 或其它 WSGI 服务器

Gunicorn
****************

在生产环境中，你可以使用 gunicorn 进行服务器部署。

1. 安装gunicorn

.. code-block:: shell
    
    pip install gunicorn

2. cd 至工程目录
3. 启动 gunicorn
   
.. code-block:: shell

    gunicorn 'homepagebuilder.server:app()'


常用可选参数
++++++++++++++++

* **-b**, socket 绑定（监听），如 `0.0.0.0:6608`
* **-w**, worker 数量，推荐每服务器核心 2-4 个 worker

你可以查阅 [Gunicorn 官方文档](https://docs.gunicorn.org/en/stable/run.html) 获取更多 Gunicorn 相关内容