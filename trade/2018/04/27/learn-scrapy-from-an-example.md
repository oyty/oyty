
## [Scrapy-2] 从一个简单例子了解Scrapy

####创建Scrapy项目
进入到你要创建项目的目录，键入下面命令：
```python
oyty-mbp:python oyty$ scrapy startproject tutorial
New Scrapy project 'tutorial', using template directory '/usr/local/lib/python3.6/site-packages/scrapy/templates/project', created in:
    /Users/oyty/Documents/newworkspace/python/tutorial
```
创建了一个`tutorial`的目录，内容如下：
```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py

```

#### 第一个爬虫
Scrapy使用Spiders的类去爬取一个或多个网页，这些类必须是`scrapy.Spider`的子类，一定要定义初始的请求，然后你可以选择性地解析网页里面的links，下载和解析网页内容。
创建我们第一个爬虫类：`tutorial/spiders/quotes_spider.py`
```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        print(page)
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```
- `name`：作为Spider的标识，它必须是唯一的，也就是说你在同一个项目中你不能为不同的爬虫类设置相同的name。
- `start_requests()`：必须返回可迭代的`Requests`对象（你可以返回一个requests的数组，也可以返回一个生成器），Scrapy将从这些请求开始爬取，后续的请求在这些初始请求后产生。
- `parse()`：解析方法，每一个请求后都会被调用，参数`response`是一个`TextResponse`对象，这个对象包含了网页的内容，并且有内置了很多有用的处理网页内容的方法。

`parse()`方法通常用来解析response，将网页内容解析为字典，然后在网页中找到新的URLs，再创建新的爬取请求。

#### 运行我们的爬虫
在项目的跟目录下，运行下面命令：
```python
scrapy crawl quotes
```
第二个参数就是我们定义在爬虫类中的`name`。

这个地方要明白一点的是，我们`start_requests`中有多个请求，这些请求是异步发起，后续的response解析也都是相互独立的，这样大大提升了爬虫的效率。

#### `start_requests`的一种快捷方式
在`scrapy.Spider`类中已经定义了`start_requests`方法：
```python
def __init__(self, name=None, **kwargs):
    if name is not None:
        self.name = name
    elif not getattr(self, 'name', None):
        raise ValueError("%s must have a name" % type(self).__name__)
    self.__dict__.update(kwargs)
    if not hasattr(self, 'start_urls'):
        self.start_urls = []

def start_requests(self):
    cls = self.__class__
    if method_is_overridden(cls, Spider, 'make_requests_from_url'):
        warnings.warn(
            "Spider.make_requests_from_url method is deprecated; it "
            "won't be called in future Scrapy releases. Please "
            "override Spider.start_requests method instead (see %s.%s)." % (
                cls.__module__, cls.__name__
            ),
        )
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
    else:
        for url in self.start_urls:
            yield Request(url, dont_filter=True)
```
从上面的代码我们可以知道，首先呢，`make_requests_from_url`这个方法已经过期了，所以啊你最好不要用了，要用`start_requests`方法。`start_requests`方法默认其实是返回了`start_urls`的迭代，而`start_urls`是Spider类的一个属性，子类自然也就获取了这个属性，所以只要在子类中初始化`start_urls`就可以了，不用再重写   `start_requests`方法。
```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
```

