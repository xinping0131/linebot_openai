from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler1 = WebhookHandler(os.getenv('CHANNEL_SECRET'))
counter=0

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
   global counter
    text1=event.message.text
    ability={"職業":"老師" ,
             "技能":"數學"
            }
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": text1}
            {"role": "system", "content": "這是GPT的個性資訊" +str(ability)}
        ],
        model="gpt-3.5-turbo-0125",
        temperature = 0.5,
    )
    try:
        ret = response['choices'][0]['message']['content'].strip()
        counter+=1
    except:
        ret = '發生錯誤！'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ret))
    counter+=1
    print(f"OpenAI 已傳送 {counter} 條訊息")
if __name__ == '__main__':
    app.run()
