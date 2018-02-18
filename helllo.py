import secinfo
import connect
from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def command_hello():
    message = open('write_chats.txt').read()
    if 'hi jean' in message:
        sc.api_call('chat.postMessage', as_user='true:', channel=connect.get_channel(),text="hello, if you need help, use command help")
        connect.clear_write_chat()

def infine_hello():
    while(1):
        command_hello()



