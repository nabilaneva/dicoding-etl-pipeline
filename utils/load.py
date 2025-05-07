import os
import gspread
import pandas as pd
from sqlalchemy import create_engine, text
from google.oauth2.service_account import Credentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, '..', 'service_account.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key('1IOVeiHOGHQjBYp48RIzMm1IhYb3HAW4j9P69DpFB-VE').sheet1

def load_to_csv(df, filename='products.csv'):
    """Menyimpan DataFrame ke file CSV"""
    try:
        df.to_csv(filename, index=False)
        print(f"Data telah berhasil disimpan ke file CSV: {filename}")
    except Exception as e:
        print(f"Tidak dapat menyimpan ke CSV: {e}")

def load_to_google_sheets(df, sheet_id, creds_file=SERVICE_ACCOUNT_FILE):
    """Mengupload DataFrame ke Google Sheets."""
    try:
        creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1

        # Mengonversi datetime ke string agar kompatibel dengan Google Sheets
        df = df.copy()
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)

        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("Data telah berhasil dimuat ke Google Sheets.")
    except Exception as e:
        print(f"Tidak dapat memuat data ke Google Sheets: {e}")

def load_to_postgres(df, db_url, table_name='fashions_products'):
    """Mengupload DataFrame ke PostgreSQL (versi untuk produksi/testing)"""
    try:
        engine = create_engine(db_url)

        # Validasi kolom
        expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Kolom berikut hilang dari DataFrame: {missing_columns}")

        # Buat tabel jika belum ada
        with engine.connect() as con:
            con.execute(text(f""" 
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    "Title" TEXT NOT NULL,
                    "Price" NUMERIC(10, 2) NOT NULL,
                    "Rating" NUMERIC(3, 2) NOT NULL,
                    "Colors" INTEGER NOT NULL,
                    "Size" TEXT NOT NULL,
                    "Gender" TEXT NOT NULL,
                    "Timestamp" TIMESTAMP NOT NULL
                );
            """))

        # Upload data
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Data telah berhasil dimuat ke PostgreSQL table '{table_name}'.")
    except Exception as e:
        print(f"Tidak dapat memuat data ke PostgreSQL: {e}")
        raise
