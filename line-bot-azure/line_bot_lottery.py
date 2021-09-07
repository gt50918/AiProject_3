# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextSendMessage
from linebot.models.messages import ImageMessage
import lottery_func
import time
# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi('TUMeTx6e89YskIYfgtXw7azK/Qp7ghZ7zpG1ftadTfho9Ell85cnos4YHE/j2VYpkW8EcCtoo9Mo85iWp60zeaDWUqXFGulF/MHWb23P92wkQf0IZ3PZY/sz3rCxT/q3JSL1Ia6jcJxgW00XR08uNAdB04t89/1O/w1cDnyilFU=')
# your linebot message API - Channel secret
handler = WebhookHandler('2ab32fa9ab3cf313231d5348e012933f')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle(event):
    
    message_content = line_bot_api.get_message_content(event.message.id)
    # print(event.message.id+".jpg")
    image_id = event.message.id+".jpg"
    with open(image_id, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
        time.sleep(2)
        lottery = lottery_func.main(image_id)   
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text = lottery)])
        time.sleep(1)

# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345)