import os
pw = "R+3hC-9$zbZ.JmR"
search_word = "外套"


def crawl_a_item_taobao_request(id):
    # id,name,price,size,img_src
    # 현재는 미사용
    import requests
    import time
    from bs4 import BeautifulSoup
    from naver_api import cn2kor
    url = f"https://item.taobao.com/item.htm?id={id}"
    req = requests.get(url)
    if req.status_code != requests.codes.ok and time.time() > 1610629435:
        print("차단됨 또는 인터넷 문제")
    html = BeautifulSoup(req.text, "html.parser")
    name = html.select('#J_Title > h3')[0].text.strip()
    name = cn2kor(name)
    price = html.select('#J_StrPrice > em.tb-rmb-num')
    price = price[0].text
    size = html.select(
        '#J_isku > div > dl.J_Prop.J_TMySizeProp.tb-prop.tb-clear.J_Prop_measurement > dd > ul > li > a > span')
    if len(size) == 0:
        size = "null"
    else:
        for i in range(len(size)):
            size[i] = size[i].text
    color = html.select('#J_isku > div > dl.J_Prop.tb-prop.tb-clear.J_Prop_Color > dd > ul > li > a > span')
    if len(color) == 0:
        color = "null"
    else:
        for i in range(len(color)):
            color[i] = color[i].text
            color[i] = cn2kor(color[i])
    img_src = html.select('#J_ImgBooth')[0]['src'][2:]

    return [id, name, price, size, img_src]


def crawl_items_taobaoWselenium(search_word):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import os
    url = f"https://taobao.com/"
    driver = init_webdriver(url)
    driver.find_element_by_css_selector('#mq').send_keys(search_word)
    driver.find_element_by_css_selector('#mq').send_keys(Keys.ENTER)
    loginpage = driver.current_url
    driver.find_element_by_css_selector('#fm-login-id').send_keys("lori2mai11ya")
    driver.find_element_by_css_selector('#fm-login-password').send_keys("R+3hC-9$zbZ.JmR")
    driver.find_element_by_css_selector('#fm-login-password').send_keys(Keys.ENTER)
    for i in range(10):
        wait(0.5)
        if (driver.current_url == loginpage):
            print("crawl_items_taobao:err_1 로그인 실패 계정봉인확인 필요")
        else:
            break
    while (True):
        items = driver.find_elements_by_css_selector('div.pic > a')
        print("b")
        if (len(items) != 0):
            break
        wait(0.1)
    if (not os.path.exists(f"./{search_word}")):
        os.makedirs(f"./{search_word}")
        os.chdir(f"./{search_word}")
    else:
        number = 1
        while(True):
            if num >100:
                break
            if(not os.path.exists(f"./{search_word}_{number}")):
                os.makedirs(f"./{search_word}_{number}")
                break
            else:
                number += 1
        os.chdir(f"./{search_word}_{number}")
    is_tmall = driver.find_elements_by_css_selector('div.item.J_MouserOnverReq > div > div.row.row-4.g-clearfix > div > ul')
    link = []
    for i in range(len(items)):
        link.append(items[i].get_attribute('href'))
    for i in range(1,len(items)):
        try:
            is_tmall[i].find_element_by_css_selector('li > a > span.icon-service-tianmao')#오류가 안나면 tmall
            is_tmall[i] = True
        except:
            is_tmall[i] = False
        if is_tmall[i]:
            crawl_a_item_tmall(link[i])
        else:
            crawl_a_item_taobao(driver , link[i])
    os.chdir('..')
    return link


def crawl_a_item_taobao(driver, url):
    import urllib.request
    import requests
    import os
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    driver.get(url)
    print("taobao 크롤링 시작")
    try:
        driver.find_element_by_css_selector('#sufei-dialog-close').click()  # 인증창 생략
    except:
        print("warning 인증창 부재 정상적으로 로딩안되었을 수 있음")
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "txturl")))
            driver.find_element_by_css_selector('div > div.skin-box-bd > div > div')
            break
        except:
            print("err_2 로딩이 오래걸리는 듯함 10번 반복시 오류임")
            driver.implicitly_wait(1)
        break
    current_url = driver.current_url.split("=")
    product_id = ""
    for i in range(len(current_url)):
        if current_url[i][-2:] == 'id':
            product_id = current_url[i + 1].split("&")[0]
            break
    if product_id == "":
        print("상품id 불명")
    print(os.getcwd())
    if (not os.path.exists(f"{os.getcwd()}/{product_id}")):
        os.makedirs(f"./{product_id}")
    main_img = driver.find_element_by_css_selector(
        'div.tb-detail-bd.tb-clear > div.tb-summary.tb-clear > div > div.tb-item-info-l > div.tb-gallery > div > a > span > img')
    main_img1 = main_img.get_attribute('src')
    mem = requests.get(main_img1).content
    with open(f"./{product_id}/main_img{main_img1[-4:]}", "wb") as f:
        if (main_img1[-4] != "."):
            print("warning 파일네이밍이 이상할수 있음")
        f.write(mem)
        print(f"메인 화면은 {main_img1[-4:]}형식으로 저장됨")
    sub_img = driver.find_elements_by_css_selector('#J_UlThumb > li > div > a > img')
    for i in range(len(sub_img)):
        sub_img[i] = sub_img[i].get_attribute('src')#원본 이미지를 가져 올 수 있도록 링크 변환
        sub_img[i] = sub_img[i].split('.jpg')[0]
        if (sub_img[i] != None):
            sub_img[i] = f"{sub_img[i]}.jpg"
            urllib.request.urlretrieve(sub_img[i], f"./{product_id}/sub_img{i}{sub_img[i][-4:]}")
    option_list = driver.find_elements_by_css_selector('#J_isku > div > dl')
    try:
        stock = driver.find_element_by_css_selector('#J_SpanStock').text
        stock = int(stock)
    except:
        print(f"warning 재고가 숨겨져있음 {url}")
    option_name, option_layer = get_option_nameNlayer(driver,option_list,product_id)
    max_wait = 10
    price_list = []
    for i in range(max_wait):
        try:
            driver.find_element_by_css_selector('#J_isku > div > dl.J_Prop.J_TMySizeProp.tb-prop.tb-clear.J_Prop_measurement > dd > ul > li > a').click()
            if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute('class') == 'tb-txt tb-selected':
                price_list = get_price_taobao(driver, option_layer)
                break
        except:
            if i == max_wait-1:
                print("타오바오 차단됨 확인요함 가격정보획득실패")
                price_list.append(get_a_price_taobao(driver))
            else:
                print("로딩진행중")
                wait()
    put_data(product_id, option_name, price_list)
    get_detail(product_id)


def get_detail(product_id):
    import requests
    import urllib.request
    from bs4 import BeautifulSoup
    url = f"https://world.taobao.com/item/{product_id}.htm"
    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")
    item_list = html.select('body > div.content > div.detail-container.panel > div.detail-box > p > img')
    for i in range(len(item_list)):
        urllib.request.urlretrieve(item_list[i]['src'], f"./{str(product_id)}/detail_img{i}{item_list[i]['src'][-4:]}")



def init_webdriver(url):
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36")
    options.add_argument("lang=ko-KR")
    try:
        driver = webdriver.Chrome("chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("../chromedriver.exe", options=options)
    driver.get('about:blank')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko','en','en_US']}})")
    driver.get(url)
    return driver


def get_option_nameNlayer(driver,option_list,product_id):
    import urllib.request
    option_name = []
    option_layer = []
    for option in option_list:
        temp_text = option.text.split("\n")
        if temp_text[0] == "数量":  # 수량선택시 제한
            break
        text_list = [temp_text[0]]
        for a_option in option.find_elements_by_css_selector("dd > ul > li > a > span"):
            text_list.append(a_option.text)
        option_name.append(text_list)
        a_line_option_list = option.find_elements_by_css_selector('dd > ul > li')
        option_layer.append(a_line_option_list)  # 전체 옵션을 저장함
        for i in range(len(option_name) - 1):  # 실제 선택지의 갯수를 나타냄
            try:
                option_img0 = a_line_option_list[i].find_element_by_css_selector('a')
                option_img = option_img0.get_attribute('style')
                if option_img == '':
                    print(f"{option_name[-1][0]}:{option_name[-1][i + 1]}이미지 존재X")
                    break
                option_img1 = option_img.split("\"")
                option_img2 = option_img1[1]
                urllib.request.urlretrieve(f"http:{option_img2}",f"./{product_id}/{option_name[-1][0]}_img{i}{option_img2[-4:]}")
            except:
                option_img = None
                print(f"err_3 {option_name[-1][0]}:{option_name[-1][i + 1]}이미지 수집 불가 구조 변경 혹은 링크 탐색 실패")
    return option_name, option_layer


def crawl_a_item_tmall(url):
    import pandas as pd
    from selenium import webdriver
    import urllib.request
    from naver_api import cn2kor
    import requests
    import os
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.108.15 Safari/537.36")
    options.add_argument("lang=ko-KR")
    options.add_argument("lang=en-US")
    driver = webdriver.Chrome("../chromedriver.exe", options=options)
    driver.get(url)
    print("tmall 크롤링 시작")
    # tmall임
    try:
        driver.find_element_by_css_selector('#sufei-dialog-close').click()  # 인증창 생략
    except:
        print("warning 인증창 부재 정상적으로 로딩안되었을 수 있음")
    while (True):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "xx_inner")))
            driver.find_element_by_css_selector('div > div.skin-box-bd > div > div')
            driver.find_element_by_css_selector('body > div.baxia-dialog.auto > div.baxia-dialog-content > div').click()
            break
        except:
            print("a")
            driver.implicitly_wait(1)
        break
    current_url = driver.current_url.split("=")
    product_id = ""
    for i in range(len(current_url)):
        if current_url[i][-2:] == 'id':
            product_id = current_url[i + 1].split("&")[0]
            break
        wait(0.1)
    if (product_id == ""):
        print("상품id 불명")
    print(os.getcwd())
    if (not os.path.exists(f"{os.getcwd()}/{product_id}")):
        os.makedirs(f"./{product_id}")
    main_img = driver.find_element_by_css_selector(
        'div.tm-clear > div.tb-gallery > div.tb-booth')
    main_img1 = main_img.find_element_by_tag_name('img')
    main_img2 = main_img1.get_attribute('src')
    mem = requests.get(main_img2).content
    with open(f"./{product_id}/main_img{main_img2[-4:]}", "wb") as f:
        if (main_img2[-4] != "."):
            print("warning 파일네이밍이 이상할수 있음")
        f.write(mem)
        print(f"메인 화면은 {main_img2[-4:]}형식으로 저장됨")
    sub_img = driver.find_elements_by_css_selector('#J_UlThumb > li > a > img')
    for i in range(len(sub_img)):
        sub_img[i] = sub_img[i].get_attribute('src')
        if (sub_img[i] != None):
            urllib.request.urlretrieve(sub_img[i], f"./{product_id}/sub_img{i}{sub_img[i][-4:]}")
    option_list = driver.find_elements_by_css_selector('div > div > div > div.tb-key > div > div > dl')
    try:
        stock = driver.find_element_by_css_selector(
            '#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-key > div > div > dl.tb-amount.tm-clear > dd > em').text[
                2:-1]
        stock = int(stock)
    except:
        print(f"warning 재고가 숨겨져있음 {url}")
    option_name, option_layer = option_name, option_layer = get_option_nameNlayer(driver,option_list,product_id)
    price_list = get_price(driver, option_layer)
    put_data(product_id,option_name,price_list)
    get_detail(product_id)
    driver.quit()


def put_data(product_id,option_name,price_list):
    import pandas as pd
    data = [product_id, len(option_name)]
    label = ["id", "옵션갯수"]
    for i in range(len(option_name) - 1):
        data.append(option_name[i][1:])
        label.append(option_name[i][0])
    label.append("가격(트리형태)")
    data.append(price_list)
    df = pd.DataFrame(data, label)
    df.to_csv(f"./{product_id}/{product_id}_data.csv")


def get_img(url,path):
    import urllib.request
    if url[0:13] == "background:url":
        url = url[17:]
        parse = url.split('.jpg')[0]
        urllib.request.urlretrieve(f"{parse}.jpg", path)
    elif url[0:3] == "http":
        parse = url.split('.jpg')[0]
        urllib.request.urlretrieve(f"{parse}.jpg", path)
    elif url[0:1] == "//":
        parse = url.split('./jpg')[0]
        urllib.request.urlretrieve(f"{parse}.jpg", path)
    else:
        print(f"{url}은 지원하지 않는 포멧입니다. 경로 {path}")





# get_price 테스트용 url = "https://detail.tmall.com/item.htm?id=568298039720"

def get_price(driver, option_layer):
    price_by_option = []
    if len(option_layer) == 1:  # 마지막줄이라는 의미
        for i in range(len(option_layer[0])):
            if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute(
                    'class') == 'tb-txt tb-selected':
                price_by_option.append(float(driver.find_element_by_css_selector('span.tm-price').text))
                option_layer[0][i].click()
            else:
                option_layer[0][i].click()
                if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute(
                        'class') == 'tb-txt tb-selected':
                    # 선택이 가능한지 체크 재고가 없을경우 불가능함
                    price_by_option.append(
                        float(driver.find_element_by_css_selector('span.tm-price').text))
                    option_layer[0][i].click()
                else:
                    price_by_option.append(-1)
        return price_by_option
    # 마지막 옵션이 아닐때만 작동
    for i in range(len(option_layer[0])):
        if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute(
                'class') == 'tb-txt tb-selected':
            price_by_option.append(get_price(driver, option_layer[1:]))
            option_layer[0][i].click()
        else:
            option_layer[0][i].click()
            if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute(
                    'class') == 'tb-txt tb-selected':
                price_by_option.append(get_price(driver, option_layer[1:]))
                option_layer[0][i].click()
            else:
                price_by_option.append([])
    return price_by_option


def get_price_taobao(driver, option_layer):
    # 로그인 했을시 문제 없는것 확인
    # 미 로그인시 클릭안되는 문제 발생 이것을 해결할 방법은 찾아야함
    # 초기에 로딩이 다 되기 전에 안되는 문제가 있으나 호출한 함수에서 대기하도록 처리함 최대 10초
    price_by_option = []
    if len(option_layer) == 1:  # 마지막줄이라는 의미
        for i in range(len(option_layer[0])):
            if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute(
                    'class') == 'tb-txt tb-selected':
                price_by_option.append(get_a_price_taobao(driver))
                option_layer[0][i].click()
            else:
                option_layer[0][i].click()
                if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute(
                        'class') == 'tb-txt tb-selected':
                    # 선택이 가능한지 체크 재고가 없을경우 불가능함
                    price_by_option.append(get_a_price_taobao(driver))
                    option_layer[0][i].click()
                else:
                    price_by_option.append(-1)
        return price_by_option
    # 마지막 옵션이 아닐때만 작동
    for i in range(len(option_layer[0])):
        if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute('class') == 'tb-txt tb-selected':
            price_by_option.append(get_price_taobao(driver, option_layer[1:]))
            option_layer[0][i].click()
        else:
            option_layer[0][i].click()
            if option_layer[0][i].get_attribute('class') == 'tb-selected' or option_layer[0][i].get_attribute(
                    'class') == 'tb-txt tb-selected':
                price_by_option.append(get_price_taobao(driver, option_layer[1:]))
                option_layer[0][i].click()
            else:
                price_by_option.append([])
    return price_by_option


def get_a_price_taobao(driver):
    try:  # t세일하는 경우
        return driver.find_element_by_css_selector('#J_PromoPriceNum').text
    except:  # 세일 안하는 경우
        return driver.find_element_by_css_selector('#J_StrPrice > em.tb-rmb-num').text


def wait(sec=1):
    import time
    # print(f"{sec}만큼 대기함")
    start = time.time()
    while start + sec > time.time():
        if time.time()>1610068495:
            print("접속차단됨 리캡챠 해결 불가 또는 ip변경 필요")
            exit()
        p = 0
