import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from google.cloud import bigquery

TABLE_ID = "harga-pangan-pipeline.raw_pihps.harga_harian"

hari_ini = date.today().isoformat()
waktu_muat = datetime.now(timezone.utc).isoformat()

if len(sys.argv) > 1:
    folder = Path(sys.argv[1])
else:
    folder = Path("data/raw") / hari_ini

if not folder.exists():
    print(f"Folder {folder} tidak ditemukan.")
    raise SystemExit(1)

print(f"Memuat data dari folder: {folder}")

semua_baris = []
for file in sorted(folder.glob("harga_*.json")):
    bagian = file.stem.split("_")
    comcat_id = f"{bagian[1]}_{bagian[2]}"
    price_type_id = int(bagian[4])

    with open(file, encoding="utf-8") as f:
        isi = json.load(f)

    for baris in isi["data"]:
        for kunci, nilai in baris.items():
            if kunci in ("no", "name", "level"):
                continue
            semua_baris.append({
                "tanggal_tarik": hari_ini,
                "price_type_id": price_type_id,
                "comcat_id": comcat_id,
                "wilayah": baris["name"],
                "level": baris["level"],
                "tanggal": kunci,
                "harga": nilai,
                "loaded_at": waktu_muat,
            })

print("Jumlah baris yang akan dimuat:", len(semua_baris))

schema = [
    bigquery.SchemaField("tanggal_tarik", "DATE"),
    bigquery.SchemaField("price_type_id", "INTEGER"),
    bigquery.SchemaField("comcat_id", "STRING"),
    bigquery.SchemaField("wilayah", "STRING"),
    bigquery.SchemaField("level", "INTEGER"),
    bigquery.SchemaField("tanggal", "STRING"),
    bigquery.SchemaField("harga", "STRING"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
]

job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition="WRITE_APPEND",
)

client = bigquery.Client.from_service_account_json("credentials/bq-key.json")
job = client.load_table_from_json(semua_baris, TABLE_ID, job_config=job_config)
job.result()

print(f"Berhasil memuat {job.output_rows} baris ke {TABLE_ID}")