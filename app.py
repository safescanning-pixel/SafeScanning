import streamlit as st
import requests
import streamlit.components.v1 as components

# ==========================================
# 1. SETUP & ULTRA CLEAN UI DESIGN (Premium)
# ==========================================
st.set_page_config(page_title="AllergyShield Pro", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #111827; font-family: 'SF Pro Display', -apple-system, sans-serif; }
    header {visibility: hidden;}
   
    /* Moderne Tabs im iOS-Stil */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white; padding: 6px; border-radius: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02); gap: 8px; justify-content: center; margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px; border-radius: 18px; color: #6B7280; font-weight: 600; font-size: 14px; padding: 0 20px;
        border: none !important;
    }
    .stTabs [aria-selected="true"] { background-color: #E0E7FF !important; color: #4F46E5 !important; }
   
    /* Cleane White Cards */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important; border-radius: 24px !important;
        border: 1px solid #F3F4F6 !important; box-shadow: 0 4px 20px rgba(0,0,0,0.02) !important; padding: 25px !important;
        margin-bottom: 15px;
    }
   
    /* Typografie */
    h1 { color: #111827 !important; text-align: center; font-weight: 800; font-size: 32px; margin-bottom: 5px;}
    h2 { color: #111827 !important; text-align: center; font-weight: 800; font-size: 26px; margin-bottom: 5px;}
    h3 { color: #111827 !important; text-align: left; font-weight: 700; font-size: 22px; margin-bottom: 10px;}
    h4 { color: #111827 !important; text-align: left; font-weight: 700; font-size: 16px; margin-bottom: 15px !important;}
    p {text-align: center; color: #6B7280; font-size: 15px; margin-bottom: 20px;}
   
    /* Buttons */
    .stButton>button {
        background-color: #4F46E5 !important; color: white !important; border-radius: 20px !important;
        height: 50px !important; width: 100% !important; font-weight: 700 !important; font-size: 15px !important; border: none !important;
        transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important;
    }
    .stButton>button:hover { background-color: #4338CA !important; transform: translateY(-1px); }
   
    /* Ergebnis-Boxen */
    .result-box-safe { background-color: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 20px; padding: 20px; color: #065F46; }
    .result-box-warn { background-color: #FEF2F2; border: 1px solid #FCA5A5; border-radius: 20px; padding: 20px; color: #991B1B; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. KONFETTI-ENGINE
# ==========================================
def throw_confetti():
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            confetti({ particleCount: 180, spread: 90, origin: { y: 0.6 }, colors: ['#4F46E5', '#10B981', '#F59E0B'] });
        </script>
        """, height=0,
    )

# ==========================================
# 3. GLOBAL STATE & SPRACHEN
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = "Deutsch"
if 'cam_on' not in st.session_state: st.session_state.cam_on = False
if 'history' not in st.session_state: st.session_state.history = []
if 'manual_code' not in st.session_state: st.session_state.manual_code = ""
if 'profile' not in st.session_state:
    st.session_state.profile = {
        "laktose": False, "fruktose": False, "histamin": False, "sorbit": False,
        "sulfite": False, "glutamat": False,
        "vegan": False, "vegetarisch": False
    }

ui = {
    "Deutsch": {
        "t1": "👤 Profil", "t2": "📸 Scanner", "t3": "⚙️ Einstellungen", "t4": "ℹ️ Info",
        "title": "Mein Schutzprofil", "sub": "Konfigurieren Sie Ihre Allergien und Unverträglichkeiten", "save": "Profil speichern",
        "cat_allergy": "Intoleranzen", "cat_additives": "Zusatzstoffe", "cat_lifestyle": "Lebensstil & Religion",
        "laktose": "Laktose / Milch", "fruktose": "Fruktose", "histamin": "Histamin", "sorbit": "Sorbit",
        "sulfite": "Sulfite", "glutamat": "Glutamat",
        "vegan": "Vegan", "vegetarisch": "Vegetarisch",
        "scan_h": "Scanner", "scan_p": "Nutzen Sie den Live-Scanner oder geben Sie den Code manuell ein",
        "btn_cam_start": "📸 Live Barcode-Scanner starten", "btn_cam_stop": "🛑 Scanner schließen",
        "safe": "✅ PRODUKT GEEIGNET!", "safe_sub": "Dieses Produkt entspricht vollständig deinem Schutzprofil.",
        "warn": "🛑 NICHT GEEIGNET!", "not_found": "⚠️ Produkt nicht gefunden.",
        "w_laktose": "🥛 Enthält Laktose/Milch", "w_fruktose": "🍎 Enthält Fruktose", "w_histamin": "🍷 Histamin-Risiko erkannt", "w_sorbit": "🍬 Enthält Sorbit (E420)",
        "w_sulfite": "🧪 Enthält Sulfite (Schwefeldioxid)", "w_glutamat": "🍕 Enthält Glutamat (Geschmacksverstärker)",
        "w_vegan": "🥩 Nicht Vegan", "w_vegetarisch": "🥩 Nicht Vegetarisch",
        "placeholder": "Barcode eintragen oder oben scannen", "team_title": "👥 Entwickler-Team Klasse 10a", "details": "🔬 Inhaltsstoffe & Analyse"
    }
}
t = ui["Deutsch"]

# Offline Backup-Daten
OFFLINE_DATA = {
    "3017620425035": {"product_name": "Nutella", "ingredients_text": "Zucker, Palmöl, Haselnüsse (13%), Magermilchpulver (8,7%), fettarmer Kakao, Emulgator Lecithine (Soja), Vanillin.", "image_front_url": "https://world.openfoodfacts.org/images/products/301/762/042/5035/front_fr.465.400.jpg"},
    "5449000000996": {"product_name": "Coca Cola Classic", "ingredients_text": "Wasser, Zucker, Kohlensäure, Farbstoff E 150d, Säuerungsmittel Phosphorsäure, natürliches Aroma, Aroma Koffein.", "image_front_url": "https://world.openfoodfacts.org/images/products/544/900/000/0996/front_de.643.400.jpg"}
}

tab_profil, tab_scanner, tab_settings, tab_info = st.tabs([t["t1"], t["t2"], t["t3"], t["t4"]])

# --- TAB 1: MEIN SCHUTZPROFIL ---
with tab_profil:
    st.markdown(f"<h1>🛡️<br>{t['title']}</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h4>⚙️ {t['cat_allergy']}</h4>", unsafe_allow_html=True)
        st.session_state.profile["laktose"] = st.toggle(t["laktose"], value=st.session_state.profile["laktose"])
        st.session_state.profile["fruktose"] = st.toggle(t["fruktose"], value=st.session_state.profile["fruktose"])
        st.session_state.profile["histamin"] = st.toggle(t["histamin"], value=st.session_state.profile["histamin"])
        st.session_state.profile["sorbit"] = st.toggle(t["sorbit"], value=st.session_state.profile["sorbit"])
    with st.container(border=True):
        st.markdown(f"<h4>🧪 {t['cat_additives']}</h4>", unsafe_allow_html=True)
        st.session_state.profile["sulfite"] = st.toggle(t["sulfite"], value=st.session_state.profile["sulfite"])
        st.session_state.profile["glutamat"] = st.toggle(t["glutamat"], value=st.session_state.profile["glutamat"])
    with st.container(border=True):
        st.markdown(f"<h4>🌱 {t['cat_lifestyle']}</h4>", unsafe_allow_html=True)
        st.session_state.profile["vegan"] = st.toggle(t["vegan"], value=st.session_state.profile["vegan"])
        st.session_state.profile["vegetarisch"] = st.toggle(t["vegetarisch"], value=st.session_state.profile["vegetarisch"])

# --- TAB 2: SCANNER (RÜCKKAMERA & AUTO-SCAN) ---
with tab_scanner:
    st.markdown(f"<h2>{t['scan_h']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['scan_p']}</p>", unsafe_allow_html=True)
   
    if not st.session_state.cam_on:
        if st.button(t["btn_cam_start"]):
            st.session_state.cam_on = True
            st.session_state.manual_code = ""
            st.rerun()
    else:
        if st.button(t["btn_cam_stop"]):
            st.session_state.cam_on = False
            st.rerun()
           
        with st.container(border=True):
            # Der HTML5/JavaScript Live-Scanner
            scan_component = components.html(
                """
                <div id="interactive" style="width:100%; max-width:400px; margin:0 auto; border-radius:12px; overflow:hidden;"></div>
                <script src="https://unpkg.com/html5-qrcode"></script>
                <script>
                    function onScanSuccess(decodedText, decodedResult) {
                        // Sendet das Ergebnis direkt an Streamlit zurück
                        Streamlit.setComponentValue(decodedText);
                    }
                   
                    // Initialisiert den Streamlit-Komponenten-Handshake
                    if (!window.Streamlit) {
                        window.addEventListener("message", function(e) {
                            if (e.data.type === "streamlit:render") { startScanner(); }
                        });
                    } else { startScanner(); }

                    function startScanner() {
                        const html5QrCode = new Html5Qrcode("interactive");
                        const config = { fps: 15, qrbox: { width: 280, height: 160 } };
                        // facingMode: "environment" erzwingt die Rückkamera
                        html5QrCode.start({ facingMode: "environment" }, config, onScanSuccess)
                        .catch(err => console.log(err));
                    }
                </script>
                """, height=300
            )
           
            if scan_component:
                st.session_state.manual_code = str(scan_component)
                st.session_state.cam_on = False
                st.rerun()

    barcode_input = st.text_input("Barcode", value=st.session_state.manual_code, placeholder=t["placeholder"])

    if barcode_input:
        barcode = "".join(filter(str.isdigit, barcode_input))
        if len(barcode) >= 8:
            with st.spinner("🔍 Analyse..."):
                product = None
                is_offline = False
               
                try:
                    headers = {'User-Agent': 'AllergyShieldPro/5.0 (School Project)'}
                    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
                    response = requests.get(url, headers=headers, timeout=5)
                    if response.status_code == 200 and response.json().get("status") == 1:
                        product = response.json()["product"]
                except:
                    pass
               
                if not product and barcode in OFFLINE_DATA:
                    product = OFFLINE_DATA[barcode]
                    is_offline = True
               
                if product:
                    p_name = product.get('product_name', 'Unbekanntes Produkt')
                    all_text = (str(product.get("ingredients_text", "")) + " " + str(product.get("allergens_hierarchy", ""))).lower()
                    warnings = []
                    p = st.session_state.profile
                   
                    if p["laktose"] and any(w in all_text for w in ["milch", "milk", "lactose", "laktose", "molke", "sahne", "butter"]): warnings.append(t["w_laktose"])
                    if p["fruktose"] and any(w in all_text for w in ["fructose", "fruktose", "fruchtzucker", "sirup"]): warnings.append(t["w_fruktose"])
                    if p["histamin"] and any(w in all_text for w in ["histamin", "hefe", "yeast", "wein", "tomate", "schokolade"]): warnings.append(t["w_histamin"])
                    if p["sorbit"] and any(w in all_text for w in ["sorbit", "sorbitol", "e420"]): warnings.append(t["w_sorbit"])
                    if p["sulfite"] and any(w in all_text for w in ["sulfit", "sulfite", "schwefeldioxid", "e220"]): warnings.append(t["w_sulfite"])
                    if p["glutamat"] and any(w in all_text for w in ["glutamat", "glutamate", "hefeextrakt", "e621"]): warnings.append(t["w_glutamat"])
                    if p["vegan"] and any(w in all_text for w in ["milch", "milk", "ei ", "egg", "fleisch", "meat", "honig", "gelatine"]): warnings.append(t["w_vegan"])
                    if p["vegetarisch"] and any(w in all_text for w in ["fleisch", "meat", "fisch", "fish", "gelatine"]): warnings.append(t["w_vegetarisch"])
                       
                    st.write("")
                    col1, col2 = st.columns([1.3, 1], gap="medium")
                    with col1:
                        st.markdown(f"<h3>{p_name}</h3>", unsafe_allow_html=True)
                        if warnings:
                            st.markdown(f'<div class="result-box-warn"><h3 style="color:#991B1B;margin:0;">{t["warn"]}</h3><p style="text-align:left;color:#991B1B;margin-top:10px;">{"<br>".join(["• " + w for w in warnings])}</p></div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="result-box-safe"><h3 style="color:#065F46;margin:0;">{t["safe"]}</h3><p style="text-align:left;color:#065F46;margin-top:10px;">{t["safe_sub"]}</p></div>', unsafe_allow_html=True)
                            throw_confetti()
                    with col2:
                        if product.get("image_front_url"):
                            st.image(product["image_front_url"], use_container_width=True)
                else:
                    st.error(t["not_found"])

# --- TAB 3 & 4: SETTINGS & INFO ---
with tab_settings:
    st.write("Spracheinstellung: Deutsch")
with tab_info:
    st.markdown(f"<h2>{t['team_title']}</h2>", unsafe_allow_html=True)
    st.caption("Hanns-Seidel-Gymnasium Aschaffenburg | Klasse 10a")
