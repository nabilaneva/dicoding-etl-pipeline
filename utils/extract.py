import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}
base_url = 'https://fashion-studio.dicoding.dev/'

def extract_product_data(product):
    """Mengambil detail produk dari elemen HTML"""
    try:
        # Mengambil informasi tentang produk
        title = product.select_one('.product-title').text.strip()
        price = product.select_one('.price-container').text.strip() if product.select_one('.price-container') else 'Price Unavailable'

        details = product.find_all('p')
        
        # Mengambil data rating, warna, ukuran, dan jenis kelamin
        rating = details[0].text.strip().split('/')[0].replace('Rating: ', '') if len(details) > 0 else 'N/A'
        colors = ''.join(filter(str.isdigit, details[1].text.strip())) if len(details) > 1 else 'N/A'
        size = details[2].text.replace('Size: ', '').strip() if len(details) > 2 else 'N/A'
        gender = details[3].text.replace('Gender: ', '').strip() if len(details) > 3 else 'N/A'

        timestamp = datetime.now().isoformat()

        # Mengembalikan data produk dalam bentuk dictionary
        return {
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Colors': colors,
            'Size': size,
            'Gender': gender,
            'Timestamp': timestamp
        }
    except Exception as e:
        print(f"Tidak dapat memproses produk: {e}")
        return None

def extract_data():
    """Mengambil data dari situs web dan mengembalikan daftar dictionary"""
    all_data = []
    print("Memulai proses ekstraksi data...")

    for page in range(1, 51):
        print(f"Mengambil data dari halaman {page}...")

        # Format URL yang benar
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}page{page}"

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Tidak dapat mengakses halaman {page}: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.select('.collection-card')

            if not products:
                print(f"Tidak ada produk di halaman {page}")
                continue

            for product in products:
                data = extract_product_data(product)
                if data:
                    all_data.append(data)

            time.sleep(2)

        except Exception as e:
            print(f"Kesalahan saat mengambil halaman {page}: {e}")

    print(f"Total data yang diekstrak: {len(all_data)} baris.")
    return all_data
