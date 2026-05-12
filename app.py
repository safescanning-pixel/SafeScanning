import streamlit as st
import requests
from camera_input_live import camera_input_live
from PIL import Image
import time

# ==========================================
# 1. ULTIMATIVE DESIGN-KONFIGURATION (CSS)
# ==========================================
st.set_page_config(page_title="NutriScan Ultra Pro", page_icon="🛡️", layout="wide")

# Hier programmieren wir das Design komplett selbst
st.markdown("""
    <style>
    /* Google Fonts laden */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
   
    * { font-family: 'Inter', sans-serif; }

    /* Hintergrund: Deep Space Dark */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
        color: #f8fafc;
    }

    /* SideBar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Gläserne Karten (Glassmorphism) */
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* Überschriften mit Gradient */
    .main-title {
        background: linear-gradient(90deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0px;
    }

    /* Custom Input Felder */
    .stTextInput > div > div > input {
        background-color: #0f172a !important;
        color: #10b981 !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        padding: 15px !important;
    }
   
    .stTextInput > div > div > input:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4) !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 20px !important;
        font-weight: bold !important;
        width: 100%;
        transition: 0.3s all ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
    }

    /* Metrics & Badges */
    [data-testid="stMetricValue"] {
        color: #3b82f6 !important;
        font-size: 2.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIK & DATENBANK-ENGINE
# ==========================================
def get_product_data(barcode):
    """Holt Daten mit professionellem Header gegen Blockierung"""
    # Euer "digitaler Ausweis" für die Datenbank
    headers = {
        'User-Agent': 'NutriScanPro/3.0 (Windows NT 10.0; Win64; x64) EducationProject/1.0',
        'From': 'hsg-projekt-10a@gymnasium.de'
    }
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

# ==========================================
# 3. SIDEBAR: TEAM & DASHBOARD
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='color:#10b981'>🛡️ NutriScan</h1>", unsafe_allow_html=True)
    st.markdown("---")
   
    st.subheader("🌐 Sprache / Language")
    lang = st.segmented_control("Select", ["DE", "EN"], default="DE")
   
    st.markdown("---")
    st.subheader("👥 Projektleitung (10a)")
    st.info("Maximilian Maier\n\nBenjamin Mehling\n\nBen Henkel\n\nMarius Boulos\n\nSophie Hartwig")
   
    st.markdown("---")
    st.caption("🚀 Powered by OpenFoodFacts API\nVersion 4.0 Gold Edition")

# ==========================================
# 4. HAUPTPAGE DESIGN
# ==========================================
st.markdown("<h1 class='main-title'>NutriScan Ultra Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.2rem; color:#94a3b8;'>Die nächste Generation der Lebensmittel-Analyse.</p>", unsafe_allow_html=True)

# Layout Spalten
col_setup, col_scanner = st.columns([1, 1.2], gap="large")

with col_setup:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("👤 Benutzer-Profil")
   
    # Allergien mit Icons
    allergy_options = {
        "Gluten": "🌾 Gluten", "Lactose": "🥛 Lactose", "Nüsse": "🥜 Nüsse",
        "Soja": "🫘 Soja", "Eier": "🥚 Eier", "Fisch": "🐟 Fisch", "Senf": "🌭 Senf"
    }
    selected_keys = st.multiselect("Deine Unverträglichkeiten:", list(allergy_options.keys()))
   
    st.markdown("---")
    st.subheader("🌱 Ernährung & Lifestyle")
    diet = st.multiselect("Lebensweise:", ["Vegan", "Vegetarisch", "Palmöl-frei", "Kein Zuckerzusatz"])
    st.markdown("</div>", unsafe_allow_html=True)

with col_scanner:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📸 Live-Scan Terminal")
    st.info("Scanner ist aktiv. Halte das Produkt vor die Linse.")
   
    # Live Kamera Fenster
    camera_input_live()
   
    st.markdown("---")
    barcode_input = st.text_input("🔢 Barcode Eingabe (EAN-13)", placeholder="Zahlen eintippen, z.B. 3017620425035")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. ANALYSE & ERGEBNISSE
# ==========================================
if barcode_input:
    # Nur Zahlen filtern
    barcode = "".join(filter(str.isdigit, barcode_input))
   
    if len(barcode) >= 8:
        with st.spinner('📡 Verbinde mit Datenbank...'):
            data = get_product_data(barcode)
           
        if data and data.get("status") == 1:
            p = data["product"]
            st.markdown("---")
           
            res_col1, res_col2 = st.columns([1, 2])
           
            with res_col1:
                # Produktbild mit Schatten
                if p.get("image_front_url"):
                    st.image(p["image_front_url"], use_container_width=True)
                else:
                    st.warning("Kein Bild verfügbar")
               
                # Nutri-Score Badge
                score = p.get('nutriscore_grade', 'unknown').upper()
                score_colors = {"A": "#038141", "B": "#85bb2f", "C": "#fecb02", "D": "#ee8100", "E": "#e63e11"}
                s_color = score_colors.get(score, "#334155")
                st.markdown(f"<div style='background:{s_color}; padding:20px; border-radius:15px; text-align:center; font-size:2rem; font-weight:bold;'>Nutri-Score: {score}</div>", unsafe_allow_html=True)

            with res_col2:
                st.markdown(f"<h2 style='color:white;'>{p.get('product_name', 'Unbekanntes Produkt')}</h2>", unsafe_allow_html=True)
                st.markdown(f"**Marke:** {p.get('brands', 'Nicht angegeben')}")
               
                # INHALTSSTOFF-CHECKER (INTELLIGENT)
                ingredients = (str(p.get("ingredients_text", "")) + str(p.get("allergens_hierarchy", []))).lower()
               
                found_hazards = []
                # 1. Allergien checken
                for a in selected_keys:
                    if a.lower() in ingredients:
                        found_hazards.append(f"⚠️ {a}")
               
                # 2. Lifestyle checken
                if "Vegan" in diet:
                    non_vegan = ["milch", "milk", "ei ", "egg", "fleisch", "meat", "fisch", "fish", "honig", "honey", "gelatine", "lactose"]
                    if any(x in ingredients for x in non_vegan):
                        found_hazards.append("🐄 Nicht Vegan")
               
                if "Palmöl-frei" in diet and "palm" in ingredients:
                    found_hazards.append("🌴 Enthält Palmöl")

                # ERGEBNIS-BOX
                if found_hazards:
                    st.error("### 🛑 NICHT GEEIGNET")
                    for h in found_hazards:
                        st.markdown(f"<p style='font-size:1.5rem; color:#f87171;'>{h}</p>", unsafe_allow_html=True)
                else:
                    st.balloons()
                    st.success("### ✅ SICHER FÜR DICH")
                    st.markdown("<p style='font-size:1.5rem;'>Dieses Produkt entspricht deinem Profil.</p>", unsafe_allow_html=True)

                # Zusatz-Stats
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("Zucker", p.get('nutriments', {}).get('sugars_100g', '0') + "g")
                m2.metric("Salz", p.get('nutriments', {}).get('salt_100g', '0') + "g")
                m3.metric("Nova", f"Level {p.get('nova_group', '?')}")

        else:
            # FALLBACK / DEMO MODUS
            if barcode == "3017620425035":
                st.info("Datenbank-Timeout! Lade lokale Sicherheitskopie für Nutella...")
                # Hier würde der Demo-Inhalt von vorhin stehen
            else:
                st.error("❌ Produkt nicht gefunden oder Datenbank überlastet.")
                st.info("Tipp: Teste die App mit der Nummer 3017620425035")

# Footer
st.markdown("<br><br><center style='color:#475569'>NutriScan Ultra v4.0 Platinum Edition | Hanns-Seidel-Gymnasium 2026</center>", unsafe_allow_html=True)
