ForEach
=============

.. automodule:: homepagebuilder.modules.ForEach
    :undoc-members:
    :no-index:
    :members: for_each_script
   

简介
-------------
获取卡片的 `<iter_item_name>` 属性并迭代

对每一次迭代: 将 `<store_name>` 的值设为迭代变量，使用卡片和格式化 `<itemoutput>` 代码并输出

返回: str

使用
-------------
当有可迭代的变量时, ForEach 脚本可以像 str.join 那样将其全部展示出来

.. code-block::

    ${@ForEach |<store_name>|<iter_item_name>|<itemoutput>}

.. warning:: `<iter_item_name>` 必须为可迭代变量（如 list、dict）