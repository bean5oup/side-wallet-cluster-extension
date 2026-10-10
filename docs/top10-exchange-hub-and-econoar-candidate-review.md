# 초기 Top10 — 공통 거래소 주소의 역할과 econoar 새 후보

## 이번 판정

**공통8zHc는 개인 고객의 동일 입금 주소라는 근거에서 제외하고, 거래소·서비스의 집금 지점일 가능성을 높여 평가했다.** 실제3Hp와4j9k의 전송 경로는 그대로 유효하다. 새로 연 상세 화면 raw4014의 현재 거래량·많은 상대 주소·Binance Hot Wallet 출금은 여러 고객이 공유하는 지점이라는 대안을 강화한다.

**econoar의 실제 Ethereum 자금 송신자 `0xbfd…5c3b`에서 ORBIO/WORM 취득 후보와 Fomo 주소로의 전달, ZZZ 역방향 반환이 처음 보였다.** 거래 해시가 있으므로 다음 개별 검증 대상으로 삼을 수 있다. 현재 화면 정보는 제공자 assertion이며 정확 시각·정수 금액·토큰 계약·영수증을 아직 검증하지 않았다. 소유자 라벨 `@econoar?`는 화면 자체가 **LOWER CONFIDENCE PREDICTION BY AN AI MODEL**이라고 표시하므로 채택하지 않는다.

엄격한 완결 사례는0건이다. 이미 승인된 개별 BUY raw2286/2893/2933의 시총 적격성과는 별도 값이다. 범위는 원래 Top10/raw141 및 고정60일 `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z`이다.

## 1. 공통8zHc를 개인 입금 근거로 쓰지 않는 이유

정확 주소는 Solana `8zHcWujHhyJri3CRTcWUGmT5WSRdwW7xrns3WTTkPGvS`다. 현재 Arkham header는 **Binance Deposit / Binance Deposit Address Solana**다. 같은 화면에 다음이 나타났다.

|현재 화면 관측|해석의 한계|
|---|---|
|Top counterparties `LAST7D`, entity grouping, `showing0-100of101items`|개별 고객 수나 역사 전체의 고유 주소 수가 아님|
|Binance 그룹 `2177 / $33.08M`|UI 집계이며 원가·수익·연구 지갑의 금액이 아님|
|Transfers `1/625`와 USD≥1 필터|화면 페이지 수이며 고정60일 전체 회수 완료가 아님|
|여러 새 주소의 반복 유입과 `Binance Hot Wallet(5tzFk)` 출금 표시|공용 집금 구조라는 대안을 강화; 개별 고객 귀속 증명은 아님|

이 관측은 현재의 제공자 화면이다. 과거9/25–30에도 같은 고객 구성이라는 주장은 하지 않는다. 실제 [3Hp→3Nyy→8zHc 및4j9k→네 중간주소→8zHc](doginu-supplier-solana-binance-deposit-review.md)는 독립 전송 근거가 있지만, **집금 주소가 같다는 사실만으로 뒷지갑 소유를 연결하지 않는다.** 새로운 전체 pooled 거래·모든 상대 주소로 확장하지 않았다.

## 2. econoar의 새 실제 조사 단서

검증 Ethereum Fomo 지갑은 `0x1605b59dfe3c1742c815d604aab6a2faa3a5c91f`다. 실제 별도 송신자 `0xbfd26274e94cbc3826d25f3217d4a756a8c25c3b`가 **10/2 01:36:59Z,0.005ETH**를 보낸 것은 기존 독립 receipt/block raw2238/2239/2241과 [거래](https://etherscan.io/tx/0xd6ff714452f4d8174cbed3c5048363c44498cedaf9386d684cb8295330fac66d)로 확인돼 있다. 가스 공급·일반 송금 등 여러 목적이 가능하며 이것만으로 토큰 매집 자금을 입증하지 않는다.

이번에는 바로 이 송신자의 [Arkham 주소 화면](https://arkm.com/explorer/address/0xbfd26274e94cbc3826d25f3217d4a756a8c25c3b)을 처음 확인했다(raw4015). 화면에 보이는 정확 해시를 보존했다.

|UI chain·후보|화면 방향|정확 거래|
|---|---|---|
|Robinhood ORBIO 취득 후보|bfd의 USDG 지출과 bfd ORBIO 수령이 같은 hash|[f7eb…1921](https://arkm.com/explorer/tx/0xf7eb376b02013923d7fec490e49ee9b1154d65de9fa2814095f56cdcaf1b1921)|
|Robinhood ORBIO 전달 후보|bfd → 정확1605 Fomo 라벨 주소|[e6d9…ff02](https://arkm.com/explorer/tx/0xe6d9b5be04e54a6da1e7a7c1b31c06cd28d3303b94f261a5ff504848ffe3ff02)|
|Robinhood WORM 취득 후보|bfd의 USDG 지출과 bfd WORM 수령이 같은 hash|[2401…dd47](https://arkm.com/explorer/tx/0x2401a39c07890707e31f7db6ba043b1f607652f97df7fcf2b571a445d8b5dd47)|
|Robinhood WORM 전달 후보|bfd → 정확1605 Fomo 라벨 주소|[428e…0912](https://arkm.com/explorer/tx/0x428e8d19b181d48909f31906524d979308f56191c506f959b20c11fc1d7f0912)|
|Robinhood ZZZ 반환 후보|1605 Fomo 라벨 주소 → bfd|[dd5b…daed](https://arkm.com/explorer/tx/0xdd5b9bfa0861ac7a1b0430374879588d07697e8c584383343a12e783f4c5daed)|

`1.525M/3.031M/6K` 등의 표시는 반올림 수량이다. 현재 표시 USD를 실제 원가·실현 수익으로 쓰지 않는다. 단순 두 transfer의 같은hash 조합을 실제 유상 BUY로 확정하지도 않았다. 정확 ERC20 계약·실제 자산변화·대가·성공 영수증·작성자 공개 시각을 다음에 확인해야 한다. Ethereum에서 검증된1605를 다른 체인의 Fomo 지갑으로 자동 새 resolution 등록하지 않았다.

추가로 Coinbase Hot Wallet→bfd의 Arbitrum USDC125K, bfd→LiFi Permit2Proxy, Robinhood Relay Solver→bfd USDG 화면 후보가 있다. source/order/destination 검증은 아직 없으며, **Coinbase→지갑 방향은 거래소 출금이다.** 이를 CEX deposit 또는 같은 고객 증명으로 바꾸지 않는다.

## 3. 보존된 공개 기록과 비교 준비

SQLite의 같은 사용자·고정 구간에서 ORBIO/WORM/ZZZ11개 이벤트(THESIS5,BUY6)를 재사용했다.

- WORM THESIS: **2026-09-18T21:07:45Z**, chain4663, contract `0x3ba500f1ababbcf0f0247d06d1c56fd7e6c4c09d`, raw2170.
- ZZZ THESIS: **2026-09-18T14:43:05Z**, chain4663, contract `0x7dbf38976f6d3b9c529e7d9484a71898b409ee6a`, raw2170.
- ORBIO 최초 보존 THESIS: **2026-10-06T02:34:05Z**, 같은 날04:08:20와22:44:00의 추가 보존 THESIS. chain4663, contract `0xaa07a0e9209e16ac99708c3ec70159c6ef3128a3`, raw673/2154/2170.
- ORBIO BUY는10/3~10/6 사이6개 보존 이벤트다. 개별 체결 횟수나 실제 bfd 취득 횟수와 동일시하지 않는다.

이는 확보된 공개 기록이며 절대 최초 공개가 아니다. **현재 UI 토큰 이름·체인만으로 exact contract를 맞춘 상태는 아니다.** 다음에 거래의 실제 token contract가 이 값과 같고, 실제 취득이 공개보다 앞인지 대조한다. 서로 다른 같은 이름 토큰은 합치지 않는다.

## 4. 원래10명의 남은 범위

기존3개 Luna/max가 네트워크 없이 현재 저장 근거를 감사했다. ARTHUR selected62 및Werey47,612USDC, 지정 F5/DET/Rare/pricedin query의 종료를 유지한다. WOOF의 마지막 raw2759까지15+78+35=128 ERC20행은 지정 고정 구간에서 닫혔으며 old tail을 다시 요청하지 않는다.

F1b의 PURR 최종 처분 뒤10USDC→DXAh와115USDC→3TW6의 실제 송금은 저장돼 있으나 recipient 역할은 미확정이다(raw3200 data512/516). 같은 저자·CEX·토큰 수익 연결 근거가 없고 소액이므로 econoar의 구체적 신규 토큰 경로 뒤에 둔다. PURR/SI 기존 cap 조회404·빈 배열·stale 표본은 보존하며 동일 실패를 반복하지 않는다.

DOGINU/5NS의 매수·재고·게시 후 매도는 가장 가까운 행동 사례지만 이벤트 시총과 사적 관계·원가가 남는다. CALI/Ek의 게시 뒤 LP 회수는 같은 토큰 직접 SELL과 구분한다. EMBER4j9k의48매도는 전부 보존 THESIS 전이다. RunningClam/Fomo 과거 로그인 및Robinhood 기존RPC403의 공백은 아직 해소하지 못했다. **전체 연구 범위가 소진됐다고 선언하지 않는다.**

## 5. 다음 작업과 보존

새 예산에서 econoar의 네 정확 취득·전달 거래 상세를 확인한다. 기존403 endpoint를 그대로 재요청하지 않고 Chrome의 실제 chain explorer·가용한 독립 증거를 쓴다. 거래가 살아남으면 같은 별도 지갑의 공개 시점 재고·게시 후 처분을 확인한다. 당시 유통 시총≤1M 조건을 통과하기 전 전체 토큰 군집·BQ 조회는 없다.

브라우저 raw4014/4015, worker raw[4016, 4017, 4018], cap raw4019, 근거 raw4020, 검토 raw4021. Chrome2회, 다른 신규 외부 요청0회. 신규 경제 행0: 실제 trade4,569·edge645·resolution11과 기존 state91개의 값을 보존하고 검토 state1개를 추가했다. AI 소유권·CEX 고객·수익 판정은 생성하지 않았다. 사용하지 않은 예약은 해제했다. 전체 goal은active다.
