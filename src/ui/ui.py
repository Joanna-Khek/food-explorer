import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from streamlit_card import card
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

from streamlit_extras.switch_page_button import switch_page

def set_page_config():
    st.set_page_config(
    page_title="Food Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)
    
def set_page_container_style() -> None:
    """Set report container style."""

    margins_css = """
    <style>
        /* Configuration of paddings of containers inside main area */
        .main > div {
            max-width: 100%;
            padding-left: 5%;
        }
        /*Font size in tabs */
        button[data-baseweb="tab"] div p {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """
    st.markdown(margins_css, unsafe_allow_html=True)


def display_logo() -> None:
    logo = Image.open("assets/food_explorer_logo.png")
    with st.sidebar:
        st.image(logo, use_column_width=True)

def get_categories(data: pd.DataFrame) -> list:
    """List of raw tags categories 

    Args:
        data (pd.DataFrame): processed data

    Returns:
        list: raw tags categories
    """
    categories = list(data.tags.str.split("\n").explode().unique())
    remove_list = ['BurppleBeyondDeals💰', 'BEYOND', 'BITES']
    categories = [item for item in categories if item not in remove_list]
    return categories


def display_sidebar(data: pd.DataFrame) -> str:
    """Select area and tags option

    Args:
        data (pd.DataFrame): processed data

    Returns:
        str: area and tags options
    """
    
    categories = get_categories(data)

    if 'option' not in st.session_state:
        st.session_state['option'] = categories

    with st.sidebar:
        area = st.selectbox("Area", ["Tampines"], disabled=True)

        option = st.selectbox("Select a category",
                          options=st.session_state.option,
                          index=st.session_state.index,
                          key='selected_category')
        st.session_state.index  = st.session_state.option.index(st.session_state.selected_category)

    return area, option

def details_page(title):
    st.session_state['card_key'] = title
    switch_page("Details")

def display_details(data_filtered):
    df_filtered = (data_filtered
                   .loc[:,['title','num_reviews', 'num_wishlisted', 'price']]
                   .drop_duplicates(subset=['title'], keep='first')
    )

    st.markdown(f"**:white_check_mark: Number of reviews:** {df_filtered.num_reviews.values[0]}")
    st.markdown(f"**:heartbeat: Number of wishlisted:** {df_filtered.num_wishlisted.values[0]}")
    st.markdown(f"**:money_mouth_face: Price per pax** ~${df_filtered.price.values[0]}")


def show_reviews(data_filtered):
    df_filtered = (data_filtered
                   .loc[:,['review_desc']]
                   .rename(columns={'review_desc': 'Reviews'})
    )

    gd = GridOptionsBuilder.from_dataframe(df_filtered)
    gd.configure_pagination(paginationAutoPageSize=True,
                            paginationPageSize=5,
                            enabled=True)
    gd.configure_columns("Reviews",wrapText = True)
    gd.configure_columns("Reviews",autoHeight = True)
    gridoptions = gd.build()
    AgGrid(df_filtered, 
           fit_columns_on_grid_load=True,
           columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
           gridOptions=gridoptions,
           wrapText=  True)

def display_title_cards(data: pd.DataFrame, category: str, area:str) -> None:
    """Clean raw tags category and filter the processed data

    Args:
        data (pd.DataFrame): processed data
        category (str): user selected raw tag category
        area (str): user selected area
    """
    clean_category = category.replace(" ", "").replace("&", "and")

    filtered_data = (data
                    .query(f"{clean_category} == 1 & area == '{area}'")
                    .loc[:, ['title', 'num_reviews', 'num_wishlisted', 'area', 'price', 
                            'review_image', 'review_title_desc']])
    
    filtered_data_no_dup = filtered_data.drop_duplicates(subset=['title'], keep='first')

    sort_option = st.radio("Sort by", ["Reviews", "Wishlisted", "Price"])
   
    col1, col2, col3 = st.columns(3)

    for i in range(len(filtered_data_no_dup)):

        if sort_option == 'Reviews':
            filtered_data_no_dup = filtered_data_no_dup.sort_values(by=['num_reviews'], ascending=False)
            text = f"{filtered_data_no_dup.num_reviews.iloc[i]} Reviews"
        
        elif sort_option == 'Wishlisted':
            filtered_data_no_dup = filtered_data_no_dup.sort_values(by=['num_wishlisted'], ascending=False)
            text = f"{filtered_data_no_dup.num_wishlisted.iloc[i]} Wishlisted"

        elif sort_option == 'Price':
            filtered_data_no_dup = filtered_data_no_dup.sort_values(by=['price'], ascending=False)
            text = f"~${filtered_data_no_dup.price.iloc[i]} per pax"

        col = i%3
        if col == 0:
            with col1:
                card(
                    title=filtered_data_no_dup.title.iloc[i],
                    text=text,
                    image=filtered_data_no_dup.review_image.iloc[i],
                    key=f"card_{i}",
                    on_click = lambda: details_page(filtered_data_no_dup.title.iloc[i])
                    )
                
        elif col == 1:
            with col2:
                card(
                    title=filtered_data_no_dup.title.iloc[i],
                    text=text,
                    image=filtered_data_no_dup.review_image.iloc[i],
                    key=f"card_{i}",
                    on_click = lambda: details_page(filtered_data_no_dup.title.iloc[i])
                    )

        elif col == 2:
            with col3:
                card(
                    title=filtered_data_no_dup.title.iloc[i],
                    text=text,
                    image=filtered_data_no_dup.review_image.iloc[i],
                    key=f"card_{i}",
                    on_click = lambda: details_page(filtered_data_no_dup.title.iloc[i])
                    )
                
def show_wordcloud(data_filtered):
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    wordcloud = WordCloud(colormap='Accent', width=800, 
                          height=500, 
                          min_font_size = 12,
                          stopwords=['nan', 'one']).generate(str(data_filtered.review_title_desc.values))
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot()

def display_review_images(data_filtered):
    col1, col2, col3 = st.columns(3)

    for i in range(len(data_filtered)):

        col = i%3
        if col == 0:
            with col1:
              st.image(data_filtered.review_image.iloc[i], width=300)
                
        elif col == 1:
            with col2:
                st.image(data_filtered.review_image.iloc[i], width=300)

        elif col == 2:
            with col3:
                st.image(data_filtered.review_image.iloc[i], width=399)
