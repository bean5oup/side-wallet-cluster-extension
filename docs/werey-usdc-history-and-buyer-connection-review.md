# Werey 본지갑 USDC 이력과 ARTHUR 매수 지갑의 자금 접점

## 결론

미확보였던9/11~9/29 구간18,345행을 확보했다. 기존20,000행과9/29 이후9,267행을 합쳐 **47,612개 고유 거래**를 대사했으며, 정확 USDC 계좌 잔액의 인접 비교47,611회에서 불일치는0이다.

조사한62개 ARTHUR 매수 지갑과의 접점은 **총93개 토큰 전송 명령**이다. 모두 같은 거래 안에 swap/route가 있어 수수료·referral·정산 대안을 배제할 수 없다. **이 지정 USDC 계좌에서62개 지갑으로의 독립적인 일반 원금 송금은 확인되지 않았다.** SOL·다른 토큰 계좌·중간 지갑·다른 체인의 자금 관계까지 없다는 뜻은 아니다.

## 1. 조회 범위와 계좌 대사

검증 Werey 주소 `DmopudSGaQQenK4cW5NgmHUsexMB3sEJNn6n1EfLKs28`, 정확 USDC ATA `EiRmHBhQEx3KKXohp3rLpay5DARpshYZUqSy34XCmfWk`. 고정 요청 구간은2026-08-08T04:43:41Z부터2026-10-07T04:43:41Z 미만이다. 성공 거래·tokenAccounts=none·지정 계좌만 조회했다.

|구간|행수|근거·종료|
|---|---:|---|
|기존 prefix|20,000|raw3143–3162, saved cursor446194389:216|
|신규 이어받기·9/29 미만|18,345|raw3255–3273, 3274HTTP503 뒤1회 재시도3275 빈/null footer|
|기존9/29 이후|9,267|배치029의 지정 query와 빈/null footer 재사용|
|합계|47,612|구간 간 signature 중복0, 정확 잔액 연속성 불일치0|

첫 반환은8/24 01:46:19UTC, 마지막은10/7 04:43:27UTC다. 첫 거래raw3143 data0에는 해당 ATA의 create·createAccount·initializeAccount3가 있고 owner/mint가 일치한다. 처음 pre0, 마지막 post **15.175564USDC**다. 이 사실은8/24에 관측된 생성·초기화의 근거이며, 다른 USDC 계좌나 지갑의 최초 생성·평생 기록·제공자의 과거 archive 완전성을 대신하지 않는다. **지정 query 합성은 종료했으며 전체 지갑 연구 종료는 아니다.**

## 2. 새 구간의4개 매수 지갑 접점

신규12개 전송은11개 지갑→Werey 합계 **46.004339USDC**,1개 Werey→CS4 **0.38USDC**다. 정수 원문·역사 token-account owner·실제 source authority 서명·성공 상태를 확인했다. 전송 명령 수량과 상대 지갑의 전체 거래 순잔액 변화는 서로 다를 수 있다. 같은 거래 안의 swap이 추가로 잔액을 바꾸기 때문이다.

|상대|방향과 전송 명령 합계|판정|
|---|---:|---|
|Gqvnd|2회→Werey0.460176USDC|DF1ow swap에 결합|
|Fxb5|1회→Werey0.236179USDC|DF1ow swap에 결합|
|CS4|7회→Werey45.108USDC,1회 역방향0.38USDC|DF1ow/Jupiter route에 결합|
|2mKwu|1회→Werey0.199984USDC|DF1ow swap에 결합|

62개 지갑의 전체93개 접점도 같은 기준으로 모두swap-context였다. 따라서 이를 본지갑의 뒷지갑 원금 공급·공동 소유로 저장하지 않았다. 전송 근거와 역할 판단을 raw audit에 별도로 남겼다.

### CS4가 다음 후보인 이유

정확 주소 `CS4RaxAyQYes9fHStTXc1hErzhByVsxWDKaASnigNyUd`. 기존 종료된 ARTHUR 대상 계좌에서 게시 전57BUY/0SELL, THESIS 순간 **30,121,906.732082ARTHUR**, 게시 후3SELL **5,081,386.533340ARTHUR**와 net **2,785.420407USDC** 수령, 최종25,000,000ARTHUR 잔류가 확인됐다. 게시 후 대상 추가 매수는 없다.

다만 가장 이른9/30 매수의 당시 cap은pending이다.10/2의 두 후속 BUY만 이벤트별100만달러 이하 cap 근거가 있고, 이를 첫 매수나 THESIS 시총에 소급하지 않는다. 9/22의 Werey→CS4 0.38은같은 swap 흐름이며 매수 원금 관계의 증거가 아니다. 다음은 **CS4의 정확 USDC 계좌에서 매수 전 자금 유입과 매도 후 회수**를 확인하는 것이다. 이미 닫힌 ARTHUR 계좌와 Werey quote는 다시 수집하지 않는다.

## 3. 큰 공통 송금과 서비스 대안

정확 USDC query의 swap 외 parsed 전송은892개 명령·57개 상대다. 상당수는 이미 검토된 deposit/bridge/service 경로다. 예를 들어 F7의307개 직접 수신 합계699,859.702540USDC는 실제 전송량이지만, 같은 F7 source가 여러 unrelated 매수 지갑에 보내는 기존 공유 서비스 근거가 있다. **공용 서비스의 전체 자금을 Werey의 개인 공급자·소유 관계로 귀속하지 않는다.** 7u·3y·Fv 등은 명령·서명·서비스 역할·주문 근거를 각각 구분한다.

기존Werey→F1bNo8,000USDC와반대200USDC는 독립 일반 송금의 근거로 유지한다. F1bNo의PURR/SI 게시 전 유상 매수·게시 후 매도·6vy→Binance 라벨5tz 경로는 [별도 보고서](werey-funded-wallet-inventory-and-cex-review.md)에 있다. 그 당시 시총·실질 소유·고객 입금 주소·의도·USD 수익은 여전히 미확정이다.

## 4. 저시총 조건과 저장

외부 실제 ARTHUR BUY corpus1,912개 고유 signature 중 이벤트별cap은30eligible/25초과/1,857pending이다. 본지갑raw2286의 적격 BUY1개는 이 외부 corpus와 별도다. THESIS cap은pending이다. 시총의300초는 표본 품질 조건이며 선행매수 탐색 기간을 제한하지 않는다.

근거raw3282/검토raw3283/시총검토raw3281, state `initial_top10_Werey_USDC_gap_and_62buyer_route_intersection_review_v1`. RPC21/30(503과재시도 포함), 다른 신규 source0, 미사용9해제. 5Luna-max는 읽기 전용·외부0으로 검토했다. 신규 canonical spot trade/edge/Fomo event는0이며 이전64states·11wallet resolutions·4,540trades·465edges·Fomo1,338/고정404events·matches73을 보존했다. 원문과 모든 정확한 전송·잔액·수수료 대안·footer를 SQLite raw와ignored 배치 산출물에 저장했다.

엄격한 완결 사례는 아직0이다. 원래Top10·60일·유통 시총100만달러 이하 범위를 유지해 적격 실제 BUY의 별도 지갑 자금 출처·회수를 이어간다. 소유·의도·고객 귀속·USD/PnL은 확정하지 않는다.
