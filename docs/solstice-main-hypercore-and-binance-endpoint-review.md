# Solstice 본지갑의 Hypercore 출금과 정확 Binance 주소 대조

## 배치055 결론 — 확보된 출금 10건의 목적지 확인 완료

확보된 공식 Hypercore ledger 64행 중 d1c에서 공용 Relay 주소 66cf로 나간 **출금 10건, 총 150,165.576050 USDC는 모두 검증된 Fomo 본지갑 4ug로 돌아왔다.** 이번에는 미조회 4건, 합계 15,205 USDC를 추가 확인했다. 10건 모두 개별 Relay 주문을 대응했으며, 이번 4건은 독립 Solana RPC로 성공 상태, 수령 계좌의 당시 소유자, 정확한 잔액 증가, 두 주문 메모를 확인했다.

이로써 **이 ledger에 있는 출금 10건의 목적지 조사**는 끝났다. 해당 계정의 모든 자산·모든 기간이나 연구 전체가 완성됐다는 뜻은 아니다. 이 10건에서 공급자 3Hp가 사용한 정확 Ethereum Binance 입금 주소 `0x487cab40f6d11a278fa7c442c6741eabe44eab5d`와의 공통 귀결은 확인되지 않았다.

### 이번에 확인한 4건

|Hypercore 출발 UTC|본지갑 실제 USDC 수령|거래|Relay / 독립 RPC raw|
|---|---:|---|---|
|2026-08-22T04:54:31Z|11000|[Solana 수령](https://solscan.io/tx/4Wv9X2MJeBtdqR5eKkfRpJ5cVhB6CVeK7KqjWRTCQeRSMq5qbapHM9vQwMrF2BjFeb7kczTaxGrLSLdedEtEW8CP)|3965/3966|
|2026-08-22T01:34:24Z|2000|[Solana 수령](https://solscan.io/tx/5oxPrGF25HYPUdjVebUGdomuhdXstik8C3vLynJiynELLvGYMWsjjSTq1M9A8weMjGAJ1hojpiJ6PneyHqCKTtHs)|3967/3968|
|2026-08-22T23:40:52Z|700|[Solana 수령](https://solscan.io/tx/7WYyLTf9yBx618nfwbH3QSgGVFcedwu6sMtKgrRokPwJpGxaSW7VEB1cY6bomQBUdiRJsAHjXaMCnWCh91qvVpo)|3970/3971|
|2026-08-19T17:22:51Z|1505|[Solana 수령](https://solscan.io/tx/4t9MXXrY4dPHwNJFfeTLcC4csEqbjxWhHo84x9qppuBr3aJxGKsGa92DXyttkxusHjxihip9GGvWhy512hohTLaF)|3972/3973|

source raw2327의 행13·12·18·7을 각각 확인했다. Hypercore Spot 원금의 provider d8 표현과 Solana USDC d6 정수량을 구분해 Decimal로 대사했으며, 메모는 정확한 Relay request ID와 order ID에 맞았다. 원금 합계는 **15,205 USDC**다. Hypercore 출발은 공식 ledger 증거이며 EVM receipt로 주장하지 않는다.

### 사례의 핵심과 남은 연결

현재 가장 강한 행동 사례는 **공통 공급자 3Hp → Solstice 본지갑 / 별도 5NS 토큰 전송**, **5NS의 보존 THESIS 이전 유상 매수 4건**, **THESIS 110초 뒤부터 같은 5NS의 매도**, **후속 5NS → HN88 → B48 송금**이다. 첫 6매도에서 추가 매수 없이 기존 재고를 팔고 quote 12.041207311 SOL을 받은 사실은 확인했다. 공급된 물량의 대가·원가와 소유권이 미확정이므로 이를 실현 이익으로 쓰지 않는다.

공급자의 `3Hp → Relay → Ethereum 213d → 3081 → 487` 입금은 9월15일로, 5NS의 첫 DOGINU 매수인 9월23일보다 앞이다. 이 입금을 DOGINU 게시 후 수익 회수로 연결할 수 없다. Binance 역할은 현재 Arkham/Etherscan의 라벨이며 같은 고객 계정의 증명은 아니다.

5NS 이후 B48는 다수 출처의 자금이 섞이는 주소다. 기존에 닫힌 20분 자료에서 이후 출금 5건은 금액이 다르고 다른 입금이 끼었다. 공용 자금 전체를 5NS에게 귀속하지 않는다. 다음은 이전 로컬 aggregator가 해결하지 못한 **5NS → HN88 / HN88 → B48의 두 정확 signature**를 공개 Relay 개별 주문 조회와 처음 대조하는 것이다. 주문이 없거나 조회가 실패하면 이 경로의 연결은 미확정으로 남긴다.

### 저장 및 한계

- 신규 BRIDGE 4건: edges 640 → 644. 기존 87개 상태, 지갑 resolution 11개, 거래 4,569개, 기존 edge 640개의 전체 값을 보존했다. 신규 검토 상태 1개를 추가했다.
- Bridge 실제 시도 5회에는 HTTP429 1회와 그에 대한 재시도 1회가 포함된다. RPC 4회. 브라우저·Fomo·시장·BigQuery 신규 요청은 0회다. 사용하지 않은 예약은 해제했다.
- 기존 Luna 5개는 저장 자료만 검토했다. 검토 중간에는 반환 8건으로 집계됐으며, 최종 본체 검증으로 10건까지 닫았다. 작업자 중간 결과는 당시 상태로 보존한다.
- 과거 Fomo 공개 이력과 역사적 유통 시총은 미확정이다. cap 상태는 `pending_cap_proxy`, 엄격한 완결 사례는 0건이다. 소유권·동일 CEX 고객·악용 의도·실현 수익은 확정하지 않는다. 전체 조사 가능 범위를 소진했다고 선언하지 않는다.

근거 raw3980, 검토 raw3981, cap raw3979, 작업자 raw[3974, 3975, 3976, 3977, 3978]. 현재 목표는 진행 중이다.

---

## 이전 배치054 기록


## 이번 판정

**본지갑과 실제 bridge로 연결된 Hypercore d1c의 미해결 출금4건, 합계123,001.449316 USDC는 모두 검증된 Fomo 본지갑4ug로 돌아왔다.** 같은 정확 Ethereum Binance입금 주소487을 함께 썼다는 증거는 이번4건에서 없었다. 이는 다른 목적지 후보를 제거하는 결과이며 별도 공급자의 소유나 의도를 확정하는 결과는 아니다.

원래Top10/raw141·고정60일 2026-08-08T04:43:41Z 이상–2026-10-07T04:43:41Z 미만을 유지했다. d1c의 별도 소유자 신원은unknown이다. 5개 기존 작업자 gpt-6-luna/max는 저장 자료만 검토했고, 본체가 네트워크 요청과 최종적재를 담당했다.

## 실제 반환과 검증

|Hypercore 출발UTC(표시는초단위)|본지갑 실제USDC수령|거래|Relay/독립RPC raw|
|---|---:|---|---|
|2026-08-23T20:40:59Z|48517.933593|[Solana 수령](https://solscan.io/tx/3uZg9KGgnu1W66NunHDajLXgmEtiF7rZG7hoovV52ChgfjkKyQ6SKmmbwkDn2CcdoSfBqe8TSXouyQYnfkRmpxeP)|3947/3950|
|2026-08-15T04:23:04Z|45756.248246|[Solana 수령](https://solscan.io/tx/3BtKYAcm59WS6wcNQV2sa334fVPTC83SwDcJ1G5oHCRhjRwdRvaG9hDSuPcqCAFKKdBT9PvppYrqg1bbVMhsuVDU)|3948/3951|
|2026-08-22T09:21:26Z|17000|[Solana 수령](https://solscan.io/tx/4iSfd8ZexsoefKnK4TtBWTYHuMmDvaqBYNzds3Q6Qnvvsh8M8Bbrxh8QPTrCruXnNGAcFayup7PLn49uUUeUeTCE)|3952/3954|
|2026-08-20T10:41:41Z|11727.267477|[Solana 수령](https://solscan.io/tx/4h5rKE4y5bHVREUEt4qqiD1RJiS7qgu89pmYzAxadthc1RdKHVe9K7dCmSuaFGP4AHmSki4Z2KpxzKhiMgnhzyDk)|3953/3955|

원래 송금 ledger는 raw2327/response/19·1·17·8이며 milliUTC는 원문과 canonical에 보존했다. 실제 Relay deposit hash/depositor/amount와 해당 ledger를 맞췄다. Hypercore USDC(Spot)의 protocol d8 raw와 Solana USDC d6 raw를 분리했고 같은 Decimal금액을 확인했다. source d8은 provider의Spot단위 매핑이며 EVM ERC20 receipt의 정수 raw로 주장하지 않는다.

도착4건은 독립 공개 Solana finalized transaction의 성공meta·slot·UTC·parsedtransfer·destination owner의 역사 pre/post token balances를 확인했다. 실제 두Memo는 각각 정확orderID/requestID와 맞았다. main USDC destinationATA GhE45의 당시owner는4ug다. pooled F7 전체유입을 추정해 개인에게 귀속한 것이 아니다.

기존10,613.661096/1,345.465638 USDC 두 반환까지 합하면 ledger64 중 **outbound10개150,165.576050 USDC**에서 **6개134,960.576050 USDC**의 본지갑 반환 목적지를 확인했다. 남은4개 **15,205 USDC**는 아직 주문 조회를 하지 않았다. 실패했거나 부재라고 판정하지 않는다.

## 남은 정확 주문

|raw2327 row|sourceamount USDC|정확sourcehash|
|---|---:|---|
|7|1505.0|`0x48602b293d01f70d49d904428606700201f8000ed80515dfec28d67bfc05d0f7`|
|12|2000.0|`0x8632a06e31f5673487ac0442b16b9c0204430053ccf8860629fb4bc0f0f9411f`|
|13|11000.0|`0x2300bef70e0200a2247a0442b4000f02032d00dca9051f74c6c96a49cd05da8c`|
|18|700.0|`0x4ec605b56f578377503f0442c288010201d0009b0a5aa249f28eb1082e5b5d61`|

다음에는 이4개를 개별 주문으로 확인한다. 이미 확인한6개를 재요청하지 않는다. 공용 Hypercore66cf의 전체 flow를 확장하지 않는다.

## 별도 공급자 경로와의 차이

[공급자 보고서](doginu-supplier-crosschain-wallet-review.md)의 **3Hp→Relay→Ethereum213d→3081→eip155:1/487**은 실제9/15 자금 이동이다. 현재 Arkham/Etherscan은487을 BinanceDeposit으로 표시한다. 그러나5NS의 첫 DOGINU 유상매수는9/23이므로 그 선행매수의 이익 회수로 쓸 수 없다. 5NS는보존THESIS110초후SELL/quote를 실제로 받았고 이후5NS→HN88→B48 송금이 있지만, B48 이후 같은487로 이어지는 개별tx/order는 미확보다.

작업자 exactaddress 비교에서213d/3081/487은11walletresolutions 등록주소와 일치하지 않았고, 기존경제movement/discovery에서도 다른 Fomo 계정 endpoint 접점이 없었다. 연구context가Solstice라고 기록된 것과 작성자 본인 소유 증거는 별도다. 같은 Binance 이름·sharedhotwallet·Relaysolver만으로합치지 않는다.

## 감사·접근 한계

- Luna4는 기존ETH3건value/fee/residual/UTC288s·24s/메모source를 독립 재계산해 일치했다. ETH증거는Etherscan indexed UI/state이고 직접EVM RPC는아니다. 5042공급주문은 routeoutput107,463,703raw/d6와 protocolorigin107,463,704raw/d6 사이 **1raw-unit 차이**가 남아 실제origin토큰수량 독립증명으로승격하지않는다.
- d1c Arkham탭은 실제열렸지만 두관측단계가timeout/kernelreset돼 라벨/활동unknown(raw3946)이다. 같은실패를추가로반복하지않았다. 최초로컬DBsave는readcursor잠금으로rollback됐고읽기종료뒤한번저장해capture를보존했다. DB설정/저널변경0이다.
- Bridge세번째lookup429은다른증거작업뒤한번재시도해성공했다. 총5attempts에는실패1+재시도1가포함된다. RPC4/8,Chrome1/3. Fomo/BQ/시장신규0이다.
- Fomo로그인/과거public확인과역사유통cap≤$1M은미확정이다. `pending_cap_proxy`, 엄격완결사례0을유지한다. missingAPI/source를활동0으로바꾸지않는다. 전체조사가능범위를소진했다고선언하지않는다.

작업자5개검토raw[3956, 3957, 3958, 3959, 3960], 근거raw3962/검토raw3963/capraw3961. 신규BRIDGE4로edges636→640/state86→87. 기존86states/11walletresolutions/4,569trades/636edges 전체 값을보존했다. 거래소고객·지갑소유·의도·PnL은unknown이다.
