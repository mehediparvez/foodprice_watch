# Literature review (starter) — RQ1 and RQ2

Status: DRAFT written 2026-11-11 from web-search result summaries only. No paper was read in full.
Every item below must be opened and checked before it is cited in the report. Items marked [CHECK] had only a secondary description.

Scope (see DEVIATIONS.md 2026-11-11): RQ1 benchmark vs naive; RQ2 value of external drivers beyond persistence.

## 1. Forecasting retail / market food prices — is persistence hard to beat?

- Bangladesh benchmark on AgriPriceBD (arXiv 2604.06227, "A Benchmark of Classical and Deep Learning Models for Agricultural Commodity Price Forecasting on A Novel Bangladeshi Market Price Dataset"). Five commodities, daily, 2020-2025. Reports no single model wins everywhere; accuracy depends on how noisy each series is more than on model complexity. Naive persistence is best for four of five commodities (per the code repo README); Prophet fails on step-like prices. Uses price history only, no external drivers. https://arxiv.org/abs/2604.06227
- Azerbaijan, imported food price index: tree-based ensemble reports 58% out-of-sample R² against a random-walk benchmark, better than ARDL/ARIMAX. Index-level, not retail items. [CHECK] https://econpapers.repec.org/RePEc:aze:wpaper:2601
- Nigeria, fresh produce, monthly: Random Forest up to 5% lower MAPE than baselines, but the baseline was a rolling average, not a random walk. [CHECK] https://www.frontiersin.org/articles/10.3389/frai.2025.1661989
- Turkey: two-stage feature-selection then forecasting using economic indicators. [CHECK] (avesis.hacibayram.edu.tr link from search)
- Ethiopia food price inflation with ML (thesis, etd.hu.edu.et). [CHECK, low priority]
- Bangladesh rice: Daffodil University paper applying five ML algorithms to retail rice prices and drivers; ICCCNT 2020 classifies rice price as reasonable/low/high. Both appear to use small, low-frequency data. [CHECK]

Reading of the gap: gains over simple benchmarks are inconsistent across studies and often measured against weak baselines. I found no study that tests, item by item with a placebo, whether external drivers beat naive for Bangladesh daily retail prices.

## 2. External drivers and pass-through (why drivers might matter)

- Huda (cointegration/ECM, Bangladesh): about 46% of a world price shock passes through to domestic food prices. [CHECK exact source and year]
- Aziz et al. (2013, ageconsearch 168584): exchange-rate pass-through to external prices full, to internal prices partial. [CHECK]
- Mortaza and Rahman (2009): monthly 2000-2008; commodities with a higher domestic supply share have lower import-price pass-through. [CHECK]
- Bangladesh onion NARDL (PLOS ONE, PMC10115283): imported onion prices strongly influence local onion prices; asymmetric transmission across market levels.
- India (RBI review): limited pass-through from international food prices; domestic factors dominate. Cross-country 2007-08 synthesis: elasticities generally below 20%. [CHECK]
- Gap: found no study isolating India's 2023 onion export restrictions on Bangladeshi retail prices. Most pass-through evidence predates 2015.
- Implication for RQ2: pass-through is partial and lagged, so drivers must be joined on their true availability date and may help only some goods. That is consistent with the pre-registered per-group, mapped-items-only design.

## 3. Methods the project relies on

- Forecast accuracy: Hyndman and Koehler (2006), "Another look at measures of forecast accuracy", Int. J. Forecasting. Proposes MASE (error scaled by in-sample naive MAE; below 1 beats in-sample naive). Used here as MASE; also gmean relMAE vs naive.
- Forecast comparison: Diebold and Mariano (1995) test; Harvey, Leybourne and Newbold (1997) small-sample correction (rescale statistic, Student-t with n-1 df). statsmodels `diebold_mariano_test` has a `harvey_adj` option. The HLN correction is formally justified for independent loss differentials; multi-step forecasts can give a negative long-run variance in small samples (Harvey, Leybourne and Whitehouse 2017). Harvey, Leybourne and Zu (2025) address time-varying loss-differential means. [CHECK original papers]
- Global tree models: in the M5 competition (retail sales with prices and calendar), LightGBM dominated; 45 of the top 50 used it, and price and calendar features were important. Cross-learning across series helped. Source is secondary (Kaggle and blog summaries); cite the official M5 papers instead. [CHECK]
- Foundation models: Chronos-2 (arXiv 2510.15821, Amazon) is a 120M-parameter encoder-only zero-shot model that accepts past and known-future covariates. Not implemented here (DEVIATIONS 2026-10-29), so RQ1 does not include it.

## 4. Positioning of this project

1. Existing Bangladesh ML work benchmarks models on price history alone. This project asks whether external drivers add value beyond persistence.
2. It tests each driver group separately, on its mapped goods only, in a fixed order, with a placebo assignment and DM-HLN with Holm correction. A "no gain" result is a valid finding.
3. Data are TCB Dhaka daily retail prices, 63 series, with availability-dated drivers, which avoids look-ahead.

## 5. To do before citing

- Open each [CHECK] item and confirm authors, year, venue, and the specific claim.
- Search more on: commodity price forecastability and random-walk benchmarks (agricultural economics), driver/exogenous-variable forecasting of food prices, Bangladesh rice and edible oil price studies, and the M5 official papers.
- Confirm who wrote AgriPriceBD and its licence before using it as a comparator.
