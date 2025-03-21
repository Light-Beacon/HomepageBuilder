模版
=================
模版（Template）是指定卡片内部的结构的字典。

模版目录
-----------------
所有模版均放在工程文件夹的 `structures/templates` 文件夹中。

例如：

.. code-block::

    structures
    ├── components
    └── templates
        ├── MyFolder
        │   ├── TemplateB1.yml
        │   └── TemplateB2.yml
        ├── TemplateA1.yml
        └── TemplateA2.yml

模版相对于 templates 目录的路径称为 **模版引用**，当使用模版作为卡片模版，或者选择模版作为基模版时使用的名称即为引用。

如：

* TemplateA1 模版的引用为 `TemplateA1`
* TemplateB1 模版的引用为 `MyFolder/TemplateB1`

你可以通过创建和构建器模版引用相同的模版来覆盖内置或插件模版。

模版内容
-----------------
模版内容主要由以下字段组成：

* **components** - 卡片构件的列表
* **base** - 基模版
* **filter** - 筛选器
* **containers** - 容器路径
* 其它字段

.. code-block:: yaml

    components:
      - HeaderImage
      - FlowDocumentViewer
      - ToolBar
    base: MyFolder/TemplateB1
    containers: base -> MyContainer -> this
    filter:
        theme: night
        file_exten:
          - md
          - markdown
    fill:
        background: "{DynamicResource ColorBrush3}"

构件列表
~~~~~~~~~~~~~~~~~
一张卡片是由数个构件叠放与嵌套组成的。构件列表 components 指定了内部构件的叠放顺序。

例如：

.. code-block:: yaml

    components:
       - HeaderImage
       - FlowDocumentViewer
       - ToolBar
  
上面所例构件列表表示了在例子模版中这三个构件的是以同级，按照从上到下的顺序排列起来。当构建器生成卡片时将会从上到下生成这些构件。

基模版
~~~~~~~~~~~~~~~~~
构件之间不仅有叠放，还有嵌套。基模版也是模版，是子模版的父级，基模版嵌套子模版。

当构建器使用子模版生成卡片时，构建器会先生成其基模版内容。换句话说，生成时会先从模版嵌套路径最外层的模版生成内容，逐渐向内层创建。

当基模版的构件列表中的某一个构件使用了 :doc:`ChildrenPresenter<../scripts/buildins/ChildrenPresenter>` 脚本占位符,
构建器会将脚本占位符替换为子模版生成的内容。这样就实现了构件之间的嵌套关系。

基模版在配置中是以引用（字符串）形式配置的。

.. code-block:: yaml

    components:
     - FlowDocumentViewer
    base: MyFolder/TemplateB1 # 模版的名称


筛选器
~~~~~~~~~~~~~~~~~
卡片可以使用的模版存在卡片的 templates 属性中，其通常是个列表，卡片会匹配第一个筛选器匹配上的模版，使用该模版进行构建。

.. code-block:: yaml

    filter:
        theme: night
        file_exten:
         - md
         - markdown
    

filter 下的每个字段都是一个检查项，当所有检查项全部匹配的时候卡片才能匹配该模版。

检查项键为卡片的属性名，检查项值为卡片需要满足的值，若检查项值为一个列表，列表中的所有值满足其一即可。

如上面例子的意思是：匹配 theme 属性为 night 的，file_exten 属性为 md 或 markdown 的卡片。

容器路径
~~~~~~~~~~~~~~~~~
当需要嵌套的层数过多，使用时基模版都只有一个控件，使用模版作为嵌套会显得十分麻烦。容器路径为嵌套提供了一种新的解决方案。

.. code-block:: yaml

    base: TemplateA1
    containers: base -> MyContainer -> this

容器路径是一个必须从 *base（基模版）* 指向 *this（本模版）* 的路径。其中中间的节点的名称是构件的引用。
当使用该模版生成卡片时，构建器从生成基模版的 ChildrenPresenter 脚本的内容时，生成的不是本模版，而是从左到右先生成中间构件，
再将中间构件的 ChildrenPresenter 脚本替换成下一个中间构件的生成内容，直到到达 this 生成本模版的内容。

上面的例子中，构建器在生成 TemplateA1 的某一个构件时，其构件使用了 ChildrenPresenter 脚本占位符，构建器就会生成 MyContainer 构件的内容替换之。
若在 MyContainer 内容中也有 ChildrenPresenter 脚本占位符，构建器这才生成了本模版的内容替换之。用另一种方式实现了嵌套。
