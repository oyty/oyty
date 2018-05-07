##Android Studio点击Run按钮的实际操作

<h4>检查项目和读取基本配置</h4>

#### Gradle Build

gradle编译的形式和你的配置有关：
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
上面配置了release和debug形式的编译，按钮点击后的最终执行的是debug还是release在Android Studio左下角的Build Variants中：

一般执行运行安装默认为debug。

####Apk install & LaunchActivity