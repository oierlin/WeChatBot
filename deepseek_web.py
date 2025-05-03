from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
input_text = ""
driver = webdriver.Edge()
think = False
search = False

def check_think():
    return think

def check_search():
    return search

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
def web_login(user_name, password):
    driver.get("https://chat.deepseek.com")
    change_button = driver.find_element(By.XPATH, '//div[@class="ds-tab__content" and text()="密码登录"]')
    change_button.click()
    user_input = driver.find_element(By.XPATH, '//input[@class="ds-input__input" and @placeholder="请输入手机号/邮箱地址"]')
    user_input.send_keys(user_name)
    password_input = driver.find_element(By.XPATH, '//input[@class="ds-input__input" and @placeholder="请输入密码"]')
    password_input.send_keys(password)
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

def web_logout():
    try:
        # 点击用户头像或菜单按钮（根据实际网站结构调整XPath）
        user_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="user-avatar"]'))
        )
        user_menu.click()
        
        # 点击登出按钮
        logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[text()="退出登录" or text()="登出"]'))
        )
        logout_button.click()
        
        # 验证是否成功登出（检查登录按钮是否出现）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="登录"]'))
        )
        print("✅ 登出成功！")
    except Exception as e:
        print("❌ 登出失败:", e)

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

