import streamlit as st
import requests
from camera_input_live import camera_input_live

# ==========================================
# 1. SETUP & MOBILE APP DESIGN (CSS)
# ==========================================
st.set_page_config(page_title="AllergyShield Pro", page_icon="🛡️", layout="centered")

# Custom CSS für das helle Thunkable "Card" Design
st.markdown("""
    <style>
    /* Hintergrund der gesamten App (helles Grau wie in echten Apps) */
    .stApp {
        background-color: #F4F6F9;
        color: #1E293B;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
   
    /* Header/Titel ausblenden für mehr App-Feeling */
    header {visibility: hidden;}
   
    /* Tabs so stylen, dass sie wie eine Navigationsleiste aussehen */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: white;
        padding: 10px;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-around;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px;
        color: #64748B;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #EEF2FF !important;
        color: #1D4ED8 !important; /* Blaues Active-Theme */
    }
   
    /* Buttons (z.B. Profil speichern) wie auf dem Screenshot */
    .stButton>button {
        background-color: #1D4ED8 !important; /* Royalblau */
        color: white !important;
        border-radius: 15px !important;
        height: 55px !important;
        width: 100% !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3) !important;
        margin-top: 20px;
    }
    .stButton>button:hover {
        background-color: #1E3A8A !important;
    }

    /* Container Boxen als weiße Karten mit Schatten */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        padding: 20px !important;
    }

    /* Toggles anpassen */
    .stToggle { margin-bottom: 10px; }

    /* Überschriften */
    h1, h2, h3 { color: #0F172A !important; font-weight: 800 !important; text-align: center; }
    h4 { color: #334155 !important; font-weight: 700 !important; margin-bottom: 15px !important;}
    p { color: #64748B !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 2. SESSION STATE (DATEN SPEICHERN)
# ==========================================
# Damit die App sich merkt, was du im Profil anklickst, wenn du zum Scanner gehst!
if 'profile' not in st.session_state:
    st.session_state.profile = {
        "laktose": False, "fruktose": False, "histamin": False, "sorbit": False,
        "sulfite": False, "glutamat": False,
        "vegan": False, "vegetarisch": False
    }


# ==========================================
# 3. NAVIGATION (TAB SYSTEM)
# ==========================================
tab_profil, tab_scanner, tab_info = st.tabs(["👤 Profil", "📸 Scanner", "ℹ️ Über uns"])

# ==============================================================================
# TAB 1: MEIN SCHUTZPROFIL (Exakter Nachbau deiner Thunkable Screenshots)
# ==============================================================================
with tab_profil:
    st.markdown("<h1>🛡️<br>Mein Schutzprofil</h1>", unsafe_allow_html=True)
    st.markdown("<p>Konfigurieren Sie Ihre Allergien und Unverträglichkeiten</p>", unsafe_allow_html=True)
    st.write("")

    # KARTE 1: Intoleranzen
    with st.container(border=True):
        st.markdown("<h4>Intoleranzen</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Laktose**")
        with col2: st.session_state.profile["laktose"] = st.toggle(" ", value=st.session_state.profile["laktose"], key="t_lak")
       
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Fruktose**")
        with col2: st.session_state.profile["fruktose"] = st.toggle(" ", value=st.session_state.profile["fruktose"], key="t_fruk")
       
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Histamin**")
        with col2: st.session_state.profile["histamin"] = st.toggle(" ", value=st.session_state.profile["histamin"], key="t_hist")
       
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Sorbit**")
        with col2: st.session_state.profile["sorbit"] = st.toggle(" ", value=st.session_state.profile["sorbit"], key="t_sorb")

    # KARTE 2: Zusatzstoffe
    with st.container(border=True):
        st.markdown("<h4>Zusatzstoffe</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Sulfite**")
        with col2: st.session_state.profile["sulfite"] = st.toggle(" ", value=st.session_state.profile["sulfite"], key="t_sulf")
       
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Glutamat**")
        with col2: st.session_state.profile["glutamat"] = st.toggle(" ", value=st.session_state.profile["glutamat"], key="t_glut")

    # KARTE 3: Lebensstil
    with st.container(border=True):
        st.markdown("<h4>Lebensstil</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Vegan**")
        with col2: st.session_state.profile["vegan"] = st.toggle(" ", value=st.session_state.profile["vegan"], key="t_veg")
       
        col1, col2 = st.columns([3, 1])
        with col1: st.write("**Vegetarisch**")
        with col2: st.session_state.profile["vegetarisch"] = st.toggle(" ", value=st.session_state.profile["vegetarisch"], key="t_vege")

    if st.button("💾 Profil speichern"):
        st.success("✅ Profil erfolgreich in der App gespeichert! Wechsle nun zum Scanner.")


# ==============================================================================
# TAB 2: DER SCANNER & DIE LOGIK
# ==============================================================================
with tab_scanner:
    st.markdown("<h2>📸 Scanner</h2>", unsafe_allow_html=True)
    st.markdown("<p>Halte den Barcode in die Kamera oder tippe ihn ein.</p>", unsafe_allow_html=True)

    with st.container(border=True):
        # Hier ist die Live-Kamera!
        st.info("Kamera aktiviert 🟢")
        camera_input_live()

    st.write("")
    with st.container(border=True):
        barcode_input = st.text_input("Oder Barcode manuell eingeben:", placeholder="z.B. 3017620425035")

    # --- DIE INTELLIGENTE DATENBANK ABFRAGE ---
    if barcode_input:
        barcode = "".join(filter(str.isdigit, barcode_input))
       
        if len(barcode) >= 8:
            st.divider()
            with st.spinner("🔍 Suche Produkt in der Datenbank..."):
               
                # Der "Anti-Blockier-Ausweis" für dein Glasfaser Internet
                headers = {'User-Agent': 'AllergyShieldPro/1.0 (Windows; School Project)'}
                url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
               
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                   
                    if response.status_code == 200:
                        data = response.json()
                       
                        if data.get("status") == 1:
                            product = data["product"]
                           
                            # Produkt Karte anzeigen
                            with st.container(border=True):
                                st.markdown(f"<h3>{product.get('product_name', 'Unbekanntes Produkt')}</h3>", unsafe_allow_html=True)
                               
                                if product.get("image_front_url"):
                                    st.image(product["image_front_url"], use_container_width=True)
                               
                                # Zutaten auslesen (alles kleingeschrieben für die Suche)
                                ingredients_str = str(product.get("ingredients_text", "")).lower()
                                allergens_str = str(product.get("allergens_hierarchy", [])).lower()
                                all_text = ingredients_str + " " + allergens_str
                               
                                # === ABGLEICH MIT DEM PROFIL ===
                                warnings = []
                                prof = st.session_state.profile
                               
                                # Wörterbuch für die Suche (Deutsch, Englisch, Französisch)
                                check_dict = {
                                    "laktose": ["milch", "milk", "lait", "laktose", "lactose", "molke", "sahne", "butter", "käse"],
                                    "fruktose": ["fruktose", "fructose", "fruchtzucker", "apfel", "birne", "honig", "sirup"],
                                    "histamin": ["tomate", "wein", "spinat", "käse", "hefe", "fermentiert", "essig", "salami"],
                                    "sorbit": ["sorbit", "sorbitol", "e420"],
                                    "sulfite": ["sulfit", "sulfite", "e220", "e221", "e222", "e223", "e224", "e226", "e227", "e228", "schwefeldioxid"],
                                    "glutamat": ["glutamat", "glutamate", "e621", "e622", "e623", "e624", "e625", "hefeextrakt"],
                                    "vegan": ["milch", "milk", "ei ", "egg", "fleisch", "meat", "fisch", "fish", "honig", "gelatine", "huhn", "rind", "schwein"],
                                    "vegetarisch": ["fleisch", "meat", "fisch", "fish", "gelatine", "huhn", "rind", "schwein"]
                                }
                               
                                # Prüfen, ob die aktiven Profil-Schalter im Text gefunden werden
                                for key, is_active in prof.items():
                                    if is_active:
                                        search_words = check_dict[key]
                                        if any(word in all_text for word in search_words):
                                            if key == "vegan" or key == "vegetarisch":
                                                warnings.append(f"Nicht {key.capitalize()}")
                                            else:
                                                warnings.append(f"Enthält {key.capitalize()}")

                                # ERGEBNIS ANZEIGEN
                                st.write("")
                                if len(warnings) > 0:
                                    st.error("### 🛑 WARNUNG!")
                                    st.write("Dieses Produkt passt **nicht** zu deinem Schutzprofil:")
                                    for w in warnings:
                                        st.markdown(f"- **{w}**")
                                else:
                                    st.success("### ✅ PRODUKT SICHER!")
                                    st.write("Es wurden keine Konflikte mit deinem Schutzprofil gefunden.")
                                    st.balloons()
                        else:
                            st.warning("⚠️ Produkt nicht gefunden. (Tipp für Nutella: 3017620425035)")
                    else:
                        st.error(f"Datenbank antwortet nicht. Fehler {response.status_code}")
               
                except Exception as e:
                    st.error(f"Verbindungsfehler. Bitte Internet prüfen. Details: {e}")

# ==============================================================================
# TAB 3: ÜBER UNS
# ==============================================================================
with tab_info:
    with st.container(border=True):
        st.markdown("<h2>👥 Entwickler-Team</h2>", unsafe_allow_html=True)
        st.markdown("<p>Hanns-Seidel-Gymnasium | Klasse 10a</p>", unsafe_allow_html=True)
        st.divider()
        st.write("👨‍💻 **Maximilian Maier**")
        st.write("👨‍💻 **Benjamin Mehling**")
        st.write("👨‍💻 **Ben Henkel**")
        st.write("👨‍💻 **Marius Boulos**")
        st.write("👩‍💻 **Sophie Hartwig**")
       
        st.info("Dieses Projekt nutzt die OpenFoodFacts API zur Analyse von über 2 Millionen Lebensmitteln.")
