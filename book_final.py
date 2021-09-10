import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from fake_useragent import UserAgent


ua = UserAgent()
user_Agent = ua.random
# print(user_Agent)
headers = {'User-Agent': user_Agent}
book_np = 0
pages=0
keyword="python"
for page in range(1,int(pages)+1):
    url = 'https://search.books.com.tw/search/query/cat/1/sort/1/v/0/spell/3/ms2/ms2_1/page/{}/key/{}'.format(str(page),keyword)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    time.sleep(1)
    title_htmls_numbers = soup.select('table[id="itemlist_table"] tbody')
    for html in title_htmls_numbers:
        book = list()
        book_intro = list()
        html = "https://www.books.com.tw/products/"+(html['id'].split('_')[1]) #書網址
        response = requests.get(html,headers = headers)
        soup2 = BeautifulSoup(response.text,"html.parser")
        title = soup2.select('div[class="mod type02_p002 clearfix"]')[0].text.replace('\n','') #書名
        image = soup2.select('div[class="cnt_mod002 cover_img"] img')[0].get('src')#圖片網址
        # print("t",title)
        # print("i",image)
        time.sleep(5)
        try:
            isbntest = soup2.select('div[class="bd"] li')[0].text  #ISBN: XXXXXX...
            isbn = isbntest.split(('：'))[1]
        except:
            isbntest = 0
            isbn = isbntest
        # isbns.append(isbn)
        time.sleep(1)
        publish = soup2.select('div[class="type02_p003 clearfix"] ul')[0]  #出版社
        for i in publish.select('span'):
            if i.text != ("") and i.text != ('\xa0'):
                publisher = i.text
        author = []
        for i in (publish.select('li')[0].select('a')):
            if i.text =='修改' or i.text =='確定' or i.text=='取消' or i.text == '新功能介紹' or i.text == '\xa0':
                pass
            else:
                author.append(i.text)
        book.extend([title,html,author,publisher,isbn,image])
        # print(book)
        # authors.append(author)
        intros = []
        intro = soup2.select('div[class="content"]')
        if intro != []:
            for i in intro:
                intros.append(i.text)
            introx = ''.join(intros).replace('\n','')
            # print(introx)
            book_intro.extend([isbn,introx])
        else:
            # print(0)
            book_intro.extend([isbn,'0'])
        # print("==============")
        if book_np is 0:
            book_np = np.array([book])
            book_intro_np = np.array([book_intro])
        else:
            book_np = np.vstack([book_np,book])
            book_intro_np = np.vstack([book_intro_np,book_intro])
        # print(book_np)
        # print(book_intro_np)
        print("Loading...")
        print("==============")
        time.sleep(5)
    print("第{}頁".format(page).center(20,"="))



    print("OK")
#     print(len(titlelist))
#     print(len(htmls))
#     print(len(authors))
#     print(len(publishs))
#     print(len(isbns))
#     print(len(images))
    


df = pd.DataFrame(data=book_np,columns=("書名","書籍網站","作者","出版社","ISBN","圖片網址"))
df_intro = pd.DataFrame(data=book_intro_np,columns=("ISBN","書籍簡介"))
df.to_csv("BOOK_python.csv",encoding="utf-8-sig",index=False)
df_intro.to_csv("BOOK_python_intro.csv",encoding="utf-8-sig",index=False)

print("Completed")


# book(input("您要搜尋的書籍?"),input("您要總查詢的頁數?"))
# (input("Press Enter to exit!"))


# https://search.books.com.tw/



