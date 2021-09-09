import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
ua = UserAgent()
titlelist = []  #書名
htmls = []      #書本網址
images = []     #書本圖片
isbns = []      #ISBN
authors = []    #作家
publishs = []   #出版社
user_Agent = ua.random
# print(user_Agent)
headers = {
    'User-Agent': user_Agent
}
def book(keyword,pages):
    for page in range(1,int(pages)+1):
    # url = 'https://search.books.com.tw/search/query/cat/1/sort/1/v/0/page/4/spell/3/ms2/ms2_1/key/python'
        url = 'https://search.books.com.tw/search/query/cat/1/sort/1/v/0/spell/3/ms2/ms2_1/page/{}/key/{}}'.format(str(page), keyword)

        # def get_titles(url):
        res = requests.get(url, headers=headers)
        # print(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        time.sleep(1)
        titles = soup.select('table[id="itemlist_table"] img')
        title_htmls_numbers = soup.select('table[id="itemlist_table"] tbody')
        for title in titles:
            images.append(title['data-srcset'])#圖片網址
            # print(title['data-srcset'])
            titlelist.append(title['alt'])  #書名

        for html in title_htmls_numbers:
            html = "https://www.books.com.tw/products/"+(html['id'].split('_')[1])
            htmls.append(html)
            print(html)
            time.sleep(5)  
            response = requests.get(html,headers = headers)
            soup2 = BeautifulSoup(response.text,"lxml")
            time.sleep(5)
            try:
                isbntest = soup2.select('div[class="bd"] li')[0].text  #ISBN: XXXXXX...
                isbn = isbntest.split(('：'))[1]
            except:
                isbntest = 0
                isbn = isbntest
            isbns.append(isbn)
            time.sleep(1)
            publish = soup2.select('div[class="type02_p003 clearfix"] ul')[0]  #出版社
            author = []
            for i in publish.select('span'):
                if i.text != ("") and i.text != ('\xa0'):
                    publishs.append(i.text)
            for i in (publish.select('li')[0].select('a')):
                if i.text =='修改' or i.text =='確定' or i.text=='取消' or i.text == '新功能介紹' or i.text == '\xa0':
                    pass
                else:
                    author.append(i.text)
            
            authors.append(author)
            time.sleep(50)
            print("==============")


    print("OK")
    print(len(titlelist))
    print(len(htmls))
    print(len(authors))
    print(len(publishs))
    print(len(isbns))
    print(len(images))

    data ={
        "書名":titlelist,
        "書籍網址":htmls,
        "作者":authors,
        "出版社":publishs,
        "ISBN":isbns,
        "圖片網址":images
        }
    df = pd.DataFrame(data=data)
    df.to_csv("BOOK_{}.csv".format(keyword),encoding="utf-8-sig",index=False)
    print("Completed")
book(input("您要搜尋的書籍?"),input("您要總查詢的頁數?"))
book(input("Press Enter to exit!"))


# https://search.books.com.tw/



