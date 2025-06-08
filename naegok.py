from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import datetime
import requests

### 코트 URL 관리 ###
bookingUrl = "https://booking.naver.com/booking/10/bizes/217811/items/"

# Need to modify!!
# 월에 맞게 코트 URL 번호 갱신해줘야함
courtUrlNumbers = {
    6 : {
        1: "4348531",  # 1번 코트
        2: "4348532",  # 2번 코트
        3: "4348535",  # 3번 코트
        4: "4348536",  # 4번 코트
        5: "4348537",  # 5번 코트
        6: "4348539",  # 6번 코트
        7: "4348540",  # 7번 코트        
        8: "6503551",  # 8번 코트
    },
    7 : {
        1: "6804184",  # 1번 코트
        2: "6804189",  # 2번 코트
        3: "6804192",  # 3번 코트
        4: "6804195",  # 4번 코트
        5: "6804221",  # 5번 코트
        6: "6804227",  # 6번 코트
        7: "6804230",  # 7번 코트
        8: "6804234",  # 8번 코트
    }
}

def getCourtURL(month, courtNumber):
    try:
        return bookingUrl + courtUrlNumbers[month][courtNumber]
    except KeyError:
        return "해당 코트의 URL이 존재하지 않습니다."
###


### 입력 받는 함수들 ###
def getCourtNumber():
    while True:
        try:
            choice = int(input("\n코트를 선택해주세요 (1 ~ 8) :  "))
            if 1 <= choice <= 8:
                return choice
            else:
                print("\n1 이상 8 이하의 수를 입력해주세요.\n")
        except ValueError:
            print("\n숫자를 입력해 주세요.\n")

def getMonth():
    while True:
        try:
            month = int(input("예약할 달을 입력해주세요 (예: 6) : "))
            if 1 <= month <= 12:
                return month
            else:
                print("\n1 이상 12 이하의 수를 입력해주세요.\n")
        except ValueError:
            print("\n숫자를 입력해 주세요.\n")

def getDay():
    while True:
        try:
            day = int(input("예약일을 입력해주세요 (예: 21): "))
            if 1 <= day <= 31:
                return day
            else:
                print("\n1부터 31 사이의 정수를 입력해주세요.\n")
        except ValueError:
            print("\n숫자를 입력해 주세요.\n")
            
            
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

            
def getOption():
    date = getDay()
    print()
    timeslot = getHours()
    print()
    return (date, timeslot)

def printOption(option):
    date, timeslot = option        
    print(f'{month}월 {date}일 {timeslot[0]}-{timeslot[-1] + 1}시에 예약하겠습니다\n')
    

def getBookingOptions():
    bookingOptions = []
    print('------------------------------------')
    idx = 0
    while(1):
        idx += 1
        print(f'\n {idx}번째 코트 예약을 도와드리겠습니다.\n')

        option = getOption()
        bookingOptions.append(option)
        printOption(option)
        
        inp = 0
        while True:
            try:
                inp = int(input("추가로 입력하려면 1, 아니면 0을 입력해주세요 : "))
                if inp == 0 or inp == 1:
                    break
                else:
                    print("\n0 또는 1을 입력해주세요.\n")
            except ValueError:
                print("\n숫자를 입력해 주세요.\n")
        
        if inp == 0:
            break
        print('-------------------------------------')
        
        
    # 예약 후보 목록
    print('\n------------ 예약 후보 목록 -------------\n')
    for date, timeslot in bookingOptions:
        print(f'{month}월 {date}일 {timeslot[0]}시-{timeslot[-1] + 1}시')
        
    print('\n-------------------------------------\n')
    return bookingOptions

def selectDay(day):
    try:
        xpath = f'//button[@class="calendar_date" and .//span[text()="{day}"]]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()
        return 1
    except TimeoutException as e:
        print("날짜 선택에 실패했습니다.", e)
        return 0

def Select(timeslot):
    try:
        WebDriverWait(driver, 10).until(
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
    except Exception as e:
        return 0
    
    return 1
    
def selectTimeSlot(timeslot):
    if Select(timeslot) == 1:
        return 1
    else:
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "slick-next"))
            ).click()
            return Select(timeslot)      
        except Exception as e2:
            print("넘어가기 버튼 실패 ㅠ")  
            return 0
    
        
def tryBooking(day, timeslot):
    # 1. 날짜 선택
    if selectDay(day) == False:
        return 0

    # 2. 원하는 시간대 선택
    if selectTimeSlot(timeslot) == False:
        return 0
    
    # # 3. 적용 버튼
    # try:
    #     WebDriverWait(driver, 50).until( 
    #         EC.element_to_be_clickable((
    #             By.XPATH, '//button[contains(text(), "적용")]'
    #         ))
    #     ).click()
    # except Exception as e:
    #     print("적용 버튼 클릭 실패:", e)
    #     return 0    
    
    # 4. 다음 버튼
    try:
        WebDriverWait(driver, 10)( 
            lambda d: (btn := d.find_element(By.XPATH, '//button[text()="다음"]')) 
                    and "disabled" not in btn.get_attribute("class") 
                    and btn.is_enabled() 
                    and btn.is_displayed() and btn
        ).click()
    except Exception as e:
        print("다음 버튼 클릭 실패:", e)
        return 0
    

    # 5. 동의 및 결제
    try:
        WebDriverWait(driver, 10).until( 
            lambda d: (btn := d.find_element(By.XPATH, '//button[text()="동의하고 결제하기"]')) 
                    and "disabled" not in btn.get_attribute("class") 
                    and btn.is_enabled() 
                    and btn.is_displayed() and btn
        ).click()
    except Exception as e:
        print("동의 및 결제 버튼 클릭 실패:", e)
        return 0    
    
    return 1


def run(courtUrl):
    for date, timeslot in bookingOptions:
        driver.get(courtUrl)
        if tryBooking(date, timeslot):
            return 1
    return 0

def getServerTime(url):
    return datetime.datetime.strptime( requests.head(url).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')

def waitFunction(url):
    while(True):
        serverTime = getServerTime(url)
        print(serverTime)
        if serverTime.second % 60 < 10:
            break

'''
Todo
1. python 설치 (3.13 기준)
2. 컴퓨터에 selenium 설치 (터미널에서 명령어 입력 : pip install selenium)
   컴퓨터에 requests 설치 (터미널에서 명령어 입력 : pip install requests)
4. 네이버 로그인
5. 화면에 따라 작동이 잘 안될 수도 있으니 꼭 테스트해보기

+) 2시간 예약인데 1시간 밖에 자리가 없는데 검색이 됨.. 문제..
'''

tmp = input('\n아무거나 입력해주세요 : ')

print('\n--------------macro loaded--------------------\n')

# 1. 예약 달과 코트 번호 입력받기
month = getMonth()
courtNumber = getCourtNumber()
print(f"\n{month}월 {courtNumber}번 코트 예약 도와드리겠습니다\n")
courtUrl = getCourtURL(month, courtNumber)

# 2. 예약 날짜와 시간 입력받기
bookingOptions = getBookingOptions() # (날짜, 시간)

# 3. 크롬 드라이버 설정
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# 4. 로그인
driver.get("https://nid.naver.com/nidlogin.login")

# # 네이버 예약 페이지 열기
WebDriverWait(driver, 50).until(EC.url_changes("https://nid.naver.com/nidlogin.login"))
driver.get(courtUrl)


#  5. 00초마다 코트 예약 시도
while(True):
    waitFunction(courtUrl)
    if run(courtUrl):
        break
    time.sleep(10)


for i in range(60, 0, -1):
    print(f'{i} 초 후 종료')
    time.sleep(1)
print("프로그램 종료")
