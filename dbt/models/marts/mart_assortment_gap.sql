select brand_name, date_trunc('week', observed_at) as observation_week,
 count(distinct coalesce(gtin,sku,product_name)) as observed_product_count,
 count(distinct seller) as observed_seller_count
from {{ ref('stg_product_offers') }} where brand_name is not null group by 1,2
