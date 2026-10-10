# 현재 수집·분석의 한계

갱신일: 2026-10-06 UTC. 현재 우선순위는 [implementation-plan.md](implementation-plan.md), 공급원 실측은 [data-sources.md](data-sources.md)를 따른다.

- **Query 결과와 history coverage:** RZD Ethereum 고정 30일 ERC-20 결과 34행을 전체 회수했고 기존 receipt log 34/34·bridge deposit 8/8과 일치했다. 이는 indexed ERC-20 표와 알려진 표본의 일치다. Native transfer, NFT, 실패 거래, 모든 contract action·swap·quote 또는 lifetime history를 전부 수집했다는 뜻이 아니다. Provider indexing 지연도 별도 평가 대상이다.
- **Fomo history:** Top 10 REST pull은 2026-10-03~06 이벤트 200건을 반환했지만 더 이른 요청 구간의 이벤트는 없었다. `hasMore=false`를 lifetime completeness로 해석하지 않는다. Leaderboard snapshot만으로 과거 모든 순위 변동을 복원할 수 없다.
- **Wallet resolution:** Solana ranks 1·5·9·10, Ethereum ranks 8·9는 event/transaction 증거로 verified다. 다른 후보와 다른 EVM chain은 별도 검증이 필요하다. Transfer edge만으로 trader의 뒷지갑 소유권이나 동일인 여부를 확정하지 않는다.
- **Solana owner activity:** known bridge 7/7과 nonzero token-balance row 11,575/11,575가 BigQuery/RPC에서 일치했다. BQ-only 184개는 모두 net delta 0이다. Query 결과와 RPC pagination 회수를 완료했어도 native-only, historical owner metadata/closed accounts, provider indexing 및 lifetime completeness는 보장하지 않는다. Balance-only source rows는 signer와 실행 의미가 unknown이다. Known 7 BQ log samples는 비어 있어 order memo proof는 직접 RPC에 의존한다.
- **Bridge coverage:** 8개 소스 deposit 중 7개는 verified RZD Solana wallet 수령과 상관관계가 검증됐다. 10,000.55003-USDC deposit 1개는 unresolved다. Shared batch의 다른 주문을 trader에게 연결하지 않는다.
- **매매·PnL:** TRANSFER는 BUY/SELL이 아니다. 실제 swap·quote·fee·이전 취득 원가·exit가 필요하다. Fomo `usdValue`는 확인된 거래의 실제 quote 지출과 일치하지 않아 원가로 쓰지 않는다. Token-2022 과거 fee 설정과 transferred-lot basis, CEX endpoint 및 연관 지갑 선행매수는 아직 확정되지 않았다.
- **비용·재개:** Ethereum billed bytes 약 32.689GiB, Solana 3 jobs 합 약 10.976TiB는 usage 통계이며 invoice/credit balance가 아니다. Solana 참고 계산은 $68.60(무료/credits 전)이고 큰 예상량을 알린 뒤 128GiB/4TiB/8TiB cap을 적용했다. 더 비싼 24.554TiB full-detail dry run은 실행하지 않았다. 다음 Solana 수집은 token-account full RPC를 먼저 사용하고 필요한 BQ subset만 추정한다. Full capture는 로컬 재파싱하며 cloud query를 반복하지 않는다. Partial capture의 result가 만료·삭제됐다면 기존 job에서 회수하지 못할 수 있다. 새 조회가 필요한 경우 최신 예상량·상한과 작업 범위를 다시 정해야 한다.

수집 데이터·DB·인증 정보는 로컬 Git ignore 대상이다. 연구 데이터의 출처별 row identity와 timestamp를 분리해 보존한다.

- **매매 분류와 THESIS:** V3는 기존 regex가 놓친 SwapTob/SwapEvent를 성공·signer·opposing balances와 함께 처리한다. 여전히 transaction-level heuristic이며 모든 protocol/quote를 decode한 것은 아니다. RZD에서 HAMSTER의 THESIS 이전 7회 매수와 2회 매도, SAPLING의 THESIS 29초 전 매수가 관측된다. 이는 verified main wallet의 activity이며 뒷지갑 존재·의도·common ownership의 증거로 확대하지 않는다. STONK의 직전 24시간 no SWAP BUY는 더 이른 보유나 미분류 movement 부재를 뜻하지 않는다. HAMSTER net amount 이동이나 USDC 잔액 변화도 취득원가·수익률을 대신하지 않는다.
- **시간창:** 18개 Fomo event의 원천 시각과 on-chain 시각을 분리했다. Oct-06 STONK THESIS와 Oct-05 HAMSTER 두 번째 THESIS의 following 24h는 frozen end 이후로 이어져 incomplete다. Query의 time-window flag는 provider coverage 보증이 아니다. X post 시각은 미수집이다.
- **Raw 재사용:** prior point-RPC null 321건과 초기 configured Nodit method-unavailable probe는 실패/제한 근거로 남긴다. 후속 QuickNode owner full pages에서 해당 nonzero movements를 검증했다. Local replay가 새 chain query를 실행하지 않도록 saved job/page/cursor 및 comparison source FK를 재사용한다.
