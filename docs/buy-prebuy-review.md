# THESIS 없는 BUY와 선행매수 조사

갱신: 2026-10-07 KST. 정책 `top100-lowcap-1m-v2`.

## 후속 실행 결과

[BUY 첫 검토 보고서](buy-first-batch-review.md), review raw2140을 우선한다. BUY26건을 실제 검토해 검증된 본지갑 매수3건과 BSC 후보 지갑 token 전달2건을 분리했다. 이 BUY26건은 제외1/일반 보류23/FDV 대용치 보류2/적격0이다. 최신 전체 목록 raw2141은184 anchors·112 tokens, 제외2/일반 보류180/대용치 보류2/적격0이다. `top100_buy_anchor_review_v2`에 frontier가 있고 `parallel_anchors.py`가 검토를 다시 적용한다.

아래 raw2099와 외부 요청0회·BUY84건 전부 검토 대기 수치는 **범위를 추가한 최초 오프라인 작업** 기록이다. 후속 배치의 시장자료20/RPC11/Nodit indexed2 및 검토 상태와 구분한다.

## 변경한 조사 범위

THESIS/CALL을 작성하지 않아도 Fomo 계정의 BUY를 독립 조사 기준으로 포함한다. 사용자의 가설은 연관 지갑이 먼저 매수하고, Fomo 본계정의 매수 노출에 이어 추종 매수가 유입될 때 앞선 지갑이 매도할 수 있다는 것이다. 아래는 이 가설을 조사하기 위한 기준과 저장 자료 목록이며 새 선행매수 군집을 확인한 결과는 아니다.

- 표본: 30d Top100 raw1654의 사용자 ID100개 고정.
- 구간: `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z`, 정확히60일.
- 시총 상한: THESIS/CALL 게시 또는 BUY 당시 **유통 시총 USD≤1,000,000**. 현재 시총·FDV·미확인은 적격 대용치가 아니다.
- BUY의 Fomo source timestamp는 예비 목록 기준이다. 실제 성공 swap·최종 owner·매수 시각을 검토한 뒤 해당 시점 cap을 확인해야 심층 작업을 배정한다.
- 같은 토큰에 THESIS가 있어도 BUY 기준을 별도로 유지한다. 글이 없는 것으로 보이는 계정도 실제 과거 글 부재가 확인된 것은 아니다.

## 저장 자료에서 확인한 규모

| 항목 | 수량 |
|---|---:|
| THESIS 기준 이벤트 | 100건 |
| BUY 기준 이벤트 | 84건 |
| THESIS에 등장한 정확한 chain/token | 87개 |
| BUY에 등장한 정확한 chain/token | 36개 |
| THESIS+BUY 통합 chain/token | 112개 |
| 전체 표본의 확보 THESIS에 없던 BUY 토큰 | 25개 |
| 해당 매수자의 같은-token THESIS 미확보 BUY | 55건 |
| 전체 표본의 같은-token THESIS 미확보 BUY | 46건 |
| 기존 온체인 event/token match 참조가 있는 BUY | 4건 |

기존 THESIS 시총 검토100건은 제외1/보류99를 재사용했다. 새 BUY84건은 모두 해당 매수 시점 cap과 실제 swap 검토 대기다. 통합184개 기준 이벤트는 제외1/보류183/심층 배정 가능0이다. 전체112개가 저시총으로 확인된 것은 아니다. 기존 온체인 match4건도 실제 경제적 BUY와 quote·owner의 검토를 이 새 기준에서 자동 완료시키지 않았다.

이번 작업은 저장 자료만 사용했다. 외부 Fomo·시장자료·RPC·Bridge·Nodit·BigQuery 신규 요청은0회이며 새 시장 매수 군집·카피 트레이딩 의도·동일인·실현 수익을 판정하지 않았다.

## THESIS 목록에 없던25개 토큰

아래 계정과 수량은 고정 표본·구간의 보존 BUY 기록이다. 원문 거래 주장은 실제 swap proof와 구분한다. 심볼이 아닌 정확한 chain/주소로 식별한다.

| 체인 | 토큰 | 보존 BUY | Fomo 계정 | 정확한 contract/mint |
|---|---|---:|---|---|
| bsc | 万事兴龙 | 1 | 82위 tontheneko | `0x1d2dad86be884940c233378dd3373fc494b17777` |
| bsc | 币安公主 | 1 | 82위 tontheneko | `0x70a56b172345c72e441a4d17282ea8a47cbb7777` |
| bsc | 中国龙 | 1 | 82위 tontheneko | `0x796b4b2ae234c3adcb51c4aaa7a026d2d0c07777` |
| bsc | CZ | 1 | 82위 tontheneko | `0xb1b798c76a9f7bc6f5002dd72c23cf0d64b76666` |
| bsc | ANIMA | 1 | 87위 Mochicapital08 | `0xc5baf7b5c225ace7fa249e8007776689b3337777` |
| ethereum | ZC | 5 | 22위 000000 | `0x4e67db19044549ff420860834c91b45bad298722` |
| solana | ALLINU | 2 | 13위 looc | `4MMQY9bwkxxTtsK3W227Q5ABT6yFY8Pmn9Ze7wmAXKY8` |
| solana | XEET | 1 | 82위 tontheneko | `6HFJ5sxVoEtczr9siAUeGssmpfhQSS3pEoBcCycUpump` |
| solana | Attention+ | 1 | 82위 tontheneko | `75gGuxuqKhQQiHae8JKDQaetK3XguKf1rUJ1csispump` |
| solana | DARK | 2 | 39위 The__Solstice, 82위 tontheneko | `7KEPApdbBMByrmqihz3bht2uMhFQcatjfSFQCKq66kH3` |
| solana | KNOTS | 1 | 1위 pointfarmcap | `8RVBk8vxLiUHueLUW1f4izFVqN3nWippLhkohKg6EGkS` |
| solana | SNDK | 1 | 1위 pointfarmcap | `8t5C4AWDg4CroMChxdo7rG2e8nJM31QG2GG7Czx9X7x2` |
| solana | FEEBITS | 1 | 82위 tontheneko | `BJUiNooYiZ4ojatPVeJAUXGEd3dcGzQ1ApWDoVTzpump` |
| solana | CRAWL | 3 | 82위 tontheneko | `BXoHJddsWJLHtAopeiSbKUSELsu8hSFMs8baGMDkpump` |
| solana | BACKERS | 1 | 53위 redemptionjizzy | `CBLx6CRcCTtbmgTdxpqnF2dP1MpWbMUjngtNbFTApump` |
| solana | PLAGUE | 1 | 82위 tontheneko | `CscZaq5twomhUkvCY8Jdd1tge32L4Yj9FbkFFEZQpump` |
| solana | SI | 5 | 8위 bystevenr, 13위 looc | `DEW9dSN6QpWyNthphCpMmAbZP1Q4cEKR9xQXAri98WDP` |
| solana | TCG | 6 | 22위 000000 | `DLGRpmkMGr7J4KD1xR5x2XjaGeQH64PLFQkyxNNSpump` |
| solana | RARI | 1 | 82위 tontheneko | `EFn88CiiFHhihqdr1Y11XBDxbbYarBf1ij92DsrigYwR` |
| solana | Ash | 1 | 2위 RareDualJay | `F5WvFdG9sCfhv3bVYAMJNWiwpx5e3X2uvpXDtLtdsDJs` |
| solana | UP | 1 | 82위 tontheneko | `FzPujTgKNJVim7YYa5HYHngGtf19QwV6ACJ1zDLWpump` |
| solana | www | 1 | 82위 tontheneko | `GAwhcphCqCv5bKHmCiN4VDdNWfbXJL4npmkc8L3Q9S9H` |
| solana | OCTO | 1 | 61위 jxnwa | `GoADAwux19tGxb3W4ykPzZz8p5JCSYaxBRpuW7s9pump` |
| solana | ZCAT | 4 | 1위 pointfarmcap, 22위 000000 | `HcRLc9VDgjLeK154xDawfb1dmVJ98DoSqcwTHGqiDeJR` |
| solana | PSTR | 2 | 82위 tontheneko | `bgzZngPG4bZTPRFjsyaVA12LMP64ZgFjdjjzHZ9qQNR` |

SI·ZCAT·DARK는 둘 이상의 Fomo 계정이 매수한 토큰이다. 이는 시총 확인의 우선 후보 신호이며 주소 간 연결이나 선행매수 군집의 증거는 아니다.

## 실제 조사 순서

1. 각 BUY의 실제 Fomo 지갑 swap·owner·tx·매수 UTC를 검토하고 그 시점 유통 시총≤$1M을 확인한다. THESIS의 cap 판정을 BUY에 복사하지 않는다.
2. 실제 매수 전2시간~후1시간을 첫 시장 탐색 창으로 두고, 매수 직전10/30/60초·5/15분을 비교한다. launch가 더 앞이면 필요한 이전 구간을 따로 배정한다. 모든 창은 고정60일 구간으로 자르며 전체 시장 coverage로 표현하지 않는다.
3. 같은-token 실제 swap의 최종 매수자를 추출한다. Fomo 매수 이전 군집과 확인된 대외 노출 이후 추종 매수를 분리한다. Transfer·router·중간 mint는 최종 매수자로 바꾸지 않는다.
4. 선행 후보의 후속 매도·quote 수령·본지갑 token 반환·비서비스 공급/회수를 확인한다. 기준 이벤트 후24시간을 초기 exit 창으로 두고 실제 근거가 있을 때 이어 간다.
5. 여러 토큰·날짜에서 반복되는지, Fomo 검증 지갑과 실제 자금 접점이 있는지, 같은 정확한 CEX 고객 deposit chain/address로 회수하는지 비교한다. 원가·이전 재고·fee·실제 exit가 있어야 PnL을 계산한다.

## 시간과 해석 규칙

- 실제 on-chain BUY, Fomo source BUY, BUY 대외 노출, THESIS/CALL, X 공개 글, 실제 SELL, capture를 별도로 저장한다. Source timestamp나 수집 시각을 과거 노출 시각으로 바꾸지 않는다.
- 실제 swap 직전 매수와 노출 직전 매수는 다른 시점 관계다. 과거 대외 노출 시각이 없으면 copy-trading 반응 지연은unknown이다.
- 동일 초·동일 block에서는 timestamp만으로 선후를 판정하지 않는다. EVM transaction index·Solana 거래/명령 순서 등 실제 순서 근거를 확인하고 미확인은 보류한다.
- 후보 군집은 봇·토큰 출시 sniper·MEV/샌드위치·동일 서비스 공유 및 비슷한 유동성/거래강도의 대조 구간과 비교한다.
- 선행매수 시각만으로 카피 트레이딩을 유도한 의도를 확정하지 않는다. 같은 exchange 이름·shared hotwallet·Relay pool은 같은 고객 근거가 아니다.
- 60일 history는 계속 미완료다. THESIS 미확보를 게시물 없음, 매수 기록 미확보를 거래 없음으로 해석하지 않는다.

## 저장과 재개

- 최신 SQLite 통합 목록: raw2141, `source=lowcap_event_inventory`, state `top100_lowcap_event_inventory_v2`. 최초 오프라인 raw2099는 보존한다. BUY 본체 검토는 raw2140, `source=top100_buy_anchor_review`, state `top100_buy_anchor_review_v2`다.
- 기준 이벤트는 기존 `fomo_events`/`fomo_thesis_observations`를 직접 참조한다. 통합 anchor/queue는 위 canonical raw JSON에 보존했고 새 관계형 테이블은 추가하지 않았다.
- 편의 파일: `data/research/parallel/top100-60d-20261007-buy-anchors-v2/{review.json,anchors.json,token-queue.json}`.
- 기존 완료 batch의 THESIS87토큰 queue와 raw2096 검토는 당시 결과로 보존한다. raw2097은 초기 목록의 THESIS 토큰 집계가112로 잘못 기록되어 현재87로 정정됐고 원문은 보존했다. raw2098은 중간 버전이며 현재 pointer를 따른다.
- 다음은 BUY-only25토큰과 여러 계정 BUY가 겹친 SI/ZCAT/DARK를 포함해 cap·실제 swap 근거를 확인하는 새 예산 예약이다. 적격 event가 생기면5개 `gpt-6-luna`·추론`max` 작업자에게 겹치는 token/window를 묶어 배정한다.
