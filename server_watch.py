import jenkins
import secinfo
import time
import os
import build
import status
import connect
from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def ping_the_server(hostname):
    if not(('@' in hostname) or (';' in hostname) or ('&' in hostname) or ('|' in hostname)):
        response = os.system("ping " + hostname)
        if response == 0:
            message = 'server is up!'
        else :
            message = 'server is down!'
        return message

def get_server_and_job(text):
    job = ''
    url = ''
    server_and_job=[]
    number = text.find('it is')
    for i in range(0,number):
        url += text[i]
    for i in range(number+6, len(text)):
        job += text[i]
    server_and_job=[url,job]
    print(server_and_job)
    return server_and_job

def eye_on_server():
    message = open('write_chats.txt').readlines()
    for i in range(0,len(message)):
        if 'watching to' in message[i]:
            text = message[i]
            chan = connect.get_channel()
            job = status.get_job(text)
            connect.clear_write_chat()
            if (status.check_status_project(get_server_and_job(job)[1]) == 'Name of project is not right'):
                 sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Name of project is not right')
            else :
                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Ok, i will keep an eye on it')
                while(ping_the_server(get_server_and_job(job)[0]) != 'server is down!'):
                    for i in range(0,600):
                        stopfile = open('stop.txt').read()
                        if(stopfile != ''):
                            if 'stop it' in stopfile:
                                sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Ok, i end watching on server')
                                return True
                        else:
                            time.sleep(0.1)
                else :
                    job_Name = get_server_and_job(job)[1]
                    build_or_nothing(job_Name,get_server_and_job(job)[0],chan)
                    connect.clear_write_chat()

def command_stop_watching():
    number = 0
    message = open('write_chats.txt').read()
    stopfile = open('stop.txt', 'w')
    if(message != ''):
        if 'stop watching' in message:
            text = 'stop it'
            file_stop = stopfile.write(text)
            connect.clear_write_chat()

def build_or_nothing(job,server,chan):
    if(status.check_status_project(job) != 'In process, wait the end of build') :
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='I can`t reach ' + server + ', but it`s not building, maybe i need to rebuild it?')
        while(command_yes(job,chan) != 2):
            command_yes(job,chan)

def command_yes(job,chan):
    number = 0
    data = open('lol.txt').read()
    if(data != ''):
        if 'yes' in data:
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Build is started')
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=build.slack_build_job_jenkins(job))
            connect.clear_write_chat()
            number = 2
            return number
        elif 'no' in data :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Okay, then i finish work')
            number = 2
            connect.clear_write_chat()
            return number
    else :
        return number

def infine_monitor_server():
    while(1):
        eye_on_server()