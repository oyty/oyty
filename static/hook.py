from flask import Flask
import os
import sys

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hook():
    os.system('git pull')
    return 'hello world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
