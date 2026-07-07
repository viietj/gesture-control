import cv2
import mediapipe as mp
import pyautogui
import math 
import time
import os


tay = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
ve  = mp.solutions.drawing_utils
MAN_RONG, MAN_CAO = pyautogui.size()
camera = cv2.VideoCapture(0)
pyautogui.PAUSE = 0

dem = {
    "click": 0,
    "chup": 0,
    "nhac": 0,
    "tiep": 0,
    "phat": 0,
    "am": 0,
    "cuon": 0
}
NGUONG = 10
dang_lam      = None
lan_cuoi_lam  = 0

def khoang_cach(a, b): 
    return math.hypot(a.x - b.x, a.y - b.y)

def xac_nhan(ten, hanh_dong, so_frame=NGUONG, cho=0.5):
    global dang_lam, lan_cuoi_lam
    if dang_lam and dang_lam != ten: dem[ten] = 0; return
    if time.time() - lan_cuoi_lam < cho: return
    dang_lam = ten; dem[ten] += 1
    if dem[ten] >= so_frame:
        hanh_dong(); dem[ten] = 0; dang_lam = None; lan_cuoi_lam = time.time()


DANH_SACH = [
    ("[1]   ", "Di chuyen"),  ("[CT]  ", "Click"),      ("[CTG] ", "Chup man hinh"),
    ("[TGU] ", "Cuon trang"), ("[CAI] ", "Am luong"),   ("[5]   ", "Play/Pause"),
    ("[CU]  ", "Next Track"), ("[4]   ", "Mo Music"),
]

def ve_overlay(frame, nhan, tien_trinh, ngon_tay):
    h, w = frame.shape[:2]
    px = w - 275
    nen = frame.copy()
    cv2.rectangle(nen, (px, 0), (w, h), (15, 15, 25), -1)
    cv2.addWeighted(nen, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, "GESTURE CONTROL", (px+8, 26), cv2.FONT_HERSHEY_DUPLEX, 0.52, (255,220,80), 1)
    cv2.line(frame, (px+8, 33), (w-8, 33), (80,80,80), 1)
    for i, (ky_hieu, ten) in enumerate(DANH_SACH):
        y = 52 + i*42; dang_on = nhan == ten
        mau = (0,220,100) if dang_on else (150,150,150)
        cv2.putText(frame, f"{ky_hieu}{ten}", (px+8, y), cv2.FONT_HERSHEY_SIMPLEX, 0.38, mau, 1)
        if dang_on:
            cv2.rectangle(frame, (px+8, y+4), (px+260, y+10), (40,40,40), -1)
            cv2.rectangle(frame, (px+8, y+4), (px+8+int(252*tien_trinh/NGUONG), y+10), (0,200,100), -1)
    for i, (ten_ngon, trang_thai) in enumerate(zip(["C","T","G","A","U"], ngon_tay)):
        cx = px + 20 + i*50
        cv2.circle(frame, (cx, h-30), 13, (0,210,100) if trang_thai else (55,55,55), -1)
        cv2.putText(frame, ten_ngon, (cx-6, h-13), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (230,230,230), 1)
    cv2.putText(frame, f">> {nhan}" if nhan else "-- Cho tay vao --",
                (10, h-10), cv2.FONT_HERSHEY_DUPLEX, 0.52, (0,220,120), 1)


while True:
    ret, frame = camera.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    h, w  = frame.shape[:2]
    ket_qua = tay.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    nhan    = ""; ngon_tay = (False,)*5

    if ket_qua.multi_hand_landmarks:
        diem = ket_qua.multi_hand_landmarks[0].landmark
        cai, tro, giua, ap, ut = (
            diem[4].x  < diem[3].x,
            diem[8].y  < diem[6].y,
            diem[12].y < diem[10].y,
            diem[16].y < diem[14].y,
            diem[20].y < diem[18].y,
        )
        
        tro_ro  = diem[8].y  < diem[5].y  - 0.03
        giua_ro = diem[12].y < diem[9].y  - 0.03
        ap_ro   = diem[16].y < diem[13].y - 0.03
        ut_ro   = diem[20].y < diem[17].y - 0.03
        cai_ro  = diem[4].x  < diem[2].x  - 0.03

        ngon_tay = (cai, tro, giua, ap, ut)
        so_ngon  = sum(ngon_tay)

        if (cai,tro,giua,ap,ut) == (False,True,False,False,False) and tro_ro:
            nhan = "Di chuyen"
            pyautogui.moveTo(diem[8].x * MAN_RONG, diem[8].y * MAN_CAO)

        elif tro_ro and not cai and not ap and not ut:
            d = khoang_cach(diem[8], diem[12])
            if d < 0.04:   
                nhan = "Click"; xac_nhan("click", pyautogui.click, 5, 0.3)

        elif tro_ro and giua_ro and cai_ro and not ap and not ut:
            nhan = "Chup man hinh"
            duong_dan = f"cap_{int(time.time())}.png"
            xac_nhan("chup", lambda p=duong_dan: pyautogui.screenshot(p), 30, 1.0)

        elif tro_ro and giua_ro and ut_ro and not cai and not ap:
            nhan = "Cuon trang"
            cy = diem[8].y * MAN_CAO
            xac_nhan("cuon", lambda: pyautogui.scroll(50 if cy < MAN_CAO*0.4 else -50))

        elif cai_ro and not tro and not giua and not ap and not ut:
            nhan = "Am luong"
            d = khoang_cach(diem[4], diem[8])
            xac_nhan("am", lambda: pyautogui.press('volumedown' if d < 0.15 else 'volumeup'))

        elif so_ngon == 5:
            nhan = "Play/Pause"; xac_nhan("phat", lambda: pyautogui.press('playpause'), cho=0.8)

        elif cai_ro and ut_ro and not tro and not giua and not ap:
            nhan = "Next Track"; xac_nhan("tiep", lambda: pyautogui.press('nexttrack'), cho=0.8)

        elif tro_ro and giua_ro and ap_ro and ut_ro and not cai:
            nhan = "Mo Music"; xac_nhan("nhac", lambda: os.system("start https://music.apple.com"), cho=2.0)

        else:
            for key in dem:
                dem[key] = 0
            dang_lam = None

        tien_trinh = dem.get(next((k for k in dem if dem[k] > 0), "click"), 0)
        ve.draw_landmarks(frame, ket_qua.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)


    else:
        for key in dem:
            dem[key] = 0
        dang_lam = None
        tien_trinh = 0

    ve_overlay(frame, nhan, tien_trinh, ngon_tay)
    cv2.imshow("Gesture Control", frame)
    k = cv2.waitKey(1)
    if k == ord('q'): break

camera.release()
cv2.destroyAllWindows()
