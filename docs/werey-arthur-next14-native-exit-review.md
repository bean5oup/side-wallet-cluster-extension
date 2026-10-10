# Werey ARTHUR 추가14개 매수 주소와 매수 직후 처분

## 이번에 확인한 내용

**F73 지정 조회를 저장 커서에서 종료했고, 추가14개 정확 토큰 계좌도 모두 조회를 마쳤다.** 새214행에서 유상 매수104·매도92를 검증했다. 나머지18행은 토큰계좌 종료이며 시장 매매로 세지 않았다.

**5vKD는 Werey 본지갑의 실제 매수2초 뒤 매수하고24초 뒤 같은 수량을 전량 매도했다.** 하지만 THESIS보다 앞선 거래이며 실제매수의 대외 노출 시각은 미확보다. 복사매매·작성자와의 연결·게시 악용으로 단정할 수 없다. 해당 매수는 당시시총100만달러 이하 조건을 통과했다.

새14개 중 THESIS 당시 재고를 보유한 주소는3jK 하나이며 게시 후 추가매수가 섞여 있다. 작성자와의 접점4건은 같은swap안의1.337908USDC지급으로 수수료·추천분배 대안을 유지했다. **뒷지갑 paidBUY→연결작성자 THESIS→동일뒷지갑 SELL→회수·원가까지 이어진 완성사례는0건**이다.

## 고정 범위

원래Top10/raw141, **2026-08-08T04:43:41Z ≤ t < 2026-10-07T04:43:41Z**, 역사유통시총≤100만달러다. 모든시각UTC.

- ARTHUR `6e8LLHkqCTa4mzGuL1PoUxSfeHmDeceJ3DaJSSUNg937`/decimals6.
- 검증Werey `DmopudSGaQQenK4cW5NgmHUsexMB3sEJNn6n1EfLKs28`.
- 실제본지갑BUY **10/2 08:00:37**, 보존THESIS **10/3 10:33:00**/raw2156. 실제BUY와공개노출은별개이며 THESIS도절대최초공개임을뜻하지 않는다.
- 이미확보한시장613행/184엄격거래를재사용했다. Fomo/새전체시장/BQ조회0.

정확ATA의성공필터·고정구간query종료이며 모든계좌·모든자산·지갑평생완료가아니다.

## 주소별 게시 재고와 매매

|owner 축약|조회 행|게시 전BUY/SELL|게시 당시ARTHUR|게시 후BUY/SELL|마지막ARTHUR|조회 상태|
|---|---:|---:|---:|---:|---:|---|
|`s8uRL…mrS2`|6|4/2|0.000000|0/0|0.000000|지정조회 종료|
|`2Yz7i…x1qY`|33|13/13|0.000000|1/1|0.000000|지정조회 종료|
|`31x1j…T242`|3|1/2|0.000000|0/0|0.000000|지정조회 종료|
|`3fZFe…c1R8`|2|1/1|0.000000|0/0|0.000000|지정조회 종료|
|`3jKBU…fA93`|11|4/3|29,939.224657|3/1|76,217.796506|지정조회 종료|
|`4ErzR…xehn`|23|8/10|0.000000|1/1|0.000000|지정조회 종료|
|`4ZtTZ…o7rw`|11|9/2|0.000000|0/0|0.000000|지정조회 종료|
|`57wLa…rCCc`|4|2/2|0.000000|0/0|0.000000|지정조회 종료|
|`5rE1T…Dyuy`|12|6/5|0.000000|0/0|0.000000|지정조회 종료|
|`5vKDt…Zo53`|12|5/5|0.000000|1/1|0.000000|지정조회 종료|
|`6pVk8…ApuG`|77|25/33|0.000000|7/4|59,685.258083|지정조회 종료|
|`8YqX8…8g3y`|6|4/1|0.000000|0/0|0.000000|지정조회 종료|
|`9D9dY…11v3`|2|1/1|0.000000|0/0|0.000000|지정조회 종료|
|`9DGHU…sWF6`|12|8/4|0.000000|0/0|0.000000|지정조회 종료|

### 5vKD의 본지갑 실제 매수 직후 왕복

`5vKDtzbvwik9eEbVM7CF3WSZhG7y15eLfg9cFrNtZo53`는직전잔고0에서 **10/2 08:00:39**에323,896.723876ARTHUR를매수하면서200USDC를썼다. **08:01:03**,24초뒤전량매도해194.826155USDC를받고대상잔고0이됐다.

- [매수거래](https://solscan.io/tx/4cB4nF34s47tfBAajEACf1pcJXYeDctp5QQLNSUo1aAeFfnxtY641nzS1Dr8kanMVv8uDzmQccYQ3yhiLq3ZgFYz),raw3114 data6.
- [매도거래](https://solscan.io/tx/5Xwz4jPLeEjSjWyXzBb2TQQEoNR2iNNkcou2MnytQXo6zKiY6NmkahyBdTdmK935fhzJgTgzisbfvwkCoTt3HcAS),raw3114 data7.

같은정확수량의왕복이며 quote순변화 **−5.173845USDC**다. SOL수수료·USD환율·소유·의도·실현수익전체를증명하지 않는다. 그후같은주소의다른사이클은게시전lot와분리한다. THESIS시점재고0인거래를THESIS악용매도로바꾸지 않는다.

2Yz의5적격BUY는08:01:36–42이며매도들이이어져08:02:39에잔고0이다. 시간적근접·고빈도는실제관측이고카피행동이나공모의증거는아니다. s8u는본지갑BUY당시재고를추가유입없이게시전에처분했다.

### 3jK의 게시재고와 새 거래 혼합

`3jKBUdKtoYZ8VKwaenTSeprXSKu4h7osvj4SCSZhfA93`는THESIS당시 **29,939.224657ARTHUR**를보유했고게시뒤3BUY/1SELL이있다. 최종 **76,217.796506ARTHUR**로새매수가섞여기존lot처분과수익을분리할수없다. 별도주소의유상매수는확인하되Werey사적관계는미확인이다.

## 임시wSOL을 통한 실제유상거래3개

USDC quote193거래와별도로 **8Y BUY2·3jK SELL1**을검증했다. 임시계좌 initializeAccount3/owner·실제transfer·closeAccount·native balance를대조했다.

1. **8Y 10/2 06:23:40**:새GMku wSOL에owner가5.3SOL을넣고route에서소비해964,666.148255ARTHUR취득. Owner native−5.301521262SOL은quote5.3+network0.000007422+targetATA rent0.001513840이다. 임시wSOL rent는close로환급된다.
2. **06:35:38**:5SOL을써917,262.226674ARTHUR취득. Owner native−5.000014098SOL=quote5+networkfee0.000014098. 같은정확targetATA이며새rent없다.
3. **3jK 10/3 08:16:39**:29,939.224656ARTHUR매도→임시BvK수령151,541,135+98,767,095=**250,308,230lamports gross**. 별도지급250,308·새다른mint6Gm계좌rent1,488,440·network19,648차감→owner native **248,549,834lamports**와일치. 그경로의6Gm/USDC중간순변화0을최종취득quote로쓰지않는다.

모두서명·성공·exacttarget변화와대가경로가있어토큰선물이나에어드롭으로분류하지않았다.8Y는게시전에물량을전량처분해THESIS재고0이다. SOL/USDC혼합거래원가와USD수익을단순합산하지않는다.

## 작성자 지급·계좌 종료와사적연결

|UTC|지급owner 축약|Werey수령USDC|같은swap방향|근거|
|---|---|---:|---|---|
|2026-10-02T08:36:09Z|`31x1j…T242`|0.642600|BUY|[실제 거래](https://solscan.io/tx/N2wMDKtrhk7vatLingHeNFkByPVTiMSqsac5B1yqp67gfuuC8RZp6v3476MVTXJFyDkamoZj5VKC8yNZSKGbQgs) · raw3100|
|2026-10-01T21:08:37Z|`4ZtTZ…o7rw`|0.199994|BUY|[실제 거래](https://solscan.io/tx/49syWzevv82Ukt19rVZRB9vXHEM4tuUiKim32Budfz3fFo188b1PYExvBSHJeri1AGeUb8ELUT9Z4xnaTTPXKKof) · raw3108|
|2026-10-02T08:55:40Z|`9DGHU…sWF6`|0.120314|BUY|[실제 거래](https://solscan.io/tx/4A5uXvzUkXTBDgQf2xTjNZh9iC2uqKzWsV1A5dmWbyciXfkWjw8StfTJX7RgMC6SHaVVaX77AJHTs2CN1BbDE4qw) · raw3122|
|2026-10-02T10:04:45Z|`9DGHU…sWF6`|0.375000|SELL|[실제 거래](https://solscan.io/tx/5XHJUSwgUtVJFjHeRQbbHvbB8ojuAXDKQJA3APXnbRVWeNo5WPrQALMFGgKP3pyUHKKTvpBee9biSmyL3ZkwvfYb) · raw3122|

4건은정확WereyUSDCATA/historicalowner·전송량·서명을대조했다. 전부실제swap안의지급이며공통실행/fee payer도있다. 사적자금공급·동일개인·CEX고객으로승격하지않았다. 보존추천자료raw2881은일반대안이며개별행의목적을확정하지않는다.

잔액변화없는18행은대상ATAcloseAccount/rent회수다. 일부같은정리거래에서소액SOL지급도있지만수령역할미확인이다. 토큰매수매도·작성자공급으로세지않았다. 이targetquery안에서verifiedTop10→후보공급은관측하지못했으나원래quote/native공급이력은이범위밖이다.

## 역사시총과자료종료

104실제BUY중 **적격7·보류97(300초초과63/선행양수표본없음34)**이다.100만달러초과확정건은0이다. 적격은2Yz5·4Erz1·5vKD1로개별거래시점만의판정이다. 임시wSOLBUY2는표본이각1,420/2,138초전이라보류다. 기준300초를늘리지않았다. 기존승인2286/2893/2933과THESIS시총보류는유지한다.

**F73 raw3095**는priorraw3085커서454115073:346에서동일계좌·필터·고정구간을이어받아0행/null이다. 기존1,990행을보존하고해당query를종료했다. 새capture는이번batch027RPC1회를썼으며body의legacybatch020표기는현재batch와별개다.

RPC29/30,다른외부요청0·5Luna/maxRO/network0. 신규actualswap167개를추가했고기존29개는정확대조후보존했다. 총 **trades4,128/edges434/states60**. 이전59states·11wallet resolutions·3961trades·434edges·Fomo1338/구간404/match73을보존했다. walletresolution/newprivateedge0.

시총raw3129/근거raw3130/검토raw3131,state `initial_top10_arthur_next14_native_and_prethesis_exit_review_v1`. 지정조회는누적 **57종료·부분0·미조회5**다. 다음새예약에서마지막5개를확인하고,유상매수·공개재고·처분사례의실제비서비스작성자자금관계를이어간다. 원래Top10전체60일public/BUY-only/cap/native/quote기초gap도유지하며연구전체가끝났다는뜻은아니다. 소유·게시악용·CEX고객·수익은미확정이다.
