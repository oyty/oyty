## 如何理解`yield`关键字
﻿
为了理解什么是`yield`，你必须理解什么是生成器。在理解生成器之前，我们先来看看什么是迭代。

####可迭代对象 Iterables
当你创建了一个列表，你可以逐项地读取它，这就叫做迭代：
```
>>> mylist = [1, 2, 3]
>>> for i in mylist:
...     print i
...
1
2
3
```
`mylist`是一个迭代对象，当你使用一个列表生成式来建立一个列表的时候，就建立了一个可迭代对象：
```
>>> mylist = [x*x for x in range(3)]
>>> for i in mylist:
...     print i
...
0
1
4
```
所以你可以使用`for...in...`语法的对象都是可迭代对象：`lists, strings, files...`

这些迭代对象你用起来很方便，因为你可以随时如你所愿地读取它们，但是这些对象数据都是存在内存中的，而当你的数据量非常大的时候，用这种方式去获取数据可能并不是你想要的了。

#### 生成器 Generators
生成器是可以迭代的，但是`你只能迭代它们一次`，生成器并不把数据都放在内存中，它是实时地生成数据。
```
>>> mygenerator = (x*x for x in range(3))
>>> for i in mygenerator:
...     print i
...
0
1
4
```
这和数组生成式是一样的除了`[]`和`()`的区别，由于生成器只能使用一次，所以你不能再次执行`for i in mygenerator`，先计算出0，再计算出1，然后一个接一个...

#### Yield 关键字
`yield`是一个关键字，作用和`return`差不多，差别在`yield`返回的是一个生成器。
```
>>> def createGenerator():
...     mylist = range(3)
...     for i in mylist:
...         yield i*i
...
>>> mygenerator = createGenerator()
>>> print mygenerator
<generator object createGenerator at 0x103c539b0>
>>> for i in mygenerator:
...     print i
...
0
1
4
```
这个例子可能没什么用，但是它让你知道，这个函数会返回一大批你只需要使用一次的数据。

为了深入理解`yield`，你必须理解：当你调用这个函数的时候，函数内部的生成器的代码并不立即执行，这个函数只是返回一个生成器对象。
那么你的生成器的代码什么时候执行呢？当你使用`for...in...`进行迭代的时候。

我来看看程序的执行情况：
```
def createGenerator():
    mylist = range(3)
    print('aaaa')
    for i in mylist:
        print('bbbb')
        yield i*i

mygenerator = createGenerator()

for i in mygenerator:
    print(str(i))


aaaa
bbbb
0
bbbb
1
bbbb
4
```
第一次`for`循环的时候，函数会执行，当遇到`yield`的时候，返回第一个结果，后续的迭代会返回函数中定义的循环的下一次的`yield`结果。所以，怎么理解呢？
**`一个生成器对应的就是一个循环，每一次对生成器对象进行迭代，都是在执行这个循环`**
如果生成器内没有`yield`关键字，那么这个生成器被认为是空的。













