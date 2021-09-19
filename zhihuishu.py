# 2021-07-05 学习浏览器程序化控制练手之作
# Copyright @WENJUNXIN
# coding:utf-8

import random
import time

from selenium import webdriver

# 这里的路径需要自己修改
driver = webdriver.Edge(executable_path="E:\\Live\\Auto Login\\msedgedriver.exe")
stuID = "1120212968"
stuPwd = "Cxw123456"
courseList = []
classList = []
num = 0


# 这里是答题的代码
def answer():
    try:
        ansCount = len(driver.find_elements_by_class_name("topic-option-item")) - 1
        ansID = random.randrange(0, ansCount, 1)
        driver.find_element_by_class_name("topic-option-item")[ansID].click()
    except:
        print("答题模块错误")
    try:
        driver.find_element_by_class_name("el-icon.el-icon-arrow-right").click()
    except:
        pass
    driver.find_element_by_xpath("//*[@id='app']/div/div[7]/div/div[3]/span/div").click()
    driver.find_element_by_class_name("bigPlayButton.pointer").click()

# 这里是判断元素是否存在的的代码
def isTips(element):
    flag = True
    try:
        driver.find_element_by_css_selector(element)
        return flag
    except:
        flag = False
        return flag

# 这里是下一个视频的代码
def nextclass(currentClassID):
    pass

# Login in
url = "https://onlineh5.zhihuishu.com/onlineWeb.html#/studentIndex"
driver.get("https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin#studentID")
try:
    driver.find_element_by_class_name("school-search-ipt").click()
    driver.find_element_by_class_name("school-search-ipt").send_keys("北京理工大学")
    time.sleep(random.random() + 2)
    driver.find_element_by_xpath("/html/body/div[4]/div/form/div[1]/ul[2]/li[1]/div/div/div/div[1]/ul/li[2]").click()
    time.sleep(random.random() + 1)
    driver.find_element_by_id("clCode").click()
    time.sleep(random.random() + 1)
    driver.find_element_by_id("clCode").send_keys(stuID)
    time.sleep(random.random() + 2)
    driver.find_element_by_id("clPassword").click()
    time.sleep(random.random() + 1)
    driver.find_element_by_id("clPassword").send_keys(stuPwd)
    time.sleep(random.random() + 2)
    driver.find_element_by_class_name("wall-sub-btn").click()
    while driver.current_url != url:
        pass
except:
    print("登陆失败！")
finally:
    driver.get(url)
    time.sleep(10)
# 下面获取共享课课程列表
try:
    driver.find_element_by_id("sharingClass").click()
    time.sleep(random.random() + 2 * random.random())
    driver.find_element_by_css_selector("[class='haveInhand borderBlack']").click()
    time.sleep(random.random() + 2 * random.random())
    courseList = driver.find_elements_by_class_name("courseName")
    while num != len(courseList):
        if driver.find_elements_by_class_name("processNum")[num].text != "100.0%":
            courseDoID = num
            break
        num += 1
except:
    print("获取课程列表失败！")
# 下面正式开始看视频
driver.find_element_by_class_name("processNum")[num].click()
try:
    time.sleep(random.random() + 1)
    driver.find_element_by_css_selector("[class='el-button btn el-button--primary']").click()
except:
    print("无诚信提示框！")
try:
    time.sleep(random.random() + 1)
    driver.find_element_by_css_selector("[class='iconfont iconguanbi']").click()
except:
    print("无学习提示框！")
time.sleep(random.random() + 1)
# 这里自动续看
driver.find_element_by_class_name("progress-num").click()
# 到这里就完成课程查看了，定义定时器，30分钟后自动关闭浏览器
currentTime = time.time()
while currentTime + 5 <= time.time():
    flag = isTips()
    if flag:
        answer()
        # driver.find_element_by_class_name("bigPlayButton.pointer").click()
    else:
        # 获取已播放时间，因为答题后会自动暂停
        playTimeCurrent = str(driver.find_element_by_class_name("currentTime").text)
        totalTime = str(driver.find_element_by_class_name("duration").text)
        if playTimeCurrent == totalTime:
            nextClass()
    time.sleep(5)
