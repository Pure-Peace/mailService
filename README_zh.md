# mailService
基于python3的邮件服务(SMTP)。提供邮件模板系统、多语言、自动翻译、多邮件服务器以及微型web api示例。
Mail service based on python3 (SMTP). Provide mail template system, multi-language, automatic translation, multi-mail server management and micro web api examples。

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

添加你的SMTP发信服务器！

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
 
调用 `mailService.send_mail()`来发送邮件

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


## 1. 多语言邮件，以及随机变换的邮件颜色（material颜色风格）

这是关于邮件模板渲染的功能，位于`emailManager.py`中，我已经内置了几套配色

![screenshot](http://otsu.fun/demos1/p1.png)

邮件的语言可由网页端选择，判断用户的语言，提交后端发送对应语言的邮件。

![screenshot](http://otsu.fun/demos1/p2.png)

---

### 2. 支持多语言的邮件模板系统（jinja2语法）

与flask html基本相同的写法，红框处展示了多语言化功能，邮件发送的效果请看第1点的截图：`1. 多语言邮件，以及随机变换的邮件颜色（material颜色风格）`

在`translations`目录中建立对应语言的翻译目录，并添加.json格式的翻译文件，即可像图片描述的一样调用多语言。

而且，你可以在python能够达到的任何地方使用多语言，包括log等等，只要你添加翻译文件，并正确调用`translator`对象的`tran()`方法即可完成。

调用模板发送邮件十分简单，你只需要调用`EmailManager`的`send_mail()`方法，并将`content`参数设为html模板的名称（如`reg_success`)，邮件系统会自动在`templates`目录下寻找对应的html邮件模板，并且渲染它。

注意，如果要为你的html邮件模板添加数据，还需要传入`template_data`数据，是一个字典。

![screenshot](http://otsu.fun/demos1/p6.png)

---

### 3. 使用简单，可添加多个发信服务器，支持SSL与一般端口（红框处）

添加服务器仅需按图上所描述的，实例化`MailServer`对象，加入列表即可
`MailServer`对象十分简单，参见`mailServer.py`，主要是对发信服务器的一些配置。

包含了回复地址`reply_address`，以及图上没有表示出来的`client_type`（用于指示是否ssl）
还有一个重要的是`sender_name`，用户收到的邮件会显示这个名字。

![screenshot](http://otsu.fun/demos1/p4.png)

---

### 4. 翻译器，默认语言为简体中文

将`language`改为指定语言的英文缩写即可实现翻译，如果找不到指定语言的翻译，它会自动选择`default_language`语言，所以请务必保证`default_language`是完整的。
同时，你需要在`translation`中增加翻译文件，来支持翻译器。
下文提供了一个小工具，自动生成谷歌翻译的.json翻译文件。

![screenshot](http://otsu.fun/demos1/p5.png)

---

### 5. json格式的多语言文件

这个就是所谓的json翻译文件了，具体的调用方法请往上翻到第2点：`2. 支持多语言的邮件模板系统（jinja2语法）`。

![screenshot](http://otsu.fun/demos1/p7.png)

---

### 6. 提供一个小工具，一键创建多国语言翻译（google translate）[makeTranslations.py]

这个工具通过调用python的谷歌翻译api创建多语言翻译文件。
首先你必须保证`translator.py`所配置的`language`所指定的语言完整，然后才可以使用这个工具。

它会以`translator`对象的`language`为基本语言，然后根据基本语言的翻译文件生成其它语言的翻译文件。


![screenshot](http://otsu.fun/demos1/p8.png)

编辑好`makeTranslations.py`，直接运行即可生成。极其简单

![screenshot](http://otsu.fun/demos1/p9.png)

---

### 8. 提供web接口调用演示（flask）[simpleApi.py]

这个很简单，运行`simpleApi.py`就可以看到效果了

比如访问`http://localhost:8898/send_mail/reg_success/youremail@email.com/test?lang=en`时，邮件服务会给用户`test <youremail@email.com>`发送一个以`reg_success`为模板，语言`lang=en`的注册成功邮件。

这意味着，你可以轻易的根据用户的浏览器语言向其发送对应语言的邮件，只需要调用api即可。

![screenshot](http://otsu.fun/demos1/p3.png)

---

enjoy

