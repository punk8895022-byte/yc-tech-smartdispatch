# YC Tech Match × TBM 競品研究與進駐決策（2026-11-02 v1.0）

**目的**：在零新增付費 API、不註冊／付費／投標的前提下，盤點台灣商業媒合平台 TBM 的會員權限、公開案源、營收機制；為既有 YC Tech Match/Media Commerce/Business OS 提供可查證的產品切片，而非再做新平台。

**狀態**：`PUBLIC_RESEARCH_PASS_SCOPED / TBM_PAID_JOIN_HOLD / YC_TECH_MATCH_G2_PARTIAL / OWNER_GATE_CLOSED`。
本檔只作公開資訊和隔離原型研究；不得作為用戶身份、授權、商業可用、已成交或支付證明。

## 1. 免費／付費機制與查核缺口

| 面向 | 2026-11-02 公開資料結論 | 仍須查核 |
| --- | --- | --- |
| 會員 | 註冊免費；一般會員可搜尋、收藏、詢價等 | 登入後完整流程未驗 |
| 一般會員投標 | 不提供免費投標次數，需要購買額度 | 最新投標單價、退費、到期 |
| 廠商權限 | 品牌服務展示需選購權限；購買功能後每月投標3次／發包3次的公開FAQ說法 | 正式書面價目、權限續費、取消 |
| 行銷工具 | CRM、型錄/QR、曝光加購是可能的付費模組 | 實際價格、效果與獲客率 |
| 金流 | 平台公開說明不保管工程交易款，也不收交易手續費 | 真實案例交易安全與爭議解決機制 |
| 費用文字衝突 | 2026-05 宣傳寫免費品牌頁；FAQ 描述品牌頁須開權限 | 以當日書面報價與合同為準 |

主要來源：
- https://www.taiwanbm.com.tw/faq/list-6
- https://www.taiwanbm.com.tw/faq/list-6?page=2
- https://www.taiwanbm.com.tw/faq/list-7?cid=7
- https://www.taiwanbm.com.tw/faq/list-7?cid=7&page=2
- https://www.taiwanbm.com.tw/service
- https://taiwanbm.com.tw/news/view-4
- https://taiwanbm.com.tw/terms/3-%E6%9C%83%E5%93%A1%E6%A2%9D%E6%AC%BE

## 2. 案源品質（有限公開抽樣，絕非全站統計）

公開首頁示例包含 2026-08-10 在地店家合作、2026-07-24 行政秘書、2026-07-15 短影音剪輯、2026-06-12 團購、2026-05-18 印刷及寵物用品廠商。當時未能核實最新30日仍開放的台南 CCTV／Wi-Fi／NAS 工程商機。部分首頁卡片保留占位內容、頁面曾出現「此為校稿頁面」。

不能將「首頁未見合適案」誤寫成「全站零案件」；也不能將刊登案件當作已確認可回覆或能成交。FAQ 說發包內容有違規審核，但不保證需求真偽、可行性；廠商驗證標章不等於履約保證。

官方首頁：https://www.taiwanbm.com.tw/

**進駐 Gate**：J0 公開研究通過；J1 書面價格/授權 HOLD；J2 有效本地工程商機樣本 HOLD；J3 投標成本、工時、成交率、實際毛利與其他平台比較 HOLD；J4 Owner 註冊、投標、付款核准 CLOSED。保持不付費。

## 3. 商業模式與小雲差異化

TBM 可見的商業機制為：廠商功能權限、投標/發包額度、CRM、型錄/QR、廣告曝光；其實際營收占比、成交量與網路效應未有可追溯公開證據，不推估營收。

小雲**不重建 TBM**。優先借鏡：
1. P0 專業需求表：地區、CCTV 設備數量、現場條件、線路、施工時間、保固與驗收項目；避免空泛需求。
2. P0 案件證據卡：原始來源、刊登/查核日期、地區、案主有效性、預算、是否仍開放、風險與 UNKNOWN；不得憑空補欄位。
3. P0 結構化報價比較：設備／施工／保固／排除範圍；先合成數據與審查模式。
4. P1 工程師服務區域、技能資格與有效期限查核；未核准不可顯示「認證」。
5. P1 詢價→報價→簽約→工單→驗收→保固 CRM；正式資料只經 Business OS canonical domain，不得以測試 SQLite 取代。

現有規格：
- Drive Asset OS/YC Tech Match 主 PRD：https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit
- Drive Business OS：https://docs.google.com/document/d/1otVSuymPm7JBoJsSZSvBBK9b0jo6LsREL3zbBQ8h838/edit
- 本 repo Draft PR #1：https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1
- 展示 Draft PR #12：https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/12
- G2 來源契約：../YC_TECH_MATCH_G2_SOURCE_AND_SCHEMA_GATE_2026-11-01_v0.1_RESEARCH_ONLY.md

## 4. 2026-11-02 CCTV 隔離政策 Gate

本地範圍限定的 TDD／synthetic policy smoke 測試，沿用 repo 既有 `marketplace_contract.py` 與 `g2_projection.py`（兩份 Git Blob SHA1 比對一致）。

- 建立虛構台南 CCTV 4 支攝影機需求的案件描述和合成識別碼。
- DRAFT/未同意/未審核不可媒合；APPROVED 只篩出符合技能/台南/資格/Owner Gate 的合成工程商。
- `staging_to_review_projection` 僅回傳 `REVIEW_ONLY`、`executable=false`；即使所有「已驗證」旗標被傳入，`assert_live_sync_enabled` 仍拒絕真正 Business OS 同步。
- 合成報價為**測試敘事資料**，不是後端寫入或真實價格承諾；未合約/Owner 核准禁止收服務費，未核實發票/銀行對帳禁止標記結清，未取得完整權利不可公開實績。
- NAS、台南以外地區、未審核、缺同意證據均 fail-closed。
- 測試命令：在 `pocs/cloudlink-staging-api` 執行 `python -m unittest -v tests/test_tbm_cctv_policy.py`（路徑/匯入依專案 checkout 調整）；新增驗證僅限此 policy slice。

**本地證據**：2026-11-02，在隔離工作目錄 `python -m unittest discover -v -p 'test_*.py'` 回傳 2 tests / OK（0 failures），不是 GitHub Actions CI、真實 API HTTP、正式 IAM/工單/履約/付款 E2E。

**阻塞**：正式 Business OS Identity/Tenant/RBAC、真實 consent/evidence 驗證、工程師資格、WorkOrder/Acceptance/Finance/Audit runtime、原 React E2E、真實買家/Owner UAT 都未通過。下一步應在經核准的隔離 Runtime 執行與既有 FastAPI/SQLite 一致的 CCTV HTTP 全流程，另以真正 schema 增補工單/驗收後才討論 G3。

## 5. 安全、Owner Gate、歷史

不註冊 TBM、不付費、不投標、不連正式客戶、不部署、不執行付費 API、不變更正式 LINE/AI OS/資料庫/三台主機；不得建立第二個 canonical DB。任何對外發包／認證／收費／上架均需 Owner 事先核准。此檔僅追加到既有 Draft 專案，保留原分支與歷史，不宣稱 production PASS。

**版本紀錄**：2026-11-02 v1.0 首版 TBM 競品研究與 CCTV policy gate；後續變更需記錄來源、日期、commit、測試、Reviewer 與 Owner Gate。