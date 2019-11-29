from twilio.rest import Client

def send_sms(account_sid,auth_token,from_man,to_man,msg):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=to_man,
            from_=from_man,
            body=msg)
        if not message:
            return None
    except Exception as e:
        return None
    return message.sid

if __name__ == '__main__':
    from configure import ACCOUNT_SID,AUTO_TOKEN,FROM_NUM,TO_NUM
    msg = '测试一下，亲爱的路人'
    send_sms(ACCOUNT_SID,AUTO_TOKEN,FROM_NUM,TO_NUM,msg)