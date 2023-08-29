import pandas as pd
from pathlib import Path
import os
from src.pipeline_utils import transform

# Set Path
root_dir = os.path.dirname(os.path.abspath(".."))

# Extract
data = pd.read_csv(Path(root_dir, "data/raw/data.csv"))

# Transform
data_clean = transform.clean_metadata(data)
data_clean.to_csv(Path(root_dir, "data/processed/processed_data.csv"), 
                  index=False,  
                  encoding='utf-8-sig')