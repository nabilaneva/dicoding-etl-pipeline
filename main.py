from utils.extract import extract_data
from utils.transform import clean_and_transform
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgres

# ID Sheet dari Google Sheets 
sheet = '1IOVeiHOGHQjBYp48RIzMm1IhYb3HAW4j9P69DpFB-VE'

# URL koneksi ke PostgreSQL
db_url = "postgresql://developer:17071707@localhost:5432/fashionsdb"

def main():
    # 1. Mengambil data dari website
    data = extract_data()

    # 2. Membersihkan dan transformasi data
    cleaned_df = clean_and_transform(data)

    # 3. Memuat data ke PostgreSQL
    load_to_csv(cleaned_df)
    load_to_google_sheets(cleaned_df, sheet)
    load_to_postgres(cleaned_df, db_url)

    print("Proses ETL telah selesai!")

if __name__ == "__main__":
    main()
 