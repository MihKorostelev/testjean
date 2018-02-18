import secinfo
from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def clear_write_chat():
    f = open('write_chats.txt','w')
    f.close()

def get_channel():
    message = open('write_chats.txt').read()
    if message != '':
        chan = ''
        for i in range(0,9):
            chan = chan + message[i]
        return chan

def connect():
    sc.rtm_connect()
    while(1):
        input = sc.rtm_read()
        if input:
            for action in input:
                if 'user' in action:
                    if action['user'] != 'U704DMX8U':
                        if 'type' in action and action['type'] == "message" :
                            username = action['user']
                            report = action['text']
                            channel = action['channel']
                            report = str(channel) + ' ' + report
                            if '@me' in report:
                                report = report.replace('@me','<@'+ username + '>')
                            if ('@all' in report):
                                report = report.replace('@all','<!@channel>')
                            f = open('write_chats.txt','a')
                            f.writelines(report)
                            f.close()



def infine_connect():
    while(1):
        connect()

