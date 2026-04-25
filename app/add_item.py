import streamlit as st
from app.utils import load_items, save_items

def add_item():
    st.write("### Add Lost/Found Item")

    item_type = st.selectbox("Is this item lost or found?", ['lost', 'found'])

    uploaded_file = st.file_uploader("Upload item image", type=["jpg", "png", "jpeg"])
    description = st.text_input("Description of the item:").strip()
    location = st.text_input("Location (e.g., library, park):").strip()
    date = st.date_input("Date (YYYY-MM-DD)")
    contact = st.text_input("Contact info (email or phone):").strip()

    if st.button("Submit"):
        if not description or not location or not contact:
            st.warning("⚠️ Please fill in all required fields.")
            return

        # For 'found' items, image is required
        if item_type == 'found' and not uploaded_file:
            st.warning("⚠️ Please provide an image name for found items.")
            return
        
        image_url = None

        if uploaded_file:
            from app.cloudinary_config import upload_image
            image_url = upload_image(uploaded_file)

        item = {
            "type": item_type,
            "image_url": image_url,
            "description": description,
            "location": location,
            "date": str(date),
            "contact": contact
        }

        items = load_items()
        items.append(item)
        save_items(items)

        st.success("✅ Item added successfully!")
