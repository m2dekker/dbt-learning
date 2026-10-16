with

source as (

    select * from {{ source('shop', 'raw_customers') }}

),

renamed as (

    SELECT
        -- ids
        cast(id as integer)                           as customer_id,

        -- strings
        trim(first_name)                                    as first_name,
        trim(last_name)                               as last_name,
        lower(email)                                  as email,
        cast(upper(trim(country_code)) as varchar(2)) as country_code,

        -- timestamps
        cast(created_at as timestamp)                 as created_at,
        cast(updated_at as timestamp)                 as updated_at

    from source

),

deduplicated as (

    -- the source can deliver the same customer twice; keep one row per customer_id
    select * from renamed
    qualify row_number() over (partition by customer_id order by updated_at desc) = 1

)

select * from deduplicated
