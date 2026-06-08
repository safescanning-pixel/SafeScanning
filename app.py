import streamlit as st
import requests
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="AllergyShield Pro", page_icon="🛡️", layout="centered")

if "scanned_barcode" in st.query_params:
    scanned = st.query_params.get("scanned_barcode")
    if scanned:
        st.session_state.manual_code = scanned
        st.session_state.cam_on = False  
        st.query_params.clear()  

st.markdown("""
    <style>
    .stApp { 
        background-color: #F8F9FA; 
        color: #111827; 
        font-family: 'SF Pro Display', -apple-system, sans-serif; 
    }
    header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { 
        background-color: white; 
        padding: 6px; 
        border-radius: 24px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.02); 
        gap: 8px; 
        justify-content: center; 
        margin-bottom: 25px; 
    }
    .stTabs [data-baseweb="tab"] { 
        height: 46px; 
        border-radius: 18px; 
        color: #6B7280; 
        font-weight: 600; 
        font-size: 14px; 
        padding: 0 20px; 
        border: none !important; 
    }
    .stTabs [aria-selected="true"] { 
        background-color: #E0E7FF !important; 
        color: #4F46E5 !important; 
    }
    div[data-testid="stVerticalBlock"] > div[style*="border"] { 
        background-color: white !important; 
        border-radius: 24px !important; 
        border: 1px solid #F3F4F6 !important; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.02) !important; 
        padding: 25px !important; 
        margin-bottom: 15px; 
    }
    h1 { color: #111827 !important; text-align: center; font-weight: 800; font-size: 32px; margin-bottom: 5px;}
    h2 { color: #111827 !important; text-align: center; font-weight: 800; font-size: 26px; margin-bottom: 5px;}
    h3 { color: #111827 !important; text-align: left; font-weight: 700; font-size: 22px; margin-bottom: 10px;}
    h4 { color: #111827 !important; text-align: left; font-weight: 700; font-size: 16px; margin-bottom: 15px !important;}
    p {text-align: center; color: #6B7280; font-size: 15px; margin-bottom: 20px;}
    .stButton>button { 
        background-color: #4F46E5 !important; 
        color: white !important; 
        border-radius: 20px !important; 
        height: 50px !important; 
        width: 100% !important; 
        font-weight: 700 !important; 
        font-size: 15px !important; 
        border: none !important; 
        transition: all 0.2s ease; 
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important; 
    }
    .stButton>button:hover { 
        background-color: #4338CA !important; 
        transform: translateY(-1px); 
    }
    .result-box-safe { 
        background-color: #ECFDF5; 
        border: 4px solid #10B981; 
        border-radius: 20px; 
        padding: 20px; 
        color: #065F46; 
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.4); 
    }
    .result-box-warn { 
        background-color: #FEF2F2; 
        border: 4px solid #EF4444; 
        border-radius: 20px; 
        padding: 20px; 
        color: #991B1B; 
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.4); 
    }
    .nutri-badge { 
        padding: 8px 16px; 
        border-radius: 10px; 
        font-weight: 800; 
        color: white; 
        display: inline-block; 
        font-size: 18px; 
        margin-top: 5px; 
    }
    .nutri-a { background-color: #038141; }
    .nutri-b { background-color: #85BB2F; }
    .nutri-c { background-color: #FECB02; }
    .nutri-d { background-color: #EE8100; }
    .nutri-e { background-color: #E63E11; }
    .nutri-unknown { background-color: #9CA3AF; }
    
    /* NEU: CSS für Werbebanner */
    .ad-banner {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(90deg, #f3f4f6, #e5e7eb, #f3f4f6);
        color: #6B7280;
        text-align: center;
        padding: 12px;
        font-weight: 800;
        font-size: 13px;
        letter-spacing: 2px;
        border-top: 1px solid #d1d5db;
        z-index: 9999;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
    }
    .ad-left-banner {
        position: fixed;
        top: 25%;
        left: 10px;
        width: 45px;
        height: 250px;
        background: linear-gradient(180deg, #f3f4f6, #e5e7eb, #f3f4f6);
        color: #6B7280;
        text-align: center;
        padding: 15px 5px;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 3px;
        border: 1px solid #d1d5db;
        border-radius: 12px;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: center;
        writing-mode: vertical-rl;
        text-orientation: mixed;
    }
    .ad-spacer {
        height: 70px; /* Verhindert, dass Content vom Banner verdeckt wird */
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def throw_confetti():
    components.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>confetti({ particleCount: 180, spread: 90, origin: { y: 0.6 }, colors: ['#4F46E5', '#10B981', '#F59E0B'] });</script>
        """, height=0,
    )


if 'lang' not in st.session_state: 
    st.session_state.lang = "Deutsch"
if 'cam_on' not in st.session_state: 
    st.session_state.cam_on = False
if 'history' not in st.session_state: 
    st.session_state.history = []
if 'manual_code' not in st.session_state: 
    st.session_state.manual_code = ""
if 'ad_free' not in st.session_state: # NEU: Status für Werbefreiheit
    st.session_state.ad_free = False
if 'profile' not in st.session_state:
    st.session_state.profile = {
        "laktose": False, 
        "fruktose": False, 
        "histamin": False, 
        "sorbit": False, 
        "sulfite": False, 
        "glutamat": False,
        "gluten": False, 
        "nuesse": False, 
        "soja": False, 
        "erdnuesse": False, 
        "vegan": False, 
        "vegetarisch": False, 
        "halal": False, 
        "koscher": False
    }

ui = {
    "Deutsch": {
        "t1": "👤 Profil", 
        "t2": "📸 Scanner", 
        "t3": "⚙️ Einstellungen", 
        "t4": "ℹ️ Info",
        "title": "Mein Schutzprofil", 
        "sub": "Konfigurieren Sie Ihre Allergien und Unverträglichkeiten", 
        "save": "Profil speichern",
        "cat_allergy": "Intoleranzen & Allergien", 
        "cat_additives": "Zusatzstoffe", 
        "cat_lifestyle": "Lebensstil & Religion",
        "laktose": "Laktose / Milch", 
        "fruktose": "Fruktose", 
        "histamin": "Histamin", 
        "sorbit": "Sorbit",
        "gluten": "Gluten / Zöliakie", 
        "nuesse": "Schalenfrüchte / Nüsse", 
        "soja": "Soja", 
        "erdnuesse": "Erdnüsse",
        "sulfite": "Sulfite", 
        "glutamat": "Glutamat", 
        "vegan": "Vegan", 
        "vegetarisch": "Vegetarisch", 
        "halal": "Halal (حلال)", 
        "koscher": "Koscher (כָּشֵׁר)",
        "scan_h": "Scanner", 
        "scan_p": "Nutzen Sie die Kamera oder geben Sie den Code manuell ein",
        "btn_cam_start": "📸 Scanner starten", 
        "btn_cam_stop": "🛑 Scanner stoppen",
        "safe": "✅ PRODUKT GEEIGNET!", 
        "safe_sub": "Dieses Produkt entspricht vollständig deinem Schutzprofil.",
        "warn": "🛑 NICHT GEEIGNET!", 
        "not_found": "⚠️ Produkt nicht in der Datenbank gefunden.", 
        "lang_select": "Wähle deine Sprache:", 
        "saved_msg": "✅ Profil erfolgreich gespeichert!", 
        "team_title": "👥 Entwickler-Team",
        "w_laktose": "🥛 Enthält Laktose/Milch", 
        "w_fruktose": "🍎 Enthält Fruktose", 
        "w_histamin": "🍷 Histamin-Risiko erkannt", 
        "w_sorbit": "🍬 Enthält Sorbit (E420)",
        "w_sulfite": "🧪 Enthält Sulfite (Schwefeldioxid)", 
        "w_glutamat": "🍕 Enthält Glutamat", 
        "w_gluten": "🌾 Enthält Gluten", 
        "w_nuesse": "🌰 Enthält Schalenfrüchte/Nüsse", 
        "w_soja": "🌱 Enthält Soja", 
        "w_erdnuesse": "🥜 Enthält Erdnüsse",
        "w_vegan": "🥩 Nicht Vegan", 
        "w_vegetarisch": "🥩 Nicht Vegetarisch", 
        "w_halal": "☪️ Nicht Halal-Konform", 
        "w_koscher": "✡️ Nicht Koscher-Konform",
        "placeholder": "Barcode eintippen...", 
        "hist_title": "🕒 Letzte Scans", 
        "details": "🔬 Inhaltsstoffe & Analyse",
        "nutri_title": "🥗 Nährwert-Qualität", 
        "cal_title": "🔥 Kalorien-Check", 
        "cal_slider": "Dein täglicher Kalorien-Richtwert (kcal):",
        "cal_percentage": "Dieses Produkt verbraucht **{:.1f}%** deines Tagesbedarfs pro 100g.", 
        "de_ingredients": "🇩🇪 Deutsche Zutatenliste (Übersetzt):"
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
        "warn": "🛑 NOT COMPATIBLE!", "not_found": "⚠️ Product not found.", 
        "lang_select": "Choose language:", "saved_msg": "✅ Profile saved!", "team_title": "👥 Team Class 10a",
        "w_laktose": "🥛 Contains Lactose", "w_fruktose": "🍎 Contains Fructose", "w_histamin": "🍷 Histamine Risk", "w_sorbit": "🍬 Contains Sorbitol",
        "w_sulfite": "🧪 Contains Sulfites", "w_glutamat": "🍕 Contains Glutamate", "w_gluten": "🌾 Contains Gluten", "w_nuesse": "🌰 Contains Nuts", "w_soja": "🌱 Contains Soy", "w_erdnuesse": "🥜 Contains Peanuts",
        "w_vegan": "🥩 Not Vegan", "w_vegetarisch": "🥩 Not Vegetarian", "w_halal": "☪️ Not Halal", "w_koscher": "✡️ Not Kosher",
        "placeholder": "Type barcode...", "hist_title": "🕒 History", "details": "🔬 Ingredients & Analysis",
        "nutri_title": "🥗 Nutritional Quality", "cal_title": "🔥 Calorie Check", "cal_slider": "Your daily calorie guideline (kcal):",
        "cal_percentage": "This product uses **{:.1f}%** of your daily budget per 100g.", "de_ingredients": "🇩🇪 German Ingredients:"
    },
    "日本語": {
        "t1": "👤 プロファイル", "t2": "📸 スキャナー", "t3": "⚙️ 設定", "t4": "ℹ️ 情報",
        "title": "保護プロファイル", "sub": "アレルギーと食事制限の設定", "save": "保存する",
        "cat_allergy": "不耐症とアレルゲン", "cat_additives": "添加物", "cat_lifestyle": "ライフスタイル",
        "laktose": "乳糖 / ミルク", "fruktose": "果糖", "histamin": "ヒスタミン", "sorbit": "ソルビトール",
        "gluten": "グルテン", "nuesse": "ナッツ類", "soja": "大豆", "erdnuesse": "ピーナッツ",
        "sulfite": "亜硫酸塩", "glutamat": "グルタミン酸", "vegan": "ヴィーガン", "vegetarisch": "ベジタリアン", "halal": "ハラール", "koscher": "コーシャ",
        "scan_h": "スキャナー", "scan_p": "カメラか手動でバーコードを入力してください",
        "btn_cam_start": "📸 スキャナーを起動", "btn_cam_stop": "🛑 スキャナーを停止",
        "safe": "✅ 安全な製品です！", "safe_sub": "プロファイルに完全に一致しています。",
        "warn": "🛑 適合しません！", "not_found": "⚠️ 製品が見つかりません。", 
        "lang_select": "言語を選択:", "saved_msg": "✅ 保存されました！", "team_title": "👥 開発チーム",
        "w_laktose": "🥛 乳成分含有", "w_fruktose": "🍎 果糖含有", "w_histamin": "🍷 ヒスタミンのリスク", "w_sorbit": "🍬 ソルビトール含有",
        "w_sulfite": "🧪 亜硫酸塩含有", "w_glutamat": "🍕 グルタミン酸含有", "w_gluten": "🌾 グルテン含有", "w_nuesse": "🌰 ナッツ類含有", "w_soja": "🌱 大豆含有", "w_erdnuesse": "🥜 ピーナッツ含有",
        "w_vegan": "🥩 ヴィーガン非対応", "w_vegetarisch": "🥩 ベジタリアン非対応", "w_halal": "☪️ ハラール非対応", "w_koscher": "✡️ コーシャ非対応",
        "placeholder": "バーコードを入力...", "hist_title": "🕒 履歴", "details": "🔬 成分と分析",
        "nutri_title": "🥗 栄養品質", "cal_title": "🔥 カロリー", "cal_slider": "一日の目標カロリー (kcal):",
        "cal_percentage": "100gあたり一日の目標の **{:.1f}%**。", "de_ingredients": "🇩🇪 成分リスト:"
    },
    "العربية": {
        "t1": "👤 الملف الشخصي", "t2": "📸 الماسح الضوئي", "t3": "⚙️ الإعدادات", "t4": "ℹ️ معلومات",
        "title": "ملف الحماية الخاص بي", "sub": "قم بتكوين الحساسية والتفضيلات الغذائية", "save": "حفظ الملف",
        "cat_allergy": "الحساسية وعدم التحمل", "cat_additives": "المواد المضافة", "cat_lifestyle": "نمط الحياة والدين",
        "laktose": "اللاكتوز / الحليب", "fruktose": "الفركتوز", "histamin": "الهيستامين", "sorbit": "السوربيتول",
        "gluten": "الغلوتين", "nuesse": "المكسرات", "soja": "الصويا", "erdnuesse": "الفول السوداني",
        "sulfite": "الكبريتيت", "glutamat": "الغلوتامات", "vegan": "نباتي تام", "vegetarisch": "نباتي", "halal": "حلال", "koscher": "كوشير",
        "scan_h": "الماسح الضوئي", "scan_p": "استخدم الكاميرا أو أدخل الرمز يدويًا",
        "btn_cam_start": "📸 تشغيل الماسح", "btn_cam_stop": "🛑 إيقاف الماسح",
        "safe": "✅ المنتج آمن ومناسب!", "safe_sub": "هذا المنتج يطابق ملفك الشخصي تمامًا.",
        "warn": "🛑 غير مناسب!", "not_found": "⚠️ لم يتم العثور على المنتج.",
        "lang_select": "اختر اللغة:", "saved_msg": "✅ تم الحفظ!", "team_title": "👥 فريق التطوير",
        "w_laktose": "🥛 يحتوي على اللاكتوز", "w_fruktose": "🍎 يحتوي على الفركتوز", "w_histamin": "🍷 خطر الهيستامين", "w_sorbit": "🍬 يحتوي على السوربيتول",
        "w_sulfite": "🧪 يحتوي على الكبريتيت", "w_glutamat": "🍕 يحتوي على الغلوتامات", "w_gluten": "🌾 يحتوي على الغلوتين", "w_nuesse": "🌰 يحتوي على المكسرات", "w_soja": "🌱 يحتوي على الصويا", "w_erdnuesse": "🥜 يحتوي على الفول السوداني",
        "w_vegan": "🥩 ليس نباتيًا تامًا", "w_vegetarisch": "🥩 ليس نباتيًا", "w_halal": "☪️ غير متوافق مع الحلال", "w_koscher": "✡️ غير متوافق مع الكوشير",
        "placeholder": "أدخل الباركود...", "hist_title": "🕒 السجل", "details": "🔬 المكونات والتحليل",
        "nutri_title": "🥗 الجودة الغذائية", "cal_title": "🔥 السعرات", "cal_slider": "السعرات المستهدفة:",
        "cal_percentage": "يستهلك **{:.1f}%** لكل 100 جرام.", "de_ingredients": "🇩🇪 المكونات:"
    },
    "简体中文": {
        "t1": "👤 个人档案", "t2": "📸 扫描仪", "t3": "⚙️ 设置", "t4": "ℹ️ 信息",
        "title": "我的防护档案", "sub": "配置您的过敏源和饮食偏好", "save": "保存档案",
        "cat_allergy": "不耐受与过敏源", "cat_additives": "添加剂", "cat_lifestyle": "生活方式与宗教",
        "laktose": "乳糖 / 牛奶", "fruktose": "果糖", "histamin": "组胺", "sorbit": "山梨糖醇",
        "gluten": "麸质", "nuesse": "坚果", "soja": "大豆", "erdnuesse": "花生",
        "sulfite": "亚硫酸盐", "glutamat": "谷氨酸钠", "vegan": "纯素食", "vegetarisch": "蛋奶素食", "halal": "清真", "koscher": "犹太洁食",
        "scan_h": "扫描仪", "scan_p": "使用摄像头或手动输入条形码",
        "btn_cam_start": "📸 开启扫描", "btn_cam_stop": "🛑 关闭扫描",
        "safe": "✅ 产品安全！", "safe_sub": "该产品完全符合您的安全配置。",
        "warn": "🛑 不适用！", "not_found": "⚠️ 未找到该产品。",
        "lang_select": "选择语言:", "saved_msg": "✅ 保存成功！", "team_title": "👥 开发团队",
        "w_laktose": "🥛 含有乳糖", "w_fruktose": "🍎 含有果糖", "w_histamin": "🍷 存在组胺", "w_sorbit": "🍬 含有山梨糖醇",
        "w_sulfite": "🧪 含有亚硫酸盐", "w_glutamat": "🍕 含有谷氨酸钠", "w_gluten": "🌾 含有麸质", "w_nuesse": "🌰 含有坚果", "w_soja": "🌱 含有大豆", "w_erdnuesse": "🥜 含有花生",
        "w_vegan": "🥩 非纯素食", "w_vegetarisch": "🥩 非素食", "w_halal": "☪️ 不符合清真", "w_koscher": "✡️ 不符合犹太洁食",
        "placeholder": "输入条形码...", "hist_title": "🕒 历史", "details": "🔬 成分与分析",
        "nutri_title": "🥗 营养质量", "cal_title": "热量检查", "cal_slider": "每日目标热量:",
        "cal_percentage": "消耗每日目标的 **{:.1f}%**。", "de_ingredients": "🇩🇪 德语成分:"
    },
    "Русский": {
        "t1": "👤 Профиль", "t2": "📸 Сканер", "t3": "⚙️ Настройки", "t4": "ℹ️ Инфо",
        "title": "Мой профиль", "sub": "Настройте ваши аллергии", "save": "Сохранить",
        "cat_allergy": "Аллергены", "cat_additives": "Добавки", "cat_lifestyle": "Образ жизни",
        "laktose": "Лактоза / Молоко", "fruktose": "Фруктоза", "histamin": "Гистамин", "sorbit": "Сорбит",
        "gluten": "Глютен", "nuesse": "Орехи", "soja": "Соя", "erdnuesse": "Арахис",
        "sulfite": "Сульфиты", "glutamat": "Глутамат", "vegan": "Веган", "vegetarisch": "Вегетарианец", "halal": "Халяль", "koscher": "Кошерно",
        "scan_h": "Сканер", "scan_p": "Используйте камеру или введите штрихкод",
        "btn_cam_start": "📸 Запустить сканер", "btn_cam_stop": "🛑 Остановить сканер",
        "safe": "✅ ПРОДУКТ БЕЗОПАСЕН!", "safe_sub": "Полностью соответствует профилю.",
        "warn": "🛑 НЕ ПОДХОДИТ!", "not_found": "⚠️ Продукт не найден.",
        "lang_select": "Выберите язык:", "saved_msg": "✅ Профиль сохранен!", "team_title": "👥 Разработчики",
        "w_laktose": "🥛 Содержит лактозу", "w_fruktose": "🍎 Содержит фруктозу", "w_histamin": "🍷 Риск гистамина", "w_sorbit": "🍬 Содержит сорбит",
        "w_sulfite": "🧪 Содержит сульфиты", "w_glutamat": "🍕 Содержит глутамат", "w_gluten": "🌾 Содержит глютен", "w_nuesse": "🌰 Содержит орехи", "w_soja": "🌱 Содержит сою", "w_erdnuesse": "🥜 Содержит арахис",
        "w_vegan": "🥩 Не веганский", "w_vegetarisch": "🥩 Не вегетарианский", "w_halal": "☪️ Не халяльно", "w_koscher": "✡️ Не кошерно",
        "placeholder": "Штрихкод...", "記録": "🕒 기록", "details": "🔬 성분",
        "nutri_title": "🥗 Питательность", "cal_title": "🔥 Калории", "cal_slider": "Суточная норма (ккал):",
        "cal_percentage": "Расходует **{:.1f}%** суточной нормы.", "de_ingredients": "🇩🇪 Ингредиенты:"
    },
    "Polski": {
        "t1": "👤 Profil", "t2": "📸 Skaner", "t3": "⚙️ Ustawienia", "t4": "ℹ️ Info",
        "title": "Mój Profil", "sub": "Skonfiguruj swoje algerie", "save": "Zapisz",
        "cat_allergy": "Alergeny", "cat_additives": "Dodatki", "cat_lifestyle": "Styl życia",
        "laktose": "Laktoza / Mleko", "fruktose": "Fruktoza", "histamin": "Histamina", "sorbit": "Sorbitol",
        "gluten": "Gluten", "nuesse": "Orzechy", "soja": "Soja", "erdnuesse": "Orzeszki ziemne",
        "sulfite": "Siarczyny", "glutamat": "Glutaminian", "vegan": "Weganin", "vegetarisch": "Wegetarianin", "halal": "Halal", "koscher": "Koszerny",
        "scan_h": "Skaner", "scan_p": "Użyj aparatu",
        "btn_cam_start": "📸 Uruchom skaner", "btn_cam_stop": "🛑 Zatrzymaj",
        "safe": "✅ BEZPIECZNY!", "safe_sub": "Produkt zgodny z profilem.",
        "warn": "🛑 NIEODPOWIEDNI!", "not_found": "⚠️ Nie znaleziono produktu.",
        "lang_select": "Wybierz język:", "saved_msg": "✅ Zapisano!", "team_title": "👥 Zespół",
        "w_laktose": "🥛 Zawiera laktozę", "w_fruktose": "🍎 Zawiera fruktozę", "w_histamin": "🍷 Ryzyko histaminy", "w_sorbit": "🍬 Zawiera sorbitol",
        "w_sulfite": "🧪 Zawiera siarczyny", "w_glutamat": "🍕 Zawiera glutaminian", "w_gluten": "🌾 Zawiera gluten", "w_nuesse": "🌰 Zawiera orzechy", "w_soja": "🌱 Zawiera soję", "w_erdnuesse": "🥜 Zawiera orzeszki ziemne",
        "w_vegan": "🥩 Nie dla wegan", "w_vegetarisch": "🥩 Nie wegetariański", "w_halal": "☪️ Nie Halal", "w_koscher": "✡️ Nie Koszer",
        "placeholder": "Kod kreskowy...", "hist_title": "🕒 Skany", "details": "🔬 Składniki",
        "nutri_title": "🥗 Jakość odżywcza", "cal_title": "🔥 Kalorie", "cal_slider": "Dzienne zapotrzebowanie (kcal):",
        "cal_percentage": "Zużywa **{:.1f}%** dziennego limitu.", "de_ingredients": "🇩🇪 Niemiecka lista składników:"
    },
    "Français": {
        "t1": "👤 Profil", "t2": "📸 Scanner", "t3": "⚙️ Réglages", "t4": "ℹ️ Info",
        "title": "Mon Profil", "sub": "Configurez vos allergies", "save": "Enregistrer",
        "cat_allergy": "Allergènes", "cat_additives": "Additifs", "cat_lifestyle": "Style de vie",
        "laktose": "Lactose / Lait", "fruktose": "Fructose", "histamin": "Histamine", "sorbit": "Sorbitol",
        "gluten": "Gluten", "nuesse": "Fruits à coque", "soja": "Soja", "erdnuesse": "Arachides",
        "sulfite": "Sulfites", "glutamat": "Glamate", "vegan": "Végétalien", "vegetarisch": "Végétarien", "halal": "Halal", "koscher": "Cascher",
        "scan_h": "Scanner", "scan_p": "Utilisez l'appareil photo",
        "btn_cam_start": "📸 Activer le scanner", "btn_cam_stop": "🛑 Arrêter",
        "safe": "✅ SÛR !", "safe_sub": "Correspond à votre profil.",
        "warn": "🛑 NON COMPATIBLE !", "not_found": "⚠️ Produit non trouvé.",
        "lang_select": "Langue :", "saved_msg": "✅ Enregistré !", "team_title": "👥 Équipe",
        "w_laktose": "🥛 Contient du lactose", "w_fruktose": "🍎 Contient du fructose", "w_histamin": "🍷 Risque histamine", "w_sorbit": "🍬 Contient du sorbitol",
        "w_sulfite": "🧪 Contient des sulfites", "w_glutamat": "🍕 Contient du glutamate", "w_gluten": "🌾 Contient du gluten", "w_nuesse": "🌰 Contient des fruits à coque", "w_soja": "🌱 Contient du soja", "w_erdnuesse": "🥜 Contient des arachides",
        "w_vegan": "🥩 Non Végétalien", "w_vegetarisch": "🥩 Non Végétarien", "w_halal": "☪️ Non Halal", "w_koscher": "✡️ Non Cascher",
        "placeholder": "Code-barres...", "hist_title": "🕒 Historique", "details": "🔬 Ingrédients",
        "nutri_title": "🥗 Nutri-Score", "cal_title": "🔥 Calories", "cal_slider": "Objectif (kcal) :",
        "cal_percentage": "Consomme **{:.1f}%** de votre budget.", "de_ingredients": "🇩🇪 Ingrédients :"
    },
    "Español": {
        "t1": "👤 Perfil", "t2": "📸 Escáner", "t3": "⚙️ Ajustes", "t4": "ℹ️ Info",
        "title": "Mi Perfil", "sub": "Configura tus allergies", "save": "Guardar",
        "cat_allergy": "Alérgenos", "cat_additives": "Aditivos", "cat_lifestyle": "Estilo de vida",
        "laktose": "Lactosa / Leche", "fruktose": "Fructosa", "histamin": "Histamina", "sorbit": "Sorbitol",
        "gluten": "Gluten", "nuesse": "Frutos secos", "soja": "Soja", "erdnuesse": "Cacahuetes",
        "sulfite": "Sulfitos", "glutamat": "Glutamato", "vegan": "Vegano", "vegetarisch": "Vegetariano", "halal": "Halal", "koscher": "Kosher",
        "scan_h": "Escáner", "scan_p": "Usa la cámara",
        "btn_cam_start": "📸 Iniciar Escáner", "btn_cam_stop": "🛑 Detener",
        "safe": "✅ ¡APTO!", "safe_sub": "Cumple con tu perfil.",
        "warn": "🛑 ¡NO COMPATIBLE!", "not_found": "⚠️ Producto no encontrado.",
        "lang_select": "Idioma:", "saved_msg": "✅ ¡Guardado!", "team_title": "👥 Equipo",
        "w_laktose": "🥛 Contiene lactosa", "w_fruktose": "🍎 Contiene fructosa", "w_histamin": "🍷 Riesgo de histamina", "w_sorbit": "🍬 Contiene sorbitol",
        "w_sulfite": "🧪 Contiene sulfitos", "w_glutamat": "🍕 Contiene glutamato", "w_gluten": "🌾 Contiene gluten", "w_nuesse": "🌰 Contiene frutos secos", "w_soja": "🌱 Contiene soja", "w_erdnuesse": "🥜 Contiene cacahuetes",
        "w_vegan": "🥩 No Vegano", "w_vegetarisch": "🥩 No Vegetariano", "w_halal": "☪️ No Halal", "w_koscher": "✡️ No Kosher",
        "placeholder": "Código...", "hist_title": "🕒 Historial", "details": "🔬 Ingredientes",
        "nutri_title": "🥗 Nutrición", "cal_title": "🔥 Calorías", "cal_slider": "Pauta diaria (kcal):",
        "cal_percentage": "Consume el **{:.1f}%** de tu presupuesto.", "de_ingredients": "🇩🇪 Ingredientes:"
    },
    "Português": {
        "t1": "👤 Perfil", "t2": "📸 Scanner", "t3": "⚙️ Definições", "t4": "ℹ️ Info",
        "title": "Meu Perfil", "sub": "Configure as suas allergies", "save": "Salvar",
        "cat_allergy": "Alérgenos", "cat_additives": "Aditivos", "cat_lifestyle": "Estilo de vida",
        "laktose": "Lactose / Leite", "fruktose": "Frutose", "histamin": "Histamina", "sorbit": "Sorbitol",
        "gluten": "Glúten", "nuesse": "Nozes", "soja": "Soja", "erdnuesse": "Amendoins",
        "sulfite": "Sulfitos", "glutamat": "Glutamato", "vegan": "Vegano", "vegetarisch": "Vegetariano", "halal": "Halal", "koscher": "Kosher",
        "scan_h": "Scanner", "scan_p": "Use a câmara",
        "btn_cam_start": "📸 Iniciar Scanner", "btn_cam_stop": "🛑 Parar",
        "safe": "✅ SEGURO!", "safe_sub": "Conformidade com o perfil.",
        "warn": "🛑 NÃO COMPATÍVEL!", "not_found": "⚠️ Produto não encontrado.",
        "lang_select": "Idioma:", "saved_msg": "✅ Salvo com sucesso!", "team_title": "👥 Equipa",
        "w_laktose": "🥛 Contém lactose", "w_fruktose": "🍎 Contém frutose", "w_histamin": "🍷 Risco de histamina", "w_sorbit": "🍬 Contém sorbitol",
        "w_sulfite": "🧪 Contém sulfitos", "w_glutamat": "🍕 Contém glutamato", "w_gluten": "🌾 Contém glúten", "w_nuesse": "🌰 Contém nozes", "w_soja": "🌱 Contém soja", "w_erdnuesse": "🥜 Contém amendoins",
        "w_vegan": "🥩 Não Vegano", "w_vegetarisch": "🥩 Não Vegetariano", "w_halal": "☪️ Não Halal", "w_koscher": "✡️ Não Kosher",
        "placeholder": "Código...", "hist_title": "🕒 Histórico", "details": "🔬 Ingredientes",
        "nutri_title": "🥗 Nutrição", "cal_title": "🔥 Calorias", "cal_slider": "Meta calórica (kcal):",
        "cal_percentage": "Consome **{:.1f}%** do seu orçamento.", "de_ingredients": "🇩🇪 Ingrédients:"
    },
    "ไทย": {
        "t1": "👤 โปรไฟล์", "t2": "📸 สแกนเนอร์", "t3": "⚙️ ตั้งค่า", "t4": "ℹ️ ข้อมูล",
        "title": "โปรไฟล์ของฉัน", "sub": "ตั้งค่าการแพ้อาหาร", "save": "บันทึก",
        "cat_allergy": "สารก่อภูมิแพ้", "cat_additives": "สารเจือปน", "cat_lifestyle": "ไลฟ์สไตล์",
        "laktose": "แลคโตส / นม", "fruktose": "ฟรุกโตส", "histamin": "ฮิสตามีน", "sorbit": "ซอร์บิทอล",
        "gluten": "กลูเตน", "nuesse": "ถั่ว", "soja": "ถั่วเหลือง", "erdnuesse": "ถั่วลิสง",
        "sulfite": "ซัลไฟต์", "glutamat": "ผงชูรส", "vegan": "วีแกน", "vegetarisch": "มังสวิรัติ", "halal": "ฮาลาล", "koscher": "โคเชอร์",
        "scan_h": "เครื่องสแกน", "scan_p": "ใช้กล้อง",
        "btn_cam_start": "📸 เริ่มสแกน", "btn_cam_stop": "🛑 หยุด",
        "safe": "✅ ปลอดภัย!", "safe_sub": "ตรงกับโปรไฟล์ของคุณ",
        "warn": "🛑 ไม่ปลอดภัย!", "not_found": "⚠️ ไม่พบสินค้า",
        "lang_select": "เลือกภาษา:", "saved_msg": "✅ บันทึกสำเร็จ!", "team_title": "👥 ทีมพัฒนา",
        "w_laktose": "🥛 มีแลคโตส", "w_fruktose": "🍎 มีฟรุกโตส", "w_histamin": "🍷 เสี่ยงฮิสตามีน", "w_sorbit": "🍬 มีซอร์บิทอล",
        "w_sulfite": "🧪 มีซัลไฟต์", "w_glutamat": "🍕 มีผงชูรส", "w_gluten": "🌾 มีกลูเตน", "w_nuesse": "🌰 มีถั่ว", "w_soja": "🌱 มีถั่วเหลือง", "w_erdnuesse": "🥜 มีถั่วลิสง",
        "w_vegan": "🥩 ไม่ใช่วีแกน", "w_vegetarisch": "🥩 ไม่ใช่มังสวิรัติ", "w_halal": "☪️ ไม่ฮาลาล", "w_koscher": "✡️ ไม่โคเชอร์",
        "placeholder": "บาร์โค้ด...", "hist_title": "🕒 ประวัติ", "details": "🔬 ส่วนผสม",
        "nutri_title": "🥗 โภชนาการ", "cal_title": "🔥 แคลอรี่", "cal_slider": "เป้าหมาย (kcal):",
        "cal_percentage": "ใช้ **{:.1f}%** ของเป้าหมายรายวัน", "de_ingredients": "🇩🇪 ส่วนผสมภาษาเยอรมัน:"
    },
    "한국어": {
        "t1": "👤 프로필", "t2": "📸 스캐너", "t3": "⚙️ 설정", "t4": "ℹ️ 정보",
        "title": "내 프로필", "sub": "알레르기 설정", "save": "저장",
        "cat_allergy": "알레르기 유발 물질", "cat_additives": "첨가물", "cat_lifestyle": "라이프스타일",
        "laktose": "유당 / 우유", "fruktose": "과당", "histamin": "히스타민", "sorbit": "소르비톨",
        "gluten": "글루텐", "nuesse": "견과류", "soja": "대두", "erdnuesse": "땅콩",
        "sulfite": "아황산염", "glutamat": "글루타민산염", "vegan": "비건", "vegetarisch": "채식주의자", "halal": "할랄", "koscher": "코셔",
        "scan_h": "스캐너", "scan_p": "카메라를 사용하세요",
        "btn_cam_start": "📸 스캐너 시작", "btn_cam_stop": "🛑 중지",
        "safe": "✅ 안전!", "safe_sub": "프로필과 일치합니다.",
        "warn": "🛑 적합하지 않음!", "not_found": "⚠️ 제품 없음.",
        "lang_select": "언어:", "saved_msg": "✅ 저장됨!", "team_title": "👥 개발 팀",
        "w_laktose": "🥛 유당 포함", "w_fruktose": "🍎 과당 포함", "w_histamin": "🍷 히스타민 위험", "w_sorbit": "🍬 소르비톨 포함",
        "w_sulfite": "🧪 아황산염 포함", "w_glutamat": "🍕 글루타민 포함", "w_gluten": "🌾 글루텐 포함", "w_nuesse": "🌰 견과류 포함", "w_soja": "🌱 대두 포함", "w_erdnuesse": "🥜 땅콩 포함",
        "w_vegan": "🥩 비건 아님", "w_vegetarisch": "🥩 채식 아님", "w_halal": "☪️ 할랄 아님", "w_koscher": "✡️ 코셔 아님",
        "placeholder": "바코드...", "記録": "🕒 기록", "details": "🔬 성분",
        "nutri_title": "🥗 영양", "cal_title": "🔥 칼로리", "cal_slider": "하루 목표 (kcal):",
        "cal_percentage": "하루 목표의 **{:.1f}%** 소비.", "de_ingredients": "🇩🇪 독일어 성분:"
    }
}

t = ui.get(st.session_state.lang, ui["Deutsch"])

INGREDIENTS_DICT = {
    "sugar": "Zucker", "palm oil": "Palmöl", "hazelnuts": "Haselnüsse", "skimmed milk powder": "Magermilchpulver",
    "fat-reduced cocoa": "fettarmer Kakao", "emulsifier": "Emulgator", "lecithins": "Lecithine", "soya": "Soja",
    "vanillin": "Vanillin", "water": "Wasser", "carbon dioxide": "Kohlensäure", "colour": "Farbstoff",
    "acid": "Säuerungsmittel", "phosphoric acid": "Phosphorsäure", "natural flavouring": "natürliches Aroma",
    "flavouring caffeine": "Aroma Koffein", "tartaric acid": "Weinsäure", "sodium hydrogen carbonate": "Natriumhydrogencarbonat",
    "sweeteners": "Süßungsmittel", "sodium cyclamate": "Natriumcyclamat", "acesulfame k": "Acesulfam-K",
    "sodium saccharin": "Saccharin-Natrium", "flavourings": "Aromen", "carotenes": "Karotine", "wheat flour": "Weizenmehl",
    "vegetable fats": "pflanzliche Fette", "shea": "Shea", "whole wheat flour": "Vollkornweizenmehl",
    "butterfat": "Buttereinfett", "wheat starch": "Weizenstärke", "whey product": "Molkenerzeugnis",
    "milk": "Milch", "salt": "Salz", "glucose syrup": "Glukosesirup", "barley malt extract": "Gerstenmalzextrakt",
    "cocoa butter": "Kakaobutter", "cocoa mass": "Kakaomasse", "whole milk powder": "Vollmilchpowler",
    "lactose": "Laktose", "whey powder": "Molkenpowder", "egg white": "Eiweiß", "yolk": "Eigelb",
    "preservative": "Konservierungsstoff", "citric acid": "Zitronensäure", "ascorbic acid": "Ascorbinsäure",
    "thickener": "Verdickungsmittel", "xanthan gum": "Xanthan", "pectin": "Pektin", "yeast": "Hefe",
    "gelatin": "Gelatine", "peanuts": "Erdnüsse", "almonds": "Mandeln", "walnuts": "Walnüsse",
    "cashews": "Cashewnüsse", "pecan nuts": "Pekannüsse", "brazil nuts": "Paranüsse", "pistachio nuts": "Pistazien",
    "macadamia nuts": "Macadamianüsse", "celery": "Sellerie", "mustard": "Senf", "sesame seeds": "Sesamsamen",
    "sulphur dioxide": "Schwefeldioxid", "sulphites": "Sulfite", "lupin": "Lupine", "molluscs": "Weichtiere",
    "fish": "Fisch", "crustaceans": "Krebstiere", "oats": "Hafer", "rye": "Roggen", "barley": "Gerste",
    "spelt": "Dinkel", "kamut": "Kamut", "apple extract": "Apfelextrakt", "cinnamon": "Zimt",
    "coriander": "Koriander", "cumin": "Kreuzkümmel", "garlic": "Knoblauch", "onion": "Zwiebel",
    "paprika": "Paprika", "tomato": "Tomate", "vinegar": "Essig", "honey": "Honig",
    "maple syrup": "Ahornsirup", "agave syrup": "Agavendicksaft", "coconut oil": "Kokosöl",
    "sunflower oil": "Sonnenblumenöl", "olive oil": "Olivenöl", "rapeseed oil": "Rapsöl",
    "corn": "Mais", "potato starch": "Kartoffelstärke", "rice": "Reis", "baking powder": "Backpulver",
    "carrageenan": "Carrageen", "guar gum": "Guarkernmehl", "locust bean gum": "Johannisbrotkernmehl",
    "agar": "Agar-Agar", "monosodium glutamate": "Mononatriumglutamat", "e621": "E621 (Glutamat)",
    "potassium sorbate": "Kaliumsorbat", "sodium benzoate": "Natriumbenzoat", "calcium propionate": "Calciumpropionat",
    "lactic acid": "Milchsäure", "malic acid": "Äpfelsäure", "tartrazine": "Tartrazin",
    "sunset yellow": "Gelborange S", "allura red": "Allurarot AC", "brilliant blue": "Brillantblau FCF"
}

def translate_ingredients_to_de(text):
    if not text:
        return "Keine Zutatenangaben im System hinterlegt."
    text_lower = text.lower()
    for eng, de in INGREDIENTS_DICT.items():
        text_lower = text_lower.replace(eng, de)
    return text_lower.capitalize()



tab_profil, tab_scanner, tab_settings, tab_info = st.tabs([t["t1"], t["t2"], t["t3"], t["t4"]])

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

with tab_scanner:
    st.markdown(f"<h2>{t['scan_h']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['scan_p']}</p>", unsafe_allow_html=True)
    
    daily_cal_budget = 2000
    if st.session_state.ad_free:
        with st.container(border=True):
            st.markdown(f"<h5>{t['cal_title']}</h5>", unsafe_allow_html=True)
            daily_cal_budget = st.slider(t["cal_slider"], min_value=1200, max_value=4000, value=2000, step=50)

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
                components.html("""
<style>
#reader { width: 100%; border-radius: 20px; overflow: hidden; position: relative; background-color: #000; }
#reader video { object-fit: cover !important; border-radius: 20px; }
.scanner-laser { position: absolute; left: 10%; width: 80%; height: 2px; background-color: #EF4444; box-shadow: 0 0 10px #EF4444; animation: scanning 2s infinite ease-in-out; z-index: 100; pointer-events: none; }
@keyframes scanning { 0% { top: 20%; } 50% { top: 80%; } 100% { top: 20%; } }
#success-overlay { display: none; text-align: center; padding: 30px 15px; background: #E0E7FF; border-radius: 20px; margin-top: 10px; animation: fadeIn 0.3s ease-in; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
</style>

<div id="reader-container">
    <div id="reader" style="position: relative;">
        <div class="scanner-laser"></div>
    </div>
</div>

<div id="success-overlay">
    <div style="font-size: 50px; margin-bottom: 10px;">🔄</div>
    <h3 style="color:#111827; margin:0; font-family:-apple-system, sans-serif;">PRODUKT WIRD ANALYSIERT...</h3>
    <p id="barcode-display" style="font-size: 26px; font-weight: 900; color: #4F46E5; margin: 10px 0; font-family: monospace;"></p>
</div>

<script src="https://unpkg.com/html5-qrcode"></script>
<script>
let finalCode = "";

function startScanner() {
    const html5QrCode = new Html5Qrcode("reader");
    const config = { fps: 15, qrbox: { width: 280, height: 160 } };

    html5QrCode.start(
        { facingMode: "environment" },
        config,
        (decodedText) => {
            finalCode = decodedText.replace(/[^0-9]/g, '');
            
            html5QrCode.stop().then(() => {
                document.getElementById('reader-container').style.display = 'none';
                document.getElementById('success-overlay').style.display = 'block';
                document.getElementById('barcode-display').innerText = finalCode;
                
                const parentDoc = window.parent.document;
                const stInputs = parentDoc.querySelectorAll('input[type="text"]');
                let targetInput = null;
                
                stInputs.forEach(input => {
                    if (input.getAttribute('aria-label') === 'Barcode Entry' || 
                        input.placeholder.includes('Barcode') || 
                        input.placeholder.includes('barcode')) {
                        targetInput = input;
                    }
                });

                if (targetInput) {
                    targetInput.focus();
                    
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(targetInput, finalCode);
                    
                    targetInput.dispatchEvent(new Event('input', { bubbles: true }));
                    targetInput.dispatchEvent(new Event('change', { bubbles: true }));
                    
                    const enterEvent = new KeyboardEvent('keydown', { 
                        bubbles: true, 
                        cancelable: true, 
                        keyCode: 13, 
                        which: 13, 
                        key: 'Enter', 
                        code: 'Enter' 
                    });
                    targetInput.dispatchEvent(enterEvent);
                    
                    setTimeout(() => {
                        targetInput.blur();
                    }, 50);
                } else {
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set("scanned_barcode", finalCode);
                    window.parent.location.assign(url.href);
                }
            });
        },
        (errorMessage) => { }
    ).catch(err => {
        document.getElementById('reader').innerHTML = "<p style='color:white; padding:20px;'>Kamerazugriff verweigert oder nicht verfügbar. Bitte im Browser erlauben.</p>";
    });
}
setTimeout(startScanner, 400);
</script>
""", height=380)
    else:
        st.session_state.cam_on = False

    if barcode_input:
        barcode = "".join(filter(str.isdigit, str(barcode_input)))
        
        if len(barcode) >= 8:
            with st.spinner("🔍 Produktdaten werden analysiert..."):
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
                    p_name = product.get('product_name', 'Unbekanntes Produkt')
                    
                    if {"name": p_name, "code": barcode} not in st.session_state.history:
                        st.session_state.history.insert(0, {"name": p_name, "code": barcode})
                        if len(st.session_state.history) > 4: st.session_state.history.pop()
                    
                    tags_text = " ".join(product.get("allergens_tags", [])) + " " + " ".join(product.get("ingredients_analysis_tags", [])) + " " + " ".join(product.get("labels_tags", []))
                    raw_ingredients = str(product.get("ingredients_text", "")) or str(product.get("ingredients_text_de", "")) or str(product.get("ingredients_text_en", ""))
                    all_text = (raw_ingredients + " " + str(product.get("ingredients_text_en", "")) + " " + str(product.get("ingredients_text_fr", "")) + " " + str(product.get("ingredients_text_de", "")) + " " + tags_text).lower()
                    
                    warnings = []
                    p = st.session_state.profile
                    
                    if p["laktose"] and any(w in all_text for w in ["milch", "milk", "lait", "lactose", "laktose", "molke", "sahne", "butter", "en:milk"]): warnings.append(t["w_laktose"])
                    if p["fruktose"] and any(w in all_text for w in ["fructose", "fruktose", "fruchtzucker", "sirup"]): warnings.append(t["w_fruktose"])
                    if p["histamin"] and any(w in all_text for w in ["histamin", "hefe", "yeast", "wein", "tomate", "schokolade", "kakao"]): warnings.append(t["w_histamin"])
                    if p["sorbit"] and any(w in all_text for w in ["sorbit", "sorbitol", "e420"]): warnings.append(t["w_sorbit"])
                    if p["gluten"] and any(w in all_text for w in ["gluten", "weizen", "wheat", "blé", "gerste", "barley", "roggen", "rye", "hafer", "oats", "en:gluten"]): warnings.append(t["w_gluten"])
                    if p["nuesse"] and any(w in all_text for w in ["nuss", "nüsse", "nuts", "amande", "noix", "haselnuss", "walnuss", "cashew", "mandel", "en:nuts"]): warnings.append(t["w_nuesse"])
                    if p["soja"] and any(w in all_text for w in ["soja", "soy", "soya", "lecithine (soja)", "en:soybeans"]): warnings.append(t["w_soja"])
                    if p["erdnuesse"] and any(w in all_text for w in ["erdnuss", "erdnüsse", "peanut", "peanuts", "cacahuète", "en:peanuts"]): warnings.append(t["w_erdnuesse"])
                    if p["sulfite"] and any(w in all_text for w in ["sulfit", "sulfite", "schwefeldioxid", "e220", "en:sulphites"]): warnings.append(t["w_sulfite"])
                    if p["glutamat"] and any(w in all_text for w in ["glutamat", "glutamate", "hefeextrakt", "e621"]): warnings.append(t["w_glutamat"])
                    if p["vegan"] and any(w in all_text for w in ["milch", "milk", "lait", "ei ", "egg", "oeuf", "fleisch", "meat", "viande", "honig", "honey", "miel", "gelatine", "en:non-vegetarian", "en:non-vegan"]): warnings.append(t["w_vegan"])
                    if p["vegetarisch"] and any(w in all_text for w in ["fleisch", "meat", "viande", "fisch", "fish", "poisson", "gelatine", "en:non-vegetarian"]): warnings.append(t["w_vegetarisch"])
                    if p["halal"] and any(w in all_text for w in ["schwein", "pork", "porc", "alkohol", "alcohol"]): warnings.append(t["w_halal"])
                    if p["koscher"] and any(w in all_text for w in ["schwein", "pork", "porc", "schalentiere", "shrimp"]): warnings.append(t["w_koscher"])
                        
                    st.write("")
                    col_left, col_right = st.columns([1.3, 1], gap="medium")
                    
                    with col_left:
                        st.markdown(f"<h3>{p_name}</h3>", unsafe_allow_html=True)
                        if warnings:
                            st.markdown(f"""<div class="result-box-warn"><h3 style="color:#991B1B; margin:0;">{t['warn']}</h3><p style="text-align:left; color:#991B1B; margin-top:10px; margin-bottom:0; font-weight:600;">{"<br>".join(["• " + w for w in warnings])}</p></div>""", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""<div class="result-box-safe"><h3 style="color:#065F46; margin:0;">{t['safe']}</h3><p style="text-align:left; color:#065F46; margin-top:10px; margin-bottom:0; font-weight:600;">{t['safe_sub']}</p></div>""", unsafe_allow_html=True)
                            throw_confetti()
                            
                    with col_right:
                        if product.get("image_front_url"):
                            st.markdown("<div style='display: flex; justify-content: center; align-items: center; max-height: 220px; overflow:hidden; border-radius:15px;'>", unsafe_allow_html=True)
                            st.image(product["image_front_url"], use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.write("")
                    st.markdown(f"### {t['nutri_title']}")
                    ns_grade = str(product.get("nutriscore_grade", "unknown")).lower()
                    if ns_grade in ["a", "b", "c", "d", "e"]:
                        st.markdown(f"<span class='nutri-badge nutri-{ns_grade}'>Nutri-Score {ns_grade.upper()}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='nutri-badge nutri-unknown'>Nutri-Score Unbekannt</span>", unsafe_allow_html=True)
                    
                    if st.session_state.ad_free:
                        nutriments = product.get("nutriments", {})
                        kcal_100g = nutriments.get("energy-kcal_100g", nutriments.get("energy-kcal", 0))
                        
                        if kcal_100g:
                            pct_of_daily = (float(kcal_100g) / daily_cal_budget) * 100
                            st.metric(label=f"{t['cal_title']} (pro 100g)", value=f"{kcal_100g} kcal")
                            st.info(t["cal_percentage"].format(pct_of_daily))
                    
                    st.write("")
                    with st.expander(t["details"]):
                        if is_offline: st.caption("ℹ️ Offline-Testdatenbank aktiv.")
                        st.write(f"**Original Zutaten:** {raw_ingredients if raw_ingredients else 'Keine Angaben verfügbar.'}")
                        
                        de_translated = translate_ingredients_to_de(raw_ingredients)
                        st.write(f"**{t['de_ingredients']}** {de_translated}")
                else:
                    st.error(t["not_found"])

    
    if st.session_state.history:
        st.write("")
        st.markdown(f"<h3>🕒 {t['hist_title']}</h3>", unsafe_allow_html=True)
        for item in st.session_state.history:
            if st.button(f"▫️ {item['name']} ({item['code']})", key=f"hist_{item['code']}", help="Erneut prüfen"):
                st.session_state.manual_code = item['code']
                st.rerun()


with tab_settings:
    st.markdown(f"<h2>{t['t3']}</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h4>🌐 {t['lang_select']}</h4>", unsafe_allow_html=True)
        lang_list = ["Deutsch", "English", "日本語", "العربية", "简体中文", "Русский", "Polski", "Français", "Español", "Português", "ไทย", "한국어"]
        new_lang = st.selectbox("Language Selection", lang_list, index=lang_list.index(st.session_state.lang), label_visibility="collapsed")
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()
            

    with st.container(border=True):
        st.markdown(f"<h4>🚫 Werbefreie Version</h4>", unsafe_allow_html=True)
        if not st.session_state.ad_free:
            st.write("Werbefreie Version kaufen?")
            st.write(":blue[ad-free.com]")
            st.markdown("""
                <div style="text-align: center; margin: 15px 0;">
                    <span style="text-decoration: line-through; color: #9CA3AF; font-size: 18px; margin-right: 12px; font-weight: 500;">7 €</span>
                    <span style="color: #10B981; font-size: 28px; font-weight: 800; background-color: #E6F4EA; padding: 6px 16px; border-radius: 14px; border: 1px solid #A7F3D0; display: inline-block;">3,99 €</span>
                    <p style="color: #6B7280; font-size: 13px; margin-top: 8px; font-weight: 500; text-align: center;">monatlich</p>
                </div>
            """, unsafe_allow_html=True)
            promo_code = st.text_input("Aktivierungscode", placeholder="Code eingeben", type="password", label_visibility="collapsed")
            if promo_code:
                if promo_code.strip().upper() == "FREE":
                    st.session_state.ad_free = True
                    st.success("✅ Werbefreie Version erfolgreich aktiviert!")
                    time.sleep(1) 
                    st.rerun()
                else:
                    st.error("❌ Ungültiger Code.")
        else:
            st.success("✨ Du nutzt bereits die werbefreie Pro-Version. Danke!")

with tab_info:
    with st.container(border=True):
        st.markdown(f"<h2>{t['team_title']}</h2>", unsafe_allow_html=True)
        st.divider()
        st.write("👨‍💻 **Marius Boulos**")
        st.write("👨‍💻 **Benjamin Mehling**")
        st.write("👩‍💻 **Sophie Hartwig**")
        st.write("👨‍💻 **Ben Henkel**")
        st.write("👨‍💻 **Maximilian Mayr**")
        st.caption("Hösbach / Germany")
        st.write(" ")
        st.write("Contact: safescanning@gmail.com")
        st.write("powered by https://de.openfoodfacts.org")
        st.write("All rights reserved")


if not st.session_state.ad_free:
    st.markdown("<div class='ad-spacer'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="ad-banner">
            ✨ HIER KÖNNTE IHRE WERBUNG STEHEN ✨
        </div>
        <div class="ad-left-banner">
            ✨ WERBUNG ✨
        </div>
    """, unsafe_allow_html=True)
