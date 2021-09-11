from bs4 import BeautifulSoup
import requests
import csv
import re
import time
import json

def create_csv(keyword):
    with open('%s.csv'%(keyword),'w',newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['書名', '書籍網址', '作者','出版社','ISBN','圖片網址'])
def create_intro_csv(keyword):
    with open('%s_intro.csv'%(keyword),'w',newline='',encoding='utf-8-sig') as f:
        writer =csv.writer(f)
        writer.writerow(['ISBN','簡介'])

def main(category,keywordlist):
    for keyword in keywordlist:
        create_csv(keyword)
        create_intro_csv(keyword)

        headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        page=1
        while True:
            searchurl='https://www.tenlong.com.tw/search?utf8=%E2%9C%93&keyword={}&page={}'.format(keyword,page)
            res=requests.get(searchurl,headers=headers)
            soup=BeautifulSoup(res.text,'html.parser')
            titles=soup.select('div[class="book-data"] a')
            
            for single in titles:
                title=single.text

                url='https://www.tenlong.com.tw/'+single['href']
                print(url+' | '+category,keyword +' 第'+str(page)+'頁')
                try:
                    #個別網頁
                    res=requests.get(url,headers=headers)
                    articlesoup=BeautifulSoup(res.text,'html.parser')
                    author=articlesoup.select('h3[class="item-author"]')[0].text.split('著')[0].strip().replace('\n',"").replace('   ','')
                    publisher=articlesoup.select('span[class="info-content"]')[0].text.replace('\n',"")

                    #isbn位置不定
                    isbn=articlesoup.select('span[class="info-content"]')
                    findstr=' '.join([i.text for i in isbn])
                    isbn=''.join(re.findall('\d{13}',findstr))

                    #沒有image設定為0
                    image=articlesoup.select('div[class="item-info"] img')[0]['src']
                    if len(re.findall('.*noimg.*',image))>0: #只要網址有noimg視為沒有照片
                        image='0'

                    introduction=articlesoup.select('div[class="item-desc"]')[0].text

                    with open('%s.csv'%(keyword),'a+',newline='',encoding='utf-8-sig') as f:
                        writer = csv.writer(f)
                        writer.writerow([title, url, author,publisher,isbn,image])
                    with open('%s_intro.csv'%(keyword),'a+',newline='',encoding='utf-8-sig') as f:
                        writer = csv.writer(f) 
                        writer.writerow([isbn,introduction])
                    time.sleep(1)
                except:
                    time.sleep(60) # 如果出現爬蟲失敗則sleep 60秒，並跳過此url的內文
                    
            if soup.select('a[rel="next"]')==[]: #如果沒有下一頁，跳出
                break

            page+=1


with open('categories.txt', "r",encoding='utf-8') as f:
    key=json.load(f)
    for category,keywordlist in key.items():
        main(category,keywordlist)