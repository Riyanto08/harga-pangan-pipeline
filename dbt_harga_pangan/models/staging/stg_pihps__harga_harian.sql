with source as (

    select * from {{ source('raw_pihps', 'harga_harian') }}

),

dibersihkan as (

    select
        price_type_id,
        comcat_id,
        wilayah,
        level,
        parse_date('%d/%m/%Y', tanggal) as tanggal,
        cast(replace(nullif(harga, '-'), ',', '') as int64) as harga,
        tanggal_tarik,
        loaded_at
    from source

),

diberi_nomor as (

    select
        *,
        row_number() over (
            partition by price_type_id, comcat_id, wilayah, tanggal
            order by loaded_at desc
        ) as urutan
    from dibersihkan

)

select
    price_type_id,
    comcat_id,
    wilayah,
    level,
    tanggal,
    harga,
    tanggal_tarik,
    loaded_at
from diberi_nomor
where urutan = 1
  and harga is not null