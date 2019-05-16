from twilio.rest import Client

def send_sms(account_sid,auth_token,from_man,to_man,msg):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=to_man,
        from_=from_man,
        body=msg)
    return message.sid

if __name__ == '__main__':
    # Your Account SID from twilio.com/console
    account_sid = "BC8473842717d4daa96bf8b611fd311f77"
    # Your Auth Token from twilio.com/console
    auth_token = "1b80jdkg15572c2901a6471ff1f59e6a"
    from_num = '(731) 711-9418'
    to_num = '+8617269512465'
    msg = 'hello world'
    send_sms(account_sid,auth_token,from_num,to_num,msg)