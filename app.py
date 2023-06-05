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
from crawler import new_snk_data

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
    
    if re.search(r'^\/.*$',msg_text):
        search_code=msg_text[1:]
        
        try : sendtext(event,new_snk_data(search_code))
        except Exception as err : 
            sendtext(event,{err})

if __name__ == "__main__":
    app.run(host="0.0.0.0")