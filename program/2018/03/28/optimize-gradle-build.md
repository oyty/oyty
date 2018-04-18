
## 加速gradle构建

###开启Daemon
Gradle Daemon是一个长期生存（3小时不被调用就会自动结束）能够提升编译速度的后台进程。它的优化原理如下：
- 由于gradle是运行在JVM之上的，并且有较多的依赖库，长期运行在后台能够节省每次编译需要重新初始化的时间。
- 通过运行时代码优化来提升编译性能，这种优化是循序渐进的，随着编译次数的增多，优化效果会越来越好，一般在5-10次编译后，优化效果趋于稳定。
- Gradle Daemon通过编译缓存提高效率。如gradle能缓存一些编译时的输入和输出，支持增量编译。
在gradle配置文件中配置如下：
```
# 为了保证每次编译的独立性，在持续集成中，不建议开启daemon
org.gradle.daemon=true
```

###Configuration on demand
gradle编译的三个阶段：
+ 初始化，gradle支持单个或多个项目同时编译，在初始化阶段，gradle决定哪些项目参与编译，并为每一个项目创建一个project实例。
+ 配置阶段，对所有项目进行配置，会执行项目里面的build.gradle文件，下载相关的插件和依赖等，决定需要执行那些任务的集合。
+ 执行阶段，执行在配置阶段确定的所有task。
按需配置（configuration on demand）只对任务相关的项目进行配置，在大型多项目编译过程中非常有用，能够大幅度减少不必要的配置时间。
```
org.gradle.configureondemand=true
```
###设置内存大小
根据自身设备进行配置：
```
org.gradle.jvmargs=-Xmx5120m -XX:MaxPermSize=2048m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```
为gradle分配最大5G内存。

###debug构建关闭proguard
proguard除了代码混淆外，还可以进行代码压缩，优化和验证，代码优化会占用很多的时间，比如一个开启了代码优化的配置如下：
```
-optimizationpasses 5
```
这就意味着代码优化会经过5次，即上一次的优化输出结果作为下一次优化的输出。
可以在gradle配置debug编译方式时禁用proguard。
```
buildTypes {
        release {
            buildConfigField("boolean", "DEBUGABLE", "false")
            buildConfigField("int", "SERVER_TYPE", "${rootProject.ext.serverEnvCode}")
            minifyEnabled true
            zipAlignEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.release
        }
        debug {
            buildConfigField("boolean", "DEBUGABLE", "true")
            buildConfigField("int", "SERVER_TYPE", "${rootProject.ext.serverEnvCode}")
            versionNameSuffix "-debug"
            minifyEnabled false
            zipAlignEnabled true
            shrinkResources false
//            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.release
        }
    }
```
直接点选运行按钮可以选择编译方式，具体参考-----

###模块化项目和并行编译
并行执行在多项目编译的项目中能有效提升编译的速度，但是并行的前提是每个项目已经被模块化，每个项目之间没有耦合，这个功能目前还在孵化中。。。
开启parallel
```
# When configured, Gradle will run in incubating parallel mode.
# This option should only be used with decoupled projects. More details, visit
# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects
org.gradle.parallel=true

```

###开启offline
开启offline后，可以强制gradle使用本地缓存的依赖，避免了网络读写操作和网络检查依赖。
如果某个依赖不存在的时候，编译会出错，这样只需要暂时关闭offline，等依赖下载下来后，再打开就可以了。
<center>
![](/images/gradle-1.png)
</center>