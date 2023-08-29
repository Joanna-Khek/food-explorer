from pathlib import Path
import streamlit as st
import os
import pandas as pd
from st_pages import Page, show_pages, hide_pages
from src.ui import ui

# Set Page Configs
ui.set_page_config()
ui.set_page_container_style()

show_pages(
    [
        Page("app.py", "Home Page"),
        Page("pages/Details.py", "Details"),
    ]
)

hide_pages(["Details"])

# Show Logo
ui.display_logo()

# Set Session Sate
if 'card_key' not in st.session_state:
    st.session_state['card_key'] = 0

if 'index' not in st.session_state:
    st.session_state.index = 0
    
# Set Path
root_dir = os.path.dirname(os.path.abspath("__file__"))

# Show Sidebar Options
data = pd.read_csv(Path(root_dir, "data/processed/processed_data.csv"))
area_option, category_option = ui.display_sidebar(data)

# Display title
ui.display_title_cards(data, category_option, area_option)