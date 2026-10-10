# RZD Solana owner 수집·THESIS 대조

작성일: 2026-10-06 UTC. 이번 자료는 고정된 Top 10의 rank 9 **RZD (@RZDxbt)** 한 명에 대한 파일럿이다. Canonical DB는 `data/research/fomo.sqlite3`; raw data와 DB는 Git에서 제외한다.

## 범위와 완료한 작업

- Snapshot: `2026-10-05T16:04:43.128Z`, Fomo user `779bceab-5c5a-5cf2-b76c-193ff7beed0e`.
- 이미 이벤트로 검증된 Solana wallet: `5MfuqNSawthUL1qdJJTN8DauQvJYSUkuuZuySXuVc6Tz`.
- UTC query window: **2026-09-06 07:46:11 포함 ~ 2026-10-06 07:46:11 제외**. 최신 분석일로 자동 연장하지 않았다.
- 기존 Ethereum→Relay→Solana USDC 수령 7건, 합계 **213,983.299662 USDC**를 BigQuery에서 다시 대조했다. 성공/slot/time/mint/owner/raw delta와 token account가 모두 일치했다. Deposit/order memo와 실제 SPL transfer proof는 기존 직접 RPC 원문을 유지한다. BQ control sample 7개의 로그가 비어 있어 BQ가 memo를 재확인한 것으로 기록하지 않는다.
- Historical token owner query 11,763 signatures를 완전히 회수했다. 실제 token 잔액 변동 11,575건은 모두 full RPC와 일치했다.
- QuickNode `tokenAccounts=balanceChanged`로 full history를 13페이지/11,580 unique signatures 회수했다. 11,579개가 BQ owner 결과와 같은 signature/slot/time/success/token delta다. BQ-only 184개는 모두 net token delta 0(성공121/실패63), RPC-only 1개는 별도 raw evidence다.
- 기존 EOA history에 없던 **11,000개 활동**을 합쳐 RZD는 12,600개 wallet/signature actions가 됐다. 새 11,000개는 TRANSFER222/UNKNOWN10,778이며 신규 SWAP 발견은 0개다. 소액 USDC credits가 큰 비중을 차지하므로 이를 모두 매수 건수로 읽으면 안 된다.
- 기존 분류에서 `SwapTob`/`Swap2WithTransferHook`/`SwapEvent`를 놓친 RZD 358개 label(TRANSFER315/UNKNOWN43)을 실제 swap log·signer·opposing balances로 교정했다. V3 최종 RZD는 **SWAP1,144 / TRANSFER318 / UNKNOWN11,138**이다. Known bridge 7개는 direct SPL/order proof로 TRANSFER로 연결했다.
- Fomo Solana BUY2/SELL11/THESIS5, 총18개 이벤트에 별도 24시간 전후 window와 원천 timestamp/signature evidence를 SQLite에 저장했다.

## 같은 지갑의 BUY/THESIS 대조

모든 시간은 UTC. 매매 수는 고정 30일 구간 안의 provisional transaction-level SWAP이며 원래 60일 EOA history와 구분한다.

| Token | 30일 BUY / SELL | 관측된 시점과 해석 |
|---|---:|---|
| SAPLING | 2 / 1 | Fomo BUY `10-03 17:15:45` → on-chain BUY `17:15:46` → THESIS `17:16:15`. 매수는 BUY 알림 **1초 뒤**, THESIS **29초 전**이다. First SELL `18:01:36`. |
| HAMSTER | 7 / 2 | 10-04 첫 매수 `01:12:45`, 마지막 매수 `04:13:48`; 두 매도 `15:48:09`, `15:48:56`; 첫 THESIS `17:15:20`. THESIS 이전24h에 **7회 매수와 2회 매도**가 관측된다. 가장 최근 매수는 **13시간1분32초 전**이다. 이전 TRANSFER-only 결론은 V3에서 교정했다. |
| STONK | 14 / 92 | 조회 구간 첫 BUY `09-16 02:14:41`, 첫 THESIS `10-03 21:31:40`. 해당 THESIS 직전24h에 SWAP BUY는 없고 이후24h에 SELL10개가 관측된다. 더 이른 매수/기존 재고가 있으므로 no pre-buy나 원가0으로 해석하지 않는다. |
| ZCAT | 16 / 5 | 조회 구간 첫 BUY `09-25 19:57:40`; 기존 bridge USDC credit `19:57:25`보다 **15초 뒤**다. 두 시점의 순서는 확인됐지만 동일한 bridge 자금만 쓰였다고 귀속하지 않는다. 수집된 Fomo event는 SELL이고 이 토큰의 BUY/THESIS event는 없다. |

HAMSTER 매수 시점은 같은 verified main wallet의 거래다. 별도 뒷지갑을 찾았다는 결론은 아니다. BQ balance rows와 RPC signer·swap 로그를 함께 사용한 거래 판정이며 quote/fee의 완전한 경제적 귀속까지 끝낸 것은 아니다. 네 mint와 event별 서명·원문 FK는 JSON report/SQLite에 있다.

STONK `10-06 00:24:20` THESIS와 HAMSTER `10-05 15:18:25` 두 번째 THESIS는 이후24h가 frozen end를 넘어가므로 후반 window가 incomplete다. STONK 첫 THESIS 주변 미분류 owner movements도 남기며 absence of SWAP BUY를 모든 acquisition 부재로 확대하지 않는다. X 시점은 아직 없다.

## 조회량과 비용

| BQ role | rows / pages | 최대 billed bytes | 실제 billed bytes |
|---|---:|---:|---:|
| known_receipts | 7 / 2 | 137,438,953,472 (128GiB) | 102,532,907,008 |
| owner_discovery | 11,763 / 12 | 4,398,046,511,104 (4TiB) | 3,673,761,513,472 |
| owner_details (owner balances) | 11,763 / 24 | 8,796,093,022,208 (8TiB) | 8,291,702,800,384 |

실제 합계 **12,067,997,220,864 bytes ≈10.976TiB**. 시작 참고 단가 $6.25/TiB를 적용하면 **$68.60**, 무료 사용량/크레딧/세금/지역별 단가 적용 전 계산이다. 사용자에게 큰 비용을 알릴 때 사용한 달러당2천원 가정에서는 약 **13.7만원**이며 실제 원화 청구액은 아니다. 크레딧 잔액을 확정하지 않는다. 초기 평가/Ethereum까지 이 스레드가 기록한 합계는 12,103,362,543,616 bytes(참고$68.80)다. 더 큰 accounts/native/log full-detail query의 24.554TiB dry-run은 실행하지 않았다. [Google Cloud pricing](https://cloud.google.com/bigquery)

QuickNode full owner page는 마지막 빈 페이지 포함 13호출, 공식 문서의 호출당120 credits로 **1,560 credits 추정**이다. Actual balance는 unknown이다. Nodit에서는 오래된 point requests321건이 null이었다. 이 시도와 최신 성공3건, method-unavailable1건은 원본으로 보존하고, 대량 개별 조회는 full page 경로로 전환했다. Credential URL은 저장·출력하지 않았고 `.env`의 Nodit 설정도 유지했다. [QuickNode method](https://www.quicknode.com/docs/solana/getTransactionsForAddress)

## 보존 위치와 다시 계산하기

- SQL/job/parameters/caps/pages: `data/raw/bigquery-solana/<collection_key>/manifest.json` 및 content-hash `captures/`와 `report.json`.
- Canonical source role table rows23,533는 signature overlap을 포함하며 unique11,763이다. Source layer와 normalized actions의 숫자는 별개다.
- RPC page13 / RPC comparisons11,579 / Fomo event windows18 / analysis1은 각각 SQLite의 관련 테이블에 있다. 원본과 대조는 source FK로 연결한다.
- Review exports: `data/research/rank9-solana-owner-rpc.json`, `rank9-solana-owner-analysis.json`; normalized CSV는 SQLite export다.
- 전체 canonical raw1,445, normalized actions44,382, token deltas62,885, trader-token timeline27이다. 다른 검증 trader3명은 원본만 V3 재분류했고 새 네트워크 history를 추가 수집하지 않았다.

```sh
PYTHONPATH=src python3 -m fomo_research.bigquery_solana --import-capture data/raw/bigquery-solana/d2b9bf914764b343c18eb8a2b971235850631b77d2252320c5882194f4d540ba
PYTHONPATH=src python3 -m fomo_research.solana_owner_rpc
PYTHONPATH=src python3 -m fomo_research.owner_analysis
```

Complete capture의 import 및 analysis는 cloud query를 반복하지 않는다. Completed owner RPC command도 saved cursor/pages를 재사용한다. New/partial owner RPC collection에만 승인된 QuickNode endpoint를 transient `SOLANA_RPC_URL`로 공급한다. [Schema](schema.md), [current implementation plan](implementation-plan.md).

## 아직 남은 연구와 다음 범위

1. 기존 Ethereum funder 후보의 같은 EVM token에 대해 Fomo BUY/THESIS 전후 acquisition/exit 후보를 조회한다. 현재 최대2-hop과 ownership unknown을 유지하고 실제 swap/quote를 대조한다.
2. HAMSTER 등 선행매수가 관측된 main wallet의 quote·router fees·이전 재고·이후 exits를 검증해 lot/inventory를 구성한다. Token-2022 fee 및 transfer basis, 네트워크 fee payer를 trader 비용과 구분한다.
3. Solana의 추가 verified wallet은 token-account full pages를 우선 확보한다. BQ는 owner/known gaps 및 작은 token/time subset의 교차 검증에 쓰며 매번 새 예상량을 확인한다.

Transfer/funding edge는 동일인이나 뒷지갑 소유권을 증명하지 않는다. 8번째 10,000.55003-USDC Relay deposit은 아직 unresolved다. CEX attribution, 뒷지갑, 경제적 realized/unrealized PnL은 이번 완료 범위에 포함되지 않는다. Complete query retrieval은 native-only·historical owner metadata·provider indexing 및 lifetime coverage를 보장하지 않는다.
