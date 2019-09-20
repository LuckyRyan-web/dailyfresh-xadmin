__author__ = 'LY'
__date__ = '2019/9/20 10:01'
import hashlib

def md5value(s):
    md5 = hashlib.md5()
    md5.update(s)
    return md5.hexdigest()

def mdfive(data):
    list = []
    for k, v in data.items():
        # print(v, '->', md5value(v.encode()))
        list.append(md5value(v.encode(encoding='UTF-8')))
    return list


if __name__ == "__main__":
    pass