import secinfo
import connect
from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def request(string):
    num_start = string.find('change') + 18
    return string[num_start:len(string)]

def new_request(string):
    num_start = string.find('rechange') + 11
    return string[num_start:len(string)]

def all_strings(string):
    return_string = ''
    f = open('ask.txt').readlines()
    for i in range(0,len(f)):
        if string in f[i]:
            return_string = f[i][0:7]
            f[i] = ''
            fw = open('ask.txt','w')
            fw.writelines(f)
    return return_string

def change_request():
    message = open('write_chats.txt').read()
    num = 0
    oldpart = ''
    if "change my request" in message:
        message = request(message)
        chan = connect.get_channel()
        oldpart = all_strings(message)
        print(oldpart)
        if oldpart != '':
            sc.api_call('chat.postMessage', as_user='true:', channel=connect.get_channel(), text='Write new request')
            num = 1
        else :
            sc.api_call('chat.postMessage', as_user='true:', channel=connect.get_channel(), text='So request isn`t found')
            num = 3
        connect.clear_write_chat()
    while(num == 1):
        num = 2
    while(num == 2):
        new_message = open('write_chats.txt').read()
        if 'rechange to' in new_message:
            f = open('ask.txt','a')
            textwrite = '\n' + oldpart + new_request(new_message)
            f.write(textwrite)
            num = 3
            sc.api_call('chat.postMessage', as_user='true:', channel=connect.get_channel(), text='I change it')
            connect.clear_write_chat()

def infine_rechange_request():
    while(1):
        change_request()