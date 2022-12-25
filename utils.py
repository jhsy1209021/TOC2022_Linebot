import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, URITemplateAction, ButtonsTemplate, MessageTemplateAction, ImageSendMessage

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token, title, text, btn):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_carousel_message(reply_token, col):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(columns = col)
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_welcome_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    text = "歡迎使用CalCal~卡路里計算機\n每天追蹤熱量並設計運動計畫吧\n" +\
              "輸入calcal開始使用，或直接輸入文字與後台人員溝通"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"



"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
