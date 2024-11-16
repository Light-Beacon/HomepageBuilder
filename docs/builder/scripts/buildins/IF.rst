IF
=============

.. automodule:: homepagebuilder.modules.IF
    :undoc-members:
    :no-index:
    :members: if_script
   

简介
-------------
判断 `<eq_expression>` 结果是否为真

真则输出 `<true_return>`，假且提供 `[false_return]` 时则输出 `[false_return]`

返回: str

使用
-------------
IF 脚本非常常用，它可以插在文档中，也可以插在模版中，只要有需要判断的地方就可以用它

.. code-block::

    ${@IF |<eq_expression>|<true_return>|[false_return]}

参数
-------------
* **eq_expression** - 等号表达式，详见下方表达式章节
* **true_return** - 为真时输出的内容
* **false_return** - （可选）为假时输出的内容，若不提供则不输出

相等表达式
-------------
表达式 `<eq_expression>` 可以为：

* 某个值。`false`、`null`、`none` 为假，其它均为真
* 某个引用或脚本。如 `${title}`，其格式化后值的判断与上一条相同
* 开始为`!`的某个值或引用，其后内容基于前两条判断，且真改为假，假改为真
* 某个含`=`的表达式。如 `${isswaped} = true`，判断等号前与等号后的值或引用格式化后是否相等
* 某个含`!=`的表达式。如 `${isswaped} != true` 判断等号前与等号后的值或引用格式化后是否不相等
