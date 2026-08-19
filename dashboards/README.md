# 📊 Dashboard specification

![Commerce intelligence dashboard](../assets/dashboard-screenshot.png)

The dashboard application is in `dashboard/`. Run `make dashboard` to rebuild its data payload and PNG screenshot from the curated CSV.

The operations view contains sidebar navigation, market and time filters, five KPI cards, a 14-observation price-index trend, availability gauge, offer-level market comparison, pipeline health and prioritized operational alerts. The 14-point trend is a deterministic validation series used to exercise visualization behavior; it is not presented as observed production history.

## Dashboard pages

| Page | Decision | Measures |
|---|---|---|
| Executive overview | Where does the market need attention? | Offers, products, sellers, validity and freshness |
| Price position | Where are prices uncompetitive? | Median, price index, spread and seller count |
| Assortment gaps | Which products or brands are missing? | Expected range, observed range and gaps |
| Availability risk | Where are stock-outs increasing? | Known availability rate and affected sellers |
| Market risk | What external events may explain change? | Relevant GDELT events, severity and geography |
| Data operations | Can the analysis be trusted? | Coverage, rejects, duplicates, throughput and cost |

## Interpretation

The sample contains three valid offers from two sellers. Trail Runner X1 is $119.99 at Summit Store and $109.99 at City Shoes, a $10 observed difference. The cheaper observation is out of stock, demonstrating why price and availability must be interpreted together. Two of three known observations are in stock, producing a 67% fixture availability rate.

These findings validate transformation and visualization behavior only. They do not describe a real market.
