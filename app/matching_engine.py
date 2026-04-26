from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_matches(input_item, items_list, threshold=0.3):
    # input_item: dict (user inout item)
    # items_list: list of dicts (existing items)

    item_type = input_item.get("type")
    description = input_item.get("description", "").lower()
    location = input_item.get("location", "").lower()

    # Get opposite type items
    opposite_items = [
        item for item in items_list
        if item.get("type") != item_type
    ]

    # Filter by location
    location_matches = [
        item for item in opposite_items
        if location in item.get("location", "").lower()
    ]

    if not location_matches:
        return []
    
    descriptions = [item.get("description", "").lower() for item in location_matches]
    all_descriptions = [description] + descriptions

    vectorizer = TfidfVectorizer().fit_transform(all_descriptions)
    vectors = vectorizer.toarray()

    matched_items = []

    for i, item in enumerate(location_matches):
        score = cosine_similarity([vectors[0]], [vectors[i + 1]])[0][0]

        if score > threshold:
            matched_items.append({
                "item": item,
                "score": score
            })

    return matched_items