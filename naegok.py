from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import requests

coutList = [
        "월 내곡 1번코트(하드)",
        "월 내곡 2번코트(하드)",
        "월 내곡 3번코트(하드)",
        "월 내곡 4번코트(하드)",
        "월 내곡 5번코트(하드)",
        "월 내곡 6번코트(하드)",
        "월 내곡 7번코트(인조잔디)",
        "월 내곡 8번코트(인조잔디)"
    ]

def getDay():
    while True:
        day = int(input("예약일을 입력해주세요 (예: 21): "))
        if 1 <= day <= 31:
            return day
        else:
            print("\n1부터 31 사이의 정수를 입력해주세요.\n")
            
            
def getHours():
    while True:
        time_range = input("예약 시간을 입력해주세요 (예: 12-14) : ")
        try:
            start, end = map(int, time_range.split('-'))
            if 6 <= start < end <= 22:
                return list(range(start, end))
            else:
                print("\n6-22 사이의 유효한 시간 범위를 입력해주세요.\n")
        except:
            print("\n형식을 지켜주세요. (예: 12-14)\n")


def chooseCourt():
    while True:
        try:
            choice = int(input("코트를 선택해 주세요 (하드는 1, 인조잔디는 2, 상관없으면 3 을 입력) : "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("\n1(하드) 또는 2(인조잔디) 또는 3(하드 + 인조잔디)를 입력해주세요.\n")
        except ValueError:
            print("\n숫자를 입력해 주세요.\n")
            
def getCandidate():
    date = getDay()
    print()
    timeslot = getHours()
    print()
    court = chooseCourt()
    print()
    return (date, timeslot, court)

def printOption(option):
    date, timeslot, court = option        
    courtType = "하드 + 인조잔디"
    if court == 1:
        courtType = "하드"
    elif court == 2:
        courtType = "인조잔디"
    print(f'{month}월 {date}일 {timeslot[0]}-{timeslot[-1] + 1}시에 {courtType}를 예약하겠습니다\n')
    

def getCourtOptions():
    courtOptions = []
    print('------------------------------------')
    idx = 0
    while(1):
        idx += 1
        print(f'\n {idx}번째 코트 예약을 도와드리겠습니다.\n')

        option = getCandidate()
        courtOptions.append(option)
        printOption(option)
        
        inp = 0
        while True:
            inp = int(input("추가로 입력하려면 1, 아니면 0을 입력해주세요 : "))
            if inp == 0 or inp == 1: break        
        if inp == 0: break
        
        print('-------------------------------------')
        
        
    # 예약 후보 목록
    print('\n------------ 예약 후보 목록 -------------\n')
    for date, timeslot, court in courtOptions:
        courtType = "하드 + 인조잔디"
        if court == 1:
            courtType = "하드"
        elif court == 2:
            courtType = "인조잔디"
            
        print(f'{month}월 {date}일 {timeslot[0]}시-{timeslot[-1] + 1}시 {courtType}')
        
    print('\n-------------------------------------\n')
    return courtOptions


def make_reservation(day, timeslot, court):
    # 1. 날짜 선택
    xpath = f'//button[@class="calendar_date" and .//span[text()="{day}"]]'
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()

    # 2. 원하는 시간대 선택
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.time_item"))
    )
    time_items = driver.find_elements(By.CSS_SELECTOR, "li.time_item")
    
    Time = 6
    for item in time_items:
        if Time in timeslot:
            if "disabled" not in item.get_attribute("class"):
                item.find_element(By.TAG_NAME, "button").click()
            else :
                print(f'{Time}시 자리가 없습니다 ㅠㅠ')
                return 0
        Time += 1
    
    WebDriverWait(driver, 10).until( # 적용 버튼
        EC.element_to_be_clickable((
            By.XPATH, '//button[contains(text(), "적용")]'
        ))
    ).click()
    
    # 3. 코트 선택    
    find = 0
    l = 0
    r = 8
    if court == 1:
        r = 6
    elif court == 2:
        l = 6
    
    for t in range(30):
        print(t)
        try : 
            for i in range(r - 1, l - 1, -1):
                xpath = f'//div[@class="desc_title" and normalize-space(text())="{coutList[i]}"]/ancestor::a[@class="item_desc"]'
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    ).click()
                    find = 1
                    break
                
                if find == 1:
                    break
        except Exception as e:
            print(f"클릭 인터셉트 오류 발생: {e} - 재시도 중...")

    if find == 0:
        print("만족하는 코트가 없습니다 ㅠㅠ")
        return 0
    
    WebDriverWait(driver, 20).until(  # 다음 버튼
        lambda d: (btn := d.find_element(By.XPATH, '//button[text()="다음"]')) 
                and "disabled" not in btn.get_attribute("class") 
                and btn.is_enabled() 
                and btn.is_displayed() and btn
    ).click()

    
    # 4. 동의 및 결제
    WebDriverWait(driver, 20).until(  # 동의하고 결제하기 버튼
        lambda d: (btn := d.find_element(By.XPATH, '//button[text()="동의하고 결제하기"]')) 
                and "disabled" not in btn.get_attribute("class") 
                and btn.is_enabled() 
                and btn.is_displayed() and btn
    ).click()
    return 1


def run():
    # 예약 가능한 코트 찾기
    for date, timeslot, court in courtOptions:
        driver.get("https://booking.naver.com/booking/10/bizes/217811")
        
        # 6. 캘린더로 이동
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "booking_select"))
        ).click()

        # 7. 달 맞추기
        while True:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "calendar_title"), ".")
            )
            current_month = int(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "calendar_title"))
            ).text.strip().split(".")[1])
            
            if(current_month == month) : break
            
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn_next"))
            ).click()
            print(f"현재 달은 {current_month}월입니다. 다음 달로 넘어갑니다.")
            
        print(f"현재 달력에서 달은 {current_month}입니다")
        
        # 8. 예약 시도
        return make_reservation(date, timeslot, court)

def getServerTime(url):
    return datetime.datetime.strptime( requests.head(url).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')

def waitFunction(url):
    while(True):
        serverTime = getServerTime(url)
        print(serverTime)
        if serverTime.second == 0:
            break

'''
Todo
1. python 설치 (3.13 기준)
2. 컴퓨터에 selenium 설치 (터미널에서 명령어 입력 : pip install selenium)
   컴퓨터에 requests 설치 (터미널에서 명령어 입력 : pip install requests)
3. 네이버 로그인
4. 화면에 따라 작동이 잘 안될 수도 있으니 꼭 테스트해보기
'''

tmp = input('\n아무거나 입력해주세요 : ')

print('--------------macro loaded--------------------')

# 1. 예약 달 입력받기
month = int(input("\n몇월에 예약하시겠습니까? "))
print(f"\n{month}월 예약 도와드리겠습니다\n") 


# 2. 예약 날짜 입력받기
coutList = [court.replace("월", f"{month}월") for court in coutList]
courtOptions = getCourtOptions() # (날짜, 시간, 코트)


# 3. 크롬 드라이버 설정
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)


# 4. 로그인
driver.get("https://nid.naver.com/nidlogin.login")

# 네이버 예약 페이지 열기
WebDriverWait(driver, 50).until(EC.url_changes("https://nid.naver.com/nidlogin.login"))
driver.get("https://booking.naver.com/booking/10/bizes/217811")

# 5. 9시 정각까지 대기


#  6. 00초마다 코트 예약 시도
while(True):
    waitFunction('https://booking.naver.com/booking/10/bizes/217811')
    if run() :
        break


for i in range(60, 0, -1):
    print(f'{i} 초 후 종료')
    time.sleep(1)
print("프로그램 종료")