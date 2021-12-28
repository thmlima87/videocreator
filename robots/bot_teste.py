#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import find_subject as fs
import time
import yaml
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# pegando as credenciais das apis
with open("credentials.yml","r") as c:
    try:
        credentials = yaml.safe_load(c)
    except yaml.YAMLError as exc:
        print(exc)

bot = telebot.TeleBot(credentials['telegram_bot_api_token'])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


##############################################################################################
'''
GOOGLE TRENDS
'''
##############################################################################################
@bot.message_handler(commands=['getgoogletrends'])
def send_googletrends(message):
    #bot.reply_to(message,"Opa... pera ai só um pouquinho q vou dar uma olhada...")
    # buscando os trending topics
    # google
    bot.send_message(message.chat.id, "Opa... guenta ai... \nOs assuntos mais pesquisados no Google são:!!!...")

    gcontent = fs.getGoogleTrends()
    time.sleep(3)
    #bot.send_message(message.chat.id, fs.formatMessageFromGoogleToTelegram(gcontent))
    counter = 1
    for i in gcontent:
        if counter <= 10:
            bot.send_message(message.chat.id, "{}) {}".format(counter, i['title']))
        counter+=1

##############################################################################################
'''
TWITTER TRENDS
'''
##############################################################################################
@bot.message_handler(commands=['gettwittertrends'])
def send_twittertrends(message):
    #bot.reply_to(message,"Opa... pera ai só um pouquinho q vou dar uma olhada...")
    # buscando os trending topics
    # google
    bot.send_message(message.chat.id, "Opa... guenta ai... \nOs 3 assuntos mais falados no Twitter no dia de hoje!!!...")

    tcontent = fs.getTwitterTrends()
    time.sleep(5)
    bot.send_message(message.chat.id, fs.formatMessageFromTwitterToTelegram(tcontent))


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    #bot.reply_to(message, message.text)
    #bot.send_message(message.chat.id, message)
    msg = message.text
    
    if msg.lower() in ["olá", "ola", "oi", "buenas", "bom dia", "boa tarde", "boa noite"]:
        msg_callback = "E aeee {} :D". format(message.from_user.first_name)
        bot.send_message(message.chat.id, msg_callback)
    else:
        bot.send_message(message.chat.id, message)



bot.polling()
