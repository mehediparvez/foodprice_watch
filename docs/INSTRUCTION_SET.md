# Reframing Food Price Watch for an honest, resumable finish

The Bangladesh Food Price Watch should be finished as an **eight-phase applied project that produces one results pack**, not as a thesis. It answers five questions. RQ1: does anything beat "tomorrow = today"? RQ2: which drivers add value beyond persistence, and for which goods? RQ3: do forecast-interval alerts catch the documented shocks? RQ4: how much of each rise do measured cost drivers explain? RQ5, new: is a flagged rise national or confined to one market, using a monthly WFP market-level module? The user's three past chats are now included in this synthesis, and they change the plan in four ways. First, a quick single-driver test found that **matched drivers barely beat placebos: 6.2% of tests significant against 6.0%, and 3.7% beat naive against 2.8%**. Only world prices showed a clear signal, leading edible oils, flour and rice by 1–3 months ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). Second, **every backtest so far leaked import data**. Imports were stamped available 75 days after each month starts, but they really arrive about 208 days later, so all import-driver results must be re-run. Third, the user already holds WFP, AgriPriceBD, World Bank Pink Sheet and Mendeley OHLC files that are not in the project. Fourth, the real environment is one Colab notebook on one Drive folder, with a work PC that blocks pip and data sites that block automated visitors. The existing first benchmark still stands: no classical model beats naive at any horizon (AutoETS gmean relMAE 1.17/1.05/1.04/1.03 at h=1/7/14/30) ([baseline results](https://claude.ai/artifact/394Xrk4k7LvgWcKwQePwNS)). The instruction set below keeps the long-running-agent pattern: a JSON ledger, an append-only log, per-unit done-markers on Drive and a git commit per stage, so a dropped session **resumes at the first unfinished unit instead of restarting** ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). It adds a test-once lock on the 2025–26 test period, a pre-registered one-driver-group-at-a-time protocol, and a mode where the user runs the cells and the agent reads the pasted output. Before the agent starts, the user must still settle authorship (every document names Romjan Chowdhury), confirm project-versus-thesis with the department, choose the alert threshold, and upload the four external datasets.

## The past chats show drivers barely beat placebos, and imports leaked

The past chats are now part of the evidence. Three of their findings change the plan directly. The first is the driver test. Each external driver was tested against the item it should affect, and also against unrelated items as a placebo. The matched pairs did no better than the placebos. **6.2% of matched tests came out significant against 6.0% for placebos. Matched drivers beat naive in 3.7% of cases against 2.8% for placebos.** The one clear signal was world prices: the FAO and IMF indices lead edible oils, flour and rice by one to three months ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). The chat itself calls this provisional, because it tested one driver at a time rather than a full model. It is also contaminated, because the same chat reports a look-ahead bug: import data were "stamped as available 75 days after each month starts, when it really arrives about 208 days later". Every backtest so far therefore used import figures about four months before they existed. A second bug produces infinite import unit values in months with zero tonnes ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). The price-only classical baseline is unaffected because it uses no drivers. Any driver result that touched imports, including the placebo test, has to be re-run before anyone cites it.

These findings drive the main reframing. The chat recommends changing the claim from "external data improve forecasts" to **"do they add value beyond persistence, and for which goods?"** That question has a publishable answer either way. It also fits the evidence: a naive forecast already wins on most series, and TCB prices sit unchanged on about 85–95% of report days in every stratum ([Proposal](https://claude.ai/artifact/7Ud96n6HY5rVPLn57zM4Nh)). The chat gives the protocol to answer it. Make every choice on 2024 data, then run the 2025–26 test once. Add one driver group at a time to a core model, with significance tests set in advance. Score the 9 short-history items separately. Build one long item × date table with "driver slots" such as "own world price", filled differently for each item. Where an item has no driver, leave the cell empty with a missing-driver flag and **never fill it with 0**. LightGBM handles empty values natively. Join each dataset on its real publication date, cap how long an old value carries forward, and **never fill prices across the 2022 gap** ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)).

The chats also give a per-item driver map that narrows the feature set sharply. Ramadan/Eid and month-of-year apply to every item. World prices apply to oils, flour, rice and milk powder, about 15–20 series. Brent applies to milk powder and imported chilli. India's onion export measures apply to onion, fishing bans to hilsa, and weather, cut from about 170 columns to about 3, to vegetables. Exchange rates, fuel prices, imports, and the disruption, cyclone and duty-cut calendars are kept **for explaining spikes, not for forecasting**. The chat drops the Bangladesh Bank remittance and reserve series (too short), the extra currency rates, WTI, and the empty river and IFPRI folders ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). Two checks are now resolved: the Ramadan file has its 2027 row, and IMF chickpea is in USD per 100 kg. One check is still open: the India and Indonesia export-ban dates are pieced together from news reports and need verifying ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)).

The chats also show that the project's data assets are larger than the 32 project files. The user holds **WFP HDX monthly retail prices for Bangladesh** (about 73 items and 110 markets, roughly 2004 to Aug 2026, in `wfp_food_prices_bgd.csv`, with market coordinates in `wfp_markets_bgd.csv`). The user also holds the AgriPriceBD daily wholesale and retail min/max CSVs for green chilli, garlic, chickpea, cucumber and sweet pumpkin, Jul 2020 to Jun 2025 ([Mendeley 10.17632/bkmxnrn3hn.1](https://doi.org/10.17632/bkmxnrn3hn.1)). The third is the World Bank Pink Sheet (`CMO-Historical-Data-Monthly.xlsx`, 1960–2026), and the fourth is a "Food Commodity Price OHLC Dataset of Bangladesh" CSV and zip with per-market rainfall, temperature, humidity and wind ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). The OHLC file is probably [Mendeley 10.17632/dd58ks2p5y.1](https://doi.org/10.17632/dd58ks2p5y.1): monthly data on 76 markets for rice, wheat flour, lentils and oil. That match was never confirmed because the file could not be opened. The same chat recorded known defects to flag, not fix silently. WFP has dates in 1900 (for example 1900-08-15 for fuel in Teknaf). The OHLC dates are in ambiguous day/month order and unsorted. Rohingya camp markets in Cox's Bazar (Balukhali, Kutupalong, Nayapara, Leda, Teknaf and similar) are excluded from national medians in this project. A preliminary run found that AgriPriceBD chilli and WFP chilli correlated at about 0.91 for the same months ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). The chats also restate the original aim, which explains why WFP matters: the project "detects unexplained food price rises in Bangladesh, **locates them (nationwide or one market)**, and explains them". TCB is Dhaka-only, so only WFP can answer the "locate" part.

The working environment sets hard constraints on the agent. "Everything runs in one Google Colab notebook that saves to a single Google Drive folder" ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). On the work PC, `pip.exe` "was blocked by your organization's Device Guard policy", so any local helper must use only the Python standard library, or run in Colab instead. The TCB site "refuses automated visitors" from sandboxes. A later data-gap search found that almost every data host was blocked inside the research session, so its seven likely sources were judged from landing pages and never opened ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). The agent should therefore assume it **cannot download protected sources itself**. The user downloads them by hand in a normal browser and drops them into Drive. The agent verifies and registers them, and marks the stage blocked until they arrive.

A few user files named in the chats were not visible to this synthesis: `Learnathon-Project-Scan.pdf`, `Masters_Project_Ideas.pdf`, `Meeting-Prep-Notes.pdf`, the two proposal PDFs, and `chilli_map.png`. The earlier chat itself noted that the meeting-notes PDF "failed to render" and that the Learnathon and Masters-ideas PDFs were never opened ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). If any of them hold supervisor constraints, those constraints are missing here.

## Ten decisions to settle before any agent runs

The decisions table now reflects what the chats revealed. The user's project memory records a direct statement that the work should be "a master's-standard project, not a thesis", with the report written later from the results ([project memory](memory:///projects/01a185b2-2e90-7128-961c-33dba0dfa3cf/areas/bangladesh-food-price-watch.md)). The proposal in the chats still frames it as a thesis with papers, and it asks the supervisor "whether a dataset paper plus a benchmark paper fits the MSc, and the department's thesis deadlines" ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). No answer to that question appears anywhere. Each default below applies only once the user approves it and records it in `DECISIONS.md`.

| # | Open decision | Why it blocks work | Recommended default (needs your approval) |
|---|---|---|---|
| D1 | **Project vs thesis.** You stated "project, not thesis". The proposal and deck still say MSc thesis plus a dataset paper and a benchmark paper, and ask the supervisor whether that fits. | It sets scope, deliverables, and whether papers, Zenodo and the dashboard count toward "done". | A non-thesis project: results pack plus reproducible repo. Papers, Zenodo and the dashboard become optional extensions. Confirm with your supervisor and rubric. No Bangladeshi non-thesis guideline was found ([CSUS guideline](https://www.csus.edu/college/engineering-computer-science/computer-science/_internal/_documents/ai-ml-ds-ms-projects-guideline.pdf)). |
| D2 | **Author name.** The proposal, dataset page and deck all name "Romjan Chowdhury". Your account describes it as your own project. | Names go into figures, the data card and any release. | `author: TO_CONFIRM`. No name appears in any output until you set it. |
| D3 | **External datasets: available, not attached.** WFP HDX prices plus markets, AgriPriceBD (5 CSVs), Pink Sheet and Mendeley OHLC are on your machine but not in the project or on Drive. | RQ5 and the cross-checks cannot run without them, and the agent must not pretend it used them. | Upload all four to `data/raw/external/` on Drive. Roles: WFP drives RQ5 and the Dhaka cross-check. AgriPriceBD is a cross-check plus literature benchmark. The Pink Sheet cross-checks IMF only and is not a second feature set. OHLC is a novelty check and an optional cross-check. Fix the project description afterwards. |
| D4 | **Threshold for "abnormal".** None is set. | Alert results depend on it, and picking it after seeing the shock results is p-hacking. | Pre-register two rules: (a) conformal 95% upper-bound exceedance on 3 of 5 report days; (b) an ALPS-style robust z ladder of 1/2/3 ([WFP ALPS](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)). Set the operating point from the 2024 false-alarm rate on non-event periods. |
| D5 | **Attribution method.** Not chosen. | It sets the RQ4 result and its wording. | A nested ladder: M0 (price + calendar) ⊂ M1 (+ forecasting drivers from the map) ⊂ M2 (+ explanation-only drivers: FX, fuel, imports at their true release lag, event calendars). TreeSHAP gives a secondary per-date view. |
| D6 | **Horizon unit.** | Lead times and false alarms per item-year depend on it. | Report days, as in the existing `step` column. Convert to calendar days for reporting. |
| D7 | **Priority items** for drivers, alerts and attribution. | Most series have no driver and no shock label. | Benchmark all 54 long-history series. Run the driver, alert and attribution stages on about 16 items (see the outline). Score short-history items separately. |
| D8 | **Time split.** The chats say: tune on 2024, test 2025–26 once. The benchmark test window holds only about 3 of the 12 in-window shocks (S15 tail, S21, S22). | Too few test labels for alerts. A second look at the test period invalidates it. | Forecasting: 2024 validation, Jan 2025–Oct 2026 test, unsealed once (lock file). Alerts: thresholds fixed on 2024 non-event false-alarm rates, then all 12 shocks scored with origins from 2023-06. Report 2025–26 events separately as the clean test, and 2023–24 events as in-sample-for-threshold. |
| D9 | **NEW: the "locate" module (WFP).** TCB is Dhaka-only, but the aim says "locate them (nationwide or one market)". | Without it the "locate" part of the aim is unmet. A full market-level daily system would be thesis-sized. | A **monthly, market-level WFP module** (RQ5): ALPS-style residuals per market × item, national median from non-camp markets, and a breadth rule (share of markets in alert) that labels each flagged month national, regional or local. It also cross-checks TCB-flagged Dhaka rises. It runs only if D3 supplies WFP; otherwise it is "skipped" and recorded as a limitation. |
| D10 | **Data-gap sources and unverified events.** Rivers and IFPRI folders are empty. Data-gap search left BBS CPI (PDF only, base-year link factor about 3.06 for the general index, food factor unknown), Bangladesh Bank FX Excel, GloFAS (needs a free Copernicus account), ACLED (needs Research access with a university email; Gmail gets aggregated data only), and a hand-coded hartal/curfew calendar. India/Indonesia ban dates are reconstructed. The Sep 2023 price caps appear in no event file. | RQ2 and RQ4 scope, and the risk of unsourced events. | Run without rivers, ACLED, CPI and hartals. List them as limitations and as optional stage S14. Verify the India/Indonesia ban dates against cited sources before the S09 event studies. The agent asks before adding any event and cites a source when it does. |

Other items stay open but do not block the start. They are: the TCB licence (no reuse terms; attribute TCB and ask for a no-objection), the novelty check against the Mendeley OHLC dataset, and confirming the reconstructed event dates. The department's real deadlines and the contents of the unseen PDFs are also open ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)).

## Final project outline: five questions, eight phases, one results pack

### Questions re-scoped to "value beyond persistence"

The proposal asked whether "external drivers and pretrained foundation models forecast Dhaka daily retail food prices better than a naive 'tomorrow = today' forecast", and whether their forecasts detect documented shocks early ([Proposal](https://claude.ai/artifact/7Ud96n6HY5rVPLn57zM4Nh)). For a non-thesis project, each question is narrowed to one a finished experiment can answer, and the driver question takes the chat's reframing. The claim stays modest: an applied system evaluated against credible baselines with statistical evidence, which is what applied MS project guidelines ask for ([CSUS guideline](https://www.csus.edu/college/engineering-computer-science/computer-science/_internal/_documents/ai-ml-ds-ms-projects-guideline.pdf)). Several items are deliberately cut: extra foundation models such as TimesFM, deep learning trained from scratch, river discharge, papers and the dashboard.

| RQ | Re-scoped question | Experiment | What counts as an answer |
|---|---|---|---|
| RQ1 Benchmark | On the 54 long-history TCB series, does any model (7 classical, LightGBM, Chronos-2) beat naive at h=1/7/14/30 report days, and in which strata? | Rolling origins on the 2025–26 test, run once; MASE and relMAE vs naive; DM-HLN with Holm | Per-stratum better/worse counts. "Nothing beats naive" is a valid finding. |
| RQ2 Drivers | Which driver groups add value beyond persistence, and for which goods? | Core model (price + calendar) plus one pre-registered driver group at a time, each on its mapped items, with a matched-vs-placebo control; tuned on 2024, tested once on 2025–26 | ΔrelMAE and Δinterval score with bootstrap CIs per group × item, and the matched-minus-placebo gap |
| RQ3 Alerts | Do forecast-interval alerts flag the 12 in-window shocks before the news peak, at what false-alarm rate, against ALPS- and IFPA-style rules? | Thresholds from 2024 non-event false alarms (D4/D8); window [onset−14d, peak+30d]; 3-of-5 persistence | Per-event detected/missed and lead days, false alarms per item-year, PR curve, Kupiec test. 2025–26 events reported separately. |
| RQ4 Explanation | For priority-item rises, how much is accounted for by measured cost drivers, and which rises stay "not explained by measured cost drivers"? | M0⊂M1⊂M2 ladder, SHAP cross-check, event studies: India Dec 2023 onion ban, 2024–25 FX moves, Sep 2023 caps if dated and sourced | Share explained per episode plus a neutral residual label, with sign checks against the pass-through literature |
| RQ5 Locate (WFP, monthly) | Is a flagged rise national or confined to one or a few markets? Do WFP Dhaka markets confirm TCB-flagged rises? | WFP market × item × month ALPS-style residuals; national median from non-camp markets; breadth = share of markets in alert | Each flagged item-month labelled national, regional or local with its markets listed, plus a TCB–WFP agreement table |

The methods follow established practice. WFP ALPS fits a trend plus month dummies per market and reads standardised positive residuals ([WFP ALPS](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)). FAO's IFPA standardises compound growth within each calendar month, with thresholds at 0.5 and 1 ([SDG 2.c.1](https://worldbank.github.io/sdg-metadata/metadata/en/2-c-1)). IFPRI's NEXQ flags returns above a 95% conditional quantile and backtests exceedances against a binomial expectation ([Martins-Filho et al.](https://ssa.foodsecurityportal.org/sites/default/files/2020-09/Martins-FilhoToreroYao2010.pdf)). ALPS admits look-ahead bias, because its trend uses the full sample. The daily TCB detector should therefore use a **strictly real-time, driver-conditioned expected price** with adaptive conformal intervals, which keep coverage valid under distribution shift ([Zaffran et al.](https://arxiv.org/pdf/2202.07282)). RQ5 is different. It is a monthly descriptive module, so ALPS with a real-time (expanding) trend is enough, and ALPS's own guidance of about 36 monthly observations is easily met by WFP's 2004 start ([WFP ALPS](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)). For RQ4, the Bangladesh literature supplies the sign checks. Dhaka rice is cointegrated with India import parity at an elasticity near 0.99 ([Dorosh & Rashid](https://cgspace.cgiar.org/server/api/core/bitstreams/ffd095df-831c-4530-a191-930b5c49fa30/content)). Rice takes about 8 months to return to equilibrium ([Hoque et al.](https://www.bb.org.bd/bbta_portal/assets/bbta_journal/articles/Price%20Transmission%20Dynamics%20in%20the%20Rice%20Market%20of%20Bangladesh.pdf)). Oil-to-food pass-through is small, with a long-run elasticity of 0.199 ([Alauddin et al.](https://bids.org.bd/uploads/publication/BDS/45/4_Oil-and-Food-Prices.pdf)). Asymmetric soybean-oil pass-through "does not necessarily mean collusion" ([BIDS](https://ideas.repec.org/a/ris/badest/0777.html)), which is why the residual label stays neutral.

### The per-item driver map, with forecasting and explanation kept apart

The map below turns the chat's recommendation into a concrete contract. Each forecasting slot is a single column in the long table, filled only for the items mapped to it. Unmapped items get an empty cell plus `has_<slot> = 0`. Groups are added to the core model in the order listed, and that order is pre-registered.

| Slot / group | Items it fills | Role | Source files | Availability rule |
|---|---|---|---|---|
| G0 calendar (core) | All items | Forecast + explain | `bd_ramadan_eid.csv`, `bd_public_holidays_2019_2027.csv`, month-of-year | Known in advance |
| G1 `own_world_price` | Soybean/palm oils, atta/maida, rice, milk powder (about 15–20 series) | Forecast + explain | `imf_commodity_prices.csv` (primary), `fao_food_price_index.csv`; Pink Sheet as cross-check only | Month end + 40 days |
| G2 `brent` | Milk powder, imported dried chilli | Forecast + explain | `fred_DCOILBRENTEU.csv` | Last value on or before report date, capped carry |
| G3 `own_export_measure` | Onion (local and imported) | Forecast + explain | `exporter_policy_events.csv` (reconstructed; verify) | Event start date as published |
| G4 `fishing_ban` | Hilsa | Forecast + explain | `bd_fishing_bans.csv` | Announced dates |
| G5 `weather_k` (k = 1..3) | Vegetables and perishables (potato, onion, brinjal, cucumber, green chilli, ginger, garlic) | Forecast + explain | `weather_open_meteo_13_locations_2019_2026.csv`, reduced to about 3 features chosen on 2024 only | +5 days |
| E1 FX | All imported items | Explain only | `yahoo_bdt_per_usd.csv` + `usd_cross_rates_npm_2024_2026.csv` (BDT column only), spliced | As of report date |
| E2 fuel | All | Explain only | `bd_fuel_price_events.csv` | Effective date |
| E3 imports | Mapped by HS code | Explain only | `bd_food_imports_mirror_comtrade_monthly_agg.csv` | **Month start + 208 days**, not 75 |
| E4 event calendars | Mapped by item | Explain only | `bd_disruption_events.csv`, `bd_cyclones_floods.csv`, `bd_import_duty_changes.csv`, `bd_political_wage_events.csv` | Event dates; out-of-coverage = unknown |
| Dropped | none | none | BB remittance and reserves (kept only as an FX sanity check), extra currencies (CNY, INR, MYR), WTI, empty river and IFPRI folders | n/a |

The table follows the chat's map directly ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). Exactly which roughly 15–20 series fall under G1, and which 3 weather features to keep, are left to S04 and S06 to fix on 2024 data, then freeze before the test. The 208-day import lag is the chat's estimate. S04 should confirm it against Comtrade's actual release pattern and record the value it uses.

### Phases, deliverables and acceptance

| Phase | Stages | Deliverable | Done when |
|---|---|---|---|
| P0 Setup, intake, decisions | S00 | Drive repo, raw manifest (32 project files plus external files if supplied), `DECISIONS.md`, environment lock | Files hashed; D1–D10 answered or PENDING; `make check` passes |
| P1 Data freeze and audit | S01 panel, S02 audit | `tcb_v1.0_rebuilt.parquet` + checksum, data-quality table, audit error rate | Panel invariants pass; audit done by a human or marked blocked |
| P2 External prices and drivers | S03 external intake, S04 driver panel | Clean WFP, AgriPriceBD, Pink Sheet and OHLC tables plus cross-check note; long item × date feature table with driver slots and flags | WFP 1900 rows quarantined; camp markets tagged; OHLC dates resolved or blocked; leakage test passes, including the 208-day import rule; no ±inf values |
| P3 Benchmark and driver value | S05 reproduce baseline, S06 core + driver groups | Benchmark tables, driver-group table, placebo table | Baseline reproduced or diff explained; pre-registration committed before the test is unsealed; test run once |
| P4 Alerts | S07 | Calibrated intervals, alert log, event scorecard | Thresholds frozen on 2024; all 12 events reported, misses included |
| P5 Locate and explain | S08 locate (WFP), S09 explanation | Breadth labels per flagged item-month and TCB–WFP agreement; explained-vs-unexplained shares and event studies | RQ5 tables or recorded "skipped"; neutral-wording test passes |
| P6 Robustness and reproducibility | S10, S11 | Robustness table, clean re-run diff, results pack | Key tables reproduce exactly; `RESULTS_REGISTER.md` complete |
| Optional | S12 dashboard, S13 extra foundation models, S14 data-gap sources (CPI, BB FX, ACLED, GloFAS, hartal calendar) | as named | Only with explicit approval |
| Review | S99 | Independent spec review | Every SPEC line checked by a session that did not build it |

If the deck's calendar still holds, P0–P2 fit November 2026, P3 December–January, P4 February, P5 March and P6 early April. Those dates are the deck's proposals, not commitments, and they "move to match the department's thesis deadlines" ([Deck](https://claude.ai/artifact/NUnU3Rj4BCu4xGFegUrPgi)).

The D7 priority set has about 16 items. It includes every in-window shock product: sugar, egg, local and imported onion, potato, coarse and medium rice, and bottled and loose soybean oil. It adds items with a clean world-price or import-parity driver: loose atta, loose palm oil, large lentil, chickpea, imported garlic, and one milk powder, which also tests the G2 Brent slot. Green chilli has a shock (S22) but only starts in February 2026, so it is scored for alerts only, in the short-history group. Imported onion needs care. It is the only series where any classical model beat naive, and it has had no price since 2026-02-10 because of an import curb ([item_meta.csv](https://claude.ai/artifact/394Xrk4k7LvgWcKwQePwNS)). For RQ5, WFP's item list is not the same as TCB's. S03 must write a TCB↔WFP item crosswalk and show it to the user before S08 runs.

### Tables and figures the results pack must produce

| ID | Table or figure | Stage | RQ / report section |
|---|---|---|---|
| T1 | Dataset summary by stratum (series, report days, % unchanged, % missing, late starters) | S01 | Data |
| T2 | Data-quality ledger: corrections applied and proposed, audit error rate with Wilson 95% CI | S01–S02 | Data validation |
| T3 | Driver inventory: source, role (forecast or explain), frequency, true availability lag, carry cap, coverage, confidence | S04 | Methods |
| T3b | External-source cross-checks: TCB vs WFP Dhaka, AgriPriceBD vs TCB (garlic, chickpea), AgriPriceBD vs WFP chilli, Pink Sheet vs IMF | S03 | Data validation |
| T4 | Benchmark: gmean relMAE, median MASE, win rate, DM better/worse by stratum × model × horizon | S05–S06 | RQ1 |
| T5 | Driver value: core vs core + one group, per group × mapped item, ΔrelMAE with CI, Holm-adjusted p | S06 | RQ2 |
| T5b | Matched vs placebo driver gap (re-run of the chat's test without import leakage) | S06 | RQ2 |
| T6 | Interval calibration: coverage, pinball, Winkler, Kupiec p | S07 | RQ3 |
| T7 | Event scorecard: each of the 12 shocks, confidence, detected or not, lead days, test vs in-sample period | S07 | RQ3 |
| T8 | False alarms per item-year by stratum and rule, alongside ALPS/IFPA | S07 | RQ3 |
| T9 | Explanation ladder per episode: shares from M1, M2 and the residual | S09 | RQ4 |
| T10 | Event-study estimates (onion ban, FX moves, caps if dated) | S09 | RQ4 |
| T11 | Robustness: weekly vs daily, min/max/mid, sliding window, placebo dates, leave-one-event-out, ginger candidates excluded | S10 | Discussion |
| T12 | Locate: flagged item-months with breadth label, markets in alert, Dhaka TCB agreement | S08 | RQ5 |
| F1 | Indexed staples (May 2021 = 100), 2022 gap shaded | S01 | Data |
| F2 | Reporting calendar heatmap | S01 | Data |
| F3 | relMAE vs horizon by stratum | S06 | RQ1 |
| F4 | Driver-group value bars by item, with placebo band | S06 | RQ2 |
| F5 | Coverage calibration plot | S07 | RQ3 |
| F6 | Alert timelines per shock | S07 | RQ3 |
| F7 | Precision–recall with the pre-registered point marked | S07 | RQ3 |
| F8 | Stacked explained-vs-unexplained decomposition for 3–4 cases (onion Dec 2023, soybean oil Oct 2024, potato 2024, rice 2023–25) | S09 | RQ4 |
| F9 | Global SHAP importance by stratum | S09 | RQ4 |
| F10 | Market map of alert breadth for 2–3 flagged months (WFP coordinates; camp markets marked, excluded from median) | S08 | RQ5 |

The later report can follow a standard non-thesis structure. It runs: introduction and questions; related work (ALPS, IFPA, NEXQ, AgriPriceBD, Bangladesh pass-through); data (data card, corrections, audit, availability lags, external sources); methods; evaluation per RQ; case studies; limitations and ethics; and a reproducibility appendix. Every section maps to rows above, so writing becomes assembly rather than analysis.

## Thirty-four data traps the agent must handle explicitly

Profiling the 32 project files showed a structurally clean core panel. It has no duplicate item-date keys, Avg = (Min+Max)/2 everywhere, and 1.42% missing prices. The driver files carry formatting traps, at least one data error is still uncorrected, and the Comtrade blanking described in SOURCES was never applied to the attached file ([DATA_CARD](project://DATA_CARD.md); [SOURCES](project://SOURCES_2026-10-26.md)). The chats add two pipeline bugs and the known defects in the external files ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). Each trap becomes a rule with a test, because an agent that "cleans" them silently will corrupt results. Rules 1–24 come from profiling the project files. Rules 25–34 are new from the chats.

| # | Known issue (file) | Rule for the agent |
|---|---|---|
| 1 | The time index is report days, not calendar days; gaps run 1–115 days. | Model on report days. Never forward-fill prices to calendar days. |
| 2 | 2022 is sparse: only 24 reports from 12 Mar to 31 Dec 2022. | Flag `gap_2022`. Use it as history only, never in an evaluation window, and **never fill prices across it**. |
| 3 | The CSV lacks derived columns, and `tcb_v1.0.parquet` and `tcb_convert.py` are not attached. | Rebuild `item_id = Product + " | " + Unit` (it must reproduce all 63 item_meta ids) and the derived columns. Name the output `_rebuilt`. |
| 4 | **Palm Olein 2 L on 2025-04-18 holds the 5 L price (840/845/842.5).** | Write it to `corrections_proposed.csv` and apply it only with approval. Both palm olein series stay excluded. |
| 5 | Two Min-only rows (2021-05-31 broiler and sugar). | Flag them; exempt them from the midpoint invariant. |
| 6 | Five one-day ±26–35% reversals in local ginger, 2021. | Keep them flagged. Resolve them in S02 or run robustness with and without. |
| 7 | The audit sample has no "checked" column, and the original TCB files are not attached. | S02 is human-in-the-loop and blocked without the originals. Never report an unmeasured error rate. |
| 8 | item_meta dates are DD-MM-YY. | Parse with `%d-%m-%y`, or use the xlsx Series sheet's ISO dates. |
| 9 | The xlsx duplicates the CSV. | Load the CSV once. |
| 10 | Pack sizes are mixed (1/2/5 L, hali = 4, dista = 24, metric ton). | Normalise before any cross-pack comparison, and before any TCB–WFP or TCB–AgriPriceBD comparison. |
| 11 | Late starters not flagged short_history: Soybean Oil 2 L, Rice Bran Oil 5 L. | Respect eval_stratum. Report the late starts in T1. |
| 12 | Imported onion has no price for about 480 days; hilsa is missing in most October bans. | Missing means not reported. Never impute in evaluation. |
| 13 | Comtrade months from 2026-05 are not blanked. HS codes are stored as ints. HS 703 and 910 mix items. | Blank periods ≥ 202605. Zero-pad HS codes. Never assign 703 or 910 to one item. |
| 14 | The IMF CSV has 4 header rows, YYYYMn periods, a duplicated POILAPSP column and unnamed columns; PTOMATO and PAPPLE use 0 for missing. PCHANA is **USD per 100 kg (confirmed)**. | Use a dedicated parser. Check units against the description row. |
| 15 | The FAO file has a title line, and recent months get revised. | Use `skiprows=1`. Record the fetch date. |
| 16 | The weather CSV has two blocks and unnamed locations; its last day is incomplete. | Split the blocks. Map locations by coordinates and log that as an inference. Drop the last day. Apply the +5-day lag. |
| 17 | Yahoo BDT is stale since Sep 2026 and runs about Tk 1.6 below BB; no spliced series is attached. | Splice npm from 2024-03-02 with Yahoo × 1.0151 before. Keep both raw series. Remittance-implied BDT is a QA check only. |
| 18 | BDT jumps +6.3% on 2024-05-10. WTI is −36.98 on 2020-04-20. | Both are real values; keep them. WTI is dropped as a driver per the chats; use Brent. |
| 19 | Three event files start with a BOM. | Read with `utf-8-sig`. |
| 20 | Event confidence varies; exporter_policy_events and the jatka bans are reconstructed. The Ramadan 2027 row is **present (confirmed)**. | Carry confidence as a feature or weight. Report results by confidence. |
| 21 | Event tables cover short spans. | Out-of-coverage periods are "unknown", not 0. |
| 22 | shock_events joins on Product. BD-S15's peak falls after its end date. | Join on Product. Raise S15 as a question; do not reorder its dates. |
| 23 | Shock magnitudes mix units. | Treat them as text. |
| 24 | bd_import_figures is not a time series. BB remittance and reserves start in 2024. | Context only; they are dropped as features per the chats. |
| 25 | **Import availability bug:** the old pipeline stamped Comtrade months available at month start + 75 days; real arrival is about 208 days. | `available_date = month_start + 208 days` (confirm, record in config). The leakage test must fail on the 75-day rule. All earlier import-driver results are void. |
| 26 | **Infinite import unit values** in zero-tonne months. | `unit_value = value / tonnes` only where tonnes > 0, else NaN with a flag. Assert no ±inf in any feature. |
| 27 | Missing drivers. | Leave cells empty, add `has_<slot>` flags, and never fill with 0 or a made-up value. |
| 28 | Stale drivers. | Cap carry-forward per frequency (config) beyond the true availability date. Past the cap, the value becomes missing. |
| 29 | **WFP dates in 1900** (for example 1900-08-15, fuel, Teknaf). | Quarantine every row dated before 2000 in `wfp_quarantine.csv`. Never guess a corrected year. |
| 30 | **Rohingya camp markets** (Balukhali, Kutupalong, Nayapara, Leda, Teknaf and similar) in Cox's Bazar. | Tag `is_camp_market` from a reviewed list shown to the user. Exclude them from national medians; keep them in market-level output. |
| 31 | WFP mixes price types, units and items across markets. | Filter and normalise explicitly (retail vs wholesale, unit, currency), each choice logged. Never pool across price types. |
| 32 | **Mendeley OHLC dates are in ambiguous day/month order and unsorted.** Its real coverage is unconfirmed. | Infer the order only if one reading is impossible (day > 12) for the whole file or per source block. Otherwise mark it blocked and ask. Report the measured first and last dates. |
| 33 | AgriPriceBD ends Jun 2025. TCB green chilli and cucumber start Feb 2026, so they have no overlap. | Cross-check only garlic and chickpea against TCB, and chilli against WFP (prior correlation about 0.91, to be reproduced, not cited as given). No bridge to Jul 2025+ is invented. |
| 34 | Pink Sheet and IMF overlap. | IMF stays the single G1 source. The Pink Sheet is used only to cross-check levels and turning points; never add both as features. |

The baseline file also has undocumented semantics. The training window, refit frequency, origin spacing and MASE scaling are not recorded, so S05 must **reproduce before extending** and never overwrite the committed file ([baseline results](https://claude.ai/artifact/394Xrk4k7LvgWcKwQePwNS)).

## The instruction set: files that let an agent resume rather than restart

The design copies what Anthropic found works for multi-session agents. An initializer session writes the scaffolding: a JSON feature list that later sessions may only flip, a progress log, an init script and a first commit. Every later session gets its bearings from files and git, runs an end-to-end check before new work, does one unit, verifies it, commits and logs it ([Anthropic harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). Anthropic's prompting guide adds three rules: JSON for state, plain text for notes, and git as the restorable checkpoint. It also notes that a fresh context window often beats compaction, because the model can "discover state from the local filesystem" ([Claude docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)). Claude Code's `/rewind` checkpoints do not cover files modified through Bash, so **git plus per-unit done-markers on Drive are the only reliable checkpoint** ([Claude Code](https://code.claude.com/docs/en/best-practices)). In Colab, a dropped runtime loses everything not on the mounted Drive, and the user already keeps everything in one Drive folder ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)). Each benchmark (model × variant × origin), alert (item × origin) and WFP market-item fit is therefore its own unit, with an atomic file and a `_SUCCESS.json` marker. DVC and Snakemake use the same principle and re-run only incomplete or changed outputs ([DVC](https://doc.dvc.org/user-guide/pipelines/running-pipelines); [Snakemake](https://linuxmanpag.es/man/1/snakemake/)).

The chats add three design changes. First, the agent often cannot execute anything in the user's Colab runtime or reach blocked data sites. The protocol therefore has a **human-runner mode**: the agent writes one notebook cell per unit, the user runs it and pastes the output, and the agent updates state only from that pasted evidence. Second, the 2025–26 test is protected by a **seal file**. A test run is refused unless the stage's pre-registration is committed, and a second unsealing needs a logged, approved deviation. This enforces "tune on 2024, test once" mechanically. Third, all downloads are manual drops into `data/raw/external/<source>/`, registered by hash. That matches the chats' finding that TCB, DAM and most data hosts block automated access ([Past chats](file:///home/claude/research_notes/Food%20price%20watch%20instructions%20with%20chats/past_chats_pasted.txt)).

The honesty rules address a documented failure mode. An audit of 30 long-horizon LLM research runs found that agents "quietly reduced datasets or training budgets" and swapped in oracle functions while still producing plausible metrics ([Yu et al.](https://tldr.takara.ai/p/2608.26753)). The countermeasures are a frozen spec, runnable checks, a provenance rule for every number, a deviation log, and an independent reviewer ([Claude Code](https://code.claude.com/docs/en/best-practices)). Paths assume a Drive root of `/content/drive/MyDrive/FoodPriceWatch`; change it once in `config.yaml`.

### 0. Manual data-drop checklist (the user does this once, before session 0)

```text
Put these on Google Drive under FoodPriceWatch/inbox/ before the setup session. The agent copies them into data/raw/ and hashes them; it never downloads them itself.

A. The 32 project files and the two docs (DATA_CARD.md, SOURCES_2026-10-26.md) -> inbox/project/
B. External price data you already hold -> inbox/external/
   wfp/           wfp_food_prices_bgd.csv, wfp_markets_bgd.csv
   agripricebd/   chickpea.csv, cucumber.csv, garlic.csv, green_chilli.csv, sweet_pumpkin.csv
   pinksheet/     CMO-Historical-Data-Monthly.xlsx
   ohlc/          Food Commodity Price OHLC Dataset of Bangladesh.csv (and the .zip)
C. Optional, only if you have them: original TCB daily Excel files (for the S02 audit) -> inbox/tcb_originals/
D. Optional later (stage S14, only if approved): BBS CPI PDFs; Bangladesh Bank exchange-rate Excel; ACLED export (needs Research access with your university email); GloFAS extract (needs a free Copernicus EWDS account); a hand-coded hartal/curfew calendar.
Record for each: where you got it and the date you downloaded it (a line in inbox/SOURCES_LOG.txt is enough).
Do not run pip on the work PC (Device Guard blocks it). Run everything in the Colab notebook.
```

### 1. Master setup prompt (paste into session 0 only)

```text
You are setting up the "Bangladesh Food Price Watch" master's PROJECT (not a thesis) so that an AI agent can run it end to end over many sessions and resume after any network or runtime drop without redoing finished work. This is the setup session only: do not run any modelling.

Context (read, do not assume beyond it):
- Aim: detect unexplained food price rises in Bangladesh, locate them (national vs one market), and explain them. Concretely: forecast Dhaka TCB daily retail prices h = 1/7/14/30 report days ahead; ask whether external drivers add value beyond persistence, and for which goods; raise alerts when a price leaves its expected range; use WFP monthly market prices to label flagged rises national, regional or local; split rises into "explained by measured cost drivers" and "not explained by measured cost drivers". Never describe residuals as hoarding, syndicates, collusion or manipulation.
- Inputs: the 32 project files plus DATA_CARD.md and SOURCES_2026-10-26.md, and (if supplied) WFP, AgriPriceBD, Pink Sheet and OHLC files in inbox/external/.
- Prior results to treat as provisional, never to cite as final: (a) baseline_results_by_group.csv, where no classical model beats naive; reproduce it, never overwrite it. (b) A one-driver-at-a-time test where matched drivers barely beat placebos (6.2% vs 6.0% significant); it used a buggy 75-day import availability rule, so it must be re-run.
- Environment: one Google Colab notebook, one Google Drive folder. If you cannot execute code yourself, work in human-runner mode (AGENTS.md): emit one cell at a time and wait for the pasted output.

Do these steps in order, and stop after step 10:
1. Confirm the Drive root from config.yaml (default /content/drive/MyDrive/FoodPriceWatch) is mounted. Work only inside it.
2. Create the layout: inbox/, data/raw/{project,external}/, data/interim/, data/processed/, outputs/, reports/{tables,figures}/, state/, config/, src/fpw/, src/stages/, tests/, logs/.
3. Copy inbox/project/* to data/raw/project/ and inbox/external/* to data/raw/external/ unchanged. Write data/raw/MANIFEST.csv (path, source, retrieved_at from inbox/SOURCES_LOG.txt or "unknown", bytes, sha256). List expected-but-missing external files as MISSING. Never edit data/raw/ after this.
4. Write AGENTS.md, CLAUDE.md, SPEC.md, state/stages.json, PROGRESS.md, DEVIATIONS.md, DECISIONS.md, config.yaml and config/item_driver_map.yaml exactly from the templates I give you, filling only the placeholders.
5. Write src/fpw/checkpoint.py from the template, and `make check` (or `python -m fpw.check`) that validates stages.json against disk markers and runs tests/.
6. Pin the environment (requirements.lock with exact versions, installed with pip inside Colab only) and set the global seed in config.yaml.
7. `git init` in the project root; .gitignore data/ and outputs/ (commit their hashes, not the data); commit "S00: scaffold [checks pass]".
8. Ask me every open decision D1-D10 in DECISIONS.md, in one message, and record my answers verbatim. Mark any I leave unanswered as PENDING. Do not choose for me.
9. If D3 says an external dataset is not supplied, set the stages that need only it (S03 parts, S08) to "blocked: data not supplied". Do not mark them skipped unless I say so.
10. Run `make check`, append PROGRESS.md, set S00 done only if checks pass, commit, and report using the session-end format.
```

### 2. AGENTS.md (keep it short; Claude Code reads it through CLAUDE.md)

```markdown
# AGENTS.md — Bangladesh Food Price Watch

## What this is
A master's PROJECT (not a thesis). The agent produces verified results; the human writes the report later from reports/ and reports/RESULTS_REGISTER.md. Scope and "done" live in SPEC.md. Machine state lives in state/stages.json. Narrative state lives in PROGRESS.md.

## Commands
- Check everything: `make check`    (stages.json vs disk markers, tests/)
- Run one stage:     `make stage S=NN` (idempotent; skips finished units)
- Dry run:           `make stage S=NN DRY=1`

## Two run modes
- Direct mode: you can execute in the Colab runtime. Run commands yourself.
- Human-runner mode: you cannot execute there (or the user prefers it). Emit ONE notebook cell per unit, ending with a printed summary (unit id, rows, sha256, check result). Wait for the user to paste the output. Update stages.json and PROGRESS.md only from pasted output. If no output was pasted, the unit is not done.
- Never write a local helper that needs pip on the work PC; local scripts must be Python standard library only. Heavy work runs in Colab.

## Startup ritual (every session, before any new work)
1. Confirm the Drive root from config.yaml is mounted; work only inside it.
2. Read, in order: this file, SPEC.md, DECISIONS.md, the last 2 PROGRESS.md entries, DEVIATIONS.md, state/stages.json, then `git log --oneline -20` and `git status`.
3. Delete *.tmp files under outputs/ and data/ (leftovers from a dropped session).
4. Run `make check`. It re-hashes every done stage's outputs against its _SUCCESS.json. If a check fails, set that stage to pending, log why, and do not pass it.
5. A stage marked in_progress is not trusted: keep only units with a valid _SUCCESS.json and resume at the next unit.
6. Pick the first stage whose status is not done/skipped and whose depends_on are all done or skipped. If it needs a PENDING decision or missing data, stop and ask.
7. Work on that one stage only.

## End-of-unit / end-of-stage ritual
- After each unit: atomic write, then its _SUCCESS.json marker. Commit at least every 30 minutes or every 20 units.
- After the stage: run its SPEC.md acceptance checks → update stages.json (status, output_sha256, git_commit, finished_at) → append PROGRESS.md → commit "SNN: <summary> [checks pass]" → stop and report.

## Rules that do not bend
- Never edit data/raw/. Corrections go to corrections_proposed.csv and need my approval.
- Never download from TCB, DAM or any blocked or credentialed site yourself. If a source is missing, mark the stage blocked and tell me exactly what file to drop into inbox/.
- Never fabricate, simulate or impute data unless SPEC.md says that stage does so. Missing drivers stay empty with a has_<slot> flag, never 0. Never fill prices across the 2022 gap.
- Every driver joins on its true availability date (config.availability). Comtrade imports: month start + 208 days, never 75. No ±inf anywhere.
- Every number in reports/ must come from a committed script and be listed in reports/RESULTS_REGISTER.md (value, file, command, commit). If you did not run it, say so.
- Never overwrite data/raw/project/baseline_results_by_group.csv or any earlier result; write new versions alongside.
- Test seal: the 2025-01..2026-10 test period may be scored only after the stage's pre-registration is committed, and only once. src/fpw/checkpoint.py enforces it. A second unsealing needs a DEVIATIONS.md entry that I approve.
- Driver groups are added to the core model one at a time, in the pre-registered order, on their mapped items only.
- Alert thresholds are fixed from 2024 non-event false-alarm rates before any event scoring. Never tune them on the 12 shock episodes.
- Wording: residual rises are "not explained by measured cost drivers". Never "hoarding", "syndicate", "collusion", "cartel" or "manipulation".
- Author: use config.yaml author. If it is TO_CONFIRM, put no name in any output.
- Any change to sample, items, dates, horizon, method, threshold or source goes into DEVIATIONS.md, with the reason, before you continue. Scope changes need my approval.
- Do not delete, edit or reorder entries in stages.json; update only their status fields.
- Ask before anything destructive or externally visible: rm -rf, git reset --hard, force-push, publishing (GitHub, Zenodo, arXiv), a public dashboard, any API key or account.

## Stop and ask when
- A needed decision is PENDING, or a needed file is MISSING in MANIFEST.csv.
- An acceptance check fails twice after honest fixes.
- A result strongly contradicts expectations (report it; do not tune until it fits).
- Baseline reproduction differs beyond tolerance.
- You find a data error not listed in SPEC.md §Data rules.
- A date, unit or market classification can only be resolved by guessing (OHLC day/month order, WFP 1900 rows, camp-market list, TCB↔WFP item crosswalk).

## Session-end report format
Done (check command and result) · Not done · Blocked (why, and what you need from me) · Deviations logged · Numbers I am unsure of · Next stage/unit.
```

```markdown
<!-- CLAUDE.md -->
@AGENTS.md
```

The `@AGENTS.md` import line for Claude Code was not verified in the research. If your tool does not support imports, paste AGENTS.md into CLAUDE.md. The AGENTS.md convention is read by Codex, Cursor, Gemini CLI, Copilot and others ([agents.md](https://www.agents.md)).

### 3. SPEC.md with per-stage acceptance criteria

```markdown
# SPEC.md — Bangladesh Food Price Watch (project, not thesis)

## Goal
Detect, locate and explain unexplained food price rises in Bangladesh. Forecast Dhaka TCB daily retail prices h = 1, 7, 14, 30 report days ahead; test whether external drivers add value beyond persistence, and for which goods; raise alerts when a price leaves its expected range; label flagged rises national/regional/local with WFP monthly market prices; decompose rises into "explained by measured cost drivers" and "not explained by measured cost drivers". Output: a reproducible repo and a results pack (reports/). The author writes the report later.

## Research questions
RQ1 Benchmark: on the 54 long-history series, does any model (Naive, SeasonalNaive, WindowAverage, RWD, AutoARIMA, AutoETS, AutoTheta, LightGBM, Chronos-2) beat naive, per eval_stratum and horizon?
RQ2 Driver value: starting from a core model (price + G0 calendar), does adding each driver group G1..G5 (one at a time, pre-registered order, mapped items only) improve over core and over naive, and does the matched driver beat a placebo assignment?
RQ3 Alerts: do interval-based alerts flag the 12 in-window shocks (BD-S09, S11, S12, S13, S14, S15, S16, S17, S19, S20, S21, S22) before news_peak, with how many false alarms per item-year, vs ALPS-style and IFPA-style rules?
RQ4 Explanation: for priority-item rises, what share do M0 ⊂ M1 ⊂ M2 explain and what residual remains; event studies for India's Dec 2023 onion ban, 2024-25 FX moves, and the Sep 2023 caps only if DECISIONS D10 supplies dated, sourced cap events.
RQ5 Locate (if WFP supplied): for each item-month flagged in WFP (ALPS-style, real-time trend) or by TCB alerts, what share of non-camp markets is in alert (breadth), and is the rise national, regional or local; do WFP Dhaka markets agree with TCB?

## Out of scope unless DECISIONS.md says otherwise
Dataset or benchmark papers, Zenodo, public dashboard, TimesFM and other extra foundation models, deep learning from scratch, river discharge, DAM wholesale, daily market-level modelling outside Dhaka, ACLED/GloFAS/CPI/hartal sources (optional S14).

## Evaluation protocol (fixed)
- Time index: report days. gap_2022 = 2022-03-12..2022-12-31 is history only; no price is filled across it.
- Split: tuning/validation = calendar 2024 (all hyperparameters, weather-feature choice, G1 series list, carry caps, alert thresholds). Test = Jan 2025 - Oct 2026, the same 87 origins as the existing baseline (S05 recovers them; if impossible, monthly origins in that span, logged). Expanding window. The test is unsealed once per stage (seal file).
- RQ2 tests: per group, DM-HLN of (core + group) vs core on each mapped item, Holm across items within the group, alpha 0.05, pre-registered in state/prereg_S06.yaml. Placebo: the same group assigned to unmapped items drawn with a fixed seed; report the matched-minus-placebo gap with a bootstrap CI.
- RQ3 origins: daily one-step-ahead from config.alert_eval_start (2023-06-01), refit every config.refit_every; thresholds frozen from 2024 non-event periods; report 2025-26 events separately as the clean test.
- Metrics: MAE (Tk), MASE (in-sample one-step naive scaling), gmean relMAE vs naive, win rate; pinball (0.9, 0.95), coverage, Winkler; DM-HLN + Holm; event recall, lead days (report and calendar days), false alarms per item-year, PR curve; Kupiec on non-event periods. Short-history items are scored and reported separately.
- Availability: monthly world prices month end + 40 d; Comtrade month start + 208 d; weather + 5 d; daily FX/Brent as of the last value on or before the report date; carry caps per config. Event matching window [onset - 14 d, news_peak + 30 d].
- RQ5: WFP retail prices only, one unit and currency per item after normalisation; market × item monthly ALPS-style residual with an expanding (real-time) trend + month dummies, alert z >= 1; national median from markets with is_camp_market = 0; breadth = share of reporting non-camp markets in alert; national if breadth >= 0.5, regional if 0.2-0.5 or all alerts in one division, local otherwise (cutoffs pre-registered in prereg_S08.yaml; change only via DECISIONS).

## Data rules (each has a test in tests/)
1 report-day index · 2 gap_2022, no fill across · 3 rebuild item_id and derived columns, output tcb_v1.0_rebuilt · 4 Palm Olein 2 L 2025-04-18 → corrections_proposed.csv; palm olein excluded · 5 two Min-only rows flagged · 6 ginger 2021 reversals flagged · 7 audit needs originals else blocked · 8 item_meta %d-%m-%y · 9 CSV once · 10 normalise pack sizes · 11 respect eval_stratum · 12 missing = not reported · 13 Comtrade blank ≥ 202605, zero-pad HS, never assign 703/910 to one item · 14 IMF parser, PCHANA USD/100 kg · 15 FAO skiprows=1 · 16 weather blocks, coordinate mapping logged, drop last day · 17 FX splice npm from 2024-03-02, Yahoo × 1.0151 before; remittance-implied rate as QA only · 18 keep real jumps; WTI dropped · 19 utf-8-sig · 20 carry confidence · 21 out-of-coverage = unknown · 22 shock join on Product; S15 question · 23 magnitudes are text · 24 import_figures, remittance, reserves context only · 25 Comtrade available = month start + 208 d; leakage test must fail on 75 d · 26 unit value NaN when tonnes = 0; no ±inf · 27 missing driver = empty + has_ flag, never 0 · 28 carry caps · 29 WFP rows dated < 2000 quarantined · 30 camp markets tagged from a user-approved list, excluded from national medians · 31 WFP price type/unit/currency filtered and logged · 32 OHLC day/month order resolved only if unambiguous, else blocked · 33 AgriPriceBD cross-check garlic, chickpea vs TCB and chilli vs WFP; no invented bridge · 34 IMF is the only G1 source; Pink Sheet cross-check only.

## Stages and acceptance criteria
S00 Scaffold + intake — all project files and supplied external files in MANIFEST with sha256; missing ones listed MISSING; config.yaml, item_driver_map.yaml, DECISIONS.md present; `make check` passes; first commit.
S01 Rebuild panel — 76,440 rows; 1,412 dates (2021-05-17..2026-10-24); 63 item_ids equal to item_meta; 0 duplicate (Date, item_id); Avg == (Min+Max)/2 except 2 flagged rows; Min ≤ Max; Week_Ago_Min matches own Min 7 calendar days earlier on ≥ 99.5% of matchable rows; corrections.csv reflected (MS Rod 70,500; Palm Olein 5 L 2025-04-18 missing); corrections_proposed.csv; parquet + sha256; T1, F1, F2.
S02 Audit (human-in-the-loop) — audit sheet from audit_sample_2pct.csv and audit_candidates.csv; if originals supplied and checked: error rate with Wilson 95% CI over 1,530 values and a decision per ginger candidate; else blocked. T2 either way ("not measured" if blocked).
S03 External intake + cross-checks — each supplied source parsed by a dedicated reader with a unit test. WFP: rows < 2000 quarantined (count reported), price type/unit/currency normalised, camp-market list proposed and approved, TCB↔WFP item crosswalk proposed and approved, measured coverage per item × market. AgriPriceBD: 5 series, measured dates. Pink Sheet vs IMF: level correlation and turning-point agreement on mapped commodities. OHLC: day/month order resolved or blocked; measured first/last dates, markets, items; note on whether it duplicates TCB (novelty check). T3b produced. Missing sources → their parts blocked, the rest proceeds.
S04 Driver panel — one long item × date table on report days with G0..G5 slots and E1..E4 explanation columns per config/item_driver_map.yaml; has_<slot> flags; availability dates and carry caps applied; leakage test passes (shifting any driver one availability step later changes no feature before that step; the 75-day import rule must fail the test); no ±inf; Comtrade 208-day lag confirmed or the value used recorded; weather reduced to ≤ 3 features chosen on 2024 only; G1 series list fixed on 2024; T3.
S05 Reproduce baseline — statsforecast models re-run under recovered settings (training window, refit, origins, season length 7, MASE scaling) written to config; ALL-stratum gmean relMAE within ±0.02 of baseline_results_by_group.csv for every model × horizon, or differences explained; original untouched.
S06 Core benchmark + driver value — prereg_S06.yaml committed before unsealing (core spec, group order G1..G5, mapped items, tests, alpha, placebo seed); 2024 tuning done before unsealing; LightGBM core and core + each group, Chronos-2 price-only (and with covariates if supported, else logged); unit = (model, variant, origin) with marker; test unsealed once; T4, T5, T5b, F3, F4.
S07 Intervals and alerts — conformal (or quantile) intervals with coverage per stratum; prereg_S07.yaml (rules, levels, persistence, operating point from 2024 non-event false alarms) committed before event scoring; ALPS-style and IFPA-style baselines on the same data; all 12 events in T7 including misses and low-confidence ones, tagged test vs in-sample; T6, T8, F5, F6, F7.
S08 Locate (WFP; skipped if D3/D9 say so) — prereg_S08.yaml committed before scoring; unit = (market, item) fit with marker; national median excludes camp markets; breadth labels for every WFP-flagged item-month and every TCB-flagged month with WFP coverage; TCB-vs-WFP Dhaka agreement; T12, F10.
S09 Explanation — M0, M1, M2 per priority item; share explained per episode; SHAP global and per-episode; sign checks (FX, world price); India/Indonesia ban dates verified against cited sources before use, or results marked "reconstructed dates"; wording test passes; T9, T10, F8, F9.
S10 Robustness — weekly vs daily, Min/Max/Avg, sliding vs expanding, placebo event dates (flag rate near nominal), leave-one-event-out, ginger candidates excluded, reconstructed-event rows excluded; T11.
S11 Results pack — clean re-run on a copy reproduces T4, T5, T7, T9 (and T12 if run) exactly with the seed; RESULTS_REGISTER.md lists every number with file, command, commit; reports/README.md indexes tables and figures by RQ.
S12-S14 Optional (dashboard; extra foundation models; data-gap sources: BBS CPI with base-year link factor, BB FX, ACLED, GloFAS, hartal calendar) — only if DECISIONS.md enables them; each new source goes through S03-style intake first.
S99 Review — a fresh reviewer session checks every SPEC line against the repo, pass/fail with evidence.
```

### 4. state/stages.json (the resume ledger)

```json
{
  "schema": "fpw-stages-v2",
  "rules": "Agents may change only status, started_at, last_unit, units_done, output_sha256, git_commit, finished_at, notes. Never delete or reorder entries. Status: pending | in_progress | done | blocked | skipped (skipped only by a recorded user decision).",
  "stages": [
    {"id": "S00", "title": "Scaffold + intake", "depends_on": [], "outputs": ["data/raw/MANIFEST.csv"], "checks": ["make check"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S01", "title": "Rebuild TCB panel", "depends_on": ["S00"], "outputs": ["data/processed/tcb_v1.0_rebuilt.parquet", "data/processed/corrections_proposed.csv", "reports/tables/T1.csv"], "checks": ["pytest tests/test_s01_panel.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S02", "title": "Audit (human-in-the-loop)", "depends_on": ["S01"], "outputs": ["reports/tables/T2.csv"], "checks": ["pytest tests/test_s02_audit.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "blocked unless original TCB files are supplied"},
    {"id": "S03", "title": "External intake + cross-checks (WFP, AgriPriceBD, Pink Sheet, OHLC)", "depends_on": ["S01"], "outputs": ["data/processed/wfp_clean.parquet", "data/processed/wfp_quarantine.csv", "config/camp_markets.yaml", "config/tcb_wfp_crosswalk.yaml", "reports/tables/T3b.csv"], "checks": ["pytest tests/test_s03_external.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "unit = source; missing sources block only their part"},
    {"id": "S04", "title": "Driver panel (long table, slots, availability)", "depends_on": ["S01"], "outputs": ["data/processed/features.parquet", "reports/tables/T3.csv"], "checks": ["pytest tests/test_s04_drivers.py tests/test_leakage.py tests/test_no_inf.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "Comtrade month start + 208 d"},
    {"id": "S05", "title": "Reproduce baseline", "depends_on": ["S01"], "outputs": ["outputs/05_baseline/results_by_group_repro.csv"], "checks": ["pytest tests/test_s05_repro.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S06", "title": "Core benchmark + driver groups one at a time", "depends_on": ["S04", "S05"], "outputs": ["state/prereg_S06.yaml", "reports/tables/T4.csv", "reports/tables/T5.csv", "reports/tables/T5b.csv"], "checks": ["pytest tests/test_s06_grid.py tests/test_seal.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "unit = model/variant/origin; test unsealed once"},
    {"id": "S07", "title": "Intervals and alerts", "depends_on": ["S06"], "outputs": ["state/prereg_S07.yaml", "reports/tables/T6.csv", "reports/tables/T7.csv", "reports/tables/T8.csv"], "checks": ["pytest tests/test_s07_alerts.py tests/test_seal.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "unit = item/origin"},
    {"id": "S08", "title": "Locate (WFP monthly market module)", "depends_on": ["S03", "S07"], "outputs": ["state/prereg_S08.yaml", "reports/tables/T12.csv"], "checks": ["pytest tests/test_s08_locate.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "unit = market/item; skipped only if D9 says so"},
    {"id": "S09", "title": "Explanation ladder + event studies", "depends_on": ["S06", "S07"], "outputs": ["reports/tables/T9.csv", "reports/tables/T10.csv"], "checks": ["pytest tests/test_s09_explain.py tests/test_wording.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S10", "title": "Robustness", "depends_on": ["S07", "S08", "S09"], "outputs": ["reports/tables/T11.csv"], "checks": ["pytest tests/test_s10_robust.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S11", "title": "Results pack + clean re-run", "depends_on": ["S10"], "outputs": ["reports/RESULTS_REGISTER.md", "reports/README.md"], "checks": ["make rerun-diff"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S12", "title": "Optional: dashboard", "depends_on": ["S11"], "outputs": [], "checks": [], "status": "skipped", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "enable via DECISIONS D1; externally visible: ask first"},
    {"id": "S13", "title": "Optional: extra foundation models", "depends_on": ["S06"], "outputs": [], "checks": [], "status": "skipped", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "needs a new seal/prereg; enable via DECISIONS"},
    {"id": "S14", "title": "Optional: data-gap sources (CPI, BB FX, ACLED, GloFAS, hartal)", "depends_on": ["S04"], "outputs": [], "checks": [], "status": "skipped", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "enable via DECISIONS D10; user downloads manually"},
    {"id": "S99", "title": "Independent review", "depends_on": ["S11"], "outputs": ["reports/REVIEW.md"], "checks": [], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "run in a fresh session"}
  ]
}
```

JSON holds state, rather than Markdown, because Anthropic found models less likely to overwrite or rewrite it improperly ([Anthropic harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). The `skipped` status lets the project finish honestly when WFP, the TCB originals or an optional source never arrive. Dependents proceed, and the skip shows up in the results pack as a limitation rather than a silent hole.

### 5. PROGRESS.md, DEVIATIONS.md and DECISIONS.md templates

```markdown
<!-- PROGRESS.md — append-only; newest entry at the bottom -->
## 2026-MM-DD HH:MM — session N — stage SNN — mode: direct | human-runner
- Resumed from: <stage/unit, or "fresh">; startup check: <make check summary>
- Did: <units completed, e.g. S06 core+G1 origins 31-58>
- Verified: <command> → <result>  (human-runner: "output pasted by user")
- Open issues: <...>
- Next: <stage/unit>
```

```markdown
<!-- DEVIATIONS.md — one entry per change from SPEC.md, written BEFORE continuing -->
| date | stage | what changed (sample/items/dates/method/threshold/source/seal) | reason | approved by user? |
|---|---|---|---|---|
```

```markdown
<!-- DECISIONS.md — the agent records the user's answers verbatim; PENDING blocks dependent stages -->
D1 Framing: project (stated by user) vs thesis; papers/Zenodo/dashboard in or out; supervisor's answer on "dataset paper + benchmark": PENDING
D2 Author name for all outputs (documents currently say "Romjan Chowdhury"): PENDING
D3 External data supplied to inbox/external/? WFP prices+markets / AgriPriceBD 5 CSVs / Pink Sheet / OHLC (each yes/no): PENDING
D4 Abnormal-rise rule (default: conformal 95% upper bound, 3-of-5 persistence; ALPS-style z 1/2/3 alongside; operating point from 2024 non-event false alarms): PENDING
D5 Attribution (default: M0 ⊂ M1 forecasting drivers ⊂ M2 + FX/fuel/imports/events; TreeSHAP secondary): PENDING
D6 Horizon unit (default: report days): PENDING
D7 Priority items (default about 16: sugar; egg; onion local; onion imported; potato; rice coarse; rice medium; soybean oil bottled 1 L; soybean oil loose; atta loose; palm oil loose; lentil large; chickpea; garlic imported; one milk powder; green chilli alerts-only): PENDING
D8 Split (default: tune on 2024; test Jan 2025-Oct 2026 once; alerts from 2023-06 with 2025-26 events reported separately): PENDING
D9 Locate module (default: monthly WFP market module RQ5, camp markets excluded from national medians, breadth cutoffs 0.5 / 0.2): PENDING
D10 Data-gap sources and events: rivers/IFPRI dropped; S14 (CPI, BB FX, ACLED, GloFAS, hartal) on or off; India/Indonesia ban dates verification; Sep 2023 cap dates and source: PENDING
Other: TCB licence/no-objection; OHLC novelty check; department deadlines; constraints in Learnathon-Project-Scan.pdf, Masters_Project_Ideas.pdf, Meeting-Prep-Notes.pdf (not yet seen): PENDING
```

### 6. config.yaml and config/item_driver_map.yaml

```yaml
# config.yaml
project_root: /content/drive/MyDrive/FoodPriceWatch
author: TO_CONFIRM                 # D2
seed: 20261029
time_index: report_day             # D6
gap_2022: ["2022-03-12", "2022-12-31"]
horizons: [1, 7, 14, 30]
split:                             # D8
  tune: ["2024-01-01", "2024-12-31"]
  test: ["2025-01-01", "2026-10-24"]
  test_unseal_limit: 1
benchmark_origins: recover_from_baseline   # else monthly in test span (log deviation)
alert_eval_start: "2023-06-01"
refit_every: 30                    # report days; actual value recorded in markers
availability:                      # days; applied before any join
  monthly_world_after_month_end: 40
  comtrade_after_month_start: 208  # was 75 (bug); confirm in S04
  weather: 5
  daily_asof: true
carry_cap_days: {daily: 7, monthly: 45, events: 0}   # beyond availability; then missing (tune on 2024)
comtrade_blank_from: 202605
fx_splice: {npm_from: "2024-03-02", yahoo_scale: 1.0151}
priority_items: []                 # D7 — exact item_ids from item_meta.csv
driver_group_order: [G1_world_price, G2_brent, G3_export_measure, G4_fishing_ban, G5_weather]
weather_max_features: 3
alerts:                            # D4 — frozen into state/prereg_S07.yaml before scoring
  rule: conformal_upper
  level: 0.95
  persistence: {k: 3, m: 5}
  z_bands: {stress: 1, alert: 2, crisis: 3}
  event_window_days: {before_onset: 14, after_peak: 30}
locate:                            # D9 — frozen into state/prereg_S08.yaml
  enabled: true
  min_year: 2000                   # rows before this go to wfp_quarantine.csv
  price_type: Retail
  alert_z: 1
  breadth_cutoffs: {national: 0.5, regional: 0.2}
explanation: {ladder: [M0_core, M1_forecast_drivers, M2_explain_drivers], shap: true}   # D5
banned_words: [hoarding, syndicate, collusion, manipulation, cartel]
optional: {dashboard: false, extra_foundation_models: false, data_gap_sources: false}
```

```yaml
# config/item_driver_map.yaml — shown to the user in S04 before features are built
# Forecasting slots (added one group at a time in S06). Unmapped items: empty + has_<slot>=0.
G0_calendar: all
G1_world_price:          # IMF series per item; exact list fixed on 2024 data in S04
  soybean_oil_items: POILSOY
  palm_oil_items: POILAPSP   # deduplicate the repeated column first
  atta_maida_items: PWHEAMT
  rice_items: PRICENPQ
  milk_powder_items: TO_CONFIRM   # check the IMF dairy series code in the description row
G2_brent: [milk_powder_items, "Dried Chilli - Imported"]
G3_export_measure: ["Onion - Local", "Onion - Imported"]   # exporter_policy_events (reconstructed)
G4_fishing_ban: ["Hilsa Fish"]
G5_weather: [Potato, "Onion - Local", Brinjal (Eggplant), Cucumber, Green Chilli, "Ginger - Local", "Garlic - Local"]
# Explanation-only (M2 and S09; never in the S06 forecasting comparison)
E1_fx: imported_items
E2_fuel: all
E3_imports: by_hs_code       # HS 703/910 never assigned to a single item
E4_events: [disruption, cyclones_floods, import_duty, political_wage]
dropped: [bb_remittance, bb_reserves, DEXCHUS, DEXINUS, DEXMAUS, wti, rivers, ifpri]
```

The IMF series codes in the map are the usual IMF primary-commodity mnemonics. They were not checked against the attached file's description row, so S04 must confirm each one, and the milk-powder code is left as `TO_CONFIRM` on purpose.

### 7. Checkpoint helper with the test seal (src/fpw/checkpoint.py)

```python
"""Atomic writes, per-unit done-markers and a test seal, so a dropped session resumes, not restarts."""
import hashlib, json, os, subprocess, time
from pathlib import Path

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def _git(*args) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()

def atomic_write_parquet(df, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)                      # never leaves a half file that looks complete

def marker_path(out: Path) -> Path:
    return out.parent / (out.name + "._SUCCESS.json")

def is_done(out: Path) -> bool:
    m = marker_path(out)
    if not (out.exists() and m.exists()):
        return False
    return json.loads(m.read_text()).get("sha256") == sha256(out)

def mark_done(out: Path, *, inputs: dict, config_hash: str, seed: int, rows: int):
    payload = {"output": str(out), "sha256": sha256(out), "inputs": inputs, "config_hash": config_hash,
               "seed": seed, "rows": rows, "code_commit": _git("rev-parse", "HEAD"),
               "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    tmp = marker_path(out).with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2))
    os.replace(tmp, marker_path(out))

def run_unit(out: Path, compute, **meta):
    """compute() -> DataFrame. Skips if a valid marker exists."""
    if is_done(out):
        return "skipped"
    df = compute()
    atomic_write_parquet(df, out)
    mark_done(out, rows=len(df), **meta)
    return "done"

def unseal_test(stage: str, prereg: Path, seal_dir: Path = Path("state/seals"), limit: int = 1):
    """Call once before scoring the test period. Refuses if the pre-registration is not committed
    or if the stage's test was already unsealed `limit` times. A resumed session re-uses the
    existing seal (same prereg hash) instead of counting a new unsealing."""
    if _git("status", "--porcelain", str(prereg)) or not _git("log", "-1", "--format=%H", "--", str(prereg)):
        raise RuntimeError(f"{prereg} must be committed before unsealing the test for {stage}")
    seal_dir.mkdir(parents=True, exist_ok=True)
    seal = seal_dir / f"{stage}.json"
    h = sha256(prereg)
    rec = json.loads(seal.read_text()) if seal.exists() else {"unsealings": []}
    if any(u["prereg_sha256"] == h for u in rec["unsealings"]):
        return "resumed"                       # same plan; a drop mid-test does not count twice
    if len(rec["unsealings"]) >= limit:
        raise RuntimeError(f"Test for {stage} already unsealed; needs an approved DEVIATIONS.md entry")
    rec["unsealings"].append({"prereg_sha256": h, "commit": _git("rev-parse", "HEAD"),
                              "at": time.strftime("%Y-%m-%dT%H:%M:%S")})
    tmp = seal.with_suffix(".tmp"); tmp.write_text(json.dumps(rec, indent=2)); os.replace(tmp, seal)
    return "unsealed"
```

Use the same skip-if-hash-matches pattern for intake. Copy each inbox file once, hash it, and skip it on re-run. If the user's existing Colab module `pl` already has loader or download functions (`pl.download_rivers`, `pl.download_global`) ([SOURCES](project://SOURCES_2026-10-26.md)), the agent should open and reuse them, but only after checking that their import-availability stamp is not the buggy 75-day rule.

### 8. Resume prompt (paste at the start of every session after S00, including after any drop)

```text
Resume the Bangladesh Food Price Watch project. Follow the startup ritual in AGENTS.md exactly: confirm the Drive root is mounted; read AGENTS.md, SPEC.md, DECISIONS.md, the last two PROGRESS.md entries, DEVIATIONS.md, state/stages.json and the git log; delete *.tmp leftovers; run `make check` and re-verify every done stage's markers. Do not redo any unit with a valid _SUCCESS.json. Continue at the first unfinished unit of the first stage whose dependencies are done or skipped. Work on that one stage only. If you cannot execute in my Colab runtime, use human-runner mode: give me one cell at a time and wait for my pasted output. Commit at least every 20 units. Never unseal a test period twice. When the stage's SPEC.md acceptance checks pass, update stages.json, append PROGRESS.md, commit "SNN: ... [checks pass]", and stop with the session-end report. If a needed decision is PENDING, a needed file is MISSING, or a stop-and-ask condition occurs, stop and ask instead.
```

### 9. Suggested per-session prompts (append to the resume prompt)

```text
S01: "This session: S01 Rebuild panel. Pay attention to data rules 3, 4 and 5. Write corrections_proposed.csv for the Palm Olein 2 L 2025-04-18 row and show it to me; do not apply it."
S02: "This session: S02 Audit. Prepare reports/audit/audit_sheet.xlsx (one row per sampled value, columns for the original value and a checked flag). If inbox/tcb_originals/ is empty, mark S02 blocked and continue only with stages that do not depend on it."
S03: "This session: S03 External intake. One unit per source. WFP: quarantine rows dated before 2000 and report the count; propose config/camp_markets.yaml (Balukhali, Kutupalong, Nayapara, Leda, Teknaf and similar, matched against wfp_markets_bgd.csv) and config/tcb_wfp_crosswalk.yaml, and show me both before using them. OHLC: test the day/month order; if any part is ambiguous, stop and show me examples. AgriPriceBD: cross-check garlic and chickpea against TCB, and chilli against WFP; report the correlation you measure, not the 0.91 from earlier. Pink Sheet: cross-check only. Write T3b."
S04: "This session: S04 Driver panel. Show me config/item_driver_map.yaml (with the IMF codes confirmed) before building. Build one long item x date table on report days with slots and has_ flags; no zeros for missing. Apply availability lags: Comtrade month start + 208 days (show me the evidence for the value you use). Prove the leakage test fails under the old 75-day rule and passes under the new one. Assert no +/-inf (zero-tonne months -> NaN). Choose at most 3 weather features using 2024 data only."
S05: "This session: S05 Reproduce the existing baseline. First recover or document training window, refit cadence, origin dates, season length and MASE scaling. If you cannot match within +/-0.02, stop and show me the diff."
S06: "This session: S06 Core benchmark and driver groups. Tune on 2024 first. Then write and commit state/prereg_S06.yaml (core spec, group order, mapped items, tests, alpha, placebo seed) and call unseal_test('S06', ...). Units are (model, variant, origin); check markers before computing. Add one driver group at a time. Run the matched-vs-placebo comparison. If Chronos-2 covariate support is unavailable, run price-only and log it. If GPU time runs out, stop at a unit boundary."
S07: "This session: S07 Intervals and alerts. Fix thresholds from 2024 non-event false-alarm rates, commit state/prereg_S07.yaml, then score. Report all 12 in-window events, misses included, with confidence ratings, and tag each as test (2025-26) or in-sample (2023-24)."
S08: "This session: S08 Locate. Commit state/prereg_S08.yaml first. Units are (market, item). Use an expanding (real-time) trend. Exclude camp markets from national medians but keep them in market output. Label each flagged item-month national/regional/local and compare with TCB Dhaka alerts. Write T12 and F10."
S09: "This session: S09 Explanation. Verify the India/Indonesia export-ban dates against cited sources first, or mark results 'reconstructed dates'. Use the neutral residual label only; tests/test_wording.py must pass. Flag any episode where FX or world-price contributions have the wrong sign."
S10: "This session: S10 Robustness, including placebo dates, leave-one-event-out, and excluding reconstructed events."
S11: "This session: S11 Results pack. Do a clean re-run on a copy, diff T4, T5, T7, T9 (and T12), and build RESULTS_REGISTER.md. Do not write report prose; the author writes the report."
```

### 10. Reviewer prompt (fresh session, S99)

```text
You did not build this repo. Review it against SPEC.md line by line. For each requirement, give PASS/FAIL with evidence (file path, command run, output). Check specifically: (1) every number in reports/ appears in RESULTS_REGISTER.md and can be regenerated; (2) no evaluation window contains gap_2022 dates and no price was filled across it; (3) each prereg_*.yaml was committed before its stage's test or event scoring (compare git timestamps with state/seals/), and no test was unsealed more than once without an approved deviation; (4) Comtrade features use month start + 208 days and the leakage test fails under 75 days; (5) no feature contains 0 where a driver is missing, and none contains +/-inf; (6) data/raw/ hashes match MANIFEST.csv; (7) baseline_results_by_group.csv is unchanged; (8) all 12 shock events appear in T7; (9) WFP national medians exclude camp markets and rows dated before 2000 are quarantined; (10) no banned words in outputs; (11) every DEVIATIONS.md entry is reflected in results; (12) no name appears if author is TO_CONFIRM. Write reports/REVIEW.md. Do not fix anything; report only.
```

If you use Claude Code, back the key rules with deterministic controls: a deny rule or PreToolUse hook blocking edits under `data/raw/` and `state/seals/`, and a Stop hook that runs `make check`. Claude Code's guidance is that a rule which keeps getting missed belongs in a hook ([Claude Code](https://code.claude.com/docs/en/best-practices)). In claude.ai sessions and in human-runner mode, hooks may not exist. There, the ledger, markers, seal file and git carry the whole guarantee, and the user's pasted cell output is the only evidence a unit ran.

## Conclusion

The chats move the project's centre of gravity. Before them, the risk looked like weak models. Now the evidence says the real risks were **leakage and over-claiming**. A one-driver screen whose matched and placebo hit rates are almost identical (6.2% vs 6.0%), run with import data four months too early, cannot support "drivers improve forecasts". It can only say that world prices are worth a careful, pre-registered test. That is why the instruction set spends its machinery on a test seal, true availability dates and a placebo control rather than on more models. The honest headline the project can deliver either way is a per-good map of where external information adds value beyond persistence. If that map shows world prices helping oils, flour and rice and almost nothing else, that is a useful negative result for a market where most prices sit unchanged day to day.

The WFP data turn the project's least-developed promise, locating rises, into a cheap monthly module rather than a second daily system. The camp-market exclusion and date quarantine make the "national vs one market" label defensible, and RQ5 is the only part of the work that reaches beyond Dhaka. What still needs a human is mostly not analytical. It is uploading four datasets the user already holds, supplying the TCB originals for the audit, confirming whose name goes on the work, and getting the supervisor's answer on project versus thesis. Until those arrive, the agent can complete S00, S01, S04 and S05, and leave every dependent stage visibly blocked rather than quietly assumed.
