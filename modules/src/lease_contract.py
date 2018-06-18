import modules
from templates.quick_replies import add_quick_reply
from templates.text import TextTemplate
from templates.button import *

entities = {
    'type':None,
    'choice':None
}

def process(input, entities = None):
    print('process',input,entities)
    output = {}
    if entities['type'] == None:
        message = TextTemplate('嗨，我是土思機器人啦！\n想要我幫你檢查看看，你簽的租賃契約合理嗎？').get_message()
        entities['type'] = 'step1'
        entities['choice'] = True
        message = add_quick_reply(message, '好啊，拿出契約來檢查一下好了！', modules.generate_postback(input,entities))
        entities['choice'] = False
        message = add_quick_reply(message, '不想，我沒有租屋啦', modules.generate_postback(input,entities))
        
    elif entities['type'] == 'step1':
        entities['type'] = 'step2'
        if entities['choice'] == True:
            message = TextTemplate('開始囉！上面寫的押金是幾個月租金呢？').get_message()
            entities['choice'] = True
            message = add_quick_reply(message, '2個月以下', modules.generate_postback(input,entities))
            entities['choice'] = False
            message = add_quick_reply(message, '2個月以上', modules.generate_postback(input,entities))
        elif entities['choice'] == False:
            message = TextTemplate('那我們無話可說…').get_message()
            entities['choice'] = None
        
    elif entities['type'] == 'step2':
        entities['type'] = 'step3'
        if entities['choice'] == True:
            message = TextTemplate('太好了，押金最高不可以超過2個月房屋租金的總額。\n也建議要在合約上寫清楚退還時間與方式喔！\n\n下一題，契約裡的租金有寫清楚嗎？').get_message()
            entities['choice'] = True
            message = add_quick_reply(message, '有喔！', modules.generate_postback(input,entities))
            entities['choice'] = False
            message = add_quick_reply(message, '好像….沒有欸？!', modules.generate_postback(input,entities))
        elif entities['choice'] == False:
            message = TextTemplate('什麼?!你知道這樣其實已經超過法律規定的額度了嗎….').get_message()
            entities['choice'] = None
            
    elif entities['type'] == 'step3':
        entities['type'] = 'step4'
        if entities['choice'] == True:
            message = TextTemplate('讚喔！除了租金的金額外，也應該包括何時給付及付款方式。還有管理費、清潔費或其他費用，也應該盡量寫在合約中。\n\n再來，修繕的責任有寫清楚嗎？').get_message()
            entities['choice'] = True
            message = add_quick_reply(message, '寫得清清楚楚', modules.generate_postback(input,entities))
            entities['choice'] = False
            message = add_quick_reply(message, '疑?!怎麼沒看到…', modules.generate_postback(input,entities))
        elif entities['choice'] == False:
            message = TextTemplate('什麼?!你知道這樣有可能被多收錢嗎…').get_message()
            entities['choice'] = None
    
    elif entities['type'] == 'step4':
        entities['type'] = 'step5'
        if entities['choice'] == True:
            message = TextTemplate('喔喔喔喔！美賣喔~~~也建議在簽約時，依照實際狀況，逐一討論並載明於租約中，未來比較不會有爭執喔！            \n\n再來，上面有寫到不能報稅嗎？').get_message()
            entities['choice'] = True
            message = add_quick_reply(message, '沒有！', modules.generate_postback(input,entities))
            entities['choice'] = False
            message = add_quick_reply(message, '可…可惡！房東特別寫下來了啦…', modules.generate_postback(input,entities))
        elif entities['choice'] == False:
            message = TextTemplate('什麼?!你知道這樣有可能被多收錢嗎…').get_message()
            entities['choice'] = None
            
    elif entities['type'] == 'step5':
        entities['type'] = 'step6'
        if entities['choice'] == True:
            message = TextTemplate('太厲害了，恭喜你完成租約的考驗！你的租賃契約寫得很不錯，要記得確保契約內容，權利才會有保障喔！').get_message()
            entities['choice'] = None
        elif entities['choice'] == False:
            message = TextTemplate('什麼?!你知道房東這樣其實是違法的嗎….').get_message()
            entities['choice'] = None
            
    elif entities['type'] == 'end':
        template = TextTemplate()
        template.set_text('更多詳細內容請看我們整理的懶人包：今天要簽約？教你看到租約一眼就抓到重點')
        text = template.get_text()
        template = ButtonTemplate(text)
        #message = TextTemplate('更多詳細內容請看我們整理的懶人包：今天要簽約？教你看到租約一眼就抓到重點').get_message()
        link = 'https://www.facebook.com/LandToast'
        #template = ButtonTemplate(message)
        template.add_web_url('傳送門', link)
        output['input'] = input
        output['output'] = template.get_message()
        output['success'] = True
        return output
    
    else:
        output['success'] = False
        return output
            
    if entities['choice'] == None:
        entities['type'] = None
        message = add_quick_reply(message, '再試一次!', 
                                  modules.generate_postback(input,entities))
        entities['type'] = 'end'
        message = add_quick_reply(message, '結束對話',
                                  modules.generate_postback(input,entities))
            
        
    output['input'] = input
    output['output'] = message
    output['success'] = True
    
    return output