
from slackclient import SlackClient
import re
import secinfo
token = secinfo.API_Token
sc = SlackClient(token)
chan=secinfo.channel_id

def verify_word(text,start,end):
    word = ''
    for i in range(start, end):
        word +=text[i]
    return word

def verify_username(i):
    try:
        text = open('write_chats.txt').readlines()
        text_string = text[i]
        if len(text_string) > 2:
            start_Name = text_string.find('@') + 1
            end_Name = text_string.find('about') - 1
            if '>' in text_string :
                end_Name = end_Name - 1
                start_Name = start_Name - 1
            username = verify_word(text_string,start_Name,end_Name)
            for j in range(0,len(secinfo.userId)):
                if (username == secinfo.userId[j]):
                    username = secinfo.userName[j]
        else:
            username = 'Void'
        return username
    except IndexError:
        username = 'Void'
        return username

def find_number_symbol_event(text,number_start,end,symbol):
    for i in range(number_start, end):
        if text [i] == symbol:
            number_search = i
            return number_search

def verify_eventname(i):
    try:
        text = open('write_chats.txt').readlines()
        text_string = text[i]
        if len(text_string) > 2:
            start_event = text_string.find('"')
            end_event = find_number_symbol_event(text_string,start_event+1,len(text_string),'"') + 1
            eventname = verify_word(text_string,start_event,end_event)
        else :
            eventname = 'Void'
        return eventname
    except IndexError:
        eventname = 'Void'
        return eventname
    except TypeError:
        eventname = 'Void'
        return eventname

def verify_timename(i):
    try:
        text = open('write_chats.txt').readlines()
        text_string = text[i]
        if len(text_string) > 2:
            time_start = text_string.find('at') + 3
            time_end = len(text_string)
            timename = verify_word(text_string,time_start,time_end)
        if not '@' in text_string:
            timename = 'Void'
        return timename
    except IndexError:
        timename = 'Void'
        return timename

def verify_int_time(i):
    try:
        Date_time = verify_timename(i)
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
    except IndexError :
        time_event = [25,61]
        return time_event

def date_start(i,format_time):
    try:
        Date_time = verify_timename(i)
        time  = re.findall('(\d+)', Date_time)
        if len(time) > 1:
            time = [time[0],':' + time[1]]
        else:
            time = [time[0],':00']
        date_start = Date_time.find(time[format_time]) + 4
        date_end = len(Date_time)
        datename = verify_word(Date_time,date_start,date_end)
        return datename
    except IndexError:
        datename = 'Void'
        return datename

def verify_str_date(i):
    try:
        Date_time = verify_timename(i)
        if ('a.m.' in  Date_time) or ('A.M.' in  Date_time) \
                or ('p.m.' in  Date_time) or ('P.M.' in  Date_time):
            _date_start = Date_time.find('. ') + 2
            date_end = len(Date_time)
            datename = verify_word(Date_time,_date_start,date_end)
        else:
            if ':' in Date_time:
                datename = date_start(i, 1)
            else:
                datename = date_start(i, 0)
        return datename
    except ValueError:
        datename = '1.07.2017'
        return datename

def verify_int_date(i):
    try:
        (day,month,year) = verify_str_date(i).split('.')
        date_event = [int(year),int(month),int(day)]
        return date_event
    except ValueError:
        date_event = [2017,7,1]
        return date_event

def verify_time_and_date(i):
    if (verify_int_date(i)[0] > 2019) or (verify_int_date(i)[1] > 12) or \
        (verify_int_date(i)[2] > 31) or (verify_int_time(i)[0]>23) or (verify_int_time(i)[1]>60):
        timename = 'Void'
    else:
        timename = verify_timename(i)
    return timename
