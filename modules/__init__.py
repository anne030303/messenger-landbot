import json
import os
import sys
import requests
import modules
from modules.src import *
from templates.text import TextTemplate
from templates.quick_replies import add_quick_reply

def generate_postback(module, entities = None):
    return {
        'intent': module,
        'entities': entities
    }

#辨識使用者說的話
def process_query(input):
    #判斷使用者的意圖後，初始化此意圖需要的實體，並將意圖設定為函式名稱
    if input == 'land' or input == 'land_toast':
        intent = 'land_toast'
        entities = {
            'type':None,
            'role':{
                'landlord':None,
                'tenant':None
            }
        }
    elif input == '租賃契約' or input == 'lease_contract':
        intent = 'lease_contract'
        entities = {
            'type':None,
            'choice':None
        }
    else:
        intent = input
        entities = None

    try:
        #判斷使用者的意圖，找到對應的工具
        if intent in src.__all__:
            return intent, entities
        else:
            return None, {}
    except:
        return None, {}



def search(input, sender=None, postback=False):
    #判斷對話
    #判斷是否有延續先前的對話
    #有延續
    if postback:
        payload = json.loads(input)
        #判斷entities需不需要初始化
        #不需要
        print(payload)
        if payload['entities'] != None:
            intent = payload['intent']
            entities = payload['entities']
        #需要
        else:
            intent, entities = process_query(payload['intent'])
    #不延續
    else:
        intent, entities = process_query(input)
    print(intent, entities)
    #依照對話給予相應的module
    if intent is not None:
        if intent in src.__personalized__ and sender is not None:
            #獲取使用者的稱謂
            r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
                'fields': 'first_name',
                'access_token': os.environ["PAGE_ACCESS_TOKEN"]
            })
            if entities is None:
                entities = {}
            #加入使用者的個人資訊
            entities['sender'] = r.json()
        #使用對應modules的process函式
        data = sys.modules['modules.src.' + intent].process(intent, entities)
        print('data',data)
        if data['success']:
            return data['output']
        else:
            if 'error_msg' in data:
                return data['error_msg']
            else:
                return TextTemplate('Something didn\'t work as expected! I\'ll report this to my master.').get_message()
    #搜尋不到意圖的情形
    else:
        message = TextTemplate(
            'I\'m sorry; I\'m not sure I understand what you\'re trying to say.\nTry typing "help" or "request"').get_message()
        message = add_quick_reply(message, 'Help', modules.generate_postback('help'))
        message = add_quick_reply(message, 'Request', modules.generate_postback('request'))
        print('Find None',message,entities)
        return message
