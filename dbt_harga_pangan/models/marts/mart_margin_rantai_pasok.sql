with harian as (

    select * from {{ ref('fct_harga_harian') }}

),

data_nasional as (

    select
        date_trunc(tanggal, month) as bulan,
        nama_kategori,
        nama_komoditas,
        nama_jenis_pasar,
        harga
    from harian
    where tingkat_wilayah = 'Nasional'

),

rata_bulanan as (

    select
        bulan,
        nama_kategori,
        nama_komoditas,
        avg(if(nama_jenis_pasar = 'Produsen', harga, null)) as harga_produsen,
        avg(if(nama_jenis_pasar = 'Pedagang Besar', harga, null)) as harga_pedagang_besar,
        avg(if(nama_jenis_pasar = 'Pasar Tradisional', harga, null)) as harga_pasar_tradisional,
        avg(if(nama_jenis_pasar = 'Pasar Modern', harga, null)) as harga_pasar_modern
    from data_nasional
    group by
        bulan,
        nama_kategori,
        nama_komoditas

)

select
    bulan,
    nama_kategori,
    nama_komoditas,
    round(harga_produsen, 0) as harga_produsen,
    round(harga_pedagang_besar, 0) as harga_pedagang_besar,
    round(harga_pasar_tradisional, 0) as harga_pasar_tradisional,
    round(harga_pasar_modern, 0) as harga_pasar_modern,
    round(
        safe_divide(harga_pedagang_besar - harga_produsen, harga_produsen) * 100,
        2
    ) as margin_produsen_ke_pedagang_besar_persen,
    round(
        safe_divide(harga_pasar_tradisional - harga_pedagang_besar, harga_pedagang_besar) * 100,
        2
    ) as margin_pedagang_besar_ke_pasar_persen,
    round(
        safe_divide(harga_pasar_tradisional - harga_produsen, harga_produsen) * 100,
        2
    ) as margin_total_persen
from rata_bulanan