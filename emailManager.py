# -*- coding: utf-8 -*-
import smtplib
import datetime
from random import choice
from email.mime.text import MIMEText
from email.header import Header
from utils import logger
from os import listdir
from jinja2 import Template
from mailServer import MailServer
from translator import Translator



class EmailManager:
    def __init__(self, template_dir='templates', template_extension='.html', translator=None):
        logger('初始化邮件管理器...')
        self.send_success = 0
        self.send_failed = 0
        self.template_dir = template_dir
        self.template_extension = template_extension
        self.templates = {}
        self.mail_servers = []
        self.init_servers()
        self.init_templates()
        self.translator = translator or Translator()
        logger('初始化邮件管理器..成功!')
        
    
    def init_servers(self):
        self.mail_servers = [
            MailServer('aliyun', 'your(sender)@email.com', 'password', 'smtpdm.aliyun.com', 80),
            MailServer('tencent_company', 'your(sender)@email.com', 'password', 'smtp.exmail.qq.com', 465)
        ]
        logger('初始化邮件服务器({})..成功!'.format(len(self.mail_servers)))
        

    def init_templates(self):
        templates = {}
        count = 0
        for fileName in listdir(self.template_dir):
            if self.template_extension in fileName:
                with open('{}/{}'.format(self.template_dir, fileName), 'r', encoding='utf-8') as template_file:
                    templates[fileName.replace(self.template_extension, '')] = Template(template_file.read())
                    count += 1
        self.templates = templates
        logger('初始化邮件模板({})..成功!'.format(count))
    
     
    def send_mail(self, recipient, title, content, sender_name='', server_name='', template_data={}, lang='cn', tried_servers=[]):
        send_status = -1
        tried_servers_temp = tried_servers if len(tried_servers) > 0 else []
        self.translator.language = lang
        if len(tried_servers) == len(self.mail_servers):
            logger('已达到最大重试次数..放弃此次发信任务！')
            return send_status, self.translator.tran('mail.errors.service_unavailable')
        
        if server_name: 
            server = [s for s in self.mail_servers if s.name == server_name][0]
        else: 
            if len(tried_servers) > 0: 
                logger('发信失败，更换服务器重试... [当前重试次数({})]'.format(len(tried_servers_temp)))
                server = [s for s in self.mail_servers if s.name not in tried_servers][0] 
            else: server = self.mail_servers[0]
            
        client = smtplib.SMTP_SSL(host=server.host) if server.port == 465 or server.client_type == 'ssl' else smtplib.SMTP(host=server.host)
        temp = self.templates.get(content)
        if temp != None:
            content = self.template_render(temp, template_data)
        
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = '{} <{}>'.format(sender_name or server.sender_name, server.account)
        msg['To'] = '{} <{}>'.format('osu!Kafuu User', recipient)
        msg['Reply-to'] = server.reply_address
        
        try:
            client.connect(server.host, server.port)
            client.login(server.account, server.password)
            client.sendmail(server.account, [recipient], msg.as_string())
            client.quit()
            send_status = 1
            re_msg = self.send_complete(server, recipient, status=1)
            
        except smtplib.SMTPConnectError as err:
            re_msg = self.send_complete(server, recipient, self.send_error(0), error=err)
        except smtplib.SMTPAuthenticationError as err:
            re_msg = self.send_complete(server, recipient, self.send_error(1), error=err)
        except smtplib.SMTPSenderRefused as err:
            re_msg = self.send_complete(server, recipient, self.send_error(2), error=err)
        except smtplib.SMTPRecipientsRefused as err:
            re_msg = self.send_complete(server, recipient, self.send_error(3), error=err)
        except smtplib.SMTPDataError as err:
            re_msg = self.send_complete(server, recipient, self.send_error(4), error=err)
        except smtplib.SMTPException as err:
            re_msg = self.send_complete(server, recipient, self.send_error(5, reason=err), error=err)
        except Exception as err:
            re_msg = self.send_complete(server, recipient, self.send_error(5, reason=err), error=err)
        
        if send_status == -1:
            tried_servers_temp.append(server.name)
            send_status, re_msg = self.send_mail(recipient, title, content, sender_name, server_name, template_data, lang, tried_servers_temp)
        
        return send_status, re_msg
    
    
    def send_error(self, error_num, reason=''):
        errors = [
            'mail.errors.connection',
            'mail.errors.authentication',
            'mail.errors.sender_rejected',
            'mail.errors.recipient_rejected',
            'mail.errors.data_reception_rejected',
             str(reason)
        ]
        return self.translator.tran(errors[error_num])
    
    
    def send_complete(self, server, recipient, error_text='', status=-1, error=None):
        if status == 1:
            self.send_success += 1
            logger('邮件发送成功 (server [{}] to {}) 成功({}) [{}]'.format(server.name, recipient, self.send_success, self.translator.language))
            return self.translator.tran('mail.complete.success')
        else:
            self.send_failed += 1
            logger('邮件发送失败 (server [{}] to {}) [{}] ({}) 失败({}) [{}]'.format(server.name, recipient, error_text, str(error), self.send_failed, self.translator.language))
            return self.translator.tran('mail.complete.failed') + error_text


    def template_render(self, temp, template_data={}):
        themes = {
            'purple': ['#EDE7F6', '#7E57C2', '#673AB7'],
            'pink': ['#FCE4EC', '#EC407A', '#E91E63'],
            'blue': ['#E3F2FD', '#42A5F5', '#2196F3'],
            'indigo': ['#E8EAF6', '#5C6BC0', '#3F51B5'],
            'green': ['#E8F5E9', '#66BB6A', '#4CAF50'],
            'orange': ['#FFF3E0', '#FFA726', '#FF9800'],
            'teal': ['#E0F2F1', '#26A69A', '#009688']
        }
        temp.globals['tran'] = self.translator.tran
        template_data['theme_color'] = themes[choice(list(themes.keys()))]
        template_data['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' GMT.'
        template_data['adminmail'] = 'example@email.com'
        return temp.render(**template_data)
    
    
if __name__ == '__main__':
    service = EmailManager()
        
