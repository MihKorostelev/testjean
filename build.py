import jenkins
import secinfo
import connect
import time
import status
from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def slack_build_job_jenkins(jobname):
    try:
        server = jenkins.Jenkins('http://jenkins.andersenlab.com', username=secinfo.username, password=secinfo.password)
        next_build_number = server.get_job_info(jobname)['nextBuildNumber']
        build_number = next_build_number - 1
        if(status.check_status_project(jobname) != 'In process, wait the end of build'):
            server.build_job(jobname, parameters=None, token = secinfo.API_Token)
            while(build_number==next_build_number-1):
                next_build_number = server.get_job_info(jobname)['nextBuildNumber']
        while(status.check_status_project(jobname) == 'In process, wait the end of build'):
            time.sleep(1)
        else :
            message = status.check_status_project(jobname)
    except jenkins.NotFoundException:
        message = 'Name of project is not right'
    return message

def build_project():
    message = open('write_chats.txt').readlines()
    text = ''
    chan = ''
    for i in range(0,len(message)):
        if 'build please' in message[i]:
            chan = connect.get_channel()
            text = message[i]
            connect.clear_write_chat()
    if(text != ''):
        if status.check_status_project(status.get_job(text)) != 'In process, wait the end of build' :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Build started now!')
        else :
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='build already start, please wait!')
        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=slack_build_job_jenkins(status.get_job(text)))

def infine_build():
    while(1):
        build_project()