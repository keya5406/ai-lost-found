import streamlit as st
from app.utils import load_items, save_items

def add_item():
    st.write("### Add Lost/Found Item")

    item_type = st.selectbox("Is this item lost or found?", ['lost', 'found'])

    image_name = st.text_input("Image file name (from /data/images/):").strip()
    description = st.text_input("Description of the item:").strip()
    location = st.text_input("Location (e.g., library, park):").strip()
    date = st.date_input("Date (YYYY-MM-DD)")
    contact = st.text_input("Contact info (email or phone):").strip()

    if st.button("Submit"):
        if not description or not location or not contact:
            st.warning("⚠️ Please fill in all required fields.")
            return

        # For 'found' items, image is required
        if item_type == 'found' and not image_name:
            st.warning("⚠️ Please provide an image name for found items.")
            return

        item = {
            "type": item_type,
            "image_name": image_name if image_name else "N/A",
            "description": description,
            "location": location,
            "date": str(date),
            "contact": contact
        }

        items = load_items()
        items.append(item)
        save_items(items)

        st.success("✅ Item added successfully!")
