'''
#! GUI功能部分
#! 核心代码在func.py
#! 小白目前工程量最大的项目,点个star呗
'''

# ---------------------------初始化部分start---------------------------

import func
# 引入底层包
import easygui
# 引入GUI包
import threading
# 做作业提醒时要用到多线程
from toast import toasts
# 引入作业提醒模块
from os.path import exists
# 引入判断文件是否存在的方法

user_id, class_tuple, class_id, class_name, user_name = None, None, None, None, None
# 消除警告 ⚠28 看起来超级烦有没有

def init():
    """
    定义全局变量,优化运行速度(原版是每个函数要用到这些变量都要加载一次)
    用到了func块的getClassID和getUserName方法
    """
    global user_id, class_tuple, class_id, class_name, user_name
    user_id = getUserID()
    class_tuple = func.getClassID(user_id)
    class_id = class_tuple[0]
    class_name = class_tuple[1]
    user_name = func.getUserName(user_id)
    return 0

def writeUserID():
    """写入保存ID的配置文件的GUI界面"""
    while True:
        user_id = easygui.enterbox(msg="输入id(如e1765849):", title="录入ID").replace("e", "")
        # 获取输入GUI
        if not user_id:
            easygui.msgbox("错误!ID不得为空!")
            # 为空时的操作
        else:
            try:
                userName = func.getUserName(user_id)
                # 尝试获取名字，检测ID是否正确
            except:
                easygui.msgbox("错误!请检查你的ID是否正确!")
                # 丢出错误
            else:
                if easygui.ccbox("您是%s吗?" % userName,choices=("是","不是")):
                # 确定
                    break
    idtxt = open("youxue_user_id.txt", 'w+')
    idtxt.write(user_id)
    # 不存在的话创建并写入ID
    easygui.msgbox("录入成功!重启生效!")
    # 重新启动以刷新全局变量
    return 0

def getUserID():
    """获取用户输入-返回ID"""
    if exists("youxue_user_id.txt"):
    # 判断文件是否存在:
        idtxt = open("youxue_user_id.txt", 'r')
        user_id = idtxt.read()
        # 若存在读出userID保存至全局变量
        return user_id
    else:
        writeUserID()

# ---------------------------初始化部分end---------------------------

# ---------------------------作业部分start---------------------------

def showAllHomework():
    """
    显示所有未完成的作业
    用到了func块的getHomework和showHomeworkInfo方法
    """
    global user_id, user_name
    showList = []
    # 储存所有未完成作业标题的列表
    cards = func.getHomework(user_id)
    # 获取有关的Dict
    for card in cards:
        showList.append(card['title'])
        # 循环加入列表
    choiceOption = easygui.choicebox("%s未完成的作业,共%i个" % (user_name, len(showList)), "YoxueHelper", showList)
    # 用choicebox显示作业
    if choiceOption:
        showHomeworkInfo(cards, showList.index(choiceOption), False)
    else:
        main()

def showHomeworkByDate():
    """
    按时间读取作业
    用到了func块的getSubject、showHomeworkInfo和getHomeworkBydate方法
    基本和showAllHomework方法相同
    """
    global user_id
    subjects = func.getSubject(user_id)
    choice = easygui.choicebox("选择你要查看的学科:", "YoxueHelper", subjects)
    # 这里是获取用户要查询的学科
    days = easygui.integerbox('输入你要查询几天前至今的作业:', 'YoxueHelper', 7, 3, 5000)
    # 查看的时间限制
    if days == None:
        main()
        return None
        # 直接关闭弹窗会返回None并报错,这儿做了一个处理
    
    cards = func.getHomeworkBydate(user_id, days, choice)
    showList = []
    for card in cards:
        showList.append(card['title'])
    choiceOption = easygui.choicebox("%s作业,共%i个" % (choice, len(showList)), "YoxueHelper", showList)
    if choiceOption:
        showHomeworkInfo(cards, showList.index(choiceOption), True)
    else:
        main()

def showHomeworkInfo(cards, choiceIndex, call):
    """
    显示作业详情
    :cards: 其实就是getHomeworkBydate或getHomework的返回值这里不重复获取,优化运行速度
    :choiceIndex: 选择的作业的索引,用来定位要查看的选项
    #// :status: bool值表示完成与否,目前有bug
    #// TODO fix the bug
    #// bug已修复
    :call: 调用方True为getHomeworkBydate,反之。
    """
    global user_id
    card = cards[choiceIndex]
    title = "作业标题:" + card['title']
    status = card['status']
    if status == 3:
        doed = "已完成"
    else:
        doed = "未完成"
    endTime = "作业结束时间:" + card['end_time']
    teacher = "布置教师:" + card['teacher_name']
    subject = "学科:" + card['subject_name']
    source = func.getHomeworkInfo(card['section_id'], card['course_hour_publish_id'], user_id)
    info = '作业内容:'
    for i in source['info']:
        info = info + '\n\t' + i
    finish = '\n完成人员:'
    for i in source['finish']:
        finish = finish + '\n\t' + i
    conText = title + '\n\t' + doed + "\n\t" + endTime + '\n\t' + teacher + '\n\t' + subject + "\n\n" + info + "\n" + finish
    easygui.textbox("作业详情", card['title'], conText)
    if call:
        showHomeworkByDate()
    else:
        showAllHomework()

# ---------------------------作业部分end---------------------------

# ---------------------------信件部分start---------------------------

def showAllMessage():
    """
    GUI收件箱
    用到了func模块的showMessageInfo和getMessage方法
    """
    global user_id, user_name
    messages = func.getMessage(user_id)
    # 获取相关Dict
    showList = []
    # 储存显示的信件标题的列表
    for message in messages:
        showList.append(message['title'])
    choiceOption = easygui.choicebox("%s未读的消息,共%i个" % (user_name, len(showList)), "YoxueHelper", showList)
    if choiceOption:
        showMessageInfo(messages, showList.index(choiceOption))
        # 显示详情
    else:
        main()

def showMessageInfo(messages, choiceIndex):
    """
    显示消息详情
    :messages: 调用func.getMessage方法返回的Dict
    :choiceIndex: 选择的消息的索引,用来定位要查看的选项
    """
    global user_id
    message = messages[choiceIndex]
    title = message['title']
    context = message['content'] + '\n' + '发送时间:' + message['time']
    message_id = message['message_id']
    easygui.msgbox(context, title, "朕已阅")
    func.delMessage(user_id, [message_id])
    # 删除已阅的消息
    showAllMessage()
    # 回到上一个界面

def delAllMessage():
    """
    删除当前用户所有的消息
    用到了func块的delMessage方法
    """
    global user_id
    # 申明一下全局变量
    if easygui.ccbox("您确定要清空消息(消息不可恢复)",choices=("确定","取消")):
        MessageIDList = []
        # 储存所有信息的ID的列表
        for item in func.getMessage(user_id):
            MessageIDList.append(item["message_id"])
            # 循环获取消息id加入列表
        func.delMessage(user_id, MessageIDList)
        # 传入delMessage方法
        easygui.msgbox('删除完毕,共删除' + str(len(MessageIDList)) + '条消息', 'YoxueHelper', '确定')
        # 提示
        main()
        # 回到主界面
    else:
        main()

# ---------------------------信件部分end---------------------------

def main():
    """索引界面"""
    global user_id, user_name, class_name
    options = ['查询作业', '未完成作业', '消息箱', '清空消息', '更换用户', '开启作业提醒', '退出']
    # 定义选项列表
    choice = easygui.choicebox("你好，来自%s的%s" % (class_name, user_name), "YoxueHelper", options)
    
    # 开始各种if...else...的骚操作
    if choice == "清空消息":
        delAllMessage()
    elif choice == "更换用户":
        writeUserID()
    elif choice == "未完成作业":
        showAllHomework()
    elif choice == "消息箱":
        showAllMessage()
    elif choice == "查询作业":
        showHomeworkByDate()
    elif choice == "开启作业提醒":
        threads = [threading.Thread(target=main), threading.Thread(target=toasts)]
        for t in threads:
            # 启动线程
            t.start()
    elif choice == "退出":
        exit()

if __name__ == "__main__":
    init()
    # 初始化
    main()
    # 显示主界面