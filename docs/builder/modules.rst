模块
=================
模块（Module）是在构建时可以运行的自定义代码，用于增加、修改、删除构建器运行行为，它们放在工程文件夹的`modules`文件夹中，目前所有的模块都为 python 文件。

模块通常被用来定义[[脚本]]，有时也会用来执行事件，也可以定义文件读写方法，版本号获取方法等。

编写模块
-----------------
构建器提供了很多接口，这些都集中放在 `homepagebuilder.interfaces` 中，你可以通过 `from homepagebuilder.interfaces import` 来导入一些需要的接口。

脚本
~~~~~~~~~~~~~~~~
脚本是模块要实现的主要功能，你可以在模块中编写脚本，详见 :doc:`脚本<../builder/scripts/index>` 页面。

事件
~~~~~~~~~~~~~~~~
当某一个事件触发时，构建器会路由到订阅该事件的函数，如你可以通过订阅事件在构建主页后执行一些操作，或者覆盖某个函数的结果。

文件读取方法
~~~~~~~~~~~~~~~~
若你的文件格式不在构建器的支持范围内，你可以自定义文件读取方法来支持这类文件。

你需要引入 `homepagebuilder.core.io.accessor.file_reader` 这个装饰器来装饰你的文件读取方法来进行注册

.. code-block:: python

    from homepagebuilder.core.io.accessor import file_reader

    @file_reader('ext1','ext2') # 读取文件扩展名为 .ext1 和 .ext2 的文件
    def myfilereader(filepath:str) -> object: # filepath 为文件绝对路径
        with open(filepath, "r+",encoding="utf-8") as file:
            data = your_reader_method(file)
            data = your_process_data_function(data)
            return data
