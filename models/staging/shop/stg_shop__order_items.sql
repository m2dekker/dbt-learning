with

source as (

    select * from {{ source('shop', 'raw_order_items') }}

),

renamed as (

    select
        -- ids
        cast(id as integer)               as order_item_id,
        cast(order_id as integer)         as order_id,
        cast(product_id as integer)       as product_id,

        -- numerics
        cast(quantity as integer)         as quantity,
        cast(unit_price_cents as integer) as unit_price_cents

    from source

)

select * from renamed
