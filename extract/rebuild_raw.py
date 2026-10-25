import subprocess
import sys
from pathlib import Path

from google.cloud import bigquery

TABLE_ID = "harga-pangan-pipeline.raw_pihps.harga_harian"

folder_backfill = sorted(
    p for p in Path("data/raw/backfill").iterdir() if p.is_dir()
)
folder_harian = sorted(
    p for p in Path("data/raw").iterdir() if p.is_dir() and p.name != "backfill"
)
semua_folder = folder_backfill + folder_harian

print(f"Ditemukan {len(semua_folder)} folder data untuk dimuat ulang")

client = bigquery.Client.from_service_account_json("credentials/bq-key.json")
client.delete_table(TABLE_ID, not_found_ok=True)
print(f"Tabel lama {TABLE_ID} dihapus")

for folder in semua_folder:
    subprocess.run(
        [sys.executable, "extract/load_bq.py", str(folder)],
        check=True,
    )

tabel = client.get_table(TABLE_ID)
print(f"Selesai. Jumlah baris: {tabel.num_rows}")
print(f"Tabel ini akan kedaluwarsa pada: {tabel.expires}")