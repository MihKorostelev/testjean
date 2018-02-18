import secinfo
import datetime
from slackclient import SlackClient
import re

token = secinfo.API_Token
sc = SlackClient(token)
chan=secinfo.channel_id

def find_number_symbol_event(text,number_start,end,symbol):
    for i in range(number_start, end):
        if text [i] == symbol:
            number_search = i
            return number_search

def selection_word(text,start,end):
    word = ''
    for i in range(start, end):
        word +=text[i]
    return word

def selection_chan(i):
        try:
            text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
            text_string = text[i]
            if (len(text_string) != 1) and (len(text_string) != 2):
                chan = selection_word(text_string,0,9)
            else:
                chan = 'Void'
            return chan
        except IndexError:
            chan = 'Void'
            return chan

def selection_username(i):
    try:
        text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
        text_string = text[i]
        if (len(text_string) != 1) and (len(text_string) != 2):
            start_Name = text_string.find('@') + 1
            end_Name = text_string.find('about') - 1
            if '>' in text_string :
                end_Name = end_Name - 1
                start_Name = start_Name - 1
            username = selection_word(text_string,start_Name,end_Name)
            for j in range(0,len(secinfo.userId)):
                if(username == secinfo.userId[j]):
                    username = secinfo.userName[j]
        else:
            username = 'Void'
        return username
    except IndexError:
        username = 'Void'
        return username

def selection_eventname(i):
    try:
        text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
        text_string = text[i]
        if (len(text_string) != 1) and (len(text_string) != 2):
            start_event = text_string.find('"')
            end_event = find_number_symbol_event(text_string,start_event+1,len(text_string),'"') + 1
            eventname = selection_word(text_string,start_event,end_event)
        else :
            eventname = 'Void'
        return eventname
    except IndexError:
        eventname = 'Void'
        return eventname
    except TypeError:
        eventname = 'Void'
        return eventname

def selection_timename(i):
    try:
        text = open('/var/lib/jenkins/workspace/DevopsTest/Jean_bot/remindlist.txt').readlines()
        text_string = text[i]
        if len(text_string) > 2:
            time_start = text_string.find('at') + 3
            time_end = len(text_string)
            timename = selection_word(text_string,time_start,time_end)
        else :
            timename = '17:00 1.07.2017'
        return timename
    except IndexError:
        timename = '17:00 1.07.2017'
        return timename

def int_time(i):
    Date_time = selection_timename(i)
    time  = re.findall('(\d+)', Date_time)
    if ('a.m.' in  Date_time) or ('A.M.' in  Date_time):
        if ':' in Date_time:
            time_event = [int(time[0]),int(time[1])]
        else:
            time_event = [int(time[0]),0]
    elif ('p.m.' in  Date_time) or ('P.M.' in  Date_time):
        if ':' in Date_time:
            time_event = [int(time[0])+12,int(time[1])]
        else:
            time_event = [int(time[0])+12,0]
    else:
        if ':' in Date_time:
            time_event = [int(time[0]),int(time[1])]
        else:
            time_event = [int(time[0]),0]
    return time_event

def str_time(i):
    string = str(int_time(i)[0]) + ':' + str(int_time(i)[1])
    return string

def _date_start(i,format_time):
    try:
        Date_time = selection_timename(i)
        time  = re.findall('(\d+)', Date_time)
        time = [time[0],':' + time[1]]
        if format_time == 1:
            date_start = Date_time.find(time[format_time]) + 4
        else:
            date_start = Date_time.find(time[format_time]) + 3
        date_end = len(Date_time)
        datename = selection_word(Date_time,date_start,date_end)
        return datename
    except IndexError:
        datename = '1.07.2017'
        return datename

def str_date(i):
    try:
        Date_time = selection_timename(i)
        if ('a.m.' in  Date_time) or ('A.M.' in  Date_time) \
                or ('p.m.' in  Date_time) or ('P.M.' in  Date_time):
            date_start = Date_time.find('. ') + 2
            date_end = len(Date_time)
            datename = selection_word(Date_time,date_start,date_end)
        else:
            if ':' in Date_time:
                datename = _date_start(i, 1)
            else:
                datename = _date_start(i, 0)
        return datename
    except ValueError:
        datename = '1.07.2017'
        return datename

def weekday_today():
    now = datetime.datetime.now()
    return now.weekday()

def day_of_week_date(i):
    day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for j in range(0,7):
        if day_of_week[j] in str_date(i):
            if j >= weekday_today():
	               j - weekday_today()
            else:
	               j - weekday_today() + 7

def int_date(i):
    try:
        (day,month,year) = str_date(i).split('.')
        date_event = [int(year),int(month),int(day)]
        return date_event
    except ValueError:
        date_event = [2017,7,1]
        return date_event
