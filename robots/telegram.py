import requests
import xmltodict
import json
import datetime
import util
import logging

def formatMessageFromGoogleToTelegram(content):
    msg = "1) {}\n2) {} \n3) {}".format(content[0]['title'], content[1]['title'], content[2]['title'])
    return msg

def formatMessageFromTwitterToTelegram(content):
    msg = "1) {}\n2) {} \n3) {}".format(content[0]['name'], content[1]['name'], content[2]['name'])
    return msg