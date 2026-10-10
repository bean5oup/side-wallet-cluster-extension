# Werey ARTHUR: 외부 지갑 12곳의 재고·매도·자금 접점

## 현재 결론

**Bqu의 실제 매수 물량이 Werey의 THESIS 때 남아 있었고, 게시 후 새 매수 없이 같은 주소에서 전량 매도됐음을 확인했다.** 아직 Werey와 비서비스 자금으로 연결된 주소라고 입증하지 못했다. 앞선31D 사례와 함께 시간표 후보로 남기며, 완성된 연관 뒷지갑 사례 수는0이다. 소유권·의도·CEX 고객·USD 수익은 미확정이다.

원래Top10(raw141), 고정60일 **2026-08-08T04:43:41Z ≤ t < 2026-10-07T04:43:41Z**, 당시 유통시총100만 달러 이하·THESIS 없는 BUY 포함을 유지한다. 시간은 모두 UTC다. 앞선 [31D와 반복 송금 주소 보고서](werey-arthur-external-wallet-and-funding-review.md)의 승인·구분은 유지한다.

## Bqu: 게시 재고와 첫 후속 매도

주소 `BquXJFnbcSbFgrL6D88FzQTWNqA5dd8DoJHRRsDLDRmS`, exact ARTHUR ATA `815T4tL4pYUEmna2P1szvfKDYGumU9DhDpqEyMWLHE8Z`.9/30 20:19:59부터의24행과빈footer(raw2909/2910)를 대조했다. 실제 매수·매도·서명·역사 token/quote owner·정수수량·인접 잔고가 일치한다.

Werey의 보존 THESIS10/3 10:33:00(raw2156) 때 **1,077,754.854547 ARTHUR**가 남았다. 다음 target 거래인 **10/3 17:33:01**, 정확히 그 수량을 전부 매도해 ATA 잔고0, owner USDC **+515.577339**가 됐다. 그 사이 새 target 매수·전송은 없다. [실제 매도](https://solscan.io/tx/pKD2HTrZid4jAZNEbvzGDFziwF7svhgTpDVFkf56M7pGFhSBuj26cRGBZyCpefyH1D99LjekNcxWvc2pyV1E75z) · raw2909 `/response/result/data/19`.

10/5 이후 두 BUY→SELL 사이클은 새 재고다. 이를 THESIS 전 물량의 반복 처분으로 합산하지 않는다. 보존 공개 시점과의 순서는 확인됐으나 절대 최초 공개·인과관계·조종 의도는 확인되지 않았다. Bqu 각 기준 매수의 시총은 보류이며, 다른 지갑의 시총 승인을 그대로 적용하지 않는다.

Bqu의 USDC ATA `2WXtGqsWwRXP3x434oFFBhFbRNZGizTkD5J74ypbassA`는raw2925/2926의500행만 확보했다. **9/2 16:10:01~9/29 22:12:50**까지며 cursor `451772565:602`가 남았다. 첫 ARTHUR 매수와 게시 후 매도 시점은 아직 이 USDC 조회에 포함되지 않았다. 따라서 자금원·후속 bridge/CEX 부재를 판정하지 않는다. 다음 배치는 동일 커서·필터·고정 종료 시각부터 이어간다.

## 12개 정확 토큰 계좌 비교

| 정확 owner 주소 | 행 | THESIS 시점 ARTHUR | 게시 전 BUY / USDC SELL | 게시 후 BUY / USDC SELL | 마지막 ARTHUR | 원문·빈footer |
|---|---:|---:|---:|---:|---:|---|
| `9Uq8r9mqmSnDSAwXdWv3aLL76C3scrcDXvpZrTxNHyvn` | 7 | 1,068,880.530123 | 3 / 2 | 2 / 0 | 2,019,875.403135 | raw2897/2898 |
| `DkxW6UwNzTZy2uFBBC91gHJQHVQDXMTss8v98bLXtM7x` | 10 | 1,019,564.903027 | 3 / 2 | 5 / 0 | 3,277,878.349040 | raw2899/2900 |
| `8vEuRcStNUGpwjRSudp8eh8SQ9Jqz6A9wg71ePNhsBNR` | 4 | 0.000000 | 3 / 1 | 0 / 0 | 0.000000 | raw2901/2902 |
| `AHsKXR1NCeKjgCgqSAB2WQun22oVAhyqWrBk1KvPkahe` | 120 | 4,743,816.603127 | 44 / 16 | 55 / 5 | 20,680,053.204457 | raw2903/2904 |
| `BYphwgWoYvXss7d1bC6Vm4MMjewyVMGFasrCiAc71Dd2` | 10 | 0.000000 | 4 / 4 | 0 / 0 | 0.000000 | raw2905/2906 |
| `GBhG2jkKFzdPZirZVhAPMKLnHpWaPnUhJntdX6bFhQ4R` | 43 | 2,063,134.191946 | 5 / 1 | 37 / 0 | 18,505,787.261336 | raw2907/2908 |
| `BquXJFnbcSbFgrL6D88FzQTWNqA5dd8DoJHRRsDLDRmS` | 24 | 1,077,754.854547 | 16 / 3 | 2 / 3 | 0.000000 | raw2909/2910 |
| `XQvgKqsXmZKiRA6bCrnPnUSQJmzhAowtzvASQSCg32W` | 24 | 1,831,819.944915 | 10 / 4 | 6 / 1 | 4,027,114.195272 | raw2911/2912 |
| `9K1HhNJwD9CfgtiLW5vVWCA74oHpqd7dT98AuVdrRz4j` | 49 | 1,944,343.551113 | 19 / 6 | 24 / 0 | 7,713,712.562683 | raw2913/2914 |
| `9x7ZokSqSqoJeUWobyDF6US2oqxqtr77mt5rPg4yQKdi` | 37 | 0.000000 | 4 / 2 | 21 / 6 | 0.000000 | raw2915/2916 |
| `6XFiFE3zF54dbWGnZbmnJ7dh8qWP74HgGH6zPXBsfvck` | 34 | 4,137,522.678322 | 16 / 0 | 10 / 8 | 0.000000 | raw2917/2918 |
| `HEg4z1say83FoZUkX4VyiccdYRScptg1Jinje5VmFNE4` | 11 | 111,609.035040 | 6 / 4 | 1 / 0 | 179,654.171278 | raw2919/2920 |

표의 BUY/SELL 숫자는 초기 USDC 판독 결과이며, 아래 SOL 보완5건과 구분한다. 9x의 THESIS 시점 재고0 판정은 모든 target 잔고 변화를 포함한다. **12개 exact ATA의 쿼리는 모두 끝났지만 지갑 전체·모든 ATA·평생 이력 완료는 아니다.** 기존3개와 합쳐62외부 매수자 중15개 정확 계좌를 확인했다.47개는 아직 검토되지 않았다.

AHs는 게시 후5회 USDC 매도가 있으나55회의 새 BUY가 섞이고 마지막20,680,053.204457 ARTHUR가 남아, 옛 lot 처분을 확정할 수 없다.6X는 게시 재고4,137,522.678322와 게시 후 새 취득이 섞인 뒤10/5에 첫 잔고0을 거쳐,10/6에는 별도 새 사이클로 다시0이 됐다.9x는 게시 시점0이고 게시 후 새 매수·매도여서 옛 선행 lot 사례에서 제외한다. 다른 보유 주소의 이 창 안 미매도는 이후·다른 ATA 매도 부재를 뜻하지 않는다.

## 실제 전송과 서비스 대안

AHs `AHsKXR1NCeKjgCgqSAB2WQun22oVAhyqWrBk1KvPkahe`의 owner 조회는9/29~고정 끝 **8.197일726행**(raw2921–2923/빈2924)에서 끝났다. 원래60일 전체 owner 완료가 아니다. 별도 `9xEJMj3aSRM6iyGj7YoQk3WU2RDwTHuWmvdD7extnrse`의 USDC ATA `EfjDkUdwdRi3HRXKkJoxs88u9sYV37SKHxsSGvJ4ybVu`로9/29 19:24:46·9/30 01:52:05·16:10:01에 **4,657.406483/3,574.669528/2,000 USDC**, 합10,232.076011을 보냈다. 실제 plain signed transfer와 양쪽 잔액을 대조했다. 용도·서비스·소유자는 미확정이다. 보존Werey와3yUM 이력에 해당 정확 상대 주소의 교차가 없어 저자 연결로 승격하지 않았다.

XQ는10/1에 source owner/signer `CA4r4rn1jBHFuEKFFrnkmfxMpmnCtxZVxGCoepn2gdvC`의 ATA `8wvGFRA81wH9dk6Bbw6BYiRUcfiB8ASuunh6uBJUeoaX`에서 **403,860.660803+305,742.678126=709,603.338929 ARTHUR**를 받았다(raw2911 data5/6). Token-2022 transferChecked·역사 owner·authority·양쪽 잔액은 일치하지만 XQ는 비서명 수령자이고 quote·swap은 없다. 따라서 유상 BUY가 아니다. 발행자·분배·서비스·저자 관련성은 미확정이다.

12개 target 자료의 외부 주소→Werey 소액 USDC 지급20건·9.124968은 실제 지급으로 보존했다. 수수료·추천 보상·서비스 가능성이 있어 사적 funding으로 올리지 않는다.8vEu의10/1 0.45 USDC는 그때의 ARTHUR BUY와 같은 거래이며,10/2 선택 fill보다19시간 먼저라는 이유로 별도 선행 자금으로 분류하지 않았다. 공식 현재추천안내raw2881은 일반 구조 근거이며 당시 개별 지급 목적·요율의 증명은 아니다.

3yUM의 실제 반복 송금·STONK 왕복은 기존원문으로 재검토했다. Werey actual BUY169건/7exact mint(THESIS 없는STUPIDINU/SNDK도 포함)와 비교했지만 같은-token 옛 lot·공개 시점·게시 후 처분·시총·저자 관계가 모두 맞는 새 완성 사례는 없다. 단순 signed address가 개인 뒷지갑을 뜻하지 않는다.

## 저시총 기준과 quote 단위

전체 새 실제BUY298건에서 기존cap2274의 직전 positive 표본을 확인해 **적격1/보류297**이다. 적격은 GBh의 **10/2 11:03:47** 매수 한 건:11:00 표본660,620.3613507042달러·227초·index32, 승인raw2933. [실제 매수](https://solscan.io/tx/44DjqDDV9nhwSC1TxhMrdXMMt7Zt3h7SSzpTd5DLdPqWcE1MK5ipvu3E1BfZsHxVMQEZ846g9KHnzycqfnzoKVM8). 이 주소의 확보된 게시 후 SELL은0이다. 시장에서 처음 고른16fill은 전부보류다. Werey 본지갑 승인2286/31D 승인2893과 **THESIS cap pending**을 바꾸지 않았다.

373행에서 **364 USDC owner net swap+5 SOL/wSOL 실제 swap**, XQ 무quote credit2건·잔고 무변화2건을 분리했다.5개의 SOL 거래는 temp account initializeAccount3/close owner·signer·실제 system input·route transfer·수량을 다시 검산했다. canonical quote는 **gross wSOL 실행수량**이며 native net·수수료·rent·추가지급은 별도로 보존했다. USDC net과gross wSOL을 섞어 USD 원가·수익을 자동 계산하지 않는다.

## 저장과 다음 추적

직접RPC30회, Chrome1회다. Chrome 거래 화면 읽기는30초timeout(raw2927)이므로 라벨 부재로 해석하지 않았다. Fomo·Bridge·시장·BigQuery·Nodit indexed·공식문서 신규조회0이다. 모든5작업자는Luna/max, 네트워크0·SQLite읽기전용이었다.

SQLite 새swap353건/실제TRANSFER5건을 추가해 trades1479/edges415/state55다. 기존54states·11wallet resolutions·1126trades·410edges·Fomo1338/고정Top10 404·match73을 보존했다. 기존16swap은 중복 적재하지 않았다. 근거raw2934/검토raw2935, state `initial_top10_remaining_arthur_buyers_and_funding_review_v1`다.

**다음은Bqu USDC 남은 커서부터 실제 매수자금·매도 뒤 회수와Werey 접점을 확인한다.**6X의 정확 USDC 자금/회수와 CA4→XQ 공급 역할은 개별 근거가 있을 때 이어간다. 전체 서비스 pooled flow·본지갑 배경·이미끝난ATA를 반복하지 않는다. 연구목표는 진행 중이다.
