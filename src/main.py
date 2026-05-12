import pandas as pd

from modules.overview import data_overview
from modules.cleaning import data_cleaned
from modules.preprocessing import preprocess_baseline

readFile = "./data/raw/Tuesday-WorkingHours.pcap_ISCX.csv"
df = pd.read_csv(readFile)

data_overview(df)
df_cleaned = data_cleaned(df)
df_cleaned.to_csv("./data/processed/tuesday_cleaned.csv", index=False)

X_train, X_test, y_train, y_test, scaler = preprocess_baseline(df_cleaned)
