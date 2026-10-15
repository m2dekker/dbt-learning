with

source as (

    select * from {{ source('shop', 'raw_orders') }}

),

renamed as (

    select
        -- ids
        cast(id as integer)           as order_id,
        cast(customer_id as integer)  as customer_id,

        -- strings
        lower(trim(status))           as order_status,

        -- timestamps
        cast(ordered_at as timestamp) as ordered_at

    from source

),

deduplicated as (

    -- the source can deliver the same order twice; keep one row per order_id
    select * from renamed
    qualify row_number() over (partition by order_id order by ordered_at) = 1

)

select * from deduplicated
