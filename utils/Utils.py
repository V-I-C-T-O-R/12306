import urllib.parse

from datetime import datetime

from utils.Log import Log


def urldeocde(str):
    return urllib.parse.unquote(str)


def check(target, log):
    if not target:
        Log.e(log)
        return False
    return True


def formatDate(date):
    return datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')


if __name__ == '__main__':
    print(formatDate('20180102'))
