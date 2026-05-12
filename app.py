import streamlit as st
import requests
from camera_input_live import camera_input_live
from PIL import Image
import io

# 1. SETUP & DESIGN
st.set_page_config(page_title="NutriScan Safe", page_icon="🍏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stAlert { border-radius: 15px; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #2ECC71; color: white; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 10px; border: 2px solid #2ECC71; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR
st.sidebar.title("NutriScan Pro")
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Entwickler-Team")
team = ["Maximilian Maier", "Benjamin Mehling", "Ben Henkel", "Marius Boulos", "Sophie Hartwig"]
for member in team:
    st.sidebar.write(f"✅ {member}")

# 3. SPRACHE & PROFIL
st.title("🍏 SafeScanning NutriScan")
lang = st.radio("Sprache wählen", ["Deutsch", "English"], horizontal=True)

if lang == "Deutsch":
    t = {
        "profile": "Dein Allergie-Profil",
        "select": "Wähle deine Unverträglichkeiten:",
        "scan_title": "📸 Barcode Scanner",
        "manual_title": "🔢 Manuelle Eingabe",
        "placeholder": "Barcode-Nummer hier eintippen...",
        "safe": "✅ Sicher für dich!",
        "warn": "❌ ACHTUNG: Enthält:",
        "not_found": "Produkt nicht gefunden.",
        "net_error": "Datenbank-Fehler (Schul-WLAN?). Zeige Demo..."
    }
else:
    t = {
        "profile": "Your Profile",
        "select": "Select your intolerances:",
        "scan_title": "📸 Barcode Scanner",
        "manual_title": "🔢 Manual Entry",
        "placeholder": "Type barcode here...",
        "safe": "✅ SAFE for you!",
        "warn": "❌ WARNING: Contains:",
        "not_found": "Product not found.",
        "net_error": "Network error. Showing demo..."
    }

with st.expander(t["profile"], expanded=True):
    user_allergies = st.multiselect(t["select"], 
        ["Gluten", "Lactose", "Fructose", "Nüsse", "Erdnüsse", "Soja", "Eier", "Fisch"])

# 4. SCANNER
st.subheader(t["scan_title"])
camera_input_live() 

barcode = st.text_input(t["manual_title"], placeholder=t["placeholder"])

# 5. LOGIK
if barcode:
    clean_bc = "".join(filter(str.isdigit, barcode))
    
    if len(clean_bc) > 7:
        url = f"https://world.openfoodfacts.org/api/v2/product/{clean_bc}.json"
        try:
            response = requests.get(url, timeout=7)
            data = response.json()
            
            if data.get("status") == 1:
                prod = data["product"]
                st.subheader(f"Ergebnis: {prod.get('product_name', 'Unbekannt')}")
                if prod.get("image_front_url"):
                    st.image(prod["image_front_url"], width=200)
                
                txt = str(prod.get("ingredients_text", "")).lower() + str(prod.get("allergens_hierarchy", [])).lower()
                found = [a for a in user_allergies if a.lower() in txt]
                
                if found:
                    st.error(f"{t['warn']} {', '.join(found)}")
                else:
                    st.success(t["safe"])
            else:
                st.warning(t["not_found"])
        except:
            st.warning(t["net_error"])
            if clean_bc == "3017620425035":
                st.subheader("Nutella (Demo)")
                st.image("https://images.openfoodfacts.org/images/products/301/762/042/5035/front_de.676.400.jpg", width=200)
                if any(x in ["Nüsse", "Haselnuss"] for x in user_allergies):
                    st.error(f"{t['warn']} Haselnüsse")
                else:
                    st.success(t["safe"])

st.markdown("---")
st.caption("NutriScan v2.0 | HSG 10a")
