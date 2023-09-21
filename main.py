import json  # json 解析
from datetime import datetime, timedelta
import requests  # http 请求库

id = '<your id>'  # 学号
pwd = '<your password>'  # 密码，默认是你的学号（不会和数字石大一起改变！！！）
semester = '2023-2024-1'  # 学期
firstDay = datetime(2023,9,3)   #学期开始时间 具体时间可以查看校历
########################
# 填写账号密码
########################

def get_token():
    loginLink = "http://jwxt.upc.edu.cn/app.do?method=authUser&xh=" + id + "&pwd=" + pwd
    rep = requests.get(loginLink)
    res = json.loads(rep.text)
    # 使用账号密码换取网站 token
    return res["token"]
def get_classes(week = '1',token=''):
    tableUrl = "http://jwxt.upc.edu.cn/app.do?method=getKbcxAzc&xh=" + id + "&xnxqid=" + semester + "&zc=" + week
    header = {
        "token": token,  # 传入 token ，鉴权
        'User-Agent': 'Mozilla/5.0 (Linux; U; Mobile; Android 6.0.1;C107-9 Build/FRF91 )',
        'Referer': 'http://www.baidu.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
        'cache-control': 'max-age=0'
    }
    res = requests.get(url=tableUrl, headers=header)
    schedule = json.loads(res.text)  # 读取课表 json
    return schedule
def init_icsfile():
    f = open('classtable.ics', 'w', encoding='utf-8')
    f.write(u"BEGIN:VCALENDAR\nVERSION:2.0\n")
    return f
def add_icsfile(name,location,start_time,end_time,f):
    f.write('BEGIN:VEVENT' + '\n')
    f.write('DTSTART:' + start_time+ '\n')
    f.write('DTEND:' + end_time+ '\n')
    f.write('SUMMARY:' + name+'\n')
    f.write('LOCATION:' + location +'\n')
    f.write("END:VEVENT" + '\n')
def close_icsfile(f):
    f.write(u"END:VCALENDAR")
    f.close()

def get_time(week,time,day):
    s = time.split(':')
    #eventdate = firstDay + timedelta(days=7 * (week - 1) + int(day),hours=int(s[0]) - 8,minutes=int(s[1]))
    #如果使用vivo的安卓手机，导入的日程会被认为是GMT时间。所以，如果是vivo用户则可以取消注释上面的，然后注释下面的
    eventdate = firstDay + timedelta(days=7 * (week - 1) + int(day), hours=int(s[0]), minutes=int(s[1]))
    return eventdate.strftime('%Y%m%dT%H%M%S')

def addclassevents(maxweek = 18):
    file = init_icsfile()
    token_string = get_token()
    for i in range(1,maxweek + 1):
        sch = get_classes(str(i),token_string)
        for event in sch:
            start = get_time(day=event['kcsj'][0],time=event['kssj'],week=i)
            end = get_time(day=event['kcsj'][0], time=event['jssj'], week=i)
            add_icsfile(name=event['kcmc'],location=event['jsmc'],start_time=start,end_time=end,f=file)
    close_icsfile(file)
if __name__ == '__main__':
    addclassevents()

