# -*- coding: utf-8 -*-
import datetime


def logger(text):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print('[{}] {}'.format(time, text))


if __name__ == '__main__':
    pass


