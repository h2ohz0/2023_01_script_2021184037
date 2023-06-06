from tkinter import *
import threading
import sys
from tkinter import messagebox
# pip install folium
import folium
# pip install cefpython3==66.1
from cefpython3 import cefpython as cef

# 지도 버튼 만들기

# cef모듈로 브라우저 실행
def showMap(frame):
    global browser
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0,0,800,600])
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
    cef.MessageLoop()


def setup():
    # 지도 저장
    # 위도 경도 지정
    m = folium.Map(location=[37.3402849, 126.7313189], zoom_start=13)
    # 마커 지정
    folium.Marker([37.3402849, 126.7313189], popup='한국산업기술대').add_to(m)
    # html 파일로 저장
    m.save('map.html')

    # 브라우저를 위한 쓰레드 생성
    thread = threading.Thread(target=showMap, args=(frame2,))
    thread.daemon = True
    thread.start()

def pressed_1():
    m = folium.Map(location=[37.3402849, 126.7313189], zoom_start=13)
    folium.Marker([37.3402849, 126.7313189], popup='한국산업기술대').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_2():
    m = folium.Map(location=[37.4145018,126.6959112], zoom_start=13)
    folium.Marker([37.4145018,126.6959112], popup='서울대').add_to(m)
    m.save('map.html')
    browser.Reload()

def pressed_3():
    m = folium.Map(location=[37.5657882,126.936378], zoom_start=13)
    folium.Marker([37.5657882,126.936378], popup='연세대').add_to(m)
    m.save('map.html')
    browser.Reload()

window = Tk()
frame1 = Frame(window)
frame1.pack(side=LEFT)
Button(frame1, text='한국산업기술대', command=pressed_1).pack()
Button(frame1, text='서울대', command=pressed_2).pack()
Button(frame1, text='연세대', command=pressed_3).pack()
frame2 = Frame(window, width=800, height=600)
frame2.pack(side=LEFT)
setup()

window.mainloop()