# Turning Food Price Watch into a resumable project

The Bangladesh Food Price Watch should be finished as a **seven-phase applied project with one results pack**, not as a thesis. The pack answers four re-scoped questions. (1) Does anything beat "tomorrow = today"? (2) Do drivers help? (3) Do forecast-interval alerts catch the 12 documented shocks inside the data? (4) How much of each rise do measured cost drivers explain, and how much is left over? The hard part is already done. A frozen 63-series, 1,412-report-day TCB panel exists, and a first benchmark found that **no classical model beats naive at any horizon** (best is AutoETS, geometric-mean relative MAE 1.17/1.05/1.04/1.03 at h=1/7/14/30) ([baseline results](https://claude.ai/artifact/394Xrk4k7LvgWcKwQePwNS)). What remains is extending that benchmark to LightGBM and Chronos-2, building alerts and the explained-vs-unexplained breakdown, and packaging every number so the user can write the report later. The AI instruction set below follows Anthropic's long-running-agent pattern: a setup session, then one verified stage per session, with a JSON ledger, an append-only progress log, done-markers and a git commit per stage. After a dropped Colab or network session, the agent re-verifies finished work and **resumes at the first incomplete unit instead of restarting** ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). Four things need the user's answer before the agent starts. All existing documents frame the work as an MSc thesis with two papers. Every artifact names **Romjan Chowdhury** as author. No WFP or AgriPriceBD data is among the 32 project files. No threshold for "abnormal" has been set. The three past chats could not be opened, so any supervisor feedback recorded there is missing from this synthesis.

## A thesis-shaped plan built around a five-part watch

The project's stated goal is "to build and evaluate a Bangladesh Food Price Watch: an open dataset and model that forecast Dhaka retail prices 1–30 days ahead and raise an early, explained alert when a price rises abnormally" ([Proposal](https://claude.ai/artifact/7Ud96n6HY5rVPLn57zM4Nh)). The proposal splits this into five deliverables: an open dataset, a benchmark, an early-warning method, an explanation layer, and a free daily dashboard. "Unexplained" is defined only in words: the share of a rise not accounted for by world prices, the exchange rate, fuel, weather and policy. It must be labelled "not explained by measured cost drivers", **never as hoarding or syndicates** ([Deck](https://claude.ai/artifact/NUnU3Rj4BCu4xGFegUrPgi)). That neutral wording matches the Bangladesh literature. Taslim and Hossain found soybean-oil pass-through is asymmetric but argue this "does not necessarily mean collusion" ([BIDS](https://ideas.repec.org/a/ris/badest/0777.html)). CPD's 2026 market-chain study similarly warns that concentration "does not establish ... collusion" ([CPD](https://cpd.org.bd/resources/2026/07/The-Food-Price-Chain_Markets-Margins-and-Intermediaries-in-Bangladesh.pdf)).

The data work is complete and documented. The panel covers **17 May 2021 to 24 Oct 2026, 1,412 report days, 63 item×unit series and 76,440 rows**. It was built from 1,417 downloaded TCB Bangla Excel files (2 corrupt and 3 duplicate dates dropped) with a fixed-dictionary translator. Four values were corrected by hand ([DATA_CARD](project://DATA_CARD.md)). Series are grouped into six evaluation strata plus a short-history group: imported staples 19, volatile perishables 10, spices 8, domestic staples 7, government-set 7, non-food 3, short history 9 ([Proposal](https://claude.ai/artifact/7Ud96n6HY5rVPLn57zM4Nh)). Drivers are already collected: daily FX and oil, 13-location ERA5 weather, monthly IMF/FAO/Comtrade/Bangladesh Bank series, and event tables. These are dated by publication rather than by reference period. Monthly world prices enter about 40 days after the month, imports about 75 days after, and weather with a 5-day lag ([Deck](https://claude.ai/artifact/NUnU3Rj4BCu4xGFegUrPgi)). Twenty-two shock episodes are mapped to TCB items. **Only 12 fall inside usable data** (BD-S09, S11–S17, S19–S22), and 7 of those 12 are rated low confidence ([shock_events.csv](https://claude.ai/artifact/394Xrk4k7LvgWcKwQePwNS)).

One result exists. Seven classical models were scored against naive across 87 forecast starts (Jan 2025–Oct 2026) on 54 series. They were significantly better on only one series (imported onion) and significantly worse on up to 53. Tests used Diebold–Mariano with the Harvey–Leybourne–Newbold correction and a Holm correction ([Deck](https://claude.ai/artifact/NUnU3Rj4BCu4xGFegUrPgi)). Naive is hard to beat because government-set oils and sugar sit unchanged on about 85% of report days ([DATA_CARD](project://DATA_CARD.md)). The closest prior work, AgriPriceBD, also found naive best on 4 of 5 items ([Proposal](https://claude.ai/artifact/7Ud96n6HY5rVPLn57zM4Nh)). This result matters for the outline. If point accuracy cannot beat persistence, the project's contribution has to come from **interval calibration, alerting and attribution**, with the benchmark as the honest floor.

The existing artifacts are all thesis-shaped. The deck cover reads "MSc research proposal". The plan slide promises a dataset paper in December 2026, a benchmark paper on arXiv in February 2027 and a "Final thesis" at the end of April 2027. The speaker notes call the dataset and benchmark "the core of the thesis" ([Deck](https://claude.ai/artifact/NUnU3Rj4BCu4xGFegUrPgi)). No accessible source records where the "not a thesis" instruction came from. It most likely came from supervisor feedback in the three inaccessible chats.

## Nine decisions the user must settle before any agent runs

The research notes leave several choices open that an agent cannot make honestly by itself. The table lists each one, why it matters, and a recommended default. The default is used only if the user approves it and records it in `DECISIONS.md`.

| # | Open decision | Why it blocks work | Recommended default (needs your approval) |
|---|---|---|---|
| D1 | **Thesis vs project.** The proposal, deck and dataset page all say MSc thesis, with a dataset paper and a benchmark paper. You say "not a thesis". | It sets scope, the deliverable list, and whether papers and the dashboard are in or out. | A non-thesis project: results pack plus reproducible repo. Papers, Zenodo and the dashboard become optional extensions, not acceptance criteria. Confirm against your department's rubric. No Bangladeshi non-thesis guideline was found online ([methods notes](https://www.csus.edu/college/engineering-computer-science/computer-science/_internal/_documents/ai-ml-ds-ms-projects-guideline.pdf)). |
| D2 | **Author name.** Every artifact and doc names "Romjan Chowdhury". Your account memory describes it as your own master's project. | Names go into figures, the data card, citations and any release. | The agent writes `author: TO_CONFIRM` everywhere and refuses to put any name into an output until you fill it in. |
| D3 | **WFP and AgriPriceBD.** Both are named in the project description, but neither is among the 32 files. AgriPriceBD is a prior-work paper (arXiv 2604.06227), not a dataset in hand. WFP appears only as a planned cross-check ([DATA_CARD](project://DATA_CARD.md)). | The agent must not pretend it used them. | Treat AgriPriceBD as a literature benchmark only. Make the WFP/HDX monthly Dhaka cross-check an optional stage that stays blocked until you supply the file. Fix the project description to match. |
| D4 | **Threshold for "abnormal".** None exists: no interval level, quantile or minimum % move ([project context](https://claude.ai/artifact/7Ud96n6HY5rVPLn57zM4Nh)). | Alert results depend entirely on it. Picking it after seeing the shock results is p-hacking. | Pre-register two rules. (a) Conformal 95% upper-bound exceedance with a persistence rule of 3 of 5 report days. (b) An ALPS-style robust z ladder of stress ≥1, alert ≥2, crisis ≥3 ([WFP ALPS](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)). Choose the operating point from the false-alarm rate on non-event periods, never from the test events. |
| D5 | **Attribution method.** The method for "driver contributions plus a residual" is not chosen. | It sets the RQ4 result and its wording. | A nested-model ladder M0 (price and calendar) ⊂ M1 (+ world price × FX, fuel) ⊂ M2 (+ policy and events), with TreeSHAP on LightGBM as a secondary per-date view. |
| D6 | **Horizon unit.** It is not stated whether h=1/7/14/30 means report days or calendar days. The DATA_CARD forbids silent forward-filling. | Lead times in days and false alarms per item-year depend on it. | Report days, as in the existing `step` column. Convert lead times to calendar days for reporting with the recorded date gaps. |
| D7 | **Priority item set** for drivers, alerts and attribution. | A non-thesis project usually covers about 10–20 items ([methods notes](https://www.csus.edu/college/engineering-computer-science/computer-science/_internal/_documents/ai-ml-ds-ms-projects-guideline.pdf)). Most series have no shock label. | Benchmark all 54 long-history series (cheap). Do drivers, alerts and attribution on about 16 items: those with in-window shocks or a clear import-parity driver (see the outline). |
| D8 | **Alert evaluation window.** The benchmark test window (Jan 2025–Oct 2026) holds only about 3 of the 12 in-window shocks (S15 tail, S21, S22). | Scoring alerts only there would leave almost no labels. | Run alert origins from mid-2023 onward, expanding window, with history before 2022 kept as training. Report coverage per period. Accept that 2023 origins have little training history and say so. |
| D9 | **Missing driver and event inputs.** GloFAS rivers, India retail prices, BB macro before 2024 and hartal days for 2021–22 are missing ([SOURCES](project://SOURCES_2026-10-26.md)). The **Sep 2023 price caps**, a named RQ4 event study, appear in none of the event files. | RQ2 and RQ4 scope. | Run without them, and record "rivers excluded" as a limitation unless you run `pl.download_rivers(ROOT, force=True)` in Colab. The agent must ask before adding the Sep 2023 cap dates, and must cite a source when it does. |

Other items stay open but do not block the start: the TCB licence (CC BY 4.0 pending a no-objection), the novelty check against the 2026 Mendeley "Food Commodity Price (OHLC) Dataset of Bangladesh", confirming the "reconstructed" event dates, and the department's real deadlines. The deck itself says its dates "move to match the department's thesis deadlines" ([Deck](https://claude.ai/artifact/NUnU3Rj4BCu4xGFegUrPgi)).

## Final project outline: four questions, seven phases, one results pack

### Re-scoped questions for a project, not a thesis

The proposal's main question asks whether external drivers and pretrained foundation models forecast Dhaka daily retail prices better than naive, and whether their forecasts detect documented shocks early ([Proposal](https://claude.ai/artifact/7Ud96n6HY5rVPLn57zM4Nh)). For a non-thesis project, each question is narrowed to something a finished experiment can answer. The novelty claim is kept modest: an applied system evaluated against credible baselines with statistical evidence, which is what applied MS project guidelines ask for ([CSUS guideline](https://www.csus.edu/college/engineering-computer-science/computer-science/_internal/_documents/ai-ml-ds-ms-projects-guideline.pdf)). The cuts are deliberate. TimesFM and other extra foundation models are optional. Deep learning trained from scratch is cut, as the deck already planned. The papers and the dashboard leave the critical path.

| RQ | Re-scoped question | Experiment | What counts as an answer |
|---|---|---|---|
| RQ1 Benchmark | On the 54 long-history TCB series, does any model (7 classical, LightGBM, Chronos-2) beat naive at h=1/7/14/30 report days, and in which strata? | Rolling-origin test Jan 2025–Oct 2026, MASE and relMAE vs naive, DM-HLN with Holm | Per-stratum tables with better/worse counts. "No model beats naive" is a valid finding. |
| RQ2 Drivers | For the priority items, do drivers improve LightGBM and Chronos-2 over price-only, and which driver groups matter? | With/without drivers, plus a leave-one-group-out ablation (FX, world prices, fuel, calendar, weather, policy/trade, disruptions, macro) | ΔrelMAE and Δinterval score with bootstrap CIs per driver group |
| RQ3 Alerts | Do forecast-interval alerts flag the 12 in-window shocks before the news peak, at what false-alarm rate, compared with ALPS- and IFPA-style rules? | Pre-registered thresholds (D4), event window [onset−14d, peak+30d], persistence rule | Per-event detected/missed, lead days, false alarms per item-year, PR curve, Kupiec coverage test |
| RQ4 Explanation | For priority-item rises, how much is accounted for by measured cost drivers, and which rises stay unexplained? | M0⊂M1⊂M2 ladder, SHAP cross-check, three event studies (India Dec 2023 onion ban, 2024–25 FX moves, Sep 2023 caps if dated per D9) | Share explained per episode plus a neutral residual label, with sign agreement against the pass-through literature |

The methods follow established practice. WFP ALPS fits a trend plus month dummies and reads standardised positive residuals at 0.25/1/2 σ ([WFP ALPS](https://documents.wfp.org/stellent/groups/public/documents/manual_guide_proced/wfp264186.pdf)). FAO's IFPA standardises compound growth rates within each calendar month, with thresholds at 0.5 and 1 ([SDG 2.c.1](https://worldbank.github.io/sdg-metadata/metadata/en/2-c-1)). IFPRI's NEXQ flags returns above a 95% conditional quantile and backtests the exceedance count against a binomial expectation ([Martins-Filho et al.](https://ssa.foodsecurityportal.org/sites/default/files/2020-09/Martins-FilhoToreroYao2010.pdf)). ALPS admits look-ahead bias because its trend uses the full sample. That is the project's opening: a **driver-conditioned, strictly real-time expected price** with conformal intervals. Adaptive conformal inference keeps coverage valid under distribution shift ([Zaffran et al.](https://arxiv.org/pdf/2202.07282)). For RQ4 the Bangladesh evidence gives sign checks. Dhaka rice is cointegrated with India import parity at an elasticity of about 0.99 ([Dorosh & Rashid](https://cgspace.cgiar.org/server/api/core/bitstreams/ffd095df-831c-4530-a191-930b5c49fa30/content)). Rice adjusts slowly, taking about 8 months to return to equilibrium ([Hoque et al.](https://www.bb.org.bd/bbta_portal/assets/bbta_journal/articles/Price%20Transmission%20Dynamics%20in%20the%20Rice%20Market%20of%20Bangladesh.pdf)). Oil-to-food pass-through is small and slow, with a long-run elasticity of 0.199 ([Alauddin et al.](https://bids.org.bd/uploads/publication/BDS/45/4_Oil-and-Food-Prices.pdf)). A five-year daily panel cannot identify slow long-run channels well. The write-up should say so, not overclaim.

### Phases, deliverables and acceptance

| Phase | Stages | Deliverable | Done when |
|---|---|---|---|
| P0 Setup and decisions | S00 | Repo on Drive, raw-file manifest, `DECISIONS.md`, environment lock | All 32 raw files hashed. D1–D9 answered or marked pending. `make check` passes. |
| P1 Data freeze and audit | S01 rebuild panel, S02 audit | `tcb_v1.0_rebuilt.parquet` plus checksum, data-quality table, audit error rate | Panel invariants pass. Proposed corrections approved. Audit is either done by a human or marked blocked. |
| P2 Driver panel | S03 | As-of-aligned feature store with lags and confidence flags, item-to-driver map | The leakage test passes. Coverage table produced. FX splice checked. |
| P3 Benchmark | S04 reproduce baseline, S05 LightGBM + Chronos-2 ± drivers | Benchmark tables and ablation | The existing baseline is reproduced or its differences are documented. Full grid complete. |
| P4 Intervals and alerts | S06 | Calibrated intervals, alert log, event scorecard | Thresholds were pre-registered before scoring. All 12 events reported, misses included. |
| P5 Explanation | S07 | Explained-vs-unexplained breakdown and event studies | Ladder shares per episode. Neutral wording audit passes. |
| P6 Robustness and reproducibility | S08, S09 | Robustness table, clean re-run diff, results pack | A clean re-run reproduces key tables exactly. `RESULTS_REGISTER.md` is complete. |
| Optional | S10 dashboard, S11 WFP cross-check, S12 extra foundation models | Static page, cross-check note | Only with explicit approval. The dashboard is externally visible. |
| Review | S99 | Independent spec review | Every SPEC requirement is checked by a reviewer that did not build it. |

If the deck's dates still hold, P0–P1 fit November 2026, P2–P3 December–January, P4 February, P5 March, and P6 early April. The user's report writing then starts from the results pack. These dates are the deck's proposals, not commitments ([Deck](https://claude.ai/artifact/NUnU3Rj4BCu4xGFegUrPgi)).

The proposed priority set for D7 has 16 items. It includes every in-window shock product: sugar, egg, local and imported onion, potato, coarse and medium rice, and bottled and loose soybean oil. Green chilli has a shock (S22) but is short-history from February 2026, so it is scored for alerts only. The set adds items with a clean world-price or import-parity driver: loose atta, loose palm oil, large lentil, chickpea, and imported garlic. Imported onion needs care. It is the only series where any model beat naive, and it has had no price since 2026-02-10 because of an import curb, so that result may be fragile ([item_meta.csv](https://claude.ai/artifact/394Xrk4k7LvgWcKwQePwNS)).

### Figures and tables the results pack must produce

Each item below is a file under `reports/` produced by a committed stage and listed in `RESULTS_REGISTER.md`. The register maps each number to its file, command and commit, and the later report is written from it.

| ID | Table or figure | Source stage | Feeds report section |
|---|---|---|---|
| T1 | Dataset summary by stratum (series, report days, % unchanged, % missing) | S01 | Data |
| T2 | Data-quality ledger: corrections applied, corrections proposed, audit error rate with Wilson 95% CI | S01–S02 | Data validation |
| T3 | Driver inventory: source, frequency, publication lag, coverage, confidence | S03 | Data / methods |
| T4 | Benchmark: gmean relMAE, median MASE, win rate, DM better/worse by stratum × model × horizon | S04–S05 | RQ1 |
| T5 | Driver ablation: ΔrelMAE and Δinterval score per driver group, bootstrap CI | S05 | RQ2 |
| T6 | Interval calibration: empirical coverage, pinball, Winkler, Kupiec p-value | S06 | RQ3 |
| T7 | Event scorecard: each of the 12 shocks with confidence, detected or not, lead days, rule | S06 | RQ3 |
| T8 | False alarms per item-year by stratum and rule, alongside ALPS/IFPA baselines | S06 | RQ3 |
| T9 | Explanation ladder per episode: share by M1, M2, residual | S07 | RQ4 |
| T10 | Event-study estimates (onion ban, FX moves, caps if dated) | S07 | RQ4 |
| T11 | Robustness: weekly vs daily, min/max/mid, sliding window, placebo dates, leave-one-event-out | S08 | Discussion |
| F1 | Indexed staples (May 2021 = 100) with the 2022 gap shaded | S01 | Data |
| F2 | Reporting calendar heatmap (gaps, Eid closures, 2022) | S01 | Data |
| F3 | relMAE vs horizon by stratum | S05 | RQ1 |
| F4 | Ablation bars per driver group | S05 | RQ2 |
| F5 | Coverage calibration plot (nominal vs empirical) | S06 | RQ3 |
| F6 | Alert timelines per shock: price, band, flags, onset and peak markers | S06 | RQ3 |
| F7 | Precision–recall over thresholds, with the pre-registered point marked | S06 | RQ3 |
| F8 | Stacked explained-vs-unexplained decomposition for 3–4 case studies (onion Dec 2023, soybean oil Oct 2024, potato 2024, rice 2023–25) | S07 | RQ4 |
| F9 | Global SHAP importance by stratum | S07 | RQ4 |

The later report can follow the structure the methods notes recommend for a non-thesis project: introduction and questions; related work (ALPS, IFPA, NEXQ, Bangladesh pass-through, CPD); data (data card, corrections, audit, lags); methods; evaluation; case studies; limitations and ethics (residuals are not collusion, TCB measurement error, Dhaka-only retail); and a reproducibility appendix ([methods notes](https://www.csus.edu/college/engineering-computer-science/computer-science/_internal/_documents/ai-ml-ds-ms-projects-guideline.pdf)). Every section maps to rows above, so writing becomes assembly rather than analysis.

## Twenty-four data traps the agent must handle explicitly

Profiling the 32 project files showed a structurally clean core panel: no duplicate item-date keys, Avg = (Min+Max)/2 everywhere, and 1.42% missing prices. The driver files, though, carry formatting traps, and **at least one data error is still uncorrected**. Profiling also found that the Comtrade blanking described in SOURCES was never applied to the attached file ([project files](project://files); [SOURCES](project://SOURCES_2026-10-26.md)). These go into the instruction set as rules, because an agent that "cleans" them silently will corrupt results.

| # | Known issue (file) | Rule for the agent |
|---|---|---|
| 1 | Time index is report days, not calendar days. Gaps run 1–115 days. | Model on report days. Never forward-fill to calendar days unless the stage says so and the deviation is logged. |
| 2 | 2022 sparse period: only 24 reports from 12 Mar to 31 Dec 2022. | Set `gap_2022` for 2022-03-12..2022-12-31. Use as history only, never inside an evaluation window. |
| 3 | The CSV lacks the derived columns (item_id, report_idx, days_since_prev_report, gap_2022, is_reported, spread_rel, reports_since_change, Source_File). `tcb_v1.0.parquet` and `tcb_convert.py` are not attached. | Rebuild item_id as `Product + " | " + Unit` (it must reproduce all 63 item_meta ids). Rebuild the other columns. Name the output `_rebuilt`, never the original v1.0. |
| 4 | **Palm Olein - Bottled 2 L on 2025-04-18 holds the 5 L price (840/845/842.5).** corrections.csv blanked only the 5 L row. | Write it to `corrections_proposed.csv`. Do not change the panel until the user approves. Both palm olein series are unusable (3–4 values) and stay excluded. |
| 5 | Two rows have Min but no Max, and Avg = Min (2021-05-31 broiler and sugar). | Keep them, flag them, and exempt them from the Avg = midpoint invariant. |
| 6 | Five one-day ±26–35% reversals in local ginger in 2021 (audit_candidates.csv). They look like new-crop vs old-crop quotes. | Do not drop them. Resolve them in S02 against the originals, or leave them flagged and run robustness with and without. |
| 7 | The audit sample (1,530 values, 28 days) has no "checked" column. The original TCB files are not attached. | S02 is human-in-the-loop. Without the originals it is **blocked**. Never report an error rate that was not measured. |
| 8 | item_meta dates are DD-MM-YY ("17-05-21"). | Parse with `%d-%m-%y`. Prefer the ISO dates in the xlsx Series sheet. |
| 9 | The xlsx duplicates the CSV, with Wide and Series sheets. | Load the CSV once. Never double-count the xlsx. |
| 10 | Pack sizes are mixed (1/2/5 L, hali = 4, dista = 24 sheets, metric ton). | Normalise to Tk per kg, litre or piece before any cross-pack comparison. Keep the original values too. |
| 11 | Late starters that are not flagged short_history: Soybean Oil 2 L (from 2024-09-03), Rice Bran Oil 5 L (from 2024-05-20). | Respect item_meta eval_stratum. Report the late starts in T1. |
| 12 | Imported onion has no price for about 480 days (curb, last 2026-02-10). Hilsa is missing during most October bans but was reported during the 2023 ban. | Missing means not reported. Never impute in evaluation. |
| 13 | Comtrade months from 2026-05 onward are **not blanked**, contrary to SOURCES. HS codes are stored as ints (0402 → 402). HS 703 and 910 mix onion+garlic and ginger+turmeric. | Blank periods ≥ 202605. Zero-pad HS codes to 4 digits. Never attribute 703 or 910 to a single item. |
| 14 | IMF CSV has 4 header rows, "1980M1" periods, a duplicated POILAPSP column and 7 code-less columns. PTOMATO and PAPPLE use 0 to mean missing. PCHANA is USD per 100 kg. | Use a dedicated parser. Check units against the description row. |
| 15 | The FAO file has a one-line title. Recent months get revised. | Read with `skiprows=1`. Record the fetch date. |
| 16 | The weather CSV has two blocks (metadata, then data). Locations are unnamed. The last day (2026-10-20) is incomplete. | Split the blocks. Map location IDs by coordinates, as an inference to confirm. Drop the last day. Apply the 5-day lag. |
| 17 | Yahoo BDT is stale since Sep 2026 and runs about Tk 1.6 below BB. The spliced `bdt_per_usd` is not attached. | Build the splice: npm from 2024-03-02, Yahoo × 1.0151 before. Cross-check against the remittance-implied rate. Keep both raw series. |
| 18 | BDT jumps +6.3% on 2024-05-10 (crawling peg). WTI is −36.98 on 2020-04-20. | These are real values. Do not winsorise them. Avoid logs on WTI (use Brent). |
| 19 | Three event files start with a UTF-8 BOM. | Read with `encoding="utf-8-sig"`. |
| 20 | Event confidence is verified, reconstructed or computed. exporter_policy_events is 100% reconstructed. All jatka bans are reconstructed. | Carry confidence as a feature or weight. Report results by confidence. |
| 21 | Event tables cover short spans: duty changes only Feb–Nov 2024, disruptions only Oct 2023–Nov 2025. | Mark out-of-coverage periods as unknown, not as zero. Log this as a limitation. |
| 22 | shock_events joins on **Product**, not item_id (bottled soybean oil = 3 item_ids). BD-S15's news_peak (2025-06-10) falls after its end date (2025-01-31). | Join on Product. Raise S15 as a data question. Do not silently reorder its dates. |
| 23 | Shock magnitudes use mixed units (eggs per dozen vs TCB per hali, maund, wholesale). | Never compare the magnitudes numerically without converting. Treat them as text. |
| 24 | bd_import_figures is not a time series (overlapping periods, mixed flow types). BB remittance and reserves start only in 2024. | Use them as qualitative context only. Keep macro drivers out of models that need history before 2024, or log the restriction. |

The baseline file also has undocumented semantics. The training window, refit frequency, origin spacing and MASE scaling are not recorded, and "better/worse" are inferred to be significance counts ([baseline results](https://claude.ai/artifact/394Xrk4k7LvgWcKwQePwNS)). So S04 has to **reproduce before extending**. If its numbers differ, both versions are kept and the difference is explained. The committed file is never overwritten.

## The instruction set: files that let an agent resume rather than restart

The design copies what Anthropic found works for multi-session agents. An initializer session writes scaffolding: a JSON feature list that later sessions may only flip, a progress log, an init script and a first commit. Every later session "gets its bearings" from files and git, runs a basic end-to-end check before new work, does one unit, verifies it, commits, and logs it ([Anthropic harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). Anthropic's prompting guide adds three rules: JSON for state, plain text for notes, and git as the restorable checkpoint. It also says a fresh context window often beats compaction because the model can "discover state from the local filesystem" ([Claude docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)). Claude Code's `/rewind` checkpoints do not cover files modified through Bash. Pipeline scripts write data through Python, so **git plus per-unit done-markers on Drive are the only reliable checkpoint** ([Claude Code](https://code.claude.com/docs/en/best-practices)).

Colab adds a specific failure: a dropped runtime loses everything except what is on the mounted Drive. That fits the user's existing habit of keeping all data in one Drive folder ([project memory](memory:///areas/bangladesh-food-price-watch.md)). The protocol therefore checkpoints below the stage level. Every benchmark (model × origin) and every alert (item × origin) is a separate unit with its own atomic file and `_SUCCESS.json` marker. A drop costs at most one unit, not a stage. Engines like DVC and Snakemake follow the same principle: DVC skips stages whose commands, dependencies and parameters are unchanged, and Snakemake re-runs only outputs it marks incomplete ([DVC](https://doc.dvc.org/user-guide/pipelines/running-pipelines); [Snakemake](https://linuxmanpag.es/man/1/snakemake/)).

The honesty rules address a documented failure mode. An audit of 30 long-horizon LLM research runs found that agents "quietly reduced datasets or training budgets" and swapped failed components for oracle functions while still producing plausible metrics ([Yu et al.](https://tldr.takara.ai/p/2608.26753)). The countermeasures are a frozen spec, runnable checks, a provenance rule for every number, a deviation log, and an independent reviewer that "isn't swayed by the reasoning that produced the code" ([Claude Code](https://code.claude.com/docs/en/best-practices)). Guidance on emphasis is consistent: piling on capitals makes models over-apply rules, so hard limits belong in hooks or deny rules where the tool supports them ([Claude Code](https://code.claude.com/docs/en/best-practices)). The files below use plain statements and pair the important ones with runnable checks.

Seven files make up the set: a setup prompt (session 0), `AGENTS.md` (with a one-line `CLAUDE.md`), `SPEC.md`, `state/stages.json`, `PROGRESS.md` / `DEVIATIONS.md` / `DECISIONS.md` templates, `config.yaml`, and a checkpoint helper. A resume prompt, per-session prompts and a reviewer prompt follow. Paths assume a Drive root of `/content/drive/MyDrive/FoodPriceWatch`. Change the root once in `config.yaml`.

### 1. Master setup prompt (paste into session 0 only)

```text
You are setting up the "Bangladesh Food Price Watch" master's PROJECT (not a thesis) so that an AI agent can run it end to end over many sessions, and resume after any network or runtime drop without redoing finished work. This is the setup session only: do not run any modelling.

Context (read, do not assume beyond it):
- Goal: forecast Dhaka TCB daily retail prices 1/7/14/30 report-days ahead, raise early alerts when a price leaves its expected range, and split rises into a part explained by measured cost drivers and a neutral "not explained by measured cost drivers" residual. Never describe residuals as hoarding, syndicates or collusion.
- Inputs: the 32 project files (TCB panel CSV/xlsx, item_meta, corrections, audit files, baseline_results_by_group, shock tables, FX, oil, IMF, FAO, Comtrade, BB macro, weather, calendar and event tables) plus DATA_CARD.md and SOURCES_2026-10-26.md.
- A first benchmark exists (baseline_results_by_group.csv): no classical model beats naive. Treat it as a prior result to reproduce, never to overwrite.

Do these steps, in order, and stop after step 9:
1. Run `pwd`. Work only inside the project root defined in config.yaml (default /content/drive/MyDrive/FoodPriceWatch). Mount Drive if needed.
2. Create the layout: data/raw/, data/interim/, data/processed/, outputs/, reports/{tables,figures}/, state/, src/fpw/, src/stages/, tests/, logs/.
3. Copy the 32 input files and the two docs into data/raw/ unchanged. Write data/raw/MANIFEST.csv (filename, source, retrieved_at if known, bytes, sha256). Never edit files in data/raw/ after this.
4. Write AGENTS.md, CLAUDE.md, SPEC.md, state/stages.json, PROGRESS.md, DEVIATIONS.md, DECISIONS.md and config.yaml exactly from the templates I give you, filling only the placeholders.
5. Write src/fpw/checkpoint.py (atomic writes, done-markers, skip-if-done) from the template, and a `make check` target (or `python -m fpw.check`) that validates stages.json against disk and runs tests/.
6. Pin the environment (requirements.lock with exact versions) and set the global seed in config.yaml.
7. `git init` in the project root; .gitignore data/ and outputs/ large files (commit their hashes, not the data); commit "S00: scaffold [checks pass]".
8. Ask me each open decision D1-D9 listed in DECISIONS.md, one message with all of them, and record my answers verbatim. Mark any I do not answer as PENDING. Do not choose for me.
9. Run `make check`, append a PROGRESS.md entry, set S00 to done in stages.json only if checks pass, commit, and report using the session-end format in AGENTS.md.
```

### 2. AGENTS.md (keep it short; Claude Code reads it through CLAUDE.md)

```markdown
# AGENTS.md — Bangladesh Food Price Watch

## What this is
A master's PROJECT (not a thesis). The agent produces verified results; the human writes the report later from reports/ and RESULTS_REGISTER.md. Scope and "done" live in SPEC.md. Machine state lives in state/stages.json. Narrative state lives in PROGRESS.md.

## Commands
- Check everything: `make check`   (validates stages.json vs disk markers, runs tests/)
- Run one stage:     `make stage S=NN`  (idempotent; skips finished units)
- Dry run:           `make stage S=NN DRY=1`

## Startup ritual (every session, before any new work)
1. `pwd`; confirm the Drive root from config.yaml is mounted. Work only inside it.
2. Read, in order: this file, SPEC.md, DECISIONS.md, the last 2 entries of PROGRESS.md, DEVIATIONS.md, state/stages.json, then `git log --oneline -20` and `git status`.
3. Delete any *.tmp files under outputs/ (leftovers from a dropped session).
4. Run `make check`. For every stage marked done, it re-hashes outputs against the stage's _SUCCESS.json. If a check fails, set that stage to pending, log why in PROGRESS.md, and do not continue past it.
5. A stage left "in_progress" is not trusted: keep only units that have a valid _SUCCESS.json, and resume at the next unit.
6. Pick the first stage whose status is not done and whose depends_on are all done. If its inputs depend on a PENDING decision, stop and ask.
7. Work on that one stage only.

## End-of-unit / end-of-stage ritual
- After each unit: atomic write, write its _SUCCESS.json marker. Commit at least every 30 minutes of work or every 20 units, whichever comes first.
- After the stage: run its acceptance checks from SPEC.md → update stages.json (status, output_sha256, git_commit, finished_at) → append PROGRESS.md → commit "SNN: <summary> [checks pass]". Then stop and report.

## Rules that do not bend
- Never edit data/raw/. Corrections go through corrections_proposed.csv and need my approval.
- Never fabricate, simulate or impute data unless SPEC.md says that stage does so. If a source is missing, unreachable or malformed, mark the stage blocked with the reason. Do not substitute another source silently.
- Every number in reports/ must be produced by a committed script from files in data/ and listed in reports/RESULTS_REGISTER.md (value, file, command, commit). If you did not run it, say so.
- Never overwrite data/raw/baseline_results_by_group.csv or any earlier result; write new versions alongside.
- Any change to sample, items, dates, horizon, method, threshold or source goes into DEVIATIONS.md with the reason before you continue. Changes to SPEC.md scope require asking me first.
- Thresholds for alerts are fixed in config.yaml before any test-period event scoring. Never tune them on the 12 shock episodes.
- Wording: rises not explained by the model are "not explained by measured cost drivers". Never "hoarding", "syndicate", "collusion" or "manipulation" in outputs.
- Author name: use config.yaml author. If it is TO_CONFIRM, put no name in any output.
- Do not delete, edit or reorder entries in stages.json; only update their status fields.
- Ask before anything destructive or externally visible: rm -rf, git reset --hard, force-push, publishing to GitHub/Zenodo/arXiv, running the dashboard publicly, using any API key.

## Stop and ask when
- A decision in DECISIONS.md that this stage needs is PENDING.
- Credentials, an API key, original TCB files or a licence answer are needed.
- An acceptance check fails twice after honest fixes.
- A result strongly contradicts expectations (report it; do not tune until it fits).
- Reproduction of the existing baseline differs beyond tolerance.
- You find a data error not listed in SPEC.md §Data rules.

## Session-end report format
Done (with the check command and result) · Not done · Blocked (why, what you need from me) · Deviations logged · Numbers I am unsure of · Next stage.
```

```markdown
<!-- CLAUDE.md -->
@AGENTS.md
```

The `@AGENTS.md` import line for Claude Code comes from the researcher's own knowledge and was not verified in the research session ([agent notes](https://www.agents.md)). If your tool does not support imports, paste AGENTS.md into CLAUDE.md. The AGENTS.md convention is supported by Codex, Cursor, Gemini CLI, Copilot and others ([agents.md](https://www.agents.md)).

### 3. SPEC.md with per-stage acceptance criteria

```markdown
# SPEC.md — Bangladesh Food Price Watch (project, not thesis)

## Goal
Forecast Dhaka TCB daily retail prices h = 1, 7, 14, 30 report-days ahead; raise alerts when a price leaves its expected range; decompose rises into "explained by measured cost drivers" and "not explained by measured cost drivers". Output: a reproducible repo and a results pack (reports/) from which the author writes the report later.

## Research questions (re-scoped)
RQ1 Benchmark: on the 54 long-history series, does any model (Naive, SeasonalNaive, WindowAverage, RWD, AutoARIMA, AutoETS, AutoTheta, LightGBM, Chronos-2) beat naive, per eval_stratum and horizon?
RQ2 Drivers: for the priority items (config.priority_items), do drivers improve LightGBM and Chronos-2 over price-only; which driver groups matter (leave-one-group-out)?
RQ3 Alerts: do interval-based alerts flag the 12 in-window shocks (BD-S09, S11, S12, S13, S14, S15, S16, S17, S19, S20, S21, S22) before news_peak, with how many false alarms per item-year, versus ALPS-style and IFPA-style rules?
RQ4 Explanation: for priority-item rises, what share do nested models M0 ⊂ M1 ⊂ M2 explain; what residual remains; event studies for India's Dec 2023 onion ban, 2024-25 FX moves, and the Sep 2023 price caps if DECISIONS D9 supplies dated, sourced cap events.

## Out of scope unless DECISIONS.md says otherwise
Dataset paper, benchmark paper, Zenodo release, public dashboard, TimesFM/other foundation models, deep learning trained from scratch, wholesale (DAM) prices, markets outside Dhaka.

## Evaluation protocol (fixed)
- Time index: report days. 2022-03-12..2022-12-31 (gap_2022) is history only, never in an evaluation window.
- RQ1/RQ2 test origins: same 87 starts as the existing baseline, Jan 2025 - Oct 2026 (S04 recovers their exact dates; if impossible, monthly origins in that span, logged in DEVIATIONS.md). Expanding window.
- RQ3 origins: daily one-step-ahead from config.alert_eval_start (default 2023-06-01) to end, expanding window, models refit at config.refit_every.
- Metrics: MAE in Tk, MASE (in-sample one-step naive scaling), gmean relMAE vs naive, win rate; pinball (0.9, 0.95), empirical coverage, Winkler score; DM test with HLN correction and Holm across items; event recall, lead days (report days and calendar days), false alarms per item-year, PR curve over thresholds; Kupiec unconditional coverage test on non-event periods.
- Drivers enter at publication date: monthly world prices +40 days after month end, Comtrade +75 days, weather +5 days, daily FX/oil as-of the last value at or before the report date.
- Event matching window: flag counts as a detection if within [onset - 14 days, news_peak + 30 days].

## Data rules (known issues; each must have a test in tests/)
1 report-day index, no silent forward-fill · 2 gap_2022 flag · 3 rebuild item_id = Product + " | " + Unit and derived columns; output named tcb_v1.0_rebuilt · 4 Palm Olein 2 L 2025-04-18 holds the 5 L price → corrections_proposed.csv, not applied without approval; palm olein 2 L/5 L excluded · 5 two Min-only rows (2021-05-31 broiler, sugar) flagged, exempt from midpoint invariant · 6 ginger 2021 reversals kept and flagged · 7 audit needs original TCB files; else blocked · 8 item_meta dates %d-%m-%y · 9 load CSV once, not xlsx too · 10 normalise pack sizes for cross-pack use · 11 respect eval_stratum (Soybean Oil 2 L, Rice Bran Oil 5 L start late) · 12 missing = not reported, no imputation in evaluation · 13 Comtrade: blank period ≥ 202605, zero-pad HS to 4 digits, never assign HS 703/910 to one item · 14 IMF: 4 header rows, YYYYMn periods, duplicate POILAPSP, unnamed columns, zeros = missing in PTOMATO/PAPPLE, PCHANA USD/100 kg · 15 FAO skiprows=1 · 16 weather: split 2 blocks, map location ids by coordinates (log as inference), drop 2026-10-20 · 17 bdt_per_usd = npm from 2024-03-02, Yahoo × 1.0151 before; keep raw series; cross-check vs remittance-implied rate · 18 keep BDT 2024-05-10 jump and WTI -36.98 (use Brent for logs) · 19 utf-8-sig for BOM files · 20 carry event confidence · 21 out-of-coverage event periods = unknown, not zero · 22 shock_events joins on Product; S15 peak-after-end raised as a question · 23 shock magnitudes are text, mixed units · 24 import_figures and pre-2024 macro are context only.

## Stages and acceptance criteria
S00 Scaffold — 32 raw files + 2 docs in MANIFEST with sha256; config.yaml, DECISIONS.md present; `make check` passes; first commit.
S01 Rebuild panel — 76,440 rows; 1,412 dates (2021-05-17..2026-10-24); 63 item_ids equal to item_meta; 0 duplicate (Date, item_id); Avg == (Min+Max)/2 except the 2 flagged rows; Min ≤ Max; Week_Ago_Min matches own Min 7 calendar days earlier on ≥ 99.5% of matchable rows; corrections.csv already reflected (MS Rod 70,500; Palm Olein 5 L 2025-04-18 missing); corrections_proposed.csv written; parquet + sha256; T1, F1, F2 produced.
S02 Audit (human-in-the-loop) — audit sheet prepared from audit_sample_2pct.csv and audit_candidates.csv; if originals are supplied and checked: error rate with Wilson 95% CI over 1,530 values, decision recorded for each of the 5 ginger candidates; else status blocked with reason. T2 produced either way (with "not measured" if blocked).
S03 Driver panel — every driver parsed by a dedicated reader with a unit test; config/item_driver_map.yaml written and shown to the user; leakage test passes (shifting any driver forward by one publication step changes no feature value at any date before that step); FX splice ratio reported and remittance cross-check within 1.5%; coverage table T3.
S04 Reproduce baseline — statsforecast models re-run under recorded settings (training window, refit, origins, season length 7, MASE scaling) documented in config; ALL-stratum gmean relMAE within ±0.02 of baseline_results_by_group.csv for every model × horizon, or differences explained in DEVIATIONS.md; original file untouched.
S05 Extended benchmark — LightGBM (global, item features; price-only and +drivers) and Chronos-2 (price-only; +covariates if the installed version supports it, else logged) on the same origins; unit = (model, variant, origin) with marker; complete grid; DM-HLN + Holm counts; ablation for priority items; T4, T5, F3, F4.
S06 Intervals and alerts — conformal (or quantile) intervals with empirical coverage per stratum; thresholds and persistence rule read from config and frozen in a pre-registration file committed before scoring; ALPS-style and IFPA-style baselines computed on the same data; all 12 events in T7 including misses and low-confidence ones; T6, T8, F5, F6, F7.
S07 Explanation — M0, M1, M2 fitted per priority item; share explained per episode; SHAP global and per-episode; sign check of FX and world-price contributions; wording check (grep outputs for banned words returns nothing); T9, T10, F8, F9.
S08 Robustness — weekly vs daily, Min/Max/Avg, sliding vs expanding window, placebo random event dates (flag rate near nominal), leave-one-event-out, results with ginger candidates excluded; T11.
S09 Results pack — clean re-run on a copy reproduces T4, T7, T9 exactly with the seed; RESULTS_REGISTER.md lists every number in reports/ with file, command, commit; reports/README.md indexes tables and figures by RQ.
S10-S12 Optional (dashboard, WFP cross-check, extra foundation models) — only if DECISIONS.md enables them.
S99 Review — a fresh reviewer session checks every line of this SPEC against the repo and lists pass/fail with evidence.
```

### 4. state/stages.json (the resume ledger)

```json
{
  "schema": "fpw-stages-v1",
  "rules": "Agents may change only status, started_at, last_unit, units_done, output_sha256, git_commit, finished_at, notes. Never delete or reorder entries.",
  "stages": [
    {"id": "S00", "title": "Scaffold", "depends_on": [], "outputs": ["data/raw/MANIFEST.csv"], "checks": ["make check"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S01", "title": "Rebuild TCB panel", "depends_on": ["S00"], "outputs": ["data/processed/tcb_v1.0_rebuilt.parquet", "data/processed/corrections_proposed.csv", "reports/tables/T1.csv"], "checks": ["pytest tests/test_s01_panel.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S02", "title": "Audit (human-in-the-loop)", "depends_on": ["S01"], "outputs": ["reports/tables/T2.csv"], "checks": ["pytest tests/test_s02_audit.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "blocked unless original TCB files are supplied"},
    {"id": "S03", "title": "Driver panel", "depends_on": ["S01"], "outputs": ["data/processed/features.parquet", "config/item_driver_map.yaml", "reports/tables/T3.csv"], "checks": ["pytest tests/test_s03_drivers.py tests/test_leakage.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S04", "title": "Reproduce baseline", "depends_on": ["S01"], "outputs": ["outputs/04_baseline/results_by_group_repro.csv"], "checks": ["pytest tests/test_s04_repro.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S05", "title": "Extended benchmark + ablation", "depends_on": ["S03", "S04"], "outputs": ["reports/tables/T4.csv", "reports/tables/T5.csv"], "checks": ["pytest tests/test_s05_grid.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "unit = model/variant/origin"},
    {"id": "S06", "title": "Intervals and alerts", "depends_on": ["S05"], "outputs": ["state/preregistration.yaml", "reports/tables/T6.csv", "reports/tables/T7.csv", "reports/tables/T8.csv"], "checks": ["pytest tests/test_s06_alerts.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "unit = item/origin"},
    {"id": "S07", "title": "Explanation ladder + event studies", "depends_on": ["S05", "S06"], "outputs": ["reports/tables/T9.csv", "reports/tables/T10.csv"], "checks": ["pytest tests/test_s07_explain.py tests/test_wording.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S08", "title": "Robustness", "depends_on": ["S06", "S07"], "outputs": ["reports/tables/T11.csv"], "checks": ["pytest tests/test_s08_robust.py"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S09", "title": "Results pack + clean re-run", "depends_on": ["S08"], "outputs": ["reports/RESULTS_REGISTER.md", "reports/README.md"], "checks": ["make rerun-diff"], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": ""},
    {"id": "S99", "title": "Independent review", "depends_on": ["S09"], "outputs": ["reports/REVIEW.md"], "checks": [], "status": "pending", "started_at": null, "last_unit": null, "units_done": 0, "output_sha256": {}, "git_commit": null, "finished_at": null, "notes": "run in a fresh session"}
  ]
}
```

Status values are `pending`, `in_progress`, `done` and `blocked`. JSON is used for state, rather than Markdown, because Anthropic found models were less likely to overwrite or rewrite it improperly ([Anthropic harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

### 5. PROGRESS.md, DEVIATIONS.md and DECISIONS.md templates

```markdown
<!-- PROGRESS.md — append-only; newest entry at the bottom -->
## 2026-MM-DD HH:MM — session N — stage SNN
- Resumed from: <stage/unit, or "fresh">; startup check result: <make check output summary>
- Did: <units completed, e.g. S05 LightGBM+drivers origins 31-58>
- Verified: <command> → <result>
- Open issues: <...>
- Next: <stage/unit>
```

```markdown
<!-- DEVIATIONS.md — one entry per change from SPEC.md, written BEFORE continuing -->
| date | stage | what changed (sample/items/dates/method/threshold/source) | reason | approved by user? |
|---|---|---|---|---|
```

```markdown
<!-- DECISIONS.md — the agent records the user's answers verbatim; PENDING blocks dependent stages -->
D1 Framing (project vs thesis; papers/Zenodo/dashboard in or out): PENDING
D2 Author name for all outputs: PENDING   (documents currently say "Romjan Chowdhury")
D3 WFP/HDX file supplied? AgriPriceBD as literature only?: PENDING
D4 Abnormal-rise rule and operating point (default: conformal 95% upper bound, 3-of-5 persistence; ALPS-style z 1/2/3 reported alongside; operating point by false-alarm rate on non-event periods): PENDING
D5 Attribution method (default: M0⊂M1⊂M2 ladder + TreeSHAP): PENDING
D6 Horizon unit (default: report days): PENDING
D7 Priority items (default 16: sugar, egg, onion local, onion imported, potato, rice coarse, rice medium, soybean oil bottled 1 L, soybean oil loose, atta loose, palm oil loose, lentil large, chickpea, garlic imported; green chilli alerts-only): PENDING
D8 Alert evaluation start (default 2023-06-01): PENDING
D9 Missing inputs: run GloFAS download? Sep 2023 price-cap dates and source?: PENDING
Other: licence/TCB no-objection; Mendeley OHLC novelty check; reconstructed event dates; department deadlines: PENDING
```

The default list for D7 names 14 items plus green chilli for alerts only. It counts the bottled-oil family as one shock product. Edit the list to the exact item_ids you want, from `item_meta.csv`.

### 6. config.yaml skeleton

```yaml
project_root: /content/drive/MyDrive/FoodPriceWatch
author: TO_CONFIRM            # D2 — no name appears in outputs until set
seed: 20261029
time_index: report_day        # D6
gap_2022: ["2022-03-12", "2022-12-31"]
horizons: [1, 7, 14, 30]
benchmark_origins: recover_from_baseline   # else monthly Jan 2025 - Oct 2026 (log deviation)
alert_eval_start: "2023-06-01"             # D8
refit_every: 30               # report days; record actual in markers
publication_lags_days: {monthly_world: 40, comtrade: 75, weather: 5}
comtrade_blank_from: 202605
fx_splice: {npm_from: "2024-03-02", yahoo_scale: 1.0151}
priority_items: []            # D7 — exact item_ids
alerts:                       # D4 — frozen into state/preregistration.yaml before scoring
  rule: conformal_upper
  level: 0.95
  persistence: {k: 3, m: 5}
  z_bands: {stress: 1, alert: 2, crisis: 3}
  event_window_days: {before_onset: 14, after_peak: 30}
explanation: {ladder: [M0_calendar, M1_cost, M2_policy_events], shap: true}   # D5
banned_words: [hoarding, syndicate, collusion, manipulation, cartel]
optional: {dashboard: false, wfp_crosscheck: false, extra_foundation_models: false}
```

### 7. Checkpoint helper (src/fpw/checkpoint.py)

```python
"""Atomic writes + per-unit done-markers so a dropped session resumes, not restarts."""
import hashlib, json, os, subprocess, time
from pathlib import Path

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def atomic_write_parquet(df, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)          # never leaves a half file that looks complete

def marker_path(out: Path) -> Path:
    return out.parent / (out.name + "._SUCCESS.json")

def is_done(out: Path) -> bool:
    m = marker_path(out)
    if not (out.exists() and m.exists()):
        return False
    return json.loads(m.read_text()).get("sha256") == sha256(out)

def mark_done(out: Path, *, inputs: dict, config_hash: str, seed: int, rows: int):
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    payload = {"output": str(out), "sha256": sha256(out), "inputs": inputs, "config_hash": config_hash,
               "seed": seed, "rows": rows, "code_commit": commit, "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
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
```

Use the same pattern for any download. Fetch to a per-file cache and skip a file if it exists and its hash matches, so a re-run fetches only what is missing ([agent notes](https://doc.dvc.org/user-guide/pipelines/running-pipelines)). If the user's existing Colab module `pl` already has download functions (`pl.download_rivers`, `pl.download_global`) ([SOURCES](project://SOURCES_2026-10-26.md)), the agent should open and reuse them rather than rewrite them.

### 8. Resume prompt (paste at the start of every session after S00, including after any drop)

```text
Resume the Bangladesh Food Price Watch project. Follow the startup ritual in AGENTS.md exactly: mount Drive, read AGENTS.md, SPEC.md, DECISIONS.md, the last two PROGRESS.md entries, DEVIATIONS.md, state/stages.json and the git log; delete *.tmp leftovers; run `make check` and re-verify every done stage's markers. Do not redo any unit with a valid _SUCCESS.json. Continue at the first unfinished unit of the first stage whose dependencies are done. Work on that one stage only. Commit at least every 20 units. When the stage's SPEC.md acceptance checks pass, update stages.json, append PROGRESS.md, commit "SNN: ... [checks pass]", and stop with the session-end report. If a needed decision is PENDING or a stop-and-ask condition occurs, stop and ask instead.
```

### 9. Suggested per-session prompts (append to the resume prompt)

```text
S01: "This session: S01 Rebuild panel. Pay particular attention to data rules 3, 4 and 5. Write corrections_proposed.csv for the Palm Olein 2 L 2025-04-18 row and show it to me; do not apply it."
S02: "This session: S02 Audit. Prepare reports/audit/audit_sheet.xlsx (one row per sampled value, columns for the original value and a checked flag). If I have not supplied the original TCB files, mark S02 blocked and move on only to stages that do not depend on it."
S03: "This session: S03 Driver panel. Show me config/item_driver_map.yaml before building features. Report the FX splice ratio and the remittance cross-check. Do not add any event (e.g. Sep 2023 price caps) without a cited source and my approval."
S04: "This session: S04 Reproduce the existing baseline. First recover or document training window, refit cadence, origin dates, season length and MASE scaling. If you cannot match within ±0.02, stop and show me the diff."
S05: "This session: S05 Extended benchmark. Units are (model, variant, origin); check markers before computing. If Chronos-2 covariate support is unavailable in the installed version, run price-only and log it in DEVIATIONS.md. If GPU time runs out, stop cleanly at a unit boundary."
S06: "This session: S06 Intervals and alerts. First write and commit state/preregistration.yaml from config.alerts, then score. Report all 12 in-window events, misses included, with their confidence ratings."
S07: "This session: S07 Explanation. Use the neutral residual label only; tests/test_wording.py must pass. Flag any episode where FX or world-price contributions have the wrong sign."
S08: "This session: S08 Robustness, including placebo dates and leave-one-event-out."
S09: "This session: S09 Results pack. Do a clean re-run on a copy, diff T4, T7, T9, and build RESULTS_REGISTER.md. Do not write report prose; the author writes the report."
```

### 10. Reviewer prompt (fresh session, S99)

```text
You did not build this repo. Review it against SPEC.md line by line. For each requirement, give PASS/FAIL with evidence (file path, command run, output). Check specifically: (1) every number in reports/ appears in RESULTS_REGISTER.md and can be regenerated; (2) no evaluation window contains gap_2022 dates; (3) thresholds in state/preregistration.yaml were committed before T7 (compare git timestamps); (4) data/raw/ hashes match MANIFEST.csv; (5) baseline_results_by_group.csv is unchanged; (6) all 12 shock events appear in T7; (7) no banned words in outputs; (8) every DEVIATIONS.md entry is reflected in results; (9) no name appears if author is TO_CONFIRM. Write reports/REVIEW.md. Do not fix anything; report only.
```

If you use Claude Code, back the key rules with deterministic controls: a deny rule or PreToolUse hook blocking edits under `data/raw/`, and a Stop hook that runs `make check`. Claude Code's guidance is that a rule which keeps getting missed belongs in a hook ([Claude Code](https://code.claude.com/docs/en/best-practices)). In claude.ai cloud sessions, the research did not verify whether hooks and resume features exist there. The ledger, markers and git then carry the whole guarantee.

## Conclusion

The first benchmark changes what the project can promise. Naive persistence already beats every classical model, and TCB prices sit unchanged on most report days. So the useful product is not a sharper point forecast. It is a **calibrated expected range plus an honest accounting of what measured costs explain**. This reframing suits a non-thesis project: RQ3 and RQ4 deliver applied value even if RQ1 stays negative, and a negative RQ1 reported per stratum with significance tests is a legitimate result. The binding constraint is labels, not models. With only 12 in-window shocks, 7 of them low confidence, and most falling in 2023–24 rather than the 2025–26 test window, alert results will carry wide uncertainty whatever the method. That is why the evaluation window (D8) and a threshold fixed before scoring (D4) matter more than adding another foundation model.

The resume protocol is built for the user's real setup, Colab with Drive, where a dropped runtime is routine. Checkpointing at the unit level rather than the stage level means a disconnect costs minutes, not a rerun of 87 origins. Two things need human action before the pipeline can finish cleanly: the original TCB files, for the audit that would turn "transcribed" into a measured error rate, and answers to D1–D9, starting with the thesis-versus-project framing and whose name goes on the work. Until then, the agent can complete S00, S01, S03 and S04 and leave every dependent stage visibly blocked rather than quietly assumed.
