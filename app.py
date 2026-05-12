import streamlit as st
import requests
from camera_input_live import camera_input_live
from PIL import Image
import io

# ==========================================
# 1. SETUP & DESIGN
# ==========================================
st.set_page_config(page_title="NutriScan Safe", page_icon="🍏", layout="centered")

# Schickes Design einfügen
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stAlert { border-radius: 15px; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #2ECC71; color: white; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 10px; border: 2px solid #2ECC71; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR (TEAM & INFO)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3075/3075977.png", width=100)
st.sidebar.title("NutriScan Pro")
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Entwickler-Team")
team = ["Maximilian Maier", "Benjamin Mehling", "Ben Henkel", "Marius Boulos", "Sophie Hartwig"]
for member in team:
    st.sidebar.write(f"✅ {member}")

st.sidebar.markdown("---")
st.sidebar.info("Projekt: 10th Grade Chemistry/IT - Hanns-Seidel-Gymnasium")

# ==========================================
# 3. SPRACHE & ALLERGIE-PROFIL
# ==========================================
st.title("🍏 SafeScanning NutriScan")
lang = st.radio("Sprache wählen / Choose Language", ["Deutsch", "English"], horizontal=True)

# Übersetzungen
if lang == "Deutsch":
    t = {
        "profile": "Dein Allergie-Profil",
        "select": "Wähle deine Unverträglichkeiten:",
        "scan_title": "📸 Barcode Scanner",
        "manual_title": "🔢 Manuelle Eingabe",
        "placeholder": "Barcode-Nummer hier eintippen...",
        "safe": "✅ Dieses Produkt ist SICHER für dich!",
        "warn": "❌ ACHTUNG: Enthält kritische Stoffe:",
        "not_found": "Produkt nicht in der Datenbank. Probiere '3017620425035' (Nutella).",
        "net_error": "Datenbank-Verbindung eingeschränkt (Schul-WLAN?). Zeige Demo-Modus..."
    }
else:
    t = {
        "profile": "Your Allergy Profile",
        "select": "Select your intolerances:",
        "scan_title": "📸 Barcode Scanner",
        "manual_title": "🔢 Manual Entry",
        "placeholder": "Type barcode number here...",
        "safe": "✅ This product is SAFE for you!",
        "warn": "❌ WARNING: Contains critical ingredients:",
        "not_found": "Product not found. Try '3017620425035' (Nutella).",
        "net_error": "Database connection limited. Showing demo mode..."
    }

with st.expander(t["profile"], expanded=True):
    user_allergies = st.multiselect(t["select"], 
        ["Gluten", "Lactose", "Fructose", "Nüsse", "Erdnüsse", "Soja", "Eier", "Fisch", "Senf"])

# ==========================================
# 4. SCANNER & INPUT
# ==========================================
st.subheader(t["scan_title"])
st.write("Halte den Barcode in die Kamera oder tippe ihn unten ein.")
camera_input_live() # Zeigt das Live-Bild

barcode = st.text_input(t["manual_title"], placeholder=t["placeholder"])

# ==========================================
# 5. DIE LOGIK (DATENBANK & CHECK)
# ==========================================
if barcode:
    # Säuberung der Eingabe (nur Zahlen)
    clean_barcode = "".join(filter(str.isdigit, barcode))
    
    if len(clean_barcode) > 7:
        url = f"https://world.openfoodfacts.org/api/v2/product/{clean_barcode}.json"
        
        try:
            # Versuch die echte Datenbank abzufragen
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get("status") == 1:
                product = data["product"]
                p_name = product.get("product_name", "Unbekanntes Produkt")
                p_img = product.get("image_front_url")
                
                # Inhaltsstoffe analysieren
                ingreds = str(product.get("ingredients_text", "")).lower()
                allerg_tags = str(product.get("allergens_hierarchy", [])).lower()
                full_text = ingreds + allerg_tags
                
                st.divider()
                st.subheader(f"Ergebnis für: {p_name}")
                if p_img: st.image(p_img, width=200)
                
                # Allergie-Check
                found = [a for a in user_allergies if a.lower() in full_text]
                
                if found:
                    st.error(f"{t['warn']} {', '.join(found)}")
                else:
                    st.success(t["safe"])
            else:
                st.warning(t["not_found"])
                
        except:
            # NOTFALL-MODUS: Wenn das Schul-WLAN die API blockt
            st.warning(t["net_error"])
            
            # Demo-Daten für Nutella (falls die Nummer eingegeben wird)
            if clean_barcode == "3017620425035":
                st.subheader("Ergebnis für: Nutella (Demo-Modus)")
                st.image("
