import streamlit as st
import requests
import streamlit.components.v1 as components
from PIL import Image
from pyzbar.pyzbar import decode

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
    
    /* Ergebnis-Boxen mit Gaming Level-Pass / Fail Glow-Effekt */
    .result-box-safe { 
        background-color: #ECFDF5; border: 4px solid #10B981; border-radius: 20px; padding: 20px; color: #065F46; 
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.6); animation: passGlow 1.5s infinite alternate;
    }
    .result-box-warn { 
        background-color: #FEF2F2; border: 4px solid #EF4444; border-radius: 20px; padding: 20px; color: #991B1B; 
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.6); animation: failGlow 1.5s infinite alternate;
    }
    
    @keyframes passGlow {
        0% { box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
        100% { box-shadow: 0 0 30px rgba(16, 185, 129, 0.9); }
    }
    @keyframes failGlow {
        0% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }
        100% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.9); }
    }
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
        "gluten": False, "nuesse": False, "soja": False, "erdnuesse": False,
        "vegan": False, "vegetarisch": False, "halal": False, "koscher": False
    }

ui = {
    "Deutsch": {
        "t1": "👤 Profil", "t2": "📸 Scanner", "t3": "⚙️ Einstellungen", "t4": "ℹ️ Info",
        "title": "Mein Schutzprofil", "sub": "Konfigurieren Sie Ihre Allergien und Unverträglichkeiten", "save": "Profil speichern",
        "cat_allergy": "Intoleranzen & Allergien", "cat_additives": "Zusatzstoffe", "cat_lifestyle": "Lebensstil & Religion",
        "laktose": "Laktose / Milch", "fruktose": "Fruktose", "histamin": "Histamin", "sorbit": "Sorbit",
        "gluten": "Gluten / Zöliakie", "nuesse": "Schalenfrüchte / Nüsse", "soja": "Soja", "erdnuesse": "Erdnüsse",
        "sulfite": "Sulfite", "glutamat": "Glutamat", "vegan": "Vegan", "vegetarisch": "Vegetarisch", "halal": "Halal (حلال)", "koscher": "Koscher (כָּشֵׁر)",
        "scan_h": "Scanner", "scan_p": "Nutzen Sie die Kamera oder geben Sie den Code manuell ein",
        "btn_cam_start": "📸 Scanner starten", "btn_cam_stop": "🛑 Scanner stoppen",
        "safe": "✅ PRODUKT GEEIGNET!", "safe_sub": "Dieses Produkt entspricht vollständig deinem Schutzprofil.",
        "warn": "🛑 NICHT GEEIGNET!", "not_found": "⚠️ Produkt nicht gefunden.", "no_conn": "📡 Keine Verbindung zur Datenbank.",
        "lang_select": "Wähle deine Sprache:", "saved_msg": "✅ Profil erfolgreich gespeichert!", "team_title": "👥 Entwickler-Team Klasse 10a",
        "w_laktose": "🥛 Enthält Laktose/Milch", "w_fruktose": "🍎 Enthält Fruktose", "w_histamin": "🍷 Histamin-Risiko erkannt", "w_sorbit": "🍬 Enthält Sorbit (E420)",
        "w_sulfite": "🧪 Enthält Sulfite (Schwefeldioxid)", "w_glutamat": "🍕 Enthält Glutamat", "w_gluten": "🌾 Enthält Gluten", "w_nuesse": "🌰 Enthält Schalenfrüchte/Nüsse", "w_soja": "🌱 Enthält Soja", "w_erdnuesse": "🥜 Enthält Erdnüsse",
        "w_vegan": "🥩 Nicht Vegan", "w_vegetarisch": "🥩 Nicht Vegetarisch", "w_halal": "☪️ Nicht Halal-Konform", "w_koscher": "✡️ Nicht Koscher-Konform",
        "placeholder": "Barcode eintippen...", "hist_title": "🕒 Letzte Scans", "details": "🔬 Inhaltsstoffe & Analyse"
    },
    "English": {
        "t1": "👤 Profile", "t2": "📸 Scanner", "t3": "⚙️ Settings", "t4": "ℹ️ Info",
        "title": "My Profile", "sub": "Configure your allergies and preferences", "save": "Save Profile",
        "cat_allergy": "Intolerances & Allergens", "cat_additives": "Additives", "cat_lifestyle": "Lifestyle & Religion",
        "laktose": "Lactose / Milk", "fruktose": "Fructose", "histamin": "Histamine", "sorbit": "Sorbitol",
        "gluten": "Gluten", "nuesse": "Tree Nuts", "soja": "Soy", "erdnuesse": "Peanuts",
        "sulfite": "Sulfites", "glutamat": "Glutamate", "vegan": "Vegan", "vegetarisch": "Vegetarian", "halal": "Halal", "koscher": "Kosher",
        "scan_h": "Scanner", "scan_p": "Use the camera or enter the code manually",
        "btn_cam_start": "📸 Start Scanner", "btn_cam_stop": "🛑 Stop Scanner",
        "safe": "✅ PRODUCT SAFE!", "safe_sub": "Matches your profile perfectly.",
        "warn": "🛑 NOT COMPATIBLE!", "not_found": "⚠️ Product not found.", "no_conn": "📡 Connection lost.",
        "lang_select": "Choose language:", "saved_msg": "✅ Profile saved!", "team_title": "👥 Team Class 10a",
        "w_laktose": "🥛 Contains Lactose", "w_fruktose": "🍎 Contains Fructose", "w_histamin": "🍷 Histamine Risk", "w_sorbit": "🍬 Contains Sorbitol",
        "w_sulfite": "🧪 Contains Sulfites", "w_glutamat": "🍕 Contains Glutamate", "w_gluten": "🌾 Contains Gluten", "w_nuesse": "🌰 Contains Nuts", "w_soja": "🌱 Contains Soy", "w_erdnuesse": "🥜 Contains Peanuts",
        "w_vegan": "🥩 Not Vegan", "w_vegetarisch": "🥩 Not Vegetarian", "w_halal": "☪️ Not Halal", "w_koscher": "✡️ Not Kosher",
        "placeholder": "Type barcode...", "hist_title": "🕒 History", "details": "🔬 Ingredients & Analysis"
    }
}

# Falls eine nicht unterstützte Sprache gewählt wird, falle auf Deutsch zurück
t = ui.get(st.session_state.lang, ui["Deutsch"])

# ==========================================
# 4. OFFLINE BACKUP DATA
# ==========================================
OFFLINE_DATA = {
    "3017620425035": {"product_name": "Nutella", "ingredients_text": "Zucker, Palmöl, Haselnüsse (13%), Magermilchpulver (8,7%), fettarmer Kakao, Emulgator Lecithine (Soja), Vanillin.", "image_front_url": "https://world.openfoodfacts.org/images/products/301/762/042/5035/front_fr.465.400.jpg"},
    "5449000000996": {"product_name": "Coca Cola Classic", "ingredients_text": "Wasser, Zucker, Kohlensäure, Farbstoff E 150d, Säuerungsmittel Phosphorsäure, natürliches Aroma, Aroma Koffein.", "image_front_url": "https://world.openfoodfacts.org/images/products/544/900/000/0996/front_de.643.400.jpg"}
}

# ==========================================
# 5. NAVIGATION (TABS)
# ==========================================
tab_profil, tab_scanner, tab_settings, tab_info = st.tabs([t["t1"], t["t2"], t["t3"], t["t4"]])

# --- TAB 1: MEIN SCHUTZPROFIL ---
with tab_profil:
    st.markdown(f"<h1>🛡️<br>{t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['sub']}</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"<h4>⚙️ {t['cat_allergy']}</h4>", unsafe_allow_html=True)
        st.session_state.profile["laktose"] = st.toggle(t["laktose"], value=st.session_state.profile["laktose"])
        st.session_state.profile["fruktose"] = st.toggle(t["fruktose"], value=st.session_state.profile["fruktose"])
        st.session_state.profile["histamin"] = st.toggle(t["histamin"], value=st.session_state.profile["histamin"])
        st.session_state.profile["sorbit"] = st.toggle(t["sorbit"], value=st.session_state.profile["sorbit"])
        st.session_state.profile["gluten"] = st.toggle(t["gluten"], value=st.session_state.profile["gluten"])
        st.session_state.profile["nuesse"] = st.toggle(t["nuesse"], value=st.session_state.profile["nuesse"])
        st.session_state.profile["soja"] = st.toggle(t["soja"], value=st.session_state.profile["soja"])
        st.session_state.profile["erdnuesse"] = st.toggle(t["erdnuesse"], value=st.session_state.profile["erdnuesse"])
        
    with st.container(border=True):
        st.markdown(f"<h4>🧪 {t['cat_additives']}</h4>", unsafe_allow_html=True)
        st.session_state.profile["sulfite"] = st.toggle(t["sulfite"], value=st.session_state.profile["sulfite"])
        st.session_state.profile["glutamat"] = st.toggle(t["glutamat"], value=st.session_state.profile["glutamat"])

    with st.container(border=True):
        st.markdown(f"<h4>🌱 {t['cat_lifestyle']}</h4>", unsafe_allow_html=True)
        st.session_state.profile["vegan"] = st.toggle(t["vegan"], value=st.session_state.profile["vegan"])
        st.session_state.profile["vegetarisch"] = st.toggle(t["vegetarisch"], value=st.session_state.profile["vegetarisch"])
        st.session_state.profile["halal"] = st.toggle(t["halal"], value=st.session_state.profile["halal"])
        st.session_state.profile["koscher"] = st.toggle(t["koscher"], value=st.session_state.profile["koscher"])

    if st.button(f"💾 {t['save']}"):
        st.success(t["saved_msg"])

# --- TAB 2: SCANNER ---
with tab_scanner:
    st.markdown(f"<h2>{t['scan_h']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['scan_p']}</p>", unsafe_allow_html=True)
    
    barcode_input = st.text_input("Barcode Entry", value=st.session_state.manual_code, placeholder=t["placeholder"], label_visibility="collapsed")
    
    if not barcode_input:
        if not st.session_state.cam_on:
            if st.button(t["btn_cam_start"]):
                st.session_state.cam_on = True
                st.rerun()
        else:
            if st.button(t["btn_cam_stop"]):
                st.session_state.cam_on = False
                st.rerun()
            
            with st.container(border=True):
                # Nativer Kamera-Input via Streamlit
                img_buffer = st.camera_input("Barcode scannen", label_visibility="collapsed")
                
                if img_buffer is not None:
                    # Bild öffnen und nach Barcode suchen
                    image = Image.open(img_buffer)
                    decoded_objects = decode(image)
                    
                    if decoded_objects:
                        # Barcode extrahieren und in den Session State speichern
                        barcode = decoded_objects[0].data.decode('utf-8')
                        st.session_state.manual_code = barcode
                        st.session_state.cam_on = False
                        st.rerun()
                    else:
                        st.warning("⚠️ Kein Barcode erkannt. Bitte halte den Code gut lesbar in die Kamera.")
    else:
        st.session_state.cam_on = False

    if barcode_input:
        barcode = "".join(filter(str.isdigit, barcode_input))
        
        if len(barcode) >= 8:
            with st.spinner("🔍 ..."):
                product = None
                is_offline = False
                
                try:
                    headers = {'User-Agent': 'AllergyShieldPro/5.0 (Windows; School Project)'}
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
                    p_name = product.get('product_name', 'Unknown Product')
                    if {"name": p_name, "code": barcode} not in st.session_state.history:
                        st.session_state.history.insert(0, {"name": p_name, "code": barcode})
                        if len(st.session_state.history) > 4: st.session_state.history.pop()
                    
                    # API-Analyse
                    tags_text = " ".join(product.get("allergens_tags", [])) + " " + " ".join(product.get("ingredients_analysis_tags", [])) + " " + " ".join(product.get("labels_tags", []))
                    all_text = (
                        str(product.get("ingredients_text", "")) + " " + 
                        str(product.get("ingredients_text_en", "")) + " " + 
                        str(product.get("ingredients_text_fr", "")) + " " + 
                        str(product.get("ingredients_text_de", "")) + " " + 
                        tags_text
                    ).lower()
                    
                    warnings = []
                    p = st.session_state.profile
                    
                    # Überprüfungskriterien
                    if p["laktose"] and any(w in all_text for w in ["milch", "milk", "lait", "lactose", "laktose", "molke", "sahne", "butter", "en:milk"]):
                        warnings.append(t["w_laktose"])
                    if p["fruktose"] and any(w in all_text for w in ["fructose", "fruktose", "fruchtzucker", "sirup"]):
                        warnings.append(t["w_fruktose"])
                    if p["histamin"] and any(w in all_text for w in ["histamin", "hefe", "yeast", "wein", "tomate", "schokolade"]):
                        warnings.append(t["w_histamin"])
                    if p["sorbit"] and any(w in all_text for w in ["sorbit", "sorbitol", "e420"]):
                        warnings.append(t["w_sorbit"])
                    if p["gluten"] and any(w in all_text for w in ["gluten", "weizen", "wheat", "blé", "gerste", "barley", "roggen", "rye", "hafer", "oats", "en:gluten"]):
                        warnings.append(t["w_gluten"])
                    if p["nuesse"] and any(w in all_text for w in ["nuss", "nüsse", "nuts", "amande", "noix", "haselnuss", "walnuss", "cashew", "mandel", "en:nuts"]):
                        warnings.append(t["w_nuesse"])
                    if p["soja"] and any(w in all_text for w in ["soja", "soy", "soya", "en:soybeans"]):
                        warnings.append(t["w_soja"])
                    if p["erdnuesse"] and any(w in all_text for w in ["erdnuss", "erdnüsse", "peanut", "peanuts", "cacahuète", "en:peanuts"]):
                        warnings.append(t["w_erdnuesse"])
                    if p["sulfite"] and any(w in all_text for w in ["sulfit", "sulfite", "schwefeldioxid", "e220", "en:sulphites"]):
                        warnings.append(t["w_sulfite"])
                    if p["glutamat"] and any(w in all_text for w in ["glutamat", "glutamate", "hefeextrakt", "e621"]):
                        warnings.append(t["w_glutamat"])
                        
                    if p["vegan"] and any(w in all_text for w in ["milch", "milk", "lait", "ei ", "egg", "oeuf", "fleisch", "meat", "viande", "honig", "honey", "miel", "gelatine", "en:non-vegetarian", "en:non-vegan"]):
                        warnings.append(t["w_vegan"])
                    if p["vegetarisch"] and any(w in all_text for w in ["fleisch", "meat", "viande", "fisch", "fish", "poisson", "gelatine", "en:non-vegetarian"]):
                        warnings.append(t["w_vegetarisch"])
                    if p["halal"] and any(w in all_text for w in ["schwein", "pork", "porc", "alkohol", "alcohol"]):
                        warnings.append(t["w_halal"])
                    if p["koscher"] and any(w in all_text for w in ["schwein", "pork", "porc", "schalentiere", "shrimp"]):
                        warnings.append(t["w_koscher"])
                        
                    # SPLIT SCREEN LAYOUT
                    st.write("")
                    col_left, col_right = st.columns([1.3, 1], gap="medium")
                    
                    with col_left:
                        st.markdown(f"<h3>{p_name}</h3>", unsafe_allow_html=True)
                        if warnings:
                            st.markdown(f"""
                            <div class="result-box-warn">
                                <h3 style="color:#991B1B; margin:0;">{t['warn']}</h3>
                                <p style="text-align:left; color:#991B1B; margin-top:10px; margin-bottom:0; font-weight:600;">
                                    {"<br>".join(["• " + w for w in warnings])}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="result-box-safe">
                                <h3 style="color:#065F46; margin:0;">{t['safe']}</h3>
                                <p style="text-align:left; color:#065F46; margin-top:10px; margin-bottom:0; font-weight:600;">{t['safe_sub']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            throw_confetti()
                            
                    with col_right:
                        if product.get("image_front_url"):
                            st.markdown("<div style='display: flex; justify-content: center; align-items: center; max-height: 220px; overflow:hidden; border-radius:15px;'>", unsafe_allow_html=True)
                            st.image(product["image_front_url"], use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.write("")
                    with st.expander(t["details"]):
                        if is_offline: st.caption("ℹ️ Offline Fallback")
                        st.write(f"**Ingredients:** {product.get('ingredients_text', 'N/A')}")
                else:
                    st.error(t["not_found"])

    # --- SCAN HISTORIE ---
    if st.session_state.history:
        st.write("")
        st.markdown(f"<h3>🕒 {t['hist_title']}</h3>", unsafe_allow_html=True)
        for item in st.session_state.history:
            if st.button(f"▫️ {item['name']} ({item['code']})", key=f"hist_{item['code']}", help="Erneut prüfen"):
                st.session_state.manual_code = item['code']
                st.rerun()

# --- TAB 3: EINSTELLUNGEN ---
with tab_settings:
    st.markdown(f"<h2>{t['t3']}</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h4>🌐 {t['lang_select']}</h4>", unsafe_allow_html=True)
        lang_list = ["Deutsch", "English"] # (Hier habe ich die anderen Sprachen zur Übersichtlichkeit ausgeblendet, du kannst das Dictionary aber einfach mit deinen anderen Sprachen wieder auffüllen)
        new_lang = st.selectbox("Language Selection", lang_list, index=lang_list.index(st.session_state.lang) if st.session_state.lang in lang_list else 0, label_visibility="collapsed")
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()

# --- TAB 4: INFO ---
with tab_info:
    with st.container(border=True):
        st.markdown(f"<h2>{t['team_title']}</h2>", unsafe_allow_html=True)
        st.divider()
        st.write("👨‍💻 **Marius Boulos**")
        st.write("👨‍💻 **Benjamin Mehling**")
        st.write("👩‍💻 **Sophie Hartwig**")
        st.write("👨‍💻 **Ben Henkel**")
        st.write("👨‍💻 **Maximilian Maier**")
        st.caption("Hanns-Seidel-Gymnasium Aschaffenburg / Germany")
