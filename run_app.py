#!/usr/bin/env python3
"""
run_app.py - Entschlüsselt app.py.encrypted und startet die Streamlit-App
Der Verschlüsselungs-Schlüssel kommt aus GitHub Secrets (ENCRYPTION_KEY)
"""
import os
import sys
import subprocess
from cryptography.fernet import Fernet

def main():
    # Lese den Schlüssel aus der Umgebungsvariable
    encryption_key = os.getenv("ENCRYPTION_KEY")
    
    if not encryption_key:
        print("❌ FEHLER: ENCRYPTION_KEY nicht gefunden!")
        print("   GitHub Secret 'ENCRYPTION_KEY' muss gesetzt sein.")
        sys.exit(1)
    
    try:
        print("🔐 Entschlüssele app.py...")
        
        # Entschlüssele die Datei
        cipher = Fernet(encryption_key.encode())
        
        with open("app.py.encrypted", "rb") as f:
            encrypted_data = f.read()
        
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Schreibe temporär als app_temp.py
        with open("app_temp.py", "wb") as f:
            f.write(decrypted_data)
        
        print("✅ App erfolgreich entschlüsselt!")
        print("🚀 Starte Streamlit...\n")
        
        # Starte Streamlit mit der entschlüsselten Datei
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app_temp.py"],
            check=False
        )
        
        # Cleanup
        if os.path.exists("app_temp.py"):
            os.remove("app_temp.py")
            
    except FileNotFoundError:
        print("❌ FEHLER: app.py.encrypted nicht gefunden!")
        print("   Bitte verschlüsseln Sie zuerst app.py mit encrypt_local.py")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ FEHLER beim Entschlüsseln: {e}")
        print("   Der Verschlüsselungs-Schlüssel könnte falsch sein.")
        sys.exit(1)

if __name__ == "__main__":
    main()
