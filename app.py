import requests
import time
from flask import Flask, render_template

app = Flask(__name__)

# Variabel untuk menyimpan proxy yang diperbarui
cached_proxies = []
last_update_time = 0
UPDATE_INTERVAL = 60  # Interval pembaruan dalam detik

def fetch_proxies():
    """Mengambil proxy dari dua URL yang berbeda."""
    global cached_proxies, last_update_time

    # Jika waktu pembaruan terakhir kurang dari interval, gunakan cache
    current_time = time.time()
    if current_time - last_update_time < UPDATE_INTERVAL:
        return cached_proxies

    # URL API proxy
    proxy_urls = '''
    https://api.proxies.is/scraped?token=9h6sAGg56801DH7T875d2&timeout=15000&excludeASN=&includeASN=&excludeCountry=&includeCountry=IN&type=
    '''.splitlines()
    #https://prem-proxy.vercel.app/sharedprem-buat-jualan.txt
    #https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&anonymity=all&timeout=20000
    #https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&anonymity=Elite&timeout=20000
    #https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite
    #https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&anonymity=elite&timeout=10000&proxy_format=ipport&format=text

    proxies_combined = []

    for url in proxy_urls:
        # Abaikan baris kosong
        if not url.strip():
            continue

        try:
            response = requests.get(url)

            # Jika respons gagal, abaikan URL ini
            if response.status_code != 200:
                print(f"Gagal mengambil proxy dari {url}. Status Code: {response.status_code}")
                continue

            # Tambahkan proxy ke daftar gabungan, hilangkan spasi, dan abaikan baris kosong
            proxies = [proxy.strip() for proxy in response.text.splitlines() if proxy.strip()]
            proxies_combined.extend(proxies)

        except requests.exceptions.RequestException as e:
            print(f"Terjadi kesalahan saat mengambil proxy dari {url}: {str(e)}")
            continue

    proxies_combined = proxies_combined[:1000000]

    # Perbarui cache
    cached_proxies = proxies_combined
    last_update_time = current_time

    return cached_proxies

@app.route('/')
def index():
    proxies = fetch_proxies()

    # Tampilkan pesan jika tidak ada proxy yang tersedia
    if not proxies:
        return render_template('index.html', error="Tidak ada proxy yang tersedia.")

    # Gabungkan proxy dalam satu string dengan newline sebagai pemisah
    formatted_proxies = "\n".join(proxies)

    return render_template('index.html', proxies=formatted_proxies)

if __name__ == '__main__':
    app.run(debug=True)
