import pandas as pd

# Завантаження файлу
df = pd.read_parquet("train-00000-of-00001-3b917f20b6cab6bc.parquet", engine="pyarrow")  # або engine="fastparquet"

df.to_csv("train-00000-of-00001-3b917f20b6cab6bc.csv", index=False)