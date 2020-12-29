"""
# File: $bingxiansheng
"""
import random

import requests
import time
import schedule
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def requests_fun():
    res = requests.get('http://www.weather.com.cn/weather1d/101010100.shtml')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    tianqi = soup.find('input', id='hidden_title')['value']
    chuanyi = soup.find('li', id='chuanyi').find('p').text
    return (tianqi, chuanyi)


def selenium_fun():
    driver = webdriver.Chrome()
    driver.get('http://www.weather.com.cn/weather1d/101010100.shtml')
    time.sleep(2)
    tianqi = driver.find_element_by_id('hidden_title').get_attribute('value')
    chuanyi = driver.find_element_by_id('chuanyi').find_element_by_tag_name('p').text
    return str(tianqi, chuanyi)
    driver.close()


def mail_fun(tianqi, chuanyi, zhuti):
    """
    配置邮你邮箱的各种信息，此处填写好个人的
    """
    mail_user = 'xxxxxx@qq.com'  # 发件人游戏
    mail_pwd = 'xxxxx'  # 密码，POP3/SMTP服务用那个码登录安全
    receiver = 'xxxxx@qq.com'  # 收件人邮箱
    subject = zhuti
    #  这里面是甜言蜜语库，每天从里面随机发一条
    love_content = ['今天也是元气满满的一天哦，乖乖听话，爱你~', '特别的爱，给特别的你~',
                    '乖乖你最漂亮了~', '生活很平淡也很苦，加上你，就足够甜了', '每天都有好心情',
                    '你是电，你是光，你是我的妞妞~', '自从遇见你，人生苦短甜长~',
                    '严于律己，甜以待你~', '我尝遍世间所有的糖果，却没有一种能带给我思念你时的甜蜜',
                    '去见你的路上，阳光温柔云朵可爱，就连风吹过来都是甜的', '我想亲你一口，就一小口',
                    '苦尽甘来，所以，你来了', '最近我牙齿痛，因为总是想你，那感觉太甜蜜，于是蛀牙了',
                    '如果我能拥有超能力，就把你心里的悲伤难过不开心打包扔掉，再放点糖进去',
                    '你的目光再温柔一点，月亮会融化，我也会', '在我身边你不用长大!', '温柔踩着清风，云朵贩卖着可爱，空气中充满了从你身上散发的甜甜的味道!',
                    '世间最烈的春药，是你低头含羞的温柔', '和你有关的念头总是太软，我总要轻拿轻放，就像睫毛上落了雪，舌尖上含着露水，手心里握着蝴蝶',
                    '采满这世间的温柔 与明月同赠于你~', '拥抱这个词真美好，我的手臂弯成一个温柔广阔的圈，把你拥在怀中，虽然没有亲吻来得那么绵长热烈，却让我感到特别安心',
                    '别人用温柔形容一个女生，而我用你来形容温柔', '见过比你美的，没见过比你美好的', '月色与雪色之间，你是第三种绝色',
                    '我把对你的喜欢揉碎，藏在对你讲的每一句话里', '要趁你在阳光下迷的睁不开眼睛时，偷亲你一下', '你是我日复一日的梦想',
                    '遇见你之后，感觉自己变成了一瓶可乐，一下被拧开，全身都冒着幸福的小泡泡', '人分为两类，是你和不是你。时间分为两段，你在的时候和你不在的时候',
                    '遇见你这么美好的事情，就像森林拥抱风声，黑夜与星星缠绵', '我已见过银河，但我只爱你这一颗']

    content = tianqi + '\t' + chuanyi + str(random.sample(love_content, 1))

    alimail = smtplib.SMTP()
    alimail.connect('smtp.qq.com', 25)
    alimail.login(mail_user, mail_pwd)

    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = Header(mail_user, 'utf-8')
    message['To'] = Header(receiver, 'utf-8')

    alimail.sendmail(mail_user, receiver, message.as_string())
    alimail.quit()


def main_fun():
    tianqi, chuanyi = requests_fun()
    zhuti = '【吱哥天气早报】    ' + time.ctime()
    mail_fun(tianqi, chuanyi, zhuti)
    print(zhuti)


schedule.every().day.at('05:40').do(main_fun)  # 定时任务 每天早上5：40发送


while True:
    schedule.run_pending()
    time.sleep(1)
