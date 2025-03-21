附加语法
==============
为了扩展 Markdown 功能，Markdown 插件还额外支持了更多语法。

内置附加语法
--------------
Wiki Link
~~~~~~~~~~~~~~
你可以像在 Meida Wiki 中使用 Wiki Link 一样使用双方括号创建链接到中文 Minecraft Wiki 或其他 Wiki 的链接，如：

::

    [[苦力怕]]是一种在夜晚生成的敌对生物，它在靠近玩家时会试图通过自爆对玩家造成伤害。....

其中 “苦力怕” 的位置创建一个链接到中文 Minecraft Wiki 苦力怕的页面。

你可以通过修改配置项 `markdown.preprocessor.wikilink.wikiurl` 来使用其它 Wiki，如将默认 Wiki 修改为中文维基百科：

.. code-block:: yaml

    markdown.preprocessor.wikilink.wikiurl: "https://zh.wikipedia.org/"

警报
~~~~~~~~~~~~~~
插件引入了 Github 的警报语法，用于强调关键信息，提醒用户注意。

.. code-block:: markdown

    > [!NOTE]
    > 用户所要知道的有用的信息。

    > [!TIP]
    > 用于帮助用户更好更轻松的完成目标的提示。

    > [!IMPORTANT]
    > 用户需要知道的关键信息。

    > [!WARNING]
    > 用于使用户避免问题的使用户注意到的紧急的信息。

    > [!CAUTION]
    > 对该行为后果产生的风险与消极后果的建议。

除此之外，你也可以使用以下警报扩展创建 PCL 内置的警报框

.. code-block:: markdown

    > [!INFO]
    > 这会创建一个蓝色底的信息框

    > [!WARN]
    > 这会创建一个红色底的警告框

协议扩展
~~~~~~~~~~~~~~
你可以使用扩展后的链接语法来使用 PCL 的某些功能。

.. warning:: 下述协议格式仅在构建器内可用，无法在浏览器内正常使用

打开其它页面
++++++++++++++
你可以使用构建器在主页中插入打开其它主页地址的链接，只需要在主页的 json url 前插入 `pcl:homepage:`。如：

.. code-block:: markdown

    [打开新闻主页](pcl:homepage:https://news.bugjump.net/News.json)

为了方便使用，即使链接结尾不是`.json`，构建器也会自动补全。如你输入以下链接：

.. code-block::

    pcl:homepage:https://news.bugjump.net/News
    pcl:homepage:https://news.bugjump.net/News/
    pcl:homepage:https://news.bugjump.net/News.xaml

打开的主页的 json 均是 `https://news.bugjump.net/News.json`

启动游戏
++++++++++++++
你可以使用构建器在主页中插入启动特定游戏的链接，并可进入特定服务器，链接语法为

.. code-block::

    pcl:launch://[游戏版本]/[服务器]

* **游戏版本**: 可选，待启动的版本，若留空（或填写 `current` ）将启动启动期当前选中的版本
* **服务器**: 可选，服务器的 IP 或域名，若填写则在游戏启动后自动加入加入指定的服务器

例如：

* 启动 1.12.2 `pcl:launch://1.12.2`
* 启动 1.12.2 并加入 Hypixel 服务器 `pcl:launch://1.12.2/mc.hypixel.net`
* 启动当前版本 `pcl:launch://`
* 启动当前版本并加入 Hypixel 服务器 `pcl:launch://current/mc.hypixel.net`

复制文本
++++++++++++++
使用以下链接将复制文本

::

    pcl:copy://<需要复制的文本>

刷新主页
++++++++++++++
使用以下链接将刷新主页

::

    pcl:refresh_homepage://

下载文件
++++++++++++++
使用以下链接格式将下载指定文件

::

   pcl:download:https://example.com

今日人品
++++++++++++++
使用以下链接将使用弹窗展示今日人品

::

    pcl:jrrp://

清理垃圾
++++++++++++++
使用以下链接将调用清理游戏垃圾

::

    pcl:rubclean://

内存优化
++++++++++++++
使用以下链接将调用内存优化

::
    
    pcl:ramclean://