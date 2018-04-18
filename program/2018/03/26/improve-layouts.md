
## 提升布局文件性能

###用include标签重用layout
像每个activity都会有title，我们可以定义一个xml表示标题的布局文件，然后在每个activity的布局文件中引入进来，这样就达到了标题栏的复用。

还有一个比较典型的用法是，很多activity页面刚进入的时候需要网络获取数据，这个时候比较好的体验是能有一个progressbar，等数据加载出来了，progressbar再隐藏。而这个progressbar布局也可以用include标签引入进来。

####使用merge标签
merge标签算是include标签的一种用法，我们在使用include标签的时候，会将include的布局整个引入进来，但是有一种场景，比如外面的布局是linearlayout，引入的布局的根布局也是linearlayout，这样就多了一层linearlayout，增加了布局的层数，性能优化的考虑，应该去掉引入的布局的外层linearlayout，这个时候就可以使用merge标签，merge标签在引入的时候会自动忽略掉。

###使用ViewStub按需载入视图
有些时候，我们需要一些很复杂的视图但是却很少用到。我们我们能在它需要的时候再载入，这样可以减少内存的使用并且给用户带来流畅的体验。

ViewStub是一个轻量级的view，没有占用空间，没有花费draw的资源，有没有参与到任何一个layout的计算与绘制里面。

每一个ViewStub简单的包含一个android:layout的属性来指定待创建的布局文件。
```
<ViewStub
        android:id="@+id/stub_import"
        android:inflatedId="@+id/panel_import"
        android:layout="@layout/progress_overlay"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom" />
```
当需要载入ViewStub中定义的布局时，可以使用如下方式：
```
((ViewStub) findViewById(R.id.stub_import)).setVisibility(View.VISIBLE);
 // or
 View importPanel = ((ViewStub) findViewById(R.id.stub_import)).inflate();
```
这样，ViewStub的层级就会消失，被创建出来的布局所替代，这个布局的ID就是ViewStub里面用`android:inflatedId`属性所定义的。

###invisible gone viewstub的区别
- invisible
view在layout布局中会占用位置，但是view不可见，view还是会创建对象，会被初始化，会占用资源。

- gone
view在layout布局中不占用位置，但是view还是会创建对象，会被初始化，会占用资源

- viewstub
轻量级的view，不可见，不占用资源











