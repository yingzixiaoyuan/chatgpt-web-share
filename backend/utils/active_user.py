import base64
import smtplib
import time
from email.message import EmailMessage

import api.globals as g
from authlib.jose import JoseError, jwt

config = g.config

def generate_token(user_id:int):
    """生成用于邮箱验证的JWT（json web token）"""
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = config.get("user_secret")
    # 待签名的数据负载
    data = {'id': user_id, 'exp': time.time() + 180}
    return base64.b64encode(jwt.encode(header=header, payload=data, key=key))
    # return jwt.encode(header=header, payload=data, key=key)
    
def validate_token(token):
    """用于验证用户注册和用户修改密码或邮箱的token, 并完成相应的确认操作"""
    key = config.get("user_secret")
    token = base64.b64decode(token.encode("utf-8"))
    try:
        data = jwt.decode(token, key)
        if data.get("exp") < time.time():
            print("get data",data)
            return data.get("id")
            # return True
        return data.get("id")
    except JoseError:
        return False

def sendMail(receiver_email: str,user_id:int):
    # s = Serializer(config.get("user_secret"), 86400)
    data = generate_token(user_id)
    token = data.decode()
    print(token)
    activation_link = f"{config.get('frontend_url')}/activate/{token}"
    # 定义相关数据,请更换自己的真实数据
    smtpserver = 'smtp.163.com'
    sender = '13522198374@163.com'
    password = 'xiaoyuan234'
    msg = EmailMessage()
    msg.set_content(f"请点击以下链接激活您的账号：\n\n{activation_link}")

    msg["Subject"] = "激活您的账号"
    msg["From"] = sender
    msg["To"] = receiver_email
    # 登陆并发送邮件
    try:
        smtp = smtplib.SMTP()
        ##打开调试模式
        # smtp.set_debuglevel(1)
        smtp.connect(smtpserver)
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver_email, msg.as_string())
    except:
        print("邮件发送失败！！")
    else:
        print("邮件发送成功")
    finally:
        smtp.quit()

