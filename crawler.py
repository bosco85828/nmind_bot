from datetime import datetime,timezone,timedelta
from pprint import pprint
import requests
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pytz

from dotenv import load_dotenv
import os 
# options = Options()
# options.add_argument("--disable-notifications")    
# # options.add_argument("--headless")
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# # options.add_argument('blink-settings=imagesEnabled=false')
# options.add_argument('--disable-dev-shm-usage')

# s=Service(ChromeDriverManager().install())
# global browser
# browser = webdriver.Chrome(service=s, options=options)

def get_snk_data(id):
    browser.get("https://snkrdunk.com/accounts/login/")
    global wait
    wait=WebDriverWait(browser,10)

    locator=(By.XPATH,'//div[@id="bcIframeWrap"]/iframe[@id="buyee-bcFrame"]')
    frame=wait.until(EC.presence_of_element_located(locator))

    browser.switch_to.frame(frame)

    

    locator=(By.XPATH,'//div[@class="bc__closeBtn"]//i')
    close=wait.until(EC.element_to_be_clickable(locator))
    close.click()

    browser.switch_to.default_content()

    locator=(By.XPATH,'//input[@name="email"]')
    acount=wait.until(EC.presence_of_element_located(locator))
    locator=(By.XPATH,'//input[@name="password"]')
    password=wait.until(EC.presence_of_element_located(locator))

    acount.send_keys('bosco85828@gmail.com')
    password.send_keys('bosco85828')
    
    locator=(By.XPATH,'//button[@class="button-type-1 button-collor-black opacity-link"]')
    submit=wait.until(EC.element_to_be_clickable(locator))
    
    # action = ActionChains(browser)
    # action.move_to_element(submit)
    # action.perform()

    try:
        submit.click()
    except :
        # 調整點擊位置
        action = ActionChains(browser)
        action.move_to_element_with_offset(submit, 5, 5)
        action.click()
        action.perform()

    # submit.click()
    browser.get(f"https://snkrdunk.com/buy/{id}/size/")
    locator=(By.XPATH,'//ul[@class="buy-size-select-box"]//p[@class="num"]')
    sizes=wait.until(EC.presence_of_all_elements_located(locator))
    locator=(By.XPATH,'//ul[@class="buy-size-select-box"]//p[@class="size-price"]')
    prices=wait.until(EC.presence_of_all_elements_located(locator))
    
    price_dict={}
    for size in sizes:
        price_dict[size.text] = None

    for i in range(len(price_dict)):
        index=list(price_dict.keys())[i]
        price_dict[index]=prices[i].text
    
    browser.quit()
    
    return price_dict    

def search_size(price_dict,size):
    size=str(size)+"cm"
    return price_dict[size]

def get_kream_data(id):
    browser.get("https://kream.co.kr/login")
    global wait
    browser.maximize_window()
    wait=WebDriverWait(browser,10)
    locator=(By.XPATH,'//input[@type="email"]')
    acount=wait.until(EC.presence_of_element_located(locator))
    locator=(By.XPATH,'//input[@type="password"]')
    password=wait.until(EC.presence_of_element_located(locator))

    acount.send_keys('liyuqian93117@naver.com')
    password.send_keys('931117@lyq')
    
    locator=(By.XPATH,'//a[@class="btn full solid"]')
    submit=wait.until(EC.element_to_be_clickable(locator))
    submit.click()

    # locator=(By.XPATH,'//a[@class="btn_search"]')
    # search=wait.until(EC.element_to_be_clickable(locator))
    # search.click()

    browser.get("https://kream.co.kr/search?keyword={}".format(id))


    # locator=(By.XPATH,'//div[@class="search_area"]//input')
    # search_input=wait.until(EC.element_to_be_clickable(locator))
    # print(search_input.get_attribute('title'))
    # search_input.send_keys(id)
    # search_input.send_keys(Keys.RETURN)
    # time.sleep(10)
    # locator=(By.XPATH,'//div[@class="suggest_item"]/a')
    # product=wait.until(EC.element_to_be_clickable(locator))
    # product.click()

    locator=(By.XPATH,'//div[@class="product"]')
    product=wait.until(EC.element_to_be_clickable(locator))
    product.click()

    locator=(By.XPATH,'//a[@class="btn_size"]')
    size_btn=wait.until(EC.element_to_be_clickable(locator))
    size_btn.click()

    locator=(By.XPATH,'//ul[@class="select_list"]/li//span[@class="size"]')
    sizes=wait.until(EC.presence_of_all_elements_located(locator))
    locator=(By.XPATH,'//ul[@class="select_list"]/li//span[@class="price"]')
    prices=wait.until(EC.presence_of_all_elements_located(locator))

    result={}
    
    for size in sizes:
        result[size.text]=None
    for i in range(len(prices)):
        index=list(result.keys())[i]
        result[index]=prices[i].text
    
    return result


def new_snk_data(id):
    # url="https://snkrdunk.com/v1/sneakers/{}/size/list".format(id)
    # headers={
    #     # "user-agent":"user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",        
    #     # 'authority': 'snkrdunk.com',
    #     # 'accept': 'application/json, text/plain, */*' ,
    #     # 'referer': 'https://snkrdunk.com/buy/{}/size/'.format(id),
    #     # 'cookie': '_gcl_au=1.1.2071998565.1683214414; _fbp=fb.1.1683214414679.1644135972; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22vgdlKaxwlURBdNvktH36%22%7D; __lt__cid=4263cfa9-6490-403a-bd26-618ff7569f2a; krt.vis=FHE34MqyUuurhoY; _pin_unauth=dWlkPU5EZzFPV1JqTXpNdFptSmhZUzAwWkRsbExXRXlNemN0WmprNVlUaGhaREE1TWpaaA; _im_id.1013119=232dc2cb3f1abf3b.1683214416.; ch-veil-id=7df24dd1-a232-4ff6-a2b9-c8f2a9592a8a; fp_token_7c6a6574-f011-4c9a-abdd-9894a102ccef=TrdjeupEgJwWkzt6OYouHDBxEB5OxpJbCKfvrnlvB1Y=; _gid=GA1.2.1265654167.1685856846; __lt__sid=d4e98da9-bdfb3494; ftr_blst_1h=1685856845934; _im_ses.1013119=1; session=MTY4NTg1NzIzNnxOd3dBTkU1S1ZGQXlTMVJOUmtKSk5WUTJSakpZV2xNMldVWmFWRmhFTlVkSk0wZEZSbGhYVURVMlIwcFlXRUZQVTBGUlNqVlZVMUU9fAO3zlaZGg7iqFBvDUPXXoFmBuiEPAlmMtZWWaxM0lBe; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%225365384%22%7D; __gads=ID=cb986a695015e63b-227032ea8fe0003a:T=1683215166:RT=1685858546:S=ALNI_Mb9vcmkcp-TkBaCwNzByyqu8i7lig; __gpi=UID=00000c019d9b3732:T=1683215166:RT=1685858546:S=ALNI_MaOaiD8eRklpMMwY-XfsS5fWLITZQ; _gat_UA-93676001-1=1; _gat_bcTracker=1; showAllItemHistory=1%3ADZ5485-031%2C1%3ADD1391-100%2C1%3ADR5415-103%2C1%3AFB7818-100%2C1%3AFD0724-657%2C1%3ACU9225-100%2C1%3ADN1555-200%2C1%3ADO6290-100%2C2%3A16328413%2C1%3ADV0788-001%2C1%3ADZ1382-001%2C1%3ACW1590-100; showSneakerItemHistory=1%3ADZ5485-031%2C1%3ADD1391-100%2C1%3ADR5415-103%2C1%3AFB7818-100%2C1%3AFD0724-657%2C1%3ACU9225-100%2C1%3ADN1555-200%2C1%3ADO6290-100%2C2%3A16328413%2C1%3ADV0788-001%2C1%3ADZ1382-001%2C1%3ACW1590-100; ch-session-62616=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiI2MjYxNi02NDUzZGRiYjY0MmFlODgwNTBiNyIsImlhdCI6MTY4NTg1ODcyMiwiZXhwIjoxNjg4NDUwNzIyfQ.vcXxYzcWHI40cd0ivjSmD3pSvLx-Wv9cVm2-4UKXv-w; forterToken=52c3ebf56b7f4a38a37b0b537e0786ef_1685858721885__UDF43-m4_15ck; _ga=GA1.2.1355932840.1683214414; cto_bundle=xrhsDF9WNlhMTDZxQXdVNkY1cVZva3BQRG93WHE1anlmdk5GYVhsWVZQSEVtJTJCTERjbVpESFdWQjNPRkpzV0JoeG54OWlqVlkyaFlqdnpUaSUyQnl0WldrS1RiaFFrWkVWQlEwOXNQTiUyQmhramR5dENOeWxTWnlyd094TyUyRjNuNGtrZFUlMkZuUVRYWSUyQnFYTk55NXNHZFlUanUzYnF2dlElM0QlM0Q; _dd_s=logs=0&expire=1685859633882; _ga_WLFPCJHLHL=GS1.1.1685856845.10.1.1685858735.20.0.0'
    #     'user-agent': 'curl/7.84.0',
    #     'accept': '*/*'
    # }
    url=f"https://snkrdunk.com/v1/sneakers/{id}/size/list"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    }

    data=requests.get(url,headers=headers).json()
    prices=data['data']['minPriceOfSizeList']
    price_list=[ x['price'] for x in prices if x]
    # print(price_list)
    minsize,maxsize = (23,32)
    sizes=(data['data']['sneaker']['minProductSize'],data['data']['sneaker']['maxProductSize'])
    (temp_minsize,temp_maxsize)=sizes
    if temp_minsize != 0 : 
        minsize = temp_minsize
    
    if temp_maxsize != 0 :
        maxsize = temp_maxsize

    size_dict={}
    size=float(minsize)
    count=0
    while size <= maxsize :
        if price_list[count] == 0 : 
            size_dict[size]="已售完"
            
        else :     
            size_dict[size]=int((int(price_list[count]) * 1.07) + 990)

        size+=0.5
        count+=1



    # return (size_dict[int(specified_size)] *1.07) + 990 
    return size_dict

def test1():
    url="https://snkrdunk.com/v1/sneakers/CW1590-100/size/list"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    }

    print(requests.get(url,headers=headers).json())
    
if __name__ == "__main__":
    pprint(new_snk_data('DZ1382-001','24'))
# print(search_size(get_snk_data('DD1391-103'),23.5))
# print(get_kream_data('DD1391103'))
# pprint(test1())

