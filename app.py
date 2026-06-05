# ==========================================
# IMPORTS
# ==========================================

import streamlit as st
import requests
import streamlit.components.v1 as components

# ==========================================
# 0. SCANNER CALLBACK & PARAMS INTERCEPT
# ==========================================

if "scanned_barcode" in st.query_params:

    scanned = st.query_params["scanned_barcode"]

    if scanned:
        st.session_state.manual_code = scanned
        st.query_params.clear()
        st.rerun()

# ==========================================
# 1. SETUP & ULTRA CLEAN UI DESIGN
# ==========================================

st.set_page_config(
    page_title="AllergyShield Pro",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""

<style>

.stApp {
    background-color: #F8F9FA;
    color: #111827;
    font-family: 'SF Pro Display', -apple-system, sans-serif;
}

header {
    visibility: hidden;
}

/* Moderne Tabs */

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

/* Cards */

div[data-testid="stVerticalBlock"] > div[style*="border"] {
    background-color: white !important;
    border-radius: 24px !important;
    border: 1px solid #F3F4F6 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.02) !important;
    padding: 25px !important;
    margin-bottom: 15px;
}

/* Typography */

h1 {
    color: #111827 !important;
    text-align: center;
    font-weight: 800;
    font-size: 32px;
    margin-bottom: 5px;
}

h2 {
    color: #111827 !important;
    text-align: center;
    font-weight: 800;
    font-size: 26px;
}

h3 {
    color: #111827 !important;
    font-weight: 700;
    font-size: 22px;
}

h4 {
    color: #111827 !important;
    font-weight: 700;
    font-size: 16px;
}

p {
    text-align: center;
    color: #6B7280;
}

/* Buttons */

.stButton>button {
    background-color: #4F46E5 !important;
    color: white !important;
    border-radius: 20px !important;
    height: 50px !important;
    width: 100% !important;
    font-weight: 700 !important;
    border: none !important;
}

/* Result Box */

.result-box-safe {
    background-color: #ECFDF5;
    border: 4px solid #10B981;
    border-radius: 20px;
    padding: 20px;
    color: #065F46;
}

.result-box-warn {
    background-color: #FEF2F2;
    border: 4px solid #EF4444;
    border-radius: 20px;
    padding: 20px;
    color: #991B1B;
}

</style>

""", unsafe_allow_html=True)

# ==========================================
# 2. CONFETTI
# ==========================================

def throw_confetti():

    components.html(
        """

        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

        <script>

        confetti({
            particleCount: 180,
            spread: 90,
            origin: { y: 0.6 },
            colors: ['#4F46E5', '#10B981', '#F59E0B']
        });

        </script>

        """,
        height=0
    )

# ==========================================
# 3. SESSION STATE
# ==========================================

if 'lang' not in st.session_state:
    st.session_state.lang = "Deutsch"

if 'cam_on' not in st.session_state:
    st.session_state.cam_on = False

if 'history' not in st.session_state:
    st.session_state.history = []

if 'manual_code' not in st.session_state:
    st.session_state.manual_code = ""

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

# ==========================================
# 4. SPRACHEN
# ==========================================

ui = {

    "Deutsch": {

        "t1": "👤 Profil",
        "t2": "📸 Scanner",
        "t3": "⚙️ Einstellungen",
        "t4": "ℹ️ Info",

        "title": "Mein Schutzprofil",
        "sub": "Konfigurieren Sie Ihre Allergien und Unverträglichkeiten",
        "save": "Profil speichern",

        "scan_h": "Scanner",
        "scan_p": "Nutzen Sie die Kamera oder geben Sie den Code manuell ein",

        "btn_cam_start": "📸 Scanner starten",
        "btn_cam_stop": "🛑 Scanner stoppen",

        "safe": "✅ PRODUKT GEEIGNET!",
        "safe_sub": "Dieses Produkt entspricht deinem Schutzprofil.",

        "warn": "🛑 NICHT GEEIGNET!",
        "not_found": "⚠️ Produkt nicht gefunden.",

        "placeholder": "Barcode eintippen...",
        "hist_title": "🕒 Letzte Scans",

        "details": "🔬 Inhaltsstoffe & Analyse",

        "lang_select": "Sprache wählen:"
    },

    "English": {

        "t1": "👤 Profile",
        "t2": "📸 Scanner",
        "t3": "⚙️ Settings",
        "t4": "ℹ️ Info",

        "title": "My Profile",
        "sub": "Configure your allergies and preferences",
        "save": "Save Profile",

        "scan_h": "Scanner",
        "scan_p": "Use camera or enter barcode manually",

        "btn_cam_start": "📸 Start Scanner",
        "btn_cam_stop": "🛑 Stop Scanner",

        "safe": "✅ PRODUCT SAFE!",
        "safe_sub": "Matches your profile perfectly.",

        "warn": "🛑 NOT COMPATIBLE!",
        "not_found": "⚠️ Product not found.",

        "placeholder": "Enter barcode...",
        "hist_title": "🕒 History",

        "details": "🔬 Ingredients & Analysis",

        "lang_select": "Choose language:"
    }
}

t = ui.get(st.session_state.lang, ui["Deutsch"])

# ==========================================
# 5. OFFLINE DATA
# ==========================================

OFFLINE_DATA = {

    "3017620425035": {

        "product_name": "Nutella",

        "ingredients_text":
        "Zucker, Palmöl, Haselnüsse (13%), Magermilchpulver, Kakao.",

        "image_front_url":
        "https://world.openfoodfacts.org/images/products/301/762/042/5035/front_fr.465.400.jpg"
    }
}

# ==========================================
# 6. TABS
# ==========================================

tab_profil, tab_scanner, tab_settings, tab_info = st.tabs([
    t["t1"],
    t["t2"],
    t["t3"],
    t["t4"]
])

# ==========================================
# TAB 1 — PROFIL
# ==========================================

with tab_profil:

    st.markdown(
        f"<h1>🛡️<br>{t['title']}</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p>{t['sub']}</p>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.session_state.profile["laktose"] = st.toggle(
            "Laktose / Milch",
            value=st.session_state.profile["laktose"]
        )

        st.session_state.profile["gluten"] = st.toggle(
            "Gluten",
            value=st.session_state.profile["gluten"]
        )

        st.session_state.profile["soja"] = st.toggle(
            "Soja",
            value=st.session_state.profile["soja"]
        )

        st.session_state.profile["vegan"] = st.toggle(
            "Vegan",
            value=st.session_state.profile["vegan"]
        )

    if st.button(f"💾 {t['save']}"):
        st.success("✅ Gespeichert!")

# ==========================================
# TAB 2 — SCANNER
# ==========================================

with tab_scanner:

    st.markdown(
        f"<h2>{t['scan_h']}</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p>{t['scan_p']}</p>",
        unsafe_allow_html=True
    )

    barcode_input = st.text_input(
        "Barcode",
        value=st.session_state.manual_code,
        placeholder=t["placeholder"],
        label_visibility="collapsed"
    )

    # ======================================
    # CAMERA
    # ======================================

    if not barcode_input:

        if not st.session_state.cam_on:

            if st.button(t["btn_cam_start"]):

                st.session_state.cam_on = True
                st.rerun()

        else:

            if st.button(t["btn_cam_stop"]):

                st.session_state.cam_on = False
                st.rerun()

            # ==================================
            # REAL BARCODE SCANNER
            # ==================================

            components.html("""

            <div id="reader"
                 style="width:100%;
                        border-radius:20px;">
            </div>

            <script src="https://unpkg.com/html5-qrcode"></script>

            <script>

            function onScanSuccess(decodedText, decodedResult) {

                const currentUrl = new URL(window.location.href);

                currentUrl.searchParams.set(
                    "scanned_barcode",
                    decodedText
                );

                window.location.href = currentUrl.toString();
            }

            const html5QrcodeScanner =
                new Html5QrcodeScanner(
                    "reader",
                    {
                        fps: 10,
                        qrbox: {
                            width: 250,
                            height: 120
                        },
                        rememberLastUsedCamera: true
                    }
                );

            html5QrcodeScanner.render(onScanSuccess);

            </script>

            """, height=500)

    else:

        st.session_state.cam_on = False

    # ======================================
    # PRODUCT CHECK
    # ======================================

    if barcode_input:

        barcode = "".join(filter(str.isdigit, barcode_input))

        if len(barcode) >= 8:

            with st.spinner("🔍 Suche Produkt..."):

                product = None

                try:

                    headers = {
                        'User-Agent': 'AllergyShieldPro'
                    }

                    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=5
                    )

                    if response.status_code == 200:

                        data = response.json()

                        if data.get("status") == 1:
                            product = data["product"]

                except:
                    pass

                if not product and barcode in OFFLINE_DATA:
                    product = OFFLINE_DATA[barcode]

                # ==================================
                # PRODUCT FOUND
                # ==================================

                if product:

                    p_name = product.get(
                        "product_name",
                        "Unknown Product"
                    )

                    ingredients = str(
                        product.get(
                            "ingredients_text",
                            ""
                        )
                    ).lower()

                    warnings = []

                    p = st.session_state.profile

                    # ==================================
                    # ALLERGY CHECKS
                    # ==================================

                    if p["laktose"]:

                        if any(x in ingredients for x in [
                            "milch",
                            "milk",
                            "lactose",
                            "butter"
                        ]):

                            warnings.append(
                                "🥛 Enthält Milch/Laktose"
                            )

                    if p["gluten"]:

                        if any(x in ingredients for x in [
                            "gluten",
                            "weizen",
                            "wheat"
                        ]):

                            warnings.append(
                                "🌾 Enthält Gluten"
                            )

                    if p["soja"]:

                        if any(x in ingredients for x in [
                            "soja",
                            "soy"
                        ]):

                            warnings.append(
                                "🌱 Enthält Soja"
                            )

                    if p["vegan"]:

                        if any(x in ingredients for x in [
                            "milk",
                            "milch",
                            "egg",
                            "ei",
                            "meat",
                            "fleisch"
                        ]):

                            warnings.append(
                                "🥩 Nicht Vegan"
                            )

                    # ==================================
                    # RESULT
                    # ==================================

                    st.write("")

                    col_left, col_right = st.columns(
                        [1.3, 1],
                        gap="medium"
                    )

                    with col_left:

                        st.markdown(
                            f"<h3>{p_name}</h3>",
                            unsafe_allow_html=True
                        )

                        if warnings:

                            st.markdown(f"""

                            <div class="result-box-warn">

                                <h3>{t['warn']}</h3>

                                <p style="text-align:left;">

                                {"<br>".join(warnings)}

                                </p>

                            </div>

                            """, unsafe_allow_html=True)

                        else:

                            st.markdown(f"""

                            <div class="result-box-safe">

                                <h3>{t['safe']}</h3>

                                <p style="text-align:left;">

                                {t['safe_sub']}

                                </p>

                            </div>

                            """, unsafe_allow_html=True)

                            throw_confetti()

                    with col_right:

                        if product.get("image_front_url"):

                            st.image(
                                product["image_front_url"],
                                use_container_width=True
                            )

                    # ==================================
                    # HISTORY
                    # ==================================

                    if {
                        "name": p_name,
                        "code": barcode
                    } not in st.session_state.history:

                        st.session_state.history.insert(
                            0,
                            {
                                "name": p_name,
                                "code": barcode
                            }
                        )

                    # ==================================
                    # DETAILS
                    # ==================================

                    with st.expander(t["details"]):

                        st.write(
                            product.get(
                                "ingredients_text",
                                "Keine Daten"
                            )
                        )

                else:

                    st.error(t["not_found"])

# ==========================================
# TAB 3 — SETTINGS
# ==========================================

with tab_settings:

    st.markdown(
        f"<h2>{t['t3']}</h2>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        lang_list = list(ui.keys())

        new_lang = st.selectbox(
            t["lang_select"],
            lang_list,
            index=lang_list.index(
                st.session_state.lang
            )
        )

        if new_lang != st.session_state.lang:

            st.session_state.lang = new_lang
            st.rerun()

# ==========================================
# TAB 4 — INFO
# ==========================================

with tab_info:

    with st.container(border=True):

        st.markdown(
            "<h2>👥 Entwickler-Team Klasse 10a</h2>",
            unsafe_allow_html=True
        )

        st.divider()

        st.write("👨‍💻 Marius Boulos")
        st.write("👨‍💻 Benjamin Mehling")
        st.write("👩‍💻 Sophie Hartwig")
        st.write("👨‍💻 Ben Henkel")
        st.write("👨‍💻 Maximilian Maier")

        st.caption(
            "Hanns-Seidel-Gymnasium Aschaffenburg / Germany"
        )
