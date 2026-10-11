select
    price_type_id,
    comcat_id,
    wilayah,
    tanggal,
    count(*) as jumlah
from {{ ref('stg_pihps__harga_harian') }}
group by
    price_type_id,
    comcat_id,
    wilayah,
    tanggal
having count(*) > 1