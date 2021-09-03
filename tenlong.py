from bs4 import BeautifulSoup
import requests
import csv
import re

def keyword(search,pages):
    with open('%s.csv'%(search),'w',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['書名', '書籍網址', '作者','出版社','ISBN','圖片網址'])
        pages=int(pages)
        for page in range(1,pages+1):
            searchurl='https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword={}&page={}'.format(search,page)
            headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
            res=requests.get(searchurl,headers=headers)
            soup=BeautifulSoup(res.text,'html.parser')
            titles=soup.select('div[class="book-data"] a')
            for single in titles:
                title=single.text
                url='https://www.tenlong.com.tw/'+single['href']

                #個別網頁
                res=requests.get(url,headers=headers)
                articlesoup=BeautifulSoup(res.text,'html.parser')
                author=articlesoup.select('h3[class="item-author"]')[0].text.split('著')[0].strip().replace('\n',"").replace('   ','')
                publisher=articlesoup.select('span[class="info-content"]')[0].text.replace('\n',"")
                isbn=articlesoup.select('span[class="info-content"]')
                
                  #isbn位置不定
                findstr=' '.join([i.text for i in isbn])
                isbn=''.join(re.findall('\d{13}',findstr))

                image=articlesoup.select('picture img')[0]['src']
                if image=='':
                  image='0'
                writer.writerow([title, url, author,publisher,isbn,image])



keyword('python','5')

