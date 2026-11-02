# TBM 台灣商業媒合平台 × 小雲：競品研究與進駐可行性判定

- **版本**：V1.0（公開資料／既有專案唯讀查核）
- **查核日期**：2026-11-02（Asia/Taipei）
- **決策狀態**：`RESEARCH_COMPLETE_PUBLIC_SCOPE / PAID_JOIN_HOLD / G5_OWNER_GATE_CLOSED`
- **限制**：未註冊 TBM、未登入測試、未付款、未發包、未投標、未聯絡業者；GitHub／Google Drive 僅讀取，未修改正式環境，未新增付費 API。實際會員後台、最新案件全量、成交及投標品質均未驗證。

## 01. 執行摘要

**結論 A：TBM 值得觀察，但現階段不值得付費進駐。** 官方資料可確認免費註冊、B2B 展示與詢價、付費投標額度／廠商權限、曝光與 CRM 加購。官網首頁目前公開可見的需求示例少，最新公開例子日期為 2026-08-10；未發現小雲優先的台南 CCTV／Wi-Fi／NAS 直接匹配案件。這不等於整站完全沒有可接案件，而是公開證據不足以支付會員與競標成本。

**結論 B：部分產品機制值得吸收，但不複製整站。** 借鏡標準化能力頁、詢價與標案流程、發包驗證、報價分級、CRM／跟進、分類導流。小雲應以「案源品質與施工交付可信度」做差異化，沿用現有 YC Tech Match、Media Commerce、Business OS；不開第二套資料庫或公開未驗收流程。

## 02. 免費功能與付費機制（官方條款／FAQ）

| 能力 | 一般會員（免費註冊） | 廠商會員（註冊免費，開通功能付費） | 查核狀態 |
|---|---|---|---|
| 搜尋廠商、產品／服務、收藏、追蹤 | 可 | 可 | 官方 FAQ 已確認 |
| 詢價車、查看詢價回覆 | 可 | 可 | 官方 FAQ 已確認 |
| 投標／發包 | 可用但**無免費次數**，須購買額度 | 選購廠商功能權限後，每月投標 3 次＋發包 3 次，未用完不遞延 | 官方 FAQ 已確認；後台未測 |
| 品牌頁、產品／服務上架、文章、活動 | 不提供 | 需購買廠商功能權限 | 官方 FAQ 已確認 |
| CRM | 可獨立加購 | 可加購 | 官方 FAQ 已確認 |
| 型錄 PDF、QR、廣告版位 | 不提供 | 廠商功能開通後另選購 | 官方 FAQ 已確認 |
| 平台保管工程款、交易抽成 | 平台公告稱**不介入金流、也不收交易手續費** | 同左 | 以公開條款／FAQ 為準，非每筆真實交易查核 |
| 廠商權限實價／投標單價／廣告及 CRM 金額 | 未能可靠讀取 | 未能可靠讀取 | `PRICE_NOT_VERIFIED` |

**價格資訊存在不一致**：2026-05-01 公告寫「免費建立品牌專頁」，但 FAQ 說廠商品牌展示須選購權限。`/service` 費用頁以圖片為主，文字抽取不足，不能聲稱已取得最新版價目。將「正式價目表、效期、稅額、退費、購買額度扣點規則、實際免費品牌頁範圍」列為採購 Gate。

**帳號結構注意**：官方 FAQ 表示一般／廠商帳號彼此獨立，不能直接互轉；廠商付費權限到期後品牌內容會下架。要做長期搜尋曝光，應評估此風險，不把 TBM 品牌頁當成唯一官網。

官方資料：
- https://www.taiwanbm.com.tw/faq/list-6
- https://www.taiwanbm.com.tw/faq/list-6?page=2
- https://www.taiwanbm.com.tw/faq/list-7?cid=7
- https://www.taiwanbm.com.tw/faq/list-7?cid=7&page=2
- https://www.taiwanbm.com.tw/service
- https://taiwanbm.com.tw/news/view-4

## 03. 公開案件品質：可驗範圍

官方首頁可觀察到「誰有需求?!」區塊有下列公開示例：

| 日期（網站標示） | 主題 | 對小雲的適配 | 主要缺口 |
|---|---|---|---|
| 2026-08-10 | 尋求在地小店／工坊異業曝光合作 | 低：可能與 Koala 行銷有間接關聯 | 未確認案主、地區、預算、時效 |
| 2026-07-24 | 遠端行政秘書 | 低 | 非主要服務，需求規格不足 |
| 2026-07-15 | 短影音剪輯服務 | 中：Media Factory 類別相關 | 無法證明目前仍開放、報價條件未知 |
| 2026-06-12 | 專櫃品牌團購合作 | 低 | 非工程主線 |
| 2026-05-18 | 尋找可配合印刷廠商 | 低 | 非主要服務 |
| 2026-05-18 | 尋求低價寵物用品廠商 | 低 | 非主要服務 |

首頁「最新媒合一覽」另見 2026-05-12 設計師、社群小編、公司清潔，以及 2025-12-18 午餐外送等示例。部分卡片出現 `#`、`公司名稱`、`商品名稱` 佔位文字；網頁標頭有「此為校稿頁面」。

**採樣限制**：這只是公開首頁可見卡片，**非全站案件數或 30 日新增案件統計**。部分完整案件頁／會員功能未能公開取樣。無法據此推估實際客戶回覆率、成交率、參標競爭數與案件造假比率。2026-11-02 的「近期 30 日小雲可投有效案件」因此列為 `NOT_VERIFIED`，不是宣稱全站 0 案。

**重要風險**：官方 FAQ 表示發包內容會審核違規／違法，但**不審查需求真偽及可行性**；廠商驗證標章基本上核對公司名稱與統編，不能視為履約擔保。交易糾紛由當事人解決，平台不介入金流。

官方資料：
- https://www.taiwanbm.com.tw/
- https://www.taiwanbm.com.tw/faq/list-7?cid=7&page=2
- https://www.taiwanbm.com.tw/faq/list-8
- https://taiwanbm.com.tw/terms/3-%E6%9C%83%E5%93%A1%E6%A2%9D%E6%AC%BE

## 04. TBM 商業模式拆解

- **客群**：台灣中小企業、製造／批發業、工作室、自由接案者、採購需求方。
- **供給端價值**：品牌與服務上架、搜尋曝光、被詢價、參與投標、CRM 管理及行銷工具。
- **需求端價值**：搜尋供應商、詢價與比價、發布需求、收藏追蹤。
- **收費槓桿**：廠商功能權限、額外發包／投標額度、CRM、型錄／QR、廣告曝光。這是公開功能結構推導出的可能營收組合，不等於已查到實際營收占比。
- **交易模式**：媒合／資訊服務，不作工程款價金保管或平台內正式履約擔保；依網站 FAQ 自述不收交易手續費。
- **成長飛輪**：供應端展示→類別頁／搜尋曝光→採購詢價→投標與案件回應→更多廠商投資展示／曝光；實際網路效應**尚無流量數據證明**。
- **可能弱點**：公開案件密度及時效難驗證、費用訊息存在衝突、部分佔位卡、分類過廣與品質分流困難、交易保障依賴雙方自行處理。

## 05. 對照小雲現有資產（GitHub／Drive 唯讀）

資料來源：
- Drive《Asset OS｜雙平台整合 PRD｜Media Commerce × YC Tech Match》：https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit
- Drive《小雲 Business OS｜多事業營運與數位商品商業化 PRD》：https://docs.google.com/document/d/1otVSuymPm7JBoJsSZSvBBK9b0jo6LsREL3zbBQ8h838/edit
- GitHub YC Tech Match 主線：https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1 （Draft／未合併）
- GitHub Media Commerce 展示：https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/12 （Draft／未合併）
- G2 來源與 schema Gate：https://github.com/punk8895022-byte/yc-tech-smartdispatch/blob/feature/asset-os-dual-platforms-20261031/docs/YC_TECH_MATCH_G2_SOURCE_AND_SCHEMA_GATE_2026-11-01_v0.1_RESEARCH_ONLY.md

| TBM 可借鏡項 | 小雲既有基礎 | 建議差異化與下一個 Gate |
|---|---|---|
| 廠商展示、能力文章、作品案例 | Media Commerce 靜態 2 案例；PR #12 G3 有範圍限定的合約／Chromium 版面 PASS | 加入有來源證據／保固說明的工程案例，但需授權、去識別、Owner 審核；不公開合成案例當實績 |
| 發包與投標 | YC Tech Match Draft PR #1 已有隔離三角色 FastAPI／SQLite 範例 | 統一需求表單：地點、類別、預算級距、現場照片、驗收項目；需要身分驗真與審核紀錄 |
| 廠商驗證 | Business OS 規劃有 Contractor/Qualification | 優先做服務區域、資格／保險文件、期限、人工查核與標章撤銷；不能只看統編即保證履約 |
| CRM 和追蹤 | Business OS 有 Customer/Opportunity/Case/Quote 等規劃 | 做詢價→合格商機→報價→簽約→工單→完工→保固可稽核漏斗；先只讀合成資料 |
| 付費廣告和投標 | 小雲尚未正式收費或對外媒合 | 先確證真實商機與單位經濟，禁止先建付費牆或宣稱成交抽成 |
| 類別分類 | 既有初期 network/cctv/access schema，NAS 尚未接通 | 第一階段只針對台南／南部 CCTV、Wi-Fi；NAS 應標未支援，不開假服務承諾 |

**現況證據分級**：既有來源比對與隔離測試有部分 PASS，但 canonical Identity/Tenant/RBAC、正式 CRM、真實同意證據、履約工單、稅務／支付及真人端到端仍未接通。不能把 G2 靜態投影、CI 自動 layout 或模擬報價寫成正式上線。

## 06. 是否進駐 TBM：決策門檻

| Gate | 必備證據 | 判定 |
|---|---|---|
| J0 公開觀察 | 官方 FAQ、費用與條款、公開案源首頁、案例與分類 | `PASS_PUBLIC_SCOPE` |
| J1 價目／權限 | 官網最新完整文字價目或平台客服正式書面回覆：投標單價、廠商年／月費、退費、有效期限、額度扣除規則 | `HOLD` |
| J2 案源有效性 | 可追溯且仍開放的台南／南部 CCTV、Wi-Fi、NAS、弱電維護或 AI 自動化需求；日期、服務地、預算／工項、身份、回覆方式 | `HOLD` |
| J3 商業評估 | 每筆必要投入工時、投標成本、成功機率的保守假設、可驗證毛利；與 Tasker／PRO360 現有渠道比較 | `HOLD` |
| J4 Owner 核准 | 是否以個人／公司註冊、資訊提供範圍、是否允許投標與支付 | `CLOSED` |

**進駐判定**：現在不買任何付費方案。允許持續查看公開頁面並記錄有來源的案源。未來只有在 J1～J3 具足夠證據、且 Owner 開 Gate 後才考慮註冊與試投。若須付費才能看到可驗證案件，不能因「可能有商機」就預付。

**經濟模型**：

> 單案可接受獲客成本 = 預估實際毛利 × 目標容許 CAC 比率；預期單案獲客成本 =（會員分攤＋投標額度＋人工搜尋／提案時間成本）÷ 預期實際成交數。尚無合理成交樣本，不能計算可靠 ROI。

## 07. 不增加成本的驗證流程

1. **公開層每週抽樣**：保留官方 URL、頁面可讀狀態、標示日期、案主可查核程度、預算、類別、地區；對重複／過期／佔位文設「不可投」標籤。
2. **分類**：P0 台南 CCTV／Wi-Fi／網路弱電；P1 NAS 維護／企業 IT；P2 AI 自動化／網站／短影音。此為商機優先序，不代表對外平台已支援。
3. **證據卡**：`source_url`、`observed_at`、`posted_at`、`category`、`region`、`budget_text`、`recency_status`、`contact_validity`、`red_flags`、`evidence_grade`、`go_no_go`；缺欄位標 UNKNOWN，不補假數據。
4. **競品差異驗證**：觀察是否有具體規格、可證實的案主、回覆窗口、重複案件；比對 Tasker／PRO360 搜尋成本與商機成熟度。
5. **最小產品切片**（Owner 授權之後才可實作）：在既有 `yc-tech-smartdispatch` 隔離分支用純合成資料產出「一筆 CCTV 報價／審核／驗收」的端到端證據；不新增主資料庫、無假登入、無自動外聯。

## 08. 建議優先的五項產品能力

- **P0｜高可信度需求表單**：地域／設備類型／現場照片／預計工期／驗收條件，避免空泛「要裝監視器」造成估價失真。
- **P0｜案件品質評分而非付費置頂優先**：時間新鮮度、工項完整性、地區、需求證據、可回覆狀態；只評估有證據的欄位，不能用 AI 想像補分。
- **P0｜報價比較與範圍界定**：材料、工資、佈線／施工、保固、排除事項、工期；方便買方比較不同標案。
- **P1｜技師資格與紀錄**：文件類型、效期、核查人與撤銷權限；與正式使用者資料隔離。
- **P1｜CRM Follow-up＋保固**：提案、未回覆提醒、成交、驗收照片、維護與推薦的可稽核閉環。

## 09. 驗收清單

- [x] 官方會員免費／付費結構公開層盤點
- [x] 官方公開展示樣本與時效風險分析
- [x] 交易責任與平台驗證邊界查核
- [x] 讀取 Google Drive Business OS／Asset OS 規格
- [x] 讀取 GitHub Draft PR #1／#12 與 G2 欄位契約
- [ ] 價格圖片的完整正式數額與最新費率查核
- [ ] 帳號登入後案源全量、刊登與投標實測
- [ ] 案主有效性、實際回覆與成交樣本
- [ ] 工程匹配度的近期 30 天樣本統計
- [ ] 正式 Owner 進駐與付款批准

### 最終 Gate

`PUBLIC_COMPETITOR_RESEARCH_PASS_SCOPED`／`TBM_PAID_JOIN_HOLD`／`YC_TECH_MATCH_G2_PARTIAL`／`G5_OWNER_GATE_CLOSED`

這不是 TBM 商業成效或小雲平台已完成 E2E 的驗收報告。所有結論只對可讀來源與既有只讀查核範圍有效。

---

## 10. 2026-11-02 Drive／GitHub 增量與 CCTV 合成政策實測（新增；不改原競品結論）

- **技術依據**：既有 `pocs/cloudlink-staging-api/marketplace_contract.py`、`g2_projection.py`，在隔離目錄比對來源 Git Blob SHA-1 均與 GitHub 相同。
- **測試檔**：[`tests/test_tbm_cctv_policy.py`](../../pocs/cloudlink-staging-api/tests/test_tbm_cctv_policy.py)。以原來源純函數執行 2026-11-02 本地 Python `unittest`，2/2 PASS，無新增相依套件。
- **合成案例**：`CCTV-SYNTHETIC-20261102-001`，台南 4 支 CCTV 虛構需求；DRAFT 不能媒合；同意＋審核的 APPROVED 只可篩選具台南服務/資格/Owner Gate 的合成工程商。
- **負測**：NAS、外縣市、未核准、缺同意證據拒絕；read-only projection 的 `executable=False`；不提供正式同步；無商用合同、發票與銀行對帳證據不能認列服務費或公開案例。
- **重要界線**：測試中的報價與「選擇」只是合成紀錄，**並未實際執行 FastAPI HTTP 的 request→moderate→quote→select**；施工工單、完工驗收、正式 IAM/Business OS 核心仍未實作／未驗收，不能以 2/2 PASS 誤稱完整 G3。
- **Drive 同步**：本文件已同步至 Asset OS 專案資料夾；雙平台 PRD 另附增量索引。原 `main` 與任何正式 Runtime 保持不變。
- **Gate**：`PUBLIC_RESEARCH_PASS_SCOPED / G2_CCTV_POLICY_LOCAL_PASS_SCOPED / G3_REAL_HTTP_AND_WORKORDER_HOLD / TBM_PAID_JOIN_HOLD / OWNER_GATE_CLOSED`。
- **下一步**：經授權的隔離執行環境跑現有 FastAPI/SQLite 真正本機 HTTP 流程，再釐清 WorkOrder/Acceptance/Audit/Finance canonical 資料契約。未取得 Owner Gate 不合併、部署、付費或公開發包。
