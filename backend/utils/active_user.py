import asyncio
import base64
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
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
    data = {'id': user_id, 'exp': time.time() + 86400}
    return base64.b64encode(jwt.encode(header=header, payload=data, key=key))
    
def validate_token(token):
    """用于验证用户注册和用户修改密码或邮箱的token, 并完成相应的确认操作"""
    key = config.get("user_secret")
    token = base64.b64decode(token.encode("utf-8"))
    try:
        data = jwt.decode(token, key)
        if data.get("exp") < time.time():
            return False
        return data.get("id")
    except JoseError:
        return False

async def sendMail(receiver_email: str,user_id:int):
    data = generate_token(user_id)
    token = data.decode()
    activation_link = f"{config.get('frontend_url')}/activate/{token}"
    # 定义相关数据,请更换自己的真实数据
    smtpserver = config.get("smtpserver")
    sender = config.get("sender")
    password = config.get("password")
    msg = MIMEMultipart("alternative")
    # msg.set_content(f"请点击以下链接激活您的账号(有效期一天)：\n\n{activation_link}")
    html = f"""\
    <html>
    <body>
        <p>Hi,请点击以下链接激活您的账号(有效期一天):<br>
        <a href="{activation_link}">激活链接</a>
        </p>
    </body>
    </html>
    """
    html_part = MIMEText(html, "html")
    msg["Subject"] = "激活您的账号"
    msg["From"] = sender
    msg["To"] = receiver_email
    msg.attach(html_part)
    # 登陆并发送邮件
    try:
        async with aiosmtplib.SMTP(hostname=smtpserver, port=587, use_tls=True) as smtp:
            await smtp.login(sender, password)
            await smtp.send_message(msg)
            print(f"邮件{receiver_email}发送成功")
    except aiosmtplib.SMTPException as e:
        print(f"邮件{receiver_email}发送失败！！",e)

