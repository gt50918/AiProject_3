import requests
import json
import os
import pandas as pd
import urllib.parse

if not os.path.exists('./WebCrawle-eslite'):
    os.mkdir('./WebCrawle-eslite')

keywords=str(input("請輸入搜尋關鍵字:"))
urlkeywords=urllib.parse.quote(keywords)
page=0
manypage=int(input("請問需要幾頁:"))

bookname=[]
bookURL=[]
bookauthor=[]
booksupplier=[]
bookisbn13=[]
picture=[]

url = 'https://athena.eslite.com/api/v2/search?q={}&final_price=0,&sort=_weight_+desc&size=20&start={}'.format(urlkeywords,page)
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'

headers = {
    'Referer': 'https://www.eslite.com/Search?keyword={}&final_price=0%2C&sort=_weight_+desc&size=20&start={}'.format(urlkeywords,page)}
res = requests.get(url, headers=headers)
jsonData = json.loads(res.text)
tempid = jsonData['hits']['hit']

for p in range(0,manypage):
    for i in range(0, 20):
        bookid = tempid[i]['id']
        book_URL = tempid[i]['fields']['url']
        bookURL.append(book_URL)
        # picture='https://s.eslite.dev'+tempid[i]['fields']['product_photo_url']
        newurl = 'https://athena.eslite.com/api/v1/products/{}'.format(bookid)
        newheaders = {'Referer': book_URL}
        newres = requests.get(newurl, headers=newheaders)
        newData = json.loads(newres.text)
        book_name = newData['name']  # 書名
        bookname.append(book_name)
        book_author = newData['auth']  # 作者
        bookauthor.append(book_author)
        book_supplier = newData['supplier']  # 出版社
        booksupplier.append(book_supplier)
        book_isbn13 = newData['isbn13']  # ISBN
        bookisbn13.append(book_isbn13)
        bookphotos = newData['photos']
        try:
            book_picture = 'https://s.eslite.dev' + bookphotos[0]['large_path']  # 書圖片
            picture.append(book_picture)
        except :
            picture.append('0')
    page += 1

eslite =pd.DataFrame({'書名': bookname,'書籍網址': bookURL,'作者': bookauthor,'出版社': booksupplier, 'ISBN': bookisbn13,'圖片網址': picture})
eslite.to_csv("./eslite-{}.csv".format(keywords),encoding='utf-8-sig',index=False)




