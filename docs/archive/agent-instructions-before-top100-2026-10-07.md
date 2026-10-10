# 과거 에이전트 지침 보관

2026-10-07 Top100·$1M 문서화 직전의 지침을 보존한다. 아래 명령형 문장은 당시 운영 기록이며 현재 작업 지시가 아니다. 현재 기준은 [루트 AGENTS.md](../../AGENTS.md)와 [병렬 계획](../parallel-investigation.md)이다. 원문 내용은 보존하고 로컬 링크만 이 보관 위치에 맞췄다.

---

# Agent instructions

## 최신 승인 범위 — 과거 THESIS와 저시총 토큰 우선, 2026-10-07

사용자가 과거 THESIS를 확보하고 저시총 대상으로만 우선 조사하라고 요청했다. 기존 두 달 window `2026-08-07T00:00:00Z`–`2026-10-07T04:43:41Z`를 유지한다. 우선 선별 기준은 **각 retained THESIS 게시 시점의 시총≤$10M**이라는 agent 가정이며 `<$30k / $30k–200k / $200k–1M / $1M–10M`로 기록한다. FDV·유통 시총·현재 시총을 분리한다. 역사적 유통 시총이 없고 낮은 총발행량 평가액만 있으면 provisional이고, 시총 unknown을 eligible로 바꾸지 않는다.

이번 연우 historical THESIS9건(9/25–10/6)과 고정 Top10 기존20건을 정규화했다. 새9건은 `fomo_events`에도 `derived_thesis_document` ID로 저장했다. 현재 이벤트999/THESIS151, 관측29/선별9. 연우 과거 두 달 completeness는 unknown이다. CZ FDV 대용치 $844,583.532464795는 예비 대상, baton은 작성45초 전 provider 시총 $14,082,929.317754881로 제외, 나머지7개는 pending이다. 가격 unknown을 시총0으로 만들지 않는다. 최신 한글 보고서는 [lowcap-thesis-review.md](../lowcap-thesis-review.md), review raw2067, validation raw2068, `collector_state.lowcap_thesis_research_v1`을 따른다.

**명시적 historical-source 예외:** 신규 Fomo는 계속 REST-only다. `/v2/alerts`는 BUY/SELL/알림 checkpoint, 문서와 live response로 확인한 `/v2/thesis/user/{id}`는 별도 과거 글 원문 경로다. 사용자 latest request로 이 REST 경로를 추가했다. WebSocket은 재개하지 않는다. 원문은 직접 raw2016에 연결하고 alert cursor를 올리지 않는다. User THESIS는 since/cursor가 문서화·반환되지 않았으므로 indexed 목록의 끝을 lifetime 완료로 선언하지 않는다. Top1 raw2017의 `available:false/upstream-unavailable`은 실패이며 empty history가 아니다.

이번 Fomo2페이지/1250credits, 직접RPC24회, GeckoTerminal20회/CoinGecko2회, Bridge0/BigQuery0다. 실행별 Fomo 총≤2페이지(THESIS+alerts와 실패 시도 합산), 직접RPC≤30, Bridge≤5를 유지한다. 현재 실행의 남은 한도를 새 프로세스로 리셋하지 않는다. GT 429 실패는 1회 재시도 후 다음 실행 frontier로 보존한다. 기존 complete capture는 재수집하지 않는다.

다음 우선순위는 CZ 검증된 PancakeSwap V3 pool `0x6f0aa2c067ce5f6e5253d7f6487548fa01601b3b`의 bounded 실제 swap/final buyer와 동시 군집이다. Token participants는 이 승인된 토큰·시간 창의 후보일 뿐 Top10 trader나 같은 소유자로 편입하지 않는다. 현재 11:31:30–14:31:30 UTC 후보 창과 첫 Fomo BUY12:27/THESIS13:31:30을 분리한다. 같은 private funding/반환/정확한 non-shared CEX deposit과 기존 Fomo 지점이 실제 겹칠 때만 분기를 확장한다. BigQuery는 필요한 window dry run/cap만 실행한다.

CZ 두 성공 receipt는 canonical factory/getPool과 공식 Swap ABI로 매수 및 final raw output 일치를 확인했다. 새 retained THESIS보다3870/682초 앞선 알려진 Fomo 대응 거래이며 뒷지갑·절대 첫 공개 이전·조종·수익 증거가 아니다. 이전 14,668전송/3711수령은 첫 BUY 이전 window이고 실제 swap buyer coverage가 아니다. 기존 RZD/Yeon wallet trace와 resolutions는 보존했다. RZD 새 tracing은 현재 재개하지 않는다.

## 최신 승인 범위 — 연우 두 달 추적, 2026-10-07

사용자가 연우 조사를 두 달 전까지 확장하라고 요청했다. 현재 고정 구간은 `2026-08-07T00:00:00Z`–`2026-10-07T04:43:41Z`이며, 연우의 기존 Fomo/연결 주소와 제보 주소가 우선 대상이다. RZD는 이번에 제한된 이전 한 달 토큰 조회만 보완했고 기존 tracing frontier는 보존했다. 이 명시적 계정 조사는 과거 Top 10 파일럿의 좁은 예외이며 다른 계정을 일괄 확대하지 않는다.

최신 한글 결과는 [두 달 추적 보고서](../two-month-review.md), review raw2014, `collector_state.research_two_month_v1`과 `yeon_wallet_trace_v1`에 있다. 저장한 Nodit 조회 12개/15,826행의 결과 회수는 complete이나 모든 체인·토큰·CALL의 coverage는 unknown이다. 이번 호출은 Fomo2페이지, 직접RPC30, Bridge5주문, Nodit Data API196요청(재시도 포함), BigQuery0이다. 다음 실행도 Fomo≤2, 직접RPC≤30, Bridge≤5를 유지한다. 보존된 complete capture를 다시 수집하지 않는다.

`54d2 → c67a → BSC Binance 51`은 같은 수량 USDC3건/588,098.805041163975619333이며 9/8 한 쌍만 양쪽 독립 receipt가 검증됐다. `54d2 → 32f023 → Binance 51`의 8/10 12.5BNB 공급과 전달도 transaction/receipt/header가 검증됐다. `32f023`과 과거 제보 주소3개의 native 관계는 현재 창 밖의 비교 근거다. `32f0a` 유사 주소의 미검증 BNB 이름 토큰 이벤트를 실제 native 자금 관계에 승격하지 않는다. 거래소 endpoint 라벨과 동일 고객·소유권을 분리한다.

Bridge 도구는 `54d2 → 1726 → Relay` Ethereum USDC3건/114,345.733494를 known Fomo Solana 주소로 연결했다. 도착 당시 token-account owner/delta와 시각의 직접 검증은 pending이다. Source tx/account/token/raw amount가 실제 source transfer와 맞는 주문만 보존하며 shared Relay/Mayan pooled flow를 귀속하지 않는다. Operation이 없는 Mayan2개는 gap이다. RPC 한도를 새 실행으로 임의 초기화하지 않는다.

CZ 첫 retained BUY 전 전송14,668행/수령주소3,711개와 제보·직접 공급 상대의 교차는 0이다. 이는 매수나 뒷지갑 부재의 판정이 아니다. Fomo CZ2개 실행은 실제 Solana quote 감소/BSC 최종 취득과 대응하지만 첫 공개 THESIS를 확보하지 못했다. 연우 retained 이벤트는10/4부터9개/THESIS0, RZD는10/3부터42개다. 브라우저 프로필은 현재 세션에서 로그인 홈페이지로 이동한다. CALL·최초 공개·매수·매도 시각과 원가/PnL을 혼동하지 않는다.

다음 순서는 c67a/32f023 inbound 및 정확한 고객 입금 주소 후보 비교, 나머지 USDC 두 쌍의 receipt, Relay 도착3개 historical owner/delta, 두 달 CALL 원본과 Solana8/7–9/6 owner gap, 실제 exit/quote/원가다. Wallet resolution과 RZD frontier를 임의 변경하지 않는다.


## CEX·STOCKER 세부 추적 갱신 — 2026-10-07 KST

최신 근거는 [rank9-cex-prebuy.md](../rank9-cex-prebuy.md)를 따른다. 6a2의 BSC CEX→wallet 9건(KuCoin 14.307388 / Robinhood 15.83557942 BNB), 과거 6a2→80cf 0.265 ETH→Coinbase 입금 후보 0.086 ETH를 RPC로 확인했다. CEX 역할은 Arkham 라벨이며 고객 계정·소유권은 unknown이다. Robinhood Chain 출금 2건은 public RPC HTTP403 때문에 Arkham-only이며 summary USD 총계의 완전 재조정도 미완료다.

6a2의 10/6 02:55:23~02:55:59 UTC STOCKER 매수 4건은 ETH supplied 1.8, network gas 0.000646099977211829, wrapped WETH 1.782, token acquired 1,114,947.519342597221320112이며 이후 RZD 본지갑 반환과 raw amount가 정확히 같다. 첫 THESIS 직전·매수 직전·반환 후 6a2 잔액은 0. 최초 retained BUY/THESIS보다 늦고 세 번째 THESIS보다 11시간42분 앞선 취득이다. 최초 공개 전 선행매수·동일 소유권·실현 수익으로 판정하지 않는다. Fomo amount_usd와 Arkham 현재 USD는 원가로 사용하지 않는다.

Ethereum discovery 3개 query/454행은 결과 회수 complete이나 chain coverage/watermark는 unknown이다. 알려진 정확한 Robinhood·Coinbase deposit 주소를 seed/funder/6a2의 canonical USDC·ETH 기록과 비교해 funder→Robinhood 1건만 관측했다. 공통 CEX 입금은 미확인이다. 미검증 token contract·0-value·dust·유사 주소를 ownership/funding graph에 자동 승격하지 않는다. 고정 window 이전은 prior_history_extension, 이후는 incremental로 구분한다.

27,001.6471 USDC 추가 공급 및 RZD Ethereum→RZD Solana Relay 주문은 양쪽 RPC·destination deposit/operation memo로 order_correlated가 됐다. SQLite tracing 신규18행/전체31행, acquisitions4행, discovery3/454행, 최신 review raw1605. collector_state.rzd_wallet_trace_v1의 latest review/frontier부터 재개한다. 다음 우선순위는 반환 STOCKER 실제 sale/exit, 정확한 CEX deposit 반복/공통 주소, BSC outflow 및 기존 pending 주문이다. 아래 milestone 수치는 과거 snapshot이다.

## Latest authorized continuation — 2026-10-07 KST Relay and funder tracing

Heartbeat `rzd-relay` is ACTIVE every 6 hours on this thread. Resume `collector_state.rzd_wallet_trace_v1`; keep unchanged runs quiet and report material new connections or required action. Per run, cap Fomo at 2 pages, direct RPC at 30 requests, and Bridge at 5 orders. The repo remains /Users/seoho/Desktop/web3/fomo-top-trader-research even when this thread cwd differs.

사용자가 Relay 실제 출발·도착과 공급 지갑의 지속 추적을 요청했다. 기존 rank9 분기에서 실제 bridge/order로 발견한 6a2 Ethereum→YDfd Solana→verified RZD Solana 반환까지 다음 bounded slice로 확장한다. 이전 2-hop 제한은 이전 파일럿의 경계이며 이 명시적 continuation의 실제 주문·전송에 따라 이어 간다. 다른 trader나 Relay pooled service 전체를 확장하지 않는다. 고정 30일 결과와 cutoff 뒤 incremental 결과를 분리한다.

상류 보존 7/7 Relay Solver→funder 주문은 verified RZD Solana owner에서 출발했고 각 SPL/USDC 감소와 성공 ETH receipt를 대조했다: 출발 599,060.667266 / 수령 599,012.409890 USDC. Order 대응은 provider assertion (`provider_order_matched_legs_verified`)이다. Funder→6a2 13,000.71504 USDC, 6a2→RZD ETH 1,114,947.519342597221320112 STOCKER를 직접 receipt로 확인했다. 6a2의 2.8821 ETH→YDfd의 64.133031727 SOL은 source deposit ID·operation ID destination memo와 양쪽 RPC가 일치한다. YDfd 수령 후 13개 거래를 읽었고 11개 KNOTS 취득 후보 net 증가 2,366,114.800191이 이후 RZD Solana에 보낸 gross와 같다. RZD net은 2,295,131.356185이다. 추가 8.027063514 SOL의 source는 unknown이다.

새 wallet_trace_edges 13행, review raw 1508와 collector_state.rzd_wallet_trace_v1로 provenance/frontier를 저장했다. 미검증 주소의 wallet resolution·ownership은 바꾸지 않았다. Ethereum getLogs plan range 실패, Robinhood Chain4663 resolver 미지원, 기존 unresolved deposit, 새 funder 공급 receipt가 남았다. RZD 새 REST event 3개를 저장했으나 KNOTS는 현재 retained RZD call이 없다. Intermediate STONK mint를 wallet-owned KNOTS 취득과 혼동하지 않는다. 다음은 정확한 STOCKER 취득/THESIS window, 실제 추가 bridge 입금의 source, 그리고 반환 이후 exit/CEX의 동일 주소 여부다. 상세 proof·시각·금액·한계는 [rank9-wallet-trace.md](../rank9-wallet-trace.md)를 따른다.

## Read first
- Read this file and [the full research brief](../research-brief.md) before changing the repository.
- The brief is the source of truth for the research question, required entities, phases, constraints, and success criteria.

## Latest approved workflow — 2026-10-06 BigQuery API/CLI

The user confirmed the existing BigQuery API/CLI route and asked to fix this workflow in the repository documentation. Use the authenticated Google Cloud `bq` CLI with explicit query project `exchange-labs`; add a direct API or Python SDK path only if result pagination or collector needs justify it. MCP is an optional interface, not a prerequisite. Dune is excluded from the active workflow. Earlier milestones below are historical snapshots; the current sequence is in the first section of `docs/implementation-plan.md`.

Source responsibilities:

- Fomo REST: leaderboard and BUY/SELL/THESIS source events, with existing per-user checkpoints.
- BigQuery: bounded historical transfers, token-account owner activity, funding candidates, and same-token event-window discovery.
- RPC/Etherscan: important transaction receipts/instructions, successful state, swap/quote/fee semantics, and source gaps.
- Local Bridge API: correlate the actual source deposit/order to its destination leg; retain direct RPC proof.
- SQLite/Python: canonical source evidence, normalized timelines, deduplication, inventory lots, and PnL only after adequate trade/cost/exit evidence.

Rank 9 RZD's Ethereum ERC-20 pilot is complete for `2026-09-06T07:46:11Z <= timestamp < 2026-10-06T07:46:11Z`: 34 rows retrieved in 2 pages, all matched to 34 retained logs across 33 successful receipts; all 8 real-USDC Relay deposits match. BigQuery event_index equals receipt log_index for all 34 reference logs. The Solana receipt/owner/event slice is now complete; follow the Solana milestone below before the existing-funder event-window slice. Existing funders may be included within the prior two-hop pilot. Expand to other verified Top 10 wallets after their source/coverage checks. Arbitrum and other chains require actual Fomo/bridge evidence.

Every BigQuery collection must preserve SQL/hash/version, project/dataset/location, parameters and UTC range, job ID, raw result pages, capture time, total/fetched rows, processed/billed bytes, and completeness. Use dry runs and `maximumBytesBilled`, finish pagination, keep exact token amounts as strings, and distinguish complete result retrieval from complete on-chain history. Verify the mapping between BigQuery event indexes and retained receipt log indexes. Do not treat a transfer as a buy or a funding edge as common ownership.

`src/fomo_research/bigquery.py` now collects the Ethereum pilot, resumes saved job/pages, imports without cloud calls, and reconciles retained receipts. SQLite tables `bigquery_collections`, `bigquery_result_pages`, and `bigquery_erc20_transfers` have 1/2/34 rows; raw payload total at Ethereum-pilot completion was 1,040; the current owner milestone has 1,445. It uses stdlib plus the existing bq CLI, a 40-GiB default cap, parameterized SQL, exact raw quantities, and additive transactional ingestion. This run retained 6 CLI captures and billed 35,100,033,024 bytes. The initial evaluation and its 1 known Solana receipt crosscheck remain prior evidence. Full query-result retrieval is confirmed; all-action/lifetime chain coverage is unknown. Do not repeat a cloud scan to reparse the complete saved capture. See README usage and `docs/schema.md`.

## Solana owner/history milestone — 2026-10-06 UTC

RZD Solana owner 파일럿도 완료했다. 같은 고정 30일 구간에서 known bridge 수령 7/7의 성공·slot·시각·USDC mint/owner/raw delta가 BigQuery와 RPC에 일치했다. BigQuery owner 11,763행 중 실제 token 잔액 변동은 11,575행이며 모두 full RPC와 일치했다. QuickNode `tokenAccounts=balanceChanged`로 13페이지/11,580개 원문을 회수했고, 기존 EOA history에 없던 11,000개 활동을 SQLite에 중복 없이 합쳤다. Fomo 18개 event의 24시간 전후 window도 저장했다. 전체 raw는 1,445, normalized actions는 44,382, token deltas는 62,885, token timelines는 27행이다. `SwapTob`/`SwapEvent` 등 로그 이름을 인식하도록 수정한 `solana-heuristic-v3`에서 RZD는 SWAP 1,144 / TRANSFER 318 / UNKNOWN 11,138행이다. Known bridge 7건은 기존 직접 SPL/order 증거로 TRANSFER이며 매수나 수익으로 처리하지 않는다. 새 11,000개 활동에서 추가 SWAP은 0개이고, 기존 RZD 358개 label은 실제 swap 로그와 opposing balances에 따라 교정됐다. 다른 세 검증 지갑도 보존 데이터만 재분류했으며 신규 history는 수집하지 않았다.

Solana BigQuery는 collection/page/source row 3/38/23,533행(행 역할 간 signature 중복을 포함), raw CLI capture 67건이다. Query별 exact SQL/version/hash/parameters, job/bytes와 페이지 provenance가 있고 complete saved capture는 cloud 재실행 없이 import한다. Billed bytes는 12,067,997,220,864(약 10.976TiB), reference $6.25/TiB에서 $68.60이며 실제 invoice/credit balance는 미확인이다. 큰 예상 비용을 사용자에게 알린 뒤 cap을 적용했다. Account/native/log 전체 projection의 24.554TiB dry run은 실행하지 않았다. QuickNode 13호출은 문서 단가 기준 1,560 credits 추정이고 잔액은 unknown이다.

다음 범위는 이미 보존한 Ethereum funder 후보의 같은 chain·같은 Fomo token에 대한 BUY/THESIS 전후 활동이다. 최대 2-hop과 ownership unknown을 유지한다. Solana 추가 wallet 수집은 먼저 `tokenAccounts=balanceChanged` full pages를 사용하고, BigQuery는 historical owner 및 known gap/토큰·시간 window 대조에 필요한 범위를 dry run으로 결정한다. 이번 full owner scan이나 기본 EOA-only history를 다시 반복하지 않는다. Quote/fee/이전 재고/exit·transfer 원가를 검증한 뒤 inventory와 PnL로 넘어간다. 상세 결과는 `docs/rank9-solana-owner-review.md`와 ignored `data/research/rank9-solana-owner-analysis.json`에 있다.

## BigQuery cost preference — 2026-10-06

The user reports approximately KRW 400,000 in Google Cloud credits and requests notification only for large costs. The working notification threshold is estimated KRW 50,000 for one research work batch, introduced as an agent assumption. Apply dry runs and maximumBytesBilled to routine queries and record actual job usage. Notify before a large batch or if forecast work would consume the remaining reported budget. This notification preference does not introduce a separate approval gate for routine authorized work. Actual credit balance, eligibility, monthly free allowance, and billing/currency rate remain unverified; use conservative estimates until known.

## Previous authorized slice — 2026-10-06 Bridge continuation

The user supplied a running local Bridge aggregator at `http://127.0.0.1:8080` and explicitly authorized cross-chain resolution of the repeated RelayDepository transfers. Related destination legs are now in scope for rank 9; this does not authorize unrelated traders or chain-wide backfill. Dune remains excluded.

The eight retained Ethereum deposits total 223,983.849692 USDC. Seven deposits, totaling 213,983.299662 USDC, are correlated with successful Solana USDC receipts owned by rank 9's already verified Solana wallet. For each, the retained Ethereum deposit event ID and the Relay operation ID both appear in the destination transaction's memo; amount, SPL mint, token-account owner, balance delta, canonical slot, and successful transaction state agree. Never use transaction hash alone to assign a shared batch's orders to the seed.

One 10,000.55003-USDC deposit (`0x007980f4ddadd0f7008d82c5312d7103f352bd415de81c75102dfd19da9c327b`, source transfer log 176, deposit event log 177) remains unresolved. Both source and arbitrary-transaction lookup returned another user's order. Keep that order and the unrelated Polygon order excluded. Missing order coverage is not proof of failed bridging. The upstream recurring funder's ownership, CEX endpoints, pre-thesis trading, and PnL remain unresolved.

`src/fomo_research/bridge.py` captures bounded source queries, preserves API assertions separately from direct RPC verification, and imports captures without additional network requests. Additive SQLite tables `bridge_deposits`, `bridge_resolve_requests`, `bridge_rpc_requests`, and `bridge_routes` have 8/9/13/7 rows. The canonical raw layer has 1,034 rows including one explicit capture-gap metadata record: a duplicate public-RPC response was overwritten during the initial scratch capture, while the same destination has a retained successful configured-RPC response. The reusable collector uses content-hash filenames. The JSON report is the ignored `data/research/rank9-bridge-evidence.json`; the prior Ethereum Flow case is preserved as its earlier snapshot.

All seven new destination signatures are absent from the earlier `solana_normalized_actions` dataset. Their transaction account keys contain token accounts rather than the owner's EOA; historical token-balance owners prove the wallet mapping. Do not describe the earlier EOA backfill as complete owner activity. Preserve the bridge receipt ledger and merge by chain/signature/wallet before inventory or PnL so incoming bridge funds are not dropped or counted twice. Follow the one unresolved deposit ID and then its verified Solana receipt activity, or resume the already bounded recurring-funder pagination. Do not assign new wallets to the trader from transfer relationships.

## Previous authorized slice — 2026-10-06 Etherscan
The user explicitly requested a tracing-first pilot and then asked to use the Etherscan skill. This narrows the current work to rank 9's already verified Ethereum wallet, a fixed recent 30-day window, and at most two hops. It is a limited exception to the earlier Phase 1 graph deferral; it does not mean the Phase 1 gate or the broader identity/PnL research is complete. Dune is excluded from the active workflow after both MCP execution and the logged-in website showed no execution access.

Etherscan CLI 1.0.8 has a usable local credential. The first case used 100 logged API attempts, including 63 transaction receipts; the one nametag call was denied by the current plan. The seed's three account feeds ended on short first pages: normal 0, ERC-20 34, internal 0. All 34 seed transfer rows were reconciled against 33 successful receipts. Counterparty coverage is partial. Store API responses and case provenance in SQLite; do not infer a CEX role from a contract name or assign counterparty ownership from transfers. `evm_flow_cases`, `evm_flow_requests`, and `evm_flow_movements` preserve the case, 100 requests, and 42 selected receipt-log movements. New raw payload total: 1,011; the earlier Fomo/Solana totals below describe the preceding slice.

The Etherscan Flow case and fetch log are in the platform scratch directory and the canonical case JSON and API evidence are also preserved in SQLite. Results and investigative findings live in the case JSON. The import command is `PYTHONPATH=src python3 -m fomo_research.etherscan_flow --case <case-file> --fetchlog <fetchlog-file> --rank 9`. It performs local ingestion only and adds no API calls. Next, resume the actual USDC counterparty pagination and inspect the retained deposit-order evidence to select a traceable onward branch. Resolve individual order/destination evidence before following a shared service's pooled funds. Continue Fomo collection through REST checkpoints. Keep other traders, chain expansion, identity attribution, and PnL outside this pilot.

## Previous milestone
The authorized scope is a fixed Top 10 pilot from the 2026-10-05 16:04:43.128 UTC 30-day leaderboard snapshot. All ten have Solana and EVM candidates. Solana ranks 1, 5, 9, and 10 are verified; the Ethereum (`chain_id=1`) candidates for ranks 8 and 9 are also verified with two distinct Fomo event IDs and two distinct successful transaction hashes each. Rank 3 and rank 8 Solana candidates remain ambiguous because multiple signatures fit their event windows. Resolution is chain-specific: do not infer Robinhood, Base, BNB, or other EVM activity from the Ethereum proof. Do not attribute other candidate wallets to traders.

New Fomo collection is REST-only through `/v2/alerts`; the old WebSocket collector is removed, and earlier short captures remain legacy evidence only. Ten user-scoped requests returned 200 unique Top 10 events dated 2026-10-03 through 2026-10-06 (99 BUY, 84 SELL, 17 THESIS; 140 Solana). Every response had `hasMore=false`. No alert before October 3 was returned despite a September 6 start; retention and lifetime completeness are unknown. The latest observed Fomo API balance is 246,250 credits after 750 credits of successful rank-8/9 Ethereum POC calls; rank-8 retryable 503 attempts cost zero.

The ignored SQLite database currently has 973 Fomo events, 458 traders, 911 raw payloads, 16 candidate/matched on-chain trade rows, 12 verified event-match links, 8 ambiguous links, and 6 chain-specific verified wallet resolutions (four Solana, two Ethereum). It contains 33,382 wallet/signature actions, 51,885 token deltas, and 27 Trader × Token rows. Action labels are provisional heuristics: 16,803 SWAP, 9,039 TRANSFER, and 7,540 UNKNOWN. The four Ethereum rows store exact target-token raw amounts and receipts; quote/protocol/amount-USD are NULL pending quote-leg attribution. Same signatures are stored once per tracked wallet so shared transactions preserve each wallet's own balance changes.

QuickNode `getTransactionsForAddress` full-history pages cover at least 60 days for ranks 1, 5, and 9 (24,400, 3,600, and 1,600 rows; 122, 18, and 8 pages). Whole boundary pages create a small spill beyond 60 days. Rank 10 has 3,782 records from 2026-08-24 through 2026-10-05, about 42.6 days, ending at the provider's returned history boundary. The 148 new requests cost an estimated 17,760 credits at the documented 120 credits each; response headers did not provide the remaining QuickNode balance. The active `SOLANA_RPC_URL` remains Nodit; the QuickNode credential was used transiently and was not saved. Never print or commit credentials or raw provider data.

Event-level windows show a same-token SWAP BUY in the prior 24 hours for 3/5 rank-1, 28/36 rank-5, 1/2 rank-9, and 7/12 rank-10 Fomo BUY events. Among complete following 24-hour windows, a same-token SWAP SELL follows 27/29 rank-5, 2/2 rank-9, and 0/1 rank-10 BUY events; rank 1 has no complete post-event window yet. These are alert counts, not unique swaps, intent, or PnL. Rank 10's two reviewed Fomo-matched transactions each spent 5,000 USDC, while the Fomo `usdValue` fields do not match those quote amounts. Transfer basis remains unknown.

The eight verified Solana event/signature matches have a local USDC quote and protocol-log screen. Direct SPL transfer legs were decoded for 956 actions that changed the 27 timeline tokens: 342 gross amounts match wallet deltas and the remaining 614 reconcile after applying same-mint observed 1%/3% inbound Token-2022 fees. Historical mint fee-config state was not fetched, and reconciled transfer amounts do not reveal acquisition cost. The four verified Ethereum event/signature matches have exact target-token output matches and successful receipts, but quote token/amount, protocol, and 30-day history coverage remain unresolved; Fomo rank-8 quote token metadata is inconsistent with Ethereum. Next, inspect only quote legs in the four retained receipts and run a bounded 30-day EVM-history coverage probe for ranks 8 and 9 against a provider that indexes contract-mediated account activity. Then build per-token inventory lots and inspect post-event exits before PnL. Keep polling Fomo with each user's saved REST checkpoint. Dune MCP remains visitor/read-only with zero credits/quota; other EVM chains and X posts are not collected. Do not expand beyond Top 10. Counterparty tracing is limited to the separately authorized rank-9 Ethereum pilot above.

## Research and data rules
- Verify providers, endpoints, fields, authentication, rate limits, and historical coverage from accessible documentation or live responses. Cite URLs and record the date checked in docs/data-sources.md.
- Never invent endpoints, undocumented fields, sample payloads, or capabilities. Mark anything that cannot be verified as unknown and record the needed credential or access.
- Keep collection event-first: leaderboard snapshots and Fomo BUY/SELL/THESIS events precede wallet backfill. The current graph exception is rank 9's bounded funding pilot and its verified bridge legs; a transfer relationship never proves common ownership.
- Do not re-enable WebSocket collection. Use REST `/v2/alerts` for alert checkpoints and the latest authorized `/v2/thesis/user/{id}` for historical post observations. Keep native alert IDs and derived thesis document IDs distinct. Record source time, parameters, capture time, HTTP status and credit cost/balance. Treat retention, missing pagination and saturation as coverage unknown.
- Keep on-chain BUY/SELL evidence separate from transfers. Never treat a token transfer as a swap without evidence.
- Preserve distinct on-chain BUY, Fomo BUY, Fomo THESIS/CALL, X POST, and on-chain SELL timestamps. Store timestamps in UTC.
- A single event-to-transaction match may be stored as a candidate but cannot verify a wallet. Require two distinct Fomo event IDs and two distinct transaction signatures, or a direct transaction hash/signature from the source.
- Never put API keys, private keys, cookies, or tokens in source control. Do not commit collected raw data or local databases.
- BigQuery is the active indexed history source. Retrieve complete job results through the authenticated CLI/API and persist raw pages, SQL/job provenance, and completeness in SQLite. Keep Dune as historical source research only. Do not assume decoded events or a DEX-only dataset cover every wallet action.
- Reuse repository conventions and choose the smallest viable architecture. Do not add providers, services, databases, or dependencies until the Step 1 findings justify them.

## Deliverable and stop condition
Record verified source facts, collection gaps, wallet-match evidence, and the next bounded slice in `docs/implementation-plan.md` and `docs/data-sources.md`. Keep every on-chain BUY/SELL distinct from transfers and every source timestamp distinct in UTC. The authorized cohort remains Top 10. The rank-9 Ethereum tracing exception is described above; do not attribute unverified candidate or counterparty wallets to traders. Four verified traders have preliminary event-token timelines; review these records and their coverage before expanding beyond the cohort.
