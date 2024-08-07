## 主页构建器基础逻辑
### 页面构成
构建器认为一个主页页面是由若干个卡片叠放而成的。所以简单来说构建器只会做这样一套流程：

1. 找到页面需要的卡片
2. 生成卡片的 XAML 代码
3. 按顺序将 XAML 代码堆在一起

所以对于一个主页来说，我们只需要交给它两样东西：一堆**卡片** 和 **页面所用的的卡片的名称列表**（我们将其扩展为**页面**这个概念）。

#### 卡片
一个大型的主页所用到的卡片是数不胜数的，并且卡片之间有可能有共同的某种特征和构建方法，因此主页构建器使用 **卡片库**（简称为**库**）来存放并管理这些卡片。
库存在于工程文件夹下的 `Libraries` 文件夹，库文件夹中会存在许多文件，但总而言之只有两类：

* `__LIBRARY__.yml` 这里存放着库的基本信息，包括库名和对其内所有卡片生效的属性
* 其他文件 所有其它文件都是用于存储卡片信息的，一个文件就是一个卡片。

例如：在模版工程中，Libraries文件夹中有两个文件，`Hello_World.md` 与 `__LIBRARY__.yml`，其中 `Hello_World.md` 文件声明并存放着其文件名 `Hello_World` 这张卡片的信息，`__LIBRARY__.yml` 用于向 `Hello_World` 这张卡片提供一些属性。

为便于管理，库中可能会有一些文件夹，这些文件夹可能为 “子库”（取决于其中是否存在 `__LIBRARY__.yml`），子库会继承父库的一些属性，并且同样可以管理其中的卡片，这里不做重点介绍。

#### 页面
页面存在于工程文件夹下的 `Pages` 文件夹，其中可能存放着两种文件

* `*.yml` 使用 YAML 语言描述的页面内容，包含页面名称、页面所拥有的卡片等信息，也是构建器使用的最常见的一种
* `*.xaml` PCL 能直接读取的 XAML 语言文件，构建该页面会直接返回文件内容

##### 示例1
在模版工程中，Pages文件夹中有一个文件，`Main.yml`:
```yml
cards:
 - Hello_World
```
描述该页面生成后会有 `Hello_World` 这个卡片。

##### 示例2
有这样一个工程，库中有三个卡片：`A`、`B`、`C`，此时页面 `Main.yml` 的内容为:
```yml
cards:
 - A
 - B
 - C
```
在构建页面后，在 PCL 中你会以从上到下的顺序看到ABC三个卡片，说明 cards 字段不仅描述存在什么卡片，也描述了卡片的位置。

### 模版
主页构建器要处理的卡片多种多样，Markdown文件是如何变成卡片的，如何知道这个卡片应该长什么样，构建器使用卡片的一个名为 `template`（**模版**） 属性决定卡片是什么样子的。

构建器内置了许多模版，模版描述了一个卡片的具体架构，卡片使用 `template` 属性来告诉构建器 “我应该用哪个模版来塑形我”。

例如当构建器生成 `Hello_World` 卡片时，它会向根库（所有库的公共祖先，拥有所有卡片的信息）请求获取该卡片的信息，库反回来的东西大概是这样的：

```JSON
"canswap": True,
"templates": ["MarkdownCard", "Raw"]
"markdown": "# 我的第一张卡片\n## 从这里，走向世界\n* 你好世界！\n"
"data": {...}
"file_name": "Hello_World"
"file_exten": "md"
"card_id": "root:Hello_World"
"card_lib": "root"
"card_name": "Hello_World"
```
模版将要通过这几个信息来生成相应的XAML代码。

模版拥有匹配规则（一般是匹配文件后缀名），你可以见到 `templates` 这个属性是一个列表，这样它就可以尝试匹配最靠前的一个模版，如果匹配上了则使用该模版，如果匹配不上则尝试使用下一个模版。

模版可以自定义，在此不做叙述。

主页构建器已经内置了几个模版，当你构建的时候就不需要重新写这些模版。（除非你有自己的需求）

|模版名称|描述|匹配规则|
|----|----|----|
|`CardFrame`|只有卡片元素的框架，其中只能放入一个 Xaml 元素|*仅用于继承*|
|`Card`|可以以列表呈现 Xaml 元素内容的卡片，卡片的最基本形态|*仅用于继承*|
|`FlowDocCard`|有流文档阅读器的卡片|*仅用于继承*|
|`Raw`|纯 Xaml，没有卡片框架的模版|匹配后缀为 .xaml 的文件|
|`RawCard`|套在卡片框架下的纯 Xaml|匹配后缀为 .xaml 的文件|
|`MarkdownCard`|呈现 Markdown 内容的卡片 *(插件扩展)*|匹配后缀为 .md .markdown 的文件