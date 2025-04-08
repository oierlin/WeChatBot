import openai

deepseek = openai.OpenAI(api_key="your Deepseek api key", base_url="https://api.deepseek.com")

import os
os.environ['OPENAI_API_KEY'] = 'your GPT api key'
gpt = openai.OpenAI()


# from wxauto import WeChat
import wxauto
import time
wx = wxauto.WeChat()
listen_list = [
    'Oblivion',
    'test',
    'BME1320_9',
    'BME1320课程群_2025春学期'
]
for i in listen_list:
    wx.AddListenChat(who=i, savepic=True)
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who              # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)   # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            msgtype = msg.type       # 获取消息类型
            content = msg.content    # 获取消息内容，字符串类型的消息内容
            print(f'【{who}】：{content}')
            if msgtype == 'friend':
                if(content[:3]=='@艾拉'):
                    print("call me")
                    content = content[3:]
                    print(content)
                    response = deepseek.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": content},
                        ],
                        stream=False  # 设置为 True 可启用流式输出
                    )

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
                    chat.SendMsg(response.choices[0].message.content) 
                else:
                    print("not call me")
    time.sleep(wait)