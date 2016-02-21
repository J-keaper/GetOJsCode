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
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"}
url="http://acm.hdu.edu.cn"
#登陆并保存cookie
def login(id,password):
    data=urllib.urlencode({"username":id,"userpass":password,"login":"Sign In"})
    login_url="http://acm.hdu.edu.cn/userloginex.php?action=login"
    cookie=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    request=urllib2.Request(login_url,data,headers)
    response=urllib2.urlopen(request,timeout=10).read().decode("gbk")
    #print response
    if id in response:
        return True
    else:
        return False
#传入runid取出代码
def getcode(runid):
    code_url="http://acm.hdu.edu.cn/viewcode.php?rid="+runid
    request=urllib2.Request(code_url,headers=headers)
    code_page=urllib2.urlopen(request,timeout=20).read().decode('gbk')
    pattern=re.compile(r'<textarea.*?style=.*?>(.*?)</textarea>',re.S)
    code=re.search(pattern,code_page).group(1)
    code=html_parser.unescape(code)#格式化html标签，如标点符号等
    code=code.replace('\r\n','\n')
    pattern=re.compile(r"<a.*?, 'HDOJ\d{4}(.*?)'.*?>[ Save to File]",re.S) 
    code_type=re.search(pattern,code_page).group(1)
    #print code,code_type
    return (code,code_type)
    
def gettitle(pro_id):
    pro_url="http://acm.hdu.edu.cn/showproblem.php?pid="+str(pro_id)
    request=urllib2.Request(pro_url,headers=headers)
    pro_page=urllib2.urlopen(request,timeout=20).read().decode('gbk')
    #访问限制
    #while "Please retry after 5000ms.Thank you." in pro_page:
    #    time.sleep(6)
    #    pro_page=urllib2.urlopen(pro_url).read().decode('utf-8')
    pattern=re.compile(r'<tr><td.*?><h1.*?>(.*?)</h1>',re.S)
    pro_title=re.search(pattern,pro_page).group(1)
    print pro_title
    return pro_title

    
def run(id,password,dirpath):
    ok=login(id,password)
    if not ok:
        print "Wrong id or wrong password!"
        return False
    print "Login success!"
    os.chdir(dirpath)
    #status页面
    #status_url="http://acm.hdu.edu.cn/status.php?first=&pid=&user="+id+"&lang=0&status=5"  
    status_url="http://acm.hdu.edu.cn/status.php?first=13009999&user=jiajiawang&pid=&lang=&status=5#status"    
    while True:
        request=urllib2.Request(status_url,headers=headers)
        page=urllib2.urlopen(request,timeout=10).read().decode('gbk')
        #print page
        pattern=re.compile("<tr.*?align=center ><td height=22px>(.*?)</td><td>.*?</td><td>.*?<a href=.*?>(.*?)</a></td>",re.S)
        pro=re.findall(pattern,page)
        #print pro
        for item in pro:
            pro_id=item[1]
            print pro_id
            run_id=item[0]
            title=gettitle(pro_id)
            code=getcode(run_id)
            pro_name=pro_id+' '+title+code[1]
            pro_name=re.sub(r'[\/:"*?<>|]'," ",pro_name)
            print u"正在保存"+pro_name+"..."     
            f=open(pro_name,"w")
            f.write(code[0].encode('utf-8'))            
            f.close()
            print u"保存"+pro_name+u"完成。"
        status_url=re.search(r'Prev Page</a><a.*?href="(.*?)">Next Page',page)
        if(status_url==None):
            break
        status_url=url+status_url.group(1)
        print status_url
        
id=raw_input("Please input your User ID:")
password=getpass.getpass("Please input your password:")
dirpath=raw_input("Please input direetory:")
run(id,password,dirpath)
#run("jiajiawang","1407084125wang","E:\hdoj")
