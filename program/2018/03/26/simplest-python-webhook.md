
## 极简python github webhook

```
from flask import Flask
import os
import sys

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    os.system('git pull')
    return "hello world"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))

```

实现原理，github有新的代码提交的时候会触发配置的post请求，请求到服务器后，会执行git pull命令，over。

让程序后段运行
```
nohup python hook.py 11111 &
```