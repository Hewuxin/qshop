import smtplib
from email.mime.text import MIMEText

subject = "今日份快乐"
content = "学习了怎么用python发邮件"
sender = "xxxxxx@163.com"
recver = """yummysama@qq.com"""
password = "xxxxxx"

message = MIMEText(content,'plain','utf-8')

"""
_text,邮件内容
_subtype='plain',内容类型，文本
_charset=None, 字符编码 utf8
"""

message["Subject"]=subject
message["From"]=sender
message["To"]=recver

smtp=smtplib.SMTP_SSL("smtp.163.com",465)

smtp.login(sender,password)
smtp.sendmail(sender,recver.split(","),message.as_string())

smtp.close()
