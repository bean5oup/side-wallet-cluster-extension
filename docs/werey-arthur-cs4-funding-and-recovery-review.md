# Werey의 ARTHUR 매수 후보 CS4: 직접 공급과 게시 후 회수 추적

## 결론

**CS4의 실제 유상 매수→Werey THESIS→CS4의 매도는 관측됐다. CS4의 별도 공급자 AaZk도 실제 송금으로 확인했다.** 다만 AaZk 또는 CS4와 Werey의 사적 자금 연결은 아직 확인되지 않았다. 본지갑과의 접점은 같은 swap의 수수료·정산 흐름이라 뒷지갑 소유 근거로 사용하지 않았다.

매도 뒤 2,199 USDC가 공용 Relay 예금 계좌로 이동했다. 거래별 resolver는 모두 미해결이므로 최종 도착 주소와 공통 고객 CEX 입금은 미확정이다. 다음은 source 명령에 담긴 정확한 주문 ID와 공급 직전의 좁은 구간이다.

## 조사 범위와 정확 주소

원래 Top10/raw141, 고정 2026-08-08T04:43:41Z 이상–2026-10-07T04:43:41Z 미만. 시각은 모두 UTC다. CS4는 검증된 Fomo 계정 지갑으로 등록된 주소가 아니라 적격 BUY를 한 외부 주소다.

|역할|정확 주소|
|---|---|
|Werey 검증 Fomo 본지갑|`DmopudSGaQQenK4cW5NgmHUsexMB3sEJNn6n1EfLKs28`|
|ARTHUR 실제 매수자|`CS4RaxAyQYes9fHStTXc1hErzhByVsxWDKaASnigNyUd`|
|CS4 정확 USDC 계좌|`C21J3rVdDtfgrg7Z3EGSsS1S7zFsx5LmjUnjMHsKgfJk`|
|CS4 정확 ARTHUR 계좌|`CpLwWfX68Fq2joMcr67xLtRiAntzgSDU1MrtvR3pWU7k`|
|실제 SOL·USDC 공급자|`AaZkwhkiDStDcgrU37XAj9fpNLrD8Erz5PNkdm4k5hjy`|

## 실제 매수·공개·매도 순서

|UTC|관측 사실|근거|
|---|---|---|
|9/30 06:40:45|첫 관측 ARTHUR 유상 BUY, 3,000 USDC 지출. 당시 cap 보류|3133/3286|
|10/2 01:03:22, 01:03:32|500·250 USDC 두 실제 BUY. 앞선 01:00 cap $713,279.12, 표본 간격 202·212초로 두 이벤트만 적격|2274/3168, 3288 data574/575|
|10/3 10:33:00|Werey의 보존 THESIS. 직전 CS4 재고 30,121,906.732082 ARTHUR|2156, 3133|
|게시 후|대상 추가 BUY 없이 3 SELL, 합계 5,081,386.533340 ARTHUR 처분, 순 2,785.420407 USDC 수령|3133/3285–93|
|10/4 03:29:41|마지막 관측 SELL 600,000 ARTHUR. USDC gross 177.362863에서 같은 거래의 0.95 지급을 빼 exact ATA 순증 176.412863|[거래](https://solscan.io/tx/2GyaFxnnxG2GP33JLN5qbve89ytRr7ZsMhRFQEgJjrNtpf5JAiWYBnAEqm8rwZKYGL8Wufp2zSBTPxg2vr61WYnC), 직접3310|

총 57 BUY의 owner USDC 지출은 **46,755.922355 USDC**다. 최종 ARTHUR 잔량은 **25,040,520.198742**이며 원가·보유 평가·전체 수익을 확정하지 않는다. 이전 배치028/032의 **25M/25,000,000** 표현은 부정확했다. 이번 정수 잔액으로 교정하며 과거 원문·state는 보존했다.

첫 BUY와 THESIS의 역사 유통 시총은 각각 보류다. 두 후속 BUY의 적격 근거를 최초 매수·전체 보유·THESIS로 소급하지 않는다. 보존 THESIS는 확보한 공개 시점이며 절대 최초 공개나 매수의 대외 노출 시점은 별도 공백이다.

## 공급 지갑 AaZk와 다른 실제 유입

|UTC|AaZk→CS4 실제 송금|확인|
|---|---:|---|
|2026-09-16T08:38:49Z|1,016.500086077 SOL|[거래](https://solscan.io/tx/2ReCP15DQSr9XsyuwpLh9siPLagKkh48cH2Qyd5u8dQcHrcfx5SJzZhhwMPxDS5cnchVEsruYspYd7uN7836DUJk), 3295 data1/직접3306|
|2026-09-16T23:24:37Z|73,992.466501 USDC|[거래](https://solscan.io/tx/hJLwc1esACsizFZFqd6ENDsszhPmnqc8WFZrUjaa4jc7T7hpDNNS9qC3njG7hhMfKnBR3mBVBPX4x1frp2phUPs), 3285 data228/직접3307|
|2026-09-24T02:43:38Z|859.053010236 SOL|[거래](https://solscan.io/tx/yx1K2BxRq1f14zjpPacUAje9kojA1DTY7RRpFtLciBmqKtrCA2ZPhjkRyn4AiRLW7WZmHBJDrp2Lc5WrnBgT9BY), 3296 data883|

SOL 합계는 **1,875.553096313 SOL**이다. 첫 1,016.500086077 SOL 유입 후 27분24초 뒤 CS4가 기존 0.2 SOL을 포함해 SOL→USDC swap으로 98,668.955805 USDC를 받았다. 이는 거래 대상 ARTHUR 매수가 아니라 결제 자산 형성의 문맥이다. source signer·성공·native 수량·수수료와 목적지 잔액을 구분했다.

다른 중요한 일반 USDC 송금은 다음과 같다. 이 목록은 실제 원금 전송이며 소유·목적·CEX 역할은 모두 미확인이다.

|UTC|정확 source owner|USDC|근거|
|---|---|---:|---|
|2026-09-17T22:32:09Z|`Go1gXQSUbC6f29ewAqaEgmjdox74wB9rM274YWERKhaX`|3,900.000000|raw3285 · [거래](https://solscan.io/tx/4mBDwEoPwpvce7xCFonidWuAHHcKAMKCViAYthQgJFtz5MeXrf12DuEus9UJTqoQT9C5zzpibHAhZ5kQRTPpQT3h)|
|2026-09-26T16:01:21Z|`9byY2BBoUrQijZ5Xwe2KKgsmwtSCxjURLFTGZZNdrGdw`|98,515.531865|raw3285 · [거래](https://solscan.io/tx/2JzK5xWFxdw6r2MjXRCGovboQ6JvTxFNVR8j79GuCtc453tNr87By7s6qosfTDdRJFzgfmpSUeLmapQLuVYK9qRR)|
|2026-09-27T15:19:25Z|`BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6`|49,674.500000|raw3286 · [거래](https://solscan.io/tx/XueZT7fnD8DzXvPZ1hSL6LACFc2z2JfXjYQ3JH25jrA34rFkQsYLt7dpKq5A49EG3gXL3HGRFM5mPYtNTYhWALK)|
|2026-10-03T02:11:03Z|`ATTcGfaxq93t2MXFAVx8zyRkigm625DEGboQafz1TAsV`|2.000000|raw3290 · [거래](https://solscan.io/tx/2tLcudmBrUZNgCuHhyGp1PYtxUKGDmkMiHpm1wHwnWpd63vcF2XJicxDGk6yqk4b41m5ofsit6CfAcurQUmULZck)|
|2026-10-03T21:19:26Z|`CzdU9tFHHXMNUV83ecHRKHWZGqxfZyCq5ab2hud2ke4r`|5.294000|raw3291 · [거래](https://solscan.io/tx/2sdURLsqezs2vDjruc7j72e6p6D7zdpeGddZ2DeWycthFsgdFVZGib5EcPJBScPsHz6HoHAqF6JagkGmuki2NZSh)|

9by의 98,515.531865 USDC 거래는 nonce 갱신과 SPL 송금이 같은 transaction에 있다. **nonce는 DEX 명령이 아니다.** 실제 송금 authority/signer는9by이며 DSc는 nonce authority/fee payer다. 직접3309로 대사했다. 3308 HTTP408은 한 번 재시도해 성공했으며 실패를 0건으로 취급하지 않았다.

AaZk owner의 기존 신규 6,000행은8/8~8/12 21:19:16까지만 반환돼 cursor438887605:1192에서 미완료다. 공급이 발생한9/16·9/24에는 아직 도달하지 않았다. Arkham 방문3299도 보안 확인 화면이므로 라벨·역할의 부재를 뜻하지 않는다. 다음은 이 고빈도 prefix를 무작정 늘리지 않고 실제 공급 직전 구간을 조회한다.

## 매도 뒤 quote 이동과 서비스 대안

마지막 SELL 직후 exact USDC 잔액은2,119.418813이었다. 같은 거래일의 이전 자금과 다른 자산 거래가 섞인다.

|UTC|이동량|확인|
|---|---:|---|
|2026-10-04T03:29:56Z|2,000.000000 USDC → shared deposit|[거래](https://solscan.io/tx/Ro3uX5Gfdx9N2M6UrHzTUQP1NfmaNjMnCcfvDznvFUdE1nxKnicSzuEuj2ccEqFJ8futFWYHNcEc1HGh8ceoimq), raw3292|
|2026-10-04T03:30:07Z|119.000000 USDC → shared deposit|[거래](https://solscan.io/tx/FggoueiR7f92exRfvQejdEpX9ZakeuS9KAH4RgncG52xtCgGTyPN9ojmVNY2ZPZ5b6AeGjHBhNSms7Rynixfwmv), raw3292|
|2026-10-04T03:32:01Z|80.000000 USDC → shared deposit|[거래](https://solscan.io/tx/4ensatuj31rrQ3yzXMP6jU5mf5Csu5wuWvCDtoK1jZK526Df6avum4wFpiN1GGD8P8h9JFZzrADkPpuTAgTLari2), raw3292|

2,000 전송은 직접3311로도 확인했다. 중간에 기존 route 0.38과 새 F7 유입80.124509가 있으므로 **2,199 전체를 ARTHUR 매도 수익으로 귀속하지 않는다.** 대상 수취 owner는`7uTT8Xi5RWXzy7h9XL244GRgEycDYDhLjr3ZyNdXi8pZ`, ATA는`4nvJ5zWdVspxJiNZzB127U6amPH98SFFkBx2JZrAduia`이며 공용 예금 endpoint다.

고정 query에는 이 endpoint로231회·392,206.260081 USDC, 공용 F7에서172회·375,838.906958 USDC가 있다. 공용 주소가 겹친다는 사실은 같은 개인·고객의 증거가 아니다. Werey와18개 USDC 명령, F1bNo와0.9 USDC 명령도 같은 swap의 수수료·정산 대안을 유지했다. 조회한 정확 quote 계좌에서는 기존 고객 입금 후보와의 일치를 확인하지 못했으며 다른 자산·체인·중간 지갑의 부재까지 뜻하지 않는다.

resolver3312–3316은HTTP200이지만 unresolved/observations0이다. source 전송은 확인됐고 order·destination은 남았다. 기존 주문 ID 복원 방법을 새 예약에서 적용한다. 같은 미해결 호출을 반복하거나 공용 금고 전체를 특정 trader에게 귀속하지 않는다.

## 저장·완성 조건

CS4 exact USDC query8,177행+빈/null footer를 대사했고8,176개 인접 잔액 불일치는0이다. ARTHUR60행/57BUY·3SELL은 기존 데이터를 재사용했다. 매수 전 owner query2,570행+footer는 native 공급 근거이며 이후 전체 지갑 이력을 대신하지 않는다.

근거 raw3323/검토3324/cap3322, state`initial_top10_CS4_funding_and_postpublic_recovery_review_v1`. RPC26/30·Bridge5/5·Chrome1/1, 다른 신규 source0. 읽기 전용 Luna5개/max의 외부 요청0. 신규 실제 공급 TRANSFER8개만 추가했고 Fomo1,338/고정404·4,540trades·11wallet resolutions·기존65states·465edges를 보존했다. 새 edge는 ownership unknown이며 서비스·dust·수수료를 개인 연결로 등록하지 않았다.

**엄격한 저시총 완결 사례는0이며 목표는 진행 중이다.** 당시 cap, 실제 Werey 사적 자금 접점 또는 동일 고객 deposit, 주문별 도착 주소·회수, 원가·비용 근거가 남았다. 현재 자료는 관측 사실의 사례 보고서에 사용할 수 있지만 뒷지갑 동일 소유·THESIS 악용 의도·USD 수익을 확정하는 자료는 아니다.
