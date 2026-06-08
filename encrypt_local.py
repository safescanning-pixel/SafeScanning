#!/usr/bin/env python3
"""
Verschlüsselt app.py für Passwort-Schutz
Dieses Script nur LOKAL ausführen, NICHT auf GitHub committen!
"""
from cryptography.fernet import Fernet

def encrypt_app():
    # WICHTIG: Diesen Schlüssel von GitHub Secrets verwenden!
    KEY = b"gAAAAABl-GENERIERTER-SCHLUESSEL"  # Wird durch Ihren echten Schlüssel ersetzt
    
    try:
        # Lese app.py
        with open("app.py", "rb") as f:
            original_data = f.read()
        
        # Verschlüssele
        cipher = Fernet(KEY)
        encrypted_data = cipher.encrypt(original_data)
        
        # Speichere als app.py.encrypted
        with open("app.py.encrypted", "wb") as f:
            f.write(encrypted_data)
        
        print("✅ app.py erfolgreich verschlüsselt!")
        print("📁 Neue Datei: app.py.encrypted")
        print("\n⚠️  WICHTIG:")
        print("   1. app.py LÖSCHEN (git rm app.py)")
        print("   2. app.py.encrypted und run_app.py committen")
        print("   3. Der Schlüssel ist in GitHub Secrets sicher gespeichert!")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    encrypt_app()
