select coalesce(gtin, sku, product_name) as product_key, date_trunc('day', observed_at) as observation_date,
 count(*) as known_status_count,
 avg(case when availability like '%InStock' then 1.0 else 0.0 end) as availability_rate,
 count(distinct seller) as observed_seller_count
from {{ ref('stg_product_offers') }} where availability is not null group by 1,2
