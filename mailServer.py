# -*- coding: utf-8 -*-
from utils import logger


class MailServer:
    def __init__(self, name, account, password, host, port, sender_name='osu!Kafuu', client_type='default', reply_address=None):
        self.name = name
        self.account = account
        self.password = password
        self.host = host
        self.port = port
        self.sender_name = sender_name
        self.client_type = client_type
        self.reply_address = reply_address or account
        logger('增加邮件服务器：{} <{}>'.format(name, account))


if __name__ == '__main__':
    server = MailServer()