# -*- coding:utf-8 -*-
# 第一个GitHub项目
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

    # 没有参数初始化对象，这样创建对象后就可以单独调用成员函数
    def __init__(self):
        pass

    # 设置网页地址和保存目录
    def initialize(self, URL, DIR=u'C:'):
        
        self.URL = URL
        self.DIR = DIR

        print u'开始爬取内容....'

        self.HTML = self.get_source(self.URL)
        self.TITLE= self.get_title(self.HTML)
        print u'网页主题：' + self.TITLE

        self.SAVE_DIR = self.DIR + '\\' + self.TITLE
        os.mkdir(self.SAVE_DIR)
        os.chdir(self.SAVE_DIR)
        print u'保存目录：' + self.SAVE_DIR

        self.all_links = self.get_allpages(self.HTML)
        self.all_imgs = {}
        for link in self.all_links:
            print u'正在处理页面：' + link 
            html = self.get_source(link)
            imgs = self.get_imgs(html)
            self.all_imgs.update(imgs)
            sleep(0.5)


    # 获取网页html文本
    def get_source(self, url):
        HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}
        html = requests.get(url, headers=HEADERS)
        html.encoding = 'utf-8'
        return html.text


    # 获取网页title（主题）
    def get_title(self, html):
        title = re.search(r'<h1>(.*?)</h1>', html, re.S).group(1)
        return title

    # 获取游民星空某个话题下所有相关页面的地址
    def get_allpages(self, html):
        pages_section = re.search(r'<div class="page_css">.*?<div class="sub sud"', html, re.S).group(0)
        all_links = re.findall(r'<a href="(.*?)">\d+</a>', pages_section, re.S)
        return all_links

    # 获取某一个地址下话题相关图片的图片名称和图片地址，返回由名称和地址组成的字典数据
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

        print u'正在保存图片：'
        for imgname, imgsrc in imgs.items():
            HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}
            bin_content = requests.get(imgsrc, headers=HEADERS).content
            img = Image.open(StringIO(bin_content))
            img.save(imgname)
            print imgname + ' saved.'
            sleep(0.5)
            