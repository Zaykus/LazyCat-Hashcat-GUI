import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import threading
import shutil
import webbrowser
import platform

# --- THEME: STEALTH BLACK ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Colors
C_BG = "#050505"
C_SIDE = "#101010"
C_CARD = "#161616"
C_BORDER = "#333333"
C_INPUT = "#000000"

class LazyCatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # WINDOW SETUP
        self.title("LAZYCAT // PURR-FESSIONAL EDITION")
        self.geometry("1100x750")
        self.configure(fg_color=C_BG)

        # PATH LOGIC
        if getattr(sys, 'frozen', False):
            self.app_dir = os.path.dirname(sys.executable)
            self.internal_dir = sys._MEIPASS
        else:
            self.app_dir = os.path.abspath(".")
            self.internal_dir = os.path.abspath(".")

        self.dirs = {
            "hashes": os.path.join(self.app_dir, "project_data", "hashes"),
            "wordlists": os.path.join(self.app_dir, "wordlists")
        }
        for d in self.dirs.values():
            if not os.path.exists(d): os.makedirs(d)

        # VARIABLES
        self.hashcat_exe = ""
        self.target_file = ""
        self.custom_wordlist = ""
        self.attack_mode = ctk.StringVar(value="0")

        # GRID LAYOUT
        self.grid_columnconfigure(0, minsize=320)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_ui()
        self.find_hashcat()
        self.scan_wordlists()

    def find_hashcat(self):
        bundled = os.path.join(self.internal_dir, "hashcat", "hashcat.exe")
        external = os.path.join(self.app_dir, "hashcat.exe")
        if os.path.exists(bundled): self.hashcat_exe = bundled; self.log("[CAT] Internal Engine Ready.")
        elif os.path.exists(external): self.hashcat_exe = external; self.log("[CAT] External Engine Ready.")
        else: self.log("[ERR] CRITICAL: Hashcat Not Found.")

    def scan_wordlists(self):
        w_list = ["Custom..."]
        if os.path.exists(self.dirs['wordlists']):
            files = [f for f in os.listdir(self.dirs['wordlists']) if f.endswith('.txt')]
            w_list.extend(files)
        self.drop_wordlist.configure(values=w_list)
        if len(w_list) > 1:
            self.drop_wordlist.set(w_list[1])
            self.custom_wordlist = os.path.join(self.dirs['wordlists'], w_list[1])

    def create_ui(self):
        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color=C_SIDE, border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Header
        ctk.CTkLabel(self.sidebar, text="/// LAZYCAT", font=("Impact", 24), text_color="#fff").pack(pady=(30, 0), anchor="w", padx=20)
        ctk.CTkLabel(self.sidebar, text="PURR-FESSIONAL CRACKER", font=("Arial", 10), text_color="#666").pack(pady=(0, 20), anchor="w", padx=22)

        # 1. TARGET
        self.section_header("1. SNIFF TARGET", self.help_target)
        c1 = self.create_card()
        self.btn_conv = ctk.CTkButton(c1, text="OPEN CONVERTER (.CAP)", height=25, fg_color="#222", hover_color="#333", border_color="#444", border_width=1, command=lambda: webbrowser.open("https://hashcat.net/cap2hashcat/"))
        self.btn_conv.pack(fill="x", padx=10, pady=10)
        self.ent_hash = ctk.CTkEntry(c1, placeholder_text="No .hc22000 file", fg_color=C_INPUT, border_color=C_BORDER)
        self.ent_hash.pack(fill="x", padx=10, pady=(0,5))
        ctk.CTkButton(c1, text="BROWSE FILE", fg_color="#333", hover_color="#444", command=self.browse_hash).pack(fill="x", padx=10, pady=(0,10))

        # 2. CONFIG
        self.section_header("2. CAT TOYS (CONFIG)", self.help_hardware)
        c2 = self.create_card()
        row_hw = ctk.CTkFrame(c2, fg_color="transparent")
        row_hw.pack(fill="x", padx=10, pady=5)
        self.ent_id = ctk.CTkEntry(row_hw, width=50, fg_color=C_INPUT, border_color=C_BORDER)
        self.ent_id.insert(0, "1")
        self.ent_id.pack(side="left")
        ctk.CTkButton(row_hw, text="TEST GPU", width=120, fg_color="#222", hover_color="#333", command=self.check_gpu).pack(side="right")
        
        # 3. ATTACK
        self.section_header("3. POUNCE (ATTACK)", self.help_attack)
        c3 = self.create_card()
        
        # Dictionary
        ctk.CTkRadioButton(c3, text="WORDLIST (Dictionary)", variable=self.attack_mode, value="0", fg_color="white", text_color="#ccc", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        self.drop_wordlist = ctk.CTkOptionMenu(c3, values=["Scanning..."], command=self.set_wordlist, fg_color="#222", button_color="#333", button_hover_color="#444")
        self.drop_wordlist.pack(fill="x", padx=30, pady=(0,10))
        
        # Mask
        ctk.CTkRadioButton(c3, text="BRUTE-FORCE (Mask)", variable=self.attack_mode, value="3", fg_color="white", text_color="#ccc", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        self.ent_mask = ctk.CTkEntry(c3, placeholder_text="e.g. ?d?d?d?d?d?d?d?d", fg_color=C_INPUT, border_color=C_BORDER)
        self.ent_mask.pack(fill="x", padx=30, pady=(0,10))

        # ACTIONS
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#333").pack(fill="x", padx=20, pady=20) 
        self.btn_start = ctk.CTkButton(self.sidebar, text="START ATTACK", height=50, fg_color="#fff", text_color="black", hover_color="#ddd", font=("Arial", 14, "bold"), command=self.start_attack)
        self.btn_start.pack(fill="x", padx=20)
        ctk.CTkButton(self.sidebar, text="DID WE WIN? (REVEAL)", fg_color="transparent", border_color="#555", border_width=1, text_color="#aaa", hover_color="#222", command=self.reveal).pack(fill="x", padx=20, pady=10)


        # TERMINAL (RIGHT)
        self.right_frame = ctk.CTkFrame(self, fg_color=C_BG, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Read-Only Console
        self.console = ctk.CTkTextbox(self.right_frame, font=("Consolas", 12), fg_color="#000", text_color="#ccc", border_width=0)
        self.console.pack(fill="both", expand=True, padx=0, pady=0)
        self.console.configure(state="disabled") # Make Read-Only by default
        
        cmd_bar = ctk.CTkFrame(self.right_frame, height=40, fg_color="#111")
        cmd_bar.pack(fill="x", side="bottom")
        
        ctk.CTkLabel(cmd_bar, text="PS C:\\LAZYCAT>", font=("Consolas", 12), text_color="#555").pack(side="left", padx=10)
        self.ent_cmd = ctk.CTkEntry(cmd_bar, placeholder_text="Type command here...", fg_color="transparent", border_width=0, font=("Consolas", 12))
        self.ent_cmd.pack(side="left", fill="x", expand=True)
        self.ent_cmd.bind("<Return>", self.run_custom_command)

        self.log("LAZYCAT INITIALIZED. MEOW.")

    # --- HELPERS ---
    def section_header(self, text, help_func):
        f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        f.pack(fill="x", padx=20, pady=(15, 5))
        ctk.CTkLabel(f, text=text, font=("Arial", 11, "bold"), text_color="#666").pack(side="left")
        ctk.CTkButton(f, text="?", width=30, height=20, fg_color="#222", hover_color="#333", command=help_func).pack(side="right")

    def create_card(self):
        f = ctk.CTkFrame(self.sidebar, fg_color=C_CARD, border_color=C_BORDER, border_width=1, corner_radius=4)
        f.pack(fill="x", padx=20, pady=0)
        return f

    # --- GUIDE POPUPS ---
    def help_target(self):
        msg = "TARGET GUIDE:\n\n1. You need a Wi-Fi Handshake file (.cap) captured using tools like Wireshark.\n2. Hashcat cannot read .cap files directly.\n3. Click 'OPEN CONVERTER' to turn your .cap into a .hc22000 file.\n4. Load that .hc22000 file here."
        messagebox.showinfo("Help: Target", msg)

    def help_hardware(self):
        msg = "HARDWARE GUIDE:\n\nDevice ID:\n1 = Usually your main Graphics Card (Fastest)\n2 = Usually Integrated Graphics or CPU (Slower)\n\nClick 'TEST GPU' to see your list of devices."
        messagebox.showinfo("Help: Hardware", msg)

    def help_attack(self):
        msg = "ATTACK GUIDE:\n\n1. WORDLIST: Tries every word in a text file. Good for common passwords.\n\n2. BRUTE-FORCE (MASK): Tries combinations of characters.\n\nMask Cheatsheet:\n?d = Digit (0-9)\n?l = Lowercase (a-z)\n?u = Uppercase (A-Z)\n?s = Symbol (!@#)\n\nExamples:\n?d?d?d?d = 4 digit PIN (0000-9999)\n?d?d?d?d?d?d?d?d = 8 digit Number (Common for Wi-Fi)"
        messagebox.showinfo("Help: Brute-Force", msg)

    # --- LOGIC ---
    def log(self, txt):
        self.console.configure(state="normal") # Unlock
        self.console.insert("end", txt + "\n")
        self.console.see("end")
        self.console.configure(state="disabled") # Lock again

    def run_custom_command(self, event=None):
        cmd = self.ent_cmd.get()
        if not cmd: return
        self.log(f"\n> {cmd}")
        self.ent_cmd.delete(0, "end")
        threading.Thread(target=self.run_process_shell, args=(cmd,)).start()

    def run_process_shell(self, cmd):
        flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        try:
            cwd = os.path.dirname(self.hashcat_exe) if self.hashcat_exe else "."
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, text=True, creationflags=flags)
            for line in iter(p.stdout.readline, ''):
                self.log(line.strip())
            p.wait()
        except Exception as e: self.log(f"Error: {e}")

    def browse_hash(self):
        f = filedialog.askopenfilename(filetypes=[("Hashcat", "*.hc22000")])
        if f:
            self.target_file = f
            self.ent_hash.delete(0, "end"); self.ent_hash.insert(0, os.path.basename(f))
            self.log(f"[CAT] Target Loaded: {f}")

    def set_wordlist(self, choice):
        if choice == "Custom...":
            f = filedialog.askopenfilename()
            if f: self.custom_wordlist = f
        else:
            self.custom_wordlist = os.path.join(self.dirs['wordlists'], choice)
        self.log(f"[CAT] Wordlist Set: {os.path.basename(self.custom_wordlist)}")

    def check_gpu(self):
        self.log("\n[CAT] Sniffing Hardware...")
        threading.Thread(target=self.run_process_list, args=([self.hashcat_exe, "-I"],)).start()

    def start_attack(self):
        if not self.target_file: return messagebox.showerror("Err", "No Target File")
        cmd = [self.hashcat_exe, "-m", "22000", self.target_file, "-w", "3", "-d", self.ent_id.get()]
        if self.attack_mode.get() == "0":
            if not self.custom_wordlist: return messagebox.showerror("Err", "No Wordlist")
            cmd.append(self.custom_wordlist)
        else:
            if not self.ent_mask.get(): return messagebox.showerror("Err", "No Mask")
            cmd.extend(["-a", "3", self.ent_mask.get()])
        self.log("\n[CAT] POUNCING (ATTACK STARTED)...")
        threading.Thread(target=self.run_process_list, args=(cmd,)).start()

    def run_process_list(self, cmd_list):
        cwd = os.path.dirname(self.hashcat_exe)
        flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        try:
            p = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, text=True, bufsize=1, creationflags=flags)
            for line in iter(p.stdout.readline, ''):
                self.log(line.strip())
            p.wait()
            self.log("\n[CAT] Nap time. (Process Finished)")
        except Exception as e: self.log(f"Process Error: {e}")

    def reveal(self):
        if not self.target_file: return
        self.log("\n[CAT] Checking if we caught the mouse...")
        cmd = [self.hashcat_exe, "-m", "22000", self.target_file, "--show"]
        threading.Thread(target=self.run_process_list, args=(cmd,)).start()

if __name__ == "__main__":
    app = LazyCatApp()
    app.mainloop()