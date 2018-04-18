
##Java中的字符串拼接

在Java中，String对象是不可变的（Immutable）。你可以创建多个某一个String对象的别名，但是这些别名的引用是相同的。

####深入剖析字符串拼接
既然字符串是不可变的，那么当多个字符串拼接时，很自然的就会以为拼接过程中会产生多余的字符串对象。
```
String a = "aaa";
String b = "bbb";
String c = "ccc";
String info = a + b + c;
```
自然会以为上面字符串拼接过程中会产生多余的字符串对象`aaabbb`，如果拼接的字符串数量足够多的话，那岂不是会产生很多多余的字符串对象，这样不就严重影响性能了吗？

然而事实并非如此。
####编译器的优化处理
事实上，在Java代码被编译为字节码的时候，jvm会对字符串拼接进行优化处理，会先生成一个StringBuilder，然后后面的拼接就直接调用StringBuilder的append方法。

这样看来，既然编译器做了优化处理，好像我们有没有必要再关注字符串拼接了，然后事实并非如此。
我们来看一种情况
```
public void implicitUseStringBuilder(String[] values) { 
    String result = ""; 
    for (int i = 0 ; i < values.length; i ++) { 
        result += values[i]; 
    } 
    System.out.println(result); 
}
```
在循环里面，字符串有拼接，这个时候jvm也会创建一个StringBuilder，但是循环流程走完后，进入下一个流程的时候又会新创建一个StringBuilder，这样就会创建大量多余的StringBuilder对象，影响性能，所以啊，还是要有好的编码习惯：
```
public void explicitUseStringBuider(String[] values) { 
    StringBuilder result = new StringBuilder(); 
    for (int i = 0; i < values.length; i ++) { 
        result.append(values[i]); 
    } 
}
```
