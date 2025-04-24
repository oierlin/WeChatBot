from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
input_text = ""
driver = webdriver.Edge()
think = False
search = False
def wait_for_new_response(last_count):
    while True:
        new_count = len(driver.find_elements(By.XPATH, '//div[@class="ds-markdown ds-markdown--block"]'))
        if new_count > last_count:
            return
def ask_web(question):
    last_count = len(driver.find_elements(By.XPATH, '//div[@class="ds-markdown ds-markdown--block"]'))
    chat_input = driver.find_element(By.XPATH, '//textarea[@id="chat-input"]')
    chat_input.send_keys(question)
    _ = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="button" and @class="_7436101"]'))
        )
    send_button = driver.find_element(By.XPATH, '//div[@role="button" and @class="_7436101"]')
    send_button.click()
    wait_for_new_response(last_count)
    response = driver.find_elements(By.XPATH, '//div[@class="ds-markdown ds-markdown--block"]')[-1].text
    last_text = ""
    while response != last_text:
        last_text = response
        time.sleep(1)
        response = driver.find_elements(By.XPATH, '//div[@class="ds-markdown ds-markdown--block"]')[-1].text
        print("res",response)
    # print("response:", driver.find_elements(By.XPATH, '//div[@class="ds-markdown ds-markdown--block"]')[-1])
    return response, 1
def change_think():
    global think
    button1 = driver.find_element(By.XPATH, '//*[@role="button" and .//span[contains(@class, "ad0c98fd") and text()="深度思考 (R1)"]]')
    button1.click()
    think = not think
    
def change_searching():
    global search
    button1 = driver.find_element(By.XPATH, '//*[@role="button" and .//span[contains(@class, "ad0c98fd") and text()="联网搜索"]]')
    button1.click()
    search = not search
def web_login():
    driver.get("https://chat.deepseek.com")
    change_button = driver.find_element(By.XPATH, '//div[@class="ds-tab__content" and text()="密码登录"]')
    change_button.click()
    user_input = driver.find_element(By.XPATH, '//input[@class="ds-input__input" and @placeholder="请输入手机号/邮箱地址"]')
    user_input.send_keys('your user name')
    password_input = driver.find_element(By.XPATH, '//input[@class="ds-input__input" and @placeholder="请输入密码"]')
    password_input.send_keys('you password')
    login_button = driver.find_element(By.XPATH, '//div[@role="button" and text()="登录"]')
    login_button.click()
    # time.sleep(2)
    try:
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "chat-input"))
        )
        print("✅ 登录成功，聊天输入框已加载！")
    except Exception as e:
        print("❌ 登录失败或输入框未出现:", e)

# web_login()
# ask_web("用python写一份helloword")
# ask_web("你好")
# ask_web("你好")
# exit(0)


import requests
def ask_deepseek(question,key,url,model, model_role="你是一个语言简洁的聊天模型"):
    API_KEY = key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": model,  # 指定使用 R1 模型（deepseek-reasoner）或者 V3 模型（deepseek-chat）
        "messages": [
            {"role": "system", "content": model_role},
            {"role": "user", "content": question}
        ],
        "stream": False  # 关闭流式传输
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'], 1
    else:
        return "请求失败，错误码："+response.status_code, 0
from queue import Empty
from threading import Thread
from wcferry import Wcf, WxMsg
wcf = Wcf()
print(wcf.is_login())
print("login user:",wcf.get_self_wxid())

chatlog = {}

rooms = ['49806583966@chatroom','47511599819@chatroom','48274704185@chatroom']

def processMsg(msg: WxMsg):
    # if(msg.roomid not in rooms):
    #     return
    print(msg.content, msg.sender, msg.id)
    # if msg.from_group():return # 不回复群消息（可选）
    # if msg.sender == "wxid_32vg1ruxuzy322": # 填入发送者的wxid，只回他的消息（可选）
    
    if(msg.content[:3]!='@艾拉' and msg.from_group()):
        print("not call me")
        return
    sender = msg.roomid
    if("深度思考" in msg.content.split()):
        change_think()
        answer = "深度思考:"+str(think)+"\n联网搜索:"+str(search)
        print("深度思考:",think)
        print("联网搜索:",search)
        wcf.send_text(answer, sender)
        return
    if("联网搜索" in msg.content.split()):
        change_think()
        answer = "深度思考:"+str(think)+"\n联网搜索:"+str(search)
        print("深度思考:",think)
        print("联网搜索:",search)
        wcf.send_text(answer, sender)
        return
    print('思考中')
    content = "我:"+msg.content+'\n'+'模型：'
    print("sender:",sender)
    chatlog[sender] = chatlog.get(sender, '')+content
    answer,success = ask_web(msg.content.removeprefix("@艾拉"))
    # answer,success = ask_deepseek(chatlog[sender],
    #                       key = "15c7cc86cc4e44aa978cbbebd70f7975",
    #                       url = " https://genaiapi.shanghaitech.edu.cn/api/v1/start/chat/completions",
    #                       model = "deepseek-v3:671b")
    # answer = ask_deepseek(chatlog[sender],
    #                       key = "0b755452512d486c974e27ba20721a44",
    #                       url = "https://genaiapi.shanghaitech.edu.cn/api/v1/start/chat/completions",
    #                       model = "deepseek-r1:671b")
    print(answer)
    chatlog[sender] = chatlog[sender]+answer
    wcf.send_text(answer, sender)
    print('回复完毕')
    
def enableReceivingMsg():
    def innerWcFerryProcessMsg():
        while wcf.is_receiving_msg():
            try:
                msg = wcf.get_msg()
                print(msg.sender) # 这个是发送者的wxid
                processMsg(msg)
            except Empty:
                continue
            except Exception as e:
                print(f"ERROR: {e}")

    wcf.enable_receiving_msg()
    Thread(target=innerWcFerryProcessMsg, name="ListenMessageThread", daemon=True).start()

web_login()
enableReceivingMsg()
wcf.keep_running()

