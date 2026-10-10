# Werey ARTHUR 추가 매수 지갑 13개와 게시 후 처분 검토

## 결론

**외부 주소 3개에서 보존 THESIS 당시 남아 있던 ARTHUR 재고를 이후 새 매수 없이 같은 주소에서 전량 매도한 흐름을 확인했다.** 다만 이 주소들이 Werey와 사적으로 연결됐다는 자금 근거는 확보하지 못했다. 같은 토큰의 시간 순서만으로 뒷지갑이라고 판단하지 않는다.

추가13개 exact token account의 성공 거래410개 중 실제 유상 매수259·매도136·타인 비용 부담의 토큰 수령1개를 구분했다.14개는 target잔고 변동이 없다. 매수259건의 시총은 **적격0·100만 달러 초과2·보류257**이다. 기존 실제 매수 적격raw2286/2893/2933은 해당 거래의 승인으로 유지하며 THESIS 당시 시총은 보류다.

**연관 별도 지갑 유상 매수→같은 작성자의 보존 공개 시점 재고→그 별도 지갑 매도→회수·원가가 연결되는 완성 사례는 아직0건**이다. 전체 뒷지갑 부재를 뜻하지 않는다. 기존62외부 매수자 중28개의 exact ARTHUR 계좌를 검토했고34개가 남았다. 원래10명 전체의60일 Fomo·체인·시총 coverage도 미완료다.

## 조사 범위와 기준 시점

- 원래 초기10명: cohort raw141. 단독RZD·Top100 확대는 재개하지 않았다.
- 고정60일: **2026-08-08T04:43:41Z ≤ t < 2026-10-07T04:43:41Z**.
- Werey 검증 Solana 지갑: `DmopudSGaQQenK4cW5NgmHUsexMB3sEJNn6n1EfLKs28`.
- ARTHUR exact mint: `6e8LLHkqCTa4mzGuL1PoUxSfeHmDeceJ3DaJSSUNg937`, decimals6.
- 기준 보존 THESIS: **2026-10-03T10:33:00Z**, raw2156. Source 시각과 실제 BUY 시각을 구분한다. 보존 THESIS가 절대 최초 공개임을 증명한 것은 아니다.
- 기존 적격 Werey 실제BUY:10/2 08:00:37, raw2286. 이전시장613행/184strict fills를 재사용하고 새전체시장 수집은0이다.

Exact 계좌의 빈footer 확인은 해당 주소·필터·고정 구간 쿼리 회수 종료다. 다른 ATA·모든 자산·지갑 평생 이력 완료가 아니다.

## 게시 재고를 이후 전량 매도한 주소 3개

|실제 서명 owner|THESIS 재고 ARTHUR|전량 매도 UTC|owner 순수령 USDC|거래와 원문|
|---|---:|---|---:|---|
|`3oe7aYLUw2Pkbm7QMAhAjn5WbzaoG9tigkrX1mAecr1P`|497,033.836556|2026-10-03T16:28:28Z|346.310900|[실제 매도](https://solscan.io/tx/246wk9BW48ngYc6qu86PNAc2xEBqND27L76vqEJqKs28mpw1XJwPBzXstsGxXuBkA81f6YfpWkxyo4xDg8Wb9QmD) · raw2985 /response/result/data/43|
|`Hwpk5iF3FYqV5U8taQUoMWaEHhJmRGpZ48N7nfSJ5tRU`|75,405.663146|2026-10-03T16:54:58Z|48.667467|[실제 매도](https://solscan.io/tx/3mDtNK151fVQSprQGtgcfLpuAssFUC4dZznTbLugrgF2d6C84XE3R59bZgBK4dia7mvoKqVyAaNpjRnH6Rij6qfk) · raw3001 /response/result/data/6|
|`GGbKCd4xQ6K1R9ShGTS7xN1vPf3SvPzsQmwUNvd9Mx2D`|96,899.999536|2026-10-06T02:49:35Z|19.765839|[실제 매도](https://solscan.io/tx/64tXurTVcrh4d4EVkEsFDHnRB3f8WvLDmCPWrHLKerwd7dYCnDfSiStteCXJmmJ5zwZNkYDquGoNBSLekz7Wetpb) · raw3003 /response/result/data/4|

세 경우 모두 대상 계좌의 시작 잔고0부터 변동이 연속으로 일치했다. 보존 THESIS 이후 첫 target변동은 SELL이고, 그 직전잔고가 THESIS 재고와 동일하며 직후0이다. 그 사이 새 target유입이 없어 **같은 계좌의 기존 포지션 전량 처분**을 확인한다. 다른 계좌·개인 소유·행동 원인·실현 수익을 증명하지 않는다.

### 3oe: 27회 매수·15회 매도 뒤 남은 포지션 처분

주소 `3oe7aYLUw2Pkbm7QMAhAjn5WbzaoG9tigkrX1mAecr1P`는 THESIS 전27BUY·15SELL 뒤 **497,033.836556 ARTHUR**가 남았고,10/3 16:28:28 그 전량을 매도했다. exact target45행+빈footer raw2985/2986이 종료했다.

직접 getTransaction raw3011에서 같은 signature/slot452987432, 성공·서명·target와USDC의 pre/post balance를 대조했다. **QuickNode의 indexed와 직접 조회라는 같은 제공자 검증**이며 독립 제공자 검증이라고 부르지 않는다.

USDC 계좌잔고는 **1,253.975159→1,600.286059**, 따라서 이 매도로 늘어난 owner잔고는 **346.310900 USDC**다. 기존잔액을 포함한1,600.286059 전체를 매도대금 또는 수익이라고 계산하지 않았다. 여러 사전 매수·매도가 있어 원가와 이전 실현량이 필요하다.

Quote 계좌 `HUZnz5s7aK7DDNvsLL8swMcpDhXv9FbpFTjaxdFTNUCV`의 raw3009/3010은 ascending1,000행 **8/8 05:09:01~8/29 15:14:52UTC**, cursor `442638179:241`, 빈footer 미확보다. 아직 ARTHUR 첫 매수와10월 매도 이후 구간을 포함하지 않아 **매수 원금 공급자·매도 뒤 회수·CEX 목적지를 판단할 수 없다**. 다음은 이미받은 prefix를 재수집하지 않고 미확보 관련 구간을 예약해 이어간다.

### Hwpk·GGbK

Hwpk는 게시전5BUY/1SELL 뒤75,405.663146, GGbK는4BUY/0SELL 뒤96,899.999536 ARTHUR를 보유했다. 각 게시후 첫매도에서전량0이 됐지만 quote 전체이력·회수·원가·작성자사적연결이 미확보다. GGbK의 확보 Werey 지급0.163717USDC는 같은 swap 안의 지급으로 수수료 대안을 유지한다.

## 13개 계좌의 전체 요약

|owner 축약|조회 행|게시전 BUY/SELL|게시 재고|게시후 BUY/SELL|최종 target잔고|조회 raw/빈footer|
|---|---:|---:|---:|---:|---:|---|
|`5hgF8…jzSB`|33|13/11|0.000000|2/2|0.000000|raw2983/2984|
|`3oe7a…cr1P`|45|27/15|497,033.836556|0/1|0.000000|raw2985/2986|
|`AxVkf…RqXF`|186|99/59|490,231.143942|18/10|1,466,131.570204|raw2987/2988|
|`7KMQ3…C23C`|19|9/0|956,762.331347|9/1|4,074,567.909386|raw2989/2990|
|`8ivjY…Xr1b`|5|2/1|0.000000|1/1|0.000000|raw2991/2992|
|`71F5c…zVfG`|40|17/15|0.000000|5/3|215,654.826380|raw2993/2994|
|`5YHqL…911k`|2|1/1|0.000000|0/0|0.000000|raw2995/2996|
|`4gGuX…izdg`|30|22/3|0.000000|3/2|0.000000|raw2997/2998|
|`6Q21c…QK2K`|4|2/2|0.000000|0/0|0.000000|raw2999/3000|
|`Hwpk5…5tRU`|7|5/1|75,405.663146|0/1|0.000000|raw3001/3002|
|`GGbKC…Mx2D`|5|4/0|96,899.999536|0/1|0.000000|raw3003/3004|
|`5Cyu7…N2ND`|13|3/2|0.000000|0/0|0.000000|raw3005/3006|
|`Fxb5M…KkbT`|21|17/4|0.000000|0/0|0.000000|raw3007/3008|

AxVk·7KMQ는 게시재고가 있지만 이후 추가매수가 섞였다. 게시 당시 lot의 정확한 원가·매도대금을 단순 귀속하지 않는다. 게시재고0인8주소의 이후 신규사이클도 게시전 물량으로 바꾸지 않는다.

## 타인이 비용을 낸 매수 경로에서 토큰만 수령한 경우

**9/30 11:57:54** 거래에서 서명payer `BiYy3juy8dg4iJL7okS5PAraXhjZWAJSfdBVh1hEz633`가 **10.1 USDC**를 부담했고, 다른 최종주소 `5Cyu7xT7pxB3M6o8d5rFYPwMyDnbs8Rj21mTg67sN2ND`는 직접 서명·USDC 지출 없이 **5,265.082259 ARTHUR**를 받았다. [실제 거래](https://solscan.io/tx/63axP4pBsBc1FQHvsTEXErsjNkBP73HuHKhhs3NBbbGRLywRyQTFizC5GVU7gPT3tMkKMYY9wAjgciYTeP4DkR6r), raw3005 data3.

역사 owner와 실제 명령을 대조한 경로는 payer USDC→route→ARTHUR pool→중간주소 `69yhtoJR4JYPPABZcSNkzuqbaFbwHsCkja1sP1Q2aVT5`→최종 수령 ATA `7fqc7HwhsidCqb8TsoFMFPE9fWAq6CDgZv3sL2ZqTYhx`다. payer 지출은 route10.0394+별도0.0606이며 중간 ARTHUR net0이다. gas계정은 별도 서명/fee지급자다.

이는 최종 수령자의 자체 유상 BUY가 아니다. 에어드롭으로 확정하지도 않았다. **타인 비용 부담의 route 수령**으로 별도 보존했다. 수령주소는 THESIS 때target0이며 Werey와의 사적 접점·payer의 서비스/소유/목적이 unknown이다. 중간route나pool을 뒷지갑·공급자로 승격하지 않고 신규 graph edge를 추가하지 않았다.

## SOL quote 거래와 수수료 지급의 구분

5hg의10/4 06:10:25 신규사이클은 임시wSOL계좌의 initializeAccount3/closeAccount owner·직접서명·실제전송을 확인해 BUY/SELL로 정정했다. **29,942.472798 ARTHUR**를 gross0.082736251SOL로 매수한 뒤 전량 gross0.075659251SOL로 매도했다. 매수route0.082653515+별도0.000082736SOL, 매도gross중0.000075659SOL 지급을 구분한다.

Native 계좌 변화는 매수−0.084503077SOL(quote·target ATA rent0.00151384·networkfee0.000252986), 매도+0.075578420SOL(net quote0.075583592−fee0.000005172)다. Gross quote·네트워크비·rent를 합쳐 owner순수령이나 USD수익이라고 하지 않는다. **이 신규lot은 THESIS 당시 재고0인 이후 사이클**이다.

추가13주소에서 Werey로 향한USDC는6주소·24건·합계 **6.762443 USDC**였으며 모두 같은 유상swap 안의 지급이다. BUY18건/SELL6건으로 분리했다. 수수료·추천 보상이라는 대안을 제외할 수 없어 **private funding·개인 소유·공모 관계의 근거로 사용하지 않았다**. 일반 추천 구조가 당시 개별 지급의 실제 원인이나 요율을 증명하는 것도 아니다.

## 역사 시총 선별

새 실제BUY259건은 기존exact mint mapping2268와 역사유통시총2274를 재사용해 실제매수 직전의 양수표본을 대조했다. 최대표본차이300초 기준을 유지했다. 보류257은 직전유효표본없음110·300초초과147이다.

|제외 실제BUY UTC|직전 표본 UTC|유통시총 USD|표본 차이|원문|
|---|---|---:|---:|---|
|2026-10-01T15:02:23Z|2026-10-01T15:00:00+00:00|1122159.393371904|143초|raw2987 /response/result/data/83 / /payload/market_caps/12|
|2026-10-02T05:03:25Z|2026-10-02T05:00:00+00:00|1012372.5226240456|205초|raw2987 /response/result/data/109 / /payload/market_caps/26|

두 건은 AxVk 실제BUY다. 오래된 표본이100만달러 아래 또는 위라고 해서 적격·제외를 판정하지 않았다. 이검토는 이미적격2286에서 확보된 외부매수자 exact계좌기초이며 **신규전체시장 수집0**, THESIS cap은pending이다. 단순가격·FDV·현재시총으로 대신하지 않는다.

## 종료·보존 상태

- XQ owner기존3,072행 cursor454116346:790은 빈/null raw2982로 **지정fixedquery 종료**했다. 기존raw/source관계·dust유사주소 제외를 유지했다.
- 13target410행+각빈footer종료, 누적28/62외부주소검토·34미검토다. 이는 전체시장·모든BUY지갑의60일완료가 아니다.
- 추가실제swap395 중29기존동일signature/owner/target/quote를 보존하고 **366행만 additive 적재**했다. canonical trades**1,852**, edges**423**, states**57**.
- 기존56states·11wallet resolutions·1,486trades·423edges·Fomo1,338/원래10구간404·match73을 변경하지 않았다. source raw와worker결과는 근거raw3018/검토raw3019/cap검토raw3017, state `initial_top10_arthur_additional13_inventory_exit_review_v1`에 연결했다.
- 5개 Luna/max는 읽기전용·외부요청0이었다. 본체 RPC30, Fomo·시장·Bridge·Nodit indexed·BigQuery·Chrome·문서조회 신규0이다. 이전Chrome보안확인 실패를 반복하지 않았으며 label·CEX부재 근거로 사용하지 않는다.
- 원래Top10 primary2175의60일coverage는partial_or_unknown이다. Nativealerts initial_since와 별도historicalfoundation 시작을 혼동하지 않았다.

## 다음 조사

1. **3oe quote의 미확보 실제매수/매도후 구간**에서 비서비스원금 공급·회수·author접점과 정확CEXendpoint를 찾는다. 동일target45/빈footer는 재수집하지 않는다.
2. Hwpk·GGbK의 실제quote계좌에서 같은 기준을 적용한다. 같은 거래소이름·서비스주소·소액swap지급을 동일고객으로 보지 않는다.
3. 기존62매수자의 나머지34개에서 공개재고·처분·실제작성자경제관계를 확인한다. 서비스전체pooled·반복완료query를 확장하지 않는다.
4. 원래10명전체의미확보Fomo/public/BUY-only/역사cap/체인frontier를 유지한다. 각소스의실제수집gap을 명시한다.

현재자료로 거래구조의 중간연구보고서는 쓸 수 있으나, **작성자 뒷지갑의 게시 악용·실현 수익을 확정한 완성 사례로 발표할 단계는 아니다**.
