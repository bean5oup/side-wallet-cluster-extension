# 초기 Top10 공개 이력 공백과 연결 EVM 매수 출처 검토

## 결론

새로운 엄격한 완결 사례는 추가하지 않았다. 기존 Werey와 별도 F1bNo의 일반 송금·PURR/SI 게시 전 실제 매수·게시 후 실제 매도·Binance 라벨 경로는 [이전 보고서](werey-funded-wallet-inventory-and-cex-review.md)에 보존했다. 당시 유통 시총100만달러 이하·실질 소유·의도·원가가 미확정이라는 제한도 유지한다.

theveeman과 실제 bridge 수령이 연결된 Ethereum 후보의 LMEOW 취득 거래는 서비스가 USDC를 투입해 대상 토큰을 전달하는 경로를 시사한다. 단순 무상 전송으로 확정하지 않는다. 그러나 원래 주문·궁극 비용 부담자·같은 작성자의 같은 토큰 공개 시점이 확보되지 않아 연구의 완결 사례로 분류하지 않았다.

## 1. LMEOW 취득과 반환

Ethereum 후보 `0xa0670863bd5cd0d60022bab2eed78e81e1a06bce`, LMEOW exact contract `0x18162f5cf35647be0910f30b4466be39295e4878`. 과거 BQ 전송128행은 지정60일 query가 이미 종료했다. 새 전체시장 수집이나 BQ 요청은 없다.

새 local bridge 응답 raw3242는 취득 tx `0x6895ad31324952cd44b85d2d4c2a17e618ea7d0a71a58d3ae09b3b1322774249`의24개 ERC20 seed 로그를 보존했다. USDC3,993.266536이 Relay 서비스에서 중개 경로로 이동하고 최종 LMEOW raw `2512481646089704575768630`이 후보 EOA에 전달된다. **Resolver 상태는 unresolved, 역할unknown, observations0, Relay pending_indexing2건이다.** Seed hydration은 제공자의 거래 해석 근거이며 독립 receipt 검증이나 원래 주문 payer 확인을 대신하지 않는다.

기존10/5·10/6 두 처분의 LMEOW raw 합계는 위 수령량과 같고, 실제 Solana F5 수령 합계569.300968USDC가 대응됐다. 이 금액은 원가나 USD 수익이 아니다. 보존된 theveeman THESIS·BUY에 exact LMEOW 대응이 없지만, 공개 이력 공백 때문에 절대 부재로 결론 내리지 않는다.

## 2. Fomo 과거 pagination 확인과 실제 제한

공식 [OpenAPI](https://api.fomoapi.io/openapi.json) raw3244에서 다음 계약을 확인했다.

- `before`는 이전 응답의 **oldestCursor opaque 문자열**이며 strictly older 페이지를 요청한다. ISO 날짜가 아니다.
- `cursor`는 **nextCursor** 기반 strictly newer 증분 재개다. 두 방향을 혼동하지 않는다.
- `since`는 과거 조회의 시간 하한이며, page 결과의 `available`과 실제 범위를 함께 확인한다.

ISO before를 보낸 raw3243은HTTP400으로 실패했다. 저장된 raw2146.oldestCursor로 한 번 교정한 raw3245는HTTP200이지만 `source=memory`, `available=false`, alerts0, oldestCursor/nextCursor null, 비용0을 반환했다. **이 응답은 과거 기록0건이나60일 수집 종료가 아니다.** 현재 source가 해당 페이지를 제공하지 않는 공백으로 저장했다. 새 websocket 수집으로 전환하지 않았다.

첫 실패의 실제 과금은 응답 헤더를 확보하지 못해 미확인이다. 예산 장부에는1,500credits를 보수적으로 남겼고, 수정 요청의 실제 비용0과 구분했다. 신규 Fomo canonical event는0이다.

## 3. 다른 후보와 남은 실제 수집

8eHf STONKCATS는 DET THESIS보다47시간22분 전에 매도했다. Solstice THESIS 이후의 매도라는 시간만으로 다른 작성자와 사적 관계를 만들지 않는다. 2KNo DARK는 게시 재고가 있지만 보존 지정 계좌에서 게시 후 동일 지갑 매도가 없어 완결 사례가 아니다. 에어드롭·공유 서비스·수수료 대안을 유지한다.

다음은 **Werey 본지갑 USDC의9/11~9/29 미확보 구간**이다. 기존20,000행 prefix의 커서 `446194389:216`에서 재개하고 이미 종료한9/29 이후9,267행과 구분한다. 기존62개의 ARTHUR 매수 지갑 중 실제 일반 자금 거래 상대가 나오는지 확인하되 같은 swap의 수수료·공유 라우터·유사주소 dust는 사적 연결에서 제외한다. 이후 원래 Top10의 Solstice/F5/DET 저장된60일 frontier를 이어간다.

범위는 원래Top10/raw141, 고정2026-08-08T04:43:41Z~2026-10-07T04:43:41Z, 역사 유통 시총100만달러 이하로 유지한다. 단독RZD 예약·Top100 확대·종료한62개 대상 계좌·거래소 pooled 전체 흐름은 재수집하지 않는다.

## 4. 저장

근거raw3252/검토raw3253/시총검토raw3251, state `initial_top10_public_history_and_linked_EVM_source_review_v1`. Fomo2시도·보수적1,500credits, Bridge1, 공개문서1, RPC/시장/Chrome/BQ0. 5Luna-max는 읽기 전용·외부 요청0으로 검토했다. 기존63states·11wallet resolutions·4,540trades·465edges와 Fomo1,338/고정404events·matches73은 보존했다. 소유·의도·고객 귀속·수익은 미확정이며 연구 목표는 진행 중이다.
