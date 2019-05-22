import requests
import re
import os
from hashlib import md5
from requests.exceptions import RequestException


def get_page(url):#请求并获取豆瓣250的源码
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_parse(html):#进行解析
    parse = re.compile('<li.*?div.*?"item".*?<a.*?img.*?src="(.*?)"'
                       '.*?div.*?"info".*?span.*?"title">(.*?)</span>'
                       '.*?div.*?"bd".*?p.*?>(.*?)<br>', re.S)
    parse_over = re.findall(parse, html)
    for item in parse_over:
        yield {
            "jpg": item[0].strip(),
            "title": item[1].strip(),
            "director": item[2].strip()
        }


def down_photo(photos_url):#下载图片
    if not os.path.exists('photo'):#查看当前路径下是否有这个文件
        os.mkdir('photo')#创建文件夹
    for photo_url in photos_url:
        try:
            photo = requests.get(photo_url)
            if photo.status_code == 200:
                name = 'photo' + os.path.sep + md5(photo.content).hexdigest() + '.jpg'
                with open(name, 'wb+') as f:
                    f.write(photo.content)
        except Exception:
            return None


if __name__ == '__main__':
    for num in range(0, 250, 25):
        photos_url = []
        url = "https://movie.douban.com/top250?start=" + str(num)
        html = get_page(url)
        items = get_parse(html)
        for item in items:
            photos_url.append(item["jpg"])
            print(item)
        down_photo(photos_url)