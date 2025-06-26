import streamlit as st
from app.add_item import add_item
from app.match_item import match_items

# Set up the title for the app
st.title('Lost and Found App')

# Create two buttons for functionality
option = st.sidebar.selectbox('Select an action:', ['Add Item', 'Find Matches'])

if option == 'Add Item':
    st.subheader('Add a Lost/Found Item')
    add_item()

elif option == 'Find Matches':
    st.subheader('Find Matching Lost/Found Items')
    match_items()
