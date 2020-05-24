# -*- coding: utf-8 -*-
'''
@name: simple web api
@author: PurePeace
'''
import time
from flask import Flask
from flask import request
import main

app = Flask('simple_api')

@app.route('/')
def index():
    return '''
        Welcome！<br>
        
        you can access this: http://localhost:8898/send_mail/reg_success/youremail@email.com/test <br><br>
        
        or select email language <br><br>
        
        http://localhost:8898/send_mail/reg_success/youremail@email.com/test?lang=en
    '''

@app.route('/send_mail/<content>/<recipient>/<username>')
def send_mail(content, recipient, username):
    lang = request.args.get('lang', 'cn')
    # send mail
    result = h.reg_success({'username': username, 'usermail': recipient}, recipient, lang)
    return { 'status': result[0], 'info': result[1], 'recipient': recipient, 'time': time.time() }


h = main.Handlers()

if __name__ == '__main__':
    app.run('0.0.0.0', 8898)