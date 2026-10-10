# 초기 Top10 — 완결 조건과 조사 범위 감사

## 판정

**완결 사례는 아직 0건이며, 조사 가능한 전체 범위를 소진했다고 입증하지 못했다.** 이전 goal 실행은 Hypercore 10개 주문의 목적지를 닫고 신규 독립 proof를 저장해 실제 진전이 있었다. 이번에는 원래10명의 닫힌 조회를 다시 수집하지 않도록 감사하고, DOGINU의 새 독립 역사 시총 원천을 실제로 조회했다.

`완결 사례 0`과 `시총 적격 매수 이벤트 0`은 다른 값이다. Werey/ARTHUR actualBUY raw2286, 31D raw2893, GBh raw2933처럼 개별 매수의 역사 시총 조건을 통과한 이벤트가 있다. 그러나 작성자와 연결된 별도 지갑의 전체 매수·보유·게시 후 처분·원가가 함께 입증된 저시총 사례는 0건이다.

## DOGINU 새 독립 시총 조회

정확 mint `5JgioXRQSq1Nw4VJvpRyXxnvm8jVtLSUC7vbf1zzDg3L`에 대해 공개 CoinGecko contract-address market-chart-range를 **처음** 조회했다. 보존 THESIS 전후30분(UNIX1790651875~1790655475), currency USD였다. **raw3993: HTTP404, `coin not found`, market_caps 없음.** 해당 제공자의 이 정확 요청에서 자료를 확보하지 못한 결과이며 토큰이 없거나 당시 시총이0이라는 판정은 아니다. 재시도하지 않았다.

[GeckoTerminal 공식 FAQ](https://apiguide.geckoterminal.com/faq)는 token price가 top pool의 가격이며 미등재/미검증 공급의 market cap은 null이라고 설명한다. [CoinGecko 공식 역사 차트 문서](https://docs.coingecko.com/reference/contract-address-market-chart-range)는 historical price/market cap을 반환하지만 과거 날짜의 자동 간격은 시간 단위이고, 더 촘촘한1m/5m는 Enterprise 조건을 제시한다. 새 구독·유료 요청 없이 공개 경로의 실제 가용성만 확인했다. 공식 문서 원문 raw3990~3992를 보존했다.

정확 DOGINU mint 분봉 raw3484/85의 첫 매수·THESIS 직전 종료 표본은 각각98초/55초로300초 운영 가정 안이다. 다만 단일풀 price와 공급상한의 곱은 계속 `pending_cap_proxy`다. 나머지 두 사전 BUY는 직전 완료 분봉이 각각19분32초/32분51초 전이며 해당 BUY를 포함한 미완성봉의 HIGH를 과거 확정값으로 쓰지 않는다. 발행1B와 mint권한 폐기는 raw3470/3475로 확인됐지만 정확 유통량·시장 전체 가격의 증명과는 별도다.

## 원래10명 범위의 재확인

5개 기존 Luna/max가 네트워크 요청 없이 저장된 결과를 감사했다. 완전한 capture는 재요청하지 않았다.

- ARTHUR selected external buyer 62개 exact target query는 닫혔다. 이들과 Werey USDC의93개 접점은 swap/route/fee 맥락이며 plain 사적 공급으로 승격하지 않았다.
- Werey exactUSDC47,612개 행으로 구성한 지정 query는 닫혔다. 예전 부분 cursor를 새 미완료 작업으로 재사용하지 않는다.
- Rare/pricedin 지정 owner1,121/776, theveeman의 F5 2,225, DET 지정 원천 query의 footer를 확인했다. 이는 모든 ATA·모든 체인·평생 이력의 완성은 아니다.
- F1b는 실제 Werey8,000→F1b→Werey200USDC 연결과 PURR/SI의 별도 매수·게시 후 매도가 있다. 해당 이벤트 시총은 pending이다. F1b의 ARTHUR는 보존 THESIS 시점 재고0이며 게시 후 거래도 지정 범위에서 미관측이다.
- 3yUM owner577에서는 ARTHUR delta0과 selected62에 대한 직접SOL/USDC 공급0을 확인했다. sQBw/YCWax 지정owner/USDCquery는 닫혔다. 일반 송금 접점을 유상 ARTHUR 선매수로 바꾸지 않는다.
- DOGINU의3Hp→4ug/5NS 실제 토큰 공급과5NS 자체매수·보유·게시 후매도는 유효한 행동 근거다. 동일소유·원가·악용 의도는 미확정이다. 새 private/control edge는 이번 감사에서 발견하지 못했다.
- RunningClam/econoar 등 원래 다른 계정의 체인 접근·quote·시총·공개 이력 공백은 유지한다. 단독RZD는 중단 상태이며 Top100으로 확장하지 않는다.

작업자 개별 결과는 `data/research/parallel/top10-60d-20261010-v1-batch057/luna_1~5/`에 보존했다. 범위 소진 여부는 전체 goal과 비교해야 하며 query footer 하나로 대신하지 않는다.

## 다음 실제 조사 대상

공급자3Hp의65개 성공 source 거래 중 **9/25 16:55:31Z → 3Nyy 1.269195999SOL** 일반 전송(raw3439 data62)은 기존에 확인된 실제 경제 관계다. recipient 주소는 `3Nyyv4d5G4SxkgefYsjKEfV4FxSLmGqCFycy3aSpsnru`다. 이 주소의 owner history query가 아직 없으므로 신규 bounded prefix를 통해 역할 및 정확4ug/5NS/3Hp 접점을 확인할 수 있다. 이미 저장된 전송을 중복 edge로 넣지 않는다.

많은 고객의 자금을 분배하는 서비스 패턴이면 전체 이력·모든수령자를 확장하지 않는다. 현재 역할·소유·CEX고객은unknown이다. 1.269195999SOL을 DOGINU 이익 회수라고 지정하지 않는다.

Fomo 로그인이 없어 절대 최초 공개 이력은 미확인이다. 기존 로그인 요청을 유지하며 같은 로그인 전 redirect를 반복하지 않는다. 시총은 독립 증거가 생길 때만 적격으로 변경한다.

## 보존

worker raw[3994, 3995, 3996, 3997, 3998], cap raw3999, 근거 raw4000, 검토 raw4001. 실제 공식문서조회3회·시장조회1회, 다른네트워크0. 경제 신규0: 기존state89개, resolution11개, 거래4,569개, edge644개의 값을 보존했고 검토state1개를 추가했다. 사용하지 않은 예약을 해제했다. 전체 goal은active다.
