ProjectInfo 插件
==============
ProjectInfo 插件为构建器提供了工程文件的额外信息。

使用
--------------
.. tip:: 该插件默认安装并启用，你无须手动启用该插件


Git 功能
~~~~~~~~~~~~~~
该功能默认启用，如果需要你可以将配置中的 `ProjectInfo.GitInfo.Enable` 设为 `False` 来禁用这些功能。
在使用这些功能之前请确认环境中安装了 Git。

版本号提供
++++++++++++++
该类使得构建器服务器在收到获取版本请求的时候能以当前工程的 Commit 版本哈希作为版本号输出给客户端。你可通过增加以下配置启用这项功能。

.. code-block:: yaml

   Server.Version.By: "githash"

配置
++++++++++++++
以下是可以选择的配置：

* `ProjectInfo.GitInfo.NoProduceNotInstalledWarning` - 若设为 `True`，在启用了 Git 功能但没有安装 Git 时不再产生警告提示。默认为 `False`
* `ProjectInfo.GitInfo.NoProduceNotRepoWarning` - 若设为 `True`，在启用了 Git 功能但工程未受到 Git 的版本管理时不再产生警告提示。默认为 `False`