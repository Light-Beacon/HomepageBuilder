自定义脚本
==============
一个脚本可以通过 `@script` 装饰器定义，例如：

.. code-block:: python

    from homepagebuilder.interfaces import script

    @script('your_script_name')
    def what_ever_you_want(env, card, arg1, arg2 = 'default_value', ...,  *args, **kwargs):
        return your_code(card, arg1, ...)

构建器不会关心函数的名称，你可以随意取名

* **env**: 当前环境 BuildingEnvironment
* **card**: 当前卡片
* **arg1**... : 使用脚本时输入的参数（命名可以自定义，运行时参数按照从左到右排序）

当在内容调用时，类似下方:

::

    ${@your_script_name|arg1value|${prop}}

当在卡片列表中调用时，类似下方

.. code-block:: yaml

    cards:
       - card1
       - ${@your_script_name|arg1value|arg2value}
       - card3