# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import getpass
import time
import HTMLParser
import re
import os

html_parser=HTMLParser.HTMLParser()
url="http://poj.org/"
#登陆并保存cookie
def login(id,password):
    data=urllib.urlencode({'user_id1':id,'password1':password,'B1':'login','url':'/'})
    login_url="http://poj.org/login"
    cookie=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"}
    request=urllib2.Request(login_url,data,headers)#POJ不检查headers，可以不验证
    response=urllib2.urlopen(request).read()
    #print response
    if id in response:
        return True
    else:
        return False
#传入runid取出代码
def getcode(runid):
    code_url="http://poj.org/showsource?solution_id="+runid
    code_page=urllib2.urlopen(code_url).read().decode('utf-8')
    pattern=re.compile(r'pre class="(.*?)" style=.*?>(.*?)</pre>',re.S)
    ans=re.search(pattern,code_page)
    code=ans.group(2)
    #print chardet.detect(code)
    code=html_parser.unescape(code)#格式化html标签，如标点符号等
    code_type=ans.group(1)#代码后缀
    code_type=re.sub("sh_",".",code_type)
    #print code,code_type
    return (code,code_type)
    
def gettitle(pro_id):
    pro_url="http://poj.org/problem?id="+str(pro_id)
    pro_page=urllib2.urlopen(pro_url).read().decode('utf-8')
    #访问限制
    while "Please retry after 5000ms.Thank you." in pro_page:
        time.sleep(6)
        pro_page=urllib2.urlopen(pro_url).read().decode('utf-8')
    pattern=re.compile(r'<div class="ptt".*?>(.*?)</div>',re.S)
    pro_title=re.search(pattern,pro_page).group(1)
    #print pro_title
    return pro_title

    
def run(id,password,dirpath):
    ok=login(id,password)
    if not ok:
        print "Wrong id or wrong password!"
        return False
    print "Login success!"
    os.chdir(dirpath)
    #status页面
    status_url="http://poj.org/status?problem_id=&user_id="+id+"&result=0&language="  
    while True:    
        page=urllib2.urlopen(status_url).read().decode('utf-8')
        #print page
        pattern=re.compile("<tr align=center><td>(.*?)</td><td><a.*?>.*?</a></td><td><a.*?>(.*?)</a>",re.S)
        pro=re.findall(pattern,page)
        #print pro
        if(pro==[]):
            break
        for item in pro:
            pro_id=item[1]
            #print pro_id
            run_id=item[0]
            title=gettitle(pro_id)
            code=getcode(run_id)
            pro_name=pro_id+' '+title+code[1]
            code_con=code[0].encode('utf-8')
            code_con=code_con.replace('\r\n','\n')
            print u"正在保存"+pro_name+"..."            
            f=open(pro_name,"w")
            f.write(code_con)            
            f.close()
            print u"保存"+pro_name+u"完成。"
            #time.sleep(2)
        status_url=url+re.search(r"Previous Page.*?\[<a href=(.*?)>",page).group(1)
        #print status_url
        
        
id=raw_input("Please input your User ID:")
password=getpass.getpass("Please input your password:")
dirpath=raw_input("Please input direetory:")
run(id,password,dirpath)
#run("jiajiawang","*****","E:\poj")

