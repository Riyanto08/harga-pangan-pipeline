import json
import time
from pathlib import Path

import requests

url = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas"

params = {
    "price_type_id": "",
    "comcat_id": "",
    "province_id": "",
    "regency_id": "",
    "showKota": "false",
    "showPasar": "false",
    "tipe_laporan": 1,
    "start_date": "2026-10-02",
    "end_date": "2026-10-09",
}

folder = Path("data/raw")
folder.mkdir(parents=True, exist_ok=True)

for pasar in range(1, 5):
    params["price_type_id"] = pasar
    print(f"=== Jenis pasar {pasar} ===")

    for i in range(1, 22):
        kode = f"com_{i}"
        params["comcat_id"] = kode

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
        except requests.RequestException as error:
            print(kode, "GAGAL:", error)
            continue

        hasil = response.json()
        nama_file = folder / f"harga_{kode}_pasar_{pasar}.json"
        with open(nama_file, "w", encoding="utf-8") as f:
            json.dump(hasil, f, ensure_ascii=False, indent=2)

        print(kode, "->", len(hasil["data"]), "baris")
        time.sleep(1)

print("Selesai!")