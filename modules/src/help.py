import modules
from templates.quick_replies import add_quick_reply
from templates.text import TextTemplate


def process(input, entities=None):
    help = '哈囉! 我是土思機! 請問有什麼需要幫助的嗎?'
    if entities is not None:
        if 'sender' in entities and 'first_name' in entities['sender']:
            sender_name = entities['sender']['first_name']
            help = help.replace('there', sender_name)
    help += '\n\n我可以幫你'
    help += '\n  - 檢查租賃契約'
    help += '\n  - 我是房東/房客'
    help += '\n\n有時我會睡著一下~需要一些時間清醒\n請稍微等我一下'
    help += '\n歡迎隨時呼叫我! 也祝你有個美好的一天~'

    message = TextTemplate(help).get_message()
    message = add_quick_reply(message, '租賃契約', modules.generate_postback('lease_contract'))
    message = add_quick_reply(message, 'land', modules.generate_postback('land_toast'))

    output = {
        'input': input,
        'output': message,
        'success': True
    }
    return output
