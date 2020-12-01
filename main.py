from WebCrawler import WebCrawler

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    landmark = '白馬塔'
    searchEngine = 'Bing'

    if searchEngine == '百度':
        # 百度
        url = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=' \
              + landmark
        xpath = '//div[@id="imgid"]/div/ul/li/div/a/img'
    elif searchEngine == '搜狐':
        # 搜狐
        url = 'https://pic.sogou.com/pics?query=' + landmark + '&di=2&_asf=pic.sogou.com&w=05009900'
        xpath = '//div[@class="figure-result"]/ul/li/div/a/img'
    elif searchEngine == 'Google':
        # Google
        url = 'https://www.google.com.tw/search?q=' + landmark + '&tbm=isch&hl=zh-TW&tbs&sa=X&ved=0CAEQpwVqFwoTCKj3nbCZm-0CFQAAAAAdAAAAABAC&biw=1279&bih=977'
        xpath = '//img[@class="rg_i Q4LuWd"]'
    else:
        # Bing
        url = 'https://www.bing.com/images/search?q=' + landmark + '&form=HDRSC2&first=1&tsc=ImageBasicHover&scenario=ImageBasicHover'
        xpath = '//*[@id="mmComponent_images_2"]/ul/li/div/div/a/div/img'

    var = WebCrawler(url, xpath, landmark)
