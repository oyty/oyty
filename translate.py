# coding=utf-8
__author__ = 'oyty'


# !/usr/bin/env python

import os
import re
import shutil
from os.path import join, dirname, basename as filename, splitext
from urllib.request import pathname2url

import markdown2
from jinja2 import PackageLoader, Environment


class Post(object):
    def __init__(self, from_file):
        if not os.path.isfile(from_file): raise RuntimeError("not a file")
        self.fromfile = from_file
        post_dir = join(website_dir, from_file)
        self.destfile = join(dirname(post_dir),
                             splitext(filename(self.fromfile))[0] + ".html")
        self.url = pathname2url(self.destfile.split(website_dir)[1])
        # print(self.destfile)
        # print(self.url)
        self._html = None
        self._title = None

    @property
    def html(self):
        if not self._html:
            with open(self.fromfile) as f:
                self._html = markdown2.markdown(f.read(),
                                                extras=['fenced-code-blocks', 'footnotes'])
                c = re.compile("<p>(\\n)+</p>")
                self._html = re.sub(c, '</br>', self._html)

                # print(self._html)
        return self._html

    @property
    def title(self):
        if not self._title:
            title = re.findall("<h2>(.*?)</h2>", self.html)
            self._title = title[0] if title else filename(self.destfile).rsplit(".")[0]
        return self._title

    def write(self):
        if not os.path.exists(dirname(self.destfile)):
            os.makedirs(dirname(self.destfile))
        with open(self.destfile, "w", encoding="utf-8", errors="xmlcharrefreplace") as fd:
            html = jinja_env.get_template("post.html").render(title=self.title, content=self.html, mottos=generate_mottos())
            # print(html)
            fd.write(html)


def generate_mottos():
    mottos_r = open(join(website_dir, "sources/motto.txt"), "r")
    mottos = []
    for motto in mottos_r:
        mottos.append(motto)
    return mottos


def all_post_file():
    post_basedir = join(root_dir, "post")
    postlist = []
    for root, dirs, files in os.walk(post_basedir):
        for f_name in files:
            # 设置忽略格式
            if f_name.startswith(".") or f_name.endswith(("pdf",)): continue
            post_path = join(root, f_name)
            # print(post_path)
            c_time = os.stat(post_path).st_ctime_ns
            postlist.append((post_path, c_time))
    return sorted(postlist, key=lambda x: x[1], reverse=False)
    # return sopostlist


def all_program_file():
    program_basedir = join(root_dir, "program")
    program_list = []
    for root, dirs, files in os.walk(program_basedir):
        for f_name in files:
            # 设置忽略格式
            if f_name.startswith(".") or f_name.endswith(("pdf",)): continue
            post_path = join(root, f_name)
            # print(post_path)
            c_time = os.stat(post_path).st_ctime_ns
            program_list.append((post_path, c_time))
    return sorted(program_list, key=lambda x: x[1], reverse=True)
    # return program_list


def all_trade_file():
    trade_basedir = join(root_dir, "trade")
    trade_list = []
    for root, dirs, files in os.walk(trade_basedir):
        for f_name in files:
            # 设置忽略格式
            if f_name.startswith(".") or f_name.endswith(("pdf",)): continue
            post_path = join(root, f_name)
            c_time = os.stat(post_path).st_ctime_ns
            trade_list.append((post_path, c_time))
    return sorted(trade_list, key=lambda x: x[1], reverse=True)
    # return trade_list


def cover_all_post():
    """create posts html format and make up index.html"""
    postlist = []
    for (post_path, _) in all_post_file():
        # print('post_path--' + post_path)
        p = Post(post_path)
        p.write()
        print(p.title, p.url)
        postlist.append(p)
    index_t = jinja_env.get_template("index.html")
    with open(join(website_dir, "index.html"), "w") as fd:
        fd.write(index_t.render(postlist=postlist, mottos=generate_mottos()))


def cover_all_program():
    """create program html format and make up program-think.html"""
    program_list = []
    for (post_path, _) in all_program_file():
        # print('post_path--' + post_path)
        p = Post(post_path)
        p.write()
        print(p.title, p.url)
        program_list.append(p)
    index_t = jinja_env.get_template("program-think.html")
    with open(join(website_dir, "program-think.html"), "w") as fd:
        fd.write(index_t.render(postlist=program_list, mottos=generate_mottos()))


def cover_all_trade():
    """create trade html format and make up trade-think.html"""
    trade_list = []
    for (post_path, _) in all_trade_file():
        # print('post_path--' + post_path)
        p = Post(post_path)
        p.write()
        print(p.title, p.url)
        trade_list.append(p)
    index_t = jinja_env.get_template("trade-think.html")
    with open(join(website_dir, "trade-think.html"), "w") as fd:
        fd.write(index_t.render(postlist=trade_list, mottos=generate_mottos()))


def copy_all_static():
    """拷贝 static/* 到 设置的website文件夹下"""
    base_websit = join(root_dir, "static")
    for root, dirs, files in os.walk(base_websit):
        relative_path = root.split(base_websit)[1].strip("/")
        for filename in files:
            if not os.path.exists(join(website_dir, relative_path)):
                os.makedirs(join(website_dir, relative_path))
            shutil.copy(join(root, filename),
                        join(website_dir, relative_path, filename))


def push_to_github():
    os.system("""cd %s && git add * && git commit -m "update" && git push origin master""" % website_dir)


def develop():
    """部署到github"""
    copy_all_static()
    cover_all_post()
    cover_all_program()
    cover_all_trade()
    push_to_github()


root_dir = dirname(__file__)
jinja_env = Environment(loader=PackageLoader(__name__))

# 文件输出地址,确定已经git init,可以直接git push origin master
website_dir = "/Users/oyty/Documents/GitHub/oyty.github.io"

# 博客名字
jinja_env.globals["title"] = "游戏人生"
jinja_env.globals["program_title"] = "程序人生"
jinja_env.globals["trade_title"] = "Trade Life"

# 博客图标
jinja_env.globals["icon"] = "logo.bmp"

# 直接添加名字和地址
jinja_env.globals["sociallist"] = (("github", "https://github.com/oyty"),)

if __name__ == "__main__":
    develop()
