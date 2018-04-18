__author__ = 'oyty'

from os.path import join, dirname, basename as filename, splitext
import os
from urllib.request import pathname2url

root_dir = dirname(__file__)
post_dir = join(root_dir, "post")

website_dir = "/Users/oyty/Documents/GitHub/oyty.github.io"


def all_post_file():
    post_basedir = join(root_dir, "post")
    postlist = []
    for root, dirs, files in os.walk(post_basedir):
        for f_name in files:
            # 设置忽略格式
            if f_name.startswith(".") or f_name.endswith(("pdf",)): continue
            post_path = join(root, f_name)
            print(post_path)
            c_time = os.stat(post_path).st_ctime
            postlist.append((post_path, c_time))
    return sorted(postlist, key=lambda x: x[1], reverse=True)


print(all_post_file())
print(root_dir)
for (post_path, _) in all_post_file():
    print(post_path)
    destfile = join(dirname(post_path.replace(root_dir, website_dir)),
                    splitext(filename(post_path))[0] + ".html")
    print(destfile)
    url = pathname2url(destfile.split(website_dir)[1])
    print(url)
    print(dirname(destfile))

