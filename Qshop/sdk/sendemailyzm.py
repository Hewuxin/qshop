import smtplib
from email.mime.text import MIMEText


def sendemail(parmas):
    """
    parmas={
        "subject":"天天生鲜注册验证"，
        "content":"天天生鲜注册【验证码：1234】"，
        "recver":"xxxxxx"

    }
    :param parmas:
    :return:
    """
    subject = parmas.get("subject")
    content = parmas.get("content")
    sender = "py_daxinzang@163.com"
    recver = parmas.get("recver")
    password = "heyuyang12"

    message = MIMEText(content, 'plain', 'utf-8')

    """
    _text,邮件内容
    _subtype='plain',内容类型，文本
    _charset=None, 字符编码 utf8
    """

    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recver

    smtp = smtplib.SMTP_SSL("smtp.163.com", 465)

    smtp.login(sender, password)
    smtp.sendmail(sender, recver.split(","), message.as_string())

    smtp.close()
