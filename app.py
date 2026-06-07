import streamlit as st
import requests
import streamlit.components.v1 as components

# 1. Page Config muss ZWINGEND ganz oben stehen
st.set_page_config(page_title="AllergyShield Pro", page_icon="🛡️", layout="centered")

# 2. Parameter-Handling: Wir lesen den Scan aus der URL, ohne die Seite zu zwingen, sofort neu zu laden
if "scanned_barcode" in st.query_params:
    st.session_state.manual_code = st.query_params["scanned_barcode"]
    # Wir löschen den Parameter nicht sofort, um Endlosschleifen zu vermeiden

# Session State Initialisierung
if 'lang' not in st.session_state: st.session_state.lang = "Deutsch"
if 'cam_on' not in st.session_state: st.session_state.cam_on = False
if 'history' not in st.session_state: st.session_state.history = []
if 'manual_code' not in st.session_state: st.session_state.manual_code = ""
if 'profile' not in st.session_state:
    st.session_state.profile = {"laktose": False, "fruktose": False, "histamin": False, "sorbit": False, "sulfite": False, "glutamat": False, "gluten": False, "nuesse": False, "soja": False, "erdnuesse": False, "vegan": False, "vegetarisch": False, "halal": False, "koscher": False}

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    header {visibility: hidden;}
    .scanner-container { border: 4px solid #4F46E5; border-radius: 20px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# UI Komponenten (identisch wie gehabt, um Konsistenz zu wahren)
# [Hier steht dein UI Code - aus Platzgründen hier gekürzt, füge hier dein UI-Design ein]

tab_profil, tab_scanner, tab_settings, tab_info = st.tabs(["👤 Profil", "📸 Scanner", "⚙️ Einstellungen", "ℹ️ Info"])

with tab_scanner:
    st.markdown("<h2>📸 Scanner</h2>", unsafe_allow_html=True)
    
    # Der optimierte JavaScript-Scanner
    if st.button("Scanner starten/stoppen"):
        st.session_state.cam_on = not st.session_state.cam_on
        st.rerun()

    if st.session_state.cam_on:
        components.html("""
        <div id="reader" style="width: 100%;"></div>
        <script src="https://unpkg.com/html5-qrcode"></script>
        <script>
        const html5QrCode = new Html5Qrcode("reader");
        html5QrCode.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: { width: 250, height: 100 } },
            (decodedText) => {
                // Hier wird der Code direkt in die URL geschrieben
                window.parent.location.href = window.parent.location.origin + window.parent.location.pathname + "?scanned_barcode=" + decodedText;
                html5QrCode.stop();
            }
        ).catch(err => { console.log(err); });
        </script>
        """, height=400)

    # Barcode Verarbeitung
    barcode_input = st.text_input("Barcode", value=st.session_state.manual_code)
    
    if barcode_input:
        # Datenbank Abfrage
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode_input}.json"
        try:
            res = requests.get(url, timeout=3).json()
            if res.get("status") == 1:
                product = res["product"]
                st.write(f"### Gefunden: {product.get('product_name')}")
                st.image(product.get('image_front_url', ''))
                # Hier deine Logik für die Allergene...
            else:
                st.error("Produkt nicht gefunden.")
        except:
            st.error("Verbindungsfehler.")
