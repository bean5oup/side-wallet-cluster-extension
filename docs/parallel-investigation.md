# Top100 · 시총 100만 달러 이하 병렬 조사 운영 계획

## 최신 실행 범위 — 초기 지정 10명 집중

사용자의 최신 지시에 따라 raw141의 초기 Top10 계정에 집중한다. 현재 순위 또는 Top100 첫 캡처 10명으로 바꾸지 않는다. **10명 과거 기록·실제 BUY·$1M 시총 선별 → 적격 토큰 1~3개 선행 매수/처분/자금 회수 추적 → 10명·토큰 사이의 반복 연결 비교**가 다음 우선순위다. 60일 구간, THESIS 없는 BUY와 Luna5개/max 설정은 유지한다. [상세 계획·원래 명단](top10-investigation-priorities.md), [focus 설정](top10-investigation-focus.json)을 우선한다.

아래 Top100 표본과 실행 결과는 보존된 이전 기록이다. 이전 다음10명 확대 queue는 이 계획으로 대체하며 새 수집을 자동 시작하지 않는다. 기존 Top100 helper의 raw1654/100명 검사가 새 focus를 자동 강제하지는 않는다. 외부 요청 전에 raw141의 명시적 ID에 맞는 capture/적재 경로와 새 예산 예약을 준비한다.

정책 버전: `top100-lowcap-1m-v2`. 갱신: 2026-10-07 KST.

## 1. 목적과 현재 상태

Fomo 상위 계정의 공개 기록과 실제 거래를 연결하고, **THESIS/CALL 게시 또는 BUY 당시 유통 시총100만 달러 이하 토큰**에서 초기 매수 군집·공개 이후 매도·공통 자금 회수를 조사한다. 군집이 Fomo 계정과 실제로 연결되는지, 동일한 고객 CEX 입금 주소로 회수하는지, 거래 근거가 충분한 경우에 한해 수익을 계산한다.

첫 batch를 실행·검토했다. 작업자5개가 기존 Top100을 확인하고 각 구간2명씩 총10명 새 캡처를 검토했다. [한글 결과·100명 진행표](top100-first-batch-review.md), review raw2096과 state `top100_parallel_foundation_v1`을 따른다. 정책 JSON은 새 `parallel_foundation.py`가 읽어 고정 cohort/기간과 root Fomo 예산을 확인한다. 모든 기존 provider/CLI를 전역 강제하는 기능은 아직 없으며, 다른 source는 사전 예약이 필요하다.

후속 [BUY 첫 검토](buy-first-batch-review.md)는7명·9토큰·26개 BUY 원문을 같은5개 작업자가 분석한 별도 배치다. 최신 review raw2140/통합 목록 raw2141, state `top100_buy_anchor_review_v2`와 `top100_lowcap_event_inventory_v2`를 우선한다. 실제 검증 BUY3건·후보 BSC 전달2건을 분리했으며 신규 심층 적격0이다. 단순 알림을 distinct fill로 계산하지 않는다. 캡처/적재를 완료한 배치이지60일 시장 분석 완료가 아니다.

## 2. 표본과 토큰 선별

- 기본 leaderboard는30d. DB의 `raw_payload_id=1654`, snapshot `2026-10-07T00:29:19.532Z`를 고정한다.100개의 서로 다른 사용자와1–100위가 저장돼 있다. All-time raw1655를 합치거나 최신 순위로 작업 중 사용자를 바꾸지 않는다. 이 표본은 현재 상위 계정 표본이며 두 달 전체의 모든 상위 계정을 대표한다고 주장하지 않는다.
- 과거 수집·분석 목표는 **정확히60일**이다. `lookback_days=60`/5,184,000초이며 `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z`로 고정한다. 시작은 종료 시각에서60일을 뺀 값이다. 모든 작업자가 같은 start/end를 상속하고 배치마다 now를 새로 계산해 구간을 이동시키지 않는다. 이후 활동은 별도 incremental 작업이다.30d는 순위 산정 기간이고60일은 과거 이력 기간이다.
- Token identity는 정확한 chain ID와 contract/mint다. 같은 이름·심볼·다른 체인의 같은 hex 주소를 같은 토큰으로 병합하지 않는다.
- 적격 여부는 token 자체에 영구 부여하지 않고 **token × 기준 event(THESIS/CALL/BUY)**로 판정한다. 같은 토큰도 앞선 CALL에서는≤$1M이고 뒤의 CALL에서는>$1M일 수 있다.

| 상태 | 조건 | 다음 작업 |
|---|---|---|
| `eligible` | 기준 이벤트 당시 유통 시총이 출처와 표본 시각을 갖추고 USD≤1,000,000; BUY는 실제 swap·owner·매수 시각 검토도 필요 | 매수 군집·exit·연결 분석 |
| `excluded_above_cap` | 같은 기준 시총>1,000,000 | 선별 근거만 보존 |
| `pending_cap` | 역사적 유통 시총이 없음 | 시총 근거 보완 |
| `pending_cap_proxy` | FDV·총발행량 평가액·현재 시총만 있음 | 유통 시총 근거 보완 |
| `pending_source` | 계약·시각·가격 등 출처 자체가 불확실함 | 원문·source gap 확인 |

100만 달러는 포함한다. 시총 구간은 `<30k`, `30k–<200k`, `200k–1M 이하`다. 시총 미확인을0으로 대체하지 않는다. 현재 가격이나 현재 발행량으로 과거 시총을 계산하지 않는다. 역사적 가격×검증된 역사적 **유통량**을 사용했다면 각 시점·원문·계산 근거를 함께 보존한다. 총발행량과 유통량은 구분한다.

THESIS/CALL은 게시 시각, BUY는 검토된 실제 매수 시각 직전의 적합한 역사적 표본을 사용하고 표본 시각·차이·해상도를 기록한다. 현재 운영 가정은 최대5분 차이다. CALL이 포함된 미완료 분봉·게시 후 자료를 게시 전 표본으로 쓰지 않는다. 표본의 불확실성 때문에 $1M 경계를 판단하기 어렵다면 보류한다. Provider market cap 자체도 assertion이며 정확한 순간값을 RPC가 검증한 것처럼 표시하지 않는다.

Top100의 기초 Fomo 원문에 대상 밖 토큰이 포함될 수 있다. 이는 선별용 원문 보존이며 심층 온체인 조사 대상은 적격 event만이다. Quote·gas·bridge·CEX 자금 이동의 USDC/ETH/BNB/SOL은 연결 증거 자산으로 쓰며 저시총 대상 토큰과 구분한다.

기존 raw2067의 $10M 선별은 과거 기록이다. CZ의 약$844,583.53은 FDV 대용치뿐이므로 현 기준에서 `pending_cap_proxy`다. 기존 두 매수 receipt는 보존하고 시총 근거가 충족되기 전 신규 전체 매수 군집 수집을 배정하지 않는다. 새 기준의 재선별 결과는 버전을 추가하고 이전 row를 덮어쓰지 않는다.

본체는 고정 표본을 다음 읽기 전용 조회로 배정할 수 있다. 결과100행·서로 다른 사용자100명과1–100위가 맞는지 확인하고 manifest에 사용자 ID를 저장한다.

```sql
SELECT rank, fomo_user_id
FROM leaderboard_snapshots
WHERE raw_payload_id = 1654 AND period = '30d'
  AND rank BETWEEN 1 AND 100
ORDER BY rank;
```

## 3. 분업과 작업 큐

| 담당 | 초기 계정 범위 | 역할 |
|---|---|---|
| Luna 1 |1–20위| 기초 수집·정규화, 이후 배정된 token 작업 |
| Luna 2 |21–40위| 동일 |
| Luna 3 |41–60위| 동일 |
| Luna 4 |61–80위| 동일 |
| Luna 5 |81–100위| 동일 |
| 본체 |전체| 고정 표본·배정·예산·SQLite 적재·근거 검토·최종 판단 |

작업자 5개 모두 모델은 `gpt-6-luna`, 추론 수준은 `max`다. 본체는 현재 모델·추론 설정을 유지한다. `spawn_agent` 생성 도구에는 `model="gpt-6-luna"`, `reasoning_effort="max"`, `fork_turns="none"`과 해당 역할 지시·작업 명세를 명시적으로 전달한다. 문서나 작업 명세의 설정만으로 실제 생성 옵션이 자동 적용되는 것은 아니다. 전체 대화와 모든 raw를 반복 전달하지 않는다. 작업자가 새 작업자를 생성하지 않는다.

순위 구간은 초기 책임 범위다. 거래량에 따라 작업을 작은 단위로 나누며 먼저 끝난 작업자에게 미처리 항목을 재배정한다. 한 작업에는 명시적 사용자 ID 또는 token/window 목록, 사용할 근거, 허용 경로, 예약 예산, 산출물을 넣는다.

작업 식별자는 cohort raw ID·단계·user ID 또는 chain/token·UTC 구간·분석 버전으로 정한다. 본체가 `queued → assigned → collected/analyzed → reviewed → ingested`를 관리한다. `deferred`와 `failed`는 원인·남은 cursor·다음 frontier를 보존한다. Raw 수집 성공, 분석 완료, 검토 완료를 같은 상태로 표시하지 않는다.

### A. 계정별 기초 자료

**수집 기간은60일**이다. Fomo 과거 글/THESIS/CALL/BUY/SELL에는 고정 start/end를 적용한다. 날짜 필터가 없는 과거 글 route는 받은 원문을 보존하고 source 게시 시각으로 구간을 선별한다. 적격 토큰 관련 검증 지갑의 매수·매도·전송 backfill에도 같은60일 목표를 적용한다.

- Stable user ID, handle, 정확한 chain별 지갑 후보·기존 검증 상태를 정리한다.
- REST `/v2/alerts`의 BUY/SELL/THESIS와 `/v2/thesis/user/{id}`의 과거 원문을 수집한다. 삭제·수정·이전 게시글의 미확보 가능성을 기록한다.
- 사용자별 raw·source ID·semantic document key·게시 UTC·trade ID·token·coverage를 보존한다. 공급자 cursor/hasMore가 없거나 upstream unavailable이면 60일 history를 complete로 표시하지 않는다.
- 고시총 토큰과 미확인 cap은 심층 작업 큐로 넘기지 않는다. Chain별 지갑 검증은 기존2개 distinct event/성공 tx 및 signer·swap·quote 기준을 유지한다. 후보 주소가 반환됐다는 이유로 verified로 승격하지 않는다.

### B. 토큰별 실제 매수·매도

본체가 유통 시총 근거를 검토한 뒤 적격 token/event만 배정한다. 같은 토큰의 겹치는 시간 창은 한 capture로 회수하고 여러 trader/event와 관계를 연결한다. 겹침 밖의 새 구간만 추가 수집한다.

토큰 시장의 초기 탐색 창은 우선 분석할 slice이며 계정/적격 토큰의60일 backfill을 대체하지 않는다. 첫 탐색은 적격 THESIS/CALL의 게시 시각 또는 적격 BUY의 검토된 실제 매수 시각 전2시간부터 후1시간을 기본 후보 창으로 둔다. THESIS 없는 BUY도 제외하지 않는다. BUY-only의 짧은 선행 창은10/30/60초와5/15분이며, anchor 이전 실제 매수와 확인된 노출 이후 추종 매수를 별도로 비교한다. 확보한 최초 공개 기록이 이보다 앞서면 시점 비교를 별도로 보존하고, 필요한 이전 구간은 본체가 추가 작업으로 배정한다. Token launch가 창에 들어가면 launch부터 확인하고, launch가 더 오래전이면 필요한 초기 구간을 별도 작업으로 배정한다. Exit는 기준 이벤트 후24시간을 초기 관찰 창으로 두되 고정 조사 종료를 넘지 않는다. 이 창 크기는 운영 가정이며 작업 명세에 정확한 UTC를 적고, 후보의 실제 회수 근거에 따라 추가 구간을 배정한다. 이 범위를 token의 lifetime 전체 거래라고 표현하지 않는다.

발견된 관련 풀·이전 풀·migration을 구분한다. 현재 유동성이 가장 큰 풀 한 개를 전체 시장으로 간주하지 않는다. 검증된 실제 swap과 최종 recipient/owner를 추출하고 multi-hop 중간 mint·router·aggregator leg를 별도의 최종 매수로 중복 계산하지 않는다.

매수 군집은 같은 블록 및10/30/60초 창을 비교한다. 예를 들어60초 내3주소 이상은 **탐색용 가정**이며 유의성·공모 판정이 아니다. 거래 강도·토큰 나이·유동성이 비슷한 대조 구간과 비교하고 bot/sniper·MEV·프로토콜 계정 및 timestamp 해상도를 표시한다. 같은 시간에 샀다는 사실과 실제 주소 간 연결을 별도로 제출한다.

### C. 자금 연결과 회수

후보의 비서비스 공통 공급, token 반환, repeated 회수, Fomo verified wallet 또는 검증된 연결 edge와의 접점을 조사한다. 관련 token/window의 실제 거래 근거를 따라 작업 명세에 있는 분기만 확장한다. 전체 shared service의 입출금을 따라가지 않는다.

Bridge는 source deposit/order ID/input/destination을 대응시키고 양쪽 chain의 성공·asset·raw amount·owner/delta를 검증한다. Provider assertion과 직접 근거를 별도 참조로 저장한다.

CEX는 `(chain_id, 정확한 recipient 주소)`를 비교한다. 서비스명이 같거나 shared hotwallet으로 모이는 것만으로 공통 고객이라 판단하지 않는다. Deposit 역할의 라벨 출처·관측 시각·고객 전용 여부의 확인 상태와 실제 전송 proof를 분리한다. 거래소 입금 주소가 달라 공통점이 없더라도 뒷지갑 부재로 판정하지 않는다.

### D. 본체 검토

본체는 [검토 지시서](../agents/reviewer.md)에 따라 시간 관계, 실제 매수/매도, shared service, 반복성, 동일 deposit 및 PnL을 검토한다. 작업자는 근거와 후보 해석을 제출하며 최종 동일인·조종·의도·수익 판정은 하지 않는다.

## 4. 시각과 수익

`onchain_buy_at`, `fomo_buy_at`, `thesis_at`, `call_at`, `x_post_at`, `onchain_sell_at`, `captured_at`을 각각 보존한다. `earliest_observed_public_at`은 확보한 공개 기록의 최소값이며 `absolute_first_public_status`는 completeness 근거 없이는unknown이다. Fomo BUY가 먼저 공개됐다면 THESIS 이전 매수를 모든 공개 이전 매수라고 부르지 않는다. 같은 초의 거래와 글은 순서가 불명확할 수 있다.

PnL은 실제 취득 원가·quote·fee·exit와 이전 재고/반환 lot을 확인한 경우에만 계산한다. Partial sale과 transferred lot의 원가 미확인을 표시한다. Token을 반환하거나 bridge한 일을 매도로, 환산 USD 값이나 Fomo position value를 매도 수령액으로 쓰지 않는다. LLM 계산 대신 정확한 정수·Decimal 및 저장된 코드/SQL 계산을 사용한다.

## 5. 저장·중복·근거 형식

작업자는 기준 SQLite를 읽기 전용으로 사용한다. 담당 작업 외의 문서·코드·state를 수정하지 않는다.

- Raw: `data/raw/parallel/<batch_id>/<task_id>/`.
- 작업 명세·결과: `data/research/parallel/<batch_id>/<task_id>/`.
- 본체 배정/예산 장부: `data/research/parallel/<batch_id>/manifest.json`.
- 최종 기준: `data/research/fomo.sqlite3`에 본체만 추가 적재.

작업자는 `result.json`, 정확한 정규화 후보 `normalized.jsonl`, 한글 `report.md`, 필요한 credential-free raw를 제출한다. 이 파일은 적재 준비 자료이며 CSV 대체 연구 DB가 아니다. 기존 importer가 지원하는 항목은 본체가 검토 후 적재한다. 새 result 구조는 기존 table이 존재한다고 가정하지 않고 우선 raw/검토 결과로 보존한다. 새로운 관계형 table이 필요하면 별도 additive schema 작업으로 기록한다.

모든 결과에는 `policy_version`, `batch_id`, `task_id`, cohort raw1654, 사용자/chain/token/window, source refs, evidence status, coverage, gaps, actual usage와 next frontier가 있어야 한다. Raw ref는 저장소의 raw ID와 locator 또는 작업자 파일 path/hash/locator를 사용한다. 작업자 임시 ID를 canonical DB ID로 가장하지 않으며 본체가 적재 후 대응표를 만든다.

정규화 identity는 chain+tx+log/instruction locator+asset+해당 wallet이다. 같은 거래가 여러 event/window에서 보인 경우 근거 관계는 여러 개일 수 있지만 거래와 수익을 여러 번 세지 않는다. Raw 정수량·decimals·gross/net·UTC·provider/RPC 근거는 별도다. 동일 identity의 내용이 다르면 덮어쓰지 말고 conflict로 제출한다.

새 기준의 screening은 threshold `1000000`과 새 version/source refs를 추가한다. 기존 raw2067 및 threshold10000000 row를 수정하지 않는다. Wallet ownership·resolution, 기존 RZD/연우 state와 native alert checkpoint는 작업자가 바꾸지 않는다.

## 6. 외부 요청·비용 운영

다음 값은 **새 Top100 계획 배치의 운영 가정**이다. 첫 배치에서는 Fomo20회/7,250credits와 시장자료7회를 사용했다. 다음 배치도 본체가 manifest와 예약을 만들고 같은 전역 상한을 지킨다. 계획 파일만으로 모든 API의 한도가 자동 적용되지 않는다.

| 자원 | 5개 작업자+본체 전체 배치 상한 |
|---|---:|
| Fomo HTTP 시도 |20회, 재시도·실패 포함 |
| Fomo 비용 |15,000 credits |
| 직접 RPC |30회, 재시도 포함 |
| Bridge resolve |5회, 재시도 포함 |
| Nodit indexed API |100회, 재시도 포함 |
| 시장 가격·시총 API |20회, provider 합계·재시도 포함 |

초기 계정 batch는10명×THESIS1페이지+alerts1페이지를 기본으로 한다.5개 작업자에게 각2명을 배정할 수 있다. 추가 페이지와 wallet resolution은 별도 예산 예약이 없으면 요청하지 않는다. 순위20명은 책임 범위이며 한 batch의 외부 요청 범위와 다르다. 알려진 페이지 단가 기준10명은13,750credits의 참고 예상이며 실제 비용은 응답 header로 기록한다. 초기100명 기초 수집 campaign은150,000credits 상한으로 계획한다. 실패나 더 많은 페이지 때문에 한도에 닿으면 미완료 frontier와 새 비용 예상을 기록한다. 단가와 잔액은 [기존 출처 관측](data-sources.md)을 확인하며 알려진 마지막 잔액을 현재 잔액으로 단정하지 않는다.

요청이 필요한 작업은 본체가 전역 상한에서 차감한 예약량을 작업 명세에 넣는다. 본체가 대신 호출하는 최소 운영도 가능하다. 각 작업자가 시작될 때 전체 한도를 새로 갖거나 새 프로세스로 초기화하지 않는다. 작업 종료 시 actual usage와 unused reservation을 반환하며 진행 중 예약을 다른 작업에 재배분하지 않는다. Shared API key별 순차 호출 또는 제한된 concurrency를 지키며429/503은 남은 예약량 안에서 최대1회 재시도한다. Retry가 부족하면 gap으로 반환한다.

BigQuery는 기존 `bq`/API, project `exchange-labs`를 사용한다. 쿼리마다 dry run과 명시적인 byte cap이 필요하다. 기본40GiB를 넘는 cap은 본체가 query/필요성/예상량을 작업 명세에 기록한다.5개 쿼리의 합산 예상량과 실제 processed/billed bytes를 관리한다. 기존 사용자 선호에 따라 작업 묶음 예상5만원 이상 또는 보고된 잔여 크레딧을 소비할 규모면 실행 전에 알린다. 실제 잔액·환율·free allowance가 미확인이라는 사실도 보존한다.

Fomo·Nodit·RPC key는 ignored `.env` 등 기존 설정에서만 읽는다. 인증 URL·cookie·key를 공유 작업 명세나 capture에 포함하지 않는다. Dune·WebSocket은 실행하지 않는다.

## 7. 실행 준비와 완료 기준

실행 준비:

1. 본체가 raw1654의100개 사용자 ID를 고정해 manifest와 작은 작업 명세에 넣는다.
2. 기존 Top10 제한과 latest-snapshot 선택 경로를 점검해 **고정 cohort의 명시적 ID**를 사용하는 수집·적재 경로를 마련한다. `collector.py`/`theses.py`가 문서만으로100명 지원으로 바뀌지 않는다. 제한을 무조건 제거하지 않는다.
3. 전역 예산 기록, 작업별 예약, 독립 결과 경로, 본체의 적재 경로를 준비한다. 예산/경로가 없는 양식은 실행하지 않는다.
4. 5개의 `gpt-6-luna` 작업자를 생성해 batch별 명세를 전달하고 결과를 기다린다. 완료한 결과를 본체가 검토·적재한 뒤 다음 계정 또는 적격 token 작업을 배정한다.

계정별 완료는 원문 회수 상태와 검증 상태를 포함한 한 행이 있어야 한다. `requested_history_days=60`, 실제 확보 시작/끝, source별 gap과 미완료 cursor를 함께 기록한다.60일 경계를 확인하지 못하거나 provider가 이전 자료를 반환하지 않으면 partial/unavailable로 기록한다. 같은 요청 예산을 유지하며 필요한 추가 페이지는 후속 batch에서 재개한다. 이미 저장한 더 오래된 자료는 삭제하지 않고 새 구간에 맞게 선택한다. 전체100명은 `완료/일부확보/실패/미착수`가 모두 집계돼야 하며 미확보를0으로 숨기지 않는다. Token별 완료는 cap decision·실제 분석 구간·pool coverage·최종 buyer·cluster·exit·자금 연결·CEX·PnL unknown과 근거를 제출한 상태다. 전체 chain/lifetime history 완료와 구분한다.

최종 한글 보고서는 사람별 개요, token별 timeline, 주소 연결도, 후보 군집, 공개 이후 매도/회수, 증거 등급, 반대 근거, coverage gap과 다음 작업을 담는다. 새 연결·반복 회수·공통 정확한 deposit·의미 있는 시점 관계 또는 사용자 조치가 필요한 실패를 우선 알린다.


## 8. 첫 실행 결과와 재개

`top100-60d-20261007-v1-batch001`은 검토 완료·history partial 상태로 종료했다. 책임 범위는20명씩이고 실제 새조회는2명씩이었다. Raw2069–2088은20개 Fomo 응답, raw2089–2095는 시장자료7회, raw2096은 본체의100명/100THESIS/$1M 선별 검토다. Worker 원문과 결과는 작업별 폴더에 있고 canonical writer는 본체였다.

Fomo source13개는 목록 반환,7개는 unavailable이다. THESIS API의81행 중78행이 고정 구간에 들었고, 기존 원문과 native THESIS를 합쳐100문서를 정규화했다. 게시 당시 cap으로 제외한 STOCKER1문서 외99문서는보류이고 eligible은0개다.60일 전체 확보나 지갑 소유권·공통 CEX 입금·선행매수 의도·수익을 확정하지 않았다.

저장된 batch의 capture/ingest 입력 경로:

```sh
PYTHONPATH=src python3 -m fomo_research.parallel_foundation --manifest data/research/parallel/top100-60d-20261007-v1-batch001/manifest.json
```

closed batch는 저장된 검토를 재사용한다. 부분 capture를 local-only로 적재하려면 `--ingest-only`를 붙인다. 기존 native alert cursor와 RZD/연우 trace state는 별도다. 새 배치에서는 새로운 batch ID와 작업 명세·예산 예약을 만들며 고정 cohort와60일 구간을 상속한다. 다음 후보10명은3·4·23·24·43·44·63·64·83·84위다. 미확보Fomo source7개와 pending cap99개는 `next_frontier`에 있다. 이번 시장자료 조회는 한글 보고서와 ignored market-cap-review.json을 따르며 hourly cap이300초 바깥이면 채택하지 않는다.

## 9. THESIS 없는 BUY와 카피 트레이딩 가설 — v2

THESIS/CALL 없이 매수만 노출해도 후속 매수가 발생할 수 있다는 사용자 가설을 추가했다. 모든 Fomo BUY를 독립 anchor로 보존한다. 같은 token의 다른 계정 THESIS 또는 해당 계정의 나중 THESIS가 있어도 BUY anchor를 제거하지 않는다. THESIS 미확보는 과거 게시 부재의 증명이 아니다.

기존 source BUY timestamp는 예비 목록·범위 작성에만 사용한다. 심층 배정 전 실제 성공 swap·최종 owner·매수 시각과 그 시점 유통 시총≤$1M을 검토한다. BUY source 시각, 실제 swap 시각, 대외 노출 시각, capture 시각은 별도다. 같은 초·같은 block의 순서는 transaction/instruction index가 있어야 판정한다. 과거 노출 시각이 없으면 copy-trading 반응 지연은 unknown이다.

검토할 패턴은 `연관 후보 실제 선행매수 → Fomo 실제 매수 → 확인된 노출 → 추종 매수 → 후보 매도/회수`다. 순서·반복성·비서비스 자금 관계·같은 정확한 CEX 고객 deposit과 가격/quote를 함께 확인하며, 시간적 선행만으로 의도·동일인·수익을 확정하지 않는다. MEV/샌드위치·토큰 출시 sniper·봇과 대조 구간도 검토한다.

`parallel_anchors.py`가 canonical THESIS 관측과 BUY 이벤트로 통합 목록을 만든다. 기존 네트워크 수집이나 완료 batch를 재실행하지 않고 아래 local-only 입력으로 갱신할 수 있다. 새 foundation batch의 적재 종료에도 해당 목록을 저장한다. Canonical 산출물은 `raw_payloads.source=lowcap_event_inventory`, pointer는 `collector_state.top100_lowcap_event_inventory_v2`다. 상세 [한글 보고서](buy-prebuy-review.md)를 따른다.

```sh
PYTHONPATH=src python3 -m fomo_research.parallel_anchors --output-directory data/research/parallel/top100-60d-20261007-buy-anchors-v2
```

대기 목록 작성은 cap 확인·시장 전체 거래 수집·매수 군집 발견과 구분한다. 신규 BUY cap과 시장 swap 수집은 별도 예산 예약 후 실행한다.
