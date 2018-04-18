
## Android性能调优之容器扩容

﻿Java和Android提供了很多容器来组织对象，比如ArrayList，HashMap等，这些容器用起来虽然方便，但是也存在一些问题，也就是它们会自动扩容。这个扩容不是简单的创建一个新的对象，而且创建一个更大的容器对象，这也就意味着要占用更大的内存空间。

从源码角度来看看它们是如何扩容的：
```
public boolean add(E e) {
    ensureCapacityInternal(size + 1);  // Increments modCount!!
    elementData[size++] = e;
    return true;
}
```
添加新的数据对象的时候，会先检测容量
```
private void ensureCapacityInternal(int minCapacity) {
    if (elementData == EMPTY_ELEMENTDATA) {
        minCapacity = Math.max(DEFAULT_CAPACITY, minCapacity);
    }

    ensureExplicitCapacity(minCapacity);
}
private void ensureExplicitCapacity(int minCapacity) {
    modCount++;

    // overflow-conscious code
    if (minCapacity - elementData.length > 0)
        grow(minCapacity);
}

```
你可以自定义最小容量，有一个默认的最小容量
```
private static final int DEFAULT_CAPACITY = 10;
```
如果容量不够，就需要扩容了grow
```
private void grow(int minCapacity) {
    // overflow-conscious code
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + (oldCapacity >> 1);
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    // minCapacity is usually close to size, so this is a win:
    elementData = Arrays.copyOf(elementData, newCapacity);
}

private static int hugeCapacity(int minCapacity) {
    if (minCapacity < 0) // overflow
        throw new OutOfMemoryError();
    return (minCapacity > MAX_ARRAY_SIZE) ?
        Integer.MAX_VALUE :
        MAX_ARRAY_SIZE;
}
```
扩容会右移一位（也就是除以2，左移一位是乘以2，我们知道位移运算要快于除法运算），也就是容量增加到原来的1.5倍。
最后使用`Arrays.copyOf()`创建新的数组，然后将原来的数组拷贝到新的数组里面，而这个是很耗费性能的，所以在使用ArrayList的时候，最好能提前知道数组的容量，然后直接确定，这样就可以避免数组自动扩容带来的性能和时间消耗。

HashMap原理和ArrayList差不多，也是创建容量对象，自动扩容，默认容量如下：
```
/**
 * The default initial capacity - MUST be a power of two.
 */
static final int DEFAULT_INITIAL_CAPACITY = 4;

```


