select
  source_url,
  crawl_id,
  cast(observed_at as timestamp) as observed_at,
  nullif(trim(name), '') as product_name,
  nullif(trim(brand), '') as brand_name,
  nullif(trim(sku), '') as sku,
  nullif(trim(gtin), '') as gtin,
  cast(price as decimal(18, 4)) as price,
  upper(currency) as currency,
  availability,
  seller
from {{ source('lakehouse', 'product_offer_snapshot') }}
where price >= 0
