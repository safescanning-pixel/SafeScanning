import streamlit as st
import requests
from camera_input_live import camera_input_live
from PIL import Image
import io

# 1. Seite konfigurieren
st.set_page_config(page_title="NutriScan Pro", page_icon="🔍", layout="centered")

# Custom CSS für den "Cleanen" Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; border: none; background-color: #2ECC71; color: white; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Team & Info in der Sidebar
st.sidebar.title("NutriScan Pro")
st.sidebar.subheader("Entwickler-Team")
for name in ["Maximilian Maier", "Benjamin Mehling", "Ben Henkel", "Marius Boulos", "Sophie Hartwig"]:
    st.sidebar.write(f"• {name}")

# 3. Sprache & Profil
st.title("🍏 NutriScan")
lang = st.radio("Sprache / Language", ["Deutsch", "English"], horizontal=True)

if lang == "Deutsch":
    t_profile = "Dein Allergie-Profil"
    t_select = "Wähle deine Allergien:"
    t_scan = "Barcode Live-Scanner"
    t_manual = "Oder Barcode manuell eingeben:"
    t_safe = "✅ Sicher für dich!"
    t_warn = "❌ WARNUNG: Enthält"
else:
    t_profile = "Your Profile"
    t_select = "Select your allergies:"
    t_scan = "Live Barcode Scanner"
    t_manual = "Or enter barcode manually:"
    t_safe = "✅ Safe for you!"
    t_warn = "❌ WARNING: Contains"

with st.expander(t_profile, expanded=True):
    allergies = st.multiselect(t_select, ["Gluten", "Lactose", "Fructose", "Nüsse", "Erdnüsse", "Soja", "Eier", "Fisch"])

# 4. LIVE SCANNER
st.subheader(t_scan)
st.info("Halte den Barcode mittig in die Kamera. (Funktioniert am besten bei gutem Licht)")
image = camera_input_live()

# Barcode-Logik
barcode = st.text_input(t_manual, key="barcode_input")

# Wenn ein Bild von der Kamera kommt, könnte man hier theoretisch eine Library wie 'pyzbar' nutzen,
# aber da das auf Servern oft crashed, ist der sauberste Weg für euch:
# Das Handy-Kamera-Input Feld oder die manuelle Eingabe.

if barcode:
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        res = requests.get(url).json()
        if res.get("status") == 1:
            prod = res["product"]
            st.markdown(f"### {prod.get('product_name', 'Unbekannt')}")
            
            # Bild anzeigen
            if prod.get("image_front_url"):
                st.image(prod["image_front_url"], width=200)

            # Check
            data = str(prod.get("ingredients_text", "")).lower() + str(prod.get("allergens_hierarchy", [])).lower()
            found = [a for a in allergies if a.lower() in data]

            if found:
                st.error(f"{t_warn} {', '.join(found)}!")
            else:
                st.success(t_safe)
        else:
            st.warning("Produkt nicht gefunden.")
    except:
        st.error("API Fehler.")

st.markdown("---")
st.caption("NutriScan v2.0 | Team SafeScanning | Data by OpenFoodFacts")
