# 2021-07-05 学习浏览器程序化控制练手之作
# Copyright @WENJUNXIN
# coding:utf-8

import random
import time

from selenium import webdriver

# 这里的路径需要自己修改
driver = webdriver.Edge(executable_path="E:\\Live\\Auto Login\\msedgedriver.exe")
loginTypeIP = 0
schoolNameIP = "北京理工大学"
stuIDIP = "1120212968"
stuPwdIP = "Cxw123456"
courseDoID = 0
courseDoIDSub = 0


# 这里是答题的代码
def answer():
    flag = False
    try:
        while flag == False:
            ansCount = len(driver.find_elements_by_class_name("topic-option-item")) - 1
            ansID = random.randrange(0, ansCount, 1)
            driver.find_element_by_class_name("topic-option-item")[ansID].click()
            flag = isTips("answer")
    except:
        print("答题模块错误")
    try:
        driver.find_element_by_class_name("el-icon.el-icon-arrow-right").click()
    except:
        pass
    # 看完了就继续
    driver.find_elements_by_class_name("clearfix.video")[courseDoIDSub].click()


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
def nextclass(nextClassID):
    driver.find_elements_by_class_name("catalogue_title4.fl.cataloguediv-l")[nextClassID].click()


# 这里是获取课程列表
def getClass(type, num=0):
    if type == 0:
        try:
            while num != len(driver.find_elements_by_class_name("courseName")):
                if driver.find_elements_by_class_name("processNum")[num].text != "100.0%":
                    courseDoID = num
                    break
                num += 1
            return courseDoID
        except:
            print("获取总的课程列表失败")
    else:
        try:
            time.sleep(random.random() + 2 * random.random())
            # 这里是弹窗处理
            try:
                time.sleep(random.random() + 1)
                driver.find_element_by_xpath("//*[@id='app']/div/div[6]/div/div[3]/span/button").click()
            except:
                print("无诚信提示框！")
            try:
                time.sleep(random.random() + 1)
                driver.find_element_by_class_name("iconfont.iconguanbi").click()
            except:
                print("无学习提示框！")
            time.sleep(random.random() + 1)
            # 弹窗处理完毕
            driver.maximize_window()
            # 下面写的有问题，正在思考ing
            # while num <= len(driver.find_elements_by_class_name("clearfix.video")):
            #     if driver.find_elements_by_class_name("processNum")[num].text == "100.0%":
            #         courseDoIDSub = num
            #         break
            #     if num == len(driver.find_elements_by_class_name("clearfix.video")):
            #         courseDoIDSub = num +1
            #         break
            #     num += 1
            return courseDoIDSub
        except:
            print("获取课程子列表失败！")


# 登录模块
def login(loginType, schoolName, stuID, stuPwd):
    if loginType == 0:
        url = "https://onlineh5.zhihuishu.com/onlineWeb.html#/studentIndex"
        driver.get(
            "https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin#studentID")
        try:
            driver.find_element_by_class_name("school-search-ipt").click()
            driver.find_element_by_class_name("school-search-ipt").send_keys(schoolName)
            time.sleep(random.random() + 2)
            driver.find_element_by_xpath(
                "/html/body/div[4]/div/form/div[1]/ul[2]/li[1]/div/div/div/div[1]/ul/li[2]").click()
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
    else:
        pass


# 登录
login(loginTypeIP, schoolNameIP, stuIDIP, stuPwdIP)
# ----------------------------------------------------------------------------------------------------------------------
# 下面获取共享课课程列表以及子课程列表
getClass(type=0)
time.sleep(random.random() + 5)
driver.find_elements_by_class_name("courseName")[courseDoID].click()
time.sleep(random.random() + 1)
getClass(type=1)
# ----------------------------------------------------------------------------------------------------------------------
# 下面正式开始看视频
driver.find_elements_by_class_name("clearfix.video")[courseDoIDSub].click()
# ----------------------------------------------------------------------------------------------------------------------
# 这里自动续看
driver.find_elements_by_class_name("catalogue_title4.fl.cataloguediv-l")[courseDoIDSub].click()
# ----------------------------------------------------------------------------------------------------------------------
# 到这里就完成课程查看了，定义定时器，30分钟后自动关闭浏览器
startTime = time.time()
while startTime + 2000 <= time.time():
    flag = isTips("topic-option-item")
    if flag:
        answer()
        driver.find_element_by_class_name("bigPlayButton.pointer").click()
    else:
        # 获取已播放时间，因为答题后会自动暂停
        playTimeCurrent = str(driver.find_element_by_class_name("currentTime").text)
        totalTime = str(driver.find_element_by_class_name("duration").text)
        if playTimeCurrent == totalTime:
            courseDoIDSub = courseDoIDSub + 1
            nextclass(courseDoIDSub)
    time.sleep(3)
