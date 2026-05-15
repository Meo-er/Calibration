import pandas as pd

from modules.overview import data_overview
from modules.cleaning import data_cleaned
from modules.preprocessing import preprocess_baseline
from modules.baseline import run_baseline
from modules.evaluation import (
    plot_label_distribution,
    plot_confusion_matrix,
    plot_reliability_diagram,
    plot_feature_boxplot,
)

readFile = "./data/raw/Tuesday-WorkingHours.pcap_ISCX.csv"
df = pd.read_csv(readFile)

data_overview(df)
df_cleaned = data_cleaned(df)
df_cleaned.to_csv("./data/processed/tuesday_cleaned.csv", index=False)

X_train, X_cal, X_test, y_train, y_cal, y_test, scaler = preprocess_baseline(df_cleaned)

plot_label_distribution(pd.concat([y_train, y_test]))

feature_sample = ["Flow Duration", "Total Fwd Packets", "Flow Bytes/s"]
existing_features = [f for f in feature_sample if f in df_cleaned.columns]
if existing_features:
    plot_feature_boxplot(df_cleaned, existing_features)

model, y_prob = run_baseline(X_train, X_test, y_train, y_test)
y_pred = model.predict(X_test)

plot_confusion_matrix(y_test, y_pred)

plot_reliability_diagram(y_test, y_prob)
