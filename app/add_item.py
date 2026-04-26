import streamlit as st
from app.utils import save_item, get_items
from app.matching_engine import find_matches
from app.cloudinary_config import upload_image

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
        
        # Upload image to Cloudinary
        image_url = None
        if uploaded_file:
            image_url = upload_image(uploaded_file)

        item = {
            "type": item_type,
            "image_url": image_url,
            "description": description,
            "location": location,
            "date": str(date),
            "contact": contact
        }

        # Save item
        save_item(item)
        st.success("✅ Item added successfully!")

        # Auto-matching
        items = get_items()
        matches = find_matches(item, items)

        if matches:
            st.success(f"🎉 Found {len(matches)} match(es) for your item!")

            for match in matches:
                matched_item = match["item"]
                score = match["score"]

                st.markdown("---")
                st.write(f"**Description**: {matched_item.get('description', 'N/A')}")
                st.write(f"**Location**: {matched_item.get('location', 'N/A')}")
                st.write(f"**Date**: {matched_item.get('date', 'N/A')}")

                # Image display
                image_url = matched_item.get("image_url")

                if image_url:
                    st.image(image_url, width="stretch")
                elif matched_item.get("image_name") and matched_item["image_name"] != "N/A":
                    st.image(f"data/images/{matched_item['image_name']}", width="stretch")
                else:
                    st.write("No image available")

                st.write(f"**Match Score**: {round(score, 2)}")

        else:
            st.info("No matches found right now. We'll keep looking!")
