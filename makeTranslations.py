# -*- coding: utf-8 -*-
'''
@name: 一键翻译工具
@author: PurePeace
@version: 0.1.0
'''
from utils import logger
from time import time
import os
from translator import Translator
from json import dumps
from googletrans import Translator as google_trans
from googletrans.constants import LANGCODES


class TranslationsBuilder:
    def __init__(self, dest_langs, translator=None, google_translator=None):
        self.dest_langs = dest_langs
        self.translator = translator or Translator()
        self.google_translator = google_translator or google_trans(service_urls=['translate.google.cn'])
        self.translate_tasks = {}
        self.origin_language = self.get_origin_language()
        self.init_translate_tasks()
        self.support_languages = LANGCODES
    
    
    def start_task(self):
        for lang in self.dest_langs:
            self.handle_translate_task(lang)
        logger('所有任务已完成。')
    
    
    def get_translated(self, text, dest_lang):
        dest_lang = self.get_origin_language(dest_lang)
        translated = self.google_translator.translate(text, src=self.origin_language, dest=dest_lang).text
        return translated
    
    
    def get_origin_language(self, dest_lang=None):
        lang = dest_lang or self.translator.language.lower()
        if lang in ('sc', 'cn'): return 'zh-cn'
        elif lang in ('hk', 'tw', 'tc'): return 'zh-tw'
        else: return lang
    
    
    def init_translate_tasks(self):
        count = 0
        origin_language_messages = self.translator.messages[self.translator.language]
        logger('源语言({}) 待处理文件数({})'.format(self.translator.language, len(origin_language_messages.keys())))
        for file_name in origin_language_messages.keys():
            temp = {}
            queue = [origin_language_messages[file_name]]
            while len(queue) > 0:
                data = queue.pop()
                for key, value in data.items():
                    if type(value) == str: temp[value] = ''
                    else: queue.append(value)
            self.translate_tasks[file_name] = temp
            count += len(temp)
            logger('文件[{}.json] 共找到{}条待翻译语句！'.format(file_name, len(temp)))
        logger('目标选择完毕，语句总数({}) 准备进行翻译...'.format(count))
    
    
    def handle_translate_task(self, dest_lang):
        logger('开始进行({})语言的翻译任务...'.format(dest_lang))
        count = 0
        start_time = time()
        for file_name in self.translate_tasks.keys():
            done = 0
            current_dict = self.translate_tasks[file_name]
            logger('文件[{}/{}.json] 开始翻译... 语句数({})'.format(dest_lang, file_name, len(current_dict)))
            for k in current_dict:
                current_dict[k] = self.get_translated(k, dest_lang)
                done += 1
                count += 1
                print('\r当前进度({}/{})'.format(done, len(current_dict)), end='')
            logger(' done!\n')
        logger('已完成所有文件({})的翻译！ 语句总数({}) 用时{}s'.format(len(self.translate_tasks.keys()), count, time() - start_time))
        logger('准备写出文件...')
        self.write_out_files(dest_lang)
    
    
    def write_out_files(self, dest_lang):
        for file_name in self.translate_tasks.keys():
            logger('开始处理文件[{}.json]...'.format(file_name))
            current_dict = self.translate_tasks[file_name]
            target_file_content = dumps(self.translator.messages[self.translator.language][file_name], ensure_ascii=False, indent=4)
            for key in current_dict: 
                target_file_content = target_file_content.replace(key, current_dict[key])
            lang_path = r'{}/{}'.format(self.translator.translations_dir, dest_lang)
            file_path = r'{}/{}.json'.format(lang_path, file_name)
            self.mkdirs(lang_path)
            with open(file_path, 'w', encoding='utf-8') as out_file:
                out_file.write(target_file_content)
            logger('文件[{}]已写出！'.format(file_path))
        logger('目标语言[{}] 所有翻译文件已写出！'.format(dest_lang))
    
    
    @staticmethod
    def mkdirs(*paths):
        for path in paths: 
            path = path.strip()
            path = path.rstrip('\\')
            isExists = os.path.exists(path)
            if not isExists: os.makedirs(path)


if __name__ == '__main__':
    # auto translate( language list )
    builder = TranslationsBuilder(['ja', 'tc', 'ko', 'ru', 'th', 'de'], Translator('cn'))
    builder.start_task()