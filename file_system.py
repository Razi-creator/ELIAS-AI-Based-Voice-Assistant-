import os
import webbrowser

class FileManager:
    def __init__(self):
        self.current_path = os.path.expanduser("~") 
        self.history = [] 
        
        # --- EXTREME PHONETIC ALIAS DICTIONARY: SETTINGS ---
        self.system_commands = {
            "ms-settings:": ["settings", "setting", "set things", "sit things", "sad things", "seethings"],
            "ms-settings:display": ["display", "screen", "monitor", "this play", "this lay", "spray"],
            "ms-settings:sound": ["sound", "audio", "volume", "some", "sand"],
            "ms-settings:bluetooth": ["bluetooth", "blue tooth", "gluteus", "blue"],
            "ms-settings:network-wifi": ["wifi", "wi-fi", "internet", "network", "y5", "wife i", "why fye", "net work"],
            "ms-settings:windowsupdate": ["update", "windows update", "up date", "of date"],
            "ms-settings:windowsdefender": ["security", "defender", "antivirus", "secure it", "defend"]
        }

        # --- EXTREME PHONETIC ALIAS DICTIONARY: APPS ---
        self.system_apps = {
            "start winword": ["word", "ms word", "microsoft word", "ward", "weird", "bird", "what", "wood", "world", "work"],
            "start excel": ["excel", "xl", "x l", "axle", "exel", "x cell", "ms excel", "egg cell", "exhale", "accel"],
            "start powerpnt": ["powerpoint", "power point", "ppt", "power pint", "our point", "tower point"],
            "notepad": ["notepad", "note pad", "not pad", "node pad", "no pad", "notebook", "snow pad"],
            "start msteams:": ["teams", "team", "ms teams", "teems", "themes", "teens", "tims", "streams"],
            "calc": ["calculator", "calc", "calculate", "cal", "calculate her"]
        }

        # --- EXTREME PHONETIC ALIAS DICTIONARY: SYSTEM PATHS ---
        self.special_paths = {
            "explorer shell:::{20D04FE0-3AEA-1069-A2D8-08002B30309D}": [
                "this pc", "this bc", "that bc", "these pc", "this p c", "this b c", "my computer", 
                "this piece", "this dc", "this peasy", "speed sea", "is pc"
            ],
            "C:\\": [
                "local disk c", "drive c", "c drive", "see drive", "sea drive", "local disc c", 
                "local this c", "local desk c", "look at this c", "see trial", "seed drive", "cd drive"
            ],
            "D:\\": [
                "local disk d", "drive d", "d drive", "the drive", "local disc d", "local desk d", 
                "local this d", "local this the", "tea drive", "deep drive", "the trial", "d drive"
            ]
        }

        self.search_roots = [
            r"D:\\",
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Documents")
        ]

    def open_website(self, target):
        if any(w in target for w in ["youtube", "you tube", "u tube", "you two"]):
            webbrowser.open("https://www.youtube.com")
            return True
        if any(w in target for w in ["google", "goggle", "go girl"]):
            webbrowser.open("https://www.google.com")
            return True
            
        url = target.replace("open", "").strip().lower()
        domains = [".com", "dot com", ".net", ".org", ".edu", ".pk"]
        if any(dom in url for dom in domains):
            url = url.replace("dot com", ".com").replace(" ", "")
            if not url.startswith("http"): url = "https://" + url
            webbrowser.open(url)
            return True
        return False

    def open_setting(self, target):
        for command, aliases in self.system_commands.items():
            if any(alias in target for alias in aliases):
                os.system(f"start {command}")
                return True
        return False

    def open_system_app(self, target):
        for command, aliases in self.system_apps.items():
            if any(alias in target for alias in aliases):
                os.system(command)
                return True
        return False

    def open_path(self, path):
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    if path != self.current_path:
                        self.history.append(self.current_path)
                        self.current_path = path
                os.startfile(path)
                return True
            except Exception: pass
        return False

    def go_back(self):
        if self.history:
            prev_path = self.history.pop()
            self.current_path = prev_path
            return prev_path
        parent_dir = os.path.dirname(self.current_path)
        if os.path.exists(parent_dir):
            self.current_path = parent_dir
            return parent_dir
        return None

    def find_and_open(self, target_name):
        target = target_name.lower()
        
        if self.open_website(target): return "website"
        if self.open_system_app(target): return "app"
        if self.open_setting(target): return "setting"

        for command, aliases in self.special_paths.items():
            if any(alias in target for alias in aliases):
                if "explorer" in command:
                    os.system(f"start {command}")
                else:
                    os.startfile(command)
                return True

        try:
            for item in os.listdir(self.current_path):
                if target in item.lower():
                    return self.open_path(os.path.join(self.current_path, item))
        except: pass

        for root_dir in self.search_roots:
            if not os.path.exists(root_dir): continue
            for dirpath, dirnames, filenames in os.walk(root_dir):
                for d in dirnames:
                    if target in d.lower(): return self.open_path(os.path.join(dirpath, d))
                for f in filenames:
                    if target in f.lower(): return self.open_path(os.path.join(dirpath, f))
        return False