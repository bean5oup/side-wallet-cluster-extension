# Fomo Top Trader Research

## 최신 연구 정리 — 2026-10-10 / 배치062

**PPT 작성 전 종합 보고서:** [연결 지갑·THESIS 전후 매매·회수 경로 한글 보고서](docs/pre-ppt-linked-wallet-research-report-ko.md).

- **Werey/PURR:** 검증 본지갑과 실제 일반 자금 송금이 오간 F1bNo의 게시 전 유상 재고, 게시 후 전량 처분과 Binance 라벨 경로를 확인했다.
- **Solstice/DOGINU:** 공통 공급자로 연결된 별도 지갑 5NS의 실제 선취득과 보존 THESIS 110초 뒤 매도를 확인했다.
- **판정 한계:** 같은 소유의 뒷지갑·개인 공통 CEX 고객·THESIS 악용 실현 수익·이벤트 당시 유통 시총≤$1M은 미확정이다. 엄격한 저시총 완결 사례는0건이며, 관측 사례가 없다는 뜻은 아니다.
- **로컬 저장 현황:** Fomo 이벤트1,338개 / 온체인 거래4,569개 / 대응73개 / 추적 연결646개 / 지갑 검증 레코드11개. 전체60일·모든 체인 수집 완료를 뜻하지 않는다.
- **저장소 구성:** 코드·정책·한글 사례 보고서를 Git으로 관리한다. API/RPC 인증정보, SQLite, 수집 원문·로컬 분석 결과는 ignored 파일로 보관하며 Git에 포함하지 않는다. 새 checkout에는 기존 증거 DB가 자동으로 제공되지 않는다.

최신 근거와 재개 지침은 [AGENTS.md](AGENTS.md), [실행 계획](docs/implementation-plan.md), [Werey 배치062 후속](docs/werey-funded-wallet-inventory-and-cex-review.md)을 따른다. 아래 이전 실행 결과의 수치·라벨·범위는 당시 기록이며 최신 판정으로 읽지 않는다.

## 최신 실행 범위 — 초기 지정 10명 집중

raw141의 초기 Top10 계정 10명을 대상으로 60일 기록과 게시/매수 당시 유통 시총 $1M 이하 사건을 조사한다. [우선순위 1·2·3과 명단](docs/top10-investigation-priorities.md), [정확한 ID·focus 설정](docs/top10-investigation-focus.json)을 따른다. 기존 Top100 확대 배정은 새 작업으로 시작하지 않는다. 아래 Top100 결과는 이전 실행 기록이며 이번 범위 갱신에서는 새 수집을 하지 않았다.

이전 BUY 후속 결과: [THESIS 없는 BUY 첫 검토](docs/buy-first-batch-review.md). 7명·9토큰·BUY26건에서 검증 본지갑 실제 매수3건과 BSC 후보 토큰 수령2건을 분리해 저장했다. ZCAT 해당 BUY1건은 시총 상한 초과로 제외, 나머지25건은 보류다. 저시총 심층 적격은 아직0이며 최신 review raw2140/통합 목록 raw2141을 재사용한다.

## 이전 운영 계획 — Top100 · 게시/매수 당시 시총100만 달러 이하

사용자 지정 기준은 **THESIS/CALL 게시 또는 BUY 당시 유통 시총 USD≤1,000,000**이다. THESIS 없는 BUY도 선별 대상으로 포함하고 실제 매수 이전 군집·노출 이후 추종 매수·매도·자금 연결을 비교한다. Fomo BUY 시각, 실제 swap 시각, 대외 노출 시각은 분리한다. [BUY 조사 기준과 현재 목록](docs/buy-prebuy-review.md).30d Top100의 기존 raw1654를 고정하고, `gpt-6-luna` · 추론 수준 `max` 작업자 5개가 계정 기초 수집과 적격 token별 군집·exit·자금 연결을 분석하며 본체가 검토·SQLite 적재·최종 판단을 맡는다. FDV·현재 시총·미확인 cap은 적격으로 바꾸지 않는다.

- 시작 지침: [AGENTS.md](AGENTS.md)
- 전체 운영 구조: [병렬 조사 계획](docs/parallel-investigation.md)
- 기계 판독 정책: [agent-research-policy.json](docs/agent-research-policy.json)
- 역할별 지시: [작업자](agents/worker.md), [본체 검토](agents/reviewer.md)
- 배정 입력: [작업 명세 양식](agents/task-packet.template.json)

**과거 수집 기간은60일**이다. 정책·배정 양식에 `lookback_days=60`을 명시했고, 첫 고정 구간은 `2026-08-08T04:43:41Z`–`2026-10-07T04:43:41Z`(UTC)다. Fomo 공개/거래 이벤트와 적격 토큰 지갑 이력에 적용한다. 공급자 보존 범위가 짧으면 미확보 기간을 기록한다.

**첫 실행 완료:** `gpt-6-luna`·`max` 작업자5개가 기존 Top100 자료와 새10명 캡처를 검토했다. 신규167이벤트를 SQLite에 적재했고, 기존 원문 포함 THESIS100건/12명/87토큰을 정규화했다. $1M 기준은 제외1건·보류99건·적격0건이며60일 history는 미완료다. [한글 결과와100명 진행표](docs/top100-first-batch-review.md). Fomo20회/7,250credits, 시장자료7회이며 이번 BigQuery 조회는없다.

## 이전 조사 결과 — 과거 THESIS와 저시총 토큰

[한글 결과 보고서](docs/lowcap-thesis-review.md): 연우 과거THESIS9건(9/25–10/6)을 새로 확보하고 기존Top10 원문20건과 정규화했다. CZ는 당시 가격×총발행량 약$844,583.53의 예비 대상, baton은 게시 시점 주변 시총 약$14.08M이라 제외,7개는 보류다. 두 달 전체 글·CZ 유통 시총·뒷지갑·수익은 미확인이다. 이는 이전 $10M 파일럿의 기록이며, 현 $1M 기준에서 CZ는 유통 시총 근거가 필요한 보류 대상이다.

`get_user_theses`는 과거 게시글 REST 어댑터다. `theses.import_saved_theses`는 저장 원문을 local-only로 정규화하고 event timeline에 THESIS를 추가한다. Canonical 저장소는 SQLite이며 `fomo_thesis_observations`, `lowcap_thesis_screens`, `collector_state.lowcap_thesis_research_v1`이 최신 자료를 가리킨다. 기존 Fomo BUY/SELL polling은 `/v2/alerts`를 유지한다. 아래 결과는 이전 milestone이다.

Research workspace for reconstructing Fomo Top Trader public events and comparing them with verified on-chain activity.

## Previous rank-9 tracing result

See [CEX/pre-buy investigation](docs/rank9-cex-prebuy.md): verified CEX-direction transfers, exact STOCKER acquisition/return, bounded Ethereum discovery, and unresolved common deposit/ownership/profit.

## Start here

1. Read AGENTS.md for the current agent instructions.
2. Read the complete research brief in docs/research-brief.md.
3. Read docs/data-sources.md and docs/implementation-plan.md before expanding collection or adding on-chain sources.

## Confirmed collection workflow

The user confirmed BigQuery through the existing authenticated API/CLI route. Use `bq` with query project `exchange-labs` for the first collector. Google Cloud authentication is managed locally; no BigQuery API key is copied into `.env`. MCP is optional. Dune is excluded from the active workflow.

| Source | Responsibility |
|---|---|
| Fomo REST | Leaderboard and BUY/SELL/THESIS timestamps |
| BigQuery API/CLI | Historical transfers, token-account owner activity, funding and same-token candidates |
| RPC/Etherscan | Important receipts/instructions and swap, quote, fee verification |
| Local Bridge API | Correlated source/deposit/destination evidence |
| SQLite/Python | Canonical evidence, normalization, timelines, inventory and verified PnL inputs |

The bounded RZD rank-9 Ethereum 30-day collector is implemented and ran successfully. Its 34 ERC-20 rows were retrieved in 2 pages and persisted in SQLite; all 34 retained receipt logs and all 8 USDC bridge deposits match, including event/log indexes. The fixed window is `2026-09-06T07:46:11Z` inclusive through `2026-10-06T07:46:11Z` exclusive. The Solana receipt/owner collection is also complete: 7/7 known receipts and all 11,575 nonzero token-balance changes agree with full RPC. Owner history adds 11,000 previously omitted activities; Fomo event windows are stored in SQLite. Other verified Top 10 wallets follow the pilot coverage checks.

The user reports about KRW 400,000 in cloud credits. The working large-cost notification threshold is KRW 50,000 per research work batch, an agent assumption rather than a user-specified limit; estimate and cap routine queries, record actual usage, and notify if forecast work would consume the reported remaining budget.

Ethereum BigQuery tables have 1 collection, 2 result pages, and 34 ERC-20 transfers. Solana tables have 3 collections, 38 pages and 23,533 role-specific source rows for 11,763 unique signatures, plus 11,579 RPC comparisons and 18 event windows. SQL/parameters, job metadata, cost statistics and 6 raw CLI captures are preserved. This is complete retrieval of the bounded ERC-20 result, not proof of all wallet activity. See [the implementation plan](docs/implementation-plan.md), [schema](docs/schema.md), and [limitations](docs/limitations.md). Older collection sections below retain prior observations.

## BigQuery Ethereum pilot

Run from the repository root with the existing Google Cloud authentication:

```sh
PYTHONPATH=src python3 -m fomo_research.bigquery --project exchange-labs --maximum-bytes-billed 42949672960 --page-size 25
```

The collector derives the wallet, fixed cohort and UTC interval from the verified rank-9 Ethereum Flow case. It dry-runs parameterized ERC-20 SQL, submits a stable job ID, records the destination result's total row count, and reads every page. A complete saved capture is reused on rerun; a partially downloaded job resumes from its saved offset. No dependency installation or new credentials are needed.

Local-only reimport:

```sh
PYTHONPATH=src python3 -m fomo_research.bigquery --import-capture data/raw/bigquery/2d414f21c65e8f562d08f27a69fd1139e33e0f38f8b6f23497647454ed8e6357
```

Evidence is in `data/raw/bigquery/2d414f21c65e8f562d08f27a69fd1139e33e0f38f8b6f23497647454ed8e6357/manifest.json`, content-addressed `captures/*.json`, and `report.json`; the same report is in `bigquery_collections.report_json`. This run matched 34/34 receipt logs and 8/8 bridge deposits, with no additional or missing ERC-20 rows against that baseline. The exact billed amount is 35,100,033,024 bytes (32.689453125 GiB). At a reference $6.25/TiB, compute is about $0.20 before free allowance/credits; actual account billing remains unverified. [Google Cloud pricing](https://cloud.google.com/bigquery)

## Local API credentials

The local repository root has an ignored .env file with FOMO_API_KEY and SOLANA_RPC_URL configured. For another checkout, copy .env.example to .env and set those values locally. BigQuery uses the locally managed Google Cloud authentication and an explicit `exchange-labs` query project. Dune credentials are not part of the active collection setup. Never commit or print credentials. Solana requests use SOLANA_RPC_URL when set; otherwise the collector falls back to the public mainnet endpoint. The current local .env uses a Nodit RPC credential URL; do not copy it into source control or logs.

## Local collector

Python 3.9+ is sufficient; the collector uses the standard library and SQLite.

```sh
PYTHONPATH=src python3 -m fomo_research init-db
PYTHONPATH=src python3 -m fomo_research snapshot --period 30d --limit 50
PYTHONPATH=src python3 -m fomo_research sync-alerts --rank 1 --since 2026-09-06T00:00:00Z
# Later polls reuse that trader's saved checkpoint and re-read the previous 5 minutes:
PYTHONPATH=src python3 -m fomo_research sync-alerts --rank 1
PYTHONPATH=src python3 -m fomo_research build-timeline --rank-limit 10
```

Fomo activity collection now uses REST `/v2/alerts`; the old WebSocket collector and its dependency have been removed. The first `sync-alerts` run needs `--since` and one Top 10 `--rank` or `--user-id`; later runs reuse that trader's SQLite checkpoint and re-read the previous 5 minutes. The REST response exposes `hasMore` and `nextCursor`; `--max-pages` bounds credits and stores the cursor for the next run. Requests with results cost 125 credits each; empty user-filtered requests may cost 0. Historical alert filters by `userId` are supported by the provider's OpenAPI and were verified in live responses. `alerts --since ... --limit ...` remains available for one-off pulls; `--type buy|sell|thesis` can narrow one request.

To check a recent Solana event against the configured RPC, run `PYTHONPATH=src python3 -m fomo_research match-solana`. A single strong event-to-transaction match is stored as a candidate. The wallet is marked verified only after at least two distinct Fomo events match at least two distinct successful transaction signatures, with signer, token direction, and quote/swap evidence. `build-timeline` merges stored EOA pages, owner/token-account full RPC pages and verified bridge receipts for the fixed verified Top 10 wallets, writes normalized rows to SQLite tables `solana_normalized_actions` and `solana_action_token_deltas`, and stores the Trader × Token result in `trader_token_timeline`. It then exports CSVs under `data/research/`. `build-timeline` also refreshes the inventory table. Run `PYTHONPATH=src python3 -m fomo_research build-inventory --rank-limit 10` when refreshing inventory alone without reprocessing full transaction pages. CSVs are convenience exports; query SQLite as the canonical research dataset. SWAP and TRANSFER labels remain evidence-based heuristics and need review before economic conclusions.

The default SQLite database is `data/research/fomo.sqlite3`. Raw responses, relational source tables, and derived research tables stay local and are ignored by Git. SQLite is canonical; CSV files are regenerated from SQLite and are also ignored. The confirmed indexed-history path is BigQuery SQL → authenticated CLI/API result retrieval → complete raw pages and job provenance → SQLite. The Ethereum and Solana history collectors/importers are implemented; complete captures are retained under ignored `data/raw/bigquery/`, with canonical normalized rows and reconciliation reports in SQLite. Earlier evaluation data remains under `data/research/`. A 30-day Top 50 leaderboard costs 250 credits per snapshot; hourly capture is about 180,000 credits per 30-day month. REST alerts cost 125 credits per request; credit cost and remaining balance are stored with each raw API response.

## Use and storage limits

FomoAPI.io's terms allow use of retrieved data in internal applications and operations, while prohibiting standalone redistribution, bulk mirroring, and a substantially similar competing API. The terms do not specify a retention duration. FomoAPI.io is independent from fomo.family; how fomo.family terms apply to third-party API output is unresolved. Keep the database private to this research workspace and do not publish raw rows. Review current terms before expanding collection or sharing derived datasets.

## Etherscan tracing pilot

The previous Etherscan pilot traced the verified rank-9 Ethereum wallet over a fixed recent 30-day window with a two-hop limit. Dune is excluded from the active workflow. Etherscan CLI 1.0.8 uses its existing local credential; do not print or copy the key. The case is an Etherscan Flow JSON document. All findings, confidence limits, and incomplete branches are inside that document, also stored as `evm_flow_cases.case_json` in SQLite.

Import a generated case and its credential-free per-request fetch log:

```sh
PYTHONPATH=src python3 -m fomo_research.etherscan_flow \
  --case /tmp/fomo-etherscan-rank9/case-afe3b520-flow.json \
  --fetchlog /tmp/fomo-etherscan-rank9/case-afe3b520-fetchlog.jsonl \
  --rank 9
```

This command adds no API requests. It verifies that the seed matches an existing verified Ethereum wallet in the fixed cohort, checks edge amounts and hashes against successful receipts, and atomically saves the case, request provenance, and individual receipt-log transfers. Reimporting the identical case does not add duplicate rows. `evm_flow_movements.amount_raw` remains a text integer; amounts are not rounded or stored as SQLite REAL. Transfer rows are separate from swaps and wallet resolutions. Native account feeds are retained as raw evidence; this pilot's normalized graph contains selected ERC-20 transfers.

The initial case has 100 recorded requests, 42 selected movements, eight graph nodes, and seven merged edges. The seed account feeds ended on short pages, while some counterparty feeds remain partial. No source balance or PnL was invented. API nametags require access that the current plan did not provide. Review the case JSON before continuing its remaining branches. SQLite remains canonical; scratch files are import artifacts.

## Cross-chain bridge continuation

The local user-supplied Bridge API is available at `http://127.0.0.1:8080`. The continuation keeps the verified rank-9 Ethereum seed and follows only its selected receipt-backed deposits. Source queries use `POST /v1/bridge/resolve`; an arbitrary-transaction query used `POST /v1/bridge/resolve-transaction`. No new API key or dependency is needed.

Capture the selected recipient's deposits, independently check returned Solana destination receipts, and save the evidence to SQLite:

```sh
PYTHONPATH=src python3 -m fomo_research.bridge \
  --recipient 0x4cd00e387622c35bddb9b4c962c136462338bc31 \
  --api-url http://127.0.0.1:8080 --max-transactions 20
```

The latest Ethereum case is selected by default; use `--case-key` to pin another retained case. The transaction limit rejects oversized batches before any API calls. Raw captures go to ignored `data/raw/bridge/` directories with content-hash filenames. If the configured Solana RPC returns a successful HTTP response with a null transaction, the collector attempts the public mainnet RPC once. RPC credential URLs are never stored in captures. There is no background polling or automatic provider retry.

Import retained captures without making network requests:

```sh
PYTHONPATH=src python3 -m fomo_research.bridge \
  --recipient 0x4cd00e387622c35bddb9b4c962c136462338bc31 \
  --captures /tmp/fomo-bridge-rank9
```

The canonical tables are `bridge_deposits`, `bridge_resolve_requests`, `bridge_rpc_requests`, and `bridge_routes`. Source movement foreign keys point to the original successful Ethereum receipt log; destination rows retain their direct RPC raw-payload ID, provider provenance, exact raw amounts, separate chain IDs and timestamps, and existing wallet-resolution status. Reimporting retained captures re-evaluates available RPC proof without duplicating raw evidence. Provider-only output remains distinct from independently verified output.

The initial eight source deposits total 223,983.849692 USDC. Seven correlate to rank 9's already verified Solana wallet, totaling 213,983.299662 USDC. A 10,000.55003-USDC deposit remains unresolved because the returned order belongs to another user in the same source batch. These are transfers, not PnL. The seven destination transactions were missing from the earlier EOA backfill and are preserved in the bridge ledger; merge this ledger with existing activity by chain/signature/wallet before inventory accounting. The ignored review export is `data/research/rank9-bridge-evidence.json`. See the latest sections of `docs/data-sources.md` and `docs/implementation-plan.md` for coverage and capture gaps.

## Previous collection status

Two 30-day Top 50 snapshots and 973 Fomo events are saved locally. Earlier short WebSocket captures remain historical raw evidence; all new Fomo event collection uses REST `/v2/alerts`. A user-scoped pull over the fixed Top 10 returned 200 unique events dated 2026-10-03 through 2026-10-06: 99 BUY, 84 SELL, and 17 THESIS, including 140 Solana events. Each of the ten user responses had `hasMore=false`; no alert before October 3 was returned despite the September 6 start, so provider retention and lifetime completeness remain unknown. Solana ranks 1, 5, 9, and 10 and Ethereum EVM candidates for ranks 8 and 9 are verified from two distinct Fomo event IDs and two successful transaction hashes each. Rank 3 and rank 8 Solana remain ambiguous; other EVM candidates and other chains for ranks 8 and 9 remain unverified. The latest Fomo API balance is 246,250 credits after the targeted Ethereum POC.

QuickNode `getTransactionsForAddress` now provides at least 60 days of full transaction history for verified ranks 1, 5, and 9: 24,400, 3,600, and 1,600 rows across 122, 18, and 8 pages. The final pages include a small amount of data beyond the cutoff. Rank 10 retains its complete returned history of 3,782 rows (2026-08-24 through 2026-10-05; about 42.6 days). The three new backfills used 148 documented 120-credit requests (17,760 credits estimated); the response did not expose a remaining-balance header, so the QuickNode account balance is unknown. No QuickNode credential was saved to the repository.

Before the Etherscan pilot, SQLite held 911 raw payloads, 16 candidate/matched on-chain trade rows, 12 verified event-match links, 8 ambiguous links, 33,382 wallet/signature actions, 51,885 token deltas, and 27 Trader × Token timeline rows. The normalizer labels 16,803 actions as SWAP, 9,039 as TRANSFER, and 7,540 as UNKNOWN using log, signer, and balance heuristics. A shared-transaction issue was corrected: the same signature is retained separately for each tracked wallet. In event-level windows, a same-token SWAP BUY appears in the 24 hours before 3/5 rank-1, 28/36 rank-5, 1/2 rank-9, and 7/12 rank-10 Fomo BUY events. Of BUY events with a complete following 24-hour window, a same-token SWAP SELL follows 27/29 rank-5, 2/2 rank-9, and 0/1 rank-10 events; rank 1 has no complete post-event window yet. These counts can reuse the same on-chain swap across overlapping alerts and are not PnL or proof of intent.

The rank-10 token review still shows why Fomo `usdValue` must not be treated as on-chain trade consideration: its two matched buys each spent 5,000 USDC, while the alerts reported different position values. Across the four verified Solana wallets, all eight matched transactions show USDC quote movements and protocol instructions; 956 target-token transfer rows now reconcile using gross amounts or same-mint observed Token-2022 fees. The four Ethereum matches have successful receipts and exact target-token amount matches, but quote token/amount and protocol remain unresolved. Historical fee-config state, acquisition costs for transferred lots, and post-event exits remain incomplete, so PnL is not calculable. Dune execution remains unavailable and the user has excluded it from the active workflow. The confirmed BigQuery workflow above sets the current next-step sequence; rank-8 history, quote attribution, other chains, and X posts remain unresolved. See `docs/implementation-plan.md` and `docs/data-sources.md`; local tables and CSV exports are under `data/research/`.

## Solana owner history and event review

Read [the RZD owner review](docs/rank9-solana-owner-review.md) for scope, costs, differences and actual pre-THESIS observations. The fixed window is the same 30 days as Ethereum. BigQuery `Transactions` historical pre/post token owners include receipts omitted by the original EOA query. The known seven BigQuery sample logs were blank; source balances alone do not classify swaps.

```sh
PYTHONPATH=src python3 -m fomo_research.bigquery_solana --stage known_receipts --maximum-bytes-billed 137438953472 --page-size 4
PYTHONPATH=src python3 -m fomo_research.bigquery_solana --stage owner_discovery --maximum-bytes-billed 4398046511104 --page-size 1000
PYTHONPATH=src python3 -m fomo_research.bigquery_solana --stage owner_details --maximum-bytes-billed 8796093022208 --page-size 500
```

These already completed captures are reused on this checkout. `--dry-run` prepares SQL/job scope without submitting a billed query; the configured cap still blocks oversized execution. Before running the owner stages in another checkout, review the work-batch cost and prefer the paginated owner RPC route. Broad Solana columns are expensive.

```sh
PYTHONPATH=src python3 -m fomo_research.bigquery_solana --import-capture data/raw/bigquery-solana/d2b9bf914764b343c18eb8a2b971235850631b77d2252320c5882194f4d540ba
PYTHONPATH=src python3 -m fomo_research.solana_owner_rpc
PYTHONPATH=src python3 -m fomo_research.owner_analysis
```

On this completed capture, the owner RPC command reuses its 13 saved pages without a network request. For a new or partial capture it requires an authorized QuickNode endpoint supplied transiently through `SOLANA_RPC_URL`; the local `.env` remains Nodit. Requests use `transactionDetails=full`, `tokenAccounts=balanceChanged`, explicit UTC bounds and pagination, with transaction version support 1. No QuickNode credential is stored. Normalization uses exact owner balances, actual signer flags and explicit swap instruction/event markers (`solana-heuristic-v3`); the 7 bridge transfers also require retained direct order/SPL proof. `UNKNOWN` remains when semantics are insufficient. The same signature is counted once per wallet. [QuickNode method reference](https://www.quicknode.com/docs/solana/getTransactionsForAddress)

Canonical tables are `bigquery_solana_collections`, `bigquery_solana_result_pages`, `bigquery_solana_transactions`, `bigquery_solana_rpc_checks`, `bigquery_solana_owner_rpc_pages`, `bigquery_solana_event_windows` and `bigquery_solana_analyses`. The report exports under ignored `data/research/` are convenience copies. The prior point-RPC route remains for source-gap checks; broad historical recovery uses full owner pages. Dune and WebSocket collection remain excluded.


## RZD Relay·공급 지갑 후속 추적

최신 연결·증거·미해결 범위는 [추적 보고서](docs/rank9-wallet-trace.md)를 따른다. SQLite `wallet_trace_edges`는 실제 transfer/bridge 양쪽을 보존하고, `collector_state.rzd_wallet_trace_v1`은 다음 frontier를 저장한다. 연관 주소 ownership은 unknown이다. 기존 fixed-window case와 이후 incremental record를 구분한다.

이미 검토한 capture의 네트워크 없는 적재:

```sh
PYTHONPATH=src python3 -m fomo_research.wallet_trace \
  --report data/raw/wallet-trace/rank9-2026-10-07/rank9-wallet-trace.json \
  --captures data/raw/wallet-trace/rank9-2026-10-07
```

Importer는 검토된 증거를 저장하며 원장 검증을 대신하지 않는다. Raw hash와 edge identity로 기존 행을 중복 적재하지 않는다. Unknown counterparty activity는 reviewed report에 남겨 verified Fomo wallet action으로 귀속하지 않는다.


### 최신 연우 두 달 추적

8월7일–10월7일의 한글 결과는 [두 달 추적 보고서](docs/two-month-review.md)에 있다. SQLite의 `indexed_api_collections`/`indexed_api_movements`는 저장한 Nodit 조회12개/15,826행의 필터·페이지·정확 수량을 보존한다. 중요한 직접 검증 전송은 `wallet_trace_edges`에 별도로 저장했다. 재개 상태는 `collector_state.research_two_month_v1` 및 `yeon_wallet_trace_v1`이며, `indexed_api.import_collection`은 raw pages의 local-only 정규화다. 같은 기간 원문을 다시 받아 파싱할 필요가 없다. 결과 회수 complete와 전체 CALL/체인 coverage를 혼동하지 않는다.
