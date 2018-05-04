
##[Scrapy-4] XPath教程

﻿XPath是一门在XML文档中查找信息的语言，XPath可用来在XML文档中对元素和属性进行遍历。

#### 如果路径以/开头，该路径表示到一个元素的绝对路径
```xml
<AAA>
    <BBB/>
    <CCC/>
    <BBB/>
    <BBB/>
    <DDD>
        <BBB/>
    </DDD>
    <CCC/>
</AAA>
```
选择根元素AAA：`/AAA`

选择AAA的所有CCC子元素：`/AAA/CCC`

选择AAA的子元素DDD的所有BBB元素：`/AAA/DDD/BBB`

####如果路径以//开头，表示选择文档中所有满足双斜线//之后规则的元素（无论层级关系）
```xml
<AAA>
    <BBB/>
    <CCC/>
    <BBB/>
    <DDD>
        <BBB/>
    </DDD>
    <CCC>
        <DDD>
            <BBB/>
            <BBB/>
        </DDD>
    </CCC>
</AAA>
```
选择所有BBB元素：`//BBB`

选择所有父元素是DDD的BBB元素：`//DDD/BBB`

####星号*表示选择所有由星号之前的路径所定位的元素
```xml
<AAA>
    <XXX>
        <DDD>
            <BBB/>
            <BBB/>
            <EEE/>
            <FFF/>
        </DDD>
    </XXX>
    <CCC>
        <DDD>
            <BBB/>
            <BBB/>
            <EEE/>
            <FFF/>
        </DDD>
    </CCC>
    <CCC>
        <BBB>
            <BBB>
                <BBB/>
            </BBB>
        </BBB>
    </CCC>
</AAA>
```
选择所有路径依附于/AAA/CCC/DDD的元素：`/AAA/CCC/DDD/*`

选择所有有3个祖先元素的BBB元素：`/*/*/*/BBB`

选择所有元素：`//*`

####方括号里的表达式可以进一步指定元素，其中数字表示元素在选择集里的位置，而last()函数表示选择集中的最后一个元素
```xml
<AAA>
    <BBB/>
    <BBB/>
    <BBB/>
    <BBB/>
</AAA>
```
选择AAA的第一个BBB元素：`/AAA/BBB[1]`

选择AAA的最后一个BBB元素：`/AAA/BBB[last()]`

####属性通过前缀@来指定
```xml
<AAA>
    <BBB id="b1"/>
    <BBB id="b2"/>
    <BBB name="bbb"/>
    <BBB/>
</AAA>
```
选择所有的id属性：`//@id`

选择有id属性的BBB元素：`//BBB[@id]`

选择有name属性的BBB元素：`//BBB[@name]`

选择有任意属性的BBB元素：`//BBB[@*]`

选择没有属性的BBB元素：`//BBB[not(@*)]`

####属性的值可以被用来做为选择的准则
**normalize-space函数删除了前部和尾部的空格，并且把连续的空格串替换为一个单一的空格**
```xml
<AAA>
    <BBB id="b1"/>
    <BBB name=" bbb "/>
    <BBB name="bbb"/>
</AAA>
```
选择含有属性id且其值为“b1”的元素：`//BBB[@id='b1']`

选择含有属性name且其值为“bbb”的BBB元素：`//BBB[@name='bbb']`

选择含有属性name且其值（在用normalize-space函数去掉前后空格后）为“bbb”的BBB元素：`//BBB[normalize-space(@name)='bbb']`

####count()函数可以计数所选元素的个数
```xml
<AAA>
    <CCC>
        <BBB/>
        <BBB/>
        <BBB/>
    </CCC>
    <DDD>
        <BBB/>
        <BBB/>
    </DDD>
    <EEE>
        <CCC/>
        <DDD/>
    </EEE>
</AAA>
```
选择含有两个BBB子元素的元素：`//*[count(BBB)=2]`

选择含有两个子元素的元素：`//*[count(*)=2]`

选择含有3哥子元素的元素：`//*[count(*)=3]`

####name()函数返回元素的名称，start-with()函数在该函数的第一个参数字符串是以第二个参数字符开始的情况返回true，contains()函数当其第一个字符串参数包含有第二个字符串参数时返回true
```xml
<AAA>
    <BCC>
        <BBB/>
        <BBB/>
        <BBB/>
    </BCC>
    <DDB>
        <BBB/>
        <BBB/>
    </DDB>
    <BEC>
        <CCC/>
        <DBD/>
    </BEC>
</AAA>
```
选择所有名称为BBB的元素（这里等价于//BBB）：`//*[name()='BBB']`

选择所有名称以“B”起始的元素：`//*[start-with(name(), 'B')]`

选择所有名称包含“C”的元素：`//*[contains(name(), 'C')]`

####string-length函数返回字符串的字符数
```xml
<AAA>
    <Q/>
    <SSSS/>
    <BB/>
    <CCC/>
    <DDDDDDDD/>
    <EEEE/>
</AAA>
```
选择名字长度为3的元素：`//*[string-length(name()) = 3]`

选择名字长度小于3的元素：`//*[string-length(name()) < 3]`

选择名字长度大于3的元素：`//*[string-length(name()) > 3]`

####多个路径可以用分隔符|合并在一起
```xml
<AAA>
    <BBB/>
    <CCC/>
    <DDD>
        <CCC/>
    </DDD>
    <EEE/>
</AAA>
```
选择所有的CCC和BBB元素：`//CCC | //BBB`

选择所有的BBB元素和所有的AAA的子元素的EEE元素：`/AAA/EEE | //BBB`

*可以合并的路径数目没有限制*

####descendant（后代）轴包含上下文节点的后代，一个后代指子节点或者子节点的子节点等等，因此descendant轴不会包含属性和命名空间节点
选择文档根元素的所有后代，即所有的元素被选择：`/descendant::*`

选择/AAA/BBB的所有后代元素：`/AAA/BBB/descendant::*`

选择在祖先元素中有CCC的所有元素：`//CCC/descendant::*`

选择所有以CCC为祖先元素的DDD元素：`//CCC/descendant::DDD`

####parent轴包含上下文节点的父节点，如果有父节点的话
选择DDD元素的所有父节点：`//DDD/parent::*`

####ancestor轴包含上下节点的祖先节点，该祖先节点由其上下文节点的父节点以及父节点的父节点等等诸如此类的节点构成，所以ancestor的轴总是包含有根节点，除非上下文节点就是根节点本身
选择一个绝对路径上的所有节点：`/AAA/BBB/DDD/CCC/EEE/ancestor::*`
<center>
![](/images/xpath-ancestor1.png)
</center>

选择FFF元素的祖先节点：`//FFF/ancestor::*`
<center>
![](/images/xpath-ancestor2.png)
</center>

####后面倒是还有一些，不过上面的足够用了













