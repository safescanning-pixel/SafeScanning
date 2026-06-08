#!/usr/bin/env python3
"""
Verschlüsselt app.py und speichert den Schlüssel sicher.
Dieses Script nur einmal lokal ausführen!
"""
from cryptography.fernet import Fernet
import base64
import hashlib

# Generiere einen neuen Verschlüsselungsschlüssel
encryption_key = Fernet.generate_key()

print("=" * 60)
print("🔐 VERSCHLÜSSELUNGS-SETUP")
print("=" * 60)
print("\n✅ Neuer Verschlüsselungs-Schlüssel generiert:\n")
print(encryption_key.decode())
print("\n" + "=" * 60)
print("📋 NÄCHSTE SCHRITTE:")
print("=" * 60)
print("\n1. GitHub → Settings → Secrets and variables → Actions")
print("2. Neues Secret hinzufügen:")
print("   Name: ENCRYPTION_KEY")
print(f"   Value: {encryption_key.decode()}")
print("\n3. Speichern und fertig!")
print("=" * 60 + "\n")
