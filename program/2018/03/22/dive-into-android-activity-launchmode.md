
## 深入理解Android中Activity的launchMode

合理地设计Activity对象是否使用已有的实例还是多次创建，会使得交互设计更加良好，也能避免很多问题。

####standard
launchMode的默认值，**每当有一次Intent请求，就会创建一个新的Activity实例**
分两种情况，当在同一程序内部启动一个新的Activity时，新生成的实例会放入发送Intent的Task的栈的顶部，很正常的情况。
<center>
![](/images/lm_1.png)
</center>
但是在跨程序之间调用的时候，在5.0前后会有所不同。
5.0之前，跨应用之间调用，新生成的实例会放在发送Intent的Task的栈的顶部，和同一程序内部启动新Activity相同。
<center>
![](/images/lm_2.png)
</center>
这种情况怪怪的，如果你打开任务管理器，你会发现显示的是发送Intent的程序，展示的却是跳转后的程序的实例。
<center>
![](/images/lm_3.png)
</center>
5.0之后改进了这个表现，跨应用之间启动Activity，会创建一个新的Task，新生成的Activity会被放入新创建的Task中：
<center>
![](/images/lm_4.png)
</center>
这个时候任务管理器的显示就比较合理了：
<center>
![](/images/lm_5.png)
</center>

####singleTop
singleTop和standard基本是一样的，也会创建多个实例，唯一的不同就是，如果调用的目标已经位于调用着的栈顶，则不创建实例，而是使用当前这个Activity实例，并调用这个实例的onNewIntent方法。

singleTop的一个典型应用场景就是搜索了，如果一个搜索框，搜索后跳转到SearchActivity页面，为了更好的体验，SearchActivity页面顶部也会放一个搜索框，这样就可以重复搜索下去，因为是singleTop的启动模式，所以在你搜索了多次后，点击返回按钮，可以直接返回到之前的页面。

####singleTask
这个和前面的就很不同了，**使用singleTask启动模式的Activity在系统中只会存在一个实例**，如果这个实例已经存在，intent就会通过onNewIntent传递到这个Activity，否则新的实例就会被创建。
#####同一程序内
如果系统中不存在singleTask Activity的实例，那就创建这个实例，并将这个实例放入和调用者相同的Task中并位于栈顶。
<center>
![](/images/lm_6.png)
</center>
如果singleTask Activity已经存在，那么在Activity会退栈中，所有位于该Activity上面的Activity实例都会被销毁掉（销毁的时候生命周期方法会被调用），这样singleTask的实例就会位于栈顶，intent会通过onNewIntent传递到这个singleTask实例。
<center>
![](/images/lm_7.png)
</center>
如果要让singleTask的实例放在一个新的task中，可以添加taskAffinity属性，配置如下：
```
<activity 
    android:name=".SingleTaskActivity" 
    android:label="singleTask launchMode" 
    android:launchMode="singleTask" 
    android:taskAffinity=""> 
</activity>
```
这个时候的效果：
<center>
![](/images/lm_8.png)
</center>
#####跨应用之间（忽略）
####singleInstance
这个模式和singleTask差不多，他们在系统中都只有一份实例，唯一不同的是存放singleInstance实例的Task只能存放一个该模式的Activity实例。如果从singleInstance实例启动另一个Activity，则新的实例会被放入其它task中。同样的，如果singleInstance被别的Activity启动，它也会被放入不同于调用者的task中。

但是这个地方有点不一样，虽然是两个task，但是在任务管理器中却只有一个位于栈顶的task，而且当我们从任务管理器中进入这个task后，无法返回到之前的task。当然这个问题有一个解决方案：
```
<activity 
    android:name=".SingleInstanceActivity" 
    android:label="singleInstance launchMode" 
    android:launchMode="singleInstance" 
    android:taskAffinity=""> 
</activity>
```
这个模式使用情况比较罕见，在Launcher中可能会使用。

####Intent Flags
除了在manifest中设置启动模式外，也可以在Intent中设置flag。下面代码就可以让StandardActivity以singleTop模式启动：
```
Intent intent = new Intent(StandardActivity.this, StandardActivity.class);
intent.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP); 
startActivity(intent);
```








