import streamlit as st
import requests
from camera_input_live import camera_input_live
from PIL import Image

# ==========================================
# 1. PAGE CONFIG & PREMIUM DARK THEME
# ==========================================
st.set_page_config(
    page_title="NutriScan Ultra Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für High-End Design
st.markdown("""
    <style>
    /* Globales Dark Theme */
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
   
    /* Glas-Effekt für Karten */
    div[data-testid="stExpander"], .stSelectbox, .stMultiSelect, .stTextInput > div > div > input {
        background-color: #1A1F26 !important;
        border: 1px solid #2D333B !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Neon-Grüne Akzente */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#2ECC71, #27AE60);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Premium Button */
    .stButton>button {
        background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0D1117 !important;
        border-right: 1px solid #30363D;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SPRACH-ENGINE
# ==========================================
lang = st.sidebar.segmented_control("Sprache / Language", ["Deutsch", "English"], default="Deutsch")

if lang == "Deutsch":
    L = {
        "tagline": "KI-gestützte Lebensmittel-Analyse",
        "profile_hdr": "🛠️ Benutzer-Konfiguration",
        "allergy_lab": "Allergien auswählen",
        "diet_lab": "Ernährungsweise",
        "scan_hdr": "📸 Echtzeit-Scanner",
        "manual_lab": "Barcode manuell",
        "status_safe": "PRODUKT KONFORM",
        "status_warn": "GEFAHR GEFUNDEN",
        "nutri": "Ernährungswerte",
        "nova": "Verarbeitungsgrad",
        "palm": "Palmöl-Check"
    }
else:
    L = {
        "tagline": "AI-Powered Food Analysis",
        "profile_hdr": "🛠️ User Configuration",
        "allergy_lab": "Select Allergies",
        "diet_lab": "Dietary Preference",
        "scan_hdr": "📸 Real-time Scanner",
        "manual_lab": "Manual Barcode",
        "status_safe": "PRODUCT SAFE",
        "status_warn": "CRITICAL INGREDIENTS",
        "nutri": "Nutrition Facts",
        "nova": "Processing Level",
        "palm": "Palm Oil Check"
    }

# ==========================================
# 3. SIDEBAR (TEAM & STATS)
# ==========================================
st.sidebar.markdown("# 🚀 NutriScan Pro")
st.sidebar.markdown(f"*{L['tagline']}*")
st.sidebar.markdown("---")
st.sidebar.subheader("👥 Projekt-Team 10a")
for name in ["Maximilian Maier", "Benjamin Mehling", "Ben Henkel", "Marius Boulos", "Sophie Hartwig"]:
    st.sidebar.markdown(f"**{name}**")
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Hanns-Seidel-Gymnasium")

# ==========================================
# 4. DASHBOARD: PROFIL
# ==========================================
st.title("🍏 NutriScan Pro v3.5")

col_a, col_b = st.columns([1, 1])

with col_a:
    with st.container():
        st.markdown(f"### {L['profile_hdr']}")
        user_allergies = st.multiselect(L['allergy_lab'],
            ["Gluten", "Lactose", "Fructose", "Nüsse", "Erdnüsse", "Soja", "Eier", "Fisch", "Sellerie", "Senf"])

with col_b:
    with st.container():
        st.markdown("### 🌱 Lifestyle")
        user_diet = st.multiselect(L['diet_lab'],
            ["Vegan", "Vegetarisch", "Palmöl-frei", "Kein Zuckerzusatz"])

# ==========================================
# 5. SCANNER AREA
# ==========================================
st.markdown("---")
col_scan, col_res = st.columns([1, 1.2])

with col_scan:
    st.markdown(f"### {L['scan_hdr']}")
    camera_input_live()
    barcode = st.text_input(L['manual_lab'], placeholder="3017620425035...")

# ==========================================
# 6. ANALYSE-ENGINE
# ==========================================
with col_res:
    if barcode:
        clean_bc = "".join(filter(str.isdigit, barcode))
        if len(clean_bc) > 7:
            url = f"https://world.openfoodfacts.org/api/v2/product/{clean_bc}.json"
            try:
                res = requests.get(url, timeout=8)
                data = res.json()
               
                if data.get("status") == 1:
                    p = data["product"]
                    st.markdown(f"## {p.get('product_name', 'Unbekannt')}")
                   
                    if p.get("image_front_url"):
                        st.image(p["image_front_url"], width=280)
                   
                    # Logik-Prüfung
                    content = (str(p.get("ingredients_text", "")) +
                               str(p.get("allergens_hierarchy", []))).lower()
                   
                    forbidden = [a.lower() for a in user_allergies]
                    if "Vegan" in user_diet: forbidden += ["milch", "milk", "ei", "egg", "fleisch", "meat", "honig", "honey", "gelatine"]
                    if "Vegetarisch" in user_diet: forbidden += ["fleisch", "meat", "fisch", "fish"]
                    if "Palmöl-frei" in user_diet: forbidden += ["palm"]

                    found = [f.capitalize() for f in forbidden if f in content and f != ""]
                    found = list(set(found))

                    # Anzeige Ergebnis
                    if found:
                        st.error(f"### {L['status_warn']}\n**{', '.join(found)}**")
                    else:
                        st.success(f"### {L['status_safe']}")
                   
                    # Zusatz-Infos (Nutri-Score)
                    st.markdown("---")
                    c1, c2 = st.columns(2)
                    with c1:
                        score = p.get('nutriscore_grade', 'n.a.').upper()
                        st.metric("Nutri-Score", score)
                    with c2:
                        nova = p.get('nova_group', '?')
                        st.metric(L['nova'], f"Gruppe {nova}")
                else:
                    st.warning("⚠️ Produkt nicht gefunden.")
            except:
                st.error("📡 Netzwerk-Fehler. Im Schul-WLAN blockiert?")
                # DEMO FÜR NUTELLA
                if clean_bc == "3017620425035":
                    st.info("Demo-Modus: Nutella geladen")
                    st.image("https://images.openfoodfacts.org/images/products/301/762/042/5035/front_de.676.400.jpg", width=250)
                    if any(x in ["Nüsse", "Gluten", "Lactose"] for x in user_allergies) or "Vegan" in user_diet:
                        st.error(f"{L['status_warn']}: Haselnüsse, Milch")
                    else: st.success(L['status_safe'])
