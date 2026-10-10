# THESIS 없는 BUY 조사: 첫 검토 결과

갱신: 2026-10-07 KST. 정책 `top100-lowcap-1m-v2`, 배치 `top100-60d-20261007-v2-buy001`.

## 이번에 진행한 내용

THESIS가 확보되지 않은 매수도 조사하도록 바꾼 뒤, **7개 계정·9개 정확한 토큰·26개 BUY 원문 이벤트**를 먼저 검토했다. 5개 `gpt-6-luna`·추론 `max` 작업자가 저장 자료를 분석했고, 본체가 외부 수집·독립 원문 대조·SQLite 적재를 맡았다. 계정 전수 조사나 토큰 전체 시장 분석을 끝낸 배치는 아니다.

고정 표본은 30d Top100 raw1654의 사용자 ID이며, 과거 구간은 `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z`다. 대상은 THESIS/CALL 게시 또는 **검토한 실제 BUY 당시 유통 시총 100만 달러 이하**인 이벤트다. 현재 시총이나 FDV를 이 조건으로 바꾸지 않았다.

| 이번 검토 항목 | 결과 |
|---|---:|
| BUY 원문 이벤트 | 26건 |
| Fomo 계정 / 정확한 chain-token | 7명 / 9개 |
| 검증된 Fomo 지갑의 실제 매수 | 3건 |
| 별도 후보 지갑의 토큰 수령 receipt | 2건 |
| BUY 시총 제외 / 유통 시총 보류 / FDV 대용치 보류 | 1 / 23 / 2건 |
| 심층 매수 군집 조사에 배정 가능한 BUY | 0건 |
| 새 온체인 거래 / 이벤트 매칭 추가 | 각각 2행 |
| BSC 인덱스 조회 / 전송 정규화 추가 | 각각 2행 |

실제 매수 3건은 기존 완전한 RPC 원문을 재사용해 검토했다. KNOTS는 이미 매칭되어 있었고, SNDK·ZCAT의 정규화와 이벤트 대응 2건을 새로 저장했다. BSC의 2건은 후보 수령주소가 토큰을 받은 근거이며, 검증된 Fomo 매수 3건에 더해 계산하지 않는다.

**연관 지갑의 선행매수·공통 고객 CEX 입금·카피 트레이딩 유도·실현 수익은 아직 판정하지 않았다.** 이번에 저시총 심층 조건을 충족한 이벤트가 없어서 신규 전체 시장 군집·CEX 분기 수집을 시작하지 않았다. 이 결과는 뒷지갑이 없다는 의미가 아니다.

## 검증된 pointfarmcap 지갑의 실제 매수

검증된 Solana 지갑은 `Beqv6dzTcjV2eodo8RRXCiCcnSYrS1vkQKhfqwHXqeit`다. 아래 시각은 모두 2026-10-06 UTC다. 성공 거래, 지갑 서명, 역사적 token-account owner, 해당 지갑의 최종 토큰 증가와 USDC 감소를 직접 RPC·기존 enhanced history 양쪽에서 대조했다. 중간 mint의 최종 잔액 변화가 0인 경우 별도 취득 토큰으로 세지 않았다.

| 토큰 | Fomo BUY 시각 | 실제 매수 | 최종 토큰 증가 | 같은 지갑의 USDC 감소 | 직접 / enhanced 원문 |
|---|---|---|---:|---:|---|
| SNDK | 01:03:45 | 01:03:46 | 472,146.35139 | 2,500 | raw698 / raw744 행68 |
| ZCAT | 01:04:15 | 01:04:16 | 35,369.093546443 | 2,000 | raw696 / raw744 행66 |
| KNOTS | 01:05:00 | 01:05:03 | 747,331.322008 | 2,000 | raw695 / raw744 행65 |

확인 링크: [SNDK 거래](https://solscan.io/tx/9CJ2tocUqCmPTvevUS98yi2kdk4VTw1wjMimqZkwv19Q7TQF6XDCr24WuBd82nZ6wQCgU7KkpY2TzX4phPG2k8L), [ZCAT 거래](https://solscan.io/tx/UMcAszMExB49BE6oyEd7WyZxRUGZdC4o3kcGKtwPt6sp6ZXdVbC9CfmoszJtpMa8o1JAJXmMGdjYqizhWDcVTgs), [KNOTS 거래](https://solscan.io/tx/LM7LP1ggb9qoXuiBo3iBzP2mFGtE9SoATxvWEXk7FZBodKKCpPsXWXmZ6pLyhbfGt9By621aQXn1uXh49eFFbRW).

ZCAT에는 00:33:32, 00:40:49, 00:44:54의 앞선 매수 3건도 있다. **모두 같은 검증 본지갑**이므로 별도 뒷지갑의 선행매수로 분류하지 않았다. KNOTS의 01:17:10, 03:09:16, 03:09:29 추가 매수도 같은 지갑의 재매수다. 보존된 이력의 최신 시각 03:09:29까지 세 대상의 이후 매도가 관측되지 않았지만, 이후 24시간 exit 창 전체를 확보한 것은 아니다.

BUY 알림의 대외 노출 시각은 미확인이다. 위 USDC 감소는 실제 거래의 quote 지출이며, Fomo의 포지션 USD 표시나 실현 수익이 아니다. 이전 재고·추가 매수·수수료·최종 매도 lot을 모두 대응시키기 전에는 PnL을 계산하지 않는다.

## 이벤트별 시총 판정

| 토큰 / BUY 원문 수 | 이번에 확보한 근거 | 최종 상태 |
|---|---|---|
| ZCAT / 4 | pointfarmcap 실제 매수 256초 전 CoinGecko 시총 $48,433,325.912141725 | 해당 1건 제외. 000000의 나머지 3건은 별도 시각·매수 검증이 필요해 보류 |
| KNOTS / 1 | 시총 $2,561,850.241285498 표본이 실제 매수 303초 전 | 운영 기준 300초를 넘어 보류. Fomo source 시각에서는 300초였으나 실제 시각 판정으로 복사하지 않음 |
| SNDK / 1 | 실제 매수·직전 완료 분봉 가격 확보, CoinGecko exact mint 조회 404 | 유통량·역사적 유통 시총 보류 |
| SI / 5 | 정확한 mint와 시간별 시총 표본 확보 | BUY 시각에서 최근 이전 표본까지 760–940초라 보류; 실제 BUY 대응도 미확인 |
| DARK / 2 | 과거 조회 429, 현재 metadata와 첫 source BUY 직전 분봉 가격 확보 | 보류. 현재 market cap의 0.0을 저시총으로 해석하지 않음 |
| TCG / 6 | 현재 metadata·분봉 5개 응답 확보 | 첫 BUY에 가까운 완료 분봉은 없고 실제 체결·유통 시총도 미확인 |
| ZC / 5 | 현재 metadata 확보 | 과거 시총·실제 체결 보류 |
| CZ / 1 | receipt 전달 시각 직전 완료 분봉×그 block 총발행량 ≈ $763,271.637633785 | FDV 대용치 보류 |
| ANIMA / 1 | receipt 전달 시각 직전 완료 분봉×그 block 총발행량 ≈ $1,097,490.71174435 | FDV 대용치 보류 |

CZ 가격은 10/5 14:11–14:12 완료 분봉, ANIMA는 14:45–14:46 완료 분봉이다. 각 수령 block에서 `decimals=18`, `totalSupply=10^27 raw`, 즉 총발행량 10억 개를 RPC로 읽었다. 분봉 종료와 수령 시각의 차이는 각각 37초·21초다. 이 계산은 **역사적 가격과 총발행량의 대용치**이며 유통 시총이 아니다. 수령 시각도 해당 Fomo 사용자의 경제적 매수로 최종 귀속하지 않았다. 가격은 provider assertion이고 발행량은 RPC 근거다.

현재 상위 pool 한 개를 선택해 짧은 가격 창을 조회했으므로 모든 역사적 pool·시장 coverage가 아니다. 이벤트가 포함된 미완료 분봉은 제외했다. ZC·TCG·CZ·ANIMA의 CoinGecko metadata는 DARK 429의 제한된 재시도 후 **요청을 생략**한 상태다. 이를 404나 토큰 부재로 기록하지 않았다. 분봉 API의 [공식 OHLCV 설명](https://docs.coingecko.com/reference/pool-ohlcv-contract-address)과 [CoinGecko 기간별 시총 API](https://docs.coingecko.com/reference/coins-id-market-chart-range)를 참고했다.

## BSC에서 찾은 두 토큰 수령 거래

Nodit은 각 후보 주소와 exact contract의 BUY source 전후 120초만 조회했다. 각 응답은 count 1·수집 1행·cursor 없음이다. 이 필터의 결과 회수가 끝났다는 뜻이며 계정 전체 이력이 완성된 것은 아니다. 관련 성공 tx·receipt·block 시각과 과거 총발행량을 별도로 RPC에서 확인했다. [Nodit BNB Token Transfers 공식 문서](https://developer.nodit.io/en/api/bnb/web3-data-api/gettokentransfersbyaccount/).

| Fomo 계정 / 토큰 | 후보 수령주소 | 토큰 전달 UTC | 수령 raw 수량 / decimals | 거래 |
|---|---|---|---|---|
| 87위 Mochicapital08 / ANIMA | `0x4e4c73d4d73219aa3c3a9d1e8eecc87cde3ac826` | 10/5 14:46:21, source +1초 | 2355271404709111851867155 / 18 | [0x5bf5…bfef2](https://bscscan.com/tx/0x5bf51f5e1cc4498e55ceb3dd2cc38506d1d05d8bf468412d8ed35a58d42bfef2) |
| 82위 tontheneko / CZ | `0xa3ad0dc6b280ee4373306200444e2d5d1133b42c` | 10/5 14:12:37, source +2초 | 3370756473008551958743816 / 18 | [0xb48e…3054](https://bscscan.com/tx/0xb48e3088349675da5421485ad7388642bf047fcb657f75c78407797d47fa3054) |

CZ는 기존에 검증한 CZ/WBNB pool `0x6f0aa2c067ce5f6e5253d7f6487548fa01601b3b`의 출력 수량이 최종 수령 raw 수량과 일치한다. ANIMA는 V2 pool의 수수료성 전송을 제외한 net 출력과 추가 contract-origin 전송의 합이 최종 수령량과 일치한다. 추가 contract leg를 독립적인 표준 swap으로 분류하는 검토는 남았다.

두 거래는 외부 실행자가 `0xccc88a9d1b4ed6b0eaba998850414b24f1c315be`에 제출했고, 토큰은 `0xb92fe925dc43a0ecde6c8b1a2709c170ec4fff4f`를 거쳐 후보 주소로 전달된다. Quote 토큰은 `0xf70da97812cb96acdf810712aa562db8dfa3dbef`에서 서비스 경로로 들어온다. 후보 주소 자체의 quote debit은 receipt에 없다.

서비스 역할은 기존 공급자 라벨에 따른 분류이고, RPC가 검증한 것은 자산 전송·수령과 실제 실행 경로다. **같은 Relay 실행 경로는 계정 간 소유권·공통 자금 공급·공통 CEX 고객 연결 근거로 채택하지 않았다.** 두 계정의 후보 지갑 검증, 주문의 원래 자금 부담자와 경제적 매수 귀속은 남아 있다. 새 2건으로 기존 지갑 resolution을 임의 변경하지 않았다. 연우의 CZ 매수·THESIS는 다른 사용자·다른 날짜의 별도 근거다.

## 반복 알림과 선행·후행 후보

000000의 TCG 6건·ZCAT 3건·ZC 5건은 총 14개의 고유 event/alert ID다. 각 토큰에서는 같은 `tradeId`를 공유하고 `positionValueUsd`가 증가한다. 단순 같은 ID 재전송은 아니지만, 정확한 수량·swap ID·tx가 없어 14개의 독립 체결로 계산하지 않았다. looc의 SI 4개 BUY 알림도 같은 trade ID를 공유한다.

SI에는 bystevenr와 looc의 BUY 알림 5건이 180초 안에 보존되어 있다. 주변 5분 여유 창의 저장 Fomo 기록은 48개 계정·82행이며, 이 자체가 실제 토큰 시장의 거래 강도나 연관 군집을 증명하지 않는다. ANIMA에는 다른 계정 LuckyNiu의 190초 앞선 BUY 알림과 이후 다른 계정 SELL 알림도 있으나, 원문 알림 단계의 후보로만 보존했다. 지갑 간 연결과 실제 swap은 확인되지 않았다.

000000의 ZCAT SELL은 마지막 BUY 알림보다 26시간 8분 10초 뒤다. SELL의 provider 손익 값을 실제 수익으로 쓰지 않았다. ZC의 보존 SELL 둘은 같은 초·별도 ID·다른 trade ID이며 해당 BUY들보다 앞선 기록이다. TCG의 SELL 미확보 역시 매도 부재를 뜻하지 않는다.

## SQLite 저장과 한도

기준 결과는 **review raw2140**, 통합 THESIS+BUY 목록은 **raw2141**이다.

- `collector_state.top100_buy_anchor_review_v2`: 이번 검토·한도·다음 작업 지점.
- `collector_state.top100_lowcap_event_inventory_v2`: 최신 184개 기준 이벤트·112개 정확한 토큰 목록.
- 통합 상태: THESIS100 + BUY84, 제외2 / 일반 보류180 / 대용치 보류2 / 심층 배정 가능0. BUY26개를 검토했고 실제 매수 확인3건을 유지한다.
- `onchain_trades`와 `event_trade_matches`에 각각 2행을 추가했다. 신규 인덱스 전송2행은 `indexed_api_movements`에 있다. 관계형 BUY screen 테이블은 새로 만들지 않았고 26개 판정·실제 시각·source refs는 canonical raw2140의 JSON에 추가 보존했다.
- 작업자 5개 원문 결과도 raw2133–2137에 저장했다. 인덱스 조회 manifest는 raw2138–2139다. 외부 수집 원문은 raw2100–2132다.
- 다음 foundation 수집과 `parallel_anchors.py` 재생성 시 본체의 저장 검토를 다시 읽는다. 실제 매수·시총 판정이 최초 보류 상태로 초기화되지 않는다. 원래 Fomo source 시각은 별도로 유지한다.
- 기존 지갑 resolution, Fomo 원문 이벤트와 native checkpoint, RZD·연우 state 내용이 적재 전후 같음을 확인했다.

| 외부 자료 | 실제 시도 | 예약 |
|---|---:|---:|
| Fomo | 0 / credits 0 | 0 |
| 시장자료 | 20 | 20 |
| 직접 RPC | 11, BSC만 | 30 |
| Nodit indexed | 2 | 20 |
| Bridge / BigQuery | 각각 0 | 각각 0 |
| 작업자 직접 외부 요청 | 0 | 0 |

시장자료 20회에는 실패와 429 재시도 1회를 포함한다. 직접 RPC와 indexed의 사용하지 않은 예약은 이번 배치 종료와 함께 해제했다. 새 프로세스로 한도를 초기화하지 않았다. 새 BigQuery 청구 작업은 없다. Nodit의 실제 청구액·잔액은 응답에서 확인되지 않아 unknown이다. 과거 원문의 `/ws/alerts`는 재사용했으며 WebSocket 수집을 다시 시작하지 않았다.

## 다음 조사 지점

1. CZ·ANIMA와 다른 보류 이벤트의 **해당 시점 유통량/유통 시총** 근거를 보완한다. 이번 가격·총발행량·receipt는 재사용하고 같은 자료를 다시 요청하지 않는다.
2. BSC 두 거래의 주문별 원래 자금 부담자와 Fomo 후보 지갑 검증을 완료한다. 단일 토큰 수령·공용 실행 경로는 동일인 근거가 아니다.
3. 000000·looc의 반복 알림을 실제 distinct fill과 대응시킨다. 필요하면 후속 예산에서 Fomo swap/trade detail과 좁은 온체인 창을 사용한다.
4. 별도 계정 기초 수집에서는 다음 10명과 미완료 과거 페이지를 이어가 **고정 60일 coverage**를 확장한다. 첫 계정 배치 이후 새 사용자별 조회 미착수90명 상태는 이번 배치로 바뀌지 않았다.
5. 적격 이벤트가 확보되면 그때 실제 매수 전2시간·후1시간, 확인된 노출 이후 매도·24시간 exit·비서비스 공급/반환·동일한 정확한 고객 CEX 입금 chain/address를 조사한다. 현재 전체 시장 분석은 미착수다.

상세 작업자 보고서는 `data/research/parallel/top100-60d-20261007-v2-buy001/luna_1`부터 `luna_5`까지 있다. 본체 최종 판정과 후속 보완 사항은 같은 배치의 `primary-review.json`을 우선한다.
