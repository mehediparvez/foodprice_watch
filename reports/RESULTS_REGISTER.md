# Results register

Generated 2026-11-11 16:11 at commit `dc13357`. Every number in reports/ comes from the table below it; each table lists the command that produced it.
Numbers not in this register were not produced by this project. Author: see config.yaml (TO_CONFIRM means no name is used).

## Stage status

| stage | title | status | notes |
|---|---|---|---|
| S00 | Scaffold + intake | done |  |
| S01 | Rebuild TCB panel | done | Palm Olein 2L proposed correction not applied |
| S02 | Audit (human-in-the-loop) | blocked | blocked: original TCB files not supplied (inbox/tcb_originals/ empty) |
| S03 | External intake + cross-checks (WFP, AgriPriceBD, Pink Sheet, OHLC) | pending |  |
| S04 | Driver panel (long table, slots, availability) | done |  |
| S05 | Reproduce baseline | done |  |
| S06 | Core benchmark + driver groups one at a time | done |  |
| S07 | Intervals and alerts | done |  |
| S08 | Locate (WFP monthly market module) | pending |  |
| S09 | Explanation ladder + event studies | done |  |
| S10 | Robustness | done |  |
| S11 | Results pack + clean re-run | in_progress |  |
| S12 | Optional: dashboard | skipped | enable via DECISIONS D1; externally visible: ask first |
| S13 | Optional: extra foundation models | skipped | needs a new seal/prereg; enable via DECISIONS |
| S14 | Optional: data-gap sources (CPI, BB FX, ACLED, GloFAS, hartal) | skipped | enable via DECISIONS D10; user downloads manually |
| S99 | Independent review | pending |  |

## S05 baseline reproduction (ALL stratum)

File `outputs/05_baseline/repro_diff_ALL.csv` · command `python src/stages/s05_score.py` · sha `03cca2d28907bd7e`

| model         |   step |   gmean_relMAE_base |   gmean_relMAE_repro |    diff |   n_items_base |   n_items_repro |   better_base |   better_repro |   worse_base |   worse_repro |   median_MASE_base |   median_MASE_repro |
|:--------------|-------:|--------------------:|---------------------:|--------:|---------------:|----------------:|--------------:|---------------:|-------------:|--------------:|-------------------:|--------------------:|
| AutoARIMA     |      1 |              1.4298 |               1.4928 |  0.063  |             52 |              52 |             0 |              0 |           30 |            32 |             0.5042 |              0.656  |
| AutoARIMA     |      7 |              1.1872 |               1.2276 |  0.0404 |             54 |              54 |             0 |              0 |           19 |            26 |             2.3146 |              2.7437 |
| AutoARIMA     |     14 |              1.1513 |               1.1858 |  0.0345 |             54 |              54 |             0 |              0 |           10 |            11 |             3.7276 |              4.4665 |
| AutoARIMA     |     30 |              1.1312 |               1.1584 |  0.0271 |             54 |              54 |             0 |              0 |            5 |             6 |             6.3955 |              7.6047 |
| AutoETS       |      1 |              1.1682 |               1.1783 |  0.0101 |             52 |              52 |             0 |              0 |           12 |            11 |             0.4474 |              0.4914 |
| AutoETS       |      7 |              1.0466 |               1.0458 | -0.0008 |             54 |              54 |             0 |              0 |            9 |             7 |             2.1175 |              2.3323 |
| AutoETS       |     14 |              1.0378 |               1.0385 |  0.0007 |             54 |              54 |             0 |              0 |            7 |             5 |             3.5282 |              4.0717 |
| AutoETS       |     30 |              1.0328 |               1.0329 |  0.0001 |             54 |              54 |             0 |              0 |            0 |             0 |             6.1872 |              7.4563 |
| AutoTheta     |      1 |              1.301  |               1.5744 |  0.2734 |             52 |              52 |             0 |              0 |           47 |            50 |             0.4476 |              0.6822 |
| AutoTheta     |      7 |              1.1918 |               1.1915 | -0.0003 |             54 |              54 |             1 |              0 |           49 |            49 |             2.4396 |              2.718  |
| AutoTheta     |     14 |              1.1804 |               1.1803 | -0      |             54 |              54 |             0 |              0 |           38 |            39 |             4.0643 |              4.6923 |
| AutoTheta     |     30 |              1.1706 |               1.1583 | -0.0123 |             54 |              54 |             0 |              0 |           12 |            14 |             6.9522 |              7.9503 |
| Naive         |      1 |              1      |               1      |  0      |             52 |              52 |           nan |              0 |          nan |             0 |             0.3892 |              0.4426 |
| Naive         |      7 |              1      |               1      |  0      |             54 |              54 |           nan |              0 |          nan |             0 |             2.0009 |              2.2695 |
| Naive         |     14 |              1      |               1      |  0      |             54 |              54 |           nan |              0 |          nan |             0 |             3.4815 |              3.9721 |
| Naive         |     30 |              1      |               1      |  0      |             54 |              54 |           nan |              0 |          nan |             0 |             5.7742 |              7.0601 |
| RWD           |      1 |              1.269  |               1.2686 | -0.0003 |             52 |              52 |             1 |              0 |           53 |            54 |             0.4562 |              0.5888 |
| RWD           |      7 |              1.3086 |               1.3074 | -0.0011 |             54 |              54 |             1 |              0 |           52 |            52 |             2.4721 |              2.9431 |
| RWD           |     14 |              1.2972 |               1.2959 | -0.0013 |             54 |              54 |             0 |              0 |           46 |            45 |             4.4059 |              5.1661 |
| RWD           |     30 |              1.2767 |               1.2755 | -0.0012 |             54 |              54 |             0 |              0 |           22 |            21 |             7.4878 |              8.845  |
| SeasonalNaive |      1 |              5.1365 |               5.1572 |  0.0207 |             52 |              52 |             0 |              0 |           25 |            24 |             2.1778 |              2.3256 |
| SeasonalNaive |      7 |              1      |               1      |  0      |             54 |              54 |             0 |              0 |            0 |             0 |             2.0009 |              2.2695 |
| SeasonalNaive |     14 |              1      |               1      |  0      |             54 |              54 |             0 |              0 |            0 |             0 |             3.4815 |              3.9721 |
| SeasonalNaive |     30 |              1.1092 |               1.1083 | -0.0009 |             54 |              54 |             0 |              0 |            1 |             1 |             6.7807 |              7.8955 |
| WindowAverage |      1 |              3.2462 |               3.2712 |  0.025  |             52 |              52 |             0 |              0 |           17 |            19 |             1.3566 |              1.514  |
| WindowAverage |      7 |              1.3139 |               1.326  |  0.0121 |             54 |              54 |             0 |              0 |            5 |             5 |             2.6708 |              3.045  |
| WindowAverage |     14 |              1.1382 |               1.1449 |  0.0067 |             54 |              54 |             0 |              0 |            2 |             2 |             4.0755 |              4.7541 |
| WindowAverage |     30 |              1.0581 |               1.0595 |  0.0015 |             54 |              54 |             0 |              0 |            0 |             0 |             6.2607 |              7.5822 |

Max |difference| in gmean relMAE: 0.2734 (tolerance 0.02).

## T1

File `reports/tables/T1.csv` · stage S01 · command `python src/stages/s01.py` · rows 7 · sha `1ff370b8998843fb` · stage commit `dc13357`

| eval_stratum        |   n_series |   report_days |   share_unchanged_median |   share_missing | first_report   |
|:--------------------|-----------:|--------------:|-------------------------:|----------------:|:---------------|
| administered        |          7 |          1412 |                    0.848 |          0.0145 | 2021-05-17     |
| domestic_staple     |          7 |          1412 |                    0.906 |          0.0007 | 2021-05-17     |
| imported_staple     |         19 |          1412 |                    0.932 |          0.0203 | 2021-05-17     |
| non_food            |          3 |          1412 |                    0.918 |          0.0007 | 2021-05-17     |
| short_history       |          9 |           591 |                    0.928 |          0.0946 | 2024-05-20     |
| spice               |          8 |          1412 |                    0.892 |          0.0006 | 2021-05-17     |
| volatile_perishable |         10 |          1412 |                    0.874 |          0.0186 | 2021-05-17     |

## T10

File `reports/tables/T10.csv` · stage S09 · command `python src/stages/s09_score.py` · rows 7 · sha `f41a186f9142c586` · stage commit `dc13357`

| event                                                            | date_confidence                                                               | origin     |   h |   n_items |   mean_abnormal_log_change |   mean_abnormal_pct |   placebo_mean |   p_one_sided |   n_placebo |
|:-----------------------------------------------------------------|:------------------------------------------------------------------------------|:-----------|----:|----------:|---------------------------:|--------------------:|---------------:|--------------:|------------:|
| India onion export ban (verified 2023-12-08)                     | verified                                                                      | 2023-12-07 |   7 |         2 |                     0.0802 |              8.3548 |         0.0055 |        0.1235 |         200 |
| India onion export ban (verified 2023-12-08)                     | verified                                                                      | 2023-12-07 |  14 |         2 |                     0.0358 |              3.6476 |        -0.0167 |        0.2715 |         200 |
| India onion export ban (verified 2023-12-08)                     | verified                                                                      | 2023-12-07 |  30 |         2 |                    -0.1275 |            -11.9747 |        -0.0152 |        0.7425 |         200 |
| BDT/USD jump 2024-05-10 (+6.3% in one day; largest 2024-25 move) | data                                                                          | 2024-05-09 |   7 |        24 |                     0.005  |              0.499  |         0.002  |        0.2265 |         200 |
| BDT/USD jump 2024-05-10 (+6.3% in one day; largest 2024-25 move) | data                                                                          | 2024-05-09 |  14 |        24 |                     0.007  |              0.7013 |        -0.0039 |        0.107  |         200 |
| BDT/USD jump 2024-05-10 (+6.3% in one day; largest 2024-25 move) | data                                                                          | 2024-05-09 |  30 |        24 |                     0.0233 |              2.3569 |         0.0068 |        0.129  |         200 |
| Sep 2023 price caps                                              | not studied: no dated, sourced cap event in the project files (DECISIONS D10) | nan        | nan |       nan |                   nan      |            nan      |       nan      |      nan      |         nan |

## T11

File `reports/tables/T11.csv` · stage S10 · command `python src/stages/s10.py` · rows 22 · sha `7c7c03b0c186ab4a` · stage commit `dc13357`

| check                                                                                       |    value | note                                                |
|:--------------------------------------------------------------------------------------------|---------:|:----------------------------------------------------|
| baseline (pre-registered conformal rule)                                                    |   0.5833 | share of 12 events detected                         |
| placebo event dates (200 draws, same items and window lengths)                              |   0.4788 | 95% range 0.25-0.67; p(placebo >= observed) = 0.285 |
| leave-one-event-out recall                                                                  |   0.5833 | min 0.55, max 0.64                                  |
| events with confidence >= medium                                                            |   0.6    | 5 events                                            |
| events with confidence >= high                                                              |   1      | 1 events                                            |
| exclude events tied to reconstructed exporter dates (BD-S12)                                |   0.5455 | BD-S13 kept: ban date verified                      |
| alternative rule robust z>=1                                                                |   0.6667 | 3-of-5 persistence                                  |
| alternative rule robust z>=2                                                                |   0.5    | 3-of-5 persistence                                  |
| alternative rule robust z>=3                                                                |   0.5    | 3-of-5 persistence                                  |
| LightGBM core expanding window, h=1                                                         |   1.0008 | gmean relMAE vs naive (reference)                   |
| LightGBM core sliding 500-report-day window, h=1                                            |   1.0003 | gmean relMAE vs naive                               |
| LightGBM core, ginger 2021 candidates removed from targets, h=1                             |   1.0009 | gmean relMAE vs naive                               |
| LightGBM core expanding window, h=7                                                         |   1.0153 | gmean relMAE vs naive (reference)                   |
| LightGBM core sliding 500-report-day window, h=7                                            |   1.0226 | gmean relMAE vs naive                               |
| LightGBM core, ginger 2021 candidates removed from targets, h=7                             |   1.0154 | gmean relMAE vs naive                               |
| LightGBM core expanding window, h=14                                                        |   1.0285 | gmean relMAE vs naive (reference)                   |
| LightGBM core sliding 500-report-day window, h=14                                           |   1.0369 | gmean relMAE vs naive                               |
| LightGBM core, ginger 2021 candidates removed from targets, h=14                            |   1.0213 | gmean relMAE vs naive                               |
| LightGBM core expanding window, h=30                                                        |   1.0848 | gmean relMAE vs naive (reference)                   |
| LightGBM core sliding 500-report-day window, h=30                                           |   1.1342 | gmean relMAE vs naive                               |
| LightGBM core, ginger 2021 candidates removed from targets, h=30                            |   1.0822 | gmean relMAE vs naive                               |
| not run: weekly vs daily aggregation; Min/Max instead of Avg targets; RQ5 locate robustness | nan      | logged in DEVIATIONS.md                             |

## T1_late_starters

File `reports/tables/T1_late_starters.csv` · stage S01 · command `python src/stages/s01.py` · rows 2 · sha `83b688e1535fdc7a` · stage commit `dc13357`

| item_id                           | first_date   |
|:----------------------------------|:-------------|
| Rice Bran Oil - Bottled | 5 litre | 2024-05-20   |
| Soybean Oil - Bottled | 2 litre   | 2024-09-03   |

## T3

File `reports/tables/T3.csv` · stage S04 · command `python src/stages/s04.py` · rows 11 · sha `11b15dd905a88d9c` · stage commit `dc13357`

| slot                  | role             | source                                                                                                   | frequency           | availability        | carry_cap             |   n_items | first_date   | last_date   |
|:----------------------|:-----------------|:---------------------------------------------------------------------------------------------------------|:--------------------|:--------------------|:----------------------|----------:|:-------------|:------------|
| G0 calendar           | forecast+explain | Ramadan/Eid, holidays, month, dow                                                                        | daily (known ahead) | 0                   | nan                   |       nan | nan          | nan         |
| G1 own_world_price    | forecast+explain | IMF PSOIL/PPOIL/PWHEAMT/PRICENPQ/PMILK (log USD, 3m change)                                              | monthly             | month end + 40 d    | 45 d                  |        17 | 2021-05-17   | 2026-10-24  |
| G2 own_brent          | forecast+explain | FRED Brent (log, 30d change)                                                                             | daily               | as of date          | 7 d                   |         5 | 2021-05-17   | 2026-10-24  |
| G3 own_export_measure | forecast+explain | India onion duty/MEP/ban (reconstructed)                                                                 | event               | start date          | coverage only         |         2 | 2022-05-06   | 2025-03-27  |
| G4 own_fishing_ban    | forecast+explain | hilsa 22-day, jatka, marine bans                                                                         | event               | announced dates     | nan                   |         1 | 2021-05-17   | 2026-10-24  |
| G5 weather_1..3       | forecast+explain | chosen on 2024: wx_bd_tmax_7d, wx_bd_tmean_30d, wx_bd_rain_7d                                            | daily               | +5 d                | 7 d                   |         7 | 2021-05-17   | 2026-10-24  |
| E1 fx                 | explain          | BDT/USD spliced (npm from 2024-03-02, Yahoo x1.0151 before)                                              | daily               | as of date          | 7 d                   |        34 | 2021-05-17   | 2026-10-24  |
| E2 diesel             | explain          | diesel administered price                                                                                | event               | effective date      | nan                   |        63 | 2021-05-17   | 2026-10-24  |
| E3 imports            | explain          | Comtrade mirror tonnes + unit value by HS                                                                | monthly             | month start + 208 d | 45 d                  |        33 | 2021-07-28   | 2026-10-24  |
| E4 events             | explain          | exporter measures (rice/wheat/sugar/palm), disruptions, cyclones/floods +14 d, duty cuts, interim regime | event               | event dates         | out of coverage = NaN |        57 | 2023-10-28   | 2025-11-17  |
| E5 world (explain)    | explain          | IMF PSUGAISA (sugar), PCHANA (chickpea)                                                                  | monthly             | month end + 40 d    | 45 d                  |         2 | 2021-05-17   | 2026-10-24  |

## T4

File `reports/tables/T4.csv` · stage S06 · command `python src/stages/s06_score.py` · rows 252 · sha `8f8f7cff0d4fb5d7` · stage commit `dc13357`

| eval_stratum    | model         |   step |   gmean_relMAE |   win_rate |   median_MASE |   n_items |   better |   worse |
|:----------------|:--------------|-------:|---------------:|-----------:|--------------:|----------:|---------:|--------:|
| imported_staple | AutoARIMA     |      1 |         1.5018 |     0.0526 |        1.1328 |        19 |        0 |      10 |
| imported_staple | AutoARIMA     |      7 |         1.3123 |     0.0526 |        4.0252 |        19 |        0 |      14 |
| imported_staple | AutoARIMA     |     14 |         1.2808 |     0.0526 |        6.5051 |        19 |        0 |      11 |
| imported_staple | AutoARIMA     |     30 |         1.2433 |     0.1579 |       11.1655 |        19 |        0 |       5 |
| imported_staple | AutoETS       |      1 |         1.1217 |     0.1579 |        0.8691 |        19 |        0 |       5 |
| imported_staple | AutoETS       |      7 |         1.0763 |     0.1579 |        2.7375 |        19 |        0 |       4 |
| imported_staple | AutoETS       |     14 |         1.0666 |     0.1053 |        4.967  |        19 |        0 |       3 |
| imported_staple | AutoETS       |     30 |         1.0562 |     0.2105 |        8.1481 |        19 |        0 |       1 |
| imported_staple | AutoTheta     |      1 |         1.4684 |     0.0526 |        1.1399 |        19 |        0 |      16 |
| imported_staple | AutoTheta     |      7 |         1.2067 |     0      |        3.4891 |        19 |        0 |      17 |
| imported_staple | AutoTheta     |     14 |         1.1928 |     0      |        5.527  |        19 |        0 |      17 |
| imported_staple | AutoTheta     |     30 |         1.1614 |     0      |        9.4785 |        19 |        0 |       6 |
| imported_staple | LGBM_M1       |      1 |         1.0011 |     0.1579 |        0.7576 |        19 |        0 |       0 |
| imported_staple | LGBM_M1       |      7 |         1.0153 |     0.1053 |        2.7638 |        19 |        0 |       4 |
| imported_staple | LGBM_M1       |     14 |         1.0266 |     0.0526 |        5.0151 |        19 |        0 |       5 |
| imported_staple | LGBM_M1       |     30 |         1.0779 |     0.0526 |        9.055  |        19 |        0 |       0 |
| imported_staple | LGBM_core     |      1 |         1.0006 |     0.2632 |        0.7601 |        19 |        0 |       0 |
| imported_staple | LGBM_core     |      7 |         1.0147 |     0.0526 |        2.7603 |        19 |        0 |       1 |
| imported_staple | LGBM_core     |     14 |         1.0359 |     0.0526 |        5.0549 |        19 |        0 |       5 |
| imported_staple | LGBM_core     |     30 |         1.0803 |     0.0526 |        8.5046 |        19 |        0 |       2 |
| imported_staple | Naive         |      1 |         1      |     0      |        0.7576 |        19 |        0 |       0 |
| imported_staple | Naive         |      7 |         1      |     0      |        2.7375 |        19 |        0 |       0 |
| imported_staple | Naive         |     14 |         1      |     0      |        4.8061 |        19 |        0 |       0 |
| imported_staple | Naive         |     30 |         1      |     0      |        8.0377 |        19 |        0 |       0 |
| imported_staple | RWD           |      1 |         1.2656 |     0      |        0.9889 |        19 |        0 |      19 |
| imported_staple | RWD           |      7 |         1.3412 |     0      |        3.7084 |        19 |        0 |      18 |
| imported_staple | RWD           |     14 |         1.3253 |     0      |        6.6645 |        19 |        0 |      18 |
| imported_staple | RWD           |     30 |         1.2932 |     0      |       11.6261 |        19 |        0 |       9 |
| imported_staple | SeasonalNaive |      1 |         4.0476 |     0      |        2.8532 |        19 |        0 |      10 |
| imported_staple | SeasonalNaive |      7 |         1      |     0      |        2.7375 |        19 |        0 |       0 |
| imported_staple | SeasonalNaive |     14 |         1      |     0      |        4.8061 |        19 |        0 |       0 |
| imported_staple | SeasonalNaive |     30 |         1.1123 |     0      |        9.0091 |        19 |        0 |       1 |
| imported_staple | WindowAverage |      1 |         2.7006 |     0      |        2.1212 |        19 |        0 |       7 |
| imported_staple | WindowAverage |      7 |         1.3302 |     0      |        3.7224 |        19 |        0 |       6 |
| imported_staple | WindowAverage |     14 |         1.1617 |     0      |        5.5619 |        19 |        0 |       2 |
| imported_staple | WindowAverage |     30 |         1.0636 |     0.0526 |        8.7037 |        19 |        0 |       0 |
| spice           | AutoARIMA     |      1 |         1.6026 |     0      |        0.3956 |         8 |        0 |       8 |
| spice           | AutoARIMA     |      7 |         1.182  |     0      |        1.8482 |         8 |        0 |       4 |
| spice           | AutoARIMA     |     14 |         1.1344 |     0      |        2.9604 |         8 |        0 |       3 |
| spice           | AutoARIMA     |     30 |         1.1259 |     0.125  |        5.121  |         8 |        0 |       0 |
| spice           | AutoETS       |      1 |         1.1894 |     0      |        0.3583 |         8 |        0 |       3 |
| spice           | AutoETS       |      7 |         1.0606 |     0.125  |        1.6018 |         8 |        0 |       2 |
| spice           | AutoETS       |     14 |         1.0507 |     0.375  |        2.5064 |         8 |        0 |       2 |
| spice           | AutoETS       |     30 |         1.0485 |     0.375  |        4.401  |         8 |        0 |       0 |
| spice           | AutoTheta     |      1 |         1.859  |     0      |        0.4882 |         8 |        0 |       8 |
| spice           | AutoTheta     |      7 |         1.2023 |     0      |        1.8564 |         8 |        0 |       8 |
| spice           | AutoTheta     |     14 |         1.205  |     0      |        2.825  |         8 |        0 |       7 |
| spice           | AutoTheta     |     30 |         1.2175 |     0      |        5.115  |         8 |        0 |       5 |
| spice           | LGBM_M1       |      1 |         0.9988 |     0.375  |        0.2783 |         8 |        0 |       0 |
| spice           | LGBM_M1       |      7 |         1.0145 |     0      |        1.6012 |         8 |        0 |       0 |
| spice           | LGBM_M1       |     14 |         1.0173 |     0      |        2.534  |         8 |        0 |       0 |
| spice           | LGBM_M1       |     30 |         1.0595 |     0      |        4.6918 |         8 |        0 |       0 |
| spice           | LGBM_core     |      1 |         1.0012 |     0.125  |        0.2783 |         8 |        0 |       0 |
| spice           | LGBM_core     |      7 |         1.0172 |     0.125  |        1.6181 |         8 |        0 |       1 |
| spice           | LGBM_core     |     14 |         1.0282 |     0      |        2.5742 |         8 |        0 |       1 |
| spice           | LGBM_core     |     30 |         1.1077 |     0      |        4.7022 |         8 |        0 |       0 |
| spice           | Naive         |      1 |         1      |     0      |        0.2783 |         8 |        0 |       0 |
| spice           | Naive         |      7 |         1      |     0      |        1.5927 |         8 |        0 |       0 |
| spice           | Naive         |     14 |         1      |     0      |        2.5205 |         8 |        0 |       0 |
| spice           | Naive         |     30 |         1      |     0      |        4.4078 |         8 |        0 |       0 |

(first 60 of 252 rows; full table in the CSV)

## T5

File `reports/tables/T5.csv` · stage S06 · command `python src/stages/s06_score.py` · rows 231 · sha `98c2232aa913b4e1` · stage commit `dc13357`

| group   | kind    | item_id                                          |   step |   relMAE_core |   relMAE_variant |   delta_relMAE |       dm |        p | relMAE_variant_vs_naive_lt1   |   p_holm | sig_better_than_core   | sig_worse_than_core   |
|:--------|:--------|:-------------------------------------------------|-------:|--------------:|-----------------:|---------------:|---------:|---------:|:------------------------------|---------:|:-----------------------|:----------------------|
| G1      | matched | Atta (Wheat Flour) - Loose | per kg              |      1 |        1      |           0.998  |        -0.002  |  -0.9671 |   0.3362 | True                          |   1      | False                  | False                 |
| G1      | matched | Atta (Wheat Flour) - Packet | per kg (packet)    |      1 |        1      |           1      |        -0      | nan      | nan      | False                         | nan      | False                  | False                 |
| G1      | matched | Maida (Refined Flour) - Loose | per kg           |      1 |        1      |           1      |         0      |   1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | matched | Maida (Refined Flour) - Packet | per kg (packet) |      1 |        1.0341 |           1.0137 |        -0.0204 |  -0.8784 |   0.3822 | False                         |   1      | False                  | False                 |
| G1      | matched | Palm Oil - Loose | per litre                     |      1 |        1      |           1.0008 |         0.0008 |   0.3764 |   0.7075 | False                         |   1      | False                  | False                 |
| G1      | matched | Powdered Milk - Dano | 1 kg                      |      1 |        0.9956 |           1      |         0.0044 |   0.9845 |   0.3276 | False                         |   1      | False                  | False                 |
| G1      | matched | Powdered Milk - Diploma (New Zealand) | 1 kg     |      1 |        1      |           1      |         0      |   1.0114 |   0.3147 | False                         |   1      | False                  | False                 |
| G1      | matched | Powdered Milk - Fresh | 1 kg                     |      1 |        1      |           1      |        -0      |  -1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | matched | Powdered Milk - Marks | 1 kg                     |      1 |        1      |           1      |        -0      |  -1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | matched | Rice - Coarse (Swarna/China IRRI) | per kg       |      1 |        1      |           1      |        -0      |  -1.181  |   0.2409 | False                         |   1      | False                  | False                 |
| G1      | matched | Rice - Fine (Nazir/Miniket) | per kg             |      1 |        1      |           1      |        -0      |  -1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | matched | Rice - Medium (Paijam) | per kg                  |      1 |        1      |           1.0001 |         0.0001 |   0.9776 |   0.331  | False                         |   1      | False                  | False                 |
| G1      | matched | Soybean Oil - Bottled | 1 litre                  |      1 |        1      |           1.0053 |         0.0053 |   1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | matched | Soybean Oil - Bottled | 2 litre                  |      1 |        1      |           1.0136 |         0.0136 |   1.439  |   0.1538 | False                         |   1      | False                  | False                 |
| G1      | matched | Soybean Oil - Bottled | 5 litre                  |      1 |        1      |           1      |         0      | nan      | nan      | False                         | nan      | False                  | False                 |
| G1      | matched | Soybean Oil - Loose | per litre                  |      1 |        1      |           1.001  |         0.001  |   0.5171 |   0.6064 | False                         |   1      | False                  | False                 |
| G1      | matched | Super Palm Oil - Loose | per litre               |      1 |        1      |           0.9987 |        -0.0013 |  -0.9373 |   0.3512 | True                          |   1      | False                  | False                 |
| G1      | placebo | Chicken - Broiler | per kg                       |      1 |        1.0009 |           1      |        -0.0009 |  -0.9686 |   0.3355 | True                          |   1      | False                  | False                 |
| G1      | placebo | Chickpea (by quality) | per kg                   |      1 |        1      |           1.0009 |         0.0009 |   1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | placebo | Coriander Seed | per kg                          |      1 |        1      |           1      |        -0      |  -1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | placebo | Dates (Ordinary Quality) | per kg                |      1 |        1      |           1.0051 |         0.0051 |   1.0115 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | placebo | Dried Chilli - Local | per kg                    |      1 |        1.0029 |           1      |        -0.0029 |  -0.6656 |   0.5075 | False                         |   1      | False                  | False                 |
| G1      | placebo | Egg - Farm | per hali (4 pcs)                    |      1 |        1.0016 |           1.0017 |         0.0001 |   0.3237 |   0.7469 | False                         |   1      | False                  | False                 |
| G1      | placebo | Garlic - Imported | per kg                       |      1 |        1      |           1      |        -0      |  -1.4624 |   0.1473 | True                          |   1      | False                  | False                 |
| G1      | placebo | Garlic - Local | per kg                          |      1 |        1      |           1.001  |         0.0011 |   1.323  |   0.1894 | False                         |   1      | False                  | False                 |
| G1      | placebo | Lentil (Masur) - Small Grain | per kg            |      1 |        1      |           1      |         0      |   1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | placebo | MS Rod (40 Grade) | per metric ton               |      1 |        1.0002 |           1      |        -0.0002 |  -1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | placebo | MS Rod (60 Grade) | per metric ton               |      1 |        1.0075 |           1      |        -0.0075 |  -1.0116 |   0.3146 | False                         |   1      | False                  | False                 |
| G1      | placebo | Mung Dal (by quality) | per kg                   |      1 |        1      |           1      |         0      |   0.9231 |   0.3585 | False                         |   1      | False                  | False                 |
| G1      | placebo | Onion - Imported | per kg                        |      1 |        1.0007 |           1      |        -0.0007 |  -0.4104 |   0.687  | False                         |   1      | False                  | False                 |
| G1      | placebo | Onion - Local | per kg                           |      1 |        1.0044 |           1.0016 |        -0.0028 |  -1.2702 |   0.2075 | False                         |   1      | False                  | False                 |
| G1      | placebo | Potato | per kg                                  |      1 |        1.0007 |           1.0033 |         0.0026 |   0.7994 |   0.4263 | False                         |   1      | False                  | False                 |
| G1      | placebo | Rice Bran Oil - Bottled | 5 litre                |      1 |        1      |           1      |         0      | nan      | nan      | False                         | nan      | False                  | False                 |
| G1      | placebo | Sugar | per kg                                   |      1 |        1      |           1      |        -0      |  -1.7695 |   0.0804 | False                         |   1      | False                  | False                 |
| G1      | matched | Atta (Wheat Flour) - Loose | per kg              |      7 |        1.0067 |           1.0052 |        -0.0015 |  -0.4233 |   0.6732 | False                         |   1      | False                  | False                 |
| G1      | matched | Atta (Wheat Flour) - Packet | per kg (packet)    |      7 |        1.0114 |           1.0212 |         0.0098 |   1.6482 |   0.103  | False                         |   0.8241 | False                  | False                 |
| G1      | matched | Maida (Refined Flour) - Loose | per kg           |      7 |        1.009  |           1.0091 |         0.0001 |   0.0254 |   0.9798 | False                         |   1      | False                  | False                 |
| G1      | matched | Maida (Refined Flour) - Packet | per kg (packet) |      7 |        1.0009 |           1.0104 |         0.0094 |   1.9727 |   0.0518 | False                         |   0.5695 | False                  | False                 |
| G1      | matched | Palm Oil - Loose | per litre                     |      7 |        0.9859 |           1.0172 |         0.0313 |   1.9706 |   0.052  | False                         |   0.5695 | False                  | False                 |
| G1      | matched | Powdered Milk - Dano | 1 kg                      |      7 |        1.0136 |           1.0474 |         0.0339 |   2.4486 |   0.0164 | False                         |   0.2296 | False                  | False                 |
| G1      | matched | Powdered Milk - Diploma (New Zealand) | 1 kg     |      7 |        1.0338 |           1.0791 |         0.0452 |   1.8189 |   0.0724 | False                         |   0.652  | False                  | False                 |
| G1      | matched | Powdered Milk - Fresh | 1 kg                     |      7 |        1.0231 |           1.0769 |         0.0538 |   2.0365 |   0.0448 | False                         |   0.5378 | False                  | False                 |
| G1      | matched | Powdered Milk - Marks | 1 kg                     |      7 |        1.0232 |           1.0634 |         0.0402 |   2.1227 |   0.0367 | False                         |   0.477  | False                  | False                 |
| G1      | matched | Rice - Coarse (Swarna/China IRRI) | per kg       |      7 |        1.0116 |           1.011  |        -0.0006 |  -0.1094 |   0.9131 | False                         |   1      | False                  | False                 |
| G1      | matched | Rice - Fine (Nazir/Miniket) | per kg             |      7 |        1.0023 |           1.0121 |         0.0099 |   1.442  |   0.153  | False                         |   0.9179 | False                  | False                 |
| G1      | matched | Rice - Medium (Paijam) | per kg                  |      7 |        1.0036 |           0.9965 |        -0.0071 |  -0.9786 |   0.3306 | True                          |   1      | False                  | False                 |
| G1      | matched | Soybean Oil - Bottled | 1 litre                  |      7 |        1.0187 |           1.0935 |         0.0748 |   3.3592 |   0.0012 | False                         |   0.0188 | False                  | True                  |
| G1      | matched | Soybean Oil - Bottled | 2 litre                  |      7 |        1.0057 |           1.095  |         0.0894 |   5.1036 |   0      | False                         |   0      | False                  | True                  |
| G1      | matched | Soybean Oil - Bottled | 5 litre                  |      7 |        1.0506 |           1.1422 |         0.0917 |   3.2639 |   0.0016 | False                         |   0.0238 | False                  | True                  |
| G1      | matched | Soybean Oil - Loose | per litre                  |      7 |        1.0071 |           1.0212 |         0.0142 |   1.6005 |   0.1132 | False                         |   0.8241 | False                  | False                 |
| G1      | matched | Super Palm Oil - Loose | per litre               |      7 |        1.0128 |           1.0293 |         0.0165 |   1.1751 |   0.2432 | False                         |   1      | False                  | False                 |
| G1      | placebo | Chicken - Broiler | per kg                       |      7 |        1.0063 |           1.0054 |        -0.001  |  -0.1569 |   0.8757 | False                         |   1      | False                  | False                 |
| G1      | placebo | Chickpea (by quality) | per kg                   |      7 |        1.0116 |           1.0101 |        -0.0015 |  -0.3039 |   0.762  | False                         |   1      | False                  | False                 |
| G1      | placebo | Coriander Seed | per kg                          |      7 |        1.0087 |           1.0181 |         0.0094 |   1.387  |   0.1691 | False                         |   1      | False                  | False                 |
| G1      | placebo | Dates (Ordinary Quality) | per kg                |      7 |        1.0139 |           1.0113 |        -0.0025 |  -0.4191 |   0.6762 | False                         |   1      | False                  | False                 |
| G1      | placebo | Dried Chilli - Local | per kg                    |      7 |        1.0379 |           1.0179 |        -0.0199 |  -1.4486 |   0.1511 | False                         |   1      | False                  | False                 |
| G1      | placebo | Egg - Farm | per hali (4 pcs)                    |      7 |        1.0063 |           1.0139 |         0.0076 |   0.9152 |   0.3627 | False                         |   1      | False                  | False                 |
| G1      | placebo | Garlic - Imported | per kg                       |      7 |        1.0043 |           1.0003 |        -0.004  |  -1.0578 |   0.2932 | False                         |   1      | False                  | False                 |
| G1      | placebo | Garlic - Local | per kg                          |      7 |        0.9991 |           1.0045 |         0.0055 |   0.5964 |   0.5525 | False                         |   1      | False                  | False                 |
| G1      | placebo | Lentil (Masur) - Small Grain | per kg            |      7 |        0.999  |           1.0131 |         0.0141 |   3.2054 |   0.0019 | False                         |   0.0323 | False                  | True                  |

(first 60 of 231 rows; full table in the CSV)

## T5b

File `reports/tables/T5b.csv` · stage S06 · command `python src/stages/s06_score.py` · rows 19 · sha `fdd98da31f63c636` · stage commit `dc13357`

| group   |   step |   n_matched |   n_placebo |   mean_delta_matched | ci_matched                                       |   mean_delta_placebo | ci_placebo                                     |     gap | gap_ci                                          |   n_sig_better_matched |   n_sig_better_placebo |   share_beats_naive_matched |   share_beats_naive_placebo |
|:--------|-------:|------------:|------------:|---------------------:|:-------------------------------------------------|---------------------:|:-----------------------------------------------|--------:|:------------------------------------------------|-----------------------:|-----------------------:|----------------------------:|----------------------------:|
| G1      |      1 |          17 |          17 |               0.0001 | (-0.003287355479329126, 0.0028874227176177796)   |              -0.0003 | (-0.0015864221980084938, 0.000792238551032097) |  0.0004 | (-0.002887615454648564, 0.003437338808399474)   |                      0 |                      0 |                      0.1176 |                      0.1176 |
| G1      |      7 |          17 |          17 |               0.0301 | (0.01630345684136006, 0.045422213799112855)      |               0.003  | (-0.0021724851533975933, 0.00799352404929173)  |  0.027  | (0.012118216539275906, 0.04282128321357513)     |                      0 |                      0 |                      0.0588 |                      0.0588 |
| G1      |     14 |          17 |          17 |               0.0164 | (0.000557042927382071, 0.03349564806106012)      |               0.002  | (-0.005373458988542748, 0.008342046020486556)  |  0.0144 | (-0.002414895766836665, 0.032682725148602404)   |                      0 |                      0 |                      0      |                      0.0588 |
| G1      |     30 |          17 |          17 |               0.0266 | (-0.0015849992504723236, 0.05511231189299759)    |               0.0089 | (-0.006982167853232389, 0.026195569333712396)  |  0.0176 | (-0.014229490108490723, 0.04929283473590535)    |                      0 |                      0 |                      0.1176 |                      0.0588 |
| G2      |      1 |           5 |           5 |               0.0022 | (-0.0008081882657694717, 0.005285914525015145)   |               0.0038 | (5.0075927920945066e-08, 0.009532842132321218) | -0.0016 | (-0.0074558855062098585, 0.0038817628037966737) |                      0 |                      0 |                      0      |                      0      |
| G2      |      7 |           5 |           5 |               0.0007 | (-0.018619184534823186, 0.02146636108215825)     |              -0.0044 | (-0.010462271006916124, 0.0011016412702386624) |  0.0052 | (-0.013899272124498478, 0.02619905360384174)    |                      0 |                      0 |                      0      |                      0      |
| G2      |     14 |           5 |           5 |              -0.0043 | (-0.03341923574452314, 0.017853425700456293)     |              -0.0036 | (-0.012867160891236028, 0.0051828584328710734) | -0.0008 | (-0.03025967554688585, 0.024063097741289587)    |                      0 |                      0 |                      0      |                      0      |
| G2      |     30 |           5 |           5 |               0.0068 | (-0.03037458879032373, 0.04947358065162226)      |               0.0237 | (-0.0035690779031214426, 0.050771678753205055) | -0.0169 | (-0.06329203939462599, 0.03394642230051215)     |                      0 |                      0 |                      0      |                      0      |
| G3      |      1 |           2 |           2 |              -0.0026 | (-0.004412940188804004, -0.0007421811924255284)  |               0.0022 | (0.0, 0.004375475924018435)                    | -0.0048 | (-0.00878841611282244, -0.0007421811924255284)  |                      0 |                      0 |                      0      |                      0      |
| G3      |      7 |           2 |           2 |              -0.0014 | (-0.0025450740475427835, -0.0002246976872460893) |               0.0122 | (0.001984712046523507, 0.02234369365987665)    | -0.0135 | (-0.024888767707419435, -0.002209409733769596)  |                      0 |                      0 |                      0.5    |                      0      |
| G3      |     14 |           2 |           2 |               0.0216 | (0.008771605290659679, 0.03437868160088842)      |              -0.0112 | (-0.01157605127578587, -0.010850002706293105)  |  0.0328 | (0.019621607996952783, 0.04595473287667429)     |                      0 |                      0 |                      0      |                      0.5    |
| G3      |     30 |           2 |           2 |               0.0477 | (-0.000341017396644272, 0.09574075612953536)     |               0.0091 | (-0.02724056355461313, 0.04534254047765618)    |  0.0386 | (-0.04568355787430045, 0.1229813196841485)      |                      0 |                      0 |                      0      |                      0.5    |
| G4      |      7 |           1 |           1 |              -0.0159 | (-0.015891831945858526, -0.015891831945858526)   |              -0.0844 | (-0.0844053827109228, -0.0844053827109228)     |  0.0685 | (0.06851355076506427, 0.06851355076506427)      |                      0 |                      1 |                      0      |                      0      |
| G4      |     14 |           1 |           1 |               0.0027 | (0.0027120913396794233, 0.0027120913396794233)   |              -0.0179 | (-0.017861880388069906, -0.017861880388069906) |  0.0206 | (0.02057397172774933, 0.02057397172774933)      |                      0 |                      0 |                      0      |                      0      |
| G4      |     30 |           1 |           1 |              -0.0103 | (-0.010302319973780394, -0.010302319973780394)   |              -0.0751 | (-0.07514719720823759, -0.07514719720823759)   |  0.0648 | (0.0648448772344572, 0.0648448772344572)        |                      0 |                      0 |                      0      |                      0      |
| G5      |      1 |           4 |           4 |               0.0005 | (-0.0013728200980492877, 0.002716347343577563)   |               0.0098 | (0.00016566754342706158, 0.027284001545113845) | -0.0093 | (-0.026838661248862472, 0.0012235668551958676)  |                      0 |                      0 |                      0      |                      0      |
| G5      |      7 |           4 |           4 |               0.0004 | (-0.009996213065699866, 0.010519496884307089)    |               0.0222 | (0.005569042724913431, 0.04289177415978229)    | -0.0218 | (-0.04500840457786411, 0.00026582106159639407)  |                      0 |                      0 |                      0.25   |                      0      |
| G5      |     14 |           4 |           4 |              -0.0366 | (-0.08919907414557576, 0.01001175006432542)      |               0.0156 | (-0.007617802489770731, 0.03876712301221952)   | -0.0521 | (-0.11327151084592374, -0.0008966077746004529)  |                      0 |                      0 |                      0.25   |                      0      |
| G5      |     30 |           4 |           4 |              -0.061  | (-0.12684488257773588, -0.011706585873079045)    |               0.0572 | (-0.04626162445910653, 0.15396167256440174)    | -0.1182 | (-0.23251616249881216, -0.0022507162018171054)  |                      0 |                      0 |                      0.5    |                      0      |

## T6

File `reports/tables/T6.csv` · stage S07 · command `python src/stages/s07_score.py` · rows 8 · sha `ab9e80a857ece54b` · stage commit `dc13357`

| eval_stratum        |     n |   cover_upper95 |   cover_90 |   pinball_90 |   pinball_95 |   winkler_90 |   kupiec_p_nonevent |   exceed_rate_nonevent |
|:--------------------|------:|----------------:|-----------:|-------------:|-------------:|-------------:|--------------------:|-----------------------:|
| administered        |  6755 |          0.9298 |     0.8725 |       0.0028 |       0.0019 |       0.0683 |              0      |                 0.0689 |
| domestic_staple     |  7175 |          0.9204 |     0.8422 |       0.0054 |       0.004  |       0.1519 |              0      |                 0.0783 |
| imported_staple     | 18881 |          0.9137 |     0.844  |       0.0055 |       0.0045 |       0.1595 |              0      |                 0.0746 |
| non_food            |  3075 |          0.9382 |     0.8842 |       0.0029 |       0.0029 |       0.0989 |              0.0038 |                 0.0618 |
| short_history       |  1116 |          0.8468 |     0.7948 |       0.0253 |       0.0184 |       0.7028 |              0      |                 0.0862 |
| spice               |  8200 |          0.938  |     0.8683 |       0.0069 |       0.0056 |       0.2008 |              0      |                 0.062  |
| volatile_perishable | 10145 |          0.9209 |     0.8541 |       0.0106 |       0.0076 |       0.318  |              0      |                 0.0628 |
| ALL                 | 55347 |          0.9215 |     0.8539 |       0.0065 |       0.005  |       0.1892 |              0      |                 0.0697 |

## T7

File `reports/tables/T7.csv` · stage S07 · command `python src/stages/s07_score.py` · rows 18 · sha `88994d35254ffdb9` · stage commit `dc13357`

| event_id   | item_id                                    | confidence   | onset      | news_peak   | period                  |   n_obs_in_window | A_conf_detected   | A_z2_detected   | A_z1_detected   | A_z3_detected   | A_alps1_detected   | A_alps2_detected   | A_ifpa_detected   | A_ifpa05_detected   | A_alps1_first   |   A_alps1_lead_days |   A_alps1_lead_reports | A_alps2_first   |   A_alps2_lead_days |   A_alps2_lead_reports | A_ifpa05_first   |   A_ifpa05_lead_days |   A_ifpa05_lead_reports | A_conf_first   |   A_conf_lead_days |   A_conf_lead_reports | A_z2_first   |   A_z2_lead_days |   A_z2_lead_reports | A_z1_first   |   A_z1_lead_days |   A_z1_lead_reports | A_z3_first   |   A_z3_lead_days |   A_z3_lead_reports | A_ifpa_first   |   A_ifpa_lead_days |   A_ifpa_lead_reports |
|:-----------|:-------------------------------------------|:-------------|:-----------|:------------|:------------------------|------------------:|:------------------|:----------------|:----------------|:----------------|:-------------------|:-------------------|:------------------|:--------------------|:----------------|--------------------:|-----------------------:|:----------------|--------------------:|-----------------------:|:-----------------|---------------------:|------------------------:|:---------------|-------------------:|----------------------:|:-------------|-----------------:|--------------------:|:-------------|-----------------:|--------------------:|:-------------|-----------------:|--------------------:|:---------------|-------------------:|----------------------:|
| BD-S09     | Sugar | per kg                             | low          | 2023-06-01 | 2023-06-25  | in_sample_for_threshold |                28 | False             | False           | False           | False           | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | nan            |                nan |                   nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S11     | Egg - Farm | per hali (4 pcs)              | low          | 2023-08-01 | 2023-08-13  | in_sample_for_threshold |                22 | False             | False           | False           | False           | True               | True               | False             | True                | 2023-08-13      |                   0 |                      0 | 2023-08-13      |                   0 |                      0 | 2023-09-03       |                  -21 |                      -6 | nan            |                nan |                   nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S12     | Onion - Imported | per kg                  | low          | 2023-08-01 | 2023-08-21  | in_sample_for_threshold |                24 | False             | False           | False           | False           | True               | True               | False             | False               | 2023-08-17      |                   4 |                      2 | 2023-08-31      |                 -10 |                     -2 | nan              |                  nan |                     nan | nan            |                nan |                   nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S12     | Onion - Local | per kg                     | low          | 2023-08-01 | 2023-08-21  | in_sample_for_threshold |                24 | True              | False           | False           | False           | True               | True               | False             | True                | 2023-08-13      |                   8 |                      3 | 2023-09-05      |                 -15 |                     -5 | 2023-09-03       |                  -13 |                      -3 | 2023-08-26     |                 -5 |                    -1 | nan          |              nan |                 nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S13     | Onion - Imported | per kg                  | medium       | 2023-10-01 | 2023-12-09  | in_sample_for_threshold |                89 | True              | True            | True            | True            | True               | True               | True              | True                | 2023-10-28      |                  42 |                     37 | 2023-11-01      |                  38 |                     34 | 2023-10-03       |                   67 |                      55 | 2023-11-01     |                 38 |                    34 | 2023-12-11   |               -2 |                  -2 | 2023-11-01   |               38 |                  34 | 2023-12-11   |               -2 |                  -2 | 2023-11-01     |                 38 |                    34 |
| BD-S13     | Onion - Local | per kg                     | medium       | 2023-10-01 | 2023-12-09  | in_sample_for_threshold |                89 | True              | False           | True            | False           | True               | True               | True              | False               | 2023-11-01      |                  38 |                     34 | 2023-11-06      |                  33 |                     32 | nan              |                  nan |                     nan | 2023-11-03     |                 36 |                    33 | nan          |              nan |                 nan | 2023-11-01   |               38 |                  34 | nan          |              nan |                 nan | 2023-11-01     |                 38 |                    34 |
| BD-S14     | Potato | per kg                            | low          | 2023-10-01 | 2023-11-13  | in_sample_for_threshold |                66 | True              | True            | True            | True            | True               | False              | False             | False               | 2023-11-15      |                  -2 |                     -2 | nan             |                 nan |                    nan | nan              |                  nan |                     nan | 2023-10-30     |                 14 |                    10 | 2023-10-23   |               21 |                  15 | 2023-10-23   |               21 |                  15 | 2023-10-23   |               21 |                  15 | nan            |                nan |                   nan |
| BD-S15     | Rice - Coarse (Swarna/China IRRI) | per kg | high         | 2023-10-01 | 2025-06-10  | in_sample_for_threshold |               580 | True              | True            | True            | True            | True               | True               | False             | True                | 2023-11-15      |                 573 |                    515 | 2023-11-15      |                 573 |                    515 | 2024-05-02       |                  404 |                     364 | 2023-10-27     |                592 |                   529 | 2023-10-27   |              592 |                 529 | 2023-10-27   |              592 |                 529 | 2024-01-17   |              510 |                 455 | nan            |                nan |                   nan |
| BD-S15     | Rice - Medium (Paijam) | per kg            | high         | 2023-10-01 | 2025-06-10  | in_sample_for_threshold |               580 | True              | True            | True            | True            | True               | True               | True              | True                | 2023-11-06      |                 582 |                    523 | 2023-11-21      |                 567 |                    509 | 2024-05-02       |                  404 |                     364 | 2023-10-27     |                592 |                   529 | 2023-11-30   |              558 |                 500 | 2023-10-27   |              592 |                 529 | 2024-10-31   |              222 |                 200 | 2024-05-02     |                404 |                   364 |
| BD-S16     | Egg - Farm | per hali (4 pcs)              | low          | 2024-05-01 | 2024-05-19  | in_sample_for_threshold |                58 | True              | True            | True            | True            | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | 2024-05-08     |                 11 |                    11 | 2024-05-08   |               11 |                  11 | 2024-04-24   |               25 |                  24 | 2024-05-08   |               11 |                  11 | nan            |                nan |                   nan |
| BD-S17     | Potato | per kg                            | medium       | 2024-07-01 | 2024-08-18  | in_sample_for_threshold |                79 | False             | False           | True            | False           | False              | False              | False             | True                | nan             |                 nan |                    nan | nan             |                 nan |                    nan | 2024-07-01       |                   48 |                      40 | nan            |                nan |                   nan | nan          |              nan |                 nan | 2024-08-29   |              -11 |                 -10 | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S19     | Potato | per kg                            | low          | 2024-09-01 | 2024-09-05  | in_sample_for_threshold |                47 | False             | False           | True            | False           | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | nan            |                nan |                   nan | nan          |              nan |                 nan | 2024-08-29   |                7 |                   7 | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S20     | Egg - Farm | per hali (4 pcs)              | medium       | 2024-10-01 | 2024-10-18  | in_sample_for_threshold |                60 | False             | False           | False           | False           | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | nan            |                nan |                   nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S21     | Soybean Oil - Bottled | 1 litre            | medium       | 2024-10-01 | 2025-02-09  | in_sample_for_threshold |               169 | True              | False           | True            | False           | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | 2024-12-13     |                 58 |                    55 | nan          |              nan |                 nan | 2024-12-13   |               58 |                  55 | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S21     | Soybean Oil - Bottled | 2 litre            | medium       | 2024-10-01 | 2025-02-09  | in_sample_for_threshold |               169 | True              | True            | True            | False           | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | 2024-12-15     |                 56 |                    53 | 2024-12-15   |               56 |                  53 | 2024-12-13   |               58 |                  55 | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S21     | Soybean Oil - Bottled | 5 litre            | medium       | 2024-10-01 | 2025-02-09  | in_sample_for_threshold |               169 | True              | False           | True            | False           | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | 2024-10-07     |                125 |                   120 | nan          |              nan |                 nan | 2024-10-07   |              125 |                 120 | nan          |              nan |                 nan | nan            |                nan |                   nan |
| BD-S21     | Soybean Oil - Loose | per litre            | medium       | 2024-10-01 | 2025-02-09  | in_sample_for_threshold |               169 | True              | True            | True            | True            | True               | False              | False             | True                | 2025-03-03      |                 -22 |                    -20 | nan             |                 nan |                    nan | 2024-12-01       |                   70 |                      67 | 2024-11-08     |                 93 |                    90 | 2024-10-01   |              131 |                 126 | 2024-09-29   |              133 |                 128 | 2024-11-13   |               88 |                  85 | nan            |                nan |                   nan |
| BD-S22     | Green Chilli | per kg                      | low          | 2026-07-01 | 2026-07-31  | clean_test              |                72 | True              | True            | True            | True            | False              | False              | False             | False               | nan             |                 nan |                    nan | nan             |                 nan |                    nan | nan              |                  nan |                     nan | 2026-07-29     |                  2 |                     2 | 2026-07-28   |                3 |                   3 | 2026-07-15   |               16 |                  16 | 2026-07-30   |                1 |                   1 | nan            |                nan |                   nan |

## T7_event_level

File `reports/tables/T7_event_level.csv` · stage S07 · command `python src/stages/s07_score.py` · rows 12 · sha `21e23d8cec75cee0` · stage commit `dc13357`

| event_id   | A_conf   | A_z2   | A_z1   | A_z3   | A_alps1   | A_alps2   | A_ifpa   | A_ifpa05   | period                  | confidence   |
|:-----------|:---------|:-------|:-------|:-------|:----------|:----------|:---------|:-----------|:------------------------|:-------------|
| BD-S09     | False    | False  | False  | False  | False     | False     | False    | False      | in_sample_for_threshold | low          |
| BD-S11     | False    | False  | False  | False  | True      | True      | False    | True       | in_sample_for_threshold | low          |
| BD-S12     | True     | False  | False  | False  | True      | True      | False    | True       | in_sample_for_threshold | low          |
| BD-S13     | True     | True   | True   | True   | True      | True      | True     | True       | in_sample_for_threshold | medium       |
| BD-S14     | True     | True   | True   | True   | True      | False     | False    | False      | in_sample_for_threshold | low          |
| BD-S15     | True     | True   | True   | True   | True      | True      | True     | True       | in_sample_for_threshold | high         |
| BD-S16     | True     | True   | True   | True   | False     | False     | False    | False      | in_sample_for_threshold | low          |
| BD-S17     | False    | False  | True   | False  | False     | False     | False    | True       | in_sample_for_threshold | medium       |
| BD-S19     | False    | False  | True   | False  | False     | False     | False    | False      | in_sample_for_threshold | low          |
| BD-S20     | False    | False  | False  | False  | False     | False     | False    | False      | in_sample_for_threshold | medium       |
| BD-S21     | True     | True   | True   | True   | True      | False     | False    | True       | in_sample_for_threshold | medium       |
| BD-S22     | True     | True   | True   | True   | False     | False     | False    | False      | clean_test              | low          |

## T8

File `reports/tables/T8.csv` · stage S07 · command `python src/stages/s07_score.py` · rows 64 · sha `db5a9e94ed7b091d` · stage commit `dc13357`

| rule                       | eval_stratum        |   fa_per_item_year |   recall_events |   recall_clean_test |
|:---------------------------|:--------------------|-------------------:|----------------:|--------------------:|
| conformal 0.975 upper, 3/5 | administered        |             1.844  |          0.5833 |                   1 |
| conformal 0.975 upper, 3/5 | domestic_staple     |             2.0069 |          0.5833 |                   1 |
| conformal 0.975 upper, 3/5 | imported_staple     |             1.8446 |          0.5833 |                   1 |
| conformal 0.975 upper, 3/5 | non_food            |             1.7279 |          0.5833 |                   1 |
| conformal 0.975 upper, 3/5 | short_history       |             1.8437 |          0.5833 |                   1 |
| conformal 0.975 upper, 3/5 | spice               |             1.7377 |          0.5833 |                   1 |
| conformal 0.975 upper, 3/5 | volatile_perishable |             1.7859 |          0.5833 |                   1 |
| conformal 0.975 upper, 3/5 | ALL                 |             1.8284 |          0.5833 |                   1 |
| robust z>=2, 3/5           | administered        |             1.4909 |          0.5    |                   1 |
| robust z>=2, 3/5           | domestic_staple     |             1.5973 |          0.5    |                   1 |
| robust z>=2, 3/5           | imported_staple     |             2.0088 |          0.5    |                   1 |
| robust z>=2, 3/5           | non_food            |             1.4923 |          0.5    |                   1 |
| robust z>=2, 3/5           | short_history       |             1.6593 |          0.5    |                   1 |
| robust z>=2, 3/5           | spice               |             2.6803 |          0.5    |                   1 |
| robust z>=2, 3/5           | volatile_perishable |             2.7754 |          0.5    |                   1 |
| robust z>=2, 3/5           | ALL                 |             2.1114 |          0.5    |                   1 |
| robust z>=1, 3/5           | administered        |             3.0603 |          0.6667 |                   1 |
| robust z>=1, 3/5           | domestic_staple     |             2.7031 |          0.6667 |                   1 |
| robust z>=1, 3/5           | imported_staple     |             2.4889 |          0.6667 |                   1 |
| robust z>=1, 3/5           | non_food            |             2.0421 |          0.6667 |                   1 |
| robust z>=1, 3/5           | short_history       |             2.9499 |          0.6667 |                   1 |
| robust z>=1, 3/5           | spice               |             3.7111 |          0.6667 |                   1 |
| robust z>=1, 3/5           | volatile_perishable |             3.9579 |          0.6667 |                   1 |
| robust z>=1, 3/5           | ALL                 |             3.0234 |          0.6667 |                   1 |
| robust z>=3, 3/5           | administered        |             0.7454 |          0.5    |                   1 |
| robust z>=3, 3/5           | domestic_staple     |             1.3106 |          0.5    |                   1 |
| robust z>=3, 3/5           | imported_staple     |             1.4782 |          0.5    |                   1 |
| robust z>=3, 3/5           | non_food            |             0.9425 |          0.5    |                   1 |
| robust z>=3, 3/5           | short_history       |             0.9218 |          0.5    |                   1 |
| robust z>=3, 3/5           | spice               |             2.1501 |          0.5    |                   1 |
| robust z>=3, 3/5           | volatile_perishable |             2.0031 |          0.5    |                   1 |
| robust z>=3, 3/5           | ALL                 |             1.5319 |          0.5    |                   1 |
| ALPS-style z>=1, 3/5       | administered        |             0.9024 |          0.5    |                   0 |
| ALPS-style z>=1, 3/5       | domestic_staple     |             0.6963 |          0.5    |                   0 |
| ALPS-style z>=1, 3/5       | imported_staple     |             0.3285 |          0.5    |                   0 |
| ALPS-style z>=1, 3/5       | non_food            |             0.2356 |          0.5    |                   0 |
| ALPS-style z>=1, 3/5       | short_history       |             0.1844 |          0.5    |                   0 |
| ALPS-style z>=1, 3/5       | spice               |             0.8836 |          0.5    |                   0 |
| ALPS-style z>=1, 3/5       | volatile_perishable |             0.6033 |          0.5    |                   0 |
| ALPS-style z>=1, 3/5       | ALL                 |             0.5615 |          0.5    |                   0 |
| ALPS-style z>=2, 3/5       | administered        |             0.1569 |          0.3333 |                   0 |
| ALPS-style z>=2, 3/5       | domestic_staple     |             0.6144 |          0.3333 |                   0 |
| ALPS-style z>=2, 3/5       | imported_staple     |             0.1516 |          0.3333 |                   0 |
| ALPS-style z>=2, 3/5       | non_food            |             0      |          0.3333 |                   0 |
| ALPS-style z>=2, 3/5       | short_history       |             0.1844 |          0.3333 |                   0 |
| ALPS-style z>=2, 3/5       | spice               |             0.8836 |          0.3333 |                   0 |
| ALPS-style z>=2, 3/5       | volatile_perishable |             0.362  |          0.3333 |                   0 |
| ALPS-style z>=2, 3/5       | ALL                 |             0.3459 |          0.3333 |                   0 |
| IFPA-style >=1             | administered        |             0.0392 |          0.1667 |                   0 |
| IFPA-style >=1             | domestic_staple     |             0.2048 |          0.1667 |                   0 |
| IFPA-style >=1             | imported_staple     |             0.1769 |          0.1667 |                   0 |
| IFPA-style >=1             | non_food            |             0.0785 |          0.1667 |                   0 |
| IFPA-style >=1             | short_history       |             0      |          0.1667 |                   0 |
| IFPA-style >=1             | spice               |             0.4418 |          0.1667 |                   0 |
| IFPA-style >=1             | volatile_perishable |             0.1448 |          0.1667 |                   0 |
| IFPA-style >=1             | ALL                 |             0.1887 |          0.1667 |                   0 |
| IFPA-style >=0.5           | administered        |             0.1569 |          0.5    |                   0 |
| IFPA-style >=0.5           | domestic_staple     |             0.3686 |          0.5    |                   0 |
| IFPA-style >=0.5           | imported_staple     |             0.2653 |          0.5    |                   0 |
| IFPA-style >=0.5           | non_food            |             0.2356 |          0.5    |                   0 |

(first 60 of 64 rows; full table in the CSV)

## T8b_precision_recall

File `reports/tables/T8b_precision_recall.csv` · stage S07 · command `python src/stages/s07_score.py` · rows 10 · sha `c044e0020f8c997d` · stage commit `dc13357`

| kind      |   value |   precision |   recall |   n_episodes |
|:----------|--------:|------------:|---------:|-------------:|
| conformal |   0.9   |      0.277  |   0.5833 |          148 |
| conformal |   0.95  |      0.2929 |   0.5833 |           99 |
| conformal |   0.975 |      0.2791 |   0.5833 |           86 |
| conformal |   0.99  |      0.2958 |   0.5833 |           71 |
| z         |   1     |      0.3049 |   0.6667 |          164 |
| z         |   1.5   |      0.3448 |   0.6667 |          116 |
| z         |   2     |      0.2921 |   0.5    |           89 |
| z         |   2.5   |      0.2923 |   0.5    |           65 |
| z         |   3     |      0.2778 |   0.5    |           54 |
| z         |   4     |      0.2424 |   0.25   |           33 |

## T9

File `reports/tables/T9.csv` · stage S09 · command `python src/stages/s09_score.py` · rows 15 · sha `40f4fc5256e10649` · stage commit `dc13357`

| event_id   | item_id                                    | confidence   | rise_start   | rise_end   |   report_days |   realized_log_change |   realized_pct |   M0_persistence_calendar |   M1_minus_M0_forecast_drivers |   M2_minus_M1_explain_drivers |   not_explained_by_measured_cost_drivers |   n_chunks |   share_M0 |   share_forecast_drivers |   share_explain_drivers |   share_not_explained | label                                          |
|:-----------|:-------------------------------------------|:-------------|:-------------|:-----------|--------------:|----------------------:|---------------:|--------------------------:|-------------------------------:|------------------------------:|-----------------------------------------:|-----------:|-----------:|-------------------------:|------------------------:|----------------------:|:-----------------------------------------------|
| BD-S09     | Sugar | per kg                             | low          | 2023-05-31   | 2023-06-24 |            14 |                0.1092 |        11.5385 |                   -0.0027 |                         0.0025 |                        0.0042 |                                   0.1052 |          1 |    -0.0245 |                   0.0227 |                  0.0386 |                0.9632 | mostly not explained by measured cost drivers  |
| BD-S12     | Onion - Imported | per kg                  | low          | 2023-07-31   | 2023-08-19 |             7 |                0.3023 |        35.2941 |                    0.0248 |                        -0.0185 |                        0.002  |                                   0.2939 |          1 |     0.0821 |                  -0.0612 |                  0.0067 |                0.9724 | mostly not explained by measured cost drivers  |
| BD-S12     | Onion - Local | per kg                     | low          | 2023-07-31   | 2023-08-19 |             7 |                0.2776 |        32      |                    0.0012 |                         0.0162 |                        0.0052 |                                   0.255  |          1 |     0.0044 |                   0.0584 |                  0.0186 |                0.9185 | mostly not explained by measured cost drivers  |
| BD-S13     | Onion - Imported | per kg                  | medium       | 2023-09-26   | 2023-12-04 |            51 |                0.5108 |        66.6667 |                   -0.0815 |                         0.1716 |                        0.0421 |                                   0.3786 |          3 |    -0.1596 |                   0.336  |                  0.0824 |                0.7412 | mostly not explained by measured cost drivers  |
| BD-S13     | Onion - Local | per kg                     | medium       | 2023-09-26   | 2023-12-04 |            51 |                0.5306 |        70      |                   -0.054  |                         0.1861 |                        0.0543 |                                   0.3442 |          3 |    -0.1017 |                   0.3507 |                  0.1022 |                0.6487 | mostly not explained by measured cost drivers  |
| BD-S14     | Potato | per kg                            | low          | 2023-09-26   | 2023-11-13 |            30 |                0.1688 |        18.3908 |                    0.0335 |                         0.0023 |                       -0.0343 |                                   0.1673 |          1 |     0.1986 |                   0.0136 |                 -0.2031 |                0.9909 | mostly not explained by measured cost drivers  |
| BD-S15     | Rice - Coarse (Swarna/China IRRI) | per kg | high         | 2023-09-26   | 2025-06-04 |           547 |                0.069  |         7.1429 |                    0.0291 |                         0.015  |                       -0.0468 |                                   0.0716 |         19 |     0.4219 |                   0.2177 |                 -0.6777 |                1.0381 | mostly not explained by measured cost drivers  |
| BD-S15     | Rice - Medium (Paijam) | per kg            | high         | 2023-09-26   | 2025-06-04 |           547 |                0.091  |         9.5238 |                   -0.0356 |                         0.0032 |                       -0.0857 |                                   0.2091 |         19 |    -0.3916 |                   0.0349 |                 -0.9417 |                2.2984 | mostly not explained by measured cost drivers  |
| BD-S16     | Egg - Farm | per hali (4 pcs)              | low          | 2024-04-30   | 2024-05-15 |            14 |                0.1782 |        19.5122 |                    0.0178 |                        -0.0098 |                        0.0001 |                                   0.1701 |          1 |     0.0999 |                  -0.0549 |                  0.0006 |                0.9544 | mostly not explained by measured cost drivers  |
| BD-S17     | Potato | per kg                            | medium       | 2024-07-01   | 2024-08-15 |            37 |               -0.1335 |       -12.5    |                    0.0176 |                         0.0186 |                       -0.0372 |                                  -0.1326 |          2 |   nan      |                 nan      |                nan      |              nan      | no rise over the window (realized change <= 0) |
| BD-S20     | Egg - Farm | per hali (4 pcs)              | medium       | 2024-10-01   | 2024-10-17 |            14 |               -0.0651 |        -6.3063 |                    0      |                        -0      |                        0.0001 |                                  -0.0652 |          1 |   nan      |                 nan      |                nan      |              nan      | no rise over the window (realized change <= 0) |
| BD-S21     | Soybean Oil - Bottled | 1 litre            | medium       | 2024-10-01   | 2025-02-03 |           120 |                0.0557 |         5.7229 |                    0.0169 |                        -0.0031 |                       -0.0042 |                                   0.046  |          4 |     0.3033 |                  -0.0551 |                 -0.0753 |                0.8271 | mostly not explained by measured cost drivers  |
| BD-S21     | Soybean Oil - Bottled | 2 litre            | medium       | 2024-10-01   | 2025-02-03 |           120 |                0.0593 |         6.1069 |                    0.0151 |                         0.004  |                        0.0008 |                                   0.0394 |          4 |     0.2543 |                   0.0674 |                  0.0134 |                0.6648 | mostly not explained by measured cost drivers  |
| BD-S21     | Soybean Oil - Bottled | 5 litre            | medium       | 2024-10-01   | 2025-02-03 |           120 |                0.0681 |         7.044  |                    0.0113 |                         0.0047 |                        0.0067 |                                   0.0453 |          4 |     0.1663 |                   0.0693 |                  0.099  |                0.6654 | mostly not explained by measured cost drivers  |
| BD-S21     | Soybean Oil - Loose | per litre            | medium       | 2024-10-01   | 2025-02-03 |           120 |                0.1372 |        14.7059 |                    0.0314 |                        -0.0095 |                        0.0153 |                                   0.1001 |          4 |     0.2286 |                  -0.0695 |                  0.1115 |                0.7294 | mostly not explained by measured cost drivers  |

## T9_shap_by_episode

File `reports/tables/T9_shap_by_episode.csv` · stage S09 · command `python src/stages/s09_score.py` · rows 15 · sha `b2e9963cc4abaa25` · stage commit `dc13357`

| event_id   | item_id                                    |   shap_sum_E1_fx |   shap_sum_E2_fuel |   shap_sum_E3_imports |   shap_sum_E4_events |   shap_sum_E5_world |   shap_sum_G1 |   shap_sum_G2 |   shap_sum_G3 |   shap_sum_G4 |   shap_sum_G5 |   shap_sum_own_calendar |
|:-----------|:-------------------------------------------|-----------------:|-------------------:|----------------------:|---------------------:|--------------------:|--------------:|--------------:|--------------:|--------------:|--------------:|------------------------:|
| BD-S09     | Sugar | per kg                             |          -0.0011 |            -0.001  |                0.0057 |              -0.0004 |              0.0003 |       -0.0008 |        0      |        0      |             0 |        0.0004 |                 -0.0016 |
| BD-S12     | Onion - Imported | per kg                  |          -0.0006 |             0      |                0.0013 |               0      |              0      |       -0.0001 |        0      |        0.004  |            -0 |       -0.0001 |                  0.0031 |
| BD-S12     | Onion - Local | per kg                     |           0      |             0      |                0.0016 |              -0      |              0      |       -0.0001 |        0.0001 |        0.004  |            -0 |        0.0083 |                  0.008  |
| BD-S13     | Onion - Imported | per kg                  |          -0.0064 |             0.0028 |                0.0017 |               0.0004 |              0      |        0.0011 |       -0      |        0.1312 |             0 |       -0.0009 |                 -0.0123 |
| BD-S13     | Onion - Local | per kg                     |           0.0004 |             0.0023 |                0.0008 |               0.0003 |              0      |        0.001  |       -0      |        0.1333 |             0 |        0.0056 |                  0.0283 |
| BD-S14     | Potato | per kg                            |          -0.0007 |             0.0006 |               -0.0046 |               0.0002 |              0      |       -0.0004 |       -0      |       -0.002  |             0 |        0.0024 |                 -0.0049 |
| BD-S15     | Rice - Coarse (Swarna/China IRRI) | per kg |           0.0066 |            -0.0045 |                0.0015 |              -0.0732 |             -0.0016 |       -0.0227 |       -0.0005 |       -0.0157 |             0 |       -0.0033 |                 -0.0216 |
| BD-S15     | Rice - Medium (Paijam) | per kg            |           0.0038 |            -0.0057 |               -0.0031 |              -0.0993 |             -0.0018 |       -0.0246 |       -0.0007 |       -0.0132 |             0 |       -0.0024 |                 -0.1033 |
| BD-S16     | Egg - Farm | per hali (4 pcs)              |           0.0002 |            -0.0001 |               -0.0001 |              -0      |              0      |       -0.0004 |       -0      |       -0.0002 |             0 |       -0.0003 |                  0.0068 |
| BD-S17     | Potato | per kg                            |           0.0002 |             0.0006 |                0.0005 |              -0.0377 |             -0.0001 |       -0.001  |        0.0002 |       -0.0002 |             0 |        0.0393 |                 -0.0104 |
| BD-S20     | Egg - Farm | per hali (4 pcs)              |          -0      |             0      |               -0.0004 |              -0      |              0      |       -0.0002 |       -0      |       -0.0002 |             0 |       -0.0004 |                 -0.0003 |
| BD-S21     | Soybean Oil - Bottled | 1 litre            |          -0.0003 |             0.002  |                0.0023 |              -0.0026 |             -0.0004 |       -0.0019 |       -0.0001 |       -0.0001 |             0 |       -0.0012 |                 -0.0135 |
| BD-S21     | Soybean Oil - Bottled | 2 litre            |           0.0011 |             0.0009 |                0.0015 |               0.0001 |             -0.0004 |       -0.0005 |       -0.0001 |       -0.0009 |             0 |       -0.0012 |                 -0.0062 |
| BD-S21     | Soybean Oil - Bottled | 5 litre            |           0.0021 |             0.0014 |                0.0019 |               0.0006 |             -0.0004 |       -0.0024 |       -0.0001 |       -0.0002 |             0 |        0.0008 |                 -0.0064 |
| BD-S21     | Soybean Oil - Loose | per litre            |           0.003  |             0.0021 |                0.0029 |               0.0004 |             -0.0004 |        0.0002 |       -0.0001 |       -0.0004 |             0 |       -0.0012 |                  0.0051 |

## T9b_sign_checks

File `reports/tables/T9b_sign_checks.csv` · stage S09 · command `python src/stages/s09_score.py` · rows 9 · sha `3a392ad76ae988cb` · stage commit `dc13357`

| feature             | items                                     |   h |     n |   spearman_value_vs_shap | expected_sign   | sign_ok   |
|:--------------------|:------------------------------------------|----:|------:|-------------------------:|:----------------|:----------|
| e1_fx_ch30          | E1 strata (imported, administered, spice) |   7 | 34643 |                  -0.1097 | +               | False     |
| e1_fx_ch30          | E1 strata (imported, administered, spice) |  14 | 34643 |                   0.0902 | +               | True      |
| e1_fx_ch30          | E1 strata (imported, administered, spice) |  30 | 34643 |                   0.4837 | +               | True      |
| own_world_price_ch3 | G1 items                                  |   7 | 18525 |                  -0.111  | +               | False     |
| own_world_price_ch3 | G1 items                                  |  14 | 18525 |                  -0.0614 | +               | False     |
| own_world_price_ch3 | G1 items                                  |  30 | 18525 |                   0.1111 | +               | True      |
| e5_world_explain    | sugar, chickpea                           |   7 |  2226 |                   0.0896 | +               | True      |
| e5_world_explain    | sugar, chickpea                           |  14 |  2226 |                  -0.3161 | +               | False     |
| e5_world_explain    | sugar, chickpea                           |  30 |  2226 |                   0.2688 | +               | True      |

## T9c_shap_importance

File `reports/tables/T9c_shap_importance.csv` · stage S09 · command `python src/stages/s09_score.py` · rows 6 · sha `1c768014d0493c59` · stage commit `dc13357`

| eval_stratum        |   E1_fx |   E2_fuel |   E3_imports |   E4_events |   E5_world |     G1 |     G2 |     G3 |   G4 |     G5 |   own_calendar |
|:--------------------|--------:|----------:|-------------:|------------:|-----------:|-------:|-------:|-------:|-----:|-------:|---------------:|
| administered        |  0.001  |    0.0006 |       0.0008 |      0.0004 |     0.0002 | 0.0025 | 0      | 0.0001 |    0 | 0.001  |         0.0031 |
| domestic_staple     |  0.0002 |    0.0008 |       0.0008 |      0.0006 |     0      | 0.001  | 0      | 0.0002 |    0 | 0.0045 |         0.0072 |
| imported_staple     |  0.0007 |    0.0005 |       0.001  |      0.0006 |     0.0001 | 0.0006 | 0.0003 | 0.0002 |    0 | 0.0008 |         0.0033 |
| non_food            |  0.0002 |    0.0005 |       0.0011 |      0.0007 |     0      | 0.0005 | 0      | 0.0002 |    0 | 0.0009 |         0.0033 |
| spice               |  0.0007 |    0.0004 |       0.0014 |      0.0004 |     0      | 0.0004 | 0      | 0.0001 |    0 | 0.0009 |         0.004  |
| volatile_perishable |  0.0002 |    0.0008 |       0.0006 |      0.0008 |     0      | 0.0005 | 0      | 0.0002 |    0 | 0.0082 |         0.0086 |