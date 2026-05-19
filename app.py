import streamlit as st
import requests
import streamlit.components.v1 as components
from camera_input_live import camera_input_live

# ==========================================
# 1. SETUP & CLEAN UI DESIGN
# ==========================================
st.set_page_config(page_title="AllergyShield Pro", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    /* Absolut minimalistisches App-Design */
    .stApp { background-color: #F8F9FA; color: #111827; font-family: 'SF Pro Display', -apple-system, sans-serif; }
    header {visibility: hidden;}
   
    /* Moderne Tabs im iOS-Stil */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white; padding: 5px; border-radius: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03); gap: 5px; justify-content: center; margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px; border-radius: 15px; color: #6B7280; font-weight: 600; font-size: 14px; padding: 0 15px;
    }
    .stTabs [aria-selected="true"] { background-color: #E0E7FF !important; color: #4F46E5 !important; }
   
    /* Cleane Karten (Cards) ohne dicke Rahmen */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important; border-radius: 24px !important;
        border: 1px solid #F3F4F6 !important; box-shadow: 0 4px 20px rgba(0,0,0,0.02) !important; padding: 25px !important;
    }
   
    /* Toggles und Texte */
    h1, h2, h3, h4 { color: #111827 !important; text-align: center; font-weight: 800; margin-bottom: 5px;}
    p {text-align: center; color: #6B7280; margin-bottom: 20px;}
   
    /* Button Styling */
    .stButton>button {
        background-color: #4F46E5 !important; color: white !important; border-radius: 18px !important;
        height: 55px !important; width: 100% !important; font-weight: bold !important; border: none !important;
        transition: 0.2s;
    }
    .stButton>button:hover { background-color: #4338CA !important; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. KONFETTI-FUNKTION (Custom JS)
# ==========================================
def throw_confetti():
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 }, colors: ['#4F46E5', '#10B981', '#F59E0B'] });
        </script>
        """,
        height=0,
    )

# ==========================================
# 3. SPEICHER & SPRACH-ENGINE
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = "Deutsch"
if 'profile' not in st.session_state:
    st.session_state.profile = {
        "laktose": False, "fruktose": False, "gluten": False, "nuesse": False, "soja": False,
        "vegan": False, "vegetarisch": False, "halal": False, "koscher": False
    }

# Wörterbuch für die Oberfläche
ui = {
    "Deutsch": {"t1": "👤 Profil", "t2": "📸 Scanner", "t3": "⚙️ Einstellungen", "title": "Mein Schutzprofil", "sub": "Allergien & Lebensstil", "save": "Profil speichern", "scan_h": "Scanner", "scan_p": "Barcode scannen oder eingeben", "safe": "✅ PRODUKT SICHER!", "warn": "🛑 WARNUNG:"},
    "English": {"t1": "👤 Profile", "t2": "📸 Scanner", "t3": "⚙️ Settings", "title": "My Protection Profile", "sub": "Allergies & Lifestyle", "save": "Save Profile", "scan_h": "Scanner", "scan_p": "Scan or enter barcode", "safe": "✅ PRODUCT SAFE!", "warn": "🛑 WARNING:"},
    "Türkçe": {"t1": "👤 Profil", "t2": "📸 Tarayıcı", "t3": "⚙️ Ayarlar", "title": "Koruma Profilim", "sub": "Alerjiler ve Yaşam Tarzı", "save": "Profili Kaydet", "scan_h": "Tarayıcı", "scan_p": "Barkodu okut veya gir", "safe": "✅ ÜRÜN GÜVENLİ!", "warn": "🛑 UYARI:"},
    "العربية": {"t1": "👤 ملفي", "t2": "📸 ماسح", "t3": "⚙️ إعدادات", "title": "ملف الحماية الخاص بي", "sub": "الحساسية ونمط الحياة", "save": "حفظ الملف", "scan_h": "الماسح الضوئي", "scan_p": "امسح أو أدخل الباركود", "safe": "✅ منتج آمن!", "warn": "🛑 تحذير:"},
    "Español": {"t1": "👤 Perfil", "t2": "📸 Escáner", "t3": "⚙️ Ajustes", "title": "Mi Perfil de Protección", "sub": "Alergias y Estilo de Vida", "save": "Guardar Perfil", "scan_h": "Escáner", "scan_p": "Escanear o ingresar código", "safe": "✅ ¡PRODUCTO SEGURO!", "warn": "🛑 ADVERTENCIA:"}
}
t = ui[st.session_state.lang]

# ==========================================
# 4. NAVIGATION
# ==========================================
tab_profil, tab_scanner, tab_settings, tab_info = st.tabs([t["t1"], t["t2"], t["t3"], "ℹ️ Info"])

# --- TAB 1: PROFIL ---
with tab_profil:
    st.markdown(f"<h1>🛡️<br>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['sub']}</p>", unsafe_allow_html=True)
   
    with st.container(border=True):
        st.markdown("<h4>⚕️ Allergien & Intoleranzen</h4>", unsafe_allow_html=True)
        st.session_state.profile["laktose"] = st.toggle("🥛 Laktose / Milch", value=st.session_state.profile["laktose"])
        st.session_state.profile["fruktose"] = st.toggle("🍎 Fruktose", value=st.session_state.profile["fruktose"])
        st.session_state.profile["gluten"] = st.toggle("🌾 Glutenfrei", value=st.session_state.profile["gluten"])
        st.session_state.profile["nuesse"] = st.toggle("🥜 Nüsse / Erdnüsse", value=st.session_state.profile["nuesse"])
        st.session_state.profile["soja"] = st.toggle("🫘 Soja", value=st.session_state.profile["soja"])
       
    with st.container(border=True):
        st.markdown("<h4>🌱 Lebensstil & Religion</h4>", unsafe_allow_html=True)
        st.session_state.profile["vegan"] = st.toggle("🌿 Vegan", value=st.session_state.profile["vegan"])
        st.session_state.profile["vegetarisch"] = st.toggle("🧀 Vegetarisch", value=st.session_state.profile["vegetarisch"])
        st.session_state.profile["halal"] = st.toggle("☪️ Halal (حلال)", value=st.session_state.profile["halal"])
        st.session_state.profile["koscher"] = st.toggle("✡️ Koscher (כָּשֵׁר)", value=st.session_state.profile["koscher"])

    if st.button(f"💾 {t['save']}"):
        st.success("✅ Gespeichert!")

# --- TAB 2: SCANNER & LOGIK ---
with tab_scanner:
    st.markdown(f"<h2>{t['scan_h']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['scan_p']}</p>", unsafe_allow_html=True)
   
    with st.container(border=True):
        camera_input_live()

    barcode_input = st.text_input("📝", placeholder="3017620425035", label_visibility="collapsed")

    if barcode_input:
        barcode = "".join(filter(str.isdigit, barcode_input))
       
        if len(barcode) >= 8:
            with st.spinner("🔄 ..."):
                headers = {'User-Agent': 'AllergyShieldPro/3.0'}
                url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
               
                try:
                    response = requests.get(url, headers=headers, timeout=8)
                   
                    if response.status_code == 200 and response.json().get("status") == 1:
                        data = response.json()
                        product = data["product"]
                       
                        with st.container(border=True):
                            st.markdown(f"<h3>{product.get('product_name', 'Unbekannt')}</h3>", unsafe_allow_html=True)
                            if product.get("image_front_url"):
                                st.image(product["image_front_url"], width=200)
                           
                            all_text = (str(product.get("ingredients_text", "")) + str(product.get("allergens_hierarchy", ""))).lower()
                            warnings = []
                            p = st.session_state.profile
                           
                            # Die Analyse-Datenbank
                            if p["laktose"] and any(w in all_text for w in ["milch", "milk", "lait", "lactose", "laktose", "molke", "sahne"]):
                                warnings.append("🥛 Enthält Laktose/Milch")
                            if p["fruktose"] and any(w in all_text for w in ["fructose", "fruktose", "fruchtzucker", "sirup"]):
                                warnings.append("🍎 Enthält Fruktose")
                            if p["gluten"] and any(w in all_text for w in ["weizen", "wheat", "roggen", "gerste", "dinkel", "hafer", "gluten"]):
                                warnings.append("🌾 Enthält Gluten")
                            if p["nuesse"] and any(w in all_text for w in ["nuss", "nut", "erdnuss", "peanut", "haselnuss", "mandel", "walnuss"]):
                                warnings.append("🥜 Enthält Nüsse")
                            if p["soja"] and any(w in all_text for w in ["soja", "soy"]):
                                warnings.append("🫘 Enthält Soja")
                               
                            if p["vegan"] and any(w in all_text for w in ["milch", "ei ", "egg", "fleisch", "meat", "honig", "gelatine", "huhn", "rind", "schwein"]):
                                warnings.append("🥩 Nicht Vegan")
                            if p["vegetarisch"] and any(w in all_text for w in ["fleisch", "meat", "fisch", "gelatine", "huhn", "rind", "schwein", "karmin"]):
                                warnings.append("🥩 Nicht Vegetarisch")
                           
                            # Religiöse Profile
                            if p["halal"] and any(w in all_text for w in ["schwein", "pork", "porc", "alkohol", "alcohol", "wein", "wine", "gelatine", "e120", "karmin", "carmine"]):
                                warnings.append("☪️ Nicht Halal-Konform")
                            if p["koscher"] and any(w in all_text for w in ["schwein", "pork", "krustentier", "shellfish", "gelatine", "karmin"]):
                                warnings.append("✡️ Nicht Koscher-Konform")
                               
                            if warnings:
                                st.error(f"### {t['warn']}")
                                for w in warnings: st.markdown(f"- **{w}**")
                            else:
                                st.success(f"### {t['safe']}")
                                throw_confetti() # Löst das Konfetti aus!
                    else:
                        st.warning("⚠️ Produkt nicht gefunden.")
                except Exception as e:
                    st.error("📡 Keine Verbindung.")

# --- TAB 3: EINSTELLUNGEN ---
with tab_settings:
    st.markdown(f"<h2>{t['t3']}</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h4>🌐 Sprache / Language</h4>", unsafe_allow_html=True)
        # Dropdown für Sprachen
        new_lang = st.selectbox("Wähle deine Sprache:", ["Deutsch", "English", "Türkçe", "العربية", "Español"], index=["Deutsch", "English", "Türkçe", "العربية", "Español"].index(st.session_state.lang))
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun() # Lädt die App sofort neu, um die Sprache zu ändern

# --- TAB 4: INFO ---
with tab_info:
    with st.container(border=True):
        st.markdown("<h2>👥 Team 10a</h2>", unsafe_allow_html=True)
        st.write("Maximilian Maier, Benjamin Mehling, Ben Henkel, Marius Boulos, Sophie Hartwig")
        st.caption("Hanns-Seidel-Gymnasium | Data by OpenFoodFacts")


