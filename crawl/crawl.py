import requests
import re
from selenium import webdriver


def getsource(url, times):
    if times == 3:
        return ""
    browser = webdriver.PhantomJS(executable_path="./phantomjs/bin/phantomjs")
    browser.set_page_load_timeout(10)
    try:
        browser.get(url)
        ans = str(browser.page_source)
        browser.close()
    except:
        browser.close()
        return getsource(url, times + 1)
    return ans


print(getsource("https://item.taobao.com/item.htm?id=562665873311", 0))

'''
    https://rate.taobao.com/feedRateList.htm?auctionNumId=39595400262&currentPageNum=1
'''
