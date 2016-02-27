# -*- coding: utf-8 -*-

import requests
import re
import HTMLParser
import getpass
import os
import msvcrt

html_parser=HTMLParser.HTMLParser()
s=requests.session()
#cookies = dict(cookies_are='working')
host="http://acm.hdu.edu.cn"
def login(id,password):
    data = {
            'username':id,
            'userpass':password,
            'login':'Sign in'
            }
    login_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
    try:
        home_page=s.post(login_url,data,timeout=30).text
    except:
        return False
    if id in home_page:
        return True
    else:
        return False

def getcode(runid):
    code_url="http://acm.hdu.edu.cn/viewcode.php?rid="+runid
    code_page=s.get(code_url,timeout=30)
    code_page.encoding='gbk'#指定编码
    code_page=code_page.text
    #print code_page
    pattern=re.compile(r'<textarea.*?style=.*?>(.*?)</textarea>',re.S)
    code=re.search(pattern,code_page).group(1)
    code=html_parser.unescape(code)#格式化html标签，如标点符号等
    code=code.replace('\r\n','\n')#很重要，不然代码会出现多余空行
    pattern=re.compile(r"<a.*?, 'HDOJ\d{4}(.*?)'.*?>[ Save to File]",re.S)
    code_type=re.search(pattern,code_page).group(1)
    #print code,code_type
    return (code,code_type)

def gettitle(pro_id):
    pro_url="http://acm.hdu.edu.cn/showproblem.php?pid="+str(pro_id)
    pro_page=s.get(pro_url,timeout=30)
    pro_page.encoding='gbk'
    pro_page=pro_page.text
    pattern=re.compile(r'<tr><td.*?><h1.*?>(.*?)</h1>',re.S)
    pro_title=re.search(pattern,pro_page).group(1)
    #print pro_title
    return pro_title

def run(id,password,dirpath):
    ok=login(id,password)
    if not ok:
        print "Login fail!Wrong id or wrong password!"
        return False
    print "Login success!"
    os.chdir(dirpath)
    status_url="http://acm.hdu.edu.cn/status.php?first=&pid=&user="+id+"&lang=0&status=5"
    while True:
        page=s.get(status_url,timeout=30).text
        pattern=re.compile("<tr.*?align=center ><td height=22px>(.*?)</td><td>.*?</td><td>.*?<a href=.*?>(.*?)</a></td>",re.S)
        pro=re.findall(pattern,page)
        #print pro
        for item in pro:
            pro_id=item[1]
            run_id=item[0]
            title=gettitle(pro_id)
            code=getcode(run_id)
            pro_name=pro_id+' '+title+code[1]
            pro_name=re.sub(r'[\/:"*?<>|]'," ",pro_name)
            #如需覆盖同名文件忽略下面4行
            tmp=1
            while(os.path.exists(dirpath+'\\'+pro_name)):
                tmp+=1
                pro_name=pro_id+' '+title+'('+str(tmp)+')'+code[1]
            print u"正在保存"+pro_name+"..."
            f=open(pro_name,"w")
            f.write(code[0].encode('utf-8'))
            f.close()
            print u"保存"+pro_name+u"完成。"
        status_url=re.search(r'Prev Page</a><a.*?href="(.*?)">Next Page',page)
        if(status_url==None):
            break
        status_url=host+status_url.group(1)
        #print status_url
    print(u"执行完毕！按任意键退出...")
    msvcrt.getch()
    return True

id=raw_input("Please input your User ID:")
password=getpass.getpass("Please input your password:")
dirpath=raw_input("Please input direetory:")
run(id,password,dirpath)
#run("jiajiawang","********","E:\hdoj")
