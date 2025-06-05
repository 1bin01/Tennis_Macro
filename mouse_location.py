# pip install pyautogui
import pyautogui

def get_mouse_position():
    try:
        while True:
            # 현재 마우스 위치 가져오기
            x, y = pyautogui.position()
            print(f"마우스 위치: X = {x}, Y = {y}")
    except KeyboardInterrupt:
        print("좌표 캡처를 종료합니다.")

# 실행
get_mouse_position()
