with harga as (

    select * from {{ ref('stg_pihps__harga_harian') }}

),

komoditas as (

    select * from {{ ref('komoditas') }}

),

jenis_pasar as (

    select * from {{ ref('jenis_pasar') }}

)

select
    harga.tanggal,
    jenis_pasar.nama_jenis_pasar,
    komoditas.nama_kategori,
    komoditas.nama_komoditas,
    komoditas.satuan,
    case
        when harga.level = 0 then 'Nasional'
        else 'Provinsi'
    end as tingkat_wilayah,
    harga.wilayah,
    harga.harga,
    harga.price_type_id,
    harga.comcat_id,
    harga.loaded_at
from harga
left join komoditas
    on harga.comcat_id = komoditas.comcat_id
left join jenis_pasar
    on harga.price_type_id = jenis_pasar.price_type_id