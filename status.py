import jenkins
import secinfo
import connect
from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def get_job(text):
    name_job = ''
    number = 0
    for count in range(0,(len(text))):
        if text[count] == '@' :
            number = count
    for count in range(number+1,len(text)):
        name_job +=text[count]
    return name_job

def check_status_project(param):
    try:
      server = jenkins.Jenkins('http://jenkins.andersenlab.com', username=secinfo.username, password=secinfo.password)
      next_build_number = server.get_job_info(param)['nextBuildNumber']
      build_number = next_build_number - 1
      build_info = server.get_build_info(param, build_number)
      status = build_info.get('result')
      if status == None:
          status = 'In process, wait the end of build'
      else:
          status = 'Status is: '+ status.lower() + ', number of build is ' + str(build_number)
    except jenkins.NotFoundException:
        status = 'Name of project is not right'
    return status

def status_project():
    message = open('write_chats.txt').readlines()
    for i in range(0,len(message)):
        if 'what about' in message[i]:
            chan = connect.get_channel()
            text = message[i]
            connect.clear_write_chat()
            report = check_status_project(get_job(text))
            if report != 'Name of project is not right':
                report= 'status is ' + report
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=report)

def infine_status():
    while(1):
        status_project()
