PublicConf
=============

.. automodule:: homepagebuilder.modules.config_script
    :no-index:
    :members: conf_script
   
简介
-------------
获取在 Public.<key> 配置的值

.. caution:: **请勿在 Public. 空间下存任何私钥、密码等隐私信息**

返回: str

使用
-------------
若需要定义全局变量，其中一个方法便是使用该脚本

.. code-block::

    ${@PublicConf | <key> | [default] }
