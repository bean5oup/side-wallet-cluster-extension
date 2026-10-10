# Top100 병렬 조사 — 첫 배치 결과

갱신: 2026-10-07 KST. 정책 `top100-lowcap-1m-v1`.

## 이번에 진행한 작업

모델 `gpt-6-luna`·추론 `max` 작업자 5개가 고정 Top100의 기존 증거를 20명씩 검토했다. 본체가 각 구간의 첫 2명, 총 10명의 과거 THESIS와 거래 알림을 순차 조회하고 SQLite에 적재했다. 작업자는 외부 요청 없이 담당 2명의 원문·적재본·기간과 공백을 재검토했다.

- 표본: 30d raw1654, snapshot `2026-10-07T00:29:19.532Z`, 사용자 ID 100개 고정.
- 목표 구간: `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z`(정확히 60일).
- 새 계정별 조회는 10명이며, 나머지 90명은 이번 배치에서 새 조회하지 않았다.
- SQLite가 기준이다. 수신 원문 전체를 보존하고 분석 구간 밖 글과 PERP 알림은 현물 THESIS/BUY/SELL 적재에서 제외했다.

## 수집 규모와 비용

- 새 Fomo 요청 20회, 실제 7,250 credits. 13개 페이지 반환, 7개 source unavailable(HTTP 실패와 구분).
- THESIS 원문 81행을 받았고, 구간 내 78행을 선택했다. Keraunos의 종료 경계 밖 3행은 raw에 보존했다.
- 새 canonical 이벤트 167건: native alert 90건 + 별도 문서에서 추가한 THESIS 77건. PERP 알림 66행은 원문만 보존했다.
- 기존 Top100 원문까지 합친 고정 구간의 THESIS는 중복 제거 100건/12명, 정확한 chain/token 87개다. 전체 Fomo 이벤트 257건은 기존 자료와 이번 자료의 합계다.
- 마지막 관측 Fomo 잔액 236625 credits, 관측 시각 `2026-10-07T06:26:30.067Z`. 현재 월간 잔액을 보장하는 값은 아니다.
- 공개 시장자료 요청 7회(429 재시도 1회 포함). 신규 RPC·Bridge·Nodit indexed·BigQuery 요청은 0회.

## 첫 10명 — 원문과 구간 내 canonical 기록

THESIS 원문 열의 `미확보`는 반환된 빈 목록이 실제 게시물 0건이라는 뜻이 아니다. 이벤트 수는 새 자료와 기존 자료를 합친 canonical 기록이며, Fomo BUY/SELL은 온체인 swap 검증과 구분한다.

| 순위 | 계정 | THESIS API 구간 내/반환 | alerts 상태 | canonical THESIS/BUY/SELL | raw |
|---|---|---|---|---|---|
| 1 | pointfarmcap | 미확보 | 10행 | 5/5/0 | 2069, 2070 |
| 2 | RareDualJay | 22/22 | 1행 | 22/2/0 | 2071, 2072 |
| 21 | boosted | 25/25 | 미확보 | 25/0/0 | 2073, 2074 |
| 22 | 000000 | 미확보 | 25행 | 0/16/3 | 2075, 2076 |
| 41 | Keraunos | 12/15 | 14행 | 13/1/4 | 2077, 2078 |
| 42 | end837 | 6/6 | 53행 | 6/0/0 | 2079, 2080 |
| 61 | jxnwa | 미확보 | 10행 | 1/1/8 | 2081, 2082 |
| 62 | escobarpablo | 13/13 | 5행 | 13/2/3 | 2083, 2084 |
| 81 | sky_link | 미확보 | 미확보 | 0/0/0 | 2085, 2086 |
| 82 | tontheneko | 미확보 | 47행 | 0/17/30 | 2087, 2088 |

## 같은 토큰의 공개 기록과 시총 선별

여러 계정이 같은 토큰을 언급한 기록은 시총 자료 확인의 우선순위다. 주소 소유권·공통 자금·선행매수 군집의 근거로 승격하지 않는다.

| 토큰 | 체인 | 확보한 공개 글 작성자 | 글 수 | cohort에서 확보한 가장 이른 게시 UTC |
|---|---|---|---|---|
| STOCKER | ethereum | RZDxbt, RareDualJay | 5 | 2026-09-28T18:46:25.000Z |
| STONK | solana | pointfarmcap, RZDxbt | 5 | 2026-10-03T21:31:40.000Z |
| CLAUS | ethereum | jxnwa, ultrapara | 2 | 2026-10-05T00:53:15.000Z |
| MOO | robinhood | wealthmaxxer, end837 | 2 | 2026-09-10T10:13:10.000Z |

**STOCKER의 10월 6일 19:04:20 UTC 글 1건은 제외했다.** 정확한 Ethereum 계약 주소를 CoinGecko `stockereum-fun`과 대응했고, 게시 260초 전인 19:00 UTC 유통 시총 표본은 `$3,349,725.1278897524`였다(raw2089/2090). 공급자 시총 assertion과 현재가·FDV를 구분했다. 다른 시점의 STOCKER 글까지 일괄 제외하지 않았다. [계약 주소 대응 명세](https://docs.coingecko.com/reference/coins-contract-address), [과거 시총 조회 명세](https://docs.coingecko.com/reference/coins-id-market-chart-range).

새 $1M 기준 결과: `{'pending_cap': 99, 'excluded_above_cap': 1}`. **eligible 0건**이다. 나머지 글은 아직 요건을 확인하지 못한 상태이며 대상이 없다는 결론이 아니다. STOCKER·STONK의 다른 글은 시간별 표본이 게시 직전 300초 이내에 없어 보류했다. CLAUS는 정확한 계약 대응까지 확인했지만 과거 차트가 429를 반환했고, 한 번 재시도한 뒤 gap으로 남겼다(raw2093–2095). MOO와 나머지 토큰은 이번 배치의 시장자료 조회 범위 밖이다.

STOCKER에서 RareDualJay의 9월 28일 글이 기존 RZD 공개 글보다 이른 기록으로 추가됐다. 이는 두 계정이 같은 토큰을 언급했다는 공개 기록일 뿐이며, 지갑 간 연결이나 조종 의도로 해석하지 않았다.

## 확인하지 못한 부분

- 100명 중 60일 전체 history 확보가 확인된 계정은 0명이다. `since=60일 전`, `hasMore=false` 또는 100개 미만 THESIS 반환만으로 공급자의 이전 보존 범위를 보장하지 않는다.
- 새 THESIS API 자료의 가장 이른 글은 boosted의 8월 29일이다. 고정 시작일 8월 8일까지의 자료는 확보하지 못했다. 계정별 상세 공백은 accounts.json에 기록했다.
- THESIS API 성공 응답의 `minEquity=0`, `minLikes=0`을 보존했다. 추가 페이지를 뜻하는 `hasMore`/cursor/total과 무필터 lifetime 보장은 확인되지 않았다.
- sky_link는 두 source 모두 unavailable이며 정상적인 0건 계정으로 집계하지 않는다. end837은 alerts 53행이 모두 PERP여서 현물 BUY/SELL 0건으로 저장됐으나 실제 현물 활동 부재를 뜻하지 않는다.
- RareDualJay의 이번 alerts raw2072는 Ash BUY 1건만 반환했지만, 같은 요청 구간의 ERRAND BUY가 기존 raw678에 남아 있다. `hasMore=false`여도 저장 원문 사이에 누락이 있다는 구체적인 반례이며, 이전 기록을 삭제하지 않았다.
- 지갑 후보는 그대로 후보이며 검증된 기존 wallet resolution만 재사용했다. 이번 실행으로 새로운 뒷지갑·공통 CEX 입금 주소·선행매수 의도·실현 수익을 확정하지 않았다.

## 저장 결과와 다음 조사

- 기준 DB: `data/research/fomo.sqlite3`. 검토 raw2096, `lowcap_thesis_screens.threshold_usd=1000000`, state `top100_parallel_foundation_v1`.
- `data/research/parallel/top100-60d-20261007-v1-batch001/`에 manifest, 100명 accounts, cap review, token queue와 5개 작업자의 한글 보고서를 저장했다. 원문은 대응하는 `data/raw/parallel/.../primary/`에 있다.
- 다음 계정 배치 후보: 3·4·23·24·43·44·63·64·83·84위. 아직 배정·조회하지 않았으며 새 전역 예산 예약이 필요하다.
- 병행할 우선 작업은 99개 보류 글의 게시 당시 유통 시총 근거다. 더 가까운 가격만 확보되더라도 역사적 유통량이 확인되지 않으면 FDV로 대체하지 않는다.
- eligible이 확인된 token/event만 실제 매수 군집, 공개 이후 매도, 비서비스 공급·반환과 정확한 고객 CEX 입금 chain/address 비교로 넘긴다.

## 전체 100명 진행표

계정 상태 집계: `{'partial': 21, 'not_started': 78, 'unavailable': 1}`. `partial`은 저장 기록이 있는 상태이고 기간 완전성을 뜻하지 않는다. `not_started`는 새 조회와 보존된 이벤트가 없는 상태다. 별도로 이번 새 조회 미착수는 90명이다.

| 순위 | 계정 | 이번 새 조회 | 저장 THESIS/BUY/SELL | 연구 상태 |
|---|---|---|---|---|
| 1 | pointfarmcap | 시도 | 5/5/0 | 일부 확보 |
| 2 | RareDualJay | 시도 | 22/2/0 | 일부 확보 |
| 3 | ExactTallTakin | 미착수 | 0/0/0 | 미착수 |
| 4 | pricedin | 미착수 | 0/0/0 | 미착수 |
| 5 | RunningClam | 미착수 | 0/0/0 | 미착수 |
| 6 | OmakaseOnly | 미착수 | 0/0/0 | 미착수 |
| 7 | bigbabba | 미착수 | 0/0/0 | 미착수 |
| 8 | bystevenr | 미착수 | 0/1/0 | 일부 확보 |
| 9 | GenerationalFumbler | 미착수 | 0/0/0 | 미착수 |
| 10 | 0xLingard | 미착수 | 0/0/0 | 미착수 |
| 11 | kv4rl | 미착수 | 0/0/0 | 미착수 |
| 12 | USronaldcarter | 미착수 | 0/0/0 | 미착수 |
| 13 | looc | 미착수 | 0/8/7 | 일부 확보 |
| 14 | CoachPauI | 미착수 | 0/0/0 | 미착수 |
| 15 | 0xstanczyk | 미착수 | 0/0/0 | 미착수 |
| 16 | fxcxc | 미착수 | 0/0/0 | 미착수 |
| 17 | _benjitrades | 미착수 | 0/0/0 | 미착수 |
| 18 | cosmic358 | 미착수 | 0/0/0 | 미착수 |
| 19 | CeruleanRange | 미착수 | 0/0/0 | 미착수 |
| 20 | khomenei | 미착수 | 0/0/0 | 미착수 |
| 21 | boosted | 시도 | 25/0/0 | 일부 확보 |
| 22 | 000000 | 시도 | 0/16/3 | 일부 확보 |
| 23 | terpinolene | 미착수 | 0/0/0 | 미착수 |
| 24 | dylansdegens | 미착수 | 0/0/0 | 미착수 |
| 25 | shootingguard | 미착수 | 0/0/0 | 미착수 |
| 26 | chosen_1 | 미착수 | 0/0/0 | 미착수 |
| 27 | Nichequantelsa | 미착수 | 0/0/0 | 미착수 |
| 28 | 0x_Darius | 미착수 | 0/0/0 | 미착수 |
| 29 | oznek | 미착수 | 0/0/0 | 미착수 |
| 30 | Hifive_07 | 미착수 | 0/0/0 | 미착수 |
| 31 | DonnyDicey | 미착수 | 0/0/0 | 미착수 |
| 32 | plottwisst | 미착수 | 0/0/0 | 미착수 |
| 33 | DONBAGS | 미착수 | 0/0/0 | 미착수 |
| 34 | ultrapara | 미착수 | 1/0/0 | 일부 확보 |
| 35 | prevaile | 미착수 | 0/0/0 | 미착수 |
| 36 | CryptoZachLA | 미착수 | 0/0/0 | 미착수 |
| 37 | ResellCalendar | 미착수 | 0/0/0 | 미착수 |
| 38 | ExtendedLocalPlatypus | 미착수 | 0/0/0 | 미착수 |
| 39 | The__Solstice | 미착수 | 1/1/0 | 일부 확보 |
| 40 | 0xfinne | 미착수 | 0/0/0 | 미착수 |
| 41 | Keraunos | 시도 | 13/1/4 | 일부 확보 |
| 42 | end837 | 시도 | 6/0/0 | 일부 확보 |
| 43 | BLSZY | 미착수 | 0/0/0 | 미착수 |
| 44 | 0xsneakky | 미착수 | 0/0/0 | 미착수 |
| 45 | 0xBEC001 | 미착수 | 0/0/0 | 미착수 |
| 46 | OscarsProficy | 미착수 | 0/0/0 | 미착수 |
| 47 | beastymcbeast | 미착수 | 0/0/0 | 미착수 |
| 48 | FuzzyOliveTrout | 미착수 | 0/0/0 | 미착수 |
| 49 | cryptoklotz | 미착수 | 0/0/0 | 미착수 |
| 50 | ManaMoonNFT | 미착수 | 0/0/0 | 미착수 |
| 51 | prometheusx91 | 미착수 | 0/0/0 | 미착수 |
| 52 | chopper_trades | 미착수 | 0/0/0 | 미착수 |
| 53 | redemptionjizzy | 미착수 | 0/1/0 | 일부 확보 |
| 54 | WashedUpWalter | 미착수 | 0/0/0 | 미착수 |
| 55 | niyedie | 미착수 | 0/0/0 | 미착수 |
| 56 | TccczGin403 | 미착수 | 0/0/0 | 미착수 |
| 57 | hitscanr | 미착수 | 0/0/1 | 일부 확보 |
| 58 | RZDxbt | 미착수 | 10/20/12 | 일부 확보 |
| 59 | andrea_tennis | 미착수 | 0/0/0 | 미착수 |
| 60 | xbtDLN | 미착수 | 0/0/0 | 미착수 |
| 61 | jxnwa | 시도 | 1/1/8 | 일부 확보 |
| 62 | escobarpablo | 시도 | 13/2/3 | 일부 확보 |
| 63 | brokeSzn | 미착수 | 0/0/0 | 미착수 |
| 64 | yams | 미착수 | 0/0/0 | 미착수 |
| 65 | Carver_ | 미착수 | 0/0/0 | 미착수 |
| 66 | exitliqexe | 미착수 | 0/0/0 | 미착수 |
| 67 | teepanddestroy | 미착수 | 0/0/0 | 미착수 |
| 68 | BeggeSol | 미착수 | 0/0/0 | 미착수 |
| 69 | wealthmaxxer | 미착수 | 2/3/0 | 일부 확보 |
| 70 | maxiplaysgames | 미착수 | 0/0/0 | 미착수 |
| 71 | Zunoxbt | 미착수 | 0/5/3 | 일부 확보 |
| 72 | JohnnyBones | 미착수 | 0/0/2 | 일부 확보 |
| 73 | starcatcher444 | 미착수 | 0/0/0 | 미착수 |
| 74 | SolarFirmDingo | 미착수 | 0/0/0 | 미착수 |
| 75 | OuterHeavyBat | 미착수 | 0/0/0 | 미착수 |
| 76 | leo | 미착수 | 0/0/0 | 미착수 |
| 77 | ztard | 미착수 | 0/0/0 | 미착수 |
| 78 | BitmanTW | 미착수 | 0/0/0 | 미착수 |
| 79 | TendersAlt | 미착수 | 0/0/0 | 미착수 |
| 80 | MINHxDYNASTY | 미착수 | 0/0/0 | 미착수 |
| 81 | sky_link | 시도 | 0/0/0 | 자료원 미확보 |
| 82 | tontheneko | 시도 | 0/17/30 | 일부 확보 |
| 83 | Tekkerrss | 미착수 | 0/0/0 | 미착수 |
| 84 | VexRex23 | 미착수 | 0/0/0 | 미착수 |
| 85 | DopamineFeenFr1 | 미착수 | 0/0/0 | 미착수 |
| 86 | Grovyle | 미착수 | 0/0/0 | 미착수 |
| 87 | Mochicapital08 | 미착수 | 0/1/0 | 일부 확보 |
| 88 | TheOnlyOMP | 미착수 | 0/0/0 | 미착수 |
| 89 | kikaka10000 | 미착수 | 0/0/0 | 미착수 |
| 90 | BarBarrBinks | 미착수 | 0/0/0 | 미착수 |
| 91 | ETH_Exy | 미착수 | 0/0/0 | 미착수 |
| 92 | PoorGoat_ | 미착수 | 1/0/0 | 일부 확보 |
| 93 | sadcrissy | 미착수 | 0/0/0 | 미착수 |
| 94 | thebiglong | 미착수 | 0/0/0 | 미착수 |
| 95 | LuckyManRRR | 미착수 | 0/0/0 | 미착수 |
| 96 | sainted007 | 미착수 | 0/0/0 | 미착수 |
| 97 | XVentures | 미착수 | 0/0/0 | 미착수 |
| 98 | gameplay | 미착수 | 0/0/0 | 미착수 |
| 99 | asado_dreams | 미착수 | 0/0/0 | 미착수 |
| 100 | chiwaua | 미착수 | 0/0/0 | 미착수 |
