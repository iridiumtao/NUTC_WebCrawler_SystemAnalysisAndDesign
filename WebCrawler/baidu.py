from selenium import webdriver
import time
import urllib.request
import os
from pathlib import Path
from PIL import Image
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaiduWebCrawler:

    def __init__(self, landscape):
        # 相同路徑
        firstPath = './'

        # 英文景點名

        # 存圖位置
        local_path = firstPath + landscape + '/'

        # 如果沒有資料夾，則創建資料夾
        Path(local_path).mkdir(parents=True, exist_ok=True)

        # 爬取頁面網址 目標元素的xpath
        url = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=' + landscape
        xpath = '//div[@id="imgid"]/div/ul/li/div/a/img'

        # 啟動chrome瀏覽器
        chromeDriver = firstPath + 'chromedriver/chromedriver'  # chromedriver檔案放的位置
        driver = webdriver.Chrome(chromeDriver)

        # 最大化窗口，因為每一次爬取只能看到視窗内的圖片
        driver.maximize_window()

        # 紀錄下載過的圖片網址，避免重複下載
        img_url_dic = {}

        # 瀏覽器打開爬取頁面
        driver.get(url)

        # 模擬滾動視窗瀏覽更多圖片
        pos = 0
        m = 0  # 圖片編號
        for i in range(10000):
            pos += i * 500  # 每次下滾500
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            time.sleep(1)

            # 設定 time out 時間(單位:秒)
            wait = WebDriverWait(driver, 10)

            for element in driver.find_elements_by_xpath(xpath):
                try:
                    img_url = element.get_attribute('src')

                    # 保存圖片到指定路徑
                    if img_url != None and not img_url in img_url_dic:
                        img_url_dic[img_url] = ''
                        m += 1
                        ext = img_url.split('/')[-1]
                        filename = str(m) + '_' + landscape + '_' + ext + '.jpg'
                        print(filename)

                        # 保存圖片
                        urllib.request.urlretrieve(img_url, os.path.join(local_path, filename))

                        self.resize_image(local_path, filename)
                    '''
                    try:
                        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[. = 'lastPage']")))
                    except TimeoutException:
                        print("time out")
                        exit(0)
                    '''

                except OSError as e:
                    print('發生OSError!')
                    print(pos)
                    print(e)
                    break

        driver.close()

    # resize image (不會刪除太小的照片)
    def resize_image(self, local_path, filename):
        print(local_path + filename)
        image = Image.open(local_path + filename)
        if (400, 400) < image.size:
            image.thumbnail((400, 400))
            image.save(local_path + filename)
            print("image resized: " + filename + str(image.size))
