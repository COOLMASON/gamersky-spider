# -*- coding:utf8 -*-
import os
import sys
import re
from time import sleep
from StringIO import StringIO 

import requests
import Image

reload(sys)
sys.setdefaultencoding('utf-8')

# 注意命名规则
class GamerskySpider(object):
    def __init__(self):
        print u'开始爬取内容....'

    def get_source(self, url):
        HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}
        html = requests.get(url, headers=HEADERS)
        html.encoding = 'utf-8'
        return html.text

    def get_title(self, html):
        title = re.search(r'<h1>(.*?)</h1>', html, re.S).group(1)
        return title

    def get_allpages(self, html):
        pages_section = re.search(r'<div class="page_css">.*?<div class="sub sud"', html, re.S).group(0)
        all_links = re.findall(r'<a href="(.*?)">\d+</a>', pages_section, re.S)
        return all_links

    def get_imgs(self, html):
        # 缩小到特征范围
        imgs_section = re.search(r'<div class="Mid2L_con">.*?<div class="page_css">', html, re.S).group(0)

        # 再缩小一定的范围，这里是贪婪模式，以匹配较多的内容
        imgsrc_section = re.search(r'<p align=.*</p>', imgs_section, re.S).group(0)
        imgsrc = re.findall(r' src="(.*?)"', imgsrc_section, re.S)

        imgname = [src.split('/')[-1] for src in imgsrc]

        # imgs as dict: imgs name as keys and imgsrc as values
        imgs = dict(zip(imgname, imgsrc))

        return imgs

    def save_imgs(self, imgs):

        for imgname, imgsrc in imgs.items():
            HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}
            bin_content = requests.get(imgsrc, headers=HEADERS).content
            img = Image.open(StringIO(bin_content))
            img.save(imgname)
            print imgname + ' saved.'
            sleep(0.5)
            

if __name__ == '__main__':

    DIR = raw_input(u'输入保存图片路径：')
    #DIR = u'E:\\Python\\requests\\pic_spider'
    URL = raw_input(u'输入网址: ')

    gamersky = GamerskySpider()

    # get html source and webpage title
    html = gamersky.get_source(URL)
    title = gamersky.get_title(html)

    # create save directory named as webpage title
    SAVE_DIR = DIR + '\\' + title
    os.mkdir(SAVE_DIR)
    print u'保存目录：' + SAVE_DIR
    # set save directory as working directory
    os.chdir(SAVE_DIR)

    # get all links
    all_links = gamersky.get_allpages(html)

    # iterate through all links
    all_imgs = {}
    for link in all_links:
        print u'正在处理页面：' + link 
        html = gamersky.get_source(link)
        imgs = gamersky.get_imgs(html)
        all_imgs.update(imgs)
        sleep(0.5)

    print u'正在保存图片：'
    gamersky.save_imgs(all_imgs)
