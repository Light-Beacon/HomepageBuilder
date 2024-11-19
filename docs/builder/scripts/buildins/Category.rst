Category
=============

.. automodule:: homepagebuilder.modules.Category
    :undoc-members:
    :no-index:
    :members: cats
   

简介
-------------
获取所有卡片 `cats` 属性中含有 `<cat_name>` 的卡片名称列表

使用
-------------
在页面卡片列表中使用该脚本

例：

.. code-block:: yaml

    cards:
        - ${@Category |<cat_name>}


