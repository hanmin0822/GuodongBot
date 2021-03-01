
class make_cq:
    # 拼接回复CQ码
    def make_reply_cq(message_id):
        return "[CQ:reply,id=" + str(message_id) + "]"

    # 拼接艾特CQ码
    def make_at_cq(qq):
        return "[CQ:at,qq=" + str(qq) + "]"

    # 拼接录音CQ码
    def make_record_cq(file, magic=0, timeout=-1, cache=1, proxy=1):
        if timeout == -1:
            return "[CQ:record,file=" + file + ",magic=" + magic + "]"
        else:
            return "[CQ:record,file=" + file + ",magic=" + magic + ",cache=" + cache + ",proxy=" + proxy + ",timeout=" + timeout + "]"

    # 拼接图片CQ码
    def make_image_cq(file, type='normal', cache=1, id=40000):
        if type == 'normal':
            return "[CQ:image,file=" + file + ",id=" + id + "]"
        else:
            return "[CQ:image,file=" + file + ",type=" + type + ",id=" + id + ",cache=" + cache + "]"

    # 拼接表情CQ码
    def make_face_cq(id):
        return "[CQ:face,id=" + str(id) + "]"

    # 拼接群聊戳一戳CQ码
    def make_poke_cq(qq):
        return "[CQ:poke,qq=" + str(qq) + "]"