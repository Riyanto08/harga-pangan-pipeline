with harian as (

    select * from {{ ref('fct_harga_harian') }}

),

data_nasional as (

    select
        tanggal,
        price_type_id,
        comcat_id,
        harga as harga_nasional
    from harian
    where tingkat_wilayah = 'Nasional'

),

data_provinsi as (

    select * from harian
    where tingkat_wilayah = 'Provinsi'

)

select
    date_trunc(data_provinsi.tanggal, month) as bulan,
    data_provinsi.nama_jenis_pasar,
    data_provinsi.nama_kategori,
    data_provinsi.nama_komoditas,
    data_provinsi.wilayah as provinsi,
    round(avg(data_provinsi.harga), 0) as rata_harga_provinsi,
    round(avg(data_nasional.harga_nasional), 0) as rata_harga_nasional,
    round(
        safe_divide(
            avg(data_provinsi.harga) - avg(data_nasional.harga_nasional),
            avg(data_nasional.harga_nasional)
        ) * 100,
        2
    ) as selisih_persen,
    count(*) as jumlah_hari_data
from data_provinsi
inner join data_nasional
    on data_provinsi.tanggal = data_nasional.tanggal
    and data_provinsi.price_type_id = data_nasional.price_type_id
    and data_provinsi.comcat_id = data_nasional.comcat_id
group by
    bulan,
    data_provinsi.nama_jenis_pasar,
    data_provinsi.nama_kategori,
    data_provinsi.nama_komoditas,
    data_provinsi.wilayah