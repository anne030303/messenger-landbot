#Python libraries that we need to import for our bot
import sys
from flask import Flask, request
from datetime import datetime
import requests
import json
import os 
import modules

app = Flask(__name__)
ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
#hahaha
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200
        return "Hello world", 200
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        data = request.get_json(force=True)
        messaging_events = data['entry'][0]['messaging']
        for event in messaging_events:
            sender = event['sender']['id']
            message = None
            print('event ', event)
            if 'message' in event and 'text' in event['message']:
                #判斷是否為快速回復
                if 'quick_reply' in event['message'] and 'payload' in event['message']['quick_reply']:
                    quick_reply_payload = event['message']['quick_reply']['payload']
                    message = modules.search(quick_reply_payload, sender=sender, postback=True)
                #由使用者輸入的字句
                else:
                    text = event['message']['text']
                    message = modules.search(text, sender=sender)

            if 'postback' in event and 'payload' in event['postback']:
                postback_payload = event['postback']['payload']
                message = modules.search(postback_payload, sender=sender, postback=True)
            if message is not None:
                payload = {
                    'recipient': {
                        'id': sender
                    },
                    'message': message
                }
                r = requests.post('https://graph.facebook.com/v2.6/me/messages', 
                                  params={'access_token': ACCESS_TOKEN},
                                  json=payload)

                        
        return "ok", 200




if __name__ == "__main__":
    app.run(debug=True)