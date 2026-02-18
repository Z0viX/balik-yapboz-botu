import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import cv2
import numpy as np
import pydirectinput
import time
import os
import sys
import ctypes
import pyautogui

# --- OYUN AYARLARI ---
pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False
CELL_SIZE = 32

# --- WINDOWS API ---
PUL = ctypes.POINTER(ctypes.c_ulong)
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def SendInput(*inputs):
    return ctypes.windll.user32.SendInput(len(inputs), (Input * len(inputs))(*inputs), ctypes.sizeof(Input))

MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP = 0x0002, 0x0004
MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP = 0x0008, 0x0010

# --- MODÜLLERİ YÜKLE ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    import bot_config
    CONFIG_LOADED = True
except ImportError:
    CONFIG_LOADED = False

try:
    from core.jigsaw import Jigsaw, SKIP_ACTION
    from core.deterministic import get_solver
except ImportError:
    pass

def is_key_down(hex_code):
    return ctypes.windll.user32.GetAsyncKeyState(hex_code) & 0x8000 != 0

# --- MODERN ARAYÜZ SINIFI ---
class ModernBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Metin2 Jigsaw Pro")
        self.root.geometry("320x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.96)

        # Değişkenler
        self.solver = None
        self.running = False
        self.calibrated = False
        self.ref_x, self.ref_y = 0, 0
        self.stats_count = 0
        self.asset_path = os.path.join(os.path.dirname(__file__), 'assets')

        # --- ARAYÜZ TASARIMI ---
        self.setup_styles()
        self.create_header()
        self.create_status_panel()
        self.create_controls()
        self.create_log_area()
        self.create_footer()

        # Başlatma
        self.log("Sistem başlatılıyor...", "system")
        if CONFIG_LOADED:
            threading.Thread(target=self.load_solver, daemon=True).start()
        else:
            self.log("HATA: bot_config.py bulunamadı!", "error")

        # Dinleyiciler
        threading.Thread(target=self.hardware_listener, daemon=True).start()
        threading.Thread(target=self.bot_loop, daemon=True).start()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Renk Paleti
        self.colors = {
            "bg": "#1e1e1e",
            "panel": "#252526",
            "accent": "#007acc",
            "success": "#4ec9b0",
            "warning": "#ce9178",
            "danger": "#f44747",
            "text": "#d4d4d4"
        }

        # Buton Stilleri
        style.configure('TButton', font=('Segoe UI', 9, 'bold'), borderwidth=0, focuscolor=self.colors["bg"])
        
        style.configure('Start.TButton', background=self.colors["success"], foreground="#1e1e1e")
        style.map('Start.TButton', background=[('active', '#3ac9a0')])
        
        style.configure('Stop.TButton', background=self.colors["danger"], foreground="white")
        style.map('Stop.TButton', background=[('active', '#d13838')])
        
        style.configure('Calib.TButton', background=self.colors["accent"], foreground="white")
        style.map('Calib.TButton', background=[('active', '#0062a3')])

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.colors["panel"], height=40)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="JIGSAW BOT", font=("Segoe UI", 12, "bold"), 
                 bg=self.colors["panel"], fg=self.colors["success"]).pack(side="left", padx=10, pady=5)
        
        self.lbl_version = tk.Label(header_frame, text="v3.1 Final", font=("Segoe UI", 8), 
                 bg=self.colors["panel"], fg="#666")
        self.lbl_version.pack(side="right", padx=10)

    def create_status_panel(self):
        panel = tk.Frame(self.root, bg=self.colors["bg"], pady=10)
        panel.pack(fill="x", padx=10)

        # Durum Göstergesi (Daire)
        self.canvas_status = tk.Canvas(panel, width=15, height=15, bg=self.colors["bg"], highlightthickness=0)
        self.canvas_status.pack(side="left", padx=(5, 5))
        self.status_circle = self.canvas_status.create_oval(2, 2, 13, 13, fill="#555", outline="")

        # Durum Metni
        self.status_var = tk.StringVar(value="BEKLİYOR")
        tk.Label(panel, textvariable=self.status_var, font=("Segoe UI", 10, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(side="left")

        # Sayaç
        self.stats_var = tk.StringVar(value="0")
        stats_frame = tk.Frame(panel, bg=self.colors["panel"], padx=10, pady=2)
        stats_frame.pack(side="right")
        tk.Label(stats_frame, text="HAMLE:", font=("Segoe UI", 8), bg=self.colors["panel"], fg="#888").pack(side="left")
        tk.Label(stats_frame, textvariable=self.stats_var, font=("Consolas", 10, "bold"), 
                 bg=self.colors["panel"], fg=self.colors["accent"]).pack(side="left", padx=5)

    def create_controls(self):
        control_frame = tk.Frame(self.root, bg=self.colors["bg"])
        control_frame.pack(fill="x", padx=20, pady=5)

        ttk.Button(control_frame, text="KONUM AL (F1)", style='Calib.TButton', 
                   command=self.calibrate, width=30).pack(pady=5)
        
        btn_group = tk.Frame(control_frame, bg=self.colors["bg"])
        btn_group.pack(fill="x", pady=5)
        
        ttk.Button(btn_group, text="BAŞLAT (F5)", style='Start.TButton', 
                   command=self.start_bot, width=13).pack(side="left", padx=(0, 5))
        
        ttk.Button(btn_group, text="DURDUR (F6)", style='Stop.TButton', 
                   command=self.stop_bot, width=13).pack(side="right", padx=(5, 0))

    def create_log_area(self):
        log_frame = tk.LabelFrame(self.root, text="Sistem Kayıtları", bg=self.colors["bg"], 
                                  fg="#666", font=("Segoe UI", 8))
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, height=8, state='disabled', 
                                                  font=("Consolas", 9), bg="#111", fg=self.colors["text"],
                                                  borderwidth=0, highlightthickness=0)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tag renkleri
        self.log_area.tag_config("system", foreground="#888")
        self.log_area.tag_config("success", foreground=self.colors["success"])
        self.log_area.tag_config("error", foreground=self.colors["danger"])
        self.log_area.tag_config("action", foreground=self.colors["accent"])
        self.log_area.tag_config("warning", foreground=self.colors["warning"])

    def create_footer(self):
        footer = tk.Frame(self.root, bg=self.colors["panel"], height=25)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="F1: Kilit | F5: Başlat | F6: Durdur | ESC: Kapat", 
                 font=("Segoe UI", 7), bg=self.colors["panel"], fg="#666").pack(pady=5)

    # --- FONKSİYONLAR ---

    def log(self, message, tag="text"):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"> {message}\n", tag)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def load_solver(self):
        try:
            self.solver = get_solver()
            self.log("Yapay Zeka Hazır!", "success")
        except: 
            self.log("AI Modülü Yüklenemedi!", "error")

    def real_click(self, x, y, button='left'):
        # Hedefe ışınlan
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
        time.sleep(0.12)
        
        # Tıkla
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        down = MOUSEEVENTF_LEFTDOWN if button == 'left' else MOUSEEVENTF_RIGHTDOWN
        up = MOUSEEVENTF_LEFTUP if button == 'left' else MOUSEEVENTF_RIGHTUP
        
        ii_.mi = MouseInput(0, 0, 0, down, 0, ctypes.pointer(extra))
        SendInput(Input(ctypes.c_ulong(0), ii_))
        time.sleep(0.12)
        
        ii_.mi = MouseInput(0, 0, 0, up, 0, ctypes.pointer(extra))
        SendInput(Input(ctypes.c_ulong(0), ii_))
        time.sleep(0.1)

    def calibrate(self):
        x, y = pyautogui.position()
        self.ref_x, self.ref_y = x, y
        self.calibrated = True
        self.log(f"Kilitlendi: {self.ref_x}, {self.ref_y}", "system")
        self.status_var.set("HAZIR")
        self.canvas_status.itemconfig(self.status_circle, fill=self.colors["warning"])

    def start_bot(self):
        if self.calibrated:
            self.running = True
            self.status_var.set("ÇALIŞIYOR")
            self.canvas_status.itemconfig(self.status_circle, fill=self.colors["success"])
            self.log("Bot Başlatıldı", "success")

    def stop_bot(self):
        self.running = False
        self.status_var.set("DURDURULDU")
        self.canvas_status.itemconfig(self.status_circle, fill=self.colors["danger"])
        self.log("Bot Durduruldu", "error")

    def hardware_listener(self):
        while True:
            if is_key_down(0x70): self.root.after(0, self.calibrate); time.sleep(0.5) # F1
            elif is_key_down(0x74): self.root.after(0, self.start_bot); time.sleep(0.5) # F5
            elif is_key_down(0x75): self.root.after(0, self.stop_bot); time.sleep(0.5) # F6
            elif is_key_down(0x1B): # ESC
                self.running = False
                self.root.quit()
                break
            time.sleep(0.05)

    # --- PARÇA TANIMA ---
    def identify_piece_on_cursor(self):
        # Mouse'u F1 noktasına (+16 piksel ortaya) götür
        ctypes.windll.user32.SetCursorPos(int(self.ref_x + 16), int(self.ref_y + 16))
        time.sleep(0.35) 

        try:
            screenshot = pyautogui.screenshot(region=(int(self.ref_x), int(self.ref_y), 32, 32))
            crop_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except: return None

        pieces = [
            ("fish_2.png", 0), # TEKLİ
            ("fish_1.png", 3), # ÇUBUK
            ("fish_3.png", 5), # L ŞEKLİ
            ("fish_4.png", 4), # TERS L
            ("fish_5.png", 1), # KARE
            ("fish_6.png", 2)  # Z ŞEKLİ
        ]
        
        for img_name, logic_id in pieces:
            path = os.path.join(self.asset_path, img_name)
            if not os.path.exists(path): continue
            template = cv2.imread(path)
            res = cv2.matchTemplate(crop_img, template, cv2.TM_CCOEFF_NORMED)
            if cv2.minMaxLoc(res)[1] > 0.75: return logic_id 
        return None

    def bot_loop(self):
        game_memory = None
        while True:
            if self.running and self.calibrated and self.solver:
                if game_memory is None: game_memory = Jigsaw()
                
                if game_memory.has_finished(): 
                    self.log("Tur tamamlandı. Bekleniyor...", "system")
                    game_memory = Jigsaw()
                    time.sleep(1.5)
                    continue

                # 1. Sandık
                cx, cy = self.ref_x + bot_config.OFF_BTN_CHEST[0], self.ref_y + bot_config.OFF_BTN_CHEST[1]
                self.real_click(cx, cy)
                time.sleep(1.0) 

                # 2. Evet -> Parça Mouse'a
                yx, yy = self.ref_x + bot_config.OFF_BTN_YES_ADD[0], self.ref_y + bot_config.OFF_BTN_YES_ADD[1]
                self.real_click(yx, yy)
                time.sleep(0.3) 

                # 3. Tanı (F1'e git)
                piece_id = self.identify_piece_on_cursor()

                if piece_id is not None:
                    best_action = self.solver.solve(game_memory)
                    
                    if best_action == SKIP_ACTION:
                        self.log("PAS GEÇİLİYOR", "warning")
                        # Sağ tık (köşedeyken)
                        self.real_click(self.ref_x + 16, self.ref_y + 16, button='right') 
                        time.sleep(0.8)
                        self.real_click(yx, yy) # Onayla
                    else:
                        # 4. Hedef
                        col, row = (best_action >> 2) & 0x0F, best_action & 0x03
                        tx, ty = self.ref_x + (col * CELL_SIZE), self.ref_y + (row * CELL_SIZE)
                        
                        self.log(f"Yerleştiriliyor: {col},{row}", "action")
                        self.real_click(tx, ty)
                        time.sleep(0.9) 
                        
                        # 5. Onay
                        self.real_click(yx, yy)
                    
                    game_memory.perform_action(best_action)
                    self.stats_count += 1
                    self.stats_var.set(str(self.stats_count))
                    time.sleep(0.4)
                
                else:
                    self.log("Parça Tanınamadı! Atlanıyor.", "error")
                    self.real_click(self.ref_x + 16, self.ref_y + 16, button='right')
                    time.sleep(0.8)
                    self.real_click(yx, yy)

            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBotGUI(root)
    root.mainloop()