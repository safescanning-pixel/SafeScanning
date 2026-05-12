import streamlit as st
import requests
from camera_input_live import camera_input_live
from PIL import Image
import io

# 1. Seite konfigurieren
st.set_page_config(page_title="NutriScan Pro", page_icon="🔍", layout="centered")

# Design-Optimierung (CSS)
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
st.sidebar.write("• Maximilian Maier")
st.sidebar.write("• Benjamin Mehling")
st.sidebar.write("• Ben Henkel")
st.sidebar.write("• Marius Boulos")
st.sidebar.write("• Sophie Hartwig")

# 3. Hauptbereich & Sprache
st.title("🍏 NutriScan")
lang = st.radio("Sprache / Language", ["Deutsch", "English"], horizontal=True)

if lang == "Deutsch":
    t_profile = "Dein Allergie-Profil"
    t_select = "Wähle deine Allergien:"
    t_scan = "Barcode Live-Scanner"
    t_manual = "Barcode manuell eingeben:"
    t_safe = "✅ Sicher für dich!"
    t_warn = "❌ WARNUNG: Enthält"
    t_not_found = "Produkt nicht gefunden."
    t_input_info = "Bitte eine gültige Nummer eingeben."
else:
    t_profile = "Your Profile"
    t_select = "Select your allergies:"
    t_scan = "Live Barcode Scanner"
    t_manual = "Enter barcode manually:"
    t_safe = "✅ Safe for you!"
    t_warn = "❌ WARNING: Contains"
    t_not_found = "Product not found."
    t_input_info = "Please enter a valid barcode number."

with st.expander(t_profile, expanded=True):
    allergies = st.multiselect(t_select, ["Gluten", "Lactose", "Fructose", "Nüsse", "Erdnüsse", "Soja", "Eier", "Fisch"])

# 4. Live-Kamera-Vorschau (Optisches Feature für die Präsentation)
st.subheader(t_scan)
st.info("Kamera-Vorschau aktiv. Tippe den Barcode unten ein:")
camera_input_live()

# 5. Barcode Eingabe
barcode = st.text_input(t_manual, value="", key="barcode_input")

# 6. Datenbank-Abfrage & Logik
if barcode and len(barcode) > 5:
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            res = response.json()
            if res.get("status") == 1:
                prod = res["product"]
                st.markdown(f"### {prod.get('product_name', 'Unbekanntes Produkt')}")
                
                if prod.get("image_front_url"):
                    st.image(prod["image_front_url"], width=200)

                # Inhaltsstoffe und Allergene prüfen
                data = str(prod.get("ingredients_text", "")).lower() + str(prod.get("allergens_hierarchy", [])).lower()
                found = [a for a in allergies if a.lower() in data]

                if found:
                    st.error(f"{t_warn} {', '.join(found)}!")
                else:
                    st.success(t_safe)
            else:
                st.warning(t_not_found)
        else:
            st.error("Datenbank-Verbindung fehlgeschlagen.")
    except:
        st.error("Netzwerk-Fehler.")
else:
    if barcode:
        st.info(t_input_info)

st.markdown("---")
st.caption("NutriScan v2.0 | Team SafeScanning | Data by OpenFoodFacts")
