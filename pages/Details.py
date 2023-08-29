import streamlit as st
import os
from pathlib import Path
import pandas as pd
from st_pages import Page, show_pages, hide_pages
from src.ui import ui

ui.set_page_config()
show_pages(
    [
        Page("app.py", "Home Page"),
        Page("pages/Details.py", "Details"),
    ]
)

hide_pages(["Details"])

ui.set_page_container_style()
ui.display_logo()

# Store user's selected title
selected_title = st.session_state['card_key']
st.title(selected_title)

# Set Path
root_dir = os.path.dirname(os.path.abspath("__file__"))

# Filter dataframe according to selected title
data = pd.read_csv(Path(root_dir, "data/processed/processed_data.csv"))
data_filtered = df_filtered = (data.query(f"title == \"{selected_title}\""))

# Display basic information of selected title
ui.display_details(data_filtered)

# Show wordcloud, reviews and images of selected title
st.info("Toggle between reviews and images!")
tab1, tab2 = st.tabs(["Reviews", "Images"])

with tab1:
    ui.show_wordcloud(data_filtered)
    ui.show_reviews(data_filtered)
with tab2:
    ui.display_review_images(data_filtered)



   