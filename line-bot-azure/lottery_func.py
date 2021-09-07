from bs4 import BeautifulSoup
import requests
import re
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def scanlottery(subscription_key,endpoint,img):
    #第一張彩色(收集號碼)
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    local_image_path = os.getcwd() +'//'+ img
    local_image = open(local_image_path, "rb")
    recognize_printed_results = computervision_client.batch_read_file_in_stream(local_image,  raw=True)
    operation_location_remote = recognize_printed_results.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]
    while True:
        get_printed_text_results = computervision_client.get_read_operation_result(operation_id)
        if get_printed_text_results.status not in ['NotStarted', 'Running']:
            break
    str1=''
    if get_printed_text_results.status == TextOperationStatusCodes.succeeded:
        for text_result in get_printed_text_results.recognition_results:
            for line in text_result.lines:
                str1+=line.text
    #第二張轉黑白(收集第幾期)
    image_file = Image.open(img)
    image_file = image_file.convert('1') # 轉成黑白
    image_file.save('another.jpg')
    local_image_path = os.getcwd() + '/another.jpg'
    local_image = open(local_image_path, "rb")
    recognize_printed_results = computervision_client.batch_read_file_in_stream(local_image,  raw=True)
    operation_location_remote = recognize_printed_results.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]
    while True:
        get_printed_text_results = computervision_client.get_read_operation_result(operation_id)
        if get_printed_text_results.status not in ['NotStarted', 'Running']:
            break
    str1 +='------------黑白之後--------------'
    if get_printed_text_results.status == TextOperationStatusCodes.succeeded:
        for text_result in get_printed_text_results.recognition_results:
            for line in text_result.lines:
                str1+=line.text
    #return str1(包括#110000078 號碼 6 X 2)
    return str1



def re_tolist(str1):
    '''用azure掃瞄照片，辨識文字 'str' '''

    numbers=" ".join(re.findall("(\d\d \d\d \d\d \d\d \d\d \d\d)[\w.]",str1)).split(' ')
    numberslist=' '.join(numbers).split(' ')
    set_n=len(numberslist)//6
    mylist=[]
    for i in range(0,set_n):
        mylist.append(numberslist[i*6:i*6+6])
    return mylist

def getsoup(lotteryNo):
    '''此為Beautifulsoup 爬取資料'''

    url = "https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx" #大樂透網址

    with requests.Session() as s:
        headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        data = {
        "Lotto649Control_history$btnSubmit": "查詢",
        "Lotto649Control_history$chk": "radNO",
        }
        data["Lotto649Control_history$txtNO"]=lotteryNo
        ss = s.get(url,headers=headers)
        soup = BeautifulSoup(ss.content,"html.parser")
        data["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
        data["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
        data["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
        ss = s.post(url,headers=headers,data=data)
        soup=BeautifulSoup(ss.text,'html.parser')
        return soup

def winning_numbers(soup):
    '''大樂透的中獎號碼'''

    winnumbers=[]  
    for i in range(1,7):
        # 六個普通號
        winnumbers.append(soup.select('span[id="Lotto649Control_history_dlQuery_No%s_0"]'%(i))[0].text) 
    # 一個特別號
    winnumbers.append(soup.select('span[id="SuperLotto638Control_history1_dlQuery_No7_0"]')[0].text) 
    return winnumbers

def match(mylist,winnumber):
    '''match 自己號碼和中獎號碼 看有幾個中
    x -> [natural=? , special=?]
    '''

    natural,special=0,0
    x=[]
    for number in mylist:
        if number in winnumber[0:6]: #前六個為普通號
            natural+=1
        elif number in winnumber[6]: #第七個為特別號
            special=1
    x.append(natural)
    x.append(special)
    return x

def getmoney(soup,x):
    '''
    soup 找出各種獎項的金額
    再用 x 得出玩家得獎金額 放入award字典中
    '''
    award={}
    natural,special=x
    if natural ==6:
        award['頭獎']=soup.select('span[id="Lotto649Control_history_dlQuery_L649_CategA4_0"]')[0].text +'元'
    elif natural ==5 and special ==1:
        award['貳獎']= soup.select('span[id="Lotto649Control_history_dlQuery_Label7_0"]')[0].text +'元'
    elif natural ==5:
        award['參獎']=soup.select('span[id="Lotto649Control_history_dlQuery_Label8_0"]')[0].text +'元'
    elif natural ==4 and special ==1:
        award['肆獎']=soup.select('span[id="Lotto649Control_history_dlQuery_Label9_0"]')[0].text +'元'
    elif natural ==4:
        award['伍獎']=soup.select('span[id="Lotto649Control_history_dlQuery_Label10_0"]')[0].text +'元'
    elif natural ==3 and special ==1:
        award['陸獎']=soup.select('span[id="Lotto649Control_history_dlQuery_Label11_0"]')[0].text +'元'
    elif natural ==2 and special ==1:
        award['柒獎']=soup.select('span[id="Lotto649Control_history_dlQuery_Label12_0"]')[0].text +'元'
    elif natural ==3:
        award['普獎']=soup.select('span[id="Lotto649Control_history_dlQuery_Label13_0"]')[0].text +'元'
    else:
        award['沒得獎']='哭哭'
    return award

def main(scan):
    subscription_key = 'e9517eef1d664b709b7610da6c009a4d'
    endpoint = 'https://tfb103vis.cognitiveservices.azure.com/'
    # scan= scand
    str1=scanlottery(subscription_key,endpoint,img=scan)
    lotteryNo=re.findall('#\d{9}',str1)[0][1:]   #大樂透第N期
    mylist = re_tolist(str1)    # Regular Expression取玩家大樂透號碼
    soup= getsoup(lotteryNo)       # 取大樂透網站的soup
    win_number=winning_numbers(soup)  # 大樂透中獎號碼
    temp = list()
    # 玩家大樂透逐筆比對
    for mylottery in mylist:    
        x=match(mylottery,win_number)
        award=getmoney(soup,x)
        mylottery_str = ' '.join(mylottery)
        result = '號碼為:'+mylottery_str
        # print(result)
        award_keys = list(award.keys())[0]
        award_values = list(award.values())[0]
        result2 = '結果為:'+award_keys+'~'+award_values
        # print(result2) #dict轉成list取出需要的key value
        r = result+'\n'+result2
        temp.append(r)
        temp_str = '\n'.join(temp)
    return temp_str
