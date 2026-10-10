# DET: 공급 지갑의 수수료 수령과 THESIS 뒤 본지갑 거래

## 결론

**공통 입금 주소를 쓰는 5py·Dyurt를 조회했지만, 두 주소의 유상 선행매수→DET 게시→동일 별도 주소 매도 사례는 이번 지정 범위에서 확인되지 않았다.** 같은 토큰을 받았다는 사실만으로 매수로 분류하지 않았다. 저시총 별도 지갑 완결 사례는0이며 연구는 계속한다.

원래Top10/raw141, 고정60일 `[2026-08-08T04:43:41Z,2026-10-07T04:43:41Z)`. 아래 UTC/정수 수량 기준. DET 검증 주소 `EC2f5DnHzuNRit1ExqghSifDbp1wgrzktsRRZCtU92MJ`.

## Dyurt CODEC: 선행매수로 오해하기 쉬운 수수료 수령

- 정확 mint `69LjZUUzxj3Cb3Fxeo1X4QpYEQTboApkhXTysPpbpump`, d6.
- **9/12 09:48:25Z**, Dyurt 신규 ATA에 **15.846915 CODEC** 수령. 원문 raw3657/data21, [거래](https://explorer.solana.com/tx/wytcpd8shuUECTQjawTyrzW1hceLWQQi8oa8MHh6kTnHh8xrfYMB73QLsrzFFR7yGtvYW9aKfi7sZw76bd54izi). Chrome3680에서도 성공/Finalized와 정확 수수료0.000005SOL을 확인했다.
- 외부 `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` 프로그램의 **ClaimFee2** 로그와 내부 transferChecked. 송신 역사owner `AbyeawAgyxZ6EHyujx64pEs4ZfdjdNHJRtfL9TF3sm8G`, 수신owner Dyurt를 확인했다. 프로그램명은 매수자 identity 근거가 아니다.
- 대가quote 감소와swap이 없다. Dyurt SOL 감소1,493,440lamports는 CODEC ATA 임대료1,488,440+fee5,000으로 잔차0이다. 토큰 대금으로 계산하지 않는다.
- 보존 DET CODEC THESIS **9/20 07:22:05Z**, 수령682,420초 뒤. 게시보다 먼저 받았어도 **paid BUY가 아니다**. 지정 source query에서 이후 CODEC 감소도 관측되지 않았다.

5py 정확주소30행+3655 빈/null footer, Dyurt300행+3659 빈/null footer로 고정구간 **successful·tokenAccounts=none 주소쿼리**를 닫았다. DET 여섯 mint 중 유일한 source delta가 위 CODEC였다. 다른 ATA·실패거래·위임 거래·전 생애에 대한 부재 증명은 아니다. 이전 Arv285/Ey83 종료 자료도 재조회하지 않았다.

## 자금 연결 독립 검증

독립 finalized public RPC3650–3653으로 기존 indexed 거래의 transaction/meta/slot/blockTime 전체가 각각 일치했다.

|기존 원문|실제 관계|독립 proof|
|---|---|---|
|3613/data14|5py→DET70SOL|3650|
|2553/data14|5py→정확8FX9,000.0012USDC|3651|
|3638/data6|Dyurt→DET50SOL|3652|
|2538/data30|Dyurt→정확8FX25SOL|3653|

5py 전체→DET210SOL, Dyurt50SOL과 같은 정확8FX 입금 관계는 유지한다. CEX 명칭은 Arkham2532 assertion이고, RPC는 전송을 확인한다. 같은8FX의 고객·실소유·의도는unknown이다. 5tz 핫월렛의 전체 pooled 흐름으로 개인을 연결하지 않았다.

## DET 남은 기간에서 확인한 내용

새 주소거래1,503개를 받았다. 고액 단독native 수신은 기존55n25/Ey250/Arv350SOL 3건으로 canonical 중복이어서 새edge0이다. 후속SOL→USDC swap은 거래별 수령 근거로 보존했으며 앞선 송금 전체lot·순익으로 귀속하지 않았다. Agm 임시ATA 임대료와 소액 주소유사dust를 개인 공급 관계로 승격하지 않았다.

STONKCATS 본지갑은 보존THESIS 뒤 **14 BUY·4 SELL**의 target/USDC 반대delta와 서명·swap로그를 확인했다. 이는 **본지갑의 게시 후 거래**이며, 별도 선매수 지갑이 게시 후 판 사례가 아니다. 기존배분14.85M을TH136초전매도한 뒤91초전5,000USDC 재매수한 시간표도 유지한다. 배분 원가·전체 realized PnL은unknown이다.

여섯 mint owner delta653건을 worker 정규화로 보존했다. HOOKED·STONK·OTC·Agency의 매도 역시 본지갑 흐름이며, 공개 이후BUY/배분/보상과 이전 재고를 분리한다. 역사 cap 미확정 토큰을 새 전체토큰 군집으로 확대하지 않았다.

## 범위와 정확 재개점

기존2,081+신규1,503=**3,584 고유signature**, 중복0. 연속첫57일 **3,137행**은 각구간empty/null footer로 종료했다. 마지막3일 `[1791089021,1791348221)`은447행, 마지막관측10/7 04:26:40Z, raw3679 **cursor `454115113:891`**이 남았다. 아직 60일 쿼리 전체종료를 선언하지 않는다.

다음 새예약에서 같은3일/limit100/asc/success/none/cursor로 남은page·footer만 받는다. 이어서 실제9UX247.5SOL·EFN300SOL 공급 주소의 같은토큰 유상취득을 확인하고, 원래 theveeman F5 partial cursor를 이어간다. 닫힌source·Ctf·8FX 자료는 재사용한다.

근거3687/검토3688/시총3686, state`initial_top10_DET_two_CEX_linked_funders_and_late_main_history_review_v1`. 기존75states/11wallet/trade4569/edge551 보존, 새state1/경제행0. 5Luna/max는 SQLiteRO/network0. RPC30/30, Chrome1/2, 나머지0/사용하지 않은예약해제. Fomo/BQ/Bridge0. 단독RZD·Top100 중단 유지.

미확인: 별도 유상선행매수·게시후동일지갑처분의 새 완결 사례, 당시 유통시총, 실소유/CEX고객/의도/USD손익. 자료 미확보와 조사범위 내 미관측을 구분한다.
