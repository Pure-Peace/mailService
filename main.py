# -*- coding:utf-8 -*-
'''
@author: PurePeace
@name: 邮件服务
@version: 0.3.0
@time: 2020-05-24
'''
from emailManager import EmailManager
from translator import Translator


class Handlers:
    def __init__(self):
        self.translator = Translator()
        self.mailService = EmailManager(translator=self.translator)
    
    def reg_success(self, data, recipient, lang='cn'):
        self.translator.language = lang
        title = self.translator.tran('main.reg_success_title').format(data['username'])
            
        return self.mailService.send_mail(recipient, title, content='reg_success', template_data=data, lang=lang)


h = Handlers()


if __name__ == '__main__':
    # send mail to your@email.com
    h.reg_success({'username': 'test', 'usermail': 'your@email.com'}, 'your@email.com')
    h.reg_success({'username': 'test', 'usermail': 'your@email.com'}, 'your@email.com', 'en')
    