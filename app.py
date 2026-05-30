import customtkinter as ctk
import threading
import voice_engine
import security
import time
import pyautogui
import webbrowser
from file_system import FileManager
from rpa_engine import AutomationAgent

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class EliasApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ELIAS Assistant")
        self.geometry("450x700") 
        self.configure(fg_color="#F4F7FB") 
        
        self.brain = FileManager()
        self.robot = AutomationAgent()
        
        self.header = ctk.CTkFrame(self, fg_color="#FFFFFF", height=80, corner_radius=0)
        self.header.pack(fill="x", side="top")
        self.logo = ctk.CTkLabel(self.header, text="Dashboard", font=("Helvetica", 24, "bold"), text_color="#1E293B")
        self.logo.pack(side="left", padx=20, pady=20)
        self.status_dot = ctk.CTkLabel(self.header, text="● Locked", font=("Helvetica", 14), text_color="#EF4444")
        self.status_dot.pack(side="right", padx=20)

        self.card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=20)
        self.card.pack(fill="both", expand=True, padx=20, pady=20)
        self.log_box = ctk.CTkTextbox(self.card, font=("Arial", 14), text_color="#475569", fg_color="transparent", wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=15, pady=15)
        self.log(">> System Ready.\n")

        self.btn_auth = ctk.CTkButton(self, text="Authenticate Face ID", height=55, font=("Helvetica", 16, "bold"), 
                                      corner_radius=27, fg_color="#0EA5E9", hover_color="#0284C7", command=self.start_auth)
        self.btn_auth.pack(fill="x", padx=40, pady=(0, 20))

    def log(self, message):
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")

    def start_auth(self):
        self.btn_auth.configure(state="disabled", text="Activating Camera...")
        threading.Thread(target=self.run_security_check).start()

    def run_security_check(self):
        self.log(">> Running Biometric Analysis...")
        if security.login(): 
            self.status_dot.configure(text="● Online", text_color="#10B981")
            self.btn_auth.configure(text="Listening...", fg_color="#10B981")
            self.log(">> Access Granted.")
            self.update()
            voice_engine.speak("Access granted.")
            time.sleep(1)
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.status_dot.configure(text="● Denied", text_color="#EF4444")
            self.btn_auth.configure(state="normal", text="Try Face ID Again")
            self.log(">> SECURITY ALERT: Unauthorized Person.")
            self.update()
            voice_engine.speak("Unauthorized person! Access denied.")

    def listen_loop(self):
        # Master lists of trigger prefixes for searches
        yt_prefixes = ["search youtube ", "youtube ", "you tube ", "u tube ", "you two "]
        gg_prefixes = ["search google ", "google ", "goggle ", "go girl "]
        gen_prefixes = ["search for ", "search 4 ", "charge for ", "surge for ", "church for ", "sort for ", "search "]
        find_prefixes = ["find ", "fine ", "sign ", "bind ", "type in search "]
        type_prefixes = ["type ", "write ", "right ", "pipe ", "tripe ", "tight "]

        while True:
            command = voice_engine.listen()
            if not command or command == "none": continue
            self.log(f"You: {command}")

            # --- 1. DIRECT YOUTUBE SEARCHING ("Search whatever you want") ---
            if any(command.startswith(prefix) for prefix in yt_prefixes):
                for p in yt_prefixes:
                    if command.startswith(p):
                        query = command[len(p):].strip()
                        break
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                self.log(f">> YouTube Search: {query}")
                continue

            # --- 2. DIRECT GOOGLE SEARCHING ("Search whatever you want") ---
            elif any(command.startswith(prefix) for prefix in gg_prefixes):
                for p in gg_prefixes:
                    if command.startswith(p):
                        query = command[len(p):].strip()
                        break
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.log(f">> Google Search: {query}")
                continue

            # --- 3. GENERAL GOOGLE SEARCH ("Search whatever you want") ---
            elif any(command.startswith(prefix) for prefix in gen_prefixes):
                for p in gen_prefixes:
                    if command.startswith(p):
                        query = command[len(p):].strip()
                        break
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.log(f">> Web Search: {query}")
                continue

            # --- 4. IN-APP KEYBOARD SEARCH (Types into current active window) ---
            elif any(command.startswith(prefix) for prefix in find_prefixes):
                for p in find_prefixes:
                    if command.startswith(p):
                        query = command[len(p):].strip()
                        break
                self.robot.perform_search(query)
                self.log(f">> Keyboard Search: {query}")
                continue
                
            # --- 5. DIRECT TYPING ---
            elif any(command.startswith(prefix) for prefix in type_prefixes):
                for p in type_prefixes:
                    if command.startswith(p):
                        text = command[len(p):].strip()
                        break
                pyautogui.write(text, interval=0.02)
                self.log(f">> Typed: {text}")
                continue

            # --- 6. EXTREME PHONETIC SCROLLING ---
            elif any(word in command for word in ["scroll down", "page down", "scall down", "school down", "crawl down", "roll down", "fall down", "scroll town"]): 
                self.robot.scroll("down")
            elif any(word in command for word in ["scroll up", "page up", "pull up", "roll up", "grow up", "scale up"]): 
                self.robot.scroll("up")
            elif any(word in command for word in ["scroll left", "page left"]): 
                self.robot.scroll("left")
            elif any(word in command for word in ["scroll right", "page right", "scroll write"]): 
                self.robot.scroll("right")

            # --- 7. EXTREME PHONETIC ARROW KEY NAVIGATION ---
            elif any(word in command for word in ["move left", "go left", "lap", "lift", "laugh", "love"]): 
                self.robot.navigate("left")
            elif any(word in command for word in ["move right", "go right", "ride", "light", "write", "white"]): 
                self.robot.navigate("right")
            elif any(word in command for word in ["move up", "go up", "hop", "cup", "pup"]): 
                self.robot.navigate("up")
            elif any(word in command for word in ["move down", "go down", "town", "dawn", "down", "gown"]): 
                self.robot.navigate("down")

            # --- 8. EXTREME PHONETIC STANDARD ACTIONS ---
            elif any(word in command for word in ["new tab", "open a new tab", "create a tab", "mu tab", "new top", "you tab", "do tap"]):
                self.robot.open_new_tab()
                self.log(">> Opened a new tab.")
                continue

            elif any(word in command for word in ["new page", "new document", "blank page", "new pitch", "new cage"]):
                self.robot.open_new_page()
                self.log(">> Opened a new page.")
                continue

            elif any(word in command for word in ["desktop", "show desktop", "dash top", "test top", "next top", "disk top"]): 
                self.robot.focus_desktop()
            elif any(word in command for word in ["close", "shut", "exit window", "clothes", "shots", "closed", "close it"]): 
                self.robot.close_window()
            elif any(word in command for word in ["go back", "move back", "back", "return", "pack", "bag", "track"]): 
                self.robot.go_back()
            elif any(word in command for word in ["open folder", "open file", "enter", "ok", "select", "click", "hunter", "okay", "an tar", "in tar", "center", "winter"]): 
                self.robot.press_ok()

            # --- 9. DICTATION & APPS ---
            elif "write in" in command or "ride in" in command or "writing" in command:
                voice_engine.speak("What should I write?")
                content = voice_engine.listen()
                voice_engine.speak("What should I save the file as?")
                filename = voice_engine.listen()
                self.robot.dictate_and_save(command, content, filename)

            elif "open" in command and not any(w in command for w in ["folder", "file"]):
                target = command.replace("open", "").strip()
                if not self.brain.find_and_open(target):
                    self.robot.open_app_via_windows(target)

            elif any(word in command for word in ["exit", "stop listening", "turn off"]):
                self.destroy()
                break

if __name__ == "__main__":
    app = EliasApp()
    app.mainloop()