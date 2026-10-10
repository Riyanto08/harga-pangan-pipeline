from google.cloud import bigquery

client = bigquery.Client.from_service_account_json("credentials/bq-key.json")
print("Terhubung ke project:", client.project)

dataset = client.get_dataset("raw_pihps")
print("Dataset ditemukan:", dataset.dataset_id)
print("Lokasi dataset:", dataset.location)