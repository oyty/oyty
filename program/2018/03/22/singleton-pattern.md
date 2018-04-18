
## 单例模式

####饿汉式
直接进行创建

####懒汉式
第一次使用时进行创建，使用synchronized修饰，避免对象不唯一

####双重检查加锁
```
public class SingleInstance {
    private static volatile SingleInstance sInstance;

    private SingleInstance() {
    }

    public static SingleInstance getInstance() {
        if (null == sInstance) {
            synchronized (SingleInstance.class) {
                if (null == sInstance) {
                    sInstance = new SingleInstance();
                }
            }
        }
        return sInstance;
    }
}

```
####利用static机制，极客型的单例
```
public class SingleInstance {
        private SingleInstance() {
        }
        public static SingleInstance getInstance() {
            return SingleInstanceHolder.sInstance;
        }
        private static class SingleInstanceHolder {
            private static SingleInstance sInstance = new SingleInstance();
        }
    }
```

####真的只有一个单例吗？
- 使用反射，虽然构造器是非公开的，但是在反射面前就不起作用了
- 使用多个类加载器加载单例类，也会导致创建多个实例并存的问题



