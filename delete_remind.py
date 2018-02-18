import secinfo
import datetime
import re
import remind_function
import status
import connect
import schedule
import create_remind
import schedule

from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def delete_remind():
    text = ''
    number = 0
    send = 'Sorry, i don`t remind you at that time'
    job = ''
    chan = connect.get_channel()
    file1 = open('write_chats.txt').readlines()
    file2 = open('remindlist.txt').readlines()
    connect.clear_write_chat()
    for i in range(0,len(file1)):
        if 'stop_remind' in file1[i]:
            number = 5
            text = file1[i]
            job = status.get_job(text)
            if ('every' in job):
                if 'a.m.' in job:
                    job = job.replace('a.m.', '')
            else:
                number_start = job.find('at') + 3
                number_end = len(job)
                noformat_job = job[0:number_start]
                format_job = job[number_start:number_end]
                format_job = create_remind.format_date(format_job)
                job = noformat_job+format_job
            for i in range(0,len(file2)):
                if job in file2[i]:
                    file3 = open('remindlist.txt','w')
                    send = 'Okay, i stop to remind you about this'
                    text = file2[i]
                    text = text.replace(job, '')
                    file2[i] = text
                    file3 = file3.writelines(file2)
                    if 'every' in file2[i]:
                        remind_function.refresh_remind()
                        remind_function.shed_date_final()
        if (number == 5):
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=send)

def infine_delete_remind():
    while(1):
        delete_remind()
        schedule.run_all()