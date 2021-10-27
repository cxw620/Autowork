# 2021-10-28 学习浏览器程序化控制练手之作
# Copyright @WENJUNXIN
# coding:utf-8
import random
import time

from selenium import webdriver

# 这里的路径需要自己修改。到官网下载好edge的webdriver后方可食用。注意，edge主程序和edge webdriver的版本须一致。路径的\需要用\转义变成\\。
driver = webdriver.Edge(executable_path="E:\\Live\\Auto Login\\msedgedriver.exe")
# 目前暂无手机号登录的方法，默认为0
loginTypeIP = 0
# 学校名字，中文，需与智慧树系统内置的一致，分校区尤其要注意
schoolNameIP = "*"
# 智慧树登录的学号
stuIDIP = "*"
# 智慧树登录的密码
stuPwdIP = "*"


# 这里是判断元素是否存在/点击的代码
def isTips(element, operation=0, list_id=0, find_type="class"):
    # element string 要定位的
    # find_type string 通过class定位/通过tag(标签)定位/通过id定位/通过name定位
    # list_id int elements逻辑顺序
    # operation variable 0代表不点击
    time.sleep(random.random() + 2)
    try:
        if not driver.find_elements_by_xpath("//*[@" + find_type + "='" + element + "']") or not element:
            return False
        if operation == 1:
            driver.find_elements_by_xpath("//*[@" + find_type + "='" + element + "']")[list_id].click()
        return True
    except:
        print(element + "不存在或点击失败！")
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
        self.__totalCourseCount__ = 0

    def tips(self, tips_string):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), tips_string)

    def warn(self, warn_string):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), warn_string)
        exit(1)

    def boxing(self):
        try:
            if isTips("", 1):
                self.tips("关闭学前必读成功！")
            else:
                self.tips("关闭学前必读失败！可能不存在该窗口！")
        except:
            self.warn("关闭诚信提示失败！未知错误！")
        time.sleep(3)
        try:
            if isTips("iconfont iconguanbi", 1):
                self.tips("关闭学前必读成功！")
            else:
                self.tips("关闭学前必读失败！可能不存在该窗口！")
        except:
            self.warn("关闭学前必读失败！未知错误！")

    def login(self):
        # 登录模块
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
                while driver.current_url != url:
                    pass
            except:
                print("登陆失败！")
            finally:
                driver.get(url)
                time.sleep(10)
        else:
            # 这儿还没写，主要是普通登录我没用过。除了学校没人用这个了吧
            pass

    def getClass(self, type):
        # type0为主页面课程获取
        if type == 0:
            self.__num__ = 0
            try:
                while self.__num__ != len(driver.find_elements_by_class_name("courseName")):
                    if driver.find_elements_by_class_name("processNum")[self.__num__].text != "100.0%":
                        break
                    self.__num__ += 1
                    self.tips("主页面课程列表获取成功！")

            except:
                self.warn("主页面课程列表获取Failed！")

        # type1为课程内部节数获取
        elif type == 1:
            try:
                self.__totalCourseCount__ = len(driver.find_elements_by_class_name("catalogue_title"))
                self.__currentCourseID__ = len(driver.find_elements_by_xpath("//*[@class='fl time_icofinish']")) - 1
                self.tips("课时列表获取成功！")
            except:
                self.warn("课时列表获取Failed！")

    # 这里是下一节课的代码
    def nextclass(self):
        self.__currentCourseID__ = self.__currentCourseID__ + 1
        isTips("clearfix video", 1)
        self.tips(["下一节课了", self.__currentCourseID__, self.__totalCourseCount__])

    # 这里是答题的代码
    def answer(self, choice):
        ansFlag = False

        if choice == 0:
            rndList = self.__rndList__[0:1]
        else:
            rndList = self.__rndList__[0:3]

        try:
            while ansFlag == False:
                random.shuffle(rndList)

                # 这里还得改
                if choice == 2:
                    choice = 4
                    for i in range(0, choice):
                        driver.find_element_by_class_name("topic-option-item")[rndList[i]].click()
                        if isTips("answer"):
                            break
                else:
                    for i in range(0, choice):
                        driver.find_element_by_class_name("topic-option-item")[rndList[i]].click()

                ansFlag = isTips("answer")
                if ansFlag:
                    driver.find_element_by_class_name("btn").click()

            self.tips("答题完毕！")
        except:
            self.warn("答题程序错误!")
        # 看完了就继续

    def watchvideo(self):
        if self.__FirstPlay__:
            driver.find_elements_by_class_name("courseName")[self.__num__].click()
            time.sleep(5)
            self.boxing()  # 这里处理弹窗！
            time.sleep(1)
            driver.find_elements_by_xpath("//*[@class='clearfix video']")[self.__currentCourseID__].click()
        # driver.execute_script('ablePlayerX("container").play()')
        startTime = time.time()
        break_all = False
        while startTime + 35 * 60 <= time.time():
            currentTime = time.time()
            while currentTime + 30 <= time.time():
                flag = isTips("topic-option-item")
                if flag:
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
                    # 获取已播放时间，因为答题后会自动暂停
                    playTimeCurrent = driver.execute_script('return ablePlayerX("container").getPosition()')
                    totalTime = driver.execute_script('return ablePlayerX("container").getDuration()')
                    if playTimeCurrent == totalTime:
                        time.sleep(3)
                        playTimeCurrent = driver.execute_script('return ablePlayerX("container").getPosition()')
                        totalTime = driver.execute_script('return ablePlayerX("container").getDuration()')
                        if playTimeCurrent == totalTime and self.__quized__:
                            self.tips("发生已知已知错误，刷新重新看！")
                            driver.execute_script("location.reload()")
                            break_all = True
                            break
                        else:
                            if not self.__quized__:
                                self.warn("致命未知错误，退出！")
                            else:
                                self.nextclass()
                    else:
                        driver.execute_script('ablePlayerX("container").play()')
                time.sleep(2)
            if break_all:
                break


happy = lesson(loginTypeIP, schoolNameIP, stuIDIP, stuPwdIP)
happy.login()
happy.getClass(0)
happy.watchvideo()
