import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_useragent import UserAgent
import re
ua = UserAgent()
titlelist = []  #書名
htmls = []      #書本網址
images = []     #書本圖片
isbns = []      #ISBN
authors = []    #作家
publishs = []   #出版社
introduces = []  #作者簡介
user_Agent = ua.random
# print(user_Agent)
headers = {
    'User-Agent': user_Agent
}
html = 'https://www.books.com.tw/products/0010758148'
 
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
# intro = soup2.select('div>div>div>div>div')
intro = soup2.select('div[style="height:auto;"]')
for f in intro:
    pass
# print (f.text)
# print(type(f.text))
introduces.append(f.text)

time.sleep(10)
data2 ={
    "ISBN":isbns,
    "作者簡介":introduces
    }
df = pd.DataFrame(data=data2)
df.to_csv("BOOK_introduce.csv",encoding="utf-8-sig",index=False)
print("Completed")
print("==============")