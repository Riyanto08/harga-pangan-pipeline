with harian as (

    select * from {{ ref('fct_harga_harian') }}

),

data_nasional as (

    select
        tanggal,
        nama_jenis_pasar,
        nama_kategori,
        nama_komoditas,
        harga
    from harian
    where tingkat_wilayah = 'Nasional'

)

select
    date_trunc(tanggal, month) as bulan,
    nama_jenis_pasar,
    nama_kategori,
    nama_komoditas,
    round(avg(harga), 0) as rata_harga,
    min(harga) as harga_terendah,
    max(harga) as harga_tertinggi,
    round(stddev_samp(harga), 0) as simpangan_baku,
    round(safe_divide(stddev_samp(harga), avg(harga)) * 100, 2) as koefisien_variasi_persen,
    round(safe_divide(max(harga) - min(harga), min(harga)) * 100, 2) as rentang_persen,
    count(*) as jumlah_hari_data
from data_nasional
group by
    bulan,
    nama_jenis_pasar,
    nama_kategori,
    nama_komoditas