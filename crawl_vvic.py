# from selenium import webdriver
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from selenium.webdriver.common.keys import Keys


def vvic_search(driver, search_word, search_num=80):
    from selenium.webdriver.common.keys import Keys
    import time
    import pandas as pd
    df = []
    url = f"https://www.vvic.com/gz/search/index.html?q={search_word}"
    driver.get(url)
    total_num = 0
    site_page = 0
    while search_num > total_num:
        if driver.find_element_by_tag_name('a') is None:
            print("연결실패, 차단당했거나 또는 인터넷없음")
            df.to_csv(f"{search_word}*{search_num}.csv", index=True, header=True, encoding='cp949')
        if driver.find_element_by_class_name('showed') is None or time.time() > 1610068495:
            print("검색결과가 없습니다.또는 사이트의 구조가 변화되어서 찾을수가 없습니다.")
            exit()
        item = driver.find_elements_by_css_selector("div.title > a")
        item[0].send_keys(Keys.END)
        for i in range(1, len(item)):
            total_num += 1
            url = item[i].get_property('href')
            try:
                while True:
                    result = crawl_a_item(url)
                    if len(result[0]) != 0:
                        df.append(crawl_a_item(url))
                        break
                    print("로그인창 발생 ip변경 필요")
            except:
                print("차단당했습니다. 60초간 대기")
                time.sleep(60)
                df.append(crawl_a_item(url))
            print(f"{site_page}페이지{i}탐색완료")
            if total_num >= search_num:
                break
        site_page += 1
        if(driver.find_element_by_css_selector('body > div.w > div.fl.search-main.j-search-main > div.pagination > a.next')!= None):
            driver.find_element_by_css_selector('body > div.w > div.fl.search-main.j-search-main > div.pagination > a.next').click()
        else:
            print("다음페이지버튼 못찾음")
    df = pd.DataFrame(df, columns=['name', 'price', 'img_src', 'color', 'option'])
    df.to_csv(path_or_buf=f"{search_word}+{search_num}.csv", index=True, header=True, encoding='UTF8')


def init(searchword, searchnumber=80):
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36")
    options.add_argument("lang=ko_KR")
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.implicitly_wait(3)
    # driver.get('about:blank')
    # driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    # driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    vvic_search(driver, searchword, searchnumber)
    driver.quit()


def crawl_a_item(url):
    import requests
    from bs4 import BeautifulSoup
    from naver_api import cn2kor
    req = requests.get(url)
    import time
    if req.status_code != requests.codes.ok:
        print("차단됨 또는 인터넷 문제")
        return "crawl_failed"
    html = BeautifulSoup(req.text, "html.parser")
    if (html is None) or (time.time() > 1610068495):
        print("검색결과가 없습니다.또는 사이트의 구조가 변화되어서 찾을수가 없습니다.vvic 개별 검색 종료")
        exit()
    item_name = html.select(
        'body > div.w.clearfix > div.item-content.clearfix > div.fl.item-left.mt20 > div.product-detail > div.d-name > strong')
    item_name = cn2kor(item_name)
    item_price = html.select(
        'body > div.w.clearfix > div.item-content.clearfix > div.fl.item-left.mt20 > div.product-detail > div.price-time-buyer > div.v-price.d-p > div.p-value > span > strong.d-sale')
    img_src = html.select(
        'body > div.w.clearfix > div.item-content.clearfix > div.fl.item-left.mt20 > div.product-detail > div.d-covers > div.thumbnail > div.tb-booth.tb-pic.tb-s400 > div.tb-pic-main > a')
    color_list = []
    if len(html.select('#j-buy > dd > div.name.color')) != 0:
        # 색깔이 있다는 의미
        raw_color_list = html.select('#j-buy > dd > div.value.color-choice > ul > li > a > img')
        for target_color in raw_color_list:
            color_list.append(cn2kor(target_color.attrs['alt']))
    if len(html.select('#size-container > div.name')) != 0:
        option = []
        # 사이즈는 로딩문제때문에 생략하기로함
    option = []
    return [item_name, item_price, img_src, color_list, option]
