import smtplib
from datetime import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(from_who, to_list, subject, mail_host, mail_user, mail_pass, contents):
    me = mail_user
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_who
    msg['To'] = ",".join(to_list)

    d = datetime.now()
    timezone = d.strftime('%Y-%m-%d %H:%M:%S')

    # 构造html

    html = """
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <title>12306订票</title>
                <body>
                <div id="container">
                  <p><strong>订票结果通知</strong></p>
                  <p>订票成功时间: """ + timezone + """</p>
                  <div id="content">
                   <table width="500" border="2" bordercolor="red" cellspacing="2">               
        """
    page = ''
    for content in contents:
        page += \
            """
            <tr>
            <td> """ + str(content[0]) + """ </td>
            <td> """ + str(content[1]) + """ </td>
            <td> """ + str(content[2]) + """ </td>
            <td> """ + str(content[3]) + """ </td>
            <td> """ + str(content[4]) + """ </td>
            <td> """ + str(content[5]) + """ </td>
            </tr>
            """

    html += page + \
            """</table>
                  </div>
                </div>
                <p><strong>请尽快登录12306客户端，在30分钟内完成支付!!!</strong> </p>
                </div>
                </body>
                </html>
            """
    context = MIMEText(html, _subtype='html', _charset='utf-8')  # 解决乱码
    msg.attach(context)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host)
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(me, to_list, msg.as_string())
        send_smtp.close()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    # 设置服务器名称、用户名、密码以及邮件后缀
    mail_host = 'smtp.qq.com'
    mail_user = '*****@qq.com'
    mail_pass = '********'
    # mailto_lists = sys.argv[1]
    # mailto_list = mailto_lists.split(',')   #发送多人
    # sub= sys.argv[2]
    mailto_list = ['******@163.com']
    subject = "test"
    contents = []
    contents.append([1, 2, 3, 4, 5, 6])
    contents.append([2, 12, 13, 14, 15, 16])
    # send_mail(mailto_list, sub)
    if send_mail(mail_user, mailto_list, subject, mail_host, mail_user, mail_pass, contents):
        print("Send mail succed!")
    else:
        print("Send mail failed!")
