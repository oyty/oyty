
## [Scrapy-3] 理解Scrapy的Response的数据结构


﻿我们知道，`Scrapy`最终给到我们的是`response`对象，了解了`response`的数据结构，我们就能更好的解析利用`response`数据。

####先来理解Response这个类
通过Response对象本身可以直接访问的对象或方法有：
```python
def __init__(self, url, status=200, headers=None, body=b'', flags=None, request=None):
    self.headers = Headers(headers or {})
    self.status = int(status)
    self._set_body(body)
    self._set_url(url)
    self.request = request
    self.flags = [] if flags is None else list(flags)

@property
def meta(self):
    try:
        return self.request.meta
    except AttributeError:
        raise AttributeError(
            "Response.meta not available, this response "
            "is not tied to any request"
        )

url = property(_get_url, obsolete_setter(_set_url, 'url'))

body = property(_get_body, obsolete_setter(_set_body, 'body'))
```
从上面的代码可以知道，通过Response对象可以直接访问的属性有`headers`，`status`， `request`， `meta`，meta即是属性也是方法， `url`， `body`，以上可以直接获取内容，还有一些方法比如`text()`，`css()`，`xpath()`，在子类中实现可以使用。

#### 看看Response的子类
```python
Response
----TextResponse
--------HtmlResponse
--------XmlResponse
```
`HtmlResponse`，`XmlResponse`两个类本身只是简单的继承了`TextResponse`，没有做任何实现，所以我们重点来看看`TextResponse`类。
`TextResponse`的主要是添加了一个新的构造函数，encoding。这个暂时还不能细致的理解，事实上对这个Python体系的编码都很晕，先放放吧。
`TextResponse`对父类的一些未实现的方法做了实现：
```python
@property
def text(self):
    """ Body as unicode """
    # access self.encoding before _cached_ubody to make sure
    # _body_inferred_encoding is called
    benc = self.encoding
    if self._cached_ubody is None:
        charset = 'charset=%s' % benc
        self._cached_ubody = html_to_unicode(charset, self.body)[1]
    return self._cached_ubody

@property
def selector(self):
    from scrapy.selector import Selector
    if self._cached_selector is None:
        self._cached_selector = Selector(self)
    return self._cached_selector

def xpath(self, query, **kwargs):
    return self.selector.xpath(query, **kwargs)

def css(self, query):
    return self.selector.css(query)
```
一般情况下，我们爬取网页获取到的`Response`对象是`HtmlResponse`，从上面的源码我们可以知道，Scrapy的数组组织结构是`Selector`。

从Html源解析数据一般有两种方式：

- `BeautifulSoup`，这个类比较有名了，它对一些标记不规范的HTML也有很好的适应能力，但它最大的缺点就是--`太慢了`。
- `lxml`，这是一个xml解析库，当然也能用来解析html，lxml并不是Python的标准库，但是它有基于`ElementTree`的极具Python风格的API。

Scrapy的`Selector`是基于lxml构建的，所以在速度和解析精度上和lxml相似。

虽然lxml的语法很强大，能够处理很多其它的任务，但是在这里，Selector的语法就很简单，这也决定了Selector的解析方式。
Seelctor或者说Scrapy的数据对象有以下三种解析方式

- ﻿`xpath`
- `css`
- `re`

这个从Selector的源码可以看出，不喜欢`css`和`re`（主要是太麻烦了，记得东西太多，每次用还要现学），我们数据解析的话就专门使用`xpath`，下一节就来好好学习学习`xpath`的语法。

```python
def css(self, query):
    """
    Apply the given CSS selector and return a :class:`SelectorList` instance.

    ``query`` is a string containing the CSS selector to apply.

    In the background, CSS queries are translated into XPath queries using
    `cssselect`_ library and run ``.xpath()`` method.
    """
    return self.xpath(self._css2xpath(query))
```
发现个比较变态的，css底层实现也是先将css转成xpath。那就不需要多此一举了。




