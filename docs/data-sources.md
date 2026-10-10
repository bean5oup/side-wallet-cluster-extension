# Data Source Ledger

## 현재 초기10명 데이터 경로 — 2026-10-07 추가 지시

[단계별 수집/BigQuery/Chrome 계획](top10-investigation-priorities.md#데이터-수집과-chrome-추적--2026-10-07-추가-지시)을 따른다. 기초 자료는 저장 원문·Fomo REST·indexed API/RPC, 넓은 적격 token/time 후보 검색과 특정 gap은 비용을 먼저 확인한 선택적 BigQuery, 개별 자금/CEX 추적은 **Chrome의 Arkham과 올바른 체인 탐색기**를 사용한다. 본체가 Chrome을 순차 담당하고 작업자는 보존 근거를 분석한다. 기존 BigQuery job의 usage는 새 query 비용이나 현재 크레딧 잔액이 아니다. 이번 갱신에서 새 유료 query/사례 capture는 실행하지 않았다.

## 최신 BUY 검토 source — 2026-10-07

[BUY 첫 검토 보고서](buy-first-batch-review.md), review raw2140/통합 목록 raw2141을 따른다. 이 후속 배치는 시장자료20시도(429 재시도1 포함)·BSC RPC11·Nodit indexed2이고 Fomo/Bridge/BigQuery0이다. 기존 direct Solana raw698/696/695와 enhanced raw744를 재사용했다. 기존 Fomo WebSocket raw를 읽었지만 새 WebSocket 수집은 없다.

CoinGecko exact contract→coin ID와 historical market_caps는 provider assertion이다. ZCAT pointfarmcap 실제 BUY256초 전 $48.433M으로 해당1건 제외; KNOTS 실제 BUY303초 전 $2.562M은 운영300초를 넘어 보류한다. SNDK contract lookup404, DARK429후1회 retry429, 이후 ZC/TCG/CZ/ANIMA metadata는 rate limit 때문에 생략한 것으로 기록했다.

GeckoTerminal exact token current metadata는 과거 cap 대용치가 아니다. Pool minute OHLCV5시도는 raw2128–2132이며 불완전 candle을 제외했다. BSC raw2120/2121,2126/2127의 historical decimals/totalSupply와 완결 가격을 곱한 CZ≈$763,271.64, ANIMA≈$1,097,490.71은 유통 시총이 아닌 FDV proxy다. 두 candidate 전달 receipt의 payer/owner는 미확인이다. Nodit API key/header와 인증 URL은 capture에서 보존하지 않는다.

## 최신 실측 — 과거 THESIS와 저시총, 2026-10-07 UTC

아래 수치는 각 이전 관측의 snapshot이다. 최신 저시총 review는 raw2067, validation raw2068, [한글 보고서](lowcap-thesis-review.md)다. 현재 DB Fomo event999/THESIS151, scope 내 정규화 관측29행이다.

- **FomoAPI historical user THESIS:** 공개 [API Reference](https://fomoapi.io/docs)와 [live OpenAPI](https://api.fomoapi.io/openapi.json)의 `GET /v2/thesis/user/{id}?limit=100&sort=recent`를 기존 key로 확인했다. 연우 raw2016 HTTP200, source=`live-fomo`,9행, source ts9/25–10/6, cost1250credits/remaining243875. 원문·id/tradeId/userId/networkId/token/ts를 저장했다. Handle이 ID로 반환돼도 기존 stable user ID와 trader handle을 사용한다. 이 반환에는 cursor/hasMore가 없으며 두 달·lifetime 완료를 뜻하지 않는다. 고정 Top1 raw2017 HTTP200 `available:false/upstream-unavailable`,cost0이며 empty result가 아니다. User feed는 문서상 색인됨에 따라 성장하는 경로다. REST alert collection과 별도로 허용하며 WebSocket은 재개하지 않는다.
- **GeckoTerminal historical pool price:** [공급자 소개](https://www.coingecko.com/learn/dex-data-api)와 [OHLCV 명세](https://docs.coingecko.com/reference/pool-ohlcv-contract-address)의 pool/minute route를 공개 `api.geckoterminal.com/api/v2`에서 실측했다. 정확한 token address로 pools page1 및 `ohlcv/minute?aggregate=1&before_timestamp=…&limit=5&currency=usd&token=…`를 캡처했다.3토큰의 분봉을 확보,5토큰 풀과MOMO 가격은429 gap이다. Token meta를 비교하고 CALL 포함 미완료 분봉을 버렸다. 현재 liquidity/FDV를 과거 시총으로 쓰지 않는다. [Pool 명세](https://docs.coingecko.com/reference/top-pools-contract-address)는 검증되지 않은 cap이 null일 수 있음을 설명한다. 현재 풀 선택과 historical 전체 pool/liquidity의 coverage는 분리한다.
- **CoinGecko historical cap:** `baton-3` 공개 metadata의 Solana 계약이 정확히 일치했다(raw2059). [Market chart range](https://docs.coingecko.com/reference/coins-id-market-chart-range) 실측raw2060의22:00 UTC cap$14,082,929.317754881을 게시45초 전 provider assertion으로 채택해 제외했다. 현재 cap/한 시간 전 cap과 혼동하지 않는다. 키 없이 공개 route의 HTTP200을 실측한 범위만 확인했다. 유료 high-resolution plan 접근을 확인한 것은 아니다.
- **Nodit BSC historical RPC:** block/header로 게시 초까지 마지막 block126068495/다음126068496을 대조하고 CZ totalSupply/decimals를 historical eth_call로 읽었다. 풀 token0/1/fee와 공식 factory/getPool 및 Swap topic hash를 추가 확인했다.24요청 중 일시429 1회 재시도, 전체 원문 보존. 가격은 provider assertion, 발행량·pool state는 독립 RPC proof다. 유통량/PnL은 검증되지 않았다.
- **정확한 시간:** Source `ts`, market candle/sample UTC, historical block UTC, 요청/수신 시각은 별개다. 이번 Fomo raw2016/2017의 raw capture 시각은 초기 스크립트상 요청 시작이었으며 provider capturedAt와 capture file metadata도 보존했다. 신규 THESIS 게시 시점으로 capture time을 쓰지 않는다.

이번 BigQuery·Bridge 새 호출은 없고 기존 완전한 capture는 재수집하지 않았다. 다음 Fomo2/RPC30/Bridge5 한도와 source frontier는 현재 AGENTS 및 lowcap state를 따른다.

조사 및 실측 갱신일: 2026-10-06 UTC. 문서 주장, 직접 관측, 미확인 범위를 구분한다.

## 현재 사용 경로 — 확정

BigQuery는 인증된 `bq` CLI/API를 통한 과거 데이터 수집 경로로 확정했다. Query project는 `exchange-labs`이며 chain별 실제 dataset location을 지정한다. Fomo REST는 account/event/call 원천, RPC/Etherscan은 중요한 거래 검증, Bridge API는 source/order/destination 상관관계, SQLite/Python은 기준 저장소와 분석을 담당한다. RZD Ethereum 30일 수집기는 구현·실행했고 34행/2페이지를 SQLite에 적재해 기존 receipt log 34개·USDC bridge deposit 8개 모두 대조했다. 다음 작업은 known Solana bridge 수령 7건 전체 검증과 수령 이후 owner 활동 보완이다. [구현 계획](implementation-plan.md)을 따른다.

Dune 관련 아래 자료는 이전 조사 기록이다. BigQuery MCP는 사용 가능한 선택지로 조사했으나 현재 채택한 수집 경로는 API/CLI다. 초기 소량 query와 기존 Solana bridge 수령 1건 검증 이후 reusable Ethereum ERC-20 collector가 추가됐다. SQLite collection/page/transfer는 1/2/34행이다. Full result retrieval과 all-action history coverage는 구분한다.

## 요약

- Fomo 공식 사이트에서 지원 체인과 제품 기능은 확인했지만 공개 개발자 API 문서는 찾지 못했다. 비공개 API가 없다고 단정하지 않는다.
- FomoAPI.io는 Fomo와 제휴하지 않은 제3자 API다. 제공받은 key로 API 인증, 30d Top 50, BUY/SELL/THESIS 수집을 확인했다. trade history는 완전하지 않다고 API 문서에 적혀 있다.
- 초기 수집에서 Top 50 snapshot 50행과 Fomo BUY/SELL/THESIS 83건을 local ignored DB에 기록했다. 이후 user-scoped REST history pull을 더해 현재 973건을 보유한다. 초기 수집은 짧은 live capture였으며 장기 운영 품질을 뜻하지 않는다.
- Top 10 event matching 결과 Solana rank 1·5·9·10, Ethereum rank 8·9가 각각 두 개의 서로 다른 Fomo event ID와 transaction hash로 verified됐다. Rank 3과 rank 8의 Solana 후보는 복수 signature가 맞아 unresolved이며, rank 1·5·10을 포함한 나머지 EVM 후보도 chain별 증거가 없어 unverified다.
- FomoAPI.io 약관은 내부 앱/업무 이용을 허용하지만 standalone raw data/feed 재배포, bulk mirroring, 유사 경쟁 API를 금지한다. retention duration은 명시되지 않았다. fomo.family 서비스 약관과 FomoAPI.io 약관은 서로 다른 문서이며, Fomo.family 약관의 제3자 API 결과 적용 범위는 확인되지 않았다. 이 요약은 법률 판단이 아니다. [FomoAPI.io Terms](https://fomoapi.io/terms), [Fomo 서비스 약관](https://fomo.family/terms)
- Dune은 새 query 실행 권한을 확보하지 못해 사용자 요청으로 현재 경로에서 제외했다. API·dataset 조사와 cached result는 아래 이전 검토 기록으로 유지한다. 현재 indexed-history 수집은 BigQuery API/CLI로 확정했다.
- 2026-10-06 Nodit 공식 지원표에서 Ethereum Node API를 확인하고 사용자 제공 key로 Ethereum `eth_chainId`/`eth_blockNumber` 요청을 성공시켰다. 상세 범위와 제한은 아래 Nodit 항목을 참고한다.

## Fomo 서비스

### 공식 자료

Fomo 공식 안내는 Solana, Base, BNB Chain, Monad를 지원 체인으로 소개한다. 제품 안내는 API 스펙이 아니다. [Fomo 보안 및 지갑 구조](https://fomo.family/blog/learn/fomo-security-wallet-architecture), [Base 체인 출시 안내](https://fomo.family/blog/september-2025-recap)

검토한 공식 페이지에서 leaderboard, trader feed, wallet, thesis 기능은 확인했으나 공개 개발자 API의 endpoint, schema, 인증, rate limit은 확인하지 못했다.

Fomo 서비스 약관은 fomo.family 서비스 자료의 사용을 개인용으로 제한하고, 허용 예외 밖의 복제·다운로드·저장·전송 등을 제한한다. FomoAPI.io는 별도 독립 공급자다. 제3자 API 출력에 대한 두 약관의 관계나 적용 범위는 이 조사만으로 결론 내릴 수 없으므로, 이를 법률 결론으로 취급하지 않는다. [Fomo 서비스 약관](https://fomo.family/terms)

### FomoAPI.io — 주 수집 후보, 비공식

FomoAPI.io는 자사 문서에서 fomo.family와 제휴하지 않은 독립 API라고 명시한다. 문서상 기능은 다음과 같다.

- 30일 leaderboard: GET /v2/leaderboard/30d. 문서상 최대 150행, trader ID, handle, rank, PnL, volume, Solana/EVM wallet candidate 포함.
- 최근 활동: GET /v2/alerts. 문서상 BUY, SELL, THESIS와 chain 정보를 제공. 이 프로젝트는 REST만 신규 수집 경로로 사용하며 이전 WebSocket 자료는 legacy evidence로 보존한다.
- 개별 거래와 thesis: /v2/trades/{tradeId}, /v2/thesis/user/{id} 등.
- 인증: 데이터 endpoint에 Bearer API key 필요. 키 없이 조회되는 /v1 및 /health는 leaderboard/activity 데이터가 아니다.
- 문서 요금: 무료 키 월 250,000 credits. 일반 leaderboard 250, alerts REST 125, thesis 페이지 1,250, wallet resolution 2,500 credits. 2026-10-06 공식 docs 확인 기준 `/v2/alerts`는 전체 activity REST fallback이고 newest-first, `since` ISO timestamp, `limit`, `type`, `chain` 필터를 문서화한다. 같은 날 공개 OpenAPI에는 `userId`, `trader`, `cursor`, `before`, `source`, `token` query parameters도 나열됐지만 HTML 설명에는 모두 기술돼 있지 않다. server `until` filter, limit 최대값 및 retention 기간은 명시되지 않았다. [Fomo API Reference](https://fomoapi.io/docs), [OpenAPI](https://api.fomoapi.io/openapi.json)
- 범위: 완전한 Fomo trade history를 제공하지 않으며 최근 closed positions 및 cursor pagination에도 깊이 제한이 있다고 문서화되어 있다. `/v2/alerts` 응답의 `hasMore=true`는 older page가 있음을 나타낸다. 응답의 `nextCursor`와 public OpenAPI의 `cursor` query parameter를 통해 page walk를 지원하는 것으로 보이며, response `cursorNote`는 inclusive timestamp 경계에서 cursor 사용을 지시한다. provider retention과 global history completeness는 여전히 unknown이다. 주소 기반 on-chain backfill은 별도로 필요하다.
- 약관: 조회 데이터의 내부 앱/업무 사용을 허용하며 standalone raw data/feed 재배포, bulk mirroring, substantially similar competing API를 금지한다. 명시적 보관 기간은 찾지 못했다. 내부 전용 로컬 DB에 한정하고 raw data를 공개하지 않는다. [FomoAPI.io Terms](https://fomoapi.io/terms)

직접 관측:

- 2026-10-05 초기 smoke test에서 30d leaderboard 3행, alerts BUY/SELL/PERP 3건, THESIS 1건 응답을 확인했다. 이 최초 smoke payload는 저장하지 않았다.
- 과거 live collector가 저장한 WebSocket rows는 legacy raw records로 유지한다. 2026-10-06에 새 REST-only collector를 추가했다. 각 raw response에는 route/query, capture time, HTTP status와 credit cost/balance가 저장된다. OpenAPI의 `userId` filter는 10개 Top 10 user에 대해 실제 요청했고 response `filters.userId` 및 row userId가 모두 일치했다. 각 user response의 `hasMore`는 false였으며 0–101 rows를 반환했다. 별도의 global `since=2026-09-06&limit=1000` probe는 500 rows, `hasMore=true`, `nextCursor`를 반환했다. global feed를 계속 페이지 처리하지 않고 Top 10 user 범위로 제한했다.
- Top 10 user-scoped API page는 총 200 unique events였다(99 BUY, 84 SELL, 17 THESIS; Solana 140, Robinhood 42, Ethereum 18). timestamp 범위는 2026-10-03 03:03~2026-10-06 02:37 UTC다. 요청 since는 2026-09-06이었지만 그보다 이전 alert는 반환되지 않았다. 이는 endpoint의 현재 관측 가능한 범위이며 Fomo account의 lifetime activity가 아니고, retention 미확인 때문에 과거 alert 부재를 입증하지 않는다.
- Rank별 반환 이벤트 수: rank 1 8건(5 BUY, 3 THESIS), rank 2 2건(1 BUY, 1 THESIS), rank 3 2 BUY, rank 4 2 BUY, rank 5 101건(49 BUY, 52 SELL), rank 6·7 각 0건, rank 8 22건(8 BUY, 8 SELL, 6 THESIS), rank 9 34건(16 BUY, 11 SELL, 7 THESIS), rank 10 29건(16 BUY, 13 SELL). 모든 per-user response가 `hasMore=false`였다.
- trade detail 1건은 21 swaps와 111 transfers를 표시했지만 문서화된 필드에서 transaction signature/hash를 확인하지 못했다. `/v2/users/{userId}/swaps?limit=50`은 retryable HTTP 503을 두 차례 반환했다.
- 2026-10-06 KST REST history query는 이전에 event 0건으로 보이던 rank 1에서 Solana BUY 5건과 THESIS 3건을 반환했고 이후 두 개의 distinct event/signature match로 검증됐다. rank 5와 9도 같은 기준으로 검증됐다. 이전 user-specific swaps 요청 HTTP 503 이력은 별도 endpoint의 제한으로 유지한다.
- 이번 EVM pilot 이후 로컬 DB 집계는 100 leaderboard rows(30d Top 50 snapshot 2회), 973 Fomo events, 458 trader records, 911 raw payloads, 16 candidate/matched on-chain trades, 12 verified event-match links, 8 ambiguous links다. Solana rank 1·5·9·10과 Ethereum rank 8·9가 각각 두 개의 distinct event/signature로 verified됐다. Rank 3과 rank 8의 Solana 후보는 ambiguous이며 나머지 EVM 후보는 unverified다. 정규화 결과는 33,382 wallet/signature actions, 51,885 token deltas, 27 timeline rows다. 이번 EVM Fomo API 조회 후 잔액은 246,250 credits다. 민감할 수 있는 trader handle, token, wallet ID와 raw payload는 이 문서에 기록하지 않았다.

문서 요금 기준 시간당 30d Top 50 snapshot은 720 × 250 = 약 180,000 credits/30일이다. REST alerts를 15분마다 10명 모두 조회하면 최대 28,800 requests × 125 = 3,600,000 credits/30일이므로 무료 한도를 크게 넘는다. 실제로는 empty user-scoped response가 0 credits일 수 있고 per-user/chain/type filter로 query를 줄일 수 있다. 현재 CLI는 한 user의 증분 조회와 page 수 제한을 지원하지만 자동 scheduler는 없다. 실제 반복 주기를 정할 때는 요청 건수 및 응답 credit headers를 기준으로 월 비용을 먼저 산정한다. [FomoAPI.io API Reference](https://fomoapi.io/docs), [OpenAPI](https://api.fomoapi.io/openapi.json)

### PooTracker Fomo API — 비교·보조 후보, 현재 신뢰도 낮음

공개 GitHub 저장소는 비공식 API라고 밝히며 profile, wallet, leaderboard, thesis 및 live thesis stream 경로를 설명한다. hosted collector와 데이터베이스는 별도 운영이라고 명시한다. [공개 저장소](https://github.com/deladevsol/fomo-api), [OpenAPI 스키마](https://fomo-public.pootracker.app/openapi.json), [API 문서](https://fomo-public.pootracker.app/docs)

2026-10-05 직접 확인: `/v2/status`는 HTTP 200이었으나 색인 범위는 partial, swaps 202, transfers 0이었다. feed collector는 29,586회 연속 upstream HTTP 403을 보고했고, 30d leaderboard의 마지막 성공 시각은 2026-09-13이었다. 직접 leaderboard 조회도 HTTP 403. status의 unresolvedFeedGaps=0은 오래된 성공 시각과 장기 403이 함께 있는 상태이므로 complete history로 해석하지 않는다.

따라서 현재 ingest source로 추천하지 않는다. 회복 후 cross-check 용도로 재평가한다. [상태 endpoint](https://fomo-public.pootracker.app/v2/status), [30일 leaderboard endpoint](https://fomo-public.pootracker.app/v2/leaderboards/traders?window=30d)

## 온체인 데이터

### Nodit — supported chains and Ethereum Node API

- 2026-10-06에 Nodit의 공식 [Supported Networks](https://developer.nodit.io/en/guides/supported-networks/)와 [API Overview](https://developer.nodit.io/en/api/api-overview/)를 확인했다. 공개 지원표에서 Node API(Elastic Node)는 Ethereum, Arbitrum, Avalanche, Base, BNB, Kaia, Optimism, Polygon, World Chain 등에서 제공된다. Ethereum은 Node API와 Web3 Data API, Webhook, Stream 모두 지원표에 표시되어 있다. 지원 여부와 testnet 범위는 네트워크별로 다르다.
- Fomo 리서치와 직접 관련된 Ethereum, Base, BNB Chain은 지원표에 있으나, Monad와 Robinhood Chain은 현재 공개 지원표에 나타나지 않는다. 이 표에 없다는 사실만으로 Dedicated Node 등 별도 계약 제품까지 지원하지 않는다고 단정하지 않는다.
- Nodit Node API URL 형식은 `https://{chain}-{network}.nodit.io/{API_KEY}`이며 Ethereum Mainnet host는 `ethereum-mainnet.nodit.io`다. API key는 URL 경로 또는 `X-API-KEY` header 중 하나로 전달할 수 있고 두 방법을 동시에 쓰면 401이 난다. 인증된 URL은 로컬 ignored `.env`에만 두고 `.env.example`에는 placeholder만 둔다. [API key 안내](https://developer.nodit.io/en/api/api-key/)
- 사용자 제공 key로 `ETHEREUM_RPC_URL`을 로컬 ignored `.env`에 설정했다. 2026-10-06의 `eth_chainId`, `eth_blockNumber`, `eth_getTransactionByHash`, `eth_getTransactionReceipt`, `eth_getCode` 호출은 성공했다. 이 endpoint는 아래의 제한된 Ethereum event matching에 쓰였지만 주소 전체 history coverage를 제공한다고 확인된 것은 아니다.

### Ethereum event-match pilot — 2026-10-06

- Nodit 공식 지원표는 Ethereum Mainnet Node API와 Web3 Data API를 모두 지원한다고 표시한다. Web3 Data API의 `getTokenTransfersByAccount`는 주소, 토큰 컨트랙트, 날짜 범위를 받아 ERC-20 transfer의 `from`, `to`, raw `value`, `timestamp`, `blockNumber`, `transactionHash`, `logIndex`와 token decimals를 돌려준다. [Nodit Supported Networks](https://developer.nodit.io/en/guides/supported-networks/), [Get Token Transfers by Account](https://developer.nodit.io/en/api/web3-data-api/gettokentransfersbyaccount/)
- 이 pilot은 fixed Top 10 중 Ethereum `chain_id=1` 알림이 있는 rank 8(IMD BUY 2건)과 rank 9(STOCKER BUY 14건, THESIS 2건)만 조회했다. `getTransactionsByAccount`는 두 주소의 제한된 날짜 구간에서 HTTP 200/count 0을 반환했다. 같은 구간의 `getTokenTransfersByAccount`는 target-token inbound transfer를 rank 8에서 2건, rank 9에서 14건 찾았다. 네 표본 transaction의 outer sender와 `to`는 후보 주소가 아니었고, receipt의 target-token Transfer log 수취인은 후보 주소였다. 그러므로 빈 account-transaction 결과를 token activity 부재로 읽지 않는다.
- Fomo API의 rank 8 `/v2/users/{userId}/swaps?tokenAddress={IMD contract}` 응답은 5개 fill을 반환했고 그중 알림 시간대 2개는 Nodit raw transfer amount와 0.01 token 단위로 일치했다. Rank 9 `/v2/trades/{tradeId}`의 15개 개별 swap detail 중 14개가 같은 방식으로 Nodit transfer와 일대일 일치했다. rank 9의 15번째 detail fill에는 저장된 alert event가 없었다. `/positions`는 포지션 집계, `/swaps`와 trade detail은 개별 fill이며, 각 rank의 검증된 두 fill은 하나의 umbrella `tradeId` 안에 있다. 따라서 여기서 verified는 두 독립 이벤트·서명 쌍의 wallet 해상도를 뜻하며, 두 개의 별도 포지션을 뜻하지 않는다. [Fomo API Reference](https://fomoapi.io/docs), [Fomo OpenAPI](https://api.fomoapi.io/openapi.json)
- 네 개의 선택된 alert/transaction 쌍은 모두 성공한 Ethereum receipt(`status=0x1`)를 갖는다. 후보 주소는 calldata에 나타나고, token contract·raw output amount·수취인이 맞으며, Fomo event와 transaction 간 시간차는 각각 -13초/-9초(rank 8), +2초/-8초(rank 9)다. delta는 `onchain time - Fomo event time`이다. 각 rank에서 두 event ID와 두 transaction hash가 달라 SQLite `wallet_resolutions`의 `chain='ethereum'` 행은 verified, 네 `event_trade_matches` 링크도 verified로 기록했다. 나머지 rank 9의 12개 pair는 일대일 transfer/fill 비교에는 포함했지만 이 pilot에서 개별 receipt를 더 조회하지 않았다.
- 외부 executor가 transaction을 제출했고 outer `from`은 후보 주소와 다르다. 후보 주소는 output token을 직접 받았고 calldata에도 포함된다. 이 근거는 event-to-wallet 관계를 지지하지만 후보가 transaction의 outer signer라는 주장은 하지 않는다. 제3자 API에서 rank 8 Ethereum `tokenIn.address`가 Solana USDC mint로 보고되는 데이터 이상도 발견했다. [Circle supported blockchains](https://help.circle.com/support/en/usdc-supported-blockchains-minting-redemption-faqs?id=kb_article_view&sysparm_article=KB0010590) Fomo alert `amount_usd`도 개별 fill notional로 사용하지 않는다. Quote token/금액, protocol, `amount_usd`는 on-chain trade row에서 NULL로 남겼으며 PnL은 계산하지 않았다.
- `/v2/trades/{tradeId}`와 `/v2/users/{userId}/positions`의 rank 8 호출은 각각 retryable HTTP 503을 반환했고 비용은 0이었다. rank 9의 trade detail과 positions, rank 8의 token-scoped swaps 성공 호출은 각 250 credits를 사용해 총 750 credits였다. 마지막 확인 잔액은 246,250 credits다. Rank 9 position 응답의 BTE/Ethereum 행에는 fixed Top 10 alert table의 대응 event가 없어 이를 별도 지갑 활동으로 해석하거나 추가 조회하지 않았다.
- 이 결과는 두 verified Ethereum 지갑의 alert-window corroboration이며 30~90일 history backfill이 아니다. Nodit account transaction query가 0건인 relay/router 거래를 주소 전체 이력으로 확장할 방법, router 내 quote leg와 비용 귀속, 이후 exit 기록은 미확인이다. Robinhood Chain(4663) history도 별도 provider access가 확보되지 않아 현재 scope 밖이다.

### Solana

공식 JSON-RPC `getSignaturesForAddress`는 주소를 참조하는 signature를 최신순으로 반환하고 `before`/`limit` 페이지네이션을 지원한다. `getTransaction`은 signature의 transaction과 metadata를 조회하며 결과가 없으면 null일 수 있다. 운영자별 rate와 보존 범위는 다르다. [Solana RPC 개요](https://solana.com/docs/rpc), [getSignaturesForAddress](https://solana.com/docs/rpc/http/getsignaturesforaddress), [getTransaction](https://solana.com/docs/rpc/http/gettransaction)

2026-10-06에 네 RPC endpoint를 비교했다. 이전 shared public endpoint `https://api.mainnet.solana.com`은 verified wallet 하나에 대해 최근 60일 조회에서 4페이지, 3,776 signatures를 반환했다. 가장 오래된 block time은 2026-08-24로 cutoff 2026-08-06보다 약 18일 짧았다. 마지막 페이지가 1,000건보다 작아 해당 endpoint가 반환하는 주소 이력 끝에 도달했다. `getFirstAvailableBlock`은 slot 0, block time 2020-03-17이었다.

사용자가 제공한 Nodit endpoint는 로컬 `.env`의 `SOLANA_RPC_URL`로 설정했다. credential이 포함된 URL은 출력·문서화하지 않는다. Nodit에서 저장된 최근 매칭 거래 1건의 성공 응답을 확인했다. `getFirstAvailableBlock`은 slot 450488863, block time 2026-09-25를 반환했고, 동일 wallet의 조회는 2페이지, 1,653건으로 가장 오래된 기록이 2026-09-25였다. 이 endpoint의 관측 history는 약 11일로 60일 백필에는 부족하다.

사용자가 별도로 제공한 Helius endpoint도 비교 조회했다. 인증 URL은 `.env`에 저장하지 않았다. `getFirstAvailableBlock`은 slot 0, block time 2020-03-16이었다. verified wallet의 60일 서명 조회는 4페이지, 3,778건이며 가장 오래된 것은 2026-08-24였다. Helius에서 저장된 최근 매칭 transaction 1건이 성공 응답으로 조회됐다.

이어 사용자가 제공한 QuickNode endpoint도 비교했다. 인증 URL은 `.env`에 저장하지 않았다. `getFirstAvailableBlock`은 slot 0, block time 2020-03-16이었고, 동일 wallet의 서명 조회는 4페이지, 3,778건으로 2026-08-24부터였다. 최근 매칭 transaction 1건도 성공 응답으로 조회됐다. Helius와 QuickNode 결과는 서로 같고, 이전 shared public RPC도 4페이지, 3,776건, 주소 시작 날짜 2026-08-24, 원장 slot 0이었다. 세 개의 깊은 endpoint가 이 주소의 최초 관측 날짜를 교차 확인했다. Nodit은 slot 450488863 / 2026-09-25부터만 반환해 약 11일 범위다.

검증된 이 wallet은 현재 관측상 약 42.6일 이력을 가진다. 세 깊은 endpoint 모두 2026-08-24 이전 서명을 반환하지 않았지만, 이 결과를 Solana 공통 RPC 한계로 일반화하지 않는다. 2026-10-06 Top 10 파일럿에서는 다른 주소 8개가 60일 cutoff 이전 서명을 반환했다. 원장 boundary가 slot 0인 provider에서 나머지 2개 주소는 각각 약 35일/42.6일 시점에 signature pagination이 끝났다. 주소의 최초 관측 활동으로 보이나 keypair 생성일과 같다고 단정하지 않는다. verified wallet 거래 상세 3,782건은 이후 QuickNode enhanced API로 raw backfill했으며 의미 정규화는 미완료다.

Solana event match는 event timestamp ±120초 안의 signature만 확인한다. 거래 성공, API wallet candidate의 signer 여부, Fomo BUY/SELL 방향과 일치하는 token delta, quote balance 이동 또는 swap log 증거를 확인한다. 단일 event로 wallet을 확정하지 않는다. 현재는 서로 다른 Fomo event 2건과 서로 다른 transaction signature 2건이 일치해 wallet resolution이 verified다. timestamp delta는 2초와 1초였다. Helius `getTransactionsForAddress`는 더 깊은 history 후보지만 유료 플랜과 credential이 필요하므로, accessible provider의 history와 처리량을 먼저 확인한 뒤 선택한다. [Helius historical RPC 안내](https://www.helius.dev/blog/introducing-gettransactionsforaddress), [요금제](https://www.helius.dev/pricing)

### Top 10 Solana pilot — 2026-10-06

- 2026-10-05 16:04:43.128 UTC의 30d Top 50 snapshot에서 rank 1–10을 고정했다. Fomo leaderboard의 wallet fields 10개 모두 Solana와 EVM 후보 주소를 제공했다. 후보는 identity proof가 아니므로 독립 event match 전에는 wallet로 확정하지 않는다. inventory는 ignored `data/research/top10_wallet_inventory.csv`에 있다.
- 공유 Solana mainnet RPC의 `getSignaturesForAddress`로 각 주소를 60일 cutoff까지 페이지 조회하고 원문 JSON 응답을 local SQLite raw layer에 저장했다. 8/10 주소는 cutoff 이전 signature를 반환했다. 2/10은 전체 반환 목록이 각각 약 35.1일, 42.6일의 observed activity에서 끝났다. 이는 provider 공통 보존 한계가 아니라 이 주소들의 현재 조회에서 가장 오래된 활동이다. 정확한 keypair 생성일은 알 수 없다.
- rank 1 후보는 60일 구간에 24,563 signatures가 있어 처음 20페이지로는 약 28.8일만 내려갔다. 추가 페이지를 이어 받아 25페이지에서 2026-08-05까지 도달했다. 이후 REST에서 서로 다른 Fomo BUY event 2건과 성공한 signature 2건이 일치해 rank 1은 verified 처리됐다.
- REST 기반 event matching 결과 Solana rank 1·5·9·10은 각 두 개의 distinct Fomo event와 successful Solana signatures로 verified됐다. Solana rank 3·8은 event window에 복수의 plausible signatures가 있어 unresolved다. 별도로 Ethereum의 rank 8·9 EVM 후보는 각각 두 개의 successful event/signature matches로 verified됐다. Rank 8의 `robinhood` THESIS(chain ID 4663)는 그 chain에서 후보 주소와 연결하는 tx evidence가 여전히 없다. 매칭 원본은 SQLite `event_trade_matches`에 저장하고 `top10_event_trade_matches.csv`는 해당 관계형 데이터의 export다.
- QuickNode 공식 `getTransactionsForAddress`는 `transactionDetails: "full"`, `limit`, `paginationToken`, `maxSupportedTransactionVersion`을 지원하며 API 문서는 호출당 120 credits로 표시한다. Rank 10의 기존 backfill은 3,782 records(2026-08-24~2026-10-05, 성공 3,603/실패 179; raw pages 16개)다. 2026-10-06에 ranks 1·5·9를 각각 60일 cutoff까지 추가 수집했다: 122/24,400, 18/3,600, 8/1,600 full transaction rows. 148 requests의 문서상 비용은 17,760 credits이며, response headers에는 남은 잔액이 없어 actual QuickNode balance는 unknown이다. 2026-10-05 16:08~16:10 UTC에 저장한 기존 signature probes와 같은 60일 cutoff로 대조한 결과, 그 probes의 signature 중 full-transaction 결과에서 빠진 것은 없고 이후 약 11시간 사이 rank 1·5·9에 각각 140·74·1개의 추가 signature가 관측됐다. 이는 두 capture 사이 새 활동까지 포함한 cross-check이지 provider lifetime completeness 증명은 아니다. 끝 경계를 확인하기 위해 cutoff 바깥의 일부 row가 각 마지막 page에 포함된다. 새 raw pages는 SQLite에 보존됐고 credentials는 `.env`에 저장하지 않았다. [QuickNode getTransactionsForAddress 문서](https://www.quicknode.com/docs/solana/getTransactionsForAddress)
- `PYTHONPATH=src python3 -m fomo_research build-timeline --rank-limit 10`은 QuickNode raw pages를 읽어 normalized SQLite tables와 CSV exports를 재생성한다. Current totals are 33,382 wallet/signature actions (16,803 SWAP, 9,039 TRANSFER, 7,540 UNKNOWN), 51,885 token deltas, and 27 token timeline rows. These labels require protocol-level review. A shared transaction signature is retained once per tracked wallet, preserving each wallet's balance changes. Historical 60-second/five-minute WebSocket captures remain legacy evidence only; the new collector uses REST. A first observed SWAP BUY precedes the first returned Fomo BUY in 5/5 rank-1 token rows, 3/8 rank-5, 0/1 rank-9, and 2/3 rank-10. First observed does not mean lifetime first, and these counts alone do not establish causation or profit. The rank-10 SNDK/ZCAT review remains the only full token-level quote/fee review. A later local pass also checked quote mints and program instructions for all eight verified event-match transactions and screened direct transfers for the 27 timeline tokens. Fomo `usdValue` did not reconcile to observed quote amounts; transfer basis and post-event exits remain unresolved.

### Event-token comparison pilot — 2026-10-06 KST

The table below is the initial detailed comparison for rank 10, using each verified Fomo BUY source timestamp as t0 and that wallet's normalized same-token actions. SWAP and TRANSFER labels remain heuristics from success/signer/balance/log evidence. Token quantities are UI token units, not USD. The four-wallet aggregate timing summary follows the quote review.

| Token | Before the Fomo BUY | Fomo event and observed on-chain sequence |
|---|---|---|
| SNDK | In the prior 24 hours: one SWAP BUY at 10:07:18 UTC (4h45m22s before t0) and eight inbound TRANSFER actions; their net wallet token balance delta is +4,685,361.071. No SELL is recorded in the retained history. | Fomo BUY at 14:52:40 UTC; matching on-chain SWAP BUY at 14:52:41 (+1s). No later same-token action appears before the wallet history ends at 16:05:28 UTC. |
| ZCAT | In the prior 24 hours: no same-token swap or transfer. In the prior seven days: one SWAP BUY at 2026-10-01 17:22:50 UTC (3d21h30m45s before t0) and one inbound TRANSFER. Across the retained pre-event history: six SWAP BUYs, three SWAP SELLs, and 21 TRANSFER actions (18 net inflows, 3 outflows; net +18,723,777.073 token units). | Fomo BUY at 14:53:35 UTC; matching on-chain SWAP BUY at 14:53:37 (+2s). No later same-token action appears before the wallet history ends at 16:05:28 UTC. |

Interpretation limits: SNDK shows pre-event token swaps and transfers into the already verified trader wallet, while ZCAT shows earlier trading and transfer activity with no same-token action in the 24 hours before the Fomo event. Transfers describe token balance movement, not purchase cost; this analysis did not inspect transfer counterparties or attribute another wallet. ZCAT's prior sells also prevent inferring that all earlier bought tokens remained held until the Fomo event. The quote-flow and fee evidence below supports cashflow comparison only; transfer basis and post-event exits are missing, so realized/unrealized PnL and continued holding cannot be concluded.

#### Quote and fee review — 2026-10-06 KST

The review covered the 12 heuristic SWAPs that changed the same target tokens in the retained transaction history (SNDK: 2, ZCAT: 10). For each, the largest counter-token balance change in the expected opposite direction was the official Solana mainnet USDC mint with 6 decimals. This classification is based on balance deltas; it does not identify the DEX/router. Solana's payments documentation lists the mainnet USDC mint and says to validate the mint rather than rely on a token label. [Solana payments documentation](https://solana.com/docs/payments/how-payments-work)

| Token | Before Fomo BUY: USDC swap flows | Fomo-matched on-chain BUY | Transaction `meta.fee` across reviewed swaps |
|---|---|---|---|
| SNDK | BUY 3,000; SELL 0 | BUY 5,000 USDC | 0.002947756 SOL total (0.002407560 before event; 0.000540196 matched transaction) |
| ZCAT | BUY 8,500; SELL 4,456.138577; net spent 4,043.861423 | BUY 5,000 USDC | 0.007982171 SOL total (0.007917250 before event; 0.000064921 matched transaction) |

All 12 QuickNode records expose `meta.fee`. In their message account keys, the tracked wallet is at index 1 and a different account is at index 0; Solana's transaction documentation identifies the first account as the fee payer. Therefore these are transaction-level network fee amounts, not costs attributed to the tracked trader. The fee payer's identity was not inspected. Fees were not converted to USD. [Solana fee-payer documentation](https://solana.com/docs/payments/send-payments/payment-processing/fee-abstraction), [QuickNode `getTransactionsForAddress` documentation](https://www.quicknode.com/docs/solana/getTransactionsForAddress)

For both captured rank-10 Fomo BUY alerts, the stored `usdValue` equals the raw `positionValueUsd` field (30,652.42 and 602,636.52), while each matched on-chain BUY spends 5,000 USDC. The feed's reported value does not reconcile to the wallet's transaction consideration. In the current schema, `fomo_events.amount_usd` preserves source `usdValue`, while `onchain_trades.amount_usd` remains NULL; do not compare those columns as the same metric. Keep provider-reported value separate from on-chain quote cashflow until its field semantics are resolved. [Fomo API Reference](https://fomoapi.io/docs)

These amounts are nominal USDC cashflows from a verified wallet and heuristic SWAP labels. SNDK's observed transfers make the full token cost basis unknown, and there is no observed sell in the retained history. ZCAT has prior buys, sells and transfers, so its remaining token basis cannot be inferred by summing buys; no post-event sell is observed. This evidence is not realized or unrealized PnL.

### Four-wallet event timing summary — 2026-10-06 UTC

Using the regenerated 60-day history for ranks 1, 5, and 9 plus rank 10's available 42.6-day history, the first heuristic SWAP BUY observed for a Fomo-BUY token predates the first returned Fomo BUY in 5/5 rank-1 token rows, 3/8 rank-5 rows, 0/1 rank-9 row, and 2/3 rank-10 rows. Among rows with a prior buy, the median gap from the first observed SWAP BUY to the first returned Fomo BUY is 701.06 hours for rank 1, 14.68 hours for rank 5, and 427.99 hours for rank 10. This uses the earliest observed buy in each available history, not the nearest preceding buy; several gaps are weeks long. The measure is a discovery summary, not evidence of intent, a causal lead, or PnL. The later event-match pass identified program instructions for eight verified transactions; full protocol decoding for every timeline swap, acquisition cost for transferred lots, and post-event exit accounting remain open.

#### Verified-match quote, program, and transfer check — 2026-10-06 UTC

This pass used only the existing SQLite and QuickNode raw pages; it made no provider calls. All eight independently verified event/signature matches show the official Solana USDC mint (`EPjFWdd5...Dt1v`, 6 decimals) as the counter-token movement. Circle identifies that mint as native USDC on Solana. [Circle supported blockchains](https://help.circle.com/support/en/usdc-supported-blockchains-minting-redemption-faqs?id=kb_article_view&sysparm_article=KB0010590)

| Rank | Verified event-linked quote movements | Swap/router instructions visible in the transaction logs |
|---|---|---|
| 1 | 2 BUYs; 2,000 USDC spent per match | DFlow-routed transactions with Raydium CLMM/CPMM and Meteora DLMM instructions |
| 5 | 1 BUY; 5,499.999999 USDC spent. 1 SELL; 5,452.487854 USDC received | BUY calls PumpSwap and Meteora DLMM. SELL calls the DFlow program and Meteora DLMM |
| 9 | 2 SELLs; 9,924.582990 and 7,936.853418 USDC received | DFlow and Meteora DLMM; one transaction also calls Orca Whirlpools |
| 10 | 2 BUYs; 5,000 USDC spent per match | Raydium CLMM/CPMM and Meteora DLMM; one transaction also calls Jupiter v6 and Orca Whirlpools |

Protocol identification comes from successful transaction log instruction names and program IDs, checked against protocol-maintained references: [Raydium](https://github.com/raydium-io/raydium-library), [Meteora DLMM](https://github.com/MeteoraAg/docs/blob/main/developer-guides/dlmm/index.mdx), [Orca Whirlpools](https://github.com/orca-so/whirlpools), [PumpSwap](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_SWAP_README.md), and [Jupiter's v6 instruction parser](https://github.com/jup-ag/instruction-parser). Some transactions call several venues through a router; the venue instruction count is not a count of separate wallet trades. The DFlow program ID has a `Swap` log instruction, but its protocol label has not been independently confirmed from a primary DFlow source.

A separate local pass examined 956 normalized `TRANSFER` actions that changed tokens in the 27 verified-wallet timeline rows. It decoded SPL `Transfer`/`TransferChecked` legs and matched source/destination token-account owners from transaction balance metadata. Gross instruction amounts exactly equal the tracked wallet's pre/post token-balance delta in 342/956 rows: rank 1 212/752, rank 5 62/64, rank 9 37/48, rank 10 31/92. The other 614 rows also reconcile when the inbound Token-2022 fee is applied using an exact rate independently observed for the same mint: each matches a 1% or 3% fee rounded up per instruction. This applies to 11 target-token mints (8 with 3% observed, 3 with 1%); per-mint evidence did not show a conflicting rate in the retained records. Of those 614 rows, the nearest same-mint single-inbound fee observation precedes 473 rows and is within seven days for 458; the other 141 use a later observation. Solana documents that `TransferFeeConfig` withholds a fee on the recipient and that `TransferChecked` applies the configured fee. We did not fetch historical mint extension state, so the fee-adjusted arithmetic is strong transaction-level evidence, not an independent proof of the fee configuration at every past slot. Transfer amounts now reconcile under this empirically derived fee model, but this alone does not establish each transferred lot's acquisition cost. Direct counterparties were not followed into other wallets. This bounded-history screen does not establish complete token inventory or PnL. [Solana Token-2022 transfer fees](https://solana.com/docs/tokens/extensions/transfer-fees)

Remaining local analysis includes fee-aware per-token inventory lots and post-event exit accounting for the 27 timeline rows, with fee-config/history gaps preserved. The current next step is the bounded RZD BigQuery collector in the implementation plan. Robinhood Chain history still needs a usable indexed/archive source; no such source has been verified for this project, and Dune is excluded from the active workflow.

### EVM — Robinhood Chain

- Fomo event의 `chain_id=4663`은 Robinhood 공식 문서상 Robinhood Chain 메인넷 ID이며, EVM 호환 Arbitrum L2다. 공식 explorer는 Blockscout다. 공식 문서는 공개 RPC가 rate-limited라 production에 권장하지 않고, historical reads/indexing은 archive/indexed provider를 이용하라고 안내한다. [Robinhood Chain 연결 문서](https://docs.robinhood.com/chain/connecting/)
- Blockscout의 공식 Robinhood API 문서는 주소 거래내역 REST 경로(`/4663/api/v2/addresses/{address}/transactions`)를 제시하고 PRO API access에 API key가 필요하다고 명시한다. 2026-10-06 직접 probe에서는 explorer host의 공개 주소 거래내역 endpoint가 HTTP 403을 반환했다. Robinhood 공식 공개 RPC의 단일 `eth_chainId` 요청도 현재 실행 환경에서 HTTP 403을 반환했다. 거래 이력은 수집되지 않았다. [Blockscout Robinhood API 문서](https://github.com/blockscout/docs/blob/main/robinhood-api.mdx), [공식 Robinhood public RPC 안내](https://docs.robinhood.com/chain/connecting/)
- 당시 직접 RPC/Blockscout probe는 HTTP 403을 반환했다. Dune은 Robinhood Chain 데이터 페이지를 제공하지만, 현재 MCP 권한은 visitor/read-only라 새 query 실행을 할 수 없다. 과거에는 실행 권한을 확보한 뒤의 query 후보로 검토했으나 현재 경로에서는 제외했다. Public cached result로는 주소별 역사 coverage를 확인하지 못했다. 단일 THESIS event와 단순 token transfer만으로 trader-wallet linkage나 BUY/SELL을 검증하지 않는다.

### Dune SQL / Query API — 이전 검토 기록, 현재 제외

2026-10-06 기준, Dune은 SQL 기반 온체인 데이터 카탈로그와 query execution/results API를 제공한다. 당시 검토한 후보였으나 현재 indexed data source는 BigQuery API/CLI로 확정했다. 아래 Dune 저장 구조와 POC 조건은 과거 제안 기록이다.

#### 검증된 기능과 데이터

- Dune curated `dex_solana.trades` 테이블은 Solana DEX trade row를 제공한다. 공개 스키마에 `block_time`, token sold/bought mint/amount, `trader_id`, `tx_id`, project 정보가 있다. 하나의 tx에서 하나 또는 여러 trade row가 나올 수 있다. 따라서 이 테이블로 DEX trade를 조회할 수 있지만, 전체 Solana transaction, non-DEX 동작, transfer, failed transaction의 완전한 원장으로 해석하면 안 된다. [Dune DEX Trading dataset](https://dune.com/data/dex-trading?id=dex_solana.trades)
- Robinhood Chain이 Dune blockchain explorer에 등록돼 있고 chain activity/dashboards가 노출된다. 다만 우리 EVM candidate address를 조회할 때 사용할 raw table 이름과 coverage는 아직 실제 query로 검증하지 않았다. [Dune Robinhood Chain](https://dune.com/blockchains/robinhood)
- 공식 API는 query 실행 후 결과를 JSON으로 받거나 `GET /api/v1/execution/{execution_id}/results/csv`로 CSV를 받을 수 있다. Python SDK에도 `run_query_csv`가 있다. 따라서 “Dune 결과를 CSV로 못 뽑아서 SQLite 연구에 쓸 수 없다”는 제한은 현재 공식 API 기준으로 맞지 않는다. CSV는 파일 수동 다운로드만 가능한 것이 아니라 자동 API 응답으로 받을 수 있다. [Get Execution Result in CSV](https://docs.dune.com/api-reference/executions/endpoint/get-execution-result-csv)
- 같은 API에서 결과 columns 선택, filters, `limit`/`offset` pagination이 가능하다. 결과 실행은 90일 후 만료된다. API 결과는 즉시 SQLite에 적재해 장기 보존해야 하며, 대량 결과는 기간/주소/필요 컬럼별로 query를 좁힌다. partial result나 잘린 결과는 complete로 표시하지 않는다. [Dune CSV 결과·pagination 문서](https://docs.dune.com/api-reference/executions/endpoint/get-execution-result-csv)
- Dune query 실행 API는 saved query 또는 SQL execution을 지원한다. query compute에 따라 credits가 소모되며 계정별 비용과 제한은 실제 usage 결과로 측정해야 한다. [Execute Query](https://docs.dune.com/api-reference/executions/endpoint/execute-query)
- 2026-10-06 KST Dune MCP를 직접 확인했다. 현재 계정 표시는 `visitor_fluid_engine`, credits used 0, quota 0이다. 공개 catalog/table 검색, public query metadata와 이미 완료된 public cached result 읽기는 가능하지만 새 SQL query execution은 read-only access로 사용할 수 없다. Dune API의 JSON/CSV 다운로드 문서가 있어도 현재 MCP 권한에서 새 결과를 만들 수 있다는 뜻은 아니다.
- 읽을 수 있던 cached community query 8262126에서 최신 Top 10 rank 1 후보와 일치하는 한 행을 확인했다(표시된 volume 약 $165,775, 247 trades, `last_active` 2026-08-07). 해당 query 실행은 2026년 8월 초여서 최신 Fomo activity가 아니며, community SQL의 주소 행 하나는 Fomo event와 연결된 tx/signature 증거가 아니다. cached query 8106909에는 같은 후보 행이 없었다. 이 내용은 조사 우선순위만 정하며 wallet resolution을 바꾸지 않는다.

#### 이 프로젝트에 적용하는 방식

```text
Fomo API ───────────────────────────┐
                                    ├─> local SQLite ─> research tables/timeline/report
Dune SQL/API ─> JSON or CSV result ─┤
RPC ─> tx/signature-level verification┘
```

- SQLite가 canonical research DB다. Dune query 결과를 Dune 안에만 두거나 임시 CSV 파일에만 의존하지 않는다. collector가 API 결과를 JSON row 또는 CSV row로 읽어서 `dex_solana.trades` 기반 normalized action/source tables에 적재한다. 기존 CSV 산출물은 SQLite에서 재생성하는 review/export 파일로 둔다.
- 적재 시 최소 provenance는 `provider`, `query_id`/SQL version, `execution_id`, query parameters(지갑/기간), requested time range, fetched_at UTC, row count, checksum, completeness/partial status다. Dune raw result의 만료 전에 반복 조회 결과를 로컬 DB로 보존한다.
- SQL은 검증된 wallet과 조사 기간을 조건으로 걸고 필요한 열만 선택한다. 포괄적인 chain-wide dump는 하지 않는다. 대용량이면 address/time window 별로 나누고 API pagination을 사용한다.
- `dex_solana.trades` 결과는 기존 QuickNode 전체 transaction set과 row-for-row로 비교하지 않는다. signature/tx ID의 교집합, Fomo 매칭 signature의 보존, DEX action classification 차이, 조회 가능한 기간을 별도로 비교한다. Transfer, non-DEX, failed transaction에는 원본 RPC 또는 다른 curated table을 계속 보완한다.

#### 아직 확인되지 않은 항목 / 다음 probe

- `DUNE_API_KEY`는 현재 저장소 환경에 설정되지 않았고, Dune live query 또는 API result download를 아직 실행하지 않았다.
- MCP query 실행 권한은 visitor/read-only, credits 0/quota 0으로 확인했다. 직접 Dune API의 별도 account scope/요금제, rate/result limits, `dex_solana.trades` 과거 coverage, Robinhood Chain 주소 query schema와 raw transaction coverage는 확인 전이다.
- 과거 제안에서는 query execution access 확인 후 첫 POC를 verified Solana 주소 1개와 그 지갑의 QuickNode transaction history로 제한하려 했다. Dune DEX rows에서 해당 Fomo matched signatures가 회수되는지, 주소/시간 필터와 SQLite provenance 적재가 동작하는지 확인한다. access가 열리기 전에는 실행하지 않는다.
- JSON과 CSV 양쪽을 모두 상시 보존할 필요는 없다. canonical SQLite 적재 + query provenance를 보장하고, CSV는 사람이 검토하거나 결과를 교환할 때 선택한다.

### X

필수 수집원으로 확정하지 않았다. X user ID 변환, post history, 인증/요금 및 보존 기간을 조사하지 않았으므로 timestamp는 optional/deferred다. Fomo BUY/THESIS와 합치지 않는다.

## 수집 정책과 다음 확인

1. FomoAPI.io 인증과 REST 수집을 확인했고 fixed Top 10 user-scoped history를 SQLite에 보존했다. 약관에 retention duration은 명시되지 않았으며, 200 returned events는 lifetime completeness를 뜻하지 않는다.
2. PooTracker는 403과 오래된 leaderboard 상태로 핵심 source에서 제외한다.
3. shared public RPC/Helius/QuickNode signature probes에서 rank-10 주소 history는 2026-08-24부터 반환됐고, Nodit은 2026-09-25부터만 반환했다. 이후 QuickNode full transaction details를 ranks 1·5·9의 60일 window까지도 확보했다. 주소별 최초 관측 activity는 keypair 생성일과 같지 않다.
4. 현재 bounded analysis는 verified ranks 1·5·9·10의 27 token timeline을 UTC event-time window로 비교한다. Eight exact event-match transactions have USDC quote and protocol-log review. A local transfer screen decoded 956 target-token transfer actions: 342 match gross balance changes and 614 match after applying the same mint's observed 1%/3% Token-2022 inbound fee. Historical mint fee configs were not fetched; build fee-aware inventory lots and inspect post-event exits before any PnL claim.
5. 현재 indexed-history 수집은 BigQuery API/CLI로 진행한다. RZD 한 지갑의 고정 30일 결과와 기존 RPC/Etherscan/Bridge 근거를 먼저 대조한 뒤 범위를 확대한다. Dune은 제외 상태이며 결과 전체 회수와 on-chain history completeness는 별도 기준으로 관리한다.


### Etherscan V2 / CLI — 2026-10-06

- 이번 rank-9 Ethereum tracing pilot은 `etherscan` CLI 1.0.8의 live help와 기존 로컬 인증 정보를 사용했다. 현재 세션에는 Etherscan MCP 도구가 노출되지 않았다. 키를 추출하거나 `.env`에 복사하지 않았다. CLI의 API 데이터 host는 `https://api.etherscan.io/v2/api`이고 `chainid=1`을 모든 호출에 명시했다.
- 사용 endpoint: `account/txlist`, `account/tokentx`, `account/txlistinternal`, `block/getblocknobytime`, `proxy/eth_getTransactionByHash`, `proxy/eth_getTransactionReceipt`, `proxy/eth_getBlockByNumber`, `proxy/eth_getCode`, `contract/getsourcecode`, `nametag/getaddresstag`. 블록 경계는 timestamp 조회로 계산했고 raw value는 정수 문자열로 유지했다. [ERC-20 transfers](https://docs.etherscan.io/api-reference/endpoint/tokentx), [internal transactions](https://docs.etherscan.io/api-reference/endpoint/txlistinternal), [time-to-block lookup](https://docs.etherscan.io/api-reference/endpoint/getblocknobytime)
- 요청 구간은 2026-09-06 07:46:11~2026-10-06 07:46:11 UTC, 블록 25,916,899~26,131,934였다. Seed feed의 일반/토큰/내부 반환 행 수는 각각 0/34/0이며 모두 첫 페이지에서 끝났다. 34개 토큰 행을 33개 성공한 receipt에 대조했다. 이것은 요청 구간의 provider 반환 coverage이며 lifetime history 보증이 아니다. 일부 상대 주소의 100행 첫 페이지는 아직 pagination이 끝나지 않았다.
- 전용 Flow 스킬의 상한인 100 network attempts와 주소당 최대 20페이지를 적용했다. CLI 프로세스는 순차 실행하고 launch 간격 350ms 이상을 지켰으며 rate-limit override나 `--all`을 쓰지 않았다. 각 API 응답은 credential-free fetch log에 즉시 저장하고 SQLite raw layer에도 적재했다. 100회 중 63회가 receipt 조회다. CLI 내부 HTTP 응답 header와 실제 API 비용/잔액은 노출되지 않아 unknown으로 유지한다.
- `nametag/getaddresstag`는 실제 호출에서 `Sorry, it looks like you are trying to access an API Exclusive endpoint. Contact us to upgrade your API plan.`를 반환했다. 이 오류는 해당 endpoint의 플랜 제한이며 다른 endpoint의 실패를 뜻하지 않는다. 검증된 `ContractName`만으로 CEX/bridge/router 라벨을 부여하지 않는다.
- 최신 code 조회가 `0xef0100`과 20-byte 주소로 이루어진 경우 EIP-7702 delegation indicator로 구분한다. 일반 계약 code와 동일하게 취급하지 않고 확인 시점의 위임 상태로 기록한다. 위임 여부나 outer sender 차이만으로 소유 관계를 추론하지 않는다. [EIP-7702 specification](https://eips.ethereum.org/EIPS/eip-7702)
- SQLite 테이블 `evm_flow_cases`는 case JSON과 coverage, `evm_flow_requests`는 요청·raw payload 관계, `evm_flow_movements`는 선택된 성공 receipt의 개별 ERC-20 Transfer log를 보존한다. `(case_key, chain_id, tx_hash, log_index)`가 movement grain이며, 동일 tx 안의 두 log를 하나로 삭제하지 않는다. 합산 graph edge와 개별 movement를 분리하고 native feed는 raw로 보존한다. 결과 및 조사 가설은 case JSON 안에서 조회한다.


### Local Bridge aggregator — 2026-10-06

- 사용자 제공 base URL: `http://127.0.0.1:8080`. 새 API 인증정보는 필요하지 않았다. 실제 `POST /v1/bridge/resolve`에 `{"sourceChain":"eip155:1","sourceTransactionHash":"0x..."}`를 보내 8개 소스 거래 모두 HTTP 200 응답을 받았다. 반환 필드는 `sourceEvidence`, `observations`, `providerIssues`, `verificationIssues`다.
- Observation은 `operationId(provider,value)`, `source`, `providerAssertion(rawStatus,status,observedAt,destinations,assetLegs)`, `provenance(adapterVersion,deploymentId,manifestDigest,retrievedAt)`, `canonicalEvidence`를 제공했다. Leg의 `role`, CAIP-2 `asset.chain`, asset kind/identifier, 정수 문자열 `rawAmount`, `accountAddress`, transaction, `basis=actual|quoted`를 그대로 보존한다. Provider의 `completed`만으로 실제 수취 또는 trader 소유를 확정하지 않는다.
- `POST /v1/bridge/resolve-transaction`은 MCP에서 확인한 실제 입력인 `{"transactionChain":"eip155:1","transactionHash":"0x...","providerHints":["relay"]}`로 1회 호출했다. HTTP 200, `status=resolved`, `role=source`였지만 목표 지갑이 아닌 같은 batch의 다른 사용자 주문이어서 귀속하지 않았다. Source endpoint 응답에는 unrelated Polygon 주문도 있었으며, 총 3개의 반환 observation(고유 다른 사용자 주문 2개)을 excluded provenance로 저장했다.
- MCP transport `http://127.0.0.1:8080/mcp`는 `MCP-Protocol-Version: 2025-11-25`로 initialize 및 tools/list가 성공했다. 서버 이름은 `bridge-api-aggregator`, version은 `mcp-transport.v1`이다. 도구는 `bridge_detect_candidates`, `bridge_resolve_transaction`이다. Detector 문서는 `ROUTING_ONLY` / `CALLER_EVIDENCE_NOT_VERIFIED`를 명시한다. 초기 구버전 protocol 협상은 거부됐고 실제 수집은 REST를 사용했다.
- 소스 provenance는 retained Etherscan successful receipt다. Deposit event topic은 verified RelayDepository ABI의 `RelayErc20Deposit(address,address,uint256,bytes32)`에 해당하며 non-indexed sender/token/amount/id를 원본 data에서 추출했다. 토큰 Transfer locator와 deposit event locator는 별도로 저장했다.
- 목적지 chain은 `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`, mint는 Solana USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`다. 직접 `getTransaction`은 `encoding=jsonParsed`, `commitment=finalized`, `maxSupportedTransactionVersion=0`을 사용했다. Configured Nodit RPC 8회 중 5개는 `result=null`, 3개는 성공 transaction이었다. Public mainnet RPC 6회에서는 6개 성공 transaction이 반환됐다. Null 응답은 실패 transaction의 증거가 아니다.
- 직접 RPC 호출은 총 14회였고 원문 13건을 보존했다. 초기 scratch capture에서 public-RPC duplicate 1건의 파일명이 겹쳐 원문이 덮어써졌다. 해당 최신 목적지 transaction의 성공 Nodit 원문은 남아 있어 주문 연결은 영향을 받지 않았다. 이 원문 누락은 `raw_payloads.source=bridge_capture_gap` metadata로 명시하고 report에서도 표시한다. 추가된 collector는 content-hash 파일명으로 같은 문제가 생기지 않게 저장한다. 현재 raw payload는 1,034건(Bridge API 9 + direct RPC 13 + capture-gap metadata 1 추가)이다.
- 7개의 연결은 소스 token/log/amount/block 일치, 목적지 성공·slot·SPL instruction·token account historical owner·balance delta 일치, 소스 deposit ID와 Relay operation ID 양쪽의 목적지 memo 일치로 확인했다. 수취 EOA는 이미 검증된 RZD Solana 주소 `5MfuqNSawthUL1qdJJTN8DauQvJYSUkuuZuySXuVc6Tz`이고 수취 token account는 `BBqJy34UgMSEGmk3ZwK1knR3Yde6Fk7k72ZhypyeKLHM`이다. Service-side 송금 계정 소유를 trader에게 귀속하지 않는다.
- 목적지 7개 signature 모두 이전 `solana_normalized_actions`에 없고 owner EOA가 transaction account keys에도 없었다. 이 표본에서 token-account owner 기반 조회가 EOA history의 누락을 보완했다. 이전 60일 EOA dataset을 모든 소유 token-account 활동의 complete history로 표현하지 않는다.
- Historical completeness, 서비스 전체 지원 체인, SLA, provider pagination, Bridge 내부 upstream 호출 수 및 실제 비용/잔액은 unknown이다. 이번 호출은 8개의 이미 발견한 source tx에만 한정된다. Latest collector는 최대 source transaction 수를 선검사하며 provider 자동 재시도나 background polling을 추가하지 않았다. Native/refund/quoted legs 및 다른 목적지 체인에서의 직접 receipt 검증은 이번 normalized proof 범위 밖이다.


### BigQuery 공개 온체인 데이터 — 적합성 평가, 2026-10-06

사용자가 제공한 Arbitrum 콘솔 링크를 기준으로 공식 문서, 로그인된 콘솔, 기존 Google Cloud CLI 인증을 확인했다. 현재 `exchange-labs`에서 BigQuery SQL 실행과 JSON 결과 회수가 성공했다. 신규 키는 만들지 않았으며, 인증 토큰은 평가 자료에 넣지 않는다. 아래 내용은 공급원 평가와 소량 교차 검증의 관측 기록이다. 이후 사용자가 API/CLI 방식을 확정했다. 평가 당시 다음 과제였던 30일 Ethereum ERC-20 collector와 SQLite 적재는 이후 완료했다. 실제 실행·대조 기록은 아래 절을 따른다.

| 데이터셋 | 실제 location | 확인한 구조 | 연구 활용 |
|---|---|---|---|
| `bigquery-public-data.goog_blockchain_ethereum_mainnet_us` | `US` | `blocks`, `transactions`, `receipts`, `logs`, `decoded_events`, `token_transfers`, `traces`, 계정 및 주소별 transaction view | 검증 지갑의 토큰 전송·native/internal 흐름, event-token 후보 검색. Ethereum token-transfer grain은 tx + event_index + batch_index다. |
| `bigquery-public-data.goog_blockchain_arbitrum_one_us` | `US` | `blocks`, `transactions`, `receipts`, `logs`, `decoded_events`의 5개 view | 실제 Arbitrum Fomo event나 검증된 bridge leg가 생길 때 사용. 전용 token-transfer/traces 테이블은 이번 목록에 없다. |
| `bigquery-public-data.crypto_solana_mainnet_us` | `us-central1` | `Blocks`, `Transactions`, `Token Transfers`, `Accounts`, `Instructions`, `Tokens` 등 | 공개 커뮤니티 공급원. Transaction의 pre/post token balances에 owner, mint, amount, decimals가 있어 EOA account-key 검색에서 빠진 소유자 활동을 확인할 수 있다. |

Ethereum/Arbitrum 공개 항목은 API metadata상 view다. `numRows=0` 또는 `numBytes=0`은 underlying blockchain의 빈 데이터 증거가 아니다. Ethereum `token_transfers`의 계약 주소 필드는 `address`, raw quantity는 STRING `quantity`, 실제 ERC-20 유형 값은 **`ERC-20`**다. 초기 `ERC20` 필터의 0행은 표기 오류였고 coverage 근거로 사용하지 않는다. Solana `Transactions`와 `Token Transfers`는 일별 `block_timestamp` partition filter를 요구하며, `Transactions`는 signature로 clustered다. `Accounts.owner`는 다른 Solana account의 program owner와 혼동하지 않도록 raw schema 및 해당 account type을 함께 확인해야 한다.

실제 최근 24시간 `blocks` 조회에서 Ethereum 26,133,209 / `2026-10-06T12:03:23Z`, Arbitrum 512,238,910 / `2026-10-06T12:03:31Z`, Solana slot 453,896,633 / `2026-10-06T12:05:55Z`가 반환됐다. 이는 각 block table의 최신성 관측이며 다른 테이블의 동일한 지연, 전체 역사 시작일, gap-free coverage 또는 SLA를 보장하지 않는다.

#### 기존 Bridge 증거와 교차 검증

기존 rank-9 RZD 수령 signature `4jJ9CmfMc4XSZyhwQYfiNt55aeMY8MjUsRsqXZWXc4arN1aEHMeL7i5WegbJ2tyK3x5qXWjPgTQ8CjpfgBboinhN`를 날짜 + signature 조건으로 조회했다. BigQuery는 성공 상태, slot 450,453,169, `2026-09-25T19:57:25Z`, 검증된 Solana wallet의 USDC mint를 반환했다. Pre/post raw balances는 27,449,411 / 50,031,549,747이며 차이는 50,004,100,336, 즉 **50,004.100336 USDC**다. 기존 Bridge report의 direct RPC slot, timestamp, mint, owner와 raw delta에 모두 일치했다. 이 signature는 이전 EOA normalized history에 없었던 7건 중 하나다. 이번에는 1건만 교차 검증했으므로 나머지 6건이나 전체 owner history의 BigQuery coverage를 확정하지 않는다. Bridge 주문 ID와 memo 상관관계는 기존 별도 증거를 유지한다.

#### 실측 조회량과 비용 통제

| 쿼리 | 조회량 | 상태 |
|---|---:|---|
| Ethereum 최신 block | 요금 산정 10 MiB | 소량 실행 완료 |
| Arbitrum 최신 block | 요금 산정 10 MiB | 소량 실행 완료 |
| Ethereum 실제 transfer 유형 1일 집계 | 요금 산정 59 MiB | 소량 실행 완료 |
| Solana 최신 block | 요금 산정 104 MiB | 소량 실행 완료 |
| 기존 Solana bridge signature 1건 | 요금 산정 70 MiB | 소량 실행 완료 |
| RZD Ethereum ERC-20 / USDC 전송 30일 | 약 25.0 GiB 상한 추정 | dry run만 수행 |
| RZD Solana pre/post owner 기준 30일 history | 약 7.145 TiB 상한 추정 | dry run만 수행 |

실행한 검증 job의 실제 처리량 합계는 248,880,239 bytes, `totalBytesBilled` 합계는 265,289,728 bytes(253 MiB)다. `totalBytesBilled`는 요금 계산에 쓰는 데이터량이며 실제 금전 청구액이 아니다. 월 무료 사용량 잔여분과 프로젝트 billing 상태는 확인하지 않았다. 무료 compute 기준은 월 1 TiB이며 공개 데이터셋이라고 모든 SQL 실행이 무료인 것은 아니다. 샌드박스의 자체 table/view/partition 60일 만료는 공개 chain history가 60일만 존재한다는 뜻이 아니다.

Dry run은 예상치다. 실제 실행량은 clustering/pruning, 데이터 추가, cache 등에 따라 달라지므로 실행 시 `maximumBytesBilled`를 반드시 지정한다. 주소 필터나 LIMIT만으로 비용 감소를 가정하지 않는다. 여러 대상 주소는 가능하면 한 기간의 query에 묶어 중복 스캔을 줄인다. 특히 Solana owner만 조건으로 30일 전체 transaction을 검색하는 방식을 기본 collector로 채택하지 않는다. 날짜·signature·검증 token account 및 token 중심의 작은 window부터 검증한다.

#### 저장과 적용 범위

Query results는 CLI/API에서 JSON으로 회수할 수 있고 REST `jobs.getQueryResults`는 pageToken pagination을 제공한다. CSV도 console export에 사용할 수 있지만 nested/repeated field는 flatten해야 한다. 로컬 research collector가 결과를 SQLite로 적재하는 구조는 가능하다. 추후 collector에는 SQL 버전/hash, parameter, dataset, location, job ID, captured_at UTC, totalRows, 모든 page의 회수 여부, actual processed/billed bytes와 latest indexed block을 함께 보존한다. EVM uint256은 STRING으로 유지한다.

체인별 실제 location을 지정해 조회한 뒤 SQLite에서 합치는 방식을 우선한다. Global/cross-region query의 권한·요금·지원 조건은 이번에 검증하지 않았다. Google의 관리 데이터 목록에서 Base/BNB/Robinhood/Monad의 해당 공급원을 확인하지 못했다. 전체 BigQuery에 데이터가 없다는 결론이나 Ethereum 주소 검증으로 다른 chain 활동을 확정하는 결론은 내리지 않는다.

BigQuery는 과거 전송과 특정 token event 후보 발견에 사용한다. Fomo 계정/BUY/SELL/THESIS 시간은 Fomo REST, 거래 성공·swap 의미·중요 원문은 RPC/Etherscan, cross-chain 주문 대응은 Bridge API에서 확인한다. Transfer를 BUY로 분류하거나 funding 관계를 동일인으로 확정하지 않는다. CEX attribution, cost basis, swaps/exit/fees 및 PnL 계산은 별도 증거와 후속 분석이 필요하다. 기존 Dune 실행 경로는 제외 상태다.

이번 metadata, 소량 결과, SQL, job 통계, dry-run 예상치와 bridge 비교는 ignored `data/research/bigquery-evaluation-2026-10-06.json`에 보존했다. SQLite의 기존 Fomo/Flow/Bridge 테이블을 변경하지 않았다.

공식 출처: [지원 데이터셋](https://docs.cloud.google.com/blockchain-analytics/docs/supported-datasets), [체인별 schema](https://docs.cloud.google.com/blockchain-analytics/docs/schema), [Ethereum 예제](https://docs.cloud.google.com/blockchain-analytics/docs/example-ethereum), [비용 추정·상한](https://docs.cloud.google.com/bigquery/docs/best-practices-costs), [sandbox 한도](https://docs.cloud.google.com/bigquery/docs/sandbox), [query result API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults), [CSV/JSON 결과 저장](https://docs.cloud.google.com/bigquery/docs/writing-results), [location](https://docs.cloud.google.com/bigquery/docs/locations). 확인일: 2026-10-06 UTC.

#### 사용자 크레딧·참고 요율 보충 — 2026-10-06

사용자는 약 40만원의 크레딧을 보유하고 비용이 클 때만 알리도록 요청했다. 한 작업 묶음 예상 5만원 이상을 현재 알림 기준으로 가정한다. 사용자 보고 예산이며 실제 billing balance를 조회한 결과는 아니다. [공식 BigQuery 안내](https://cloud.google.com/bigquery)의 온디맨드 시작 요율 $6.25/TiB를 기존 상한 추정에 대입하면 Ethereum 30일 약 $0.153, Solana owner-history 30일 약 $44.65다. 무료 allowance와 크레딧 적용 전 참고 계산이며 실제 단가/요금제/통화 환율은 아직 확인하지 않았다. 큰 처리량이라는 이유만으로 유용한 Solana history 추출을 제외하지 않고, coverage 보완 효과·batch scope·예상 금액을 함께 판단한다. 첫 추출 결과는 보존하고 반복 full scan 비용을 줄인다. 이번 보충에서 새로운 BigQuery 대량 조회나 DB import는 실행하지 않았다.

#### BigQuery API·MCP 인터페이스 확인 — 2026-10-06

공식 REST API와 Python client library(`google-cloud-bigquery`)가 있다. REST `jobs.query`는 SQL 실행, `jobs.insert`는 비동기 job 생성, `jobs.getQueryResults`는 결과 pagination에 사용한다. Dry-run/maximumBytesBilled 및 job provenance를 유지하는 자동 history 수집·SQLite 적재는 API/CLI 경로로 확정했다. 기존 `bq`/`gcloud` CLI는 설치되어 있고 앞선 실제 SQL/JSON 회수 검증에 사용됐다. Python SDK 설치 및 SDK의 ADC 호출은 이번 turn에서 검증하지 않았다.

Google 공식 remote MCP endpoint는 `https://bigquery.googleapis.com/mcp`다. 도구 목록에는 dataset/table 목록·정보, `execute_sql_readonly`, `execute_sql`, `get_query_results`, `get_job`, `cancel_job`가 있다. OAuth 2.0/IAM 인증이며 `mcp.tools.call` 등 권한이 필요하다. 일반 BigQuery CLI 성공만으로 remote MCP 호출 권한까지 검증된 것은 아니다. 공식 안내에 기본 3분 처리 제한과 3,000행 결과 제한이 적혀 있으며, reference에는 결과 pagination 도구도 있다. 대량 회수 조건은 연결 후 실제 schema/응답으로 다시 확인한다.

현재 Codex 설정과 이 세션에서 노출된 도구에는 BigQuery MCP 연결이 없다. 이 확인에서는 MCP 설정 변경·설치·권한 부여 또는 authenticated MCP 호출을 수행하지 않았다. 별도의 공식 local MCP Toolbox for Databases도 ADC 기반 연결 옵션으로 제공된다. 현재 수집 경로는 인증된 API/CLI다. MCP는 필요할 때 schema 탐색·임시 분석에 사용할 수 있는 선택지로 유지한다.

출처: [REST jobs](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs), [client libraries](https://docs.cloud.google.com/bigquery/docs/reference/libraries), [공식 remote MCP reference](https://docs.cloud.google.com/bigquery/docs/reference/mcp), [MCP 인증·제한](https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp), [local MCP Toolbox](https://docs.cloud.google.com/bigquery/docs/pre-built-tools-with-mcp-toolbox). 확인일 2026-10-06 UTC.


### BigQuery Ethereum ERC-20 실제 수집 — 2026-10-06

`src/fomo_research/bigquery.py`가 기존 Google Cloud 인증과 `bq` CLI를 사용했다. Dataset은 `bigquery-public-data.goog_blockchain_ethereum_mainnet_us` / `token_transfers`, location은 `US`, query project는 `exchange-labs`다. Wallet 및 시작·끝 TIMESTAMP는 query parameter로 전달했고 실제 enum `ERC-20`, `removed=false/null`, 시작 포함·끝 제외 조건을 적용했다. Outer transaction sender에 의존하지 않는다.

Job `fomo_eth_2d414f21c65e8f562d08f27a69fd1139e33e0f38f8b6f23497647454ed8e6357`에서 totalRows 34를 destination result table의 `numRows`로 확인하고 `bq head --job`의 start_row/max_rows로 25+9행을 회수했다. 결과 합계와 event identity 중복 여부를 확인한 뒤 완료 상태로 저장했다. SQL/version/hash, scope/parameter, dry-run/job/table metadata, raw stdout 및 개별 result page를 보존했다. Bq CLI는 integer와 BOOLEAN 셀을 문자열로 출력하며 이번 `removed`는 `"false"`, quantity는 정확한 문자열이었다. [bq CLI reference](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference)

Retained successful receipts 33개의 ERC-20 log 34개와 모든 field 및 event_index/log_index가 일치했다. Bridge source deposit 8개도 대응하며 추가·누락·상이한 baseline 행은 없다. USDC 유사 이름의 다른 계약 2행은 canonical USDC와 구분한다. 수집 범위는 이 기간·이 지갑의 indexed ERC-20 transfer rows다. Native funding, NFT, 실패 거래, swap semantics/quote/PnL 또는 lifetime completeness는 이 query로 확인하지 않았다.

예상량 35,244,881,963 bytes에 40 GiB cap을 적용했다. 실제 processed 35,099,642,244 bytes / billed 35,100,033,024 bytes, cache hit false다. Billed bytes는 금액 청구서가 아니다. Reference $6.25/TiB 계산은 약 $0.20이고 실제 단가·무료 allowance·크레딧 적용은 별도다. [비용 상한](https://docs.cloud.google.com/bigquery/docs/best-practices-costs), [Google Cloud pricing](https://cloud.google.com/bigquery)

SQLite에 collection 1행, result page 2행, transfer 34행과 raw capture 6건을 저장했다. Full capture의 재파싱은 새 SQL 없이 가능하다. Manifest/content-hash captures와 report는 ignored `data/raw/bigquery/2d414f21c65e8f562d08f27a69fd1139e33e0f38f8b6f23497647454ed8e6357/`에 있고 같은 report는 `bigquery_collections.report_json`에 있다. 전체 history coverage는 unknown으로 명시한다.

### Solana owner BigQuery + full RPC 실측 — 2026-10-06 UTC

- Dataset `bigquery-public-data.crypto_solana_mainnet_us.Transactions`, location `us-central1`, project `exchange-labs`. Fixed rank 9 RZD wallet와 동일 30일 구간이다. Historical `pre_token_balances.owner` / `post_token_balances.owner`를 사용한다. `Accounts.owner`는 program owner이므로 wallet owner 조건으로 쓰지 않았다.
- Query는 known receipt full fields → owner signature discovery → signature-set owner balances 단계다. Raw amount는 `CAST(amount AS STRING)`으로 보존하고 정수/decimals/UTC/identity 및 총 결과 행 수를 검증한다. Owner balances에는 signer/fee/native/instruction 정보가 없으며 unknown을 false/zero로 채우지 않는다. Detailed accounts/native/log 일괄안은 dry run 26,998,031,561,814 bytes에서 실행하지 않았다.
- 결과는 7행/2페이지, 11,763행/12페이지, 11,763행/24페이지다. Billed bytes는 각각 102,532,907,008 / 3,673,761,513,472 / 8,291,702,800,384, cap은 128GiB / 4TiB / 8TiB였다. 원본 CLI 67개를 SQLite에 보존했다. 큰 예상량을 알린 뒤 진행했으며 total 12,067,997,220,864 billed bytes의 시작단가 참고 계산은 $68.60다. 실제 invoice/free allowance/credits/tax/FX는 확인하지 않았다. 초기 evaluation 및 Ethereum까지 이 스레드의 기록된 billed bytes 합은 12,103,362,543,616(참고 $68.80)이며 프로젝트 전체 사용량을 뜻하지 않는다. [Cost controls](https://docs.cloud.google.com/bigquery/docs/best-practices-costs), [Pricing](https://cloud.google.com/bigquery)
- Known 7 receipts의 상태·slot·시각·SPL mint·owner·raw delta/token-account가 retained RPC와 일치했다. BigQuery의 해당 7개 `log_messages`는 빈 문자열이어서 memo를 BQ가 다시 검증한 것으로 기록하지 않았다. Deposit ID + operation ID memo와 실제 transfer instruction은 기존 직접 RPC proof를 유지한다.
- Nodit point RPC는 오래된 321개 요청에 null을 반환했다. 최신 3개 연구 거래는 조회됐다. 무결과 원문은 삭제하지 않았고 후속 owner full pages로 보완했다. 초기 method-unavailable 요청 raw ID 1432는 configured Nodit을 사용한 실패 probe로, collector의 intended QuickNode label과 별개다. 유효 page나 비교 근거에서 제외했다. 현재 bulk collector는 새 호출 때 QuickNode host를 먼저 확인한다.
- QuickNode official API의 `tokenAccounts=balanceChanged`, blockTime gte/lt, full/jsonParsed, version 1과 cursor를 사용했다. 13호출(마지막 빈 page 포함) / 11,580 unique RPC signatures; owner BQ 11,579개와 같은 signature/slot/time/success/net owner token deltas였다. BQ-only 184개는 모두 net token delta 0(성공 121/실패 63)이며 실제 nonzero 11,575개는 전부 RPC와 일치한다. RPC-only 1개도 원문으로 보존했다. 끝 cursor는 null로 result pagination 종료를 확인했다. 13×120=1,560 QuickNode credits는 문서 단가 추정이며 실제 잔액은 unknown이다. [QuickNode method](https://www.quicknode.com/docs/solana/getTransactionsForAddress)
- 원본 amount/state 대조와 SWAP 의미 해석을 분리한다. `SwapTob`, `Swap2WithTransferHook`, `SwapEvent`처럼 붙는 이름을 기존 단어 검색이 놓쳤다. V3에서 성공·wallet signer·swap instruction/event log·opposing balances를 함께 요구한다. RZD 기존 358개가 SWAP으로 교정됐고 다른 verified 3명도 raw source만 재분류했다. Known bridge 7개는 별도의 direct SPL/order proof로 TRANSFER다. 이는 일반 DEX decoder나 PnL 완성이 아니다.
- SQLite source-role rows 23,533개는 11,763 unique signatures의 다른 projection을 포함한다. Normalized wallet/signature는 한 번만 저장한다. RZD 12,600행 및 18개 event windows; global actions 44,382, deltas 62,885, timeline 27행이다. Detailed results are in [owner review](rank9-solana-owner-review.md).
- 이후 Solana owner 수집은 full owner RPC를 우선 재사용한다. BigQuery는 owner metadata 누락/closed account·알려진 gap·기존 자금 후보와 token/time subset을 좁혀 대조하며, 새 scope의 dry run으로 비용을 결정한다. Same owner balances라도 native-only/owner metadata gaps/lifetime history completeness는 증명하지 않는다.


## Arkham CEX 연결 조사 — 2026-10-07 KST

**추가 관측:** 같은 2-hop 안에서 `0x6a2…6ee1`로 나간 2026-10-06 02:51:47/02:53:23 UTC의 5,000.31502/8,000.40002 USDC가 Arkham 상세에 표시됐다. CEX 라벨·소유권은 미확인이며 receipt 검증이 다음 첫 단계다. 고정 cutoff 이후 거래는 15:00:11 UTC의 새 본지갑 공급 1건이다. 원문 11개와 report 두 revision을 SQLite raw layer에 보존했으며 원장 normalized 행은 추가하지 않았다.


Arkham은 현재 연구에서 브라우저를 통한 주소/service/CEX 라벨 보조 확인에 사용했다. API credential이나 신규 수집기를 추가하지 않았다. 로그인된 화면에서 공급 지갑 2/2 페이지의 표시 거래 20행, 정확한 tx 상세, 본지갑·Relay solver·Robinhood deposit 라벨을 보존했다. 로그인 전 보이는 zero-prefix demo tx 행은 증거에서 제외했다. 전체 원장 coverage는 unknown이며 화면의 cutoff 이후 행은 고정 구간 normalized ledger에 추가하지 않았다.

[입금 거래 상세](https://arkm.com/explorer/tx/0x4565d12dec31248b20e1242006a5eab2e02ba75d46a382fa519f4e7c8d2055fa)의 Ethereum USDC 5,000.780122, 주소, 2026-09-15 04:01:47 UTC와 성공 상태는 retained Etherscan receipt **984**, Transfer log **217**, raw **5000780122**에 일치했다. 전송 사실은 receipt로, [Robinhood Deposit 역할](https://arkm.com/explorer/address/0x056f02966a8ec618df3da0ea7cd9c7cc3f26fa16)은 Arkham assertion으로 구분한다. 고객 신원·전용 입금 주소 여부·실제 fiat cashout은 unknown이다.

[공급 지갑](https://arkm.com/explorer/address/0xe7af3221ad9b407055e9105aba5a783443d2c3c5)의 `@riziderxbt?`에는 **Lower confidence prediction by an AI model**이 표시된다. [상류 주소](https://arkm.com/explorer/address/0xf70da97812cb96acdf810712aa562db8dfa3dbef)는 **Relay.link: Bridge Solver**다. 이러한 provider 라벨은 기존 wallet resolution이나 소유권의 확정 근거로 사용하지 않았다. Fomo 기존 handle과 Arkham alias의 차이도 보존했다. 자세한 source/receipt/관측 시각과 다음 범위는 [review](rank9-arkham-cex-review.md), ignored JSON 및 canonical SQLite raw layer를 따른다. 신규 BigQuery/RPC 호출은 0개다.


## Relay/funder continuation — checked 2026-10-07 KST

Local `POST http://127.0.0.1:8080/v1/bridge/resolve-transaction` accepts `transactionChain`, `transactionHash`, and `providerHints:["relay"]`. Seven retained Ethereum Solver→funder transactions resolved to the verified RZD Solana owner after three upstream-rate-limit 503s were retried sequentially. Independent saved QuickNode full transactions (raw885) and Etherscan receipt logs prove both legs; cross-chain correspondence remains provider assertion. One new Ethereum native deposit→Solana route also matches source deposit ID and operation ID in direct destination memo. Raw API canonical evidence, provider assertion and direct configured RPC responses are kept separately.

Configured Nodit Ethereum RPC returned successful receipts, blocks, transaction and historical decimals() calls for selected funder/6a2 transfers. A 1,000-block USDC getLogs range returned JSON-RPC -32604 current-plan block-range failure for both wallets; this is incomplete coverage, not empty history. Configured Nodit Solana RPC returned the actual native recipient transaction plus a 25-signature head page crossing that receipt. All 13 returned post-receipt transactions were recovered, including two initial429s with one later retry each. These read-only calls do not establish lifetime history completeness.

Arkham logged-in UI supplied exact transaction discovery links and chain icons for 6a2; only page1/59 TRANSFERS and page1/27 OUTFLOW was read. Snapshot texts, capture file times and screenshot hash are retained. Robinhood-chain4663 source lookup returned HTTP422 source_unsupported_chain. Destination lookup for another 8.027063514-SOL credit returned HTTP200 unresolved. Both remain gaps. A chain4663 bridge is different from the earlier chain1 Robinhood CEX Deposit label.

Fomo rank9 REST checkpoint resumed: 3 new events,1 page hasMore=false,125 credits,latest observed balance246125. New calls: STOCKER THESIS14:37:30 UTC and STONK BUY15:02:50/15:02:55 UTC on October6. New KNOTS transfer mint differs from STONK; no retained rank9 same-mint call was found. No new BigQuery query was run. All48 capture records and review raw1508 are in SQLite. See [trace review](rank9-wallet-trace.md) for exact amount/time/proof and [offline importer](../src/fomo_research/wallet_trace.py).

## RZD CEX/pre-buy source checks — 2026-10-07 KST

The latest slice uses authenticated BigQuery CLI for three bounded Ethereum wallet queries (token transfer365 / top-level transaction62 / native call trace27 rows, fully retrieved, billed691,803,258,880 bytes). Critical transfer and buy legs are checked against configured Nodit Ethereum RPC. Reusing the user's authorized Nodit key on its documented BNB endpoint returned BSC chain56 and all9 observed CEX-withdrawal transaction/receipt/header triples. Official BNB public RPC returned null for four historical hashes, which is retained as an endpoint result rather than transaction absence. Robinhood Chain official public RPC returned HTTP403; its2 observed CEX withdrawals stay Arkham-only. Browser snapshots retain exact CEX labels and transfer directions. Arkham's exchange-usage USD summary is not fully reconciled to this individual subset.

STOCKER historical balanceOf calls at three named blocks and exact receipt quote/token/gas legs supplement Fomo event IDs/timestamps. A fresh27,001.6471 USDC bridge's source Deposit ID and operation ID both occur in the destination memo; Nodit Solana owner delta agrees. More detail and evidence links: [rank9-cex-prebuy.md](rank9-cex-prebuy.md).


## 두 달 연우 범위에서 재확인 — 2026-10-07

- [Nodit BNB Get Transactions By Account](https://developer.nodit.io/en/api/bnb/web3-data-api/gettransactionsbyaccount/)의 `fromDate/toDate`, `relation`, page/rpp/withCount를 사용했다. Native value는 거래의 최상위 값이므로 ERC-4337·internal native 전체가 아니다. 응답 range와 count를 보존했다. 데이터 인덱스 성공과 직접 Node receipt 검증은 별개다.
- `token/getTokenTransfersByAccounts`는 BNB/Ethereum에서 saved credential로 HTTP200을 반환했다. account·token 계약·relation·시간 필터와 페이지 원문을 보존했다. 공식 [다중 계정 Token Transfer 스키마](https://developer.nodit.io/en/api/chiliz/web3-data-api/gettokentransfersbyaccounts/)와 실제 반환값을 대조했다. 한 요청의 accountAddresses는10개 이하로 제한했다. CZ 초기 partial과 inclusive time partition의 합집합 count14,668이 맞았으나 전체 토큰시장 coverage는 unknown이다.
- 브라우저에서 [Relay Depository](https://etherscan.io/address/0x4cd00e387622c35bddb9b4c962c136462338bc31), [Mayan Forwarder](https://bscscan.com/address/0x337685fdab40d39bd02028545a4ffa7d287cc3e2) 라벨을 읽었다. 탐색기 라벨은 provider assertion이다. Public reader의403은 browser fallback으로 보완했다. C67 주소에는 별도 거래소 소유 라벨을 확인하지 못했다.
- `fomo.family/profile/yeon__`는 현재 브라우저 세션에서 Login 버튼이 있는 홈페이지로 이동했다. REST since8/7의 hasMore=false도 두 달 CALL 전체 확보로 해석하지 않았다. 별도 reader가 선택한 feature-gate SDK JSON은 프로필 데이터가 아니어서 제외했다.
- 기존 로컬 Bridge API에5개 신규 source tx를 조회했다. Relay3개는 source/account/token/raw quantity가 맞는 operation과 known Solana output 주소를 반환했고, Mayan2개는 source evidence만 반환했다. 도구 canonical destination instruction과 독립 historical owner/delta proof를 구별한다. 원문과 요약은 최신 review raw2014에 보존했다.
- 조회 횟수: Fomo2/250credits, Nodit Data196(재시도 포함), 직접RPC30, Bridge5, BigQuery0. Node의 과거 BNB balance 두 호출은 metadata-not-found, CZ 공급/실행 주소의 token0/token1 두 호출은 revert였다. Complete checkpoint로 승격하거나 반복 range 요청하지 않았다. Nodit 청구액·잔액은 unknown이다.

한글 결과와 정확한 tx/수량/미확인 사항은 [두 달 추적 보고서](two-month-review.md), canonical DB 상태는 `research_two_month_v1`을 따른다.


### 2026-10-09 과거 alerts cursor 계약 보완

공식 OpenAPI raw3244: `/v2/alerts`의 `before`에는 이전 `oldestCursor` opaque 값을 넣어 strictly older 페이지를 조회한다. `cursor`/`nextCursor`는 strictly newer 증분이다. ISO before는 raw3243HTTP400; 교정 raw3245는HTTP200이나 source=memory/available=false로 해당 과거 페이지를 제공하지 않았다. 이를0건·history완료로 해석하지 않는다. 기존 source checkpoint를 자동 재작성하지 않는다.
