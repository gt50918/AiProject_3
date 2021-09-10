import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
import copy
ua = UserAgent()
 
titlelist = ''  #書名
htmls = ''      #書本網址
images = ''     #書本圖片
isbns = ''      #ISBN
authors = ''    #作家
publishs = ''   #出版社

data ={
    # "書名":titlelist,
    "書籍網址":htmls,
    "作者":authors,
    "出版社":publishs,
    "ISBN":isbns,
    # "圖片網址":images
    }

df = pd.DataFrame(columns=data)
df.to_csv("BOOK.csv",encoding="utf-8-sig",index=False)

request_times=0
for page in range(1, 1):
    # url = 'https://search.books.com.tw/search/query/cat/1/sort/1/v/0/page/4/spell/3/ms2/ms2_1/key/python'
    url = 'https://search.books.com.tw/search/query/cat/1/sort/1/v/0/spell/3/ms2/ms2_1/page/%s/key/python'%(page)
    user_Agent = ua.random
    headers = {
        'User-Agent': user_Agent
    }

    res = requests.get(url, headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')   
    time.sleep(1)

    titles = soup.select('table[id="itemlist_table"] img')
    title_htmls_numbers = soup.select('table[id="itemlist_table"] tbody')

    # for title in titles:
    #     images.append(title['data-srcset'])#圖片網址
    #     # print(title['data-srcset'])
    #     titlelist.append(title['alt'])  #書名
    #     print(titlelist)

    for html in title_htmls_numbers:
        html = "https://www.books.com.tw/products/"+(html['id'].split('_')[1])
        htmls=html
        print(htmls)
        time.sleep(5) 

        response = requests.get(html,headers = headers)
        time.sleep(5)
        response1 =copy.deepcopy(response.text)
        soup2 = BeautifulSoup(response1,"lxml")

        time.sleep(5)
        # titlelist=
        # images=
        isbntest = soup2.select('div[class="bd"] li')[0].text  #ISBN: XXXXXX...
        isbn = isbntest.split(('：'))[1]
        isbns=isbn

        time.sleep(1)
        publish = soup2.select('div[class="type02_p003 clearfix"] ul')[0]  #出版社

        author = []
        for i in publish.select('span'):
            if i.text != ("") and i.text != ('\xa0'):
                publishs=i.text


        for i in (publish.select('li')[0].select('a')):
            if i.text =='修改' or i.text =='確定' or i.text=='取消' or i.text == '新功能介紹' or i.text == '\xa0':
                pass
            else:
                
                author.append(i.text)

        authors=''.join(author)

        time.sleep(2)

        request_times+=1
        if request_times %30 ==0:
            time.sleep(30)
        print("==============",request_times,'次')

        df1=pd.DataFrame([[htmls,authors,publishs,isbns]])
        df1.to_csv("BOOK.csv",encoding="utf-8-sig",mode = 'a', header = False, index = False)

        # titlelist = ''  #書名
        htmls = ''      #書本網址
        # images = ''     #書本圖片
        isbns = ''      #ISBN
        authors = ''    #作家
        publishs = ''   #出版社

    print('已經訪問',request_times,'次')
    print("OK")
    print(len(titlelist))
    print(len(htmls))
    print(len(authors))
    print(len(publishs))
    print(len(isbns))
    print(len(images))


    print("Completed")




# https://search.books.com.tw/

