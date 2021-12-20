# 2021-10-28 学习浏览器程序化控制练手之作
# Copyright @WENJUNXIN
# coding:utf-8
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

# 这里的路径需要自己修改。到官网下载好edge的webdriver后方可食用。注意，edge主程序和edge webdriver的版本须一致
driver = webdriver.Edge(executable_path="F:\\Live\\Auto Login\\msedgedriver.exe")
# 目前暂无手机号登录的方法，默认为0
loginTypeIP = 0
# 学校名字，中文，需与智慧树系统内置的一致，分校区尤其要注意
schoolNameIP = "*"
# 智慧树登录的学号
stuIDIP = "*"
# 智慧树登录的密码
stuPwdIP = "*"

debug_mode = True

def printdebug(element):
    if debug_mode:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "DEBUG" + element)


# 这里是判断元素是否存在/点击的代码
def isTips(element, operation=1, list_id=0, find_type="class"):
    # element string 要定位的
    # find_type string 通过class定位/通过tag(标签)定位/通过id定位/通过name定位
    # list_id int elements逻辑顺序
    # operation variable 0代表模糊匹配不点击，2表示模糊匹配点击。1代表精确匹配不点击，3代表精确匹配点击。其他表示判断元素是否存在、可点击，默认模糊匹配。
    time.sleep(random.random() + 2)
    try:
        if operation == 0 or operation == 2:
            # 这个是模糊匹配开头
            if not driver.find_elements_by_xpath("//*[starts-with(@" + find_type + "," + element + ")]") or not element:
                printdebug("模糊匹配失败")
                return False
            elementSelected = driver.find_elements_by_xpath("//*[starts-with(@" + find_type + "," + element + ")]")[list_id]
            printdebug(elementSelected)
            if operation == 2:
                try:
                    elementSelected.click()
                except:
                    printdebug("selenium点击方法失败")
                    driver.execute_script("arguments[0].click();", elementSelected)
        elif operation == 1 or operation == 3:
            if not driver.find_elements_by_xpath("//*[@" + find_type + "='" + element + "']") or not element:
                printdebug("精确匹配失败")
                return False
            elementSelected = driver.find_elements_by_xpath("//*[@" + find_type + "='" + element + "']")[list_id]
            if operation == 3:
                try:
                    elementSelected.click()
                except:
                    printdebug("selenium点击方法失败")
                    driver.execute_script("arguments[0].click();", elementSelected)
        else:
            if isTipsClickable(element, list_id, find_type):
                pass
            else:
                raise Exception("元素不可见或不可点击！可能存在其他提示框！")
        return True
    except:
        print(element + "不存在或点击失败！")
        return False


def isTipsClickable(element, list_id=0, find_type="class"):
    # element string 要定位的
    # find_type string 通过class定位/通过tag(标签)定位/通过id定位/通过name定位
    # list_id int elements逻辑顺序
    # operation variable 0代表不点击
    time.sleep(random.random() + 2)
    try:
        if not driver.find_elements_by_xpath("//*[starts-with(@" + find_type + "," + element + ")]") or not element:
            return False
        elementSelected = driver.find_elements_by_xpath("//*[starts-with(@" + find_type + "," + element + ")]")[list_id]
        if elementSelected.is_displayed() and elementSelected.is_enabled():
            return True
        else:
            return False
    except:
        return False


class lesson:
    # 这里是获取课程列表
    def __init__(self, _loginType, _schoolName, _stuID, _stuPwd):
        self.__logintype__ = _loginType
        self.__schoolName__ = _schoolName
        self.__stuID__ = _stuID
        self.__stuPwd__ = _stuPwd
        self.__rndList__ = [0, 1, 2, 3, 4]
        self.__quized__ = False
        self.__FirstPlay__ = True
        self.__currentCourseID__ = 0
        self.__currentSubCourseID__ = 0
        self.__totalSubCourseCount__ = 0

    def tips(self, tips_string):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), tips_string)

    def warn(self, warn_string):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), warn_string)
        exit(1)

    def boxing(self):
        # 处理开始的时候的弹窗
        # ver 3.0.211220
        try:
            if isTips("el-button btn el-button--primary", 3):
                self.tips("关闭智慧树警告成功！")
            else:
                self.tips("关闭智慧树警告失败！可能不存在该窗口！")
            time.sleep(3)
            if isTips("iconfont iconguanbi", 3):
                self.tips("关闭学前必读成功！")
            else:
                self.tips("关闭学前必读失败！可能不存在该窗口！")
            if isTips("fl cataloguediv-c", 5):
                self.tips("弹窗处理完毕！")
            else:
                self.tips("似乎出现了别的弹窗！请在10s内手动关闭，否则程序将自动退出！")
                if isTips("el-dialog__close el-icon el-icon-close", 3):
                    self.tips("关闭智慧树警告成功！")
                else:
                    self.tips("关闭智慧树警告失败！可能不存在该窗口！")
                time.sleep(3)
                if isTips("iconfont iconguanbi", 3):
                    self.tips("关闭学前必读成功！")
                else:
                    self.tips("关闭学前必读失败！可能不存在该窗口！")
                if isTips("fl cataloguediv-c", 5):
                    self.tips("弹窗处理完毕！")

                time.sleep(10)
                if isTips("fl cataloguediv-c", 5):
                    self.tips("处理弹窗完毕！开始看视频！")
                    return True
                else:
                    raise Exception("似乎出现了别的弹窗！")
        except:
            self.warn("处理弹窗出现未知错误！")

    def login(self):
        # 登录模块
        # ver 4.0.211220
        if self.__logintype__ == 0:
            url = "https://onlineh5.zhihuishu.com/onlineWeb.html#/studentIndex"
            driver.get(
                "https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin#studentID")
            try:
                driver.find_element_by_class_name("school-search-ipt").click()
                driver.find_element_by_class_name("school-search-ipt").send_keys(self.__schoolName__)
                time.sleep(random.random() + 2)
                driver.find_element_by_xpath(
                    "/html/body/div[4]/div/form/div[1]/ul[2]/li[1]/div/div/div/div[1]/ul/li[2]").click()
                time.sleep(random.random() + 1)
                driver.find_element_by_id("clCode").click()
                time.sleep(random.random() + 1)
                driver.find_element_by_id("clCode").send_keys(self.__stuID__)
                time.sleep(random.random() + 2)
                driver.find_element_by_id("clPassword").click()
                time.sleep(random.random() + 1)
                driver.find_element_by_id("clPassword").send_keys(self.__stuPwd__)
                time.sleep(random.random() + 2)
                driver.find_element_by_class_name("wall-sub-btn").click()
                Wait(driver, 10).until(EC.presence_of_element_located((By.ID, "sharingClass")))
            except:
                print("登陆失败！")
            finally:
                if url == driver.current_url:
                    driver.get(url)
                    time.sleep(5)
        else:
            # 这儿还没写，主要是普通登录我没用过。除了学校没人用这个了吧
            pass

    def getClass(self, id=0):
        # 自动从第一个开始，如需自定义请加参数.
        _num = 0
        try:
            while _num != len(driver.find_elements_by_class_name("courseName")):
                if driver.find_elements_by_class_name("processNum")[_num].text != "100.0%":
                    self.__currentCourseID__ = _num
                    break
                _num += 1
            self.tips("主页面课程列表获取成功！")
        except:
            self.warn("主页面课程列表获取Failed！")
        isTips("courseName", 3, self.__currentCourseID__)

        self.boxing()  # 这里处理弹窗！
        try:
            self.__totalSubCourseCount__ = len(
                driver.find_elements_by_xpath("//*[starts-with(@class,'clearfix video')]"))
            self.__currentSubCourseID__ = len(driver.find_elements_by_xpath("//*[@class='fl time_icofinish']")) - 1
            self.tips("课时列表获取成功！")
        except:
            self.warn("课时列表获取Failed！")

    # 这里是下一节课的代码
    def nextclass(self):
        self.__currentSubCourseID__ += 1
        isTips("clearfix video", 2, self.__currentSubCourseID__)
        self.tips(["下一节课了", self.__currentSubCourseID__, self.__totalSubCourseCount__])

    # 这里是答题的代码
    def answer(self, choice):
        if choice == 0 or choice == 1:
            rndList = self.__rndList__[0:1]
        else:
            _lenAns = len(driver.find_elements_by_xpath("//*[@class,'icon topic-option']"))-1
            rndList = self.__rndList__[0:_lenAns]

        try:
            while not isTips("answer"):
                random.shuffle(rndList)

                # 这里还得改
                if choice == 2:
                    for i in range(0, _lenAns):
                        driver.find_element_by_class_name("topic-option-item")[rndList[i]].click()
                        if isTips("answer"):
                            break
                else:
                    driver.find_element_by_class_name("topic-option-item")[0].click()

            if isTips("answer"):
                driver.find_element_by_class_name("btn").click()
            self.tips("答题完毕！")
        except:
            self.warn("答题程序错误!")
        # 看完了就继续

    def watchvideo(self):
        isTips("clearfix video",2,self.__currentSubCourseID__)

        totalTime = driver.execute_script('return ablePlayerX("container").getDuration()')

        time.sleep(5)
        playTimeCurrent = driver.execute_script('return ablePlayerX("container").getPosition()')
        if playTimeCurrent == totalTime:
            driver.execute_script('ablePlayerX("container").play()')
        #     这里是可能一开始不播放

        while playTimeCurrent <= totalTime:
            playTimeCurrent = driver.execute_script('return ablePlayerX("container").getPosition()')
            if isTips("topic-option-item"):
                quiz = driver.find_element_by_class_name("title-tit").text
                if quiz == "【判断题】":
                    quizType = 0
                elif quiz == "【单项选择题】":
                    quizType = 1
                elif quiz == "【多项选择题】":
                    quizType = 2
                self.answer(quizType)
                self.__quized__ = True
                driver.execute_script('ablePlayerX("container").play()')
            else:
                time.sleep(5)
        playTimeCurrent = driver.execute_script('return ablePlayerX("container").getPosition()')

        # 历史代码，不知道干嘛的
        # if playTimeCurrent == totalTime and self.__quized__:
        #     self.tips("发生已知已知错误，刷新重新看！")
        #     driver.execute_script("location.reload()")


happy = lesson(loginTypeIP, schoolNameIP, stuIDIP, stuPwdIP)
happy.login()
happy.getClass()
happy.watchvideo()
