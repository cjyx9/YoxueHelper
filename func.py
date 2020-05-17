from requests import get
from datetime import datetime, date, timedelta

'''
#! 这是实现优学派助手的底层模块
#! 基本上是简单的get请求,自己访问一下api就知道了,懒得写注释🐆
'''

def getDate(days):
    """
    取days天前的日期
    格式化为年-月-日
    """
    return (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")

def getSubjectID(user_id, subject_name):
    """获取学科ID"""
    class_id = getClassID(user_id)[0]
    api = 'https://www.anoah.com/api/?q=json/ebag5/Classes/getClassSubject&info={"class_id":' + class_id + '}'
    subjectInfoList = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}).json()['recordset']
    for subject in subjectInfoList:
        if subject['subject_name'] == subject_name:
            return subject['edu_subject_id']

def getSubject(user_id):
    """获取所有学科"""
    class_id = getClassID(user_id)[0]
    api = 'https://www.anoah.com/api/?q=json/ebag5/Classes/getClassSubject&info={"class_id":' + class_id + '}'
    subjectInfoList = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}).json()['recordset']
    reli = []
    for subject in subjectInfoList:
        reli.append(subject['subject_name'])
    return reli

def getUserName(user_id):
    """根据优学ID获取真名"""
    api = 'https://www.anoah.com/api/?q=json/ebag/user/score/score_rank&info={"userid":"' + user_id + '"}'
    # 拼接api
    infoJson = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
    # 发送get请求
    return infoJson.json()['recordset']['real_name']
    # 返回real_name值

def getClassID(user_id):
    """根据优学ID获取班级ID"""
    api = 'https://www.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={"userid":"' + user_id + '"}'
    # 拼接api
    infoJson = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
    # 发送get请求
    return str(infoJson.json()['recordset'][0]['class_id']), str(infoJson.json()['recordset'][0]['class_name'])
    # 返回(class_id,class_name)值

def getMessage(user_id):
    """获取消息"""
    api = 'https://www.anoah.com/api/?q=json/ebag/Message/getList&info={"userid":"' + user_id+ '","page":1,"limit":800,"filter":{"message_type":2}}'
    # 拼接api
    infoJson = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}).json()
    # 发送get请求
    messageList = infoJson['recordset']['list']
    messageLTotal = infoJson['recordset']['total']
    returnList = []
    for message in messageList:
        cleanJson = {
            "message_id": message['message_id'],
            "title": message['title'],
            "content": message['content'],
            "time": message['push_time']
        }
        # 提取精华部分
        returnList.append(cleanJson)
        # 加入返回列表

    return returnList

def delMessage(user_id, idList):
    """删除信息"""
    api = 'https://www.anoah.com/api/?q=json/ebag/Message/deleteAll&info={"message_id":' + str(idList).replace("'", '"') + ',"user_id":"' + user_id + '"}'
    # 拼接api
    infoJson = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
    # 发送get请求
    print(infoJson.json()['msg'])
    return 0

def getHomework(user_id):
    """获取未完成的作业"""
    class_id = getClassID(user_id)[0]
    api = 'https://www.anoah.com/api/?q=json/ebag5/Homework/readHomework&info={"user_id":"' + user_id + '","type":1,"page":1,"class_id":"' + class_id + '"}'
    # 拼接api
    infoJson = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
    # 发送get请求
    items = infoJson.json()['recordset']['home_work']
    returnList = []
    for item in items:
        cleanJson = {
            "title": item['title'],
            "end_time": item['deadline'],
            "section_id": item['course_hour_section_id'],
            "course_hour_publish_id": item['course_hour_publish_id'],
            "teacher_name": item['teacher_name'],
            "subject_name": item["subject_name"],
            "status":item['status']
        }
        # 提取精华部分
        returnList.append(cleanJson)
        # 加入返回列表
    return returnList

def getHomeworkBydate(user_id, days, subject_name):
    """获取自from_date来的所有作业"""
    date = getDate(days)
    subject_id = getSubjectID(user_id, subject_name)
    class_id = getClassID(user_id)[0]
    api = 'https://www.anoah.com/api/?q=json/ebag5/Homework/readHomework&info={"from_date":"' + date + '","subject_id":' + str(subject_id) + ',"user_id":"' + user_id + '","type":1,"page":1,"per_page":1000,"class_id":' + class_id + ',"status":""}&v=3.0'
    subjectInfo = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
    infoJson = subjectInfo.json()
    items = infoJson['recordset']['home_work']
    returnList = []
    for item in items:
        cleanJson = {
            "title": item['title'],
            "end_time": item['deadline'],
            "section_id": item['course_hour_section_id'],
            "course_hour_publish_id": item['course_hour_publish_id'],
            "teacher_name": item['teacher_name'],
            "subject_name": item["subject_name"],
            "status":item['status']
        }
        # 提取精华部分
        returnList.append(cleanJson)
        # 加入返回列表
    return returnList

def getHomeworkInfo(section_id, course_hour_publish_id, user_id):
    api = 'https://www.anoah.com/api/?q=json/ebag5/Homework/readResource&info={"section_id":"' + section_id + '","course_hour_publish_id":"' + course_hour_publish_id + '","user_id":"' + user_id + '","view_userid":"' + user_id + '"}'
    finishedApi = 'https://www.anoah.com/api/?q=json/ebag5/Homework/finishStudent&info={"publish_id":"' + course_hour_publish_id + '"}'
    info = get(api, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}).json()
    finish = get(finishedApi, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}).json()
    
    list = info['recordset']['course_resource_list']

    returnList = []
    for topic in list:
        cleanInfo = topic['resource_name']
        returnList.append(cleanInfo)
    finishStudents = finish['recordset']

    returnList2 = []
    for student in finishStudents:
        cleanInfo2 = student['real_name'] + '(' + student['loginnm'] + ')'
        returnList2.append(cleanInfo2)

    returnList3 = []
    for topic in list:
        if topic['icom_name'] == "互动试题":
            returnList3.append({
                "pulishId": topic['course_hour_publish_id'],
                "qid": "test:" + topic["qti_id"]
            })

    returnJson = {
        "info": returnList,
        "finish": returnList2,
        "qti": returnList3
    }
    return returnJson


def getAnswer(qid, publishId):
    url = 'https://www.anoah.com/api_cache/?q=json/Qti/get&info={"param":{"qid":"' + qid + '"},"pulishId":"' + publishId + '"}'
    info = get(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}).json()
    title = info['title']
    anli = info['section'][0]['items']
    time = "大约需要" + str(round(len(anli)*0.33+0.2, 1)) + "分钟完成"
    count = 0
    retext = title + '(' + time + ')' + ":\n"

    for dict in anli:
        count += 1
        canswer = dict['answer']
        if isinstance(canswer, list):
            answer = ''
            for an in canswer:
                if isinstance(an, list):
                    answer = answer + an[0] + ';'
                else:
                    answer = answer + ';' + an
        elif str(canswer.replace(' ','')) == '':
            answer = "没有找到答案"
        elif isinstance(canswer, int) or isinstance(canswer, str):
            answer = str(canswer).strip()

        question = '(' + dict['qtypeName'] + ')' + dict['prompt'][:40] + '...'
        re = str(count) + '.' + question + '\n答案:' + answer + '\n'
        retext += re
    print(retext)