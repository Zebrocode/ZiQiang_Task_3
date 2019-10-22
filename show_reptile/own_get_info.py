from bs4 import BeautifulSoup
from urllib.parse import urlencode  # 编码 URL 字符串
import time
import requests
import re
import sys


#get one page's whole html
def get_raw_page(i):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        
        urlFormat = 'http://cs.whu.edu.cn/news_show.aspx?id={0}'
        url = urlFormat.format(i)
        response = requests.get(url,headers = headers)
        # print('response.status_code:',response.status_code)
        if response.status_code == 200:  
            return response.text
        return None
    except RequestException:
        print('爬取失败')

#main loop        
def get_page_loop(page_num):
    #result list
    ans = []
    try_id = 1175
    empty_count = 0
    valid_count = 0
    while True:
        dict={}
        #get one page
        html = get_raw_page(try_id)
        # print("trying :",try_id)
        # print("empty_id:",empty_count)
        if not is_page_exist(html):
            empty_count += 1
            if empty_count > 5: #5 consecutive empties get out of the  while loop
                break;
        else:
            empty_count = 0
            dict['title'],dict['time'],dict['content'] = get_info(html)
            ans.append(dict)
            valid_count += 1
        try_id -= 1
        if valid_count >= page_num:
            break;
    return ans


#judge the html is valid or not    
def is_page_exist(html):
    soup = BeautifulSoup(html,features='html.parser')
    #find_all: name attrs recursive text **kwargs
    ret = soup.find(name='div',attrs={"class": "content"})
    if ret ==None:
        return True
    if ret.contents[0].strip() == "出错啦，您要浏览的页面不存在或已删除！":
        return False
    else:
        return True


#get title time contents
def get_info(html):
    soup = BeautifulSoup(html,features='html.parser')
    title = soup.find(name='div',attrs={"class":"sp1"}).contents[0].strip()
    time = soup.find(text=re.compile("[1-2][0-9]{3}[\u4e00-\u9fa5][0-1][1-9][\u4e00-\u9fa5][0-3][0-9][\u4e00-\u9fa5]"))
    content = ""
    pre_content = soup.find(name='div',attrs={"class":"right_list_sp"}).contents[5]
    content = pre_content.get_text(strip=True)#get text from tag(include its  descendants)
    content = content.replace(u'\xa0', u' ')# space delete
    return title,time,content

#save the raw html code in files for analyse
def save_page(html):
    with open("cs_info_text.html",'w',encoding='utf-8') as file:
        file.write(html)
    

if __name__ == "__main__":  
    get_page_loop(int(sys.argv[1]))
    print("成功爬取的通知数:",len(ans))
    print("爬取内容如下:\n")
    print(ans)

    

    
    
    
