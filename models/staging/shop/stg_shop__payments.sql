with

source as (

    select * from {{ source('shop', 'raw_payments') }}

),

renamed as (

    select
        -- ids
        cast(id as integer)           as payment_id,
        cast(order_id as integer)     as order_id,

        -- strings
        lower(trim(payment_method))   as payment_method,

        -- numerics
        cast(amount_cents as integer) as amount_cents,

        -- timestamps
        cast(created_at as timestamp) as paid_at

    from source

)

select * from renamed
