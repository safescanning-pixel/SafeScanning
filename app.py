import streamlit as st
import requests
import streamlit.components.v1 as components
from camera_input_live import camera_input_live

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
   
    /* History Buttons */
    .stButton>button[data-testid="baseButton-secondary"] {
        background-color: #F3F4F6 !important; color: #4B5563 !important; height: 38px !important; border-radius: 12px !important; font-size: 13px !important; box-shadow: none !important;
    }
   
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
# 3. GLOBAL STATE & SPRACHEN (FEHLER BEHOBEN)
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = "Deutsch"
if 'cam_on' not in st.session_state: st.session_state.cam_on = False
if 'history' not in st.session_state: st.session_state.history = []
if 'manual_code' not in st.session_state: st.session_state.manual_code = ""
if 'profile' not in st.session_state:
    st.session_state.profile = {
        "laktose": False, "fruktose": False, "histamin": False, "sorbit": False,
        "sulfite": False, "glutamat": False,
        "vegan": False, "vegetarisch": False, "halal": False, "koscher": False
    }

ui = {
    "Deutsch": {
        "t1": "👤 Profil", "t2": "📸 Scanner", "t3": "⚙️ Einstellungen", "t4": "ℹ️ Info",
        "title": "Mein Schutzprofil", "sub": "Konfigurieren Sie Ihre Allergien und Unverträglichkeiten", "save": "Profil speichern",
        "cat_allergy": "Intoleranzen", "cat_additives": "Zusatzstoffe", "cat_lifestyle": "Lebensstil & Religion",
        "laktose": "Laktose / Milch", "fruktose": "Fruktose", "histamin": "Histamin", "sorbit": "Sorbit",
        "sulfite": "Sulfite", "glutamat": "Glutamat",
        "vegan": "Vegan", "vegetarisch": "Vegetarisch", "halal": "Halal (حلال)", "koscher": "Koscher (כָּشֵׁر)",
        "scan_h": "Scanner", "scan_p": "Nutzen Sie die Kamera oder geben Sie den Code manuell ein",
        "btn_cam_start": "📸 Live-Kamera starten", "btn_cam_stop": "🛑 Kamera ausschalten",
        "safe": "✅ PRODUKT GEEIGNET!", "safe_sub": "Dieses Produkt entspricht vollständig deinem Schutzprofil.",
        "warn": "🛑 NICHT GEEIGNET!", "not_found": "⚠️ Produkt nicht gefunden.", "no_conn": "📡 Keine Verbindung zur Datenbank (Offline-Modus aktiv).",
        "lang_select": "Wähle deine Sprache:", "saved_msg": "✅ Profil erfolgreich gespeichert!", "team_title": "👥 Entwickler-Team Klasse 10a",
        "w_laktose": "🥛 Enthält Laktose/Milch", "w_fruktose": "🍎 Enthält Fruktose", "w_histamin": "🍷 Histamin-Risiko erkannt", "w_sorbit": "🍬 Enthält Sorbit (E420)",
        "w_sulfite": "🧪 Enthält Sulfite (Schwefeldioxid)", "w_glutamat": "🍕 Enthält Glutamat (Geschmacksverstärker)",
        "w_vegan": "🥩 Nicht Vegan", "w_vegetarisch": "🥩 Nicht Vegetarisch", "w_halal": "☪️ Nicht Halal-Konform", "w_koscher": "✡️ Nicht Koscher-Konform",
        "placeholder": "Barcode eintippen (z.B. 3017620425035)", "hist_title": "🕒 Letzte Scans", "details": "🔬 Inhaltsstoffe & Analyse einsehen"
    },
    "English": {
        "t1": "👤 Profile", "t2": "📸 Scanner", "t3": "⚙️ Settings", "t4": "ℹ️ Info",
        "title": "My Protection Profile", "sub": "Configure your allergies and dietary preferences", "save": "Save Profile",
        "cat_allergy": "Intolerances", "cat_additives": "Additives", "cat_lifestyle": "Lifestyle & Religion",
        "laktose": "Lactose / Milk", "fruktose": "Fructose", "histamin": "Histamine", "sorbit": "Sorbitol",
        "sulfite": "Sulfites", "glutamat": "Glutamate",
        "vegan": "Vegan", "vegetarisch": "Vegetarian", "halal": "Halal", "koscher": "Kosher",
        "scan_h": "Scanner", "scan_p": "Use the camera or enter the code manually",
        "btn_cam_start": "📸 Start Live Camera", "btn_cam_stop": "🛑 Turn Off Camera",
        "safe": "✅ PRODUCT SAFE!", "safe_sub": "This product matches your protection profile perfectly.",
        "warn": "🛑 NOT COMPATIBLE!", "not_found": "⚠️ Product not found.", "no_conn": "📡 No database connection (Offline Mode active).",
        "lang_select": "Choose your language:", "saved_msg": "✅ Profile successfully saved!", "team_title": "👥 Developer Team Class 10a",
        "w_laktose": "🥛 Contains Lactose/Milk", "w_fruktose": "🍎 Contains Fructose", "w_histamin": "🍷 Histamine risk detected", "w_sorbit": "🍬 Contains Sorbitol (E420)",
        "w_sulfite": "🧪 Contains Sulfites", "w_glutamat": "🍕 Contains Glutamate",
        "w_vegan": "🥩 Not Vegan", "w_vegetarisch": "🥩 Not Vegetarian", "w_halal": "☪️ Not Halal Compliant", "w_koscher": "✡️ Not Kosher Compliant",
        "placeholder": "Type barcode (e.g. 3017620425035)", "hist_title": "🕒 Scan History", "details": "🔬 View Ingredients & Analysis"
    },
    "Türkçe": {
        "t1": "👤 Profil", "t2": "📸 Tarayıcı", "t3": "⚙️ Ayarlar", "t4": "ℹ️ Bilgi",
        "title": "Koruma Profilim", "sub": "Alerjilerinizi ve diyet tercihlerinizi yapılandırın", "save": "Profili Kaydet",
        "cat_allergy": "İntoleranslar", "cat_additives": "Katkı Maddeleri", "cat_lifestyle": "Yaşam Tarzı ve Din",
        "laktose": "Laktoz / Süt", "fruktose": "Fruktoz", "histamin": "Histamin", "sorbit": "Sorbitol",
        "sulfite": "Sülfitler", "glutamat": "Glutamat",
        "vegan": "Vegan", "vegetarisch": "Vejetaryen", "halal": "Helal", "koscher": "Koşer",
        "scan_h": "Tarayıcı", "scan_p": "Kamerayı kullanın veya kodu manuel olarak girin",
        "btn_cam_start": "📸 Canlı Kamerayı Başlat", "btn_cam_stop": "🛑 Kamerayı Kapat",
        "safe": "✅ ÜRÜN GÜVENLİ!", "safe_sub": "Bu ürün koruma profilinizle tamamen eşleşiyor.",
        "warn": "🛑 UYGUN DEĞİL!", "not_found": "⚠️ Ürün bulunamadı.", "no_conn": "📡 Veritabanı bağlantısı yok (Çevrimdışı Mod aktif).",
        "lang_select": "Dilinizi seçin:", "saved_msg": "✅ Profil başarıyla kaydedildi!", "team_title": "👥 Geliştirici Ekibi Sınıf 10a",
        "w_laktose": "🥛 Laktoz/Süt içerir", "w_fruktose": "🍎 Fruktoz içerir", "w_histamin": "🍷 Histamin riski", "w_sorbit": "🍬 Sorbitol içerir",
        "w_sulfite": "🧪 Sülfit içerir", "w_glutamat": "🍕 Glutamat içerir",
        "w_vegan": "🥩 Vegan Değil", "w_vegetarisch": "🥩 Vejetaryen Değil", "w_halal": "☪️ Helal Değil", "w_koscher": "✡️ Koşer Değil",
        "placeholder": "Barkod yazın (örn. 3017620425035)", "hist_title": "🕒 Tarama Geçmişi", "details": "🔬 İçerik ve Analizi Görüntüle"
    },
    "العربية": {
        "t1": "👤 ملفi", "t2": "📸 ماسح", "t3": "⚙️ إعدادات", "t4": "ℹ️ معلومات",
        "title": "ملف الحماية الخاص بي", "sub": "قم بتكوين الحساسية وتفضيلاتك الغذائية", "save": "حفظ الملف",
        "cat_allergy": "عدم التحمل", "cat_additives": "المضافات الغذائية", "cat_lifestyle": "نمط الحياة والدين",
        "laktose": "اللاكتوز / الحليب", "fruktose": "الفركتوز", "histamin": "الهيستامين", "sorbit": "السوربيتول",
        "sulfite": "الكبريتيت", "glutamat": "الغلوتامات",
        "vegan": "نباتي تام (Vegan)", "vegetarisch": "نباتي (Vegetarian)", "halal": "حلال", "koscher": "كوشر",
        "scan_h": "الماسح الضوئي", "scan_p": "استخدم الكاميرا أو أدخل الرمز يدويًا",
        "btn_cam_start": "📸 تشغيل الكاميرا الحية", "btn_cam_stop": "🛑 إيقاف الكاميرا",
        "safe": "✅ المنتج آمن!", "safe_sub": "هذا المنتج يتوافق تمامًا مع ملف الحماية الخاص بك.",
        "warn": "🛑 غير متوافق!", "not_found": "⚠️ لم يتم العثور على المنتج.", "no_conn": "📡 لا يوجد اتصال بقاعدة البيانات (الوضع غير المتصل نشط).",
        "lang_select": "اختر لغتك:", "saved_msg": "✅ تم حفظ الملف بنجاح!", "team_title": "👥 فريق التطوير الصف 10a",
        "w_laktose": "🥛 يحتوي على اللاكتوز/الحليب", "w_fruktose": "🍎 يحتوي على الفركتوز", "w_histamin": "🍷 خطر الهيستامين", "w_sorbit": "🍬 يحتوي على السوربيتول",
        "w_sulfite": "🧪 يحتوي على الكبريتيت", "w_glutamat": "🍕 يحتوي على الغلوتامات",
        "w_vegan": "🥩 ليس نباتياً تاماً", "w_vegetarisch": "🥩 ليس نباتياً", "w_halal": "☪️ غير متوافق مع الحلال", "w_koscher": "✡️ غير متوافق مع الكوشر",
        "placeholder": "اكتب الباركود (مثال: 3017620425035)", "hist_title": "🕒 تاريخ المسح", "details": "🔬 عرض المكونات والتحليل"
    },
    "Español": {
        "t1": "👤 Perfil", "t2": "📸 Escáner", "t3": "⚙️ Ajustes", "t4": "ℹ️ Info",
        "title": "Mi Perfil de Protección", "sub": "Configure sus alergias y preferencias dietéticas", "save": "Guardar Perfil",
        "cat_allergy": "Intolerancias", "cat_additives": "Aditivos", "cat_lifestyle": "Estilo de Vida y Religión",
        "laktose": "Lactosa / Leche", "fruktose": "Fructosa", "histamin": "Histamina", "sorbit": "Sorbitol",
        "sulfite": "Sulfitos", "glutamat": "Glutamato",
        "vegan": "Vegano", "vegetarisch": "Vegetariano", "halal": "Halal", "koscher": "Kosher",
        "scan_h": "Escáner", "scan_p": "Use la cámara o ingrese el código manualmente",
        "btn_cam_start": "📸 Activar Cámara", "btn_cam_stop": "🛑 Apagar Cámara",
        "safe": "✅ ¡PRODUCTO SEGURO!", "safe_sub": "Este producto coincide perfectamente con tu perfil.",
        "warn": "🛑 ¡NO COMPATIBLE!", "not_found": "⚠️ Producto no encontrado.", "no_conn": "📡 Sin conexión a la base de datos (Modo Offline activo).",
        "lang_select": "Elige tu idioma:", "saved_msg": "✅ ¡Perfil guardado con éxito!", "team_title": "👥 Equipo de Desarrollo Clase 10a",
        "w_laktose": "🥛 Contiene Lactosa/Leche", "w_fruktose": "🍎 Contiene Fructosa", "w_histamin": "🍷 Riesgo de histamina", "w_sorbit": "🍬 Contiene Sorbitol",
        "w_sulfite": "🧪 Contiene Sulfitos", "w_glutamat": "🍕 Contiene Glutamato",
        "w_vegan": "🥩 No es Vegano", "w_vegetarisch": "🥩 No es Vegetariano", "w_halal": "☪️ No es Halal", "w_koscher": "✡️ No es Kosher",
        "placeholder": "Escriba el código (ej. 3017620425035)", "hist_title": "🕒 Historial de Scans", "details": "🔬 Ver Ingredientes y Análisis"
    }
}
t = ui[st.session_state.lang]

# ==========================================
# 4. OFFLINE BACKUP DATA
# ==========================================
OFFLINE_DATA = {
    "3017620425035": {"product_name": "Nutella", "ingredients_text": "Zucker, Palmöl, Haselnüsse (13%), Magermilchpulver (8,7%), fettarmer Kakao, Emulgator Lecithine (Soja), Vanillin.", "image_front_url": "https://world.openfoodfacts.org/images/products/301/762/042/5035/front_fr.465.400.jpg"},
    "5449000000996": {"product_name": "Coca Cola Classic", "ingredients_text": "Wasser, Zucker, Kohlensäure, Farbstoff E 150d, Säuerungsmittel Phosphorsäure, natürliches Aroma, Aroma Koffein.", "image_front_url": "https://world.openfoodfacts.org/images/products/544/900/000/0996/front_de.643.400.jpg"},
    "4008400130723": {"product_name": "Hanuta", "ingredients_text": "Zucker, pflanzliche Fette (Palm, Shea), Weizenmehl (13,5%), Haselnüsse (13%), Süßmolkenpulver, fettarmer Kakao, Vollmilchschokolade, Magermilchpulver, Butterreinfett, Salz, Emulgator Sojalecithine.", "image_front_url": "https://world.openfoodfacts.org/images/products/400/840/013/0723/front_de.121.400.jpg"},
    "4003050000551": {"product_name": "Haribo Goldbären", "ingredients_text": "Glukosesirup; Zucker; Gelatine; Dextrose; Fruchtsaft aus Fruchtsaftkonzentrat: Apfel, Erdbeere, Himbeere, Orange, Zitrone, Ananas; Säuerungsmittel: Citronensäure; Frucht- und Pflanzenkonzentrate; Aroma; Überzugsmittel: Bienenwachs weiß und gelb, Carnaubawachs.", "image_front_url": "https://world.openfoodfacts.org/images/products/400/305/000/0551/front_de.229.400.jpg"}
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
                camera_input_live()
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
                    p_name = product.get('product_name', 'Unknown')
                    if {"name": p_name, "code": barcode} not in st.session_state.history:
                        st.session_state.history.insert(0, {"name": p_name, "code": barcode})
                        if len(st.session_state.history) > 4: st.session_state.history.pop()
                   
                    all_text = (
                        str(product.get("ingredients_text", "")) + " " +
                        str(product.get("ingredients_text_en", "")) + " " +
                        str(product.get("ingredients_text_fr", "")) + " " +
                        str(product.get("allergens_hierarchy", ""))
                    ).lower()
                   
                    warnings = []
                    p = st.session_state.profile
                   
                    # Überprüfungskriterien
                    if p["laktose"] and any(w in all_text for w in ["milch", "milk", "lait", "lactose", "laktose", "molke", "sahne", "butter", "whey"]):
                        warnings.append(t["w_laktose"])
                    if p["fruktose"] and any(w in all_text for w in ["fructose", "fruktose", "fruchtzucker", "sirup", "syrup"]):
                        warnings.append(t["w_fruktose"])
                    if p["histamin"] and any(w in all_text for w in ["histamin", "hefe", "yeast", "wein", "wine", "tomate", "schokolade", "chocolate"]):
                        warnings.append(t["w_histamin"])
                    if p["sorbit"] and any(w in all_text for w in ["sorbit", "sorbitol", "e420"]):
                        warnings.append(t["w_sorbit"])
                    if p["sulfite"] and any(w in all_text for w in ["sulfit", "sulfite", "schwefeldioxid", "sulfur dioxide", "e220", "e221", "e222", "e223", "e224"]):
                        warnings.append(t["w_sulfite"])
                    if p["glutamat"] and any(w in all_text for w in ["glutamat", "glutamate", "hefeextrakt", "mononatiumglutamat", "e621"]):
                        warnings.append(t["w_glutamat"])
                       
                    if p["vegan"] and any(w in all_text for w in ["milch", "milk", "lait", "ei ", "egg", "fleisch", "meat", "honig", "honey", "gelatine", "rind", "schwein", "pork", "beef"]):
                        warnings.append(t["w_vegan"])
                    if p["vegetarisch"] and any(w in all_text for w in ["fleisch", "meat", "fisch", "fish", "gelatine", "schwein", "pork", "rind", "beef", "karmin"]):
                        warnings.append(t["w_vegetarisch"])
                    if p["halal"] and any(w in all_text for w in ["schwein", "pork", "porc", "alkohol", "alcohol", "wein", "wine", "gelatine"]):
                        warnings.append(t["w_halal"])
                    if p["koscher"] and any(w in all_text for w in ["schwein", "pork", "krustentier", "shellfish", "gelatine"]):
                        warnings.append(t["w_koscher"])
                       
                    # SPLIT SCREEN LAYOUT: LINKS ERGEBNIS | RECHTS BILD
                    st.write("")
                    col_left, col_right = st.columns([1.3, 1], gap="medium")
                   
                    with col_left:
                        st.markdown(f"<h3>{p_name}</h3>", unsafe_allow_html=True)
                        if warnings:
                            st.markdown(f"""
                            <div class="result-box-warn">
                                <h3 style="color:#991B1B; margin:0;">{t['warn']}</h3>
                                <p style="text-align:left; color:#991B1B; margin-top:10px; margin-bottom:0;">
                                    {"<br>".join(["• " + w for w in warnings])}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="result-box-safe">
                                <h3 style="color:#065F46; margin:0;">{t['safe']}</h3>
                                <p style="text-align:left; color:#065F46; margin-top:10px; margin-bottom:0;">{t['safe_sub']}</p>
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
                        if is_offline: st.caption("ℹ️ OfflineFallback")
                        st.write(f"**Ingredients:** {product.get('ingredients_text', 'N/A')}")
                else:
                    st.error(t["not_found"])

    if st.session_state.history:
        st.write("")
        st.markdown(f"<h5>{t['hist_title']}</h5>", unsafe_allow_html=True)
        h_cols = st.columns(len(st.session_state.history))
        for idx, item in enumerate(st.session_state.history):
            with h_cols[idx]:
                if st.button(item["name"], key=f"hist_{idx}", use_container_width=True):
                    st.session_state.manual_code = item["code"]
                    st.rerun()

# --- TAB 3: EINSTELLUNGEN ---
with tab_settings:
    st.markdown(f"<h2>{t['t3']}</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h4>🌐 {t['lang_select']}</h4>", unsafe_allow_html=True)
        new_lang = st.selectbox("Language Selection", ["Deutsch", "English", "Türkçe", "العربية", "Español"], index=["Deutsch", "English", "Türkçe", "العربية", "Español"].index(st.session_state.lang), label_visibility="collapsed")
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()

# --- TAB 4: INFO ---
with tab_info:
    with st.container(border=True):
        st.markdown(f"<h2>{t['team_title']}</h2>", unsafe_allow_html=True)
        st.divider()
        st.write("👨‍💻 **Benjamin Mehling**")
        st.write("👨‍💻 **Benjamin Henkel**")
        st.write("👨‍💻 **Maximilian Maier**")
        st.write("👨‍💻 **Marius Boulos**")
        st.write("👨‍💻 **Tomma Meyer**")
        st.write("👩‍💻 **Sophie Hartwig**")
        st.caption("Hanns-Seidel-Gymnasium Aschaffenburg | Klasse 10a")

