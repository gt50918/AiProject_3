## 操作步驟

1.打開SecretFile.txt
把需要的資料貼到對應的位置
對照:
|channelAccessToken|channelSecret|subscription_key|endpoint
|:---|:---|:---|:---
|LINE Message API Token|LINE channel Secret|AZURE 金鑰|AZURE 端點

2.cd到資料夾底下執行:
```
docker-compose up
``` 
3.使用另一個終端機cd 到資料夾底下，執行:
```
curl $(docker port chatbot_ngrok 4040)/api/tunnels
```
把「https:....」貼到LINE BOT DEVELOPER 的Webhook ，再加上/callback

4.可以常使用LINE BOT了


## 影片網址
[line-bot大樂透兌獎成果](https://www.youtube.com/watch?v=mA5YPS0AZfY)

