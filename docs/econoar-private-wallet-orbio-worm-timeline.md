# econoar — 별도 지갑의 ORBIO·WORM 전달 시점

## 판정

**같은 별도 지갑이 두 토큰을 Fomo 주소로 전달한 구체적 관계를 확인했다.** Arkham 상세의 ORBIO 취득·자산변화와20초 뒤 전달, WORM의 보존 THESIS37초 전 전달을 원문으로 저장했다. 이는 provider 화면 근거이며 독립 chain receipt 검증과 구분한다. 엄격한 저시총 완결 사례는 아직0건이다.

대상은 원래 Top10 econoar/user `c573ebfa-5e98-580c-ae15-c8672f11c151`, 고정60일 `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z`다. 별도 주소는 `0xbfd26274e94cbc3826d25f3217d4a756a8c25c3b`, Fomo 연결 주소는 `0x1605b59dfe3c1742c815d604aab6a2faa3a5c91f`다. 기존 Ethereum0.005ETH 송금은 독립 raw2238/2239/2241로 확인돼 있다. 다른 체인의 wallet resolution은 자동 추가하지 않았다.

## ORBIO

|UTC|관측|출처|
|---|---|---|
|9/30 21:07:31|Robinhood, bfd가124,948.533095 USDG 지출·1,525,221.08389185277232859 ORBIO 수령, 성공/block76825739|[취득 거래](https://arkm.com/explorer/tx/0xf7eb376b02013923d7fec490e49ee9b1154d65de9fa2814095f56cdcaf1b1921), raw4023|
|9/30 21:07:51|20초 뒤 bfd→1605, 같은 표시 수량 전송·양쪽 자산변화, 성공/block76825936|[전달 거래](https://arkm.com/explorer/tx/0xe6d9b5be04e54a6da1e7a7c1b31c06cd28d3303b94f261a5ff504848ffe3ff02), raw4024|
|10/6 02:34:05|최초 보존 THESIS, 전달 계약과 같은4663/aa07…128a3|Fomo raw673/2154/2170|

취득 후보는 최초 보존 THESIS보다 **5일5시간26분34초** 앞이다. 단순 한 전송을 BUY로 바꾼 것이 아니라 상세가 TRADES1/FILLS7/TOKEN TRANSFERS21과 bfd의 USDG 감소·ORBIO 증가를 표시했다. 단순 무료 수령이라는 대안과는 다르지만, **화면만으로 정확 buy 계약·독립 영수증을 확정하지 않았다.** 취득 화면의 token link는 global slug이며, 전달의 tx destination `0xaa07a0e9209e16ac99708c3ec70159c6ef3128a3`가 보존 THESIS의 계약과 일치한다. 정확 raw integer/decimals는 독립 log로 검증해야 한다.

이 경로의 현재 분류는 **별도 지갑에서 유상 취득 후보→Fomo 주소 전달→나중 THESIS**다. 사용자가 원하는 **별도 지갑에 계속 보유→THESIS→그 별도 지갑에서 매도**는 아직 확인되지 않았다. 실제 취득 직후 같은 수량을 Fomo 주소로 옮긴 사실은 이 구분에 중요하다. 6개 Fomo BUY source 이벤트와 실제 bfd 취득 횟수는 합치지 않는다. 보존 SELL0도 전체 매도 부재를 뜻하지 않는다.

## WORM

**2026-09-18T21:07:08Z**, bfd→1605로3,031,388.715612183155949703 WORM이 전달됐다고 상세가 표시한다. 성공/block66533933, tx destination `0x3ba500f1ababbcf0f0247d06d1c56fd7e6c4c09d`는 보존 THESIS의 exact4663contract와 일치한다([거래](https://arkm.com/explorer/tx/0x428e8d19b181d48909f31906524d979308f56191c506f959b20c11fc1d7f0912), raw4025). 보존 THESIS21:07:45Z보다 **37초 앞**이다.

취득 후보 [2401…dd47](https://arkm.com/explorer/tx/0x2401a39c07890707e31f7db6ba043b1f607652f97df7fcf2b571a445d8b5dd47)은 기존 주소 페이지raw4015의 USDG/WORM 힌트만 있다. 상세를 열었지만 화면 읽기 연결이 중단됐고, 정상 새 연구 탭의 단일 제한 복구도 실패했다. 완료 capture가 없으므로 paidBUY·정확 취득 시각은 미확정이다. 접근 실패를 거래 부재로 해석하지 않는다.

## 반복 관계와 남은 검증

두 exacttoken 전달은 같은bfd→1605 방향이다. 일반적인 shared Relay solver나 거래소 hotwallet를 통한 우연한 겹침보다 구체적인 연결이지만, **같은 소유자·범행 의도 증명은 아니다.** bfd의 `@econoar?`는 낮은 신뢰도의AI예측이므로 채택하지 않는다. 앞서 나온ZZZ6K반환은 다른토큰이어서 ORBIO/WORM 회수로 합치지 않는다.

다음은 화면에 실제 제공된 Robinhood Blockscout outlink로 정확 buy/transfer계약·영수증·정수 수량을 확인하고, 같은 token의 반환·게시 후 같은별도주소SELL·quote수령을 연결한다. 당시 유통 시총≤1M은 아직 보류다. 현재USD·FDV를 대체하지 않으며, cap확정 전 전체token/BQ군집은 수집하지 않는다. 최초 보존 THESIS와 절대 최초 공개도 별개다.

브라우저5회(사전4회+미완료상세 단일복구1회), 다른 외부조회0. 새원문4023–4025, 근거4026/검토4027. 기존4569trade·645edge·11resolution과92state를 보존했고, 경제행0·검토state1만 추가했다. 스키마·collector·테스트·소유자라벨은 변경하지 않았다. 브라우저 중단과 worker연결 실패를 보존하며 전체 goal은active다.


## 후속 독립 원천 확인 — 배치061

공식[Blockscout REST 문서](https://docs.blockscout.com/devs/apis/rest)는 공개 instance API를 안내한다(raw4029). 그러나 해당 Robinhood instance의 `/api-docs`는 웹 조회에서403을 반환했고(raw4030), ORBIO의 정확 취득 hash에 대한 첫 공개 REST 거래 조회도403을 반환했다(raw4032). 공식 명세 검색raw4031은 정확 transaction 방법을 추가 검증하지 못했다. **독립 receipt/log는 아직 확보하지 못했다.** 같은 실패 endpoint를 다른 hash로 반복하거나 인증·보안 우회를 하지 않았다.

Chrome 화면 읽기가 반복 중단돼 사용자에게 연구용 브라우저 연결 복구를 요청했다. 앞서 저장한 ORBIO20초 전달·WORM37초 전 전달 사실은 provider 근거로 유지한다. 이 접점이 있다는 것과 실제 소유자·게시 후 같은별도지갑SELL·저시총·수익은 별개다. 원래10명 전체 범위 소진이나 완결을 선언하지 않는다.

작업자1의 최종 저장자료 검토도 보존했다. ORBIO 계약의 canonical trade0·보존 Fomo SELL0은 **검색한 저장자료에 근거가 없다는 뜻**이다. 기존Ethereum indexed6transfer는 다른토큰d34a이며 Robinhood ORBIO의 회수·60일 전체 기록으로 쓰지 않는다.

신규 문서 조회3회(사전+1 포함), publicindexed1회, 다른0. 근거4033/검토4034. 기존93state·11resolution·4569trade·645edge의 값을 보존하고 새검토state1만 추가했다. 경제행0, 남은indexed3예약 해제. 첫 정확API403은 닫힌 요청으로 기록하고 실제 접근 조건이 바뀌기 전 재조회하지 않는다. 전체 goal은active다.
