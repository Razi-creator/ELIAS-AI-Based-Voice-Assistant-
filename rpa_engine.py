import pyautogui
import time
import os
import subprocess

class AutomationAgent:
    def __init__(self):
        pyautogui.FAILSAFE = True 
        pyautogui.PAUSE = 0.1 

    def perform_search(self, query):
        pyautogui.hotkey('ctrl', 'e')  
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'l')  
        time.sleep(0.1)
        pyautogui.press('/')           
        time.sleep(0.5) 
        pyautogui.write(query, interval=0.02)
        time.sleep(0.2)
        pyautogui.press('enter')

    def scroll(self, direction):
        if direction == "down": pyautogui.scroll(-800)
        elif direction == "up": pyautogui.scroll(800)
        elif direction == "right": pyautogui.hscroll(800)
        elif direction == "left": pyautogui.hscroll(-800)

    def navigate(self, direction):
        if direction == "down": pyautogui.press('down')
        elif direction == "up": pyautogui.press('up')
        elif direction == "left": pyautogui.press('left')
        elif direction == "right": pyautogui.press('right')

    def press_ok(self):
        pyautogui.press('enter')

    def close_window(self):
        pyautogui.hotkey('alt', 'f4')

    def go_back(self):
        pyautogui.hotkey('alt', 'left')

    def open_new_tab(self):
        pyautogui.hotkey('ctrl', 't')

    # --- NEW: OPEN BLANK PAGE IN WORD/NOTEPAD ---
    def open_new_page(self):
        """Presses Ctrl+N to open new pages/documents in Word and Notepad."""
        pyautogui.hotkey('ctrl', 'n')

    def focus_desktop(self):
        pyautogui.hotkey('win', 'd')

    def open_app_via_windows(self, app_name):
        pyautogui.press('win')
        time.sleep(0.5) 
        pyautogui.write(app_name, interval=0.05)
        time.sleep(1) 
        pyautogui.press('enter')
        return True

    def open_teams_section(self, section):
        try:
            os.system("start msteams:")
            time.sleep(3)
            if "activity" in section: pyautogui.hotkey('ctrl', '1')
            elif "chat" in section: pyautogui.hotkey('ctrl', '2')
            elif "teams" in section: pyautogui.hotkey('ctrl', '3')
            elif "assignments" in section: pyautogui.hotkey('ctrl', '4')
            return True
        except: return False

    def dictate_and_save(self, app_name, content, filename):
        if "notepad" in app_name: subprocess.Popen("notepad.exe")
        elif "word" in app_name: os.system("start winword")
        elif "excel" in app_name: os.system("start excel")
        
        time.sleep(3) 
        if "word" in app_name or "excel" in app_name:
            pyautogui.press('enter')
            time.sleep(1.5)

        if not content or content == "none": content = "Automated test document."
        pyautogui.write(content, interval=0.02)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1.5)
        
        if not filename or filename == "none": filename = "Auto_Save"
        pyautogui.write(filename)
        time.sleep(0.5)
        pyautogui.press('enter')
        return True