from WebCrawler import WebCrawler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    landmark = 'White Horse Pagoda'

    # 百度
    # url = 'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=' + landscape
    # xpath = '//div[@id="imgid"]/div/ul/li/div/a/img'

    # 搜狐
    url = 'https://pic.sogou.com/pics?query=' + landmark + '&di=2&_asf=pic.sogou.com&w=05009900'
    xpath = '//div[@class="figure-result"]/ul/li/div/a/img'

    var = WebCrawler(url, xpath, landmark)
