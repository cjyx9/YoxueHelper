import datetime
from time import sleep
from winsound import MessageBeep
# 在win平台上播放提示声
from easygui import msgbox, ccbox
from func import getMessage, delMessage

# 简单的作业提醒
# 思路是根据重复获取消息箱的消息,并判断是否为新作业,再弹出提示

def toasts():
    idtxt = open("youxue_user_id.txt", 'r')
    user_id = idtxt.read()
    sumNum = 0
    while True:
        sumNum += 1
        messages = getMessage(user_id)
        for message in messages:
            if "发布了新作业" in message['content']:
                MessageBeep()
                # msgbox(message['content'], title= message['title'],ok_button="知道啦")
                if ccbox(message['content'], title= message['title'],choices=("知道啦","马上去做")):
                    delMessage(user_id, [message['message_id']])
                else:
                    from webbrowser import open as opurl
                    opurl("https://e.anoah.com/ebags/")
                    delMessage(user_id, [message['message_id']])
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
        print("第%i次刷新,时间:%s,消息%i条" % (sumNum, time_str, len(messages)))
        del messages, curr_time, time_str
        sleep(180)

if __name__ == "__main__":
    toasts()