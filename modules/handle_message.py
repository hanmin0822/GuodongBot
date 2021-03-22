import re
import os
import requests
import configparser
from modules.send_message import send_message
from modules.make_CQ import make_cq
import redis

config = configparser.ConfigParser()
print(os.path.dirname(os.path.dirname(__file__)))
config.read(os.path.dirname(os.path.dirname(__file__)) + '\\config.ini', encoding='GB18030')
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

#得到所有CQ码的数组
def getAllCQ(str):
    return re.findall("\[CQ:[^(\[CQ)]*?\]",str)


#是否艾特了BOT
def is_atBOT(res):
    atselfstr = "[CQ:at,qq=" + config.get('account','BOTqq') + "]"
    if atselfstr in res:
        return True
    return False

def getPic(rev):
    if "[CQ:image" in rev["message"]:
        return getmidstring(rev["message"],"[CQ:image,file=",".image")
    return "-1"

def getPicStr(rev):
    if "私聊图片#" in rev["message"]:
        return getmidstring(rev["message"],"私聊图片#","#")
    return "-1"


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

def isQQInGroup(qq_id,group_id):
    data = {
        'user_id': qq_id,
        'group_id': group_id
    }
    cq_url = config.get('network', 'SEND_ADDRESS') + "get_group_member_info"
    rev = requests.post(cq_url, data=data)
    if rev.json()['status'] == 'ok':
        return True
    return False

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

def private_handle(rev):
    cqResArr = getAllCQ(rev["message"]);
    # 保证有人在群里
    if isQQInGroup(rev["user_id"],909403785) == True:
        if getPic(rev) != "-1":
            send_message("[私聊图片#" + getPic(rev) + "#] 群友" + make_cq.make_at_cq(rev["user_id"]) + "发送了一张私聊图片，复制这条消息私聊发送给机器人即可查看！遵守群规，请勿将这张图发送到群里哦！",909403785,"group")
            r.incr("pic_send_" + rev["user_id"], amount=1)
        elif getPicStr(rev) != "-1":
            send_message(make_cq.make_image_cq(getPicStr(rev) + ".image"),rev["user_id"],"private")
            r.incr("pic_look_" + rev["user_id"], amount=1)
        else:
            send_message("暂不支持", rev["user_id"], "private")

