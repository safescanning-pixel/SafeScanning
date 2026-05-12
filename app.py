import streamlit as st
import requests

# 1. Grundkonfiguration der Seite
st.set_page_config(page_title="NutriScan", page_icon="🍏")

# Sprach-Wörterbuch für die Mehrsprachigkeit
translations = {
    "Deutsch": {
        "title": "NutriScan Allergie-Check",
        "profile": "Dein Profil",
        "select_all": "Wähle deine Allergien/Intoleranzen:",
        "lifestyle": "Lifestyle & Ernährung:",
        "scan_now": "Produkt-Barcode",
        "input_label": "Barcode hier eingeben oder mit Handy-Kamera scannen:",
        "result_safe": "✅ Sicher für dich!",
        "result_warn": "❌ ACHTUNG: Enthält ",
        "not_found": "Produkt nicht gefunden.",
        "team": "Entwickler-Team",
        "disclaimer": "Hinweis: Daten stammen von Open Food Facts. Packung immer prüfen!"
    },
    "English": {
        "title": "NutriScan Allergy Check",
        "profile": "Your Profile",
        "select_all": "Select your allergies/intolerances:",
        "lifestyle": "Lifestyle & Diet:",
        "scan_now": "Product Barcode",
        "input_label": "Enter barcode here or scan with your phone camera:",
        "result_safe": "✅ Safe for you!",
        "result_warn": "❌ WARNING: Contains ",
        "not_found": "Product not found.",
        "team": "Developer Team",
        "disclaimer": "Note: Data from Open Food Facts. Always check the physical package!"
    }
}

# 2. Sidebar: Sprache und Impressum
st.sidebar.title("NutriScan Settings")
lang_choice = st.sidebar.selectbox("Language / Sprache", ["Deutsch", "English"])
t = translations[lang_choice]

st.sidebar.markdown("---")
st.sidebar.subheader(t["team"])
st.sidebar.write("Maximilian Maier")
st.sidebar.write("Benjamin Mehling")
st.sidebar.write("Ben Henkel")
st.sidebar.write("Marius Boulos")
st.sidebar.write("Sophie Hartwig")

# 3. Hauptbereich: User Profil
st.title(t["title"])

with st.expander(t["profile"], expanded=True):
    selected_allergies = st.multiselect(
        t["select_all"],
        ["Gluten", "Lactose", "Fructose", "Nüsse / Nuts", "Erdnüsse / Peanuts", "Soja", "Eier / Eggs", "Fisch"]
    )
    selected_lifestyle = st.multiselect(
        t["lifestyle"],
        ["Vegan", "Vegetarisch", "Halal"]
    )

# 4. Barcode Eingabe Bereich
st.subheader(t["scan_now"])
# Wir nutzen text_input, da dies am stabilsten auf allen Geräten läuft
barcode = st.text_input(t["input_label"])

# 5. Logik & API Abfrage
if barcode:
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url).json()
        
        if response.get("status") == 1:
            product = response["product"]
            p_name = product.get('product_name', 'Unbekanntes Produkt')
            st.info(f"Produkt: **{p_name}**")
            
            # Daten für den Check sammeln
            ingred_text = str(product.get("ingredients_text", "")).lower()
            allergen_tags = str(product.get("allergens_hierarchy", [])).lower()
            combined_data = ingred_text + allergen_tags
            
            found = []
            # Abgleich der Auswahl
            for a in selected_allergies:
                clean_a = a.split(" / ")[0].lower()
                if clean_a in combined_data:
                    found.append(a)
            
            # Ergebnis-Anzeige
            if found:
                st.error(f"{t['result_warn']} {', '.join(found)}!")
            else:
                st.success(t["result_safe"])
                
            # Produktbild anzeigen
            img_url = product.get("image_front_url")
            if img_url:
                st.image(img_url, width=150)
                
        else:
            st.warning(t["not_found"])
    except:
        st.error("Fehler bei der API-Abfrage.")

st.markdown("---")
st.caption(t["disclaimer"])
