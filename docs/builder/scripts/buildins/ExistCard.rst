ExistCard
=============

.. automodule:: homepagebuilder.modules.ExistCard
    :undoc-members:
    :no-index:
    :members: exist_card
   

简介
-------------
获取库中是否有名为 `<cardname>` 的卡片

返回: bool

使用
-------------
可以配合 IF 脚本使用该脚本

例：

.. code-block::

    ${@IF | ${@ExistCard | <cardname>} | content }


