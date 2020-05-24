# mailService
基于python3的邮件服务。提供邮件模板系统、多语言、自动翻译、多邮件服务器以及微型web api示例。
Mail service based on python3. Provide mail template system, multi-language, automatic translation, multi-mail server management and micro web api examples。

## 🍖Easy:

- 🍊`基于python3，而且轻量！`
- 🍉`可添加多个发信服务器，一个服务器坏了自动切换其它服务器发信` 
- 🍩`邮件html模板系统（jinja2语法，跟flask一样的写法）`
- 🌼`多国语言支持，什么语言的网页就发什么语言的邮件`
- 🌠`还算好用的翻译器和.json文件`
- 🍖`奇怪的机翻生成器，自动根据主要语言生成其它语言的翻译`
- ⛅`还有一个简单的flask示例，用web接口调用这个邮件服务`

<h2 align="center">🏆-Start-</h2>

 1. **🍬Clone this repository**
 
```bash
git clone https://github.com/Pure-Peace/mailService
```

2、**🍙Install dependencies (just flask、py-google-translate...)**
```bash
pip install -r requirements.txt
```

3、**🍮Add mail server (emailManager.py)**
```python
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
        
    # this way!
    def init_servers(self):
        self.mail_servers = [
            MailServer('aliyun', 'your(sender)@email.com', 'password', 'smtpdm.aliyun.com', 80),
            MailServer('tencent_company', 'your(sender)@email.com', 'password', 'smtp.exmail.qq.com', 465)
        ]
        logger('初始化邮件服务器({})..成功!'.format(len(self.mail_servers)))
    ...
```

 4. **🌽try [send email]（main.py）**
 ```python
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
    h.reg_success({'username': 'test', 'usermail': 'your@email.com'}, 'your@email.com', 'en') # you can change language!!
```
 
5. **🍁try [generate translation file]（makeTranslations.py）**

```bash
python makeTranslations.py
```

6. **🍭try [use web api send mail] (simpleApi.py)**

```bash
python simpleApi.py
```
then open

```
http://localhost:8898/
```


## 📷Features Show:


## 多语言邮件，以及随机变换的邮件颜色（material颜色风格）
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p1.png)
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p2.png)

---

### 支持多语言的邮件模板系统（jinja2语法）
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p6.png)

---

### 使用简单，可添加多个发信服务器，支持SSL与一般端口（红框处）
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p4.png)

---

### 翻译器，默认语言为简体中文
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p5.png)

---

### json格式的多语言文件
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p7.png)

---

### 提供一个小工具，一键创建多国语言翻译（google translate）[makeTranslations.py]
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p8.png)

### 直接运行，自动创建翻译

![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p9.png)

---

### 提供web接口调用演示（flask）
![screenshot](https://github.com/Pure-Peace/mailService/blob/master/screenshot/p3.png)

---



