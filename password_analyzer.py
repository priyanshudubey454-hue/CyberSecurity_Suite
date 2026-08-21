import re
import requests

def check_password_strength(password):
    """Check password strength and return score with suggestions"""
    score = 0
    suggestions = []
    
    # Length check
    if len(password) < 8:
        suggestions.append("❌ Password should be at least 8 characters long")
    elif len(password) >= 12:
        score += 2
    else:
        score += 1
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one uppercase letter (A-Z)")
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one lowercase letter (a-z)")
    
    # Digit check
    if re.search(r'\d', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one digit (0-9)")
    
    # Special character check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        suggestions.append("❌ Add at least one special character (!@#$%^&*)")
    
    # Common password check
    common_passwords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'admin', 'letmein']
    if password.lower() in common_passwords:
        score = 0
        suggestions = ["❌ This is a commonly used password! Choose something unique."]
    
    # Determine strength
    if score >= 5:
        strength = "🟢 Strong"
    elif score >= 3:
        strength = "🟡 Medium"
    else:
        strength = "🔴 Weak"
    
    return strength, score, suggestions

def check_breach(password):
    """Check if password has been breached using HaveIBeenPwned API"""
    try:
        import hashlib
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code == 200:
            if suffix in response.text:
                return True
        return False
    except:
        return "⚠️ Could not check breach status (check internet)"