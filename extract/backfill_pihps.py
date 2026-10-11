import calendar
import json
import time
from datetime import date
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
    "start_date": "",
    "end_date": "",
}

hari_ini = date.today()
folder_utama = Path("data/raw/backfill")

daftar_bulan = []
tahun, bulan = 2026, 1
while (tahun, bulan) <= (hari_ini.year, hari_ini.month):
    daftar_bulan.append((tahun, bulan))
    bulan += 1
    if bulan == 13:
        bulan = 1
        tahun += 1

print(f"Akan menarik {len(daftar_bulan)} bulan data")

for tahun, bulan in daftar_bulan:
    awal = date(tahun, bulan, 1)
    hari_terakhir = calendar.monthrange(tahun, bulan)[1]
    akhir = min(date(tahun, bulan, hari_terakhir), hari_ini)

    params["start_date"] = awal.isoformat()
    params["end_date"] = akhir.isoformat()

    folder = folder_utama / f"{tahun}-{bulan:02d}"
    folder.mkdir(parents=True, exist_ok=True)

    file_baru = 0
    file_gagal = 0

    for pasar in range(1, 5):
        params["price_type_id"] = pasar

        for i in range(1, 22):
            kode = f"com_{i}"
            nama_file = folder / f"harga_{kode}_pasar_{pasar}.json"

            if nama_file.exists():
                continue

            params["comcat_id"] = kode

            try:
                response = requests.get(url, params=params, timeout=60)
                response.raise_for_status()
                hasil = response.json()
            except requests.RequestException as error:
                print(f"  {kode} pasar {pasar} GAGAL: {error}")
                file_gagal += 1
                continue

            with open(nama_file, "w", encoding="utf-8") as f:
                json.dump(hasil, f, ensure_ascii=False, indent=2)

            file_baru += 1
            time.sleep(1)

    print(f"{tahun}-{bulan:02d}: {file_baru} file baru, {file_gagal} gagal")

print("Backfill selesai!")