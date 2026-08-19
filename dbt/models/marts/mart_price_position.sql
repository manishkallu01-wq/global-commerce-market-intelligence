with offers as (
  select *, percentile_cont(0.5) within group (order by price)
    over (partition by coalesce(gtin, sku, product_name), currency, date_trunc('day', observed_at)) as market_median_price
  from {{ ref('stg_product_offers') }}
)
select
  coalesce(gtin, sku, product_name) as product_key,
  currency,
  date_trunc('day', observed_at) as observation_date,
  count(*) as observed_offer_count,
  count(distinct seller) as observed_seller_count,
  min(price) as minimum_price,
  max(price) as maximum_price,
  max(market_median_price) as median_price,
  avg(price / nullif(market_median_price, 0)) as average_price_index
from offers
group by 1, 2, 3
