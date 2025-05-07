import pandas as pd
import numpy as np

def transform_to_DataFrame(data):
    """Mengubah list of dict menjadi DataFrame dengan validasi."""
    if not isinstance(data, list):
        raise TypeError("Input data harus berupa list")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Setiap item dalam data harus berupa dictionary")

    try:
        df = pd.DataFrame(data)
        if df.empty:
            raise ValueError("DataFrame kosong setelah transformasi")
        return df
    except Exception as e:
        print(f"Terjadi kesalahan saat mengubah data menjadi DataFrame: {e}")
        raise

def clean_and_transform(data):
    """Membersihkan dan mentransformasi DataFrame."""
    df = transform_to_DataFrame(data)

    expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Kolom berikut tidak ditemukan di data: {missing_columns}")

    df['Price'] = df['Price'].replace('Price Unavailable', np.nan)
    df.dropna(subset=['Price'], inplace=True)
    df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True).astype(float) * 16000

    df = df[df['Title'] != 'Unknown Product']

    df['Rating'] = pd.to_numeric(df['Rating'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')
    df['Colors'] = pd.to_numeric(df['Colors'].str.extract(r'(\d+)')[0], errors='coerce').fillna(0).astype(int)

    df['Size'] = df['Size'].str.replace('Size: ', '', regex=True)
    df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=True)

    return df
