import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.matching_engine import find_matches
from app.utils import get_items

def match_items():
    st.write("### Match Lost & Found Items")

    item_type = st.selectbox("Select your item type:", ['lost', 'found'])
    user_description = st.text_input("Item description:").strip().lower()
    user_location = st.text_input("Item location:").strip().lower()
    user_date = st.date_input("Date (YYYY-MM-DD)")
    user_contact = st.text_input("Contact info (optional):").strip()

    if st.button("Find Matches"):
        if not user_description or not user_location:
            st.warning("⚠️ Please fill in description and location.")
            return

        items = get_items()

        input_item = {
            "type": item_type,
            "description": user_description,
            "location": user_location
        }

        matched_items = find_matches(input_item, items)

        if matched_items:
            st.success(f"🔍 Found {len(matched_items)} potential match(es):")

            for match in matched_items:
                item = match["item"]
                score = match["score"]

                st.markdown("---")
                st.write(f"**Description**: {item.get('description', 'N/A')}")
                st.write(f"**Location**: {item.get('location', 'N/A')}")
                st.write(f"**Date**: {item.get('date', 'N/A')}")
                st.write(f"**Contact**: {item.get('contact', 'N/A')}")
                
                # Image handling (Cloudinary + local fallback)
                image_url = item.get("image_url")

                if image_url:
                    st.image(image_url, caption="Image", width="stretch")
                
                elif item.get("image_name") and item["image_name"] != "N/A":
                    st.image(
                        f"data/images/{item['image_name']}",
                        caption="Image",
                        width="stretch"
                    )
                
                else:
                    st.write("**Image**: No image available")

                st.write(f"**Match Score**: {round(score, 2)}")
        else:
            st.warning("😕 No strong matches found based on description.")
