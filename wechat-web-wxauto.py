import openai
from personal_info import DEEPSEEK_API_KEY, personal_listen_list, account, password
# personal_info.py is manually created by administrator, which includes 4 variables:
# DEEPSEEK_API_KEY:str, personal_listen_list:List[str], account:str, password:str
# account and password are used to login deepseek web

deepseek = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def ask_deepseek(content):
    response = deepseek.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": content},
                        ],
                        stream=False  # 设置为 True 可启用流式输出
                    )
    return response.choices[0].message.content


import os
os.environ['OPENAI_API_KEY'] = 'your GPT api key'
gpt = openai.OpenAI()


# from wxauto import WeChat
import wxauto
import time

from deepseek_web import ask_web, web_login, change_think, change_searching, check_think, check_search

chatlog = {}

def processMsg(who, content):
    print(content)
    if("深度思考" in content.split() or "联网搜索" in content.split()):
        if("深度思考" in content.split()):
            change_think()
        if("联网搜索" in content.split()):
            change_searching()
        think_flag = check_think()
        search_flag = check_search()
        answer = "深度思考:"+str(think_flag)+"\n联网搜索:"+str(search_flag)
        print("深度思考:",think_flag)
        print("联网搜索:",search_flag)
        return answer
    print('思考中')
    content = "我:"+content+';  '+'模型：'
    print("sender:",who)
    print(content)
    chatlog[who] = chatlog.get(who, '')+content
    answer,success = ask_web(content)
    print(answer)
    # answer,success = ask_deepseek(chatlog[sender],
    #                       key = "15c7cc86cc4e44aa978cbbebd70f7975",
    #                       url = " https://genaiapi.shanghaitech.edu.cn/api/v1/start/chat/completions",
    #                       model = "deepseek-v3:671b")
    # answer = ask_deepseek(chatlog[sender],
    #                       key = "0b755452512d486c974e27ba20721a44",
    #                       url = "https://genaiapi.shanghaitech.edu.cn/api/v1/start/chat/completions",
    #                       model = "deepseek-r1:671b")
    chatlog[who] = chatlog[who]+answer
    return answer

if __name__ == "__main__":


    wx = wxauto.WeChat()
    robot_name = '艾拉'  # 机器人名称
    # listen_list = [
    #     'Oblivion',
    #     'test',
    #     'BME1320_9',
    #     'BME1320课程群_2025春学期'
    # ]
    listen_list = personal_listen_list
    for i in listen_list:
        wx.AddListenChat(who=i, savepic=True)
    wait = 1  # 设置1秒查看一次是否有新消息
    web_login(account, password)
    while True:
        msgs = wx.GetListenMessage()
        for chat in msgs:
            who = chat.who              # 获取聊天窗口名（人或群名）
            one_msgs = msgs.get(chat)   # 获取消息内容
            print(len(one_msgs))
            # 回复收到
            for msg in one_msgs:
                msgtype = msg.type       # 获取消息类型
                content = msg.content    # 获取消息内容，字符串类型的消息内容
                print(msgtype)
                print(f'【{who}】：{content}')
                if msgtype == 'friend' or msgtype == 'self':
                    if(content[:len(robot_name)+1]==('@'+robot_name)):
                        print("call me")
                        content = content[len(robot_name)+1:]
                        print(content)
                        answer = processMsg(who, content)
                        print(content,answer)
                        

                        # response = gpt.chat.completions.create(
                        #     model="gpt-4o-mini",
                        #     messages=[
                        #         {"role": "system", "content": "You are a helpful assistant."},
                        #         {
                        #             "role": "user",
                        #             "content": content
                        #         }
                        #     ]
                        # )
                        # chat.SendMsg(ask_deepseek(answer)) 
                        chat.SendMsg(answer) 
                    else:
                        print("not call me")
        time.sleep(wait)