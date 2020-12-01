# coding=UTF-8

'''
Author: OFDL.Dev HYT
Create on: 11/26/2020
Description: Please put the chromedriver.exe in the same directory and don't rename it.
'''

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import os, time
import sys


class se(object):
    def __init__(self, name, url, img_xpath, end_xpath, btn_xpath, driver):
        self.cnt = 0
        self.name = name  # name: se名稱
        self.url = url  # url: se網址
        self.img_xpath = img_xpath  # img_xpath: 圖片xpath
        self.end_xpath = end_xpath  # end_xpath[判斷標籤, 屬性, 數值]: 判斷load到最底, 當標籤的屬性等於數值時成立
        self.btn_xpath = btn_xpath  # btn_xpath按鈕標籤: 點"顯示更多按鈕", 當按鈕顯示時點擊
        self.driver = driver  # driver: chromedriver物件

    def load_full(self):  # load到最底
        print('正在等待頁面載入', end='', flush=True)
        while True:
            # 滑到頁底
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                # 到最底時 break
                if self.driver.find_element_by_xpath(self.end_xpath[0]).get_attribute(self.end_xpath[1]) == \
                        self.end_xpath[2]:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    break
            except NoSuchElementException:
                break
            # except Exception as e:
            # pass
            # print(e)

            # 點"顯示更多按鈕"
            try:
                if self.btn_xpath != None:
                    if self.driver.find_element_by_xpath(self.btn_xpath).is_displayed():
                        self.driver.find_element_by_xpath(self.btn_xpath).click()
            except NoSuchElementException:
                pass
            # except Exception as e:
            # pass
            # print(e)

    def download_img(self):  # 下載圖片
        # 尋找img標籤
        elements = self.driver.find_elements_by_xpath(self.img_xpath)

        # 等待Response
        total = 0
        print('\r正在等待Response', end='', flush=True)
        while total != len(elements):
            total = len(elements)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            elements = self.driver.find_elements_by_xpath(self.img_xpath)

        # 下載圖片
        for element in elements:
            try:
                # 用src屬性找圖片網址
                img_url = element.get_attribute('src')
                if img_url != None:
                    urllib.request.urlretrieve(img_url,
                                               os.path.join(save_path, self.name + '_' + str(self.cnt + 1) + '.jpg'))
                    self.cnt += 1
                else:
                    # 若src找不到, 換用data-src找(for google)
                    img_url = element.get_attribute('data-src')
                    if img_url != None:
                        urllib.request.urlretrieve(img_url, os.path.join(save_path,
                                                                         self.name + '_' + str(self.cnt + 1) + '.jpg'))
                        self.cnt += 1
            except Exception as e:
                pass
            print('\r%4d / %4d ( 已下載圖片數 / 已找到img標籤數 )' % (self.cnt, total), end='', flush=True)
        print(end='\n')

    def run(self):
        print('\n' + self.name + '\n')
        self.driver.get(self.url)
        self.load_full()
        self.download_img()
        return self.cnt


if __name__ == '__main__':
    total = 0
    # 輸入關鍵字
    searchList = []
    print("請輸入關鍵字：")
    while True:
        searchList.append(input())
        if searchList[-1] == "END_OF_THE_LIST":
            searchList = searchList[:-1]
            break

    print(searchList)

    for search in searchList:
        # 存圖路徑
        save_path = './train/'
        # 建立folder
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        save_path += search + '/'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        search = search.replace(' ', '+')

        # 啟動chrome
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver/chromedriver')
        driver.maximize_window()

        # 建立search engine
        # google = se('google',
        #             'https://www.google.com.tw/search?q=' + search + '&tbm=isch&hl=zh-TW&tbs&sa=X&ved=0CAEQpwVqFwoTCKj3nbCZm-0CFQAAAAAdAAAAABAC&biw=1279&bih=977',
        #             '//img[@class="rg_i Q4LuWd"]',
        #             ['//*[@id="islmp"]/div/div/div/div/div[4]', 'data-status', '3'],
        #             '//input[@class="mye4qd"]',
        #             driver
        #             )
        # total += google.run()

        # bing = se('bing',
        #           'https://www.bing.com/images/search?q=' + search + '&form=IRFLTR&first=1&tsc=ImageBasicHover&scenario=ImageBasicHover',
        #           '//img[@class="mimg"]',
        #           ['//*[@id="mmComponent_images_2_exp"]', 'class', 'expandButton txtaft disabled'],
        #           '//*[@class="btn_seemore cbtn mBtn"]',
        #           driver
        #           )
        # total += bing.run()

        yahoo = se('yahoo',
                   'https://tw.images.search.yahoo.com/search/images;_ylt=AwrtahNbVr5f3FUA9xJr1gt.;_ylu=Y29sbwN0dzEEcG9zAzEEdnRpZANDMTExMF8xBHNlYwNwaXZz?p=' + search + '&fr2=piv-web&fr=yfp-search-sb',
                   '//div/div/section/div/ul/li/a/img',
                   ['//button[@name="more-res"]', 'style', 'display: none;'],
                   '//button[@name="more-res"]',
                   driver
                   )
        total += yahoo.run()

        # duckduckgo稍慢
        # duckduckgo = se('duckduckgo',
        #                 'https://duckduckgo.com/?q=' + search + '&t=h_&iax=images&ia=images',
        #                 '//img[@class="tile--img__img  js-lazyload"]',
        #                 ['//div[@class="footer"]', 'style', 'display: block;'],
        #                 None,
        #                 driver
        #                 )
        # total += duckduckgo.run()

        # baidu稍慢
        # baidu = se( 'baidu',
        #     'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=' + search,
        #     '//*[@id="imgid"]/div/ul/li/div/a/img',
        #     ['//*[@id="loading"]', 'style', 'display: none;'],
        #     None,
        #     driver
        #     )
        # total += baidu.run()

        '''
        # yandex超慢 不準
        yandex = se( 'yandex',
            'https://yandex.com/images/search?text=' + search,
            '//img[@class="serp-item__thumb justifier__thumb"]',
            ['//div[5]/div[1]/div[1]/div[4]', 'class', 'competitors competitors_theme_light i-bem competitors_js_inited'],
            None,
            driver
            )
        total += yandex.run()
        '''
        driver.close()

        print(f'\n--------------------------------------------\n\n{search} 總下載數: ' + str(total))
