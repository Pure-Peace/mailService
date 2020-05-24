# -*- coding: utf-8 -*-
from os import listdir, path
from sys import path as cwd
from json import load
from utils import logger


class Object(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def build_object(data):
        if not isinstance(data, dict): return data
        for k, v in data.items():
            if isinstance(v, dict):
                data[k] = Object(v)
                Object.build_object(data[k])
        return Object(data)


class LanguageObject:
    def __init__(self, dict_data):
        self.__dict__ = Object.build_object(dict_data)
        self.data = dict_data
        
    
class Translator:
    def __init__(self, language='cn', default_language='cn'):
        self.translations_dir = 'translations'
        self.translations_extension = '.json'
        self.language = language
        self.default_language = default_language or language
        self.messages = {}
        self.init_messages_dict()
        self.language_object = LanguageObject(self.messages)


    def tran(self, target):
        if self.language not in self.messages: self.language = self.default_language
        lang_object = getattr(
            self.language_object, self.language, 
            getattr(self.language_object, list(self.messages.keys())[0], {})
        )
        try: return eval(r'lang_object.{}'.format(target))
        except: return target


    def init_messages_dict(self):
        messages = {}
        count = 0
        for language_dir in [d for d in listdir(self.translations_dir) if path.isdir(path.join(cwd[0], self.translations_dir, d))]:
            temp_messages = {}
            for fileName in listdir('{}/{}'.format(self.translations_dir, language_dir)):
                if self.translations_extension in fileName:
                    try:
                        filePath = '{}/{}/{}'.format(self.translations_dir, language_dir, fileName)
                        with open(filePath, 'r', encoding='utf-8') as translation_file:
                            temp_messages[fileName.replace(self.translations_extension, '')] = load(translation_file)
                            count += 1
                    except Exception as err:
                        logger('文件[{}] 添加失败 ({})'.format(filePath, err))
            messages[language_dir] = temp_messages
        self.messages.update(messages)
        logger('支持语言数({})，共添加翻译文件共({})个..完毕!'.format(len(messages), count))
        
    
if __name__ == '__main__':
    translator = Translator()
    