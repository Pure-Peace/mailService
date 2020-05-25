# 🔥 mailService
基于python3的邮件服务(SMTP)。提供邮件模板系统、多语言、自动翻译、多邮件服务器以及微型web api示例。
Mail service based on python3 (SMTP). Provide mail template system, multi-language, automatic translation, multi-mail server management and micro web api examples。

- 🌺English / 💖[中文](https://github.com/Pure-Peace/mailService/blob/master/README_zh.md)


## 🍖Easy:

- 🍊`Based on python3, and lightweight`
- 🍉`Allow to add multiple sending servers, if one server is broken, it will automatically switch to other servers` 
- 🍩`Email html template system (jinja2 syntax, the same way as flask)`
- 🌼`Multi-language support, e-mail in any language`
- 🌠`A fairly good translator, add .json translation file and eat it`
- 🍖`Multilingual translation generator, automatically generates translations in other languages based on the main language`
- ⛅`Provide a simple flask example, try to use the web interface to call this mail service`

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

Add your SMTP mail server!

```python
class EmailManager:
    def __init__(self, template_dir='templates', template_extension='.html', translator=None):
        logger('Initialize the mail manager...')
        self.send_success = 0
        self.send_failed = 0
        self.template_dir = template_dir
        self.template_extension = template_extension
        self.templates = {}
        self.mail_servers = []
        self.init_servers()
        self.init_templates()
        self.translator = translator or Translator()
        logger('Initialize mail manager: successful!')
        
    # this way!
    def init_servers(self):
        self.mail_servers = [
            MailServer('aliyun', 'your(sender)@email.com', 'password', 'smtpdm.aliyun.com', 80),
            MailServer('tencent_company', 'your(sender)@email.com', 'password', 'smtp.exmail.qq.com', 465)
        ]
        logger('Initialize the mail server({})..success!'.format(len(self.mail_servers)))
    ...
```

 4. **🌽try [send email]（main.py）**
 
 use `mailService.send_mail()` to send mail
 
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
lets try

## 📷Features Show:


## 1. Multi-language mail, and a randomly-transformed mail color demo (material color style)

This is about the function of email template rendering, located in `emailManager.py`, I have built several sets of color matching

![screenshot](http://otsu.fun/demos1/p1.png)

The language of the e-mail can be selected by the webpage, determine the user's language, and submit the backend to send the e-mail in the corresponding language.

![screenshot](http://otsu.fun/demos1/p2.png)

---

### 2. Email template system supporting multiple languages (jinja2 syntax)

Basically the same writing as flask html, the multi-language function is shown in the red box, please see the screenshot of point 1 for the effect of email sending: `1. Multi-language email, and the randomly changed email color (material color style)

Create a translation directory for the corresponding language in the `translations` directory, and add a translation file in .json format to call multiple languages as described in the picture.

Moreover, you can use multiple languages wherever Python can reach it, as long as you add the translation file and call the `tran ()` method of the `translator` object correctly.

Calling the template to send mail is very simple, you only need to call the send_mail () method of ʻEmailManager`, and set the `content` parameter to the name of the html template (such as` reg_success`), the mail system will automatically be in the `templates` directory Find the corresponding html mail template and render it.

Note that if you want to add data to your html mail template, you also need to pass in `template_data` data, which is a dictionary.

![screenshot](http://otsu.fun/demos1/p6.png)

---

### 3. Simple to use, allows you to add multiple mail servers, supports SSL (note the content in the red box on the screenshot)

To add a server, just instantiate the `MailServer` object as described in the figure and add it to the list.

The `MailServer` object is very simple, see` mailServer.py`, mainly for some configuration of the sending server, contains the reply address `reply_address`, and` client_type` not shown in the figure (used to indicate whether it is ssl)
Another important thing is `sender_name`, which will be displayed in the emails received by users.



![screenshot](http://otsu.fun/demos1/p4.png)

---

### 4. Translator, the default language is simplified Chinese(cn)

Translation can be achieved by changing `language` to the English abbreviation in the specified language. If the translator cannot find a translation in the specified language, it will automatically select the `default_language` language, so please make sure that` default_language` is at least complete.

At the same time, you need to add translation files in `translation` to support the translator.
The following provides a small tool that automatically generates a Google translated .json translation file.

![screenshot](http://otsu.fun/demos1/p5.png)

---

### 5. Translation file in json format

This is the translation file in json format. 

For the specific calling method, please turn up to point 2: `2. Multi-language mail template system (jinja2 syntax)`.

![screenshot](http://otsu.fun/demos1/p7.png)

---

### 6. Provide a small tool to create multi-language translations with one click [makeTranslations.py]

This tool creates a multilingual translation file by calling Python's Google Translate API.

First of all, you must ensure that the language specified in the `language` configuration of` translator.py` is complete before you can use this tool.

It will use `language` of the` translator` object as the basic language, and then generate translation files in other languages based on the translation files in the basic language.


![screenshot](http://otsu.fun/demos1/p8.png)

Edit `makeTranslations.py` and run it directly to create a language directory in the` translations` directory and generate translation files in json format. 

very simple

![screenshot](http://otsu.fun/demos1/p9.png)

---

### 8. Provide web interface call demo (flask) [simpleApi.py]

This is very simple, you can see the effect by running simpleApi.py

For example, when you visit `http://localhost:8898/send_mail/reg_success/youremail@email.com/test?lang=en`, the mail service will send the user `test <youremail@email.com>` a template with `reg_success` email,
The email language is `lang=en`.

This means that you can easily send emails in the corresponding language according to the user's browser language, just call the API.

![screenshot](http://otsu.fun/demos1/p3.png)

---

enjoy

