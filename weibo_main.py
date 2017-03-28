#coding:utf-8
import urllib2
import urllib
import requests
import post_encode
from weibo_login import WeiboLogin
import get_weibo
import re
from lxml import html
from lxml import etree
import string
import random
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#if __name__ == '__main__':
Login = WeiboLogin('linghuwd@sina.com', 'dan5493')
if Login.login() == True:
    print "登录成功"
urls_1,names_1=get_weibo.get_url()
length=len(urls_1)
for i in range(length):
    urls=[]
    names_2=re.sub('\\\\n','',names_1[i])
    names_3=re.sub('   ','',names_2)
    new_path = get_weibo.path(names_3.decode('unicode_escape'))
    url_1=re.sub('\\\\','',urls_1[i])
    url_2='http://s.weibo.com'+url_1
    url_3=re.sub('Refer=top','page=1.html',url_2)    #每一话题的第一页
    print url_3 
    sleeptime_rand=random.randint(3,10)
    time.sleep(sleeptime_rand)
    urls.append(url_3)     
    page=get_weibo.get_page(url_3)
    length_2=len(page)
    for j in xrange(2,length_2):
        url_4=re.sub('1.html','',url_3)
        url_5=url_4 + str(j) + '.html'
        print url_5
        urls.append(url_5)
    for url in urls:
        html=get_weibo.decode_html(url)    
        number_info=get_weibo.get_number_info(html)
        print len(number_info)
        (nick_name,nickname_href,content_text,times)=get_weibo.get_details(html)
        get_weibo.write_all_info(new_path,nick_name,nickname_href,content_text,times,number_info)
        sleeptime_rand=random.randint(15,40)
        print sleeptime_rand
        time.sleep(sleeptime_rand)

