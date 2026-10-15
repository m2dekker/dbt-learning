with

source as (

    select * from {{ source('shop', 'raw_products') }}

),

renamed as (

    select
        -- ids
        cast(id as integer)      as product_id,

        -- strings
        trim(name)               as product_name,
        lower(trim(category))    as product_category,

        -- numerics
        cast(price_cents as integer) as price_cents

    from source

)

select * from renamed
