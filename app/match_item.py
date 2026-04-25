import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils import load_items

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

        items = load_items()

        # Get opposite type items
        opposite_items = [item for item in items if item["type"] != item_type]

        # Location match
        location_matches = [
            item for item in opposite_items
            if user_location in item.get("location", "").lower()
        ]

        if not location_matches:
            st.info("❌ No items found in this location.")
            return

        # Description similarity
        descriptions = [item.get("description", "").lower() for item in location_matches]
        all_descriptions = [user_description] + descriptions

        vectorizer = TfidfVectorizer().fit_transform(all_descriptions)
        vectors = vectorizer.toarray()

        matched_items = []
        for i, item in enumerate(location_matches):
            score = cosine_similarity([vectors[0]], [vectors[i+1]])[0][0]
            if score > 0.3:
                matched_items.append((item, score))

        if matched_items:
            st.success(f"🔍 Found {len(matched_items)} potential match(es):")
            for item, score in matched_items:
                st.markdown("---")
                st.write(f"**Description**: {item.get('description', 'N/A')}")
                st.write(f"**Location**: {item.get('location', 'N/A')}")
                st.write(f"**Date**: {item.get('date', 'N/A')}")
                st.write(f"**Contact**: {item.get('contact', 'N/A')}")
                
                # Show image only if available, otherwise display a message
                # Handling both Cloudinary + local images
                if item.get("image_url"):
                    st.image(item["image_url"], caption="Image", width="stretch")
                
                elif item.get("image_name") and item["image_name"] != "N/A":
                    st.image(
                        f"data/images/{item['image_name']}",
                        caption="Image",
                        width="stretch"
                    )
                
                else:
                    st.write("**Image**: No image available")
                    st.write(item)

                st.write(f"**Match Score**: {round(score, 2)}")
        else:
            st.warning("😕 No strong matches found based on description.")
