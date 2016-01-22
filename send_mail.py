#!/usr/bin/env python
#-_- coding: utf-8 -_-
import smtplib
from email.Header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def sendMail(sender,reciver,subject):
    smtserver="mail.ag866.com"
    #username=""
    #password=""
    msg=MIMEMultipart("alternative")
    msg['Subject']=Header(subject,'utf-8')
    #html格式
    html="""\
    <html>
    <head>测试一下</head>
    <body>
    <p>来吧!<br>
    你们好啊<br>
    点击进入 <a href=" http://www.baidu.com ">百度搜索</a>
    <br><img src="cid:image1"></br>
    </p>
    </body>
    </html>
    """
    htm=MIMEText(html,'html','utf-8')
    msg.attach(htm)
    #构造图片
    fp=open('1.jpg','rb')
    msgImage=MIMEImage(fp.read())
    fp.close()
    msgImage.add_header("Content-ID", "<image1>")
    msg.attach(msgImage)
    #msg['From']="monitor@ag866.com"
    msg['To']=";".join(reciver)
    
    #发送邮件
    smtp=smtplib.SMTP()
    smtp.connect("mail.ag866.com")
    smtp.ehlo()
    smtp.starttls()
    #smtp.login(username, password)
    smtp.sendmail(sender, reciver, msg.as_string())
    smtp.quit()

if __name__=="__main__":
    sender="monitor@ag866.com"
    reciver=['Arno@ag866.com']
    subject="测试邮件"
    try:
        sendMail(sender, reciver, subject)
        print '发送成功'
    except Exception,e:
        print str(e)
