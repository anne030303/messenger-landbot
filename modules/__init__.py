import json
import os
import sys
import requests
import modules
from modules.src import *
from templates.text import TextTemplate

def generate_postback(module,entities = None):
    return {
        'intent': module,
        'entities': entities
    }


def process_query(input):
    if input == 'land':
        intent = 'land_toast'
        entities = {
            'type':None,
            'role':{
                'landlord':None,
                'tenant':None
            }
        }
    
    if intent in src.__all__:
        return intent, entities

    return None, {}


def search(input, sender=None, postback=False):
    if postback:
        payload = json.loads(input)
        intent = payload['intent']
        entities = payload['entities']
    else:
        intent, entities = process_query(input)

    if intent is not None:
        if intent in src.__personalized__ and sender is not None:
            r = requests.get('https://graph.facebook.com/v2.6/' + str(sender), params={
                'fields': 'first_name',
                'access_token': os.environ["PAGE_ACCESS_TOKEN"]
            })
            if entities is None:
                entities = {}
            entities['sender'] = r.json()
        data = sys.modules['modules.src.' + intent].process(intent, entities)
        print('data',data)
        if data['success']:
            return data['output']
        else:
            if 'error_msg' in data:
                return data['error_msg']
            else:
                return TextTemplate('Something didn\'t work as expected! I\'ll report this to my master.').get_message()
    else:
        message = TextTemplate(
            'I\'m sorry; I\'m not sure I understand what you\'re trying to say.\nTry typing "help" or "request"').get_message()
        message = add_quick_reply(message, 'Help', modules.generate_postback('help'))
        message = add_quick_reply(message, 'Request', modules.generate_postback('request'))
        return message,entities
