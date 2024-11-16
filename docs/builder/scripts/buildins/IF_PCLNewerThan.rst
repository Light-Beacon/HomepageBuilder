IF_PCLNewerThan
=====================

.. automodule:: homepagebuilder.modules.pcl_versions
    :undoc-members:
    :no-index:
    :members: newer_script
   
简介
-------------
判断 PCL 版本是否比 `<versionid>` 高或相等，若是输出 `<content>` 内容

返回: str

使用
-------------
可以在卡片中插入该脚本判断 PCL 是否支持该构件

.. code-block::

    ${@IF_PCLNewerThan |<versionid>|<content>}
