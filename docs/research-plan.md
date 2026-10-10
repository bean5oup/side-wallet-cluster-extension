# 리서치 계획

## 현재 범위 — Top100 · 시총100만 달러 이하

사용자 지정 조사 상한은 **각 THESIS/CALL 게시 당시 유통 시총USD≤1,000,000**이다. 이전 $10M 가정을 대체한다. 정확한 chain/token/event가 연구 단위이며 현재 시총·FDV·unknown은 적격으로 사용하지 않는다. 기존 CZ는 FDV-only이므로 `pending_cap_proxy`다.

30d Top100 snapshot `2026-10-07T00:29:19.532Z`/raw1654와 **60일 고정 구간** `2026-08-08T04:43:41Z <= t < 2026-10-07T04:43:41Z`를 기본으로 사용한다.5개 `gpt-6-luna` · 추론 수준 `max` 작업자에게 초기1–20/21–40/41–60/61–80/81–100위 계정 기초 작업을 맡기고, 이후 중복 제거한 token/window 작업으로 전환한다. 본체가 통합·SQLite 적재·최종 근거 검토를 맡는다.

기간 설정은 `lookback_days=60`이다. Fomo 공개·매수매도 이벤트와 적격 토큰 지갑 backfill에 적용하며, 미완료 페이지는 공유 예산 안의 후속 batch에서 이어간다. 실제 확보 기간과 source gaps를 별도로 기록한다.

진행 순서:

1. Fomo 계정·chain별 지갑 후보/검증 상태·과거 THESIS/CALL/BUY/SELL과 coverage.
2. 역사적 유통 시총 gate: 적격/상한 초과/미확인/FDV-only를 구분.
3. 적격 token의 실제 pool swap/final buyer와 동일 block·10/30/60초 매수 군집.
4. 확보한 최초 공개 시각과의 비교, 공개 이후 실제 매도·quote·반환/회수.
5. 비서비스 공통 자금 공급, Fomo의 실제 접점, bridge order와 동일 exact CEX customer chain/address.
6. 여러 적격 token에서의 반복성과 반대 근거, 충분한 cost/exit/quote/fee/이전 lot의 수익 분석.

군집은 배경 거래 강도·유동성·토큰 나이가 비슷한 대조 구간과 비교한다. 같은 router/Relay/shared hotwallet은 동일인·같은 고객의 근거가 아니다. 60일 전체 공개 글과 절대 최초 공개는 근거 없이는unknown이다. PnL과 소유권도 독립 근거가 부족하면unknown을 유지한다.

운영 구조·예산·저장·완료 기준은 [병렬 조사 계획](parallel-investigation.md), 기계 판독 범위는 [정책 JSON](agent-research-policy.json), 실행 단계는 [implementation-plan.md](implementation-plan.md)를 따른다. 현재 문서화 상태이며 신규 Top100 수집과5개 작업자 실행은 별도 단계다. 이전 파일럿 결과는 [lowcap-thesis-review.md](lowcap-thesis-review.md)에 보존한다.
