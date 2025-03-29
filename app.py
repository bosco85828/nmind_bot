import os 
from flask import Flask, request, abort
import re
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,
)
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os 
from crawler import main

load_dotenv()

LINE_TOKEN=os.getenv('LINE_TOKEN')
LINE_SECRET=os.getenv('LINE_SECRET')

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

path=os.path.dirname(os.path.abspath(__file__))
   
@app.route("/callback", methods=['POST'])
def callback():
    global data
    global data_type
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    data = json.loads(body)
    data_type = data['events'][0]['type']
    app.logger.info("Request body: " + body)
    print(data)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

    # try : 
    #     if data_type == 'unsend' : 

            
    #         msgID = data['events'][0]['unsend']['messageId']
    #         groupID = data['events'][0]['source']['groupId']
    #         userID = data['events'][0]['source']['userId']
            
    #         usermsg = getsheet2(msgID)
    #         profile = line_bot_api.get_profile(userID)
    #         profile = json.loads(str(profile)) 
    #         userName = profile['displayName']
    #         msg = f'{userName}收回訊息:{usermsg}'
    #         line_bot_api.push_message(groupID, TextSendMessage(text=msg))

    #     elif data_type == 'message' :
    #         usermsg = data['events'][0]['message']['text']
    #         msgID = data['events'][0]['message']['id']
    #         msglist = [msgID,usermsg]
    #         gsheet2(msglist)
        
    #     return 'OK'
    # except:
    #     return 'OK'

    


@app.route("/",methods=['get'])
def index():
    print('Welcome')
    return 'success'

def sendimg(event,msgurl):
    line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                    original_content_url=msgurl,
                    preview_image_url=msgurl))
def sendtext(event,msg):
    line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg))



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    msg_text= event.message.text
    msg_type= event.type
    
    if re.search(r'^\/.*',msg_text):
        search_code=msg_text[1:]
        try:
            data=main(search_code)
            if data:
                # result=json.dumps(data,ensure_ascii=False).replace('}, {','\n').replace('[{','\n').replace('],','\n')
                
                china_data = "\n".join(json.dumps(item, ensure_ascii=False) for item in data['大陸'])  if data.get('大陸') else None
                japen_data = "\n".join(json.dumps(item, ensure_ascii=False) for item in data['日本']) if data.get('日本') else None
                korea_data = "\n".join(json.dumps(item, ensure_ascii=False) for item in data['韓國']) if data.get('韓國') else None


            else : 
                sendtext(event,"查無此產品")  
        except Exception as err : 
            sendtext(event,err)
        
        try : sendtext(event,f"""
{search_code} + '查詢結果如下' 
=== 中國 === 
{china_data}

=== 日本 ===
{japen_data}

=== 韓國 ===
{korea_data}
                       """)
        except Exception as err : 
            sendtext(event,{err})
    
    else:
        sendtext(event,"Please input type for '/your_id'") 

if __name__ == "__main__":

    app.run(host="0.0.0.0")