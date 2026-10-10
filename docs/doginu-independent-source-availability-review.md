# DOGINU 독립 과거 공개·시총 자료의 가용성 확인

## 결론

[이전 종합보고서](top10-linked-wallet-case-and-cashout-report.md)의 거래 패턴과 정산은 보존했다. 이번에는 미확정 조건을 채울 독립 웹 원천을 확인했다. **확정 저시총 뒷지갑 사례는 여전히0이며 전체 연구 완료·자료 소진으로 선언하지 않는다.**

대상은 최초Top10/raw141, 고정60일 `2026-08-08T04:43:41Z ≤ t < 2026-10-07T04:43:41Z`다. 새로운 거래·지갑 검증·시총 적격 판정은 추가하지 않았다.

## 1. Fomo 과거 게시 원문

기존 raw2167에 정확한 작성자 handle `the__solstice`, DOGINU mint, 보존 thesis `2026-09-29T03:47:55Z`가 있다. 사용자Chrome에서 [정확 프로필](https://fomo.family/profile/the__solstice)로 직접 진입했으나 [랜딩 화면](https://fomo.family/)으로 이동했다(raw3897). 화면의 Start trading을 누르니 **Login or create an account** 창과 Apple/Google 로그인 선택이 표시됐다(raw3898).

현재 세션에서는 과거 프로필 목록을 확인하지 못했다. 기존 계정 로그인을 사용자에게 비동기로 요청했고 화면을 유지했다. 가입·약관 동의·거래 실행·인증정보 수집은 진행하지 않았다. 이 응답은 계정 삭제·thesis 없음·절대 최초 공개의 증명이 아니다. 기존 올바른 REST older cursor의 미가용 raw3245도 그대로 보존한다.

## 2. DOGINU와 상대 토큰의 시총 혼동 방지

[기존 정확 풀](https://www.geckoterminal.com/solana/pools/Gxy3xbjisxAWiNGMRU8Bv3wV66HuKR4vw6ZuRGmRW5w1)은 `tKalshi / DOGINU`다. 초기 화면의 선택된 토큰은 **T-Kalshi(TKLS)**였으며 가격$446.64, MCAP$695.81K, FDV$695.8K가 표시됐다. **이 숫자는 DOGINU의 당시 시총으로 사용하지 않았다.** 화면에 DOGINU mint `5JgioXRQSq1Nw4VJvpRyXxnvm8jVtLSUC7vbf1zzDg3L`은 상대 토큰으로 표시됐다.

Invert pair로 대상 토큰을 바꾸려는 단계에서 제어가 응답하지 않았다. DOM·화면 확인도 실패했고, 같은 사용자Chrome 프로필의 공식 재연결을 시도했으나 제어 연결이 복구되지 않았다. 최종 선택 상태와 과거 차트 수치는 확인되지 않았다(raw3899). 브라우저 초기화·인증 우회·숨겨진 API 호출은 하지 않았다. 이 문제를 시장 자료 자체의 부재로 해석하지 않는다.

CoinGecko 공식 변경기록은 검증되지 않은 onchain market cap이null일 수 있고 GeckoTerminal 표시값이FDV와 일치할 수 있다고 설명한다. 따라서 화면의 MCAP라는 글자만으로 검증된 유통 시총으로 승격하지 않는다. [공식 변경기록](https://docs.coingecko.com/changelog/10122018), [공식 풀 문서](https://docs.coingecko.com/reference/top-pools-contract-address); 원문 검색3900/문서3901. 이는 provider 동작 설명이며 DOGINU의 역사 시총 증명은 아니다.

기존 역사 발행 상한10억·권한 폐기, 완료 분봉 HIGH의 조건부$146,822.98/$435,103.58, 정확 거래의 가격 검산은 유지했다. `pending_cap_proxy`는 변경하지 않았다.

## 3. 다음 작업의 실제 조건

1. 사용자 기존 Fomo 로그인과 Chrome 제어가 확보되면 정확 Solstice 프로필의 과거 게시를 확인한다. 이전 로그인 요청은 그대로 유효하다.
2. 같은 풀의 화면을 복구하더라도 정확 DOGINU 대상·시점·유통 시총 원천을 먼저 확인한다. 현재 TKLS 값이나 FDV를 대입하지 않는다.
3. 이미 닫힌29개 DOGINU 성공swap/실패 합집합33개와 거래소·브리지 라벨은 재수집하지 않는다. 서비스의 전체 입출금이나 다른 계정으로 조사 범위를 넓히는 것으로 공백을 대신하지 않는다.

이번 원천 가용성 검토는 종료했으며 연구 목표는진행중이다. 로그인·접근이 회복되지 않은 동안 동일 실패를 반복하지 않는다. 같은 원천에서 확인하지 못했다는 사실과 거래 자체가 없다는 결론을 구분한다.

실제 사용: Chrome3/3, 공식문서2/2, RPC/Fomo/Bridge/시장API/BQ0. 기존82states/11wallet resolutions/4,569trades/626edges는 전체 값·경제행 해시로 보존했으며 새로운 state만 추가했다. 근거 raw3903/검토 raw3904/cap raw3902; state `initial_top10_DOGINU_independent_public_and_cap_source_availability_review_v1`.


## 배치051: 브라우저 복구와 공급 지갑의 실제 자금 출처

Chrome 제어가 복구됐다. 같은 정확 풀을 한 번 열고 `Invert pair`를 성공시켜 정확 DOGINU mint를 선택했다(raw3906). 최초 클릭은 전달 전에 응답하지 않았고, 새 화면 확인 뒤 한 차례 재시도해 전환을 확인했다. DOGINU/USD 1분 차트에서 2026-09-29 12:47(UTC+9), 즉 03:47 UTC를 지정했다. 과거 차트는 표시됐지만 선택된 봉의 날짜·가격과 역사 유통량을 독립적으로 연결하지 못했다. 현재 표시된 MCAP와 FDV는 모두$19,889.27이다. 이 현재 값으로 과거 시총을 확정하지 않는다. `pending_cap_proxy`, 엄격한 완결 사례0을 유지한다. 이전 배치의 제어 불가 설명은 당시 상황이며 현재는 제어가 가능하다. Fomo 로그인은 아직 필요하다.

공급 지갑 `3HpNWdgjK9yMLMbmJdpsZcx6iiK39hPrDzTFYc65oQdr`의 기존 owner 조회 raw3439는 **성공65행**이고 raw3440은 빈/null 종료 응답이다. 지정60일·tokenAccounts:none 조건으로 64개의 연속 잔액 비교가 모두 맞았다. 55라는 숫자는 DOGINU 선물 행의 인덱스이며 조회 전체 건수가 아니다. 전체 토큰 계좌·실패 거래·생애 이력까지 완결됐다는 의미는 아니다.

### 자금 흐름

|UTC|실제 전송|금액 SOL|원문|
|---|---|---:|---|
|2026-09-14T18:56:35Z|`F7p3…`→`3HpN…`|1.724688730|[거래](https://solscan.io/tx/4ZTbsXYhn1Q6ZWyMiKhWs86GEqk2o21eHeogbKMtJT8FqgVQbVbJsP6iQkV2iSDi3R6wUm1ahXzzQ3HvwHd3gecv) · raw3439 data0|
|2026-09-15T01:04:21Z|`3HpN…`→`7uTT…`|1.972652699|[거래](https://solscan.io/tx/5zr2ABKJe16GXGaVGLT7mJaoYDvZZraxxwQpqriFibaVkz8zbxvqtAGwyj7gZQVmopQp2F6gpTfqftLG7yvxFgHe) · raw3439 data11|
|2026-09-15T01:42:07Z|`F7p3…`→`3HpN…`|1.824579314|[거래](https://solscan.io/tx/2xSrtFEedpTCWGydtLW1YhmQmPbTfmYpyFESvEr96SVmSVJaMdW2N8CHaHxtYD3mDk1DAQBXj4Vss6H8KTHhqSzY) · raw3439 data13|
|2026-09-15T23:43:00Z|`3HpN…`→`7uTT…`|1.366935672|[거래](https://solscan.io/tx/gTvz586ca2NnEATRTgnj8FhQr3Z1y6re1kmsWpY6kmewGWX1ippjm51f7g7Z1UbbbyztvaZwwfGJLzBwCRRHwS9) · raw3439 data19|
|2026-09-18T16:18:40Z|`F7p3…`→`3HpN…`|0.960483554|[거래](https://solscan.io/tx/2yLDxjTjrK7rsXUGNeJYeAAebXi9bkdBGmwA972LaNfQjXZbqmfwaDgUjNDbKTdXmXupqNqM5dvHV84BJfMVzskV) · raw3439 data20|
|2026-09-25T16:55:31Z|`3HpN…`→`3Nyy…`|1.269195999|[거래](https://solscan.io/tx/3aG5na6oM87Tb4dHNBWE5uRmip6gzMiNAU1rjxTw9CWgswkSQhviosgE6gjZiLKB1EEfYjBPz6bY1J43CcXJEhnU) · raw3439 data62|

F7→3Hp 3건은 합계 **4.509751598 SOL**이고 각각 32바이트 메모 두 개가 붙었다. 이는 주문을 찾을 수 있는 실제 단서이며 원래 출발 지갑이나 CEX 계정이 확정된 상태는 아니다. 메모가 Relay의 어느 필드와 대응하는지, 실제 origin과 destination이 맞는지 다음에 검증한다.

3Hp→7uTT 2건 합계 **3.339588371 SOL**은 source signer와 실제 native 감소·수수료가 일치했다. 7uTT는 raw3887의 현재 Arkham Relay.link 브리지 라벨이 있으므로 공통 CEX 고객 입금으로 분류하지 않는다. 두 건은 DOGINU 매수보다 앞선 거래이며 DOGINU 수익 회수로 표시하지 않는다.

3Hp→3Nyy **1.269195999 SOL**은 이미 canonical에 저장된 동일 거래라 추가하지 않았다. DOGINU 공급 뒤 일반 송금이라는 사실만으로 매도 대금의 동일 lot 또는 CEX 현금화를 증명하지 않는다. 기존 임시 WSOL 계좌 Hxepa의 wrap/route는 다른 지갑으로의 송금 집계에서 제외했다.

이 6개 송금은 저장된 indexed 원문에서 signer·payer·명령·금액·잔액식을 확인했다. 이번 배치에서 새 독립 RPC 증명을 추가했다고 주장하지 않는다. 원래 자금의 소유자·공모·손익은 unknown을 유지한다.

다음은 새로 발견한 메모에 따른 **실제 주문별 출발 주소 검증**이다. 과거 게시 확인이 로그인에 막혔다고 원문 없는 상태를 활동0으로 해석하지 않는다. 신규 전체 토큰/BQ 수집과 Top100/RZD 재개는 실행하지 않았다.

근거 raw3908, 검토 raw3909, cap raw3907. Chrome1, RPC/Fomo/Bridge/시장/BQ0. 기존83states/11wallet resolutions/4,569trades/626edges 전체값 및 경제행 해시를 보존했고 state만 하나 추가했다. 전체 연구 목표는 진행 중이다.
