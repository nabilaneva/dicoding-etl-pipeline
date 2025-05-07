import unittest
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import load_to_postgres

class TestLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_url = "postgresql://developer:17071707@localhost:5432/fashionsdb"
        cls.engine = create_engine(cls.db_url)
        cls.sample_data = pd.DataFrame([{
            'Title': 'T-shirt 01',
            'Price': 400000.0,
            'Rating': 4.5,
            'Colors': 3,
            'Size': 'M',
            'Gender': 'Unisex',
            'Timestamp': '2025-03-20T12:00:00'
        }])
        
        with cls.engine.connect() as con:
            con.execute(text(""" 
            CREATE TABLE IF NOT EXISTS products (
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
            print("Tabel 'products' berhasil dibuat.")

            result = con.execute(text("""SELECT * FROM information_schema.tables WHERE table_name = 'products';""")).fetchone()
            if result:
                print("Tabel 'products' ada di database.")
            else:
                raise Exception("Tabel 'products' tidak ditemukan.")

    def test_load_to_postgres(self):
        """Uji apakah data dapat dimuat ke PostgreSQL"""
        load_to_postgres(self.sample_data, self.db_url, 'products')
        
        with self.engine.connect() as con:
            result = con.execute(text("""SELECT * FROM products WHERE "Title" = 'T-shirt 01';""")).fetchone()
            
            if result:
                columns = [col[0] for col in con.execute(text("SELECT * FROM products LIMIT 0")).cursor.description]
                result = dict(zip(columns, result))
            
            self.assertIsNotNone(result, "Data tidak ditemukan di tabel products")
            self.assertEqual(result['Title'], 'T-shirt 01', "Data yang dimuat tidak sesuai.")

    @classmethod
    def tearDownClass(cls):
        with cls.engine.connect() as con:
            result = con.execute(text("""SELECT * FROM information_schema.tables WHERE table_name = 'products';""")).fetchone()
            if result:
                con.execute(text('DELETE FROM products WHERE "Title" = :title'),
                            {'title': 'T-shirt 01'})
                print("Data uji berhasil dihapus.")
            else:
                print("Tabel 'products' tidak ditemukan, tidak ada data yang dihapus.")

if __name__ == '__main__':
    unittest.main()
