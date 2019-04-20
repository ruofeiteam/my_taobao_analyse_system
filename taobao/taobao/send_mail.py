from MyModel.models import Mail
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os, configparser


def send(taobao_id, mail):
    # 读config.ini文件
    dir_now = os.path.dirname(__file__)
    conf = configparser.ConfigParser()
    conf.read(dir_now + '/config.ini')

    my_sender = conf.get('mail', 'user')  # 发件人邮箱账号
    my_pass = conf.get('mail', 'passwd')  # 发件人邮箱密码(当时申请smtp给的口令)
    my_user = mail  # 收件人邮箱账号，我这边发送给自己

    def mail():
        ret = True
        try:
            text = "您的分析已完成，请点击链接以查看结果：http://127.0.0.1:8000/analyse/?taobao_id=" + taobao_id
            msg = MIMEText(text, 'plain', 'utf-8')
            msg['From'] = formataddr(["陈怡", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["everyone", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "分析结果-提醒"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret

    ret = mail()
    if ret:
        print("邮件发送成功")
        Mail.objects.filter(taobao_id=taobao_id).delete()
    else:
        print("邮件发送失败")


def get_mail(taobao_id):
    # 根据id查邮箱
    mail = Mail.objects.filter(taobao_id=taobao_id)

    for e in mail:
        print(e.mail)
        send(taobao_id, e.mail)
