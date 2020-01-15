#!/usr/bin/env python3
# coding=utf-8
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from os import path
import os
import logging


class Mail(object):
    # mailbox setting
    local_dir = path.dirname(__file__)
    with open(os.path.join(local_dir, 'mailbox.txt'), 'r') as f:
        mail_setting = f.readlines()
    from_addr = mail_setting[0].strip()
    password = mail_setting[1].strip()
    smtp_server = mail_setting[2].strip()

    def __init__(self, text, sender, receiver, subject, address):
        self.text = text
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.address = address
        self.to_addr = address
        # From above to below: mail content, sender nickname, receiver nickname, subject
        self.msg = MIMEText(self.text, 'plain', 'utf-8')
        self.msg['From'] = self._format_addr(self.sender + '<' + self.from_addr + '>')
        self.msg['To'] = self._format_addr(self.receiver + '<' + self.to_addr + '>')
        self.msg['Subject'] = Header(self.subject, 'utf-8').encode()

    # format the email address
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self):
        # server = smtplib.SMTP(self.smtp_server, 25)  # 25 normal，465 SSL
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        # server.starttls()  # SSL required
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        try:
            server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
        except Exception:
            return False
        logging.info('----This email\'s info: %s, %s, %s', self.text, self.receiver, self.to_addr)
        server.quit()
        return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    send_email = Mail('test', 'wo', 'ni', 'test', 'xxxxxxx@qq.com')
    send_email.send()
