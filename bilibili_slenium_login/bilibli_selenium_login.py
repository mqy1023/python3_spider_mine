import time
from PIL import Image
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



class bilibili_login():
    #初始化
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.left = 60
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Chrome/37.0.0.0"')
        self.driver = webdriver.Chrome(executable_path="/Users/eric/envirs/chromedriver")
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver,5)
        #用户信息
        self.username = 'your username' # 输入用户名
        self.password = 'your password' # 输入密码

    #输入用户名和密码
    def input_name_password(self):
        self.driver.get(self.url)
        self.user = self.wait.until(EC.presence_of_element_located((By.ID,'login-username')))
        self.passwd = self.wait.until(EC.presence_of_element_located((By.ID,'login-passwd')))
        self.user.clear()
        self.user.send_keys(self.username)
        self.passwd.clear()
        self.passwd.send_keys(self.password)
        time.sleep(1)

    #获取登录按钮并点击获取图片
    def click_login_button(self):
        login_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'a.btn.btn-login')))
        login_button.click()
        time.sleep(1)
        # 刷新，更像人工操作一点
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_refresh_1'))).click()
        time.sleep(1)
        #缺口图片保存
        gapimag = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"geetest_canvas_bg")))
        time.sleep(1)
        gapimag.screenshot(r'./imag1.png')
        #设置完整图片可见
        js = 'var change = document.getElementsByClassName("geetest_canvas_fullbg");change[0].style = "display:block;"'
        self.driver.execute_script(js)
        time.sleep(1)
        # 完整图片保存
        fullimg = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))
        time.sleep(1)
        fullimg.screenshot(r'./imag2.png')

    #判断两张图片是否相同
    def is_smilar(self,imag1,imag2,x,y):
        pixel1 = imag1.load()[x,y]
        pixel2 = imag2.load()[x,y]
        threhold = 60
        if abs(pixel1[0] - pixel2[0])< threhold and abs(pixel1[1] - pixel2[1]) < threhold and abs(pixel1[2] - pixel2[2]) < threhold:
            return True
        else:
            return False
    #找到缺口位置
    def get_diff_location(self):
        imag1 = Image.open('imag1.png')
        imag2 = Image.open('imag2.png')
        for x in range(self.left,imag1.size[0]):
            for y in range(imag1.size[1]):
                if not self.is_smilar(imag1,imag2,x,y):
                    print(x,y)
                    return x
    #移动滑块
    def move_slider(self,track):
        slider = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.geetest_slider_button')))
        ActionChains(self.driver).click_and_hold(slider).perform()
        time.sleep(0.6)
        ActionChains(self.driver).move_by_offset(xoffset=0.70 * track, yoffset=0).perform()
        time.sleep(0.3)
        ActionChains(self.driver).move_by_offset(xoffset=0.30 * track, yoffset=0).perform()
        time.sleep(0.5)  # 0.70和0.30（0.7+0.3=1）可以是其他随意数值，也可以生成随机数, 模拟成人来操作
        ActionChains(self.driver).release().perform()  # 松开鼠标
    def crack(self):
        self.input_name_password()
        self.click_login_button()
        gap = self.get_diff_location()
        gap = gap - 6
        self.move_slider(gap)
        # time.sleep(2)
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # self.driver.execute_script("alert('To Bottom')")
        time.sleep(5)
        # tree = self.driver.find_element_by_xpath("//div[@class='zone-list-box']")
        # tree = tree.get_attribute('innerHTML')
        # tree = etree.HTML(tree)
        # text = tree.xpath('string(.)')
        # print(text)
if __name__ == '__main__':
    bilibili = bilibili_login()
    bilibili.crack()
