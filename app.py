import streamlit as st
import requests
import streamlit.components.v1 as components

# ==========================================
# 1. SETUP & ULTRA CLEAN UI DESIGN
# ==========================================
st.set_page_config(page_title="AllergyShield Pro", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #111827; font-family: sans-serif; }
    header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { background-color: white; padding: 6px; border-radius: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.02); gap: 8px; justify-content: center; margin-bottom: 25px; }
    .stTabs [data-baseweb="tab"] { height: 46px; border-radius: 18px; color: #6B7280; font-weight: 600; padding: 0 20px; border: none !important; }
    .stTabs [aria-selected="true"] { background-color: #E0E7FF !important; color: #4F46E5 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. STATE & KONFIGURATION
# ==========================================
if 'cam_on' not in st.session_state: st.session_state.cam_on = False
if 'scanned_code' not in st.session_state: st.session_state.scanned_code = ""
if 'profile' not in st.session_state:
    st.session_state.profile = {"laktose": False, "fruktose": False, "histamin": False, "sorbit": False, "sulfite": False, "glutamat": False, "vegan": False, "vegetarisch": False}

# ==========================================
# 3. TABS & INHALTE
# ==========================================
tab_profil, tab_scanner, tab_settings, tab_info = st.tabs(["👤 Profil", "📸 Scanner", "⚙️ Einstellungen", "ℹ️ Info"])

with tab_profil:
    st.markdown("<h1>🛡️ Mein Schutzprofil</h1>", unsafe_allow_html=True)
    for key in st.session_state.profile:
        st.session_state.profile[key] = st.toggle(key.capitalize(), value=st.session_state.profile[key])

with tab_scanner:
    st.markdown("<h2>📸 Scanner</h2>", unsafe_allow_html=True)
    
    if st.button("📸 Kamera starten" if not st.session_state.cam_on else "🛑 Kamera stoppen"):
        st.session_state.cam_on = not st.session_state.cam_on
        st.rerun()

    if st.session_state.cam_on:
        scanner_html = """
        <div id="reader" style="width:100%"></div>
        <script src="https://unpkg.com/html5-qrcode"></script>
        <script>
            function onScanSuccess(decodedText) {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: decodedText}, '*');
            }
            new Html5Qrcode("reader").start({ facingMode: "environment" }, { fps: 10, qrbox: 250 }, onScanSuccess);
        </script>
        """
        components.html(scanner_html, height=350)

    barcode = st.text_input("Barcode eingeben", value=st.session_state.scanned_code)
    
    # JS-Listener für den Barcode-Empfang
    components.html("""
    <script>
        window.addEventListener("message", (e) => {
            if (e.data.type === "streamlit:setComponentValue") {
                const input = window.parent.document.querySelector('input[type="text"]');
                const nativeValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                nativeValueSetter.call(input, e.data.value);
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });
    </script>
    """, height=0)

    if barcode and len(barcode) > 5:
        with st.spinner("Analysiere..."):
            try:
                res = requests.get(f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json").json()
                if res.get("status") == 1:
                    prod = res["product"]
                    st.image(prod.get("image_front_url", ""), width=200)
                    st.subheader(prod.get("product_name", "Produkt"))
                    st.success("✅ Produkt gefunden!")
                else:
                    st.error("Nicht gefunden.")
            except:
                st.error("Verbindungsfehler.")

with tab_settings:
    st.selectbox("Sprache wählen", ["Deutsch", "English", "Français", "Türkçe", "Español", "Italiano"])

with tab_info:
    st.markdown("<h2>👥 Entwickler-Team Klasse 10a</h2>", unsafe_allow_html=True)
    st.write("**Mitglieder:** Benjamin Mehling, Sophie Hartwig, Ben Henkel, Maximilian Maier, Marius Boulos")
    st.write("Hanns-Seidel-Gymnasium Aschaffenburg")
