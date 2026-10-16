-- One row per order + product.
-- The source can put the same product on several lines of one order; we merge them here.
-- Lines with quantity 0 are not real sales and are dropped (see data-quality policy).

with

order_items as (

    select * from {{ ref('stg_shop__order_items') }}

),

valid_lines as (

    select * from order_items
    where quantity > 0

),

merged as (

    select
        order_id,
        product_id,
        count(*)                         as source_line_count,
        sum(quantity)                    as quantity,
        sum(quantity * unit_price_cents) as line_amount_cents

    from valid_lines
    group by order_id, product_id

),

final as (

    select
        {{ dbt_utils.generate_surrogate_key(['order_id', 'product_id']) }} as order_product_key,
        order_id,
        product_id,
        quantity,
        line_amount_cents,
        source_line_count

    from merged

)

select * from final
