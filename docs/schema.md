## THESIS+BUY 조사 기준 이벤트 — 2026-10-07 v2

`parallel_anchors.py`는 기존 `fomo_events` BUY와 `fomo_thesis_observations` semantic THESIS를 고정 cohort/60일 구간으로 조회한다. BUY84/THESIS100 기준 이벤트, 전체112개의 정확한 chain/token 대기 목록을 `raw_payloads.source=lowcap_event_inventory`의 JSON 연구 결과로 추가 저장했다. 최신 raw2099, `collector_state.top100_lowcap_event_inventory_v2`가 결과와 frontier를 가리킨다. 새 관계형 anchor/screen 테이블은 아직 없다. BUY를 THESIS로 변환하거나 기존 `lowcap_thesis_screens`에 가짜 thesis key를 넣지 않는다.

JSON anchor는 type/key/Fomo event ID 또는 thesis key, 정확한 chain/token/user, reference UTC와 basis, source raw/locator, BUY source·actual swap·public visibility·capture 시각을 구분한다. BUY의 actual swap/public visibility는 검토 전NULL·pending/unknown이고 기존 verified event/token match를 자동 경제적 BUY로 승격하지 않는다. BUY cap84건은pending이며 기존 THESIS cap100건은 threshold1000000 검토를 재사용했다. queue는 BUY-only 여부·distinct BUY traders·THESIS authors·각 anchor cap 상태를 별도 보존한다.

원본 schema와 wallet resolutions·native alert cursor·RZD/연우 state는 유지했다. JSON 편의 파일은 canonical raw 결과의 내보내기다. 상세 [한글 조사 보고서](buy-prebuy-review.md)를 따른다.

## Top100 첫 배치 — 2026-10-07

기존 스키마를 재사용한다. `fomo_events`에167행 추가(native90/별도THESIS77), 현재 Top100 고정구간 이벤트257행(THESIS100/BUY84/SELL73)이다. `fomo_thesis_observations`는 해당 cohort101 source observations/100 semantic documents이며 같은 원문에 둘 이상의 source ref가 있을 수 있다. `lowcap_thesis_screens`에 threshold1000000의100행을 새 raw2096/version으로 추가했다(excluded1/pending99). 과거 $10M row와 wallet resolution·RZD/연우 state는 보존한다. 상태는 `collector_state.top100_parallel_foundation_v1`, 결과와100명 진행표는 [첫 배치 보고서](top100-first-batch-review.md)다. 아래 수치는 과거 milestone 기록이다.

# SQLite schema

## Top100 병렬 계획의 저장 계약 — 2026-10-07 KST

[정책 JSON](agent-research-policy.json)과 [작업 명세](../agents/task-packet.template.json)는 에이전트용 문서 계약이다. 기존 수집기가 자동으로 읽는 설정이나 새 DB table이 아니다. 이번에는 코드·스키마·DB를 변경하지 않았다.

Worker 결과는 자체 ignored 작업 경로에 raw/정규화 후보/근거를 저장하고, 본체가 검토 후 기준 SQLite에 추가 적재한다. 임시 파일 refs를 canonical raw ID에 매핑하고 transaction identity·provider assertion/RPC proof·exact raw amount·UTC·coverage를 보존한다. 신규 cluster/task 관계형 table은 아직 구현하지 않았으며 필요 시 별도 additive 작업으로 만든다.

기존 `lowcap_thesis_screens`의threshold10000000 및 raw2067은 과거 결과다. 새 기준은 threshold1000000/새 review version으로 추가해야 하며, 문서가 바뀌었다고 기존 row의 decision을 새 기준의 적격값으로 취급하지 않는다. 초기 cohort raw1654의100개 사용자 ID는 기존 Top10 importer scope와 별도 확인이 필요하다.

## 과거 THESIS·저시총 선별 추가 — 2026-10-07

- `fomo_thesis_observations`:29 source observations/29 semantic document keys. Author+exact chain/token+publication UTC+trade+원문으로 문서 키를 만들고, 원본 raw ID·locator·provider ID·text·source timestamp를 별도로 보존한다. 시각이 같아도 글이 다르면 다른 문서다. 원본 alias가 진짜 Fomo native ID인지 임의 확정하지 않는다. Publication은 provider assertion, absolute first public은 unknown이다.
- `fomo_events`: 새 사용자 THESIS9행은 `event_id_kind=derived_thesis_document`, `event_id=thesis_doc_<semantic hash>`로 추가한다. Native alert 원문과 정확히 같은 semantic 문서면 중복하지 않는다. `amount_usd=NULL`, 원본 raw2016 직접참조, source UTC를 사용하며 alert checkpoint를 변경하지 않는다.
- `lowcap_thesis_screens`: review+thesis key별 versioned9행씩. Historical market_cap과 FDV proxy 별도 TEXT, exact raw supply TEXT/decimals, sample/block시각, threshold10000000, decision/status 및 모든 source raw refs를 저장한다. 같은 원문을 재분석한 review는 additive로 남으며 latest state가 current review를 가리킨다.
- `collector_state.lowcap_thesis_research_v1`:현재 review raw2067/validation raw2068, 고정 window, provider 갭, 제한과 next frontier. `lowcap_thesis_collection_run_2026_10_07_v1`는2회 Fomo 시도를 보존한다.

모듈은 `src/fomo_research/theses.py`다. `import_saved_theses`/`save_screens`는 local-only이고 canonical 기존 trace·wallet resolution·alert cursor를 수정하지 않는다. API 어댑터 `get_user_theses`가 문서화된 historical route만 제공한다. 선택 분봉은 모든 CALL 포함 미완료 interval을 버리고 source UTC/5분 이내로 검증한다. 현재9 screens,29관측과 원본 FK0오류를 확인했다. 아래 내용은 이전 schema milestones다.

갱신일: 2026-10-06 UTC. 기준 DB는 ignored `data/research/fomo.sqlite3`다. 기본 source/event/wallet/timeline schema는 `src/fomo_research/store.py`, Etherscan Flow는 `etherscan_flow.py`, Bridge는 `bridge.py`, BigQuery는 `bigquery.py`·`bigquery_solana.py`, owner RPC는 `solana_owner_rpc.py`, event 분석은 `owner_analysis.py`의 실제 CREATE TABLE을 따른다.

## BigQuery Ethereum pilot

| Table | Key | 저장 내용 | 현재 행 수 |
|---|---|---|---:|
| `bigquery_collections` | `collection_key`; project/location/job unique | 고정 case·Fomo user·wallet, SQL/version/hash, typed parameters, dataset/location, UTC 구간, 예상·상한·processed/billed bytes, row count, retrieval/coverage, 대조 report, raw metadata FK | 1 |
| `bigquery_result_pages` | collection/page index; collection/start row unique | 페이지 offset·row count·capture time, raw_payloads FK | 2 |
| `bigquery_erc20_transfers` | collection/tx hash/event index/batch index | block hash/number/time·transaction index, token contract, from/to, exact quantity, TRANSFER label, raw page FK, matched receipt log index/raw FK/status | 34 |

`raw_payloads`에는 `source=bigquery_bq_cli`로 6개 CLI 응답을 보존했다. CLI argv, SQL stdin hash, stdout, parsed payload, exit code, capture/completion time을 저장하며 인증 키나 토큰을 전달·기록하지 않는다. 조회 SQL 원문과 typed parameter는 collection 및 capture manifest에 있다.

### 연결과 정밀도

- Collection은 기존 `evm_flow_cases.case_key`와 `traders.fomo_user_id`에 연결한다. 해당 case의 고정 Top 10 snapshot 및 Ethereum wallet resolution `verified`를 확인한 뒤 수집한다.
- Result page는 원본 `raw_payloads.id`를 가리킨다. Transfer는 자신의 page 원본과 대응한 Etherscan receipt 원본을 각각 보존한다.
- `quantity_raw`와 byte 통계는 TEXT이며 uint256을 float로 바꾸지 않는다. 실제 raw CLI 문자열은 원본에 그대로 있다. Amount unit 환산은 검증된 decimals가 있을 때만 한다.
- ERC-20의 null `batch_index`는 normalized key에서 -1로 표기한다. 원본의 null은 유지된다. BigQuery `event_index`와 receipt `log_index`는 별도 컬럼이며 이번 34건에서 같음을 확인했다.
- `receipt_comparison_status=exact`는 성공한 보존 receipt와 토큰·주소·금액·블록 정보·event/log index가 일치한 경우다. New rows는 근거가 없으면 미검증 상태다.
- `retrieval_status=complete`는 query가 성공하고 totalRows 전체 회수·연속 페이지·중복 검증을 통과했다는 뜻이다. `history_coverage_json.history_status=unknown`은 모든 종류의 온체인 history를 보장하지 않는다는 뜻이다.
- 기존 source tables를 교체하지 않고 세 테이블을 추가했다. 완전한 같은 collection 재적재는 기존 report를 재사용한다. 최초 raw/page/transfer 삽입은 하나의 SQLite transaction으로 진행한다.

SQL `report_json`에는 baseline receipt log별 비교, bridge deposit별 비교, canonical-USDC 여부를 구분한 contract별 raw 합계, 추가 행, 비용·회수·coverage 근거가 있다. `data/raw/bigquery/<collection_key>/report.json`은 같은 report의 로컬 export다.

## Solana owner sources and event windows

| Table | Key | 저장 내용 | 행 수 |
|---|---|---|---:|
| `bigquery_solana_collections` | collection key; project/location/job unique | rank-9 Ethereum source case와 chain별 verified Solana wallet 연결, role, actual SQL/version/hash/typed parameters, scope/snapshot/UTC, job and byte statistics, raw metadata/coverage/report | 3 |
| `bigquery_solana_result_pages` | collection/page index; collection/start row unique | 연속 offset·row count·capture time·raw FK | 38 |
| `bigquery_solana_transactions` | collection/signature | slot/time/status, exact original projected row JSON, raw page FK | 23,533 |
| `bigquery_solana_rpc_checks` | collection/signature FK | available-field 대조, verified/mismatch/unavailable, original RPC raw page/point FK, checks JSON | 11,579 |
| `bigquery_solana_owner_rpc_pages` | collection/page index | request/response cursor, typed full request JSON, row count, raw capture FK/time | 13 |
| `bigquery_solana_event_windows` | collection/event ID; Fomo event FK | independent Fomo time, token/wallet/type, prior/following 24h time bounds, time-scope flags, observed swap counts/times/delay, raw signature evidence/unknown movements | 18 |
| `bigquery_solana_analyses` | collection key | analysis version, scope/results/token timelines/job usage/limits and generated time | 1 |

Owner rows have 3 roles: known_receipts=7, owner_discovery=11,763, owner_details=11,763. Role overlap is source evidence, not additional transactions; source signature cardinality is 11,763. `solana_owner_balances_v1` detail rows intentionally omit account keys/native balances/fee/logs and retain signer/semantics as unknown. UInt64 raw token balances remain exact strings in source JSON. RPC comparison links may point to a full page containing many signatures; the signature and page index inside `checks_json` identify the transaction. Point null attempts remain in raw payloads even where verified bulk evidence replaced their comparison status.

Canonical `solana_normalized_actions` / `solana_action_token_deltas` remain wallet/signature based. Source loaders reuse prior EOA history, verified bridge points, full owner RPC pages and available indexed fields; no source-role double counting. Balance-only rows cannot imply signer=false, native delta=0, swap or transfer. `classification_version=solana-heuristic-v3` records explicit swap instruction/event patterns and retained bridge SPL/order proofs. Total actions/deltas are 44,382/62,885; RZD 12,600 actions are SWAP 1,144 / TRANSFER 318 / UNKNOWN 11,138. `trader_token_timeline` still has 27 rows and preserves UTC source times and observed history bounds.

Event windows only count successful, same-token provisional SWAP sides. Equal timestamps and transfers are not automatically pre-event buys. The two scope flags describe whether all 24 hours fit inside the frozen query range; provider history is still unknown. `evidence_json` retains prior buys/following sells and unmatched semantic owner movements. Window results do not inherit source lifetime completeness or economic PnL. Saved analysis is also exported under ignored `data/research/rank9-solana-owner-analysis.json` for review.


## Wallet tracing continuation — 2026-10-07 KST

`src/fomo_research/wallet_trace.py` adds `wallet_trace_edges` without modifying prior cases, owner labels or wallet resolutions. The edge key hashes type + both chain/address/tx/locator/asset identities. Exact from/to amounts are TEXT; gross and recipient net may differ. Columns separately preserve chain, address, transaction, locator, UTC, asset, raw amount, decimals and successful source/destination raw references. `provider_raw_payload_id` is separate. `edge_type` is TRANSFER or BRIDGE; statuses distinguish `rpc_verified`, `provider_order_matched_legs_verified`, and `order_correlated`. Counterparty `ownership_status` remains unknown. `scope_context` distinguishes fixed historical window and incremental continuation.

Initial rows: 13 edges (8 bridge orders,5 transfer logs/instructions). Existing request captures and reviewed recipient activity are preserved in raw_payloads; the report raw 1508 contains 13 reviewed Solana recipient actions, with per-capture references and exact observed target/native deltas. These unverified counterparty actions are not inserted as verified trader actions. State key `rzd_wallet_trace_v1` stores frontier/gaps/latest report pointer. It does not advance Ethereum history completeness over failed log queries. Import is offline, transactional for rows, and skips existing raw hashes and edge identities. It preserves reviewed evidence, not an independent proof validator.

## CEX/pre-buy tracing extension — 2026-10-07 KST

`cex_prebuy.py` adds `wallet_trace_discovery_collections` (3 rows: exact SQL/parameters/job/window/dry-run/cap/statistics/total/page provenance), `wallet_trace_discovery_rows` (454 rows: exact projected JSON/raw-page FK and discovery cautions), and `wallet_trace_acquisitions` (4 rows: chain/address/tx/token raw amount, ETH supplied/WETH wrapped/network gas, unknown ownership, receipt/tx/header/query FK, individual Fomo event timing evidence). The existing `wallet_trace_edges` adds 18 reviewed edges, total31. Latest CEX/pre-buy review raw1605; raw payload total1605. Discovery rows are not attributed to RZD ownership, and acquisitions are not inserted into verified RZD action tables.

Historical extensions before fixed-window start use scope_context `prior_history_extension`. Complete query pagination is separate from unknown chain/watermark/lifetime coverage. Exact CEX roles remain third-party Arkham assertions even when transfer legs are independently RPC-verified. See [rank9-cex-prebuy.md](rank9-cex-prebuy.md).


## Nodit 인덱스 조회 근거 — 두 달 확장, 2026-10-07

`src/fomo_research/indexed_api.py`의 `import_collection`은 저장된 SQLite raw page만 읽는다. 네트워크 요청이나 wallet resolution 변경은 하지 않는다. 기존 테이블을 지우지 않고 다음 두 테이블을 추가한다.

- `indexed_api_collections`: provider/chain/route, research-context Fomo user, 정확한 UTC 요청 범위와 필터, reported/fetched unique rows, retrieval 상태와 별도 history coverage, manifest raw FK와 원문을 보존한다. Fomo user는 조회의 연구 맥락이며 상대 주소 소유권 귀속이 아니다. Key는 provider·chain·method·request의 hash다.
- `indexed_api_movements`: collection별 tx/locator/block/UTC/from/to/asset/raw amount 문자열/decimals, selector, row 원문, raw page FK와 주의 사항을 보존한다. Key는 tx·locator·asset이며 PK는 collection과 movement의 조합이다. 같은 tx가 다른 조회 역할로 반복될 수 있다.

Native row는 `TOP_LEVEL_TRANSACTION`, token row는 `TOKEN_TRANSFER_EVENT`다. 원문 event를 매수로 바꾸지 않는다. 전부 `provider_indexed_assertion`이며 zero-value, contract call, dust, 성공 미확인 상태를 별도로 표시한다. 직접 RPC로 검증한 중요 전송은 기존 `wallet_trace_edges`의 별도 근거로 저장한다. 미검증 토큰 또는 fake symbol이 동일 소유권·funding 근거가 되지 않는다.

Complete collection은 unique normalized row 수와 provider count가 맞아야 한다. 경계가 겹치는 시간 분할은 tx/log/batch identity로 중복 제거하며 서로 다른 금액/from/to를 가진 동일 identity는 거부한다. 이미 더 큰 결과가 저장돼 있으면 더 작은 partial 결과로 교체하지 않는다. 이번 실제 저장은12collections/15,826movements이며 count0 조회도 필터와 gap을 보존했다. 전체 체인 이력 coverage는 unknown이다.

Wallet trace에 이번15edges가 추가됐다(현재 구간9, 이전 비교6). CZ2개 bridge edge는 양쪽 transaction을 직접 검증했지만 대응은 prior Relay UI assertion이라 `provider_ui_correlated_legs_rpc_verified`다. 3개의 새 Ethereum→Solana Relay 도착은 historical owner/delta/time 미검증으로 review raw와 frontier에만 보존했다. `checkedAt/observedAt`을 실제 거래 시각으로 쓰지 않는다.


## BUY 실제 매수·시총 후속 검토 — 2026-10-07

새 관계형 BUY screen 테이블은 추가하지 않았다. `raw_payloads.source=top100_buy_anchor_review`의 raw2140에26개 exact BUY identity, 별도 Fomo/실제 swap/후보 token 전달/공개 노출 시각, cap status·sample·raw refs·gap·한도·frontier를 보존했다. 작업자 결과 원문/정규화/report/hash는 `parallel_buy_worker_review` raw2133–2137, indexed collection manifest는 raw2138–2139다.

`onchain_trades`/`event_trade_matches`에 SNDK·ZCAT2쌍을 추가했다. Raw698/696의 success·signer·historical owner별 최종 token/quote net delta를 확인했고 existing verified seed를 사용했다. 기존 KNOTS match와 wallet resolution은 변경하지 않았다. BSC 후보 token 수령2건은 index movements와 canonical review에 저장했으며 verified Fomo economic BUY table로 승격하지 않았다. 인덱스의 reported/fetched1/cursor 없음은 각각 정확한 account+contract±120초 filter의 retrieval만 뜻한다.

`parallel_anchors.py`는 저장된 본체 BUY review를 정책/cohort/window/threshold/source identity로 대조해 적용한다. 실제 시각·cap evidence를 보존하고, eligible/excluded는 실제 swap 검토·양수 circcap·직전300초 sample와 threshold가 맞아야 한다. FDV 대용치는 pending이며 source clock/ownership은 덮어쓰지 않는다. Latest state는 `top100_buy_anchor_review_v2`, 통합 목록 state는 `top100_lowcap_event_inventory_v2`/raw2141이다. 전체184 anchors 중 excluded2/pending_cap180/pending_cap_proxy2/eligible0, reviewed BUY26/actual verified3이다.
