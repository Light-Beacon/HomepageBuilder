---
title: 行内链接
---

构建器支持行内链接。

如 `[打开示例网页](https://example.com)` 方括号内是链接文本，圆括号内是链接 URL

这是上面的显示效果：[打开示例网页](https://example.com)

### 更多功能
从 Pagebuilder 0.14.3 起，构建起支持除打开链接外的其他功能

#### 打开其它页面
你可以使用构建器在主页中插入打开其它主页地址的链接，只需要在主页的 json url 前插入 `pcl:homepage:` 
如 `[打开新闻主页](pcl:homepage:https://news.bugjump.net/News.json)`

http 与 https 均可使用。

这是上面的显示效果：[打开新闻主页](pcl:homepage:https://news.bugjump.net/News.json)

为了方便使用，即使链接结尾不是`.json`，构建器也会自动补全。
如你输入以下链接

```
pcl:homepage:https://news.bugjump.net/News
pcl:homepage:https://news.bugjump.net/News/
pcl:homepage:https://news.bugjump.net/News.xaml
```

打开的主页的 json 均是 `https://news.bugjump.net/News.json`

#### 启动游戏
你可以使用构建器在主页中插入启动特定游戏的链接，并可进入特定服务器，链接语法为
```
pcl:launch://[游戏版本]/[服务器]
```

**游戏版本**: 可选，待启动的版本，若留空（或填写 `current` ）将启动启动期当前选中的版本
**服务器**: 可选，服务器的 IP 或域名，若填写则在游戏启动后自动加入加入指定的服务器

##### 例
* 启动 1.12.2 `pcl:launch://1.12.2`
* 启动 1.12.2 并加入 Hypixel 服务器 `pcl:launch://1.12.2/mc.hypixel.net`
* 启动当前版本 `pcl:launch://`
* 启动当前版本并加入 Hypixel 服务器 `pcl:launch://current/mc.hypixel.net`

#### 今日人品
使用以下链接将使用弹窗展示今日人品
```
pcl:jrrp://
```

#### 清理垃圾
使用以下链接将清理游戏垃圾
```
pcl:rubclean://
```

#### 内存优化
使用以下链接将调用内存优化
```
pcl:ramclean://
```

#### 复制文本
使用以下链接将复制文本
```
pcl:copy://<需要复制的文本>
```

#### 刷新主页
使用以下链接将刷新主页
```
pcl:refresh_homepage://
```

#### 下载文件
使用以下链接格式将下载指定文件
```
pcl:download:https://example.com
```