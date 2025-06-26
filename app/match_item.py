import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from app.utils import load_items

def match_items():
    st.write("\n--- Match Lost & Found Items ---")
    
    # Step 1: User input
    item_type = st.selectbox("Enter item type (lost/found):", ['lost', 'found']).strip().lower()
    user_description = st.text_input("Enter item description: ").strip().lower()
    user_location = st.text_input("Enter item location: ").strip().lower()
    user_date = st.date_input("Enter date (YYYY-MM-DD): ").strip()
    user_contact = st.text_input("Enter contact details: ").strip()
    
    # Step 2: Load existing items from storage
    items = load_items()
    
    # Step 3: Filter for opposite type (if it's a 'lost' item, find 'found' items and vice versa)
    if item_type == "lost":
        opposite_items = [item for item in items if item["type"] == "found"]
    elif item_type == "found":
        opposite_items = [item for item in items if item["type"] == "lost"]
    else:
        st.warning("❌ Invalid item type. Only 'lost' or 'found' are allowed.")
        return
    
    # Step 4: Match items by location
    location_matches = [item for item in opposite_items if user_location in item["location"].lower()]
    
    if not location_matches:
        st.warning("❌ No items found in this location.")
        return
    
    # Step 5: Match items by description (using cosine similarity)
    descriptions = [item["description"] for item in location_matches]
    all_descriptions = [user_description] + descriptions
    
    vectorizer = TfidfVectorizer().fit_transform(all_descriptions)
    vectors = vectorizer.toarray()

    matched_items = []

    # Step 6: Compare descriptions and collect all matches
    for i, item in enumerate(location_matches):
        item_vector = vectors[i+1]  # Skip the first vector (user's item description)
        user_vector = vectors[0]
        score = cosine_similarity([user_vector], [item_vector])[0][0]
        
        if score > 0.3:  # Only consider matches with a decent score
            matched_items.append({
                "item": item,
                "score": score
            })

    # Step 7: Output result
    if matched_items:
        st.write(f"\n🔗 Best matches found for your {item_type} item:")
        for match in matched_items:
            item = match["item"]
            score = match["score"]
            st.write(f"\n✅ Description: {item['description']}")
            st.write(f"📍 Location: {item['location']}")
            st.write(f"📅 Date: {item['date']}")
            st.write(f"📞 Contact: {item['contact']}")
            st.write(f"🔢 Match Score: {round(score, 2)}")

            # Show image if it exists
            if item.get("image_name"):
                image_path = f"data/images/{item['image_name']}"
                st.image(image_path, caption=f"Image of the {item['type']} item", use_container_width=True)
    else:
        st.warning(f"⚠️ No strong matches found for your {item_type} item.")
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
        location_matches = [item for item in opposite_items if user_location in item["location"].lower()]

        if not location_matches:
            st.info("❌ No items found in this location.")
            return

        # Description similarity
        descriptions = [item["description"].lower() for item in location_matches]
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
                st.write(f"**Description**: {item['description']}")
                st.write(f"**Location**: {item['location']}")
                st.write(f"**Date**: {item['date']}")
                st.write(f"**Contact**: {item['contact']}")
                
                # Show image only if available, otherwise display a message
                if item['image_name'] != 'N/A':
                    st.image(f"data/images/{item['image_name']}", caption="Image", use_container_width=True)
                else:
                    st.write("**Image**: No image available")

                st.write(f"**Match Score**: {round(score, 2)}")
        else:
            st.warning("😕 No strong matches found based on description.")
