import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
import emoji

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def one_hot_encode_tags(data: pd.DataFrame) -> pd.DataFrame:
    """Split the tags and one hot encode it

    Args:
        data (pd.DataFrame): raw data

    Returns:
        pd.DataFrame: data with one hot encoded tags
    """
    data["clean_tags"] = (data["tags"].str.replace(" ", "", regex=False)).str.replace("&", "and")
    data_clean = data.join(data['clean_tags'].str.split("\n").str.join('|').str.get_dummies())

    return data_clean

def clean_reviews(data, STOPWORDS, PUNCT_TO_REMOVE):
    data["review_title"]  = data["review_title"].astype(str)
    data["review_desc"] = data["review_desc"].astype(str)
    data["review_title_desc"] = (data["review_title"] + " " + data["review_desc"]).str.replace("nan", "", regex=False)
    
    data = (data
            .assign(review_title_desc=lambda df_: (df_
                                                   .review_title_desc
                                                   .str.lower()
                                                   .str.translate(str.maketrans('', '', 
                                                                                PUNCT_TO_REMOVE))
                                                    )
                    )
            )
    
    data["review_title_desc"] = data["review_title_desc"].apply(lambda x: emoji.replace_emoji(x))
    data["review_title_desc"] = data["review_title_desc"].apply(lambda x: (" ".join([word for word in str(x)
                                                                                     .split() if word not in STOPWORDS])))
    
            
    return data

def clean_num_reviews(data):
     data['num_reviews'] = (data['num_reviews']
                            .str.findall(r'\d+')
                            .str.join(", ")
                            .astype(int))
     return data

def clean_num_wishlisted(data):
    data['num_wishlisted'] = (data['num_wishlisted']
                              .str.findall(r'\d+')
                              .str.join(", ")
                              .astype(int))
    return data

def clean_price(data):
    data['price'] = (data['price']
                     .str.replace("Know the average price?", "0", regex=True)
                     .str.findall(r'\d+')
                     .str.join(", ")
                     .astype(int))
    return data

def clean_title(data):
    data['title'] = data['title'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
    return data

def clean_metadata(data: pd.DataFrame) -> pd.DataFrame:

    # Set stopwords and punctuations to remove
    PUNCT_TO_REMOVE = string.punctuation
    STOPWORDS = set(stopwords.words('english'))
    STOPWORDS.update(["nan", "like", "’", "tampines", "burpple", "would"])
   
    data_clean = clean_title(data)
    STOPWORDS.update(data_clean.title.unique())

    data_clean = one_hot_encode_tags(data)
    data_clean = clean_num_reviews(data_clean)
    data_clean = clean_num_wishlisted(data_clean)
    data_clean = clean_price(data_clean)
    data_clean = clean_reviews(data_clean, STOPWORDS, PUNCT_TO_REMOVE)

    # Remove listings with no reviews
    # Only keep necessary columns
    data_clean = (data_clean
                  .query("num_reviews > 0")
                  .drop(['bio', 'review_title'], axis=1)
    )


    return data_clean
