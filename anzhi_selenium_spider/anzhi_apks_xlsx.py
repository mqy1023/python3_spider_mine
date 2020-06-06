
#coding:utf-8
import time

from selenium import webdriver
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

import xlsxwriter
from bs4 import BeautifulSoup
import re
from urllib import request
import os
import pandas as pd

from fake_useragent import UserAgent

# option = webdriver.ChromeOptions()
# option.add_argument('--headless') # 不启动chrome界面模式

def write_excel(typename, name, openurl, downloadcount, company, size, downloadurl):
    # print(typename)
    # print(name)
    # print(openurl)
    # print(downloadcount)
    # print(company)
    # print(downloadurl)
    global row
    row += 1
    sheet.write(row, 0, typename)
    sheet.write(row, 1, name)
    sheet.write(row, 2, openurl)
    sheet.write(row, 3, company)
    sheet.write(row, 4, downloadcount)
    sheet.write(row, 5, size)
    sheet.write(row, 6, downloadurl)

def downloadApk(typename, name, url, downloadcount, downloadid, company, size):
    # http://www.anzhi.com/dl_app.php?s=3216545&n=5
    apkurl = 'http://www.anzhi.com' + '/dl_app.php?s=' + downloadid + '&n=5'  # 通过分析安智市场得到的下载链接
    write_excel(typename, name, url, downloadcount, company, size, apkurl)

def openAndDownloadApk(name, url):
    req = request.Request(url)
    ua = UserAgent()
    req.add_header("User-Agent", ua.random)

    response = request.urlopen(req)
    soup = BeautifulSoup(response, "html.parser")
    url_vals = soup.find(attrs={"class": "app_detail"})  #["onclick"]

    info_details = soup.find(attrs={"id": "detail_line_ul"}).find_all('li')  #["onclick"]

    typename = info_details[0].text.strip()[3:]
    downloadcount = info_details[1].find('span').text.strip()[3:]
    size = info_details[3].find('span').text.strip()[3:] #截取大小
    company = info_details[6].text.strip()[3:] # 作者

    download_elem = soup.find(attrs={"class": "detail_down"}).a['onclick']

    startIndex = download_elem.index("(") + 1
    endIndex = download_elem.index(")")
    download_id = download_elem[startIndex:endIndex]

    downloadApk(typename, name, url, downloadcount, download_id, company, size)


def gethtml(html):
    try:
        # html = browser.page_source       # 获取网页源代码
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        allDivs = soup.find(attrs={"class": "app_list border_three"})

        allItems = allDivs.find_all("li")

        # acount = 1
        for oneItem in allItems:
            # acount += 1
            openUrl = "http://www.anzhi.com" + oneItem.find("span", attrs={"class": "app_name"}).a['href']
            write_excel(" ", " ", openUrl, " ", " ", " ", " ")
            # if oneItem.a is not None:
            #     name = title_div.a.img['title']
            #     url = "http://www.anzhi.com" + title_div.a['href']
                # print(name)
                # print(url)
                # openAndDownloadApk(name, url)
                # if (acount == 10): # 方便测试用
                    # break

        # click_ele = browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
        # click_ele.click()
    except NoSuchElementException as e:
        pass

# 填充满所有信息
def fillAllInfo():
    xlsx1 = '1anzhi.xlsx'
    xlsxData = pd.read_excel(xlsx1)
    # uaVal = UserAgent().random
    for index, row in xlsxData.iterrows():
        openUrl = str(row['详情页链接']).strip() # 打开地址

        req = request.Request(openUrl)
        # req.add_header("User-Agent", uaVal)

        response = request.urlopen(req)
        soup = BeautifulSoup(response, "html.parser")
        url_vals = soup.find(attrs={"class": "app_detail"})  #["onclick"]
        name = soup.find(attrs={"class": "detail_line"}).find('h3').text.strip()

        info_details = soup.find(attrs={"id": "detail_line_ul"}).find_all('li')

        typeName = info_details[0].text.strip()[3:]
        downloadCount = info_details[1].find('span').text.strip()[3:]
        apkSize = info_details[3].find('span').text.strip()[3:-1] #截取大小
        company = info_details[6].text.strip()[3:] # 作者

        download_elem = soup.find(attrs={"class": "detail_down"}).a['onclick']

        startIndex = download_elem.index("(") + 1
        endIndex = download_elem.index(")")
        download_id = download_elem[startIndex:endIndex]

        downloadUrl = 'http://www.anzhi.com/dl_app.php?s=' + download_id + '&n=5'

        if float(apkSize) > 220:
            continue

        xlsxData.iloc[index, 0] = typeName
        xlsxData.iloc[index, 1] = name
        xlsxData.iloc[index, 3] = company
        xlsxData.iloc[index, 4] = downloadCount
        xlsxData.iloc[index, 5] = apkSize
        xlsxData.iloc[index, 6] = downloadUrl
        print(name)
        xlsxData.to_excel('anzhi_all_data.xlsx')


row = 0
file = xlsxwriter.Workbook('1anzhi.xlsx')
sheet = file.add_worksheet()
sheet.write(row, 0, '分类')
sheet.write(row, 1, '名字')
sheet.write(row, 2, '详情页链接')
sheet.write(row, 3, '开发者')
sheet.write(row, 4, '下载量')
sheet.write(row, 5, '安装包大小')
sheet.write(row, 6, '下载地址')

# sel = Selector(text=browser.page_source)
# print(sel.xpath("//span[@class='price J-p-7652013']/text()").extract_first())
# browser.close()

if __name__ == '__main__':
    browser = webdriver.Chrome(executable_path="/Users/eric/envirs/chromedriver")

    for i in range(10,20): # 40 - 100
        htmlUrl = "http://www.anzhi.com/list_1_" + str(i) + "_new.html"
        # print(htmlUrl)
        browser.get(htmlUrl) #
        html = browser.page_source
        gethtml(html)
        time.sleep(0.1)
    browser.close()
    file.close() # 保存xlsx
    time.sleep(0.1)
    fillAllInfo()
    time.sleep(0.1)
    if os.path.exists('1anzhi.xlsx'):
        os.remove('1anzhi.xlsx')
    print('fill end')
