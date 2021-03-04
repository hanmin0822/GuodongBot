import re
import os
import requests
import configparser
from modules.send_message import send_message
from modules.make_CQ import make_cq

config = configparser.ConfigParser()
print(os.path.dirname(os.path.dirname(__file__)))
config.read(os.path.dirname(os.path.dirname(__file__)) + '\\config.ini', encoding='GB18030')

#得到所有CQ码的数组
def getAllCQ(str):
    return re.findall("\[CQ:[^(\[CQ)]*?\]",str)


#是否艾特了BOT
def is_atBOT(res):
    atselfstr = "[CQ:at,qq=" + config.get('account','BOTqq') + "]"
    if atselfstr in res:
        return True
    return False


#取中间字符串
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


def getPicIfHas(res):
    for str in res:
        if ("[CQ:image" in str) and ("url=" in str):
            return getmidstring(str,"url=",",")
    return None


def is_keyword_hit_message(message,keywordList):
    for kwstr in keywordList:
        if kwstr in message:
            return True
    return False

def rand_cartoon_pic():
    url="https://open.pixivic.net/wallpaper/pc/random?size=large&domain=https://i.pixiv.cat&webp=0&detail=1"
    r = requests.head(url, stream=True)  
    picstr = r.headers['Location']
    picstrarr = picstr.split('?',1)
    return picstrarr[0]

def pixiv_pic(pixiv_id,pic_format="jpg"):
    return "https://pixiv.cat/" + pixiv_id + "." + pic_format

def group_handle(rev):
    cqResArr = getAllCQ(rev["message"]);
    if is_atBOT(cqResArr) == True:
        #自己被艾特了，开始处理信息
        if is_keyword_hit_message(rev["message"],['十连抽卡','方舟十连','十连']) == True:
            send_message(make_cq.make_reply_cq(rev["message_id"]) + make_cq.make_at_cq(rev["user_id"]) + "先用这个过过瘾 https://evanchen486.gitee.io/gacha-simulator/",rev["group_id"],"group")
        elif is_keyword_hit_message(rev["message"],['setu','涩图','来图']) == True:
            send_message(make_cq.make_reply_cq(rev["message_id"]) + make_cq.make_at_cq(rev["user_id"]) + "还没有涩图，差不多得了",rev["group_id"],"group")
        elif is_keyword_hit_message(rev["message"],['翻译器在哪下载','翻译器怎么下载','翻译器下载']) == True:
            send_message(make_cq.make_reply_cq(rev["message_id"]) + make_cq.make_at_cq(rev["user_id"]) + "翻译器下载请见群文件，一些其他插件并不是全部都需要的，如有时间后续会整合", rev["group_id"], "group")
        elif is_keyword_hit_message(rev["message"],['为什么没有翻译','翻译器怎么用','翻译器问题']) == True:
            send_message(make_cq.make_reply_cq(rev["message_id"]) + make_cq.make_at_cq(rev["user_id"]) + "翻译器使用问题请先见b站教程https://space.bilibili.com/4834971或文字教程https://blog.csdn.net/hanmin822/article/details/107575287", rev["group_id"], "group")
        elif is_keyword_hit_message(rev["message"],['来点二次元','随机图']) == True:
            send_message(make_cq.make_image_cq(rand_cartoon_pic()), rev["group_id"], "group")
        elif is_keyword_hit_message(rev["message"],['pixiv（']) == True:
            if rev["user_id"] in [512240272,1210561304]:
                pixivid = getmidstring(rev["message"],"pixiv（","）")
                send_message(make_cq.make_image_cq(pixiv_pic(pixivid)), rev["group_id"], "group")
        else:
            send_message(make_cq.make_reply_cq(rev["message_id"]) + "别叫，还没支持呢", rev["group_id"], "group")
