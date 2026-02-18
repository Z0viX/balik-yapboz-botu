import cv2
import numpy as np
import pyautogui
import keyboard
import time
import os
import sys
import ctypes

# --- YENİ GRID AYARI ---
# Main.pyw'deki ayarın aynısı olmak ZORUNDA.
CELL_SIZE = 32 
HALF_CELL = CELL_SIZE / 2

asset_path = os.path.join(os.path.dirname(__file__), 'assets')
if not os.path.exists(asset_path): os.makedirs(asset_path)

print("===================================================")
print(f"   OTOMATİK KAYIT (Grid: {CELL_SIZE})")
print("===================================================")
print("1. Oyunu aç, F1 ile SOL ÜST KÖŞEYİ seç.")
print("2. Parçayı al (Mouse ucunda olsun).")
print("3. Hangi parça ise o tuşa bas (1-6).")
print("⚠️ MOUSE KENDİ HAREKET EDECEK (MÜDAHALE ETME)!")
print("---------------------------------------------------")
print("   [1] DİKEY ÇUBUK          -> fish_1.png")
print("   [2] TEKLİ                -> fish_2.png")
print("   [3] L ŞEKLİ              -> fish_3.png")
print("   [4] TERS L               -> fish_4.png")
print("   [5] KARE (2x2)           -> fish_5.png")
print("   [6] Z ŞEKLİ              -> fish_6.png")
print("---------------------------------------------------")

ref_x, ref_y = 0, 0
calibrated = False

def auto_capture(filename, shape_name):
    print(f"📸 {shape_name} pozisyonlanıyor...")
    
    # Yeni Merkeze Git (37.4 / 2 = 18.7 piksel)
    target_x = int(ref_x + HALF_CELL)
    target_y = int(ref_y + HALF_CELL)
    
    ctypes.windll.user32.SetCursorPos(target_x, target_y)
    
    time.sleep(0.6)
    
    try:
        screenshot = pyautogui.screenshot(region=(int(ref_x), int(ref_y), 32, 32))
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        cv2.imwrite(os.path.join(asset_path, filename), frame)
        print(f"✅ KAYDEDİLDİ: {filename}")
        
        # Önizleme
        display = cv2.resize(frame, (128, 128), interpolation=cv2.INTER_NEAREST)
        cv2.rectangle(display, (0,0), (127,127), (0,255,0), 2)
        cv2.imshow("KAYDEDILEN", display)
        cv2.waitKey(1)
        
    except Exception as e:
        print(f"Hata: {e}")

while True:
    if keyboard.is_pressed('f1'):
        ref_x, ref_y = pyautogui.position()
        calibrated = True
        print(f"✅ Kilitlendi: {ref_x}, {ref_y}")
        time.sleep(0.5)

    if calibrated:
        if keyboard.is_pressed('1'): auto_capture("fish_1.png", "DIKEY CUBUK"); time.sleep(0.5)
        elif keyboard.is_pressed('2'): auto_capture("fish_2.png", "TEKLI"); time.sleep(0.5)
        elif keyboard.is_pressed('3'): auto_capture("fish_3.png", "L SEKLI"); time.sleep(0.5)
        elif keyboard.is_pressed('4'): auto_capture("fish_4.png", "TERS L"); time.sleep(0.5)
        elif keyboard.is_pressed('5'): auto_capture("fish_5.png", "KARE"); time.sleep(0.5)
        elif keyboard.is_pressed('6'): auto_capture("fish_6.png", "Z SEKLI"); time.sleep(0.5)

    if cv2.waitKey(1) == 27: break

cv2.destroyAllWindows()