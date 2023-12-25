pip install selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import math

def str_to_num_cleanup(x):
    n = ""
    for i in range(len(x)):
        if x[i].isnumeric():
            n += x[i]
    return int(n)

driver = webdriver.Chrome()
url = 'https://google.com'
driver.get(url)
driver.find_element_by_css_selector('.gLFyf').send_keys('네이버뉴스')
driver.find_element_by_css_selector('.gLFyf').send_keys(Keys.ENTER)
driver.find_element_by_css_selector('.LC20lb.MBeuO.DKV0Md').click()

var = True
while var:
    category = int(input("1.정치 2.경제, 3.사회, 4.생활/문화, 5.IT/과학, 6.세계 뉴스 중 선택해주세요."))
    if category == 1:
        driver.find_elements_by_css_selector('.Nitem_link_menu')[category - 1].click()
        xpath_var = '//*[@id="main_content"]/div/div[2]/div[1]/div[3]/div[1]/ul/li[1]/div[2]/a'
        break
    elif 2 <= category <= 6:
        driver.find_elements_by_css_selector('.Nitem_link_menu')[category - 1].click()
        xpath_var = '//*[@id="main_content"]/div/div[2]/div[1]/div[3]/div[2]/ul/li[1]/div[2]/a'
        break
    else:
        print("Invalid input. Please retry.")
        continue

print("네이버 Hot Issue 뉴스:")
try:
    for i in range(2):
        xpath_var_alpha = xpath_var.replace('[3]', f'[{i + 1}]')
        print(driver.find_element_by_xpath(xpath_var_alpha).text)
except Exception as e:
    print(f"ERROR: {e}")
    print("현재 네이버 뉴스 헤드라인이 존재하지 않습니다.")
    sys.exit()

while var:
    choice = input("Which news do you want to scrape comments from? ('first' or 'second')")
    if choice == 'first' or choice == 'second':
        driver.find_element_by_xpath(xpath_var.replace('[3]', f'[1]')).click() if choice == 'first' else driver.find_element_by_xpath(xpath_var.replace('[3]', f'[2]')).click()
        break
    else:
        print("Invalid input. Please retry.")
        continue

# 유저가 선택한 기사가 '정치' 인 경우
if category == 1:
    try:  # 정치-잠긴댓글
        # 댓글수가 0인지 확인
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        com_count = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/h5/em').text
        if com_count == '0':
            print("ERROR: There are no comments available!!!")
            sys.exit()

        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div/a[1]/div').click()  # 잠긴댓글보기

    except:  # 정치-열린댓글
        # 댓글수가 0인지 확인
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        com_count = driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[1]/a/span[1]').text
        if com_count == '0':
            print("ERROR: There are no comments available!!!")
            sys.exit()

        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[9]/a/span[1]').click()  # 댓글더보기

    # 댓글이 딱 1개
    if com_count == '1':
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        print('Comment:')
        print(driver.find_element_by_xpath('//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li/div[1]/div/div[2]/span[1]').text)
        print("-------------------------")

    # 댓글 1페이지 이상일때 모든 댓글 노출
    if str_to_num_cleanup(com_count) > 20:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        comment_block = math.ceil(int(com_count) / 20)
        for i in range(comment_block - 1):
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[9]/a').click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 댓글 크롤링
    if com_count != '1':
        print('Comments:')
        for i in range(str_to_num_cleanup(com_count)):
            try:
                time.sleep(0.75)
                print(driver.find_element_by_xpath(f'//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li[{i + 1}]/div[1]/div/div[2]').text)
                print("-------------------------")
            except:
                time.sleep(0.75)
                print("작성자에 의해 삭제된 댓글입니다.")
                print("-------------------------")

# 유저가 선택한 기사가 '경제,사회,생활/문화,IT/과학,세계' 인 경우
if category != 1:
    # 댓글수가 0인지 확인
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    com_count = driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[1]/a/span[1]').text
    if com_count == '0':
        print("ERROR: There are no comments available!!!")
        sys.exit()

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[9]/a/span[1]').click()  # 댓글더보기

    # 댓글이 딱 1개
    if com_count == '1':
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        print('Comment:')
        print(driver.find_element_by_xpath('//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li/div[1]/div/div[2]/span[1]').text)
        print("-------------------------")

    # 댓글 1
