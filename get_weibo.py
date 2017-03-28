#coding:utf-8
import requests
import urllib
import urllib2
import re
import os
import time
import random
import json
from bs4 import BeautifulSoup
from lxml import html
from lxml import etree
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#get_html()函数用于获取所爬取的页面的html源码

def decode_html(original_html):
    html=urllib2.urlopen(original_html).read()
	#将获取到的html源码分行，因为新浪微博将网页进行了压缩
    lines = html.splitlines()
    for line in lines:
        if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct","js":["apps'):
            n = line.find('"html":"')
            if n > 0:
                decoded_html = line[n + 8: ].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\", "")
    return decoded_html

def get_url():
    url_list=['realtimehot','total&key=friends','total&key=all','total&key=films','total&key=person']
    for cate in url_list:
        url='http://s.weibo.com/top/summary?cate=%s' % cate
        request=urllib2.Request(url)
        response=urllib2.urlopen(request)
        page=response.read().decode('utf-8')
        tree=etree.HTML(page)
        summary_xpath='//script/text()'
        summary=tree.xpath(summary_xpath)
        for script in summary:
            script_1=re.findall(r'"html":"(.+?)"}',script)
            for script_2 in script_1:
                script_3=re.sub('\\\\"','"',script_2)
                try:
                    tree_2=html.fromstring(script_3)
                except Exception,e:
                    continue
                else:
                    name_xpath='//div[@class="rank_content"]/p[@class="star_name"]/a/text()'
                    names=tree_2.xpath(name_xpath)
                    url_text='//div[@class="rank_content"]/p[@class="star_name"]/a/@href'
                    urls=tree_2.xpath(url_text)
        return urls,names

def get_page(first_page_url):
    request=urllib2.Request(first_page_url)
    response=urllib2.urlopen(request)
    htmlcode=response.read().decode('utf-8')
    #print page    可以read出全部源代码的 
    pages=re.findall(r'\u7b2c(.+?)\u9875',htmlcode)
    weibo_pages=[]
    for i in pages:
        weibo_page=re.sub('\\\\','',i)
        weibo_pages.append(weibo_page)
    return weibo_pages

def get_urls():
    urls=[]
    urls_1,names_1=get_url()
    for i in range(len(urls_1)):
        names_2=re.sub('\\\\n','',names_1[i])
        #new_path = path(names_2.decode('unicode_escape'))
        url_1=re.sub('\\\\','',urls_1[i])
        url_2='http://s.weibo.com'+url_1
        url_3=re.sub('Refer=top','page=1.html',url_2)    #每一话题的第一页
        print url_3 
        sleeptime_rand=random.randint(3,10)
        time.sleep(sleeptime_rand)
        urls.append(url_3)     
        page=get_page(url_3)
        for j in xrange(2,len(page)):
            url_4=re.sub('1.html','',url_3)
            url_5=url_4 + str(j) + '.html'
            urls.append(url_5)
            print url_5
    return urls
   
def get_details(html):
    soup=BeautifulSoup(html)
    
    div_content = soup.find_all(attrs={'class': 'content clearfix'})
    div_time=soup.find_all(attrs={'class':'feed_from W_textb'})
    nick_name=[]
    nickname_href=[]
    content_text=[]
    time=[]
    
    for i in range(len(div_content)):
        a_tag=div_content[i].find('a')
        nick_name.append(a_tag.get('nick-name'))
        nickname_href.append(a_tag.get('href'))
        p_tag=div_content[i].find('p')
        content_text.append(p_tag.get_text()) 
    for j in range(len(div_time)): 
        a_time=div_time[j].find('a')
        time.append(a_time.get('title'))
    return (nick_name,nickname_href,content_text,time)

def get_number_info(html):
    soup=BeautifulSoup(html)
    get=soup.find_all(attrs={'class': 'feed_action_info feed_action_row4'})
    get_number_info=[]
    for i in range(len(get)):
        forward=get[i].find(attrs={'action-type':'feed_list_forward'})
        forward_em=forward.find_all('em')

        if (len(forward_em[0].get_text())==0):
            temp_forward="0"
            get_number_info.append(temp_forward)
        else:
            temp_forward=forward_em[0].get_text()
            get_number_info.append(temp_forward)

        comment=get[i].find(attrs={'action-type':'feed_list_comment'})
        if bool(comment.find_all('em')):
            comment_em=comment.find_all('em')
            temp_comment=comment_em[0].get_text()
            get_number_info.append(temp_comment)
        else:
            temp_comment="0"
            get_number_info.append(temp_comment)

        like=get[i].find(attrs={'action-type':'feed_list_like'})
        if like==None:
            continue
        like_em=like.find_all('em')
        if (len(like_em[0].get_text())==0):
            temp_like="0"
            get_number_info.append(temp_like)
        else:
            temp_like=like_em[0].get_text()
            get_number_info.append(temp_like)
    return get_number_info

def path(name):
    path='F:/微博/%s/' % name
    isExits = os.path.exists(path)  
    if not isExits:
        os.makedirs(path)  
    else:  
        pass
    return path        

def write_all_info(basic_path,nick_name,nickname_href,content_text,times,number_info):
    nick_name_list=nick_name
    nickname_href_list=nick_name
    content_text_list=content_text
    time_list=times
    number_info_list=number_info
    temp=0
    for i in range(len(nick_name)):
        try:
            write_all_list=open(basic_path+nick_name[i]+".txt",'w+')
            #write_all_list.writelines("微博用户名称："+nick_name_list[i]+"\n")
            #write_all_list.writelines("微博链接："+nickname_href[i]+"\n")
            #write_all_list.writelines("正文："+content_text_list[i]+"\n")
            #write_all_list.writelines("发微博时间："+time_list[i]+"\n")
            content_text_list[i]=re.sub(r'#(.*?)#','',content_text_list[i])
            content_text_list[i]=re.sub(r'#','',content_text_list[i]).strip()
            write_all_list.writelines(content_text_list[i]+"\n")
            #j=0
            #while (j!=3):
                #write_all_list.writelines("==="+number_info_list[temp]+"==="+"\n")
                #j+=1
                #temp+=1
            write_all_list.close()
        except Exception as e:
            pass













































