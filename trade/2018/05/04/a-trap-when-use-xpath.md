
##﻿[Scrapy-6] XPath使用的一个坑

﻿先上代码：
```python
import scrapy
from scrapy.selector import Selector


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com/"
    ]

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            print(quote.xpath("//span[@class='text']/text()").extract_first())
```
再看看网页的结构

![](/images/xpath-html.jpeg)

我们自然想当然的以为，第一步xpath，将包含quote的所有div都找出来，然后遍历每一个div，再到每一个div中找到quote，这样打印出来的应该是当前页面所有的quote。Try it。

你会发现打印出来的都是第一个div里面的quote，这就是坑了。
我来试着解释一下，当前的代码处理xpath是分段处理了的，只要没有extract或者extract_first，xptah的处理都是一个整体，也就是说，循环里面的处理实际上是连接了上面的xpath处理，所以处理对象是整个response，这样每次取得就是第一条数据，那么如何实现我们想要的那种处理方式呢，先将xpath的数据extract出来，这样就是固定的区域了，然后再包装成Selector对象进行xpath处理，代码如下：
```python
import scrapy
from scrapy.selector import Selector


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com/"
    ]

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']").extract()
        for quote in quotes:
            print(Selector(text=quote).xpath("//span[@class='text']/text()").extract_first())
```
`That's it.`