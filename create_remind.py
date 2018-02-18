import secinfo
import datetime
import re
import status
import verify
import connect
from slackclient import SlackClient
token = secinfo.API_Token
sc = SlackClient(token)

def count_day(month):
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        counts_day = 31
    elif month == 2:
        counts_day = 28
    else:
        counts_day = 30
    return counts_day

def weekday_today():
    now = datetime.datetime.now()
    return now.weekday()

def format_date(string):
    _time_now = str(datetime.datetime.now().date())
    _time_now = _time_now[0:10]
    (year_now, month_now, day_now) = _time_now.split('-')
    year_now = int(year_now)
    day_now = int(day_now)
    month_now = int(month_now)
    if 'p.m.' in string:
        time  = re.findall('(\d+)', string)
        time_replace = time[0] + ':'
        time_null = str(int(time[0])+12) + ':'
        string = string.replace(time_replace, time_null)
        string = string.replace(' p.m.', '')
    if 'a.m.' in string:
        string = string.replace(' a.m.', '')
    if 'at' in string:
        date_event = ''
        string = string.replace('at', date_event)
    if 'tommorow' in string:
        if day_now >= count_day(month_now):
            month_now = str(int(month_now)+1)
            day_now = 1
        else :
            day_now = int(day_now) + 1
        date_event = str(day_now)+'.'+str(month_now)+'.'+str(year_now)
        string = string.replace('tommorow', date_event)
    elif 'today' in string:
        date_event = str(day_now)+'.'+str(month_now)+'.'+str(year_now)
        string = string.replace('today', date_event)
    elif ('monday' in string) or \
        ('tuesday' in string) or \
        ('wednesday' in string) or \
        ('thursday' in string) or \
        ('friday' in string) or \
        ('saturday' in string) or \
        ('sunday' in string):
        day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for j in range(0,7):
            if day_of_week[j] in string:
                name_day = day_of_week[j]
                if j >= weekday_today():
                    dweek = j - weekday_today()
                else:
                    dweek = j - weekday_today() + 7
        dweek = dweek + int(day_now)
        if count_day(int(month_now)) < dweek:
            day_now = dweek - count_day(int(day_now))
            date_event = str(day_now)+'.'+str(month_now + 1)+'.'+str(year_now)
            string = string.replace(name_day, date_event)
        else:
            day_now = dweek
            date_event = str(day_now)+'.'+str(month_now)+'.'+str(year_now)
            string = string.replace(name_day, date_event)
    return string

def write_remindlist():
    text = ''
    send = ''
    job = ''
    chan = connect.get_channel()
    file3 = open('remindlist.txt').read()
    file1 = open('write_chats.txt').readlines()
    file2 = open('remindlist.txt','a')
    for i in range(0,len(file1)):
        try :
            if ' remind' in file1[i]:
                text = file1[i]
                job = status.get_job(text)
                number_start = job.find('at') + 3
                number_end = len(job)
                noformat_job = job[0:number_start]
                format_job = job[number_start:number_end]
                if  not ':' in job:
                    time  = re.findall('(\d+)', format_job)
                    time_replace = time[0] + ':' + '00'
                    format_job = format_job.replace(time[0], time_replace)
                    job = noformat_job+format_job
                if ('every' in job):
                    if 'p.m.' in job :
                        time  = re.findall('(\d+)', format_job)
                        time_replace = time[0] + ':'
                        time_null = str(int(time[0])+12) + ':'
                        format_job = format_job.replace(time_replace, time_null)
                        format_job = format_job.replace('p.m.', '')
                        job = noformat_job+format_job
                    if 'a.m.' in job:
                        job = job.replace('a.m.', '')
                        job = '@' + job
                else:
                    format_job = format_date(format_job)
                    job = '@' + noformat_job+format_job
                if job in file3:
                    send = 'So remind already has in remindlist'
                    sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=send)
                else :
                    if(verify.verify_username(i) == 'Void') or \
                        (verify.verify_eventname(i) == 'Void') or (verify.verify_time_and_date(i) == 'Void'):
                        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Incorrect data')
                    else :
                        if 'channel' in verify.verify_username(i) :
                            send = 'Okay, i will remind '+ '<!channel>'
                        elif '@' in verify.verify_username(i) :
                            send = 'Okay, i will remind '+ '<' + verify.verify_username(i) + '>'
                        else :
                            send = 'Okay, i will remind '+ verify.verify_username(i)
                        file2 = file2.write(chan + ' ' + job + '\n')
                        sc.api_call('chat.postMessage', as_user='true:', channel=chan, text=send)
                connect.clear_write_chat()
        except IndexError:
            sc.api_call('chat.postMessage', as_user='true:', channel=chan, text='Incorrect time')
            connect.clear_write_chat()

def infine_create_remind():
    while(1):
        write_remindlist()