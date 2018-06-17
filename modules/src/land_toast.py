import json
import modules
from templates.quick_replies import add_quick_reply
from templates.text import TextTemplate

in_entities = {
            'type':None,
            'role':{
                'landlord':None,
                'tenant':None
            }
        }

def process(input, entities=None):
    print('process',input,entities)
    output = {}
    try:
        if entities['type'] == None:
            message = TextTemplate('選擇你的角色').get_message()
            entities['type'] = 'choice'
            entities['role'] = {'landlord':1,'tenant':0}
            message = add_quick_reply(message, '我是房東', modules.generate_postback(input,entities))
            entities['role'] = {'landlord':0,'tenant':1}
            message = add_quick_reply(message, '我是房客', modules.generate_postback(input,entities))
            #message = add_quick_reply(message, '其他', modules.generate_postback('other'))
            
            output['input'] = input
            output['output'] = message
            output['success'] = True
            
        elif entities['type'] == 'choice' and entities['role']['landlord'] == 1:
            entities['type'] = 'landlord_model'
            message = TextTemplate('房東注意事項').get_message()
            message = add_quick_reply(message, '了解更多', modules.generate_postback(input,entities))
            message = add_quick_reply(message, '再試一次!', modules.generate_postback(input,in_entities))
            output['input'] = input
            output['output'] = message
            output['success'] = True
            
        elif entities['type'] == 'choice' and entities['role']['tenant'] == 1:
            entities['type'] = 'tenant_model'
            message = TextTemplate('房客注意事項').get_message()
            message = add_quick_reply(message, '了解更多', modules.generate_postback(input,entities))
            message = add_quick_reply(message, '再試一次!', modules.generate_postback(input,in_entities))
            output['input'] = input
            output['output'] = message
            output['success'] = True
            
        elif entities['type'] == 'landlord_model':
            message = TextTemplate('房東注意事項...').get_message()
            output['input'] = input
            output['output'] = message
            output['success'] = True
        elif entities['type'] == 'tenant_model':
            message = TextTemplate('房客注意事項...').get_message()
            output['input'] = input
            output['output'] = message
            output['success'] = True
        else:
            output['success'] = False
    
    except:
        output['success'] = False
    return output