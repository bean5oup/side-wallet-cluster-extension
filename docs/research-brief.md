# 목표

## 최신 실행 범위 — 초기 지정 10명 집중

사용자의 최신 지시에 따라 raw141의 초기 Top10 계정에 집중한다. 현재 순위 또는 Top100 첫 캡처 10명으로 바꾸지 않는다. **10명 과거 기록·실제 BUY·$1M 시총 선별 → 적격 토큰 1~3개 선행 매수/처분/자금 회수 추적 → 10명·토큰 사이의 반복 연결 비교**가 다음 우선순위다. 60일 구간, THESIS 없는 BUY와 Luna5개/max 설정은 유지한다. [상세 계획·원래 명단](top10-investigation-priorities.md), [focus 설정](top10-investigation-focus.json)을 우선한다.

아래 Top100 표본과 실행 결과는 보존된 이전 기록이다. 이전 다음10명 확대 queue는 이 계획으로 대체하며 새 수집을 자동 시작하지 않는다. 기존 Top100 helper의 raw1654/100명 검사가 새 focus를 자동 강제하지는 않는다. 외부 요청 전에 raw141의 명시적 ID에 맞는 capture/적재 경로와 새 예산 예약을 준비한다.

## 현재 사용자 확정 기준 — Top100 · $1M 이하, 2026-10-07

사용자가 병렬 조사 구조를 문서화하고 조사 토큰을100만 달러 이하로 한정하도록 요청했다. 이전 $10M 가정·Top10 파일럿을 현재 계획에 그대로 적용하지 않는다. **각 THESIS/CALL 게시 또는 BUY 당시 유통 시총 USD≤1,000,000**을 확인한 event가 대상이다. THESIS 없는 BUY도 독립 기준으로 포함한다. BUY는 실제 swap·owner·시각 검토와 매수 시점 cap 확인 후 심층 대상이 되며 Fomo source timestamp는 초기 대기 목록 기준이다. 현재 시총·FDV·unknown은 보류한다.

기본 표본은 기존30d Top100 raw1654의 명시적 사용자 ID와 `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z` **60일 고정 구간**이다. 기간 설정은 `lookback_days=60`이며 Fomo 공개/거래 이벤트와 적격 토큰 지갑 이력의 backfill에 적용한다. Provider가60일을 제공하지 못하면 실제 확보 범위와 gap을 기록하고, pagination은 후속 예약 batch에서 재개한다.5개 `gpt-6-luna` · 추론 수준 `max` 작업자가 계정별 기초 자료를 정리한 뒤 중복 제거된 token/time 작업을 분석하고, 본체가 실제 매수·동시 군집·공개 이후 매도·비서비스 자금 연결·같은 정확한 CEX 입금 지점과 PnL 근거를 검토한다.

현재 [THESIS 없는 BUY 첫 검토 결과](buy-first-batch-review.md)는 raw2140/통합 목록 raw2141이며 실제 매수·후보 전달·시총 보류를 구분한다. 현재 운영 지침은 [병렬 조사 계획](parallel-investigation.md), [정책 JSON](agent-research-policy.json)과 루트AGENTS.md다. 계획 문서화와 실제 작업자 실행·수집기 구현은 구분한다. 이하 초기 요청 원문·Phase1 보류·Top10/$10M 설명과 개별 tracing 절은 과거 요구와 당시 결과 기록이다. 현재 scope·역할·한도에 충돌하면 이 절과 최신 사용자 지시를 우선한다. 기존 정확 수량·시간 분리·source proof·SQLite·coverage 원칙은 유지한다.

## 이전 사용자 방향 — 2026-10-07 과거 THESIS·저시총 파일럿

사용자가 두 달 구간의 조사를 유지하면서 과거 THESIS를 확보하고 저시총 토큰을 우선 대상으로 진행하도록 요청했다. 현재 기본 선별 가정은 THESIS 작성 시점의 시총≤$10M이다. 현재 시총·FDV·유통 시총을 혼용하지 않는다. 역사적 자료가 없는 토큰은 보류하고 낮은 FDV proxy만 확보한 CZ는 예비 대상으로 표시한다.

검증된 토큰 pool의 실제 swap/final buyer를 시간 창으로 찾아 매수 군집, 비서비스 공통 자금 공급·토큰 반환·회수와 Fomo의 실제 접점을 조사한다. 동일 정확한 CEX 고객 deposit chain/address는 독립 근거로 대조하며 shared 서비스 endpoint를 동일인 근거로 쓰지 않는다. 기존 Phase1 graph 보류보다 이번 명시적 방향을 우선하되 승인된 token/time 후보 창으로 제한한다. 실제 취득/CALL/exit/quote/fee/원가 없이 조종·선행매수 의도·실현 수익을 확정하지 않는다.

원문 게시 시각과 on-chain/Fomo BUY·X·SELL·capture 시각은 계속 분리한다. SQLite가 기준이며 모든 원문/provenance와 coverage gap을 저장한다. 최신 결과는 [과거 THESIS·저시총 보고서](lowcap-thesis-review.md)다.

## CEX·STOCKER 세부 추적 갱신 — 2026-10-07 KST

최신 근거는 [rank9-cex-prebuy.md](rank9-cex-prebuy.md)를 따른다. 6a2의 BSC CEX→wallet 9건(KuCoin 14.307388 / Robinhood 15.83557942 BNB), 과거 6a2→80cf 0.265 ETH→Coinbase 입금 후보 0.086 ETH를 RPC로 확인했다. CEX 역할은 Arkham 라벨이며 고객 계정·소유권은 unknown이다. Robinhood Chain 출금 2건은 public RPC HTTP403 때문에 Arkham-only이며 summary USD 총계의 완전 재조정도 미완료다.

6a2의 10/6 02:55:23~02:55:59 UTC STOCKER 매수 4건은 ETH supplied 1.8, network gas 0.000646099977211829, wrapped WETH 1.782, token acquired 1,114,947.519342597221320112이며 이후 RZD 본지갑 반환과 raw amount가 정확히 같다. 첫 THESIS 직전·매수 직전·반환 후 6a2 잔액은 0. 최초 retained BUY/THESIS보다 늦고 세 번째 THESIS보다 11시간42분 앞선 취득이다. 최초 공개 전 선행매수·동일 소유권·실현 수익으로 판정하지 않는다. Fomo amount_usd와 Arkham 현재 USD는 원가로 사용하지 않는다.

Ethereum discovery 3개 query/454행은 결과 회수 complete이나 chain coverage/watermark는 unknown이다. 알려진 정확한 Robinhood·Coinbase deposit 주소를 seed/funder/6a2의 canonical USDC·ETH 기록과 비교해 funder→Robinhood 1건만 관측했다. 공통 CEX 입금은 미확인이다. 미검증 token contract·0-value·dust·유사 주소를 ownership/funding graph에 자동 승격하지 않는다. 고정 window 이전은 prior_history_extension, 이후는 incremental로 구분한다.

27,001.6471 USDC 추가 공급 및 RZD Ethereum→RZD Solana Relay 주문은 양쪽 RPC·destination deposit/operation memo로 order_correlated가 됐다. SQLite tracing 신규18행/전체31행, acquisitions4행, discovery3/454행, 최신 review raw1605. collector_state.rzd_wallet_trace_v1의 latest review/frontier부터 재개한다. 다음 우선순위는 반환 STOCKER 실제 sale/exit, 정확한 CEX deposit 반복/공통 주소, BSC outflow 및 기존 pending 주문이다. 아래 milestone 수치는 과거 snapshot이다.

## 추가 승인 범위 — 2026-10-07 KST

사용자가 Relay 출발·도착과 공급 지갑까지 지속 추적하도록 요청했다. 현재 rank9의 실제 bridge 주문 및 연결 전송을 따라 verified seeds와 연관 미검증 주소를 조사한다. 과거 최대 2-hop 파일럿을 이 분기의 실제 주문 증거에 따라 확장한다. 다른 trader나 shared service 전체의 pooled flow는 확대하지 않는다. 목적은 같은 chain/token CALL 전후의 취득·회수와 정확히 같은 CEX deposit endpoint의 중첩을 검사하는 것이다. Ownership/선행매수 의도/PnL은 독립 검증 전까지 unknown이다. 최신 범위·증거는 [후속 추적 보고서](rank9-wallet-trace.md)를 따른다.

Fomo Top Trader 온체인 리서치를 위한 초기 데이터 수집 및 분석 환경을 구축한다.

최종 연구 목표는 다음과 같다.

> Fomo 상위 트레이더의 실제 온체인 거래와 공개 call 시점을 복원하고, 이후 해당 트레이더와 자금 관계가 있는 연관 지갑들이 동일 토큰을 반복적으로 선행 매수/매도하는지 분석한다.

하지만 지금 단계에서는 연관 지갑 분석까지 무리하게 구현하지 않는다.

이번 작업의 핵심은 다음 파이프라인을 안정적으로 구축하는 것이다.

```text
Fomo Leaderboard
        ↓
Trader Registry
        ↓
BUY / SELL / THESIS Event 수집
        ↓
On-chain Transaction Matching
        ↓
Trader Wallet 검증
        ↓
최근 30~90일 거래 Backfill
        ↓
Trader × Token Event Timeline
```

이후 단계에서만:

```text
Funding Graph
→ Linked Wallet
→ Lead-Lag
→ PnL 비교
```

를 추가한다.

---

# 0. 작업 원칙

먼저 현재 repository 전체를 읽고 기존 구조, 언어, DB, API client, config 방식이 존재한다면 최대한 재사용한다.

새로운 구조를 만들기 전에 다음을 수행한다.

1. repository tree 확인
2. README / AGENTS.md / docs 확인
3. 기존 API/RPC client 확인
4. DB 또는 storage 구조 확인
5. 현재 테스트 방식 확인

기존 코드와 충돌하지 않는 방향으로 설계한다.

외부 API endpoint나 undocumented field를 추측해서 구현하지 않는다.

실제 사용 가능한 API/RPC를 확인할 수 없는 경우 interface와 mock adapter를 먼저 만들고, TODO와 필요한 credential을 문서화한다.

API key, private key, cookie, token을 코드에 하드코딩하지 않는다.

---

# 1. 수집 전략

전체 수집 전략은 반드시 다음 원칙을 따른다.

## Event-first

처음부터 Fomo Top 100 지갑의 모든 온체인 transaction과 모든 연관 wallet을 수집하지 않는다.

먼저 Fomo에서 발생하는 event를 저장한다.

수집 대상:

```text
Leaderboard Snapshot
BUY
SELL
THESIS / CALL
```

이 데이터를 기준으로 연구 대상 Trader와 Token Event를 결정한다.

## Wallet Backfill

분석 대상으로 선정된 Trader의 실제 wallet을 검증한 이후에만 해당 wallet의 과거 30~90일 transaction을 backfill한다.

## Graph Expand

Funding graph와 linked wallet 탐색은 Trader Event Dataset이 완성된 이후 별도 Phase에서 수행한다.

---

# 2. 초기 분석 Universe

초기 설정값은 config로 변경 가능하게 한다.

기본값:

```text
Leaderboard Universe:
- 30d Top 50

Deep Analysis:
- 우선 Top 10
- 최대 Top 20

Historical Backfill:
- 기본 60일
- configurable: 30 / 60 / 90 days
```

현재 leaderboard만 사용하는 survivorship bias를 줄이기 위해 leaderboard snapshot을 지속적으로 저장할 수 있는 구조를 만든다.

예:

```text
2026-10-05 12:00
rank 1 trader A
rank 2 trader B

2026-10-06 12:00
rank 1 trader C
rank 3 trader A
```

---

# 3. 데이터 계층

데이터를 반드시 3계층으로 분리한다.

## Raw Layer

외부 API/RPC 응답을 가능한 원본 그대로 저장한다.

```text
data/raw/fomo/
data/raw/x/
data/raw/evm/
data/raw/solana/
```

또는 현재 repository의 storage convention을 사용한다.

Raw payload를 저장하는 이유:

- API schema 변경
- parser 수정
- 재현성
- 분석 로직 변경

때문이다.

## Normalized Layer

공통 schema로 변환한다.

예:

```text
Trader
FomoEvent
Wallet
Trade
Transfer
Call
XPost
```

## Research Layer

최종 분석을 위한 데이터.

예:

```text
TokenEvent
TraderTimeline
WalletLink
LeadLag
PnL
```

이번 Phase에서는 `TokenEvent`와 `TraderTimeline`까지 구현한다.

---

# 4. 필요한 핵심 Entity

다음 모델을 설계한다.

## Trader

```text
fomo_user_id
handle
display_name

rank
rank_period
snapshot_time

reported_pnl
reported_volume

evm_wallet_candidate
solana_wallet_candidate

wallet_resolution_status
```

`handle`은 변경될 수 있으므로 가능하면 stable user id를 primary identifier로 사용한다.

---

## FomoEvent

```text
event_id

fomo_user_id
event_type

BUY
SELL
THESIS

chain

token_address
token_symbol

timestamp

amount_token
amount_usd

trade_id

raw_source
```

---

## OnchainTrade

```text
chain
wallet

tx_hash_or_signature

timestamp

token_address

side
BUY / SELL

token_amount
quote_asset
quote_amount
amount_usd

execution_price

protocol
dex

source
```

단순 transfer와 실제 swap은 반드시 구분한다.

---

## TokenEvent

Trader별 특정 token에 대한 연구 단위다.

```text
event_id

trader_id
chain
token_address

trader_first_buy_at
trader_first_buy_tx
trader_first_buy_amount
trader_first_buy_price

fomo_buy_at

fomo_thesis_at

x_post_at

public_call_at

trader_first_sell_at
trader_first_sell_price

reported_pnl
```

`public_call_at`은 가능하면:

```text
min(fomo_thesis_at, x_post_at)
```

으로 정의한다.

---

# 5. 반드시 분리해야 하는 Timestamp

다음 시점을 절대로 하나로 합치지 않는다.

```text
T1 = 실제 On-chain BUY
T2 = Fomo BUY 표시 시점
T3 = Fomo THESIS / CALL
T4 = X POST
T5 = 실제 On-chain SELL
```

향후 연구에서 다음을 계산한다.

```text
Trader Buy → Fomo Call
Trader Buy → X Post
First Public Call
```

예:

```text
12:42 On-chain BUY
12:43 Fomo BUY
13:00 Fomo Thesis
13:12 X Post
```

이 timeline이 자동 생성되어야 한다.

---

# 6. Fomo Collector

Fomo 데이터 source를 조사하고 adapter 형태로 구현한다.

interface 예시:

```text
FomoProvider

GetLeaderboard(period)
GetTrader(userID)
GetTraderTrades(userID)
GetTraderTheses(userID)
GetRecentEvents()
```

공식 API가 없다면 현재 접근 가능한 데이터 source를 확인한다.

비공식 API나 indexing service를 사용할 경우:

- 실제 endpoint
- response schema
- limitation
- authentication requirement
- rate limit
- historical completeness

를 `docs/data-sources.md`에 기록한다.

Fomo provider가 변경되어도 분석 코드가 영향을 받지 않도록 provider interface를 분리한다.

---

# 7. Prospective Collection

온체인 transaction은 나중에도 복원할 수 있지만 leaderboard/call/post는 사라지거나 변경될 수 있다.

따라서 우선적으로 지속 저장 가능한 collector를 만든다.

최소 수집:

```text
Leaderboard Snapshot
Fomo BUY
Fomo SELL
Fomo THESIS
```

polling interval은 config로 관리한다.

예:

```text
leaderboard_interval = 1h
event_interval = 1~5m
```

실제 API 제한에 맞게 조절한다.

Collector는 반드시:

- idempotent
- retry-safe
- duplicate-safe

해야 한다.

---

# 8. Trader Wallet Resolution

Fomo가 표시하는 token / timestamp / amount / side와 온체인 transaction을 비교해 실제 wallet을 검증한다.

Matching key:

```text
chain
token_address
side
timestamp ± tolerance
amount ± tolerance
```

High confidence 조건 예시:

```text
서로 다른 Fomo 거래 2건 이상이
동일 wallet의 온체인 거래와 일치
```

또는 tx hash/signature가 직접 존재하는 경우.

한 건만 일치한 wallet을 확정하지 않는다.

wallet resolution 결과는 다음처럼 저장한다.

```text
wallet
chain
confidence
matched_event_count
evidence
```

---

# 9. EVM Data Source

초기 지원 후보:

```text
Base
BNB Chain
Ethereum
```

실제 scope는 repository와 Fomo Top Trader activity를 확인하고 좁힌다.

최소 RPC:

```text
eth_getTransactionByHash
eth_getTransactionReceipt
eth_getLogs
eth_getBlockByNumber
```

복잡한 router/aggregator 거래가 필요하면:

```text
debug_traceTransaction
```

지원 여부를 provider별로 확인한다.

Indexer/API 후보:

```text
Etherscan V2
Blockscout
Alchemy
QuickNode
기타 실제 사용할 수 있는 provider
```

Indexer는 discovery에 사용하고 최종 중요한 transaction은 raw RPC/log/receipt로 검증할 수 있게 한다.

---

# 10. Solana Data Source

필요 RPC:

```text
getSignaturesForAddress
getTransaction
getTokenAccountsByOwner
```

parse 시 확인:

```text
instructions
innerInstructions

preTokenBalances
postTokenBalances

program IDs
SPL transfers
```

Indexer 후보:

```text
Helius
QuickNode
```

가능하면:

```text
Indexer → discovery
Raw Solana RPC → verification
```

구조로 만든다.

---

# 11. Transaction Semantic Normalization

EVM과 Solana의 transaction 구조가 달라도 최종 분석에서는 같은 형태로 출력되게 한다.

공통 모델:

```text
EconomicAction {
    chain
    wallet
    timestamp

    action_type

    token_in
    amount_in

    token_out
    amount_out

    execution_price

    protocol

    tx_id
}
```

초기 지원 action:

```text
SWAP
TRANSFER
UNKNOWN
```

처음부터 lending/LP/perp까지 전부 지원하지 않는다.

현재 연구에서 가장 중요한 것은 `실제 BUY/SELL 시점`이므로 SWAP 정확도를 우선한다.

---

# 12. Trader Wallet Backfill

wallet이 검증되면 해당 wallet의 최근 30~90일 데이터를 가져온다.

최소:

```text
모든 DEX swap
token transfer
native funding
stablecoin funding
```

이번 Phase에서는 funding graph 전체 분석까지 하지 않는다.

다만 추후 분석을 위해 raw transfer는 보존한다.

Trading history에서 생성할 데이터:

```text
wallet
token
side
timestamp
amount
execution_price
tx
dex
```

---

# 13. Trader Timeline 생성

이번 Phase의 핵심 산출물이다.

Trader × Token별로 자동 생성:

```text
Trader A / Token X

12:43  ONCHAIN BUY   $31,000
12:44  FOMO BUY
12:57  FOMO CALL
13:11  X POST
14:38  ONCHAIN SELL  $17,000
```

결과 테이블:

```text
trader
token

onchain_first_buy
fomo_buy
fomo_call
x_post

onchain_first_sell

buy_to_call_seconds
buy_to_x_seconds
```

X 데이터가 이번 Phase에서 바로 구현하기 어렵다면 adapter/interface를 먼저 만들고 optional source로 둔다.

---

# 14. Phase 1에서 아직 하지 말 것

다음 기능은 구현하지 않거나 placeholder만 둔다.

```text
전체 Top 100 deep indexing
2-hop / 3-hop wallet graph
동일인 판정
CEX deposit clustering
Lead-Lag 통계
linked wallet PnL
ML clustering
insider detection
```

Phase 1 목적은 **연구 기반 데이터셋을 신뢰성 있게 만드는 것**이다.

---

# 15. Phase 1 성공 기준

최소 다음 결과가 나와야 한다.

## A. Trader Registry

```text
Top 50 leaderboard snapshot 저장
```

## B. Fomo Event Dataset

```text
BUY / SELL / THESIS event 저장
```

## C. Wallet Resolution

최소 3~5명의 trader에 대해 실제 wallet을 높은 confidence로 검증.

## D. Historical Backfill

해당 trader의 최근 30~60일 swap history 복원.

## E. Timeline

최소 다음 표를 자동 생성.

```text
Trader
Token
On-chain Buy
Fomo Buy
Fomo Call
On-chain Sell
```

가능하면 X post 추가.

---

# 16. 첫 번째 분석 결과

연관 wallet 분석 전에 다음 baseline 결과부터 만든다.

Trader별:

```text
Total Fomo Calls
Total On-chain Buys

Call-backed Buy Count

Median Buy → Fomo Call Delay
Median Buy → X Delay

Median Position Size at Call

Median Hold Time
```

예:

```text
Trader A

Calls                 27
On-chain buys        183
Call-backed buys      24

Median Buy→Call      18m
Median Buy→X         41m
```

이 결과가 자동 생성되어야 한다.

---

# 17. Storage

현재 repository에 DB가 없다면 MVP는 과도한 인프라를 만들지 않는다.

권장:

```text
SQLite or DuckDB
+
Parquet
```

중 현재 프로젝트와 맞는 것을 선택한다.

Raw JSON은 별도로 보존한다.

추후 데이터 규모가 커지면 PostgreSQL/ClickHouse 등으로 교체 가능하도록 repository layer를 분리한다.

---

# 18. Directory Structure

기존 repository convention이 없다면 다음 형태를 참고한다.

```text
src/
├── providers/
│   ├── fomo/
│   ├── x/
│   ├── evm/
│   └── solana/
│
├── collectors/
│   ├── leaderboard/
│   ├── fomo_events/
│   └── onchain/
│
├── resolution/
│   └── trader_wallet/
│
├── semantics/
│   └── swaps/
│
├── normalization/
│
├── research/
│   └── timelines/
│
├── storage/
│
└── cli/

data/
├── raw/
├── normalized/
└── research/

docs/
├── research-plan.md
├── data-sources.md
├── schema.md
└── limitations.md
```

기존 repository 구조가 있다면 새 구조를 강제하지 말고 통합한다.

---

# 19. CLI

최소 다음 작업을 독립적으로 실행 가능하게 한다.

예:

```text
collect-leaderboard
collect-fomo-events

resolve-wallet --trader <id>

backfill-wallet --wallet <address> --days 60

build-timeline --trader <id>

report-baseline
```

실제 언어/CLI framework는 현재 repository에 맞춘다.

---

# 20. 테스트

최소 테스트:

```text
Fomo API response parsing
duplicate event 처리
wallet matching
EVM swap parsing
Solana swap parsing
timeline ordering
timestamp normalization
```

모든 timestamp는 내부적으로 UTC로 저장한다.

display에서만 timezone을 변환한다.

---

# 21. Documentation

구현 후 반드시 다음 문서를 작성한다.

## docs/research-plan.md

- 연구 질문
- Event-first 전략
- Phase 구분

## docs/data-sources.md

각 API/RPC에 대해:

```text
provider
endpoint
fields
authentication
rate limit
historical availability
known limitations
```

## docs/schema.md

실제 저장되는 entity 설명.

## docs/limitations.md

특히:

```text
Fomo historical completeness
wallet resolution false positive
transfer vs buy
ticker ambiguity
timestamp accuracy
```

를 작성한다.

---

# 22. 작업 방식

한 번에 전부 구현하지 않는다.

다음 순서로 진행한다.

## Step 1

Repository 분석 + 데이터 source 조사 + implementation plan 작성.

아직 대규모 구현하지 않는다.

결과:

```text
docs/implementation-plan.md
```

## Step 2

Fomo leaderboard / event collector 구현.

테스트 데이터 확보.

## Step 3

한 명의 Trader를 end-to-end로 처리한다.

```text
Fomo Event
→ Wallet Resolution
→ On-chain Trade
→ Timeline
```

## Step 4

3~5명으로 확대.

## Step 5

Top 10~20 backfill.

## Step 6

Baseline report 생성.

---

# 23. Agent가 첫 작업 후 보고해야 할 내용

첫 iteration이 끝나면 다음 형식으로 보고한다.

```text
1. 현재 repository 구조

2. 실제 사용 가능한 Fomo 데이터 source

3. Fomo에서 확보 가능한 필드

4. 확보하기 어려운 필드

5. EVM/Solana provider 선택

6. 제안 schema

7. 구현한 파일 목록

8. 실제 수집 성공한 샘플

9. 현재 blocker

10. 다음 iteration에서 할 일
```

가능한 경우 실제 Trader 1명에 대해:

```text
Fomo Event
↓
Matched On-chain Tx
↓
Resolved Wallet
↓
Timeline
```

샘플까지 제시한다.

---

# 최종 목표

이번 작업의 완료 기준은 linked wallet을 찾아내는 것이 아니다.

**Fomo Top Trader의 공개 활동과 실제 온체인 행동을 신뢰성 있게 동일 timeline 위에 올리는 것**이 이번 Phase의 목표다.

최종적으로 다음과 같은 데이터가 자동 생성되면 성공이다.

```text
Trader A / Token X

12:42:18  On-chain BUY
12:42:25  Fomo BUY
13:01:14  Fomo CALL
13:12:42  X POST
14:05:31  On-chain SELL
```

이 기반이 완성된 이후 다음 Phase에서:

```text
Funding Graph
→ Linked Wallet
→ Pre-Trading
→ Lead-Lag
→ PnL
```

분석을 진행한다.

---

# 이전 운영 계획 보충 — 2026-10-06 Dune 검토

Fomo leaderboard와 BUY/SELL/THESIS 이벤트는 Fomo API에서 직접 수집한다. 우선 검증된 지갑의 기존 Solana history에서 Fomo 이벤트 token과 같은 token의 swap/transfer timeline을 대조한다. 특정 transaction signature 확인과 보존 범위 보완에는 RPC/indexed provider를 쓴다. 당시 시장 전체의 과거 DEX scan은 Dune 실행 권한을 확인한 뒤 제한된 POC로 수행하는 안을 검토했다. 현재 수집 경로와 구현 순서는 아래 확정 BigQuery API/CLI 절을 따른다.

Dune은 query result를 JSON 또는 CSV로 API에서 회수할 수 있다. Dune이 연구 DB에 직접 쓰는 것은 아니므로 collector가 결과와 query/execution provenance를 SQLite에 적재한다. SQLite를 canonical dataset으로 유지하고 CSV는 선택적 export로 취급한다. Dune execution results는 90일 뒤 만료되므로 필요한 결과를 로컬에 보존한다.

Dune curated DEX table은 모든 wallet activity와 동의어가 아니다. 특히 transfer, 실패 transaction, non-DEX 동작은 별도 source로 검증한다. 현재 Dune MCP는 visitor/read-only로 public cached results만 읽을 수 있고 credits/quota는 0이다. 따라서 fresh query execution은 보류한다. 당시 검토한 Dune POC는 채택하지 않았으며 현재는 BigQuery의 한 검증 지갑 파일럿을 진행한다. Dune API key를 새로 설정하는 경우에도 `DUNE_API_KEY` 환경변수만 사용하고 저장소에는 기록하지 않는다.


# 운영 계획 변경 — 2026-10-06 Etherscan tracing pilot

사용자는 추적 파일럿을 먼저 진행하고 Etherscan 스킬을 사용하도록 요청했다. 기존 Phase 1의 graph 보류 규칙에 대한 예외를 rank 9의 이미 검증된 Ethereum 지갑, 고정된 최근 30일, 최대 2-hop으로 한정한다. 다른 trader나 전체 체인 graph로 확장하지 않는다. Phase 1 전체 완료 또는 동일인 판정을 선언하는 변경이 아니다.

Dune은 현재 실행 권한이 확인되지 않아 사용자 요청에 따라 이번 경로에서 제외한다. Fomo REST와 SQLite 운영은 유지하고, Etherscan CLI/API의 응답 및 요청 이력과 receipt-log 전송을 SQLite에 보존한다. 결과와 가설, CEX 라벨의 한계, pagination의 미완료 범위는 Etherscan Flow case JSON 안에 기록한다. 반복 송금이나 같은 금액은 소유자의 동일성, CEX 매도, acquisition cost 또는 PnL을 확정하지 않는다.


# 운영 계획 변경 — 2026-10-06 Bridge API 연계

사용자가 실행 중인 로컬 Bridge aggregator API를 제공하고 반복되는 RelayDepository 입금을 크로스체인으로 연결하도록 요청했다. 기존 rank-9 Ethereum tracing pilot의 실제 입금 거래에 대응하는 목적지 체인·거래·수취인·토큰 전송까지 조회 범위를 확장한다. 다른 trader, 전체 체인 backfill, 동일인 판정 또는 PnL 완료를 의미하지 않는다.

소스 tx hash만으로 batch 안의 모든 주문을 trader에게 귀속하지 않는다. 기존 성공 receipt의 sender·수신 계약·토큰 계약·raw amount·log index·block hash를 확인하고 provider의 실제 input leg와 일치하는 주문만 연결한다. Solana 목적지는 원본 성공 transaction, SPL mint, token account의 historical owner, 실제 instruction amount와 balance delta를 대조한다. 소스 deposit ID 및 Relay operation ID와 목적지 memo가 함께 일치할 때 `order_correlated`로 분류한다. Provider status, API canonical evidence, 직접 RPC 근거를 분리해서 SQLite에 보존한다.

이번 8개 Ethereum 입금 중 7개가 기존 verified RZD Solana 지갑으로 연결됐다. 나머지 1건은 API가 batch 안의 다른 사용자 주문만 반환해 unresolved다. 새 수취인의 trader 소유권 또는 CEX 입금을 추정하지 않는다. 목적지 7건은 기존 Solana EOA 기반 normalized history에 없었고, 실제 token-account owner로만 확인됐다. 이후 inventory/PnL 전에 bridge receipt ledger를 포함해 chain/signature/wallet 기준으로 중복 없이 합친다. 정밀 결과와 누락 사유는 SQLite와 `data/research/rank9-bridge-evidence.json`에서 조회한다.


# 현재 확정 운영 방식 — 2026-10-06 BigQuery API/CLI

사용자는 기존 Google Cloud 인증으로 BigQuery를 API/CLI 방식으로 쓰고, 이 방식을 문서에 확정하도록 요청했다. 본 절은 공급원 선택과 다음 작업 순서에서 이전 Dune 검토 계획보다 우선한다. 초기 event-first·Top 10 cohort·wallet 검증·timestamp 분리·transfer/swap 구분 원칙은 유지한다.

- **Fomo REST:** account/leaderboard 및 BUY/SELL/THESIS source timestamp를 기존 checkpoint 방식으로 수집한다.
- **BigQuery API/CLI:** 과거 token/native transfer, Solana token-account owner 활동, 기존 자금 관계 후보와 thesis token의 event-window 거래 후보를 검색한다. Query project는 `exchange-labs`; 우선 인증된 `bq`를 재사용한다. MCP는 현재 필수 경로로 두지 않는다.
- **RPC/Etherscan + Bridge API:** 중요한 거래의 성공·quote·fee·swap 의미와 개별 cross-chain deposit/order/destination 대응을 검증한다.
- **SQLite/Python:** 원본 결과와 provenance, normalized action, timeline, inventory lots 및 검증된 PnL 입력을 기준 데이터로 저장하고 재계산한다. CSV는 export다.

RZD rank-9의 verified Ethereum 지갑을 `2026-09-06T07:46:11Z <= timestamp < 2026-10-06T07:46:11Z`로 조회하는 reusable collector와 SQLite importer를 구현·실행했다. Dry run → 40 GiB cap → job 실행 → 전체 34행/2페이지 → 원본/SQL/job provenance 저장을 완료했고 기존 ERC-20 log 34/34 및 real-USDC Relay deposit 8/8 모두 일치했다. Ethereum의 contract-mediated 활동을 outer sender만으로 누락시키지 않는다.

같은 RZD의 known Solana bridge signature 7개와 30일 historical owner 활동의 대조·보완을 완료했다. 다음은 이미 보존한 funder의 같은-chain·같은-token event window다. 이미 발견한 funder에 대해 최대 2-hop 및 same-token call 전후 후보 검색을 진행한다. 다른 verified Top 10 지갑은 첫 공급원/coverage 파일럿 이후 같은 기간의 batch query로 확대한다. 새로운 체인은 실제 Fomo event나 검증된 bridge leg가 있을 때 추가한다. Transfer 관계만으로 뒷지갑 소유권이나 CEX endpoint를 확정하지 않는다.

모든 조회는 SQL/hash/version, parameter, project/dataset/location, UTC 범위, job ID, 원본 page, row count, 실제 processed/billed bytes와 completeness를 보존한다. 전체 결과 회수 여부와 chain history coverage는 구분한다. Token amount는 정확한 문자열/정수로 유지한다. 결과를 저장해 반복 분석에서 cloud 전체 history를 다시 스캔하지 않는다.

사용자가 보고한 크레딧은 약 40만원이다. 작업 묶음당 예상 5만원 이상을 큰 비용의 임시 알림 기준으로 둔다. 이는 사용자 지정 한도가 아니라 agent의 운영 가정이다. Routine query에는 dry run/최대 조회량을 적용한다. 큰 작업이나 예정 작업이 보고된 잔여 예산을 소비할 때 알린다. 실제 청구 단가·잔액은 별도로 확인한다.

현재 완료된 BigQuery 작업은 초기 metadata/SQL/JSON·block 최신성·비용 추정·Solana bridge 1건 검증과 Ethereum 30일 ERC-20 collector/importer 실행이다. Ethereum 결과는 기존 log 34/34, bridge deposit 8/8과 event/log index까지 일치했고 SQLite collection/page/transfer는 1/2/34행이다. Solana owner/receipt/event slice도 완료됐으며 최신 수치와 선행매수 결과는 아래 append 및 owner review를 따른다. 이번 결과는 indexed ERC-20 query 전체 회수이며 모든 온체인 활동 coverage나 PnL 완료를 뜻하지 않는다. 실제 다음 단계와 상태는 [implementation-plan.md](implementation-plan.md)의 상단 절을 따른다. Dune은 현재 수집 경로에서 제외한다.

## Solana owner 및 event-timeline 완료 — 2026-10-06 UTC

RZD Solana owner 파일럿도 완료했다. 같은 고정 30일 구간에서 known bridge 수령 7/7의 성공·slot·시각·USDC mint/owner/raw delta가 BigQuery와 RPC에 일치했다. BigQuery owner 11,763행 중 실제 token 잔액 변동은 11,575행이며 모두 full RPC와 일치했다. QuickNode `tokenAccounts=balanceChanged`로 13페이지/11,580개 원문을 회수했고, 기존 EOA history에 없던 11,000개 활동을 SQLite에 중복 없이 합쳤다. Fomo 18개 event의 24시간 전후 window도 저장했다. `SwapTob`/`SwapEvent` 등 로그 이름을 인식하도록 수정한 `solana-heuristic-v3`에서 RZD는 SWAP 1,144 / TRANSFER 318 / UNKNOWN 11,138행이다. Known bridge 7건은 기존 직접 SPL/order 증거로 TRANSFER이며 매수나 수익으로 처리하지 않는다. 새 11,000개 활동에서 추가 SWAP은 0개이고, 기존 RZD 358개 label은 실제 swap 로그와 opposing balances에 따라 교정됐다. 다른 세 검증 지갑도 보존 데이터만 재분류했으며 신규 history는 수집하지 않았다.

Solana BigQuery는 collection/page/source row 3/38/23,533행(행 역할 간 signature 중복을 포함), raw CLI capture 67건이다. Query별 exact SQL/version/hash/parameters, job/bytes와 페이지 provenance가 있고 complete saved capture는 cloud 재실행 없이 import한다. Billed bytes는 12,067,997,220,864(약 10.976TiB), reference $6.25/TiB에서 $68.60이며 실제 invoice/credit balance는 미확인이다. 큰 예상 비용을 사용자에게 알린 뒤 cap을 적용했다. Account/native/log 전체 projection의 24.554TiB dry run은 실행하지 않았다. QuickNode 13호출은 문서 단가 기준 1,560 credits 추정이고 잔액은 unknown이다.

다음 범위는 이미 보존한 Ethereum funder 후보의 같은 chain·같은 Fomo token에 대한 BUY/THESIS 전후 활동이다. 최대 2-hop과 ownership unknown을 유지한다. Solana 추가 wallet 수집은 먼저 `tokenAccounts=balanceChanged` full pages를 사용하고, BigQuery는 historical owner 및 known gap/토큰·시간 window 대조에 필요한 범위를 dry run으로 결정한다. 이번 full owner scan이나 기본 EOA-only history를 다시 반복하지 않는다. Quote/fee/이전 재고/exit·transfer 원가를 검증한 뒤 inventory와 PnL로 넘어간다. 상세 결과는 `docs/rank9-solana-owner-review.md`와 ignored `data/research/rank9-solana-owner-analysis.json`에 있다.

주요 발견: SAPLING은 Fomo BUY 1초 뒤·THESIS 29초 전에 첫 관측 매수됐다. HAMSTER는 첫 THESIS 이전 24시간에 7개 매수·2개 매도를 이미 실행했고 최신 매수는 13시간 1분 32초 앞선다. 이는 같은 verified main wallet의 관측이며 뒷지갑 판정이나 PnL 완료가 아니다. 이전 HAMSTER TRANSFER-only 결과는 swap instruction 이름을 누락한 V1 분류였고 V3 결과로 교정한다.
