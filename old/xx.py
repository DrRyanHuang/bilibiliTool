# 本代码无效, 用于测试


from selenium import webdriver
from selenium.webdriver.common.by import By


browser = webdriver.Chrome(executable_path='./chromedriver.exe')
browser.get('https://passport.bilibili.com/login')

login_input = browser.find_element_by_id('login-username') # 找到搜索框
login_input.send_keys('iPhone') # 传送入关键词
login_input.clear() # 清空搜索框

password_input = browser.find_element_by_id('login-passwd') # 找到搜索框
password_input.send_keys('iPhone') # 传送入关键词
password_input.clear() # 清空搜索框

#button = browser.find_element_by_class_name('btn btn-reg') # 找到搜索按钮
# 行吧可以找他的XPATH
xpath = '//*[@id="geetest-wrap"]/div/div[5]/a[1]'
login_button = browser.find_element_by_xpath(xpath)
login_button.click()