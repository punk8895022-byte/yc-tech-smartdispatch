# YC Dual Platforms｜Media Commerce × Tech Match｜2026-10-31 v0.1 DRAFT

狀態：**RESEARCH_ONLY / NOT_DEPLOYED / OWNER_GATE_CLOSED**。雙平台產品／開發任務規格，不宣稱已上線或已收款。

## 產品定位
- A：小雲 Media Commerce｜原創自媒體內容、聯盟商品候選、合法合作揭露、UTM、外部結清佣金追蹤、自有服務導流。
- B：YC Tech Match｜資訊弱電發案、師傅資格審查、需求與地區配對、報價、客戶選擇、工程驗收、依約收取服務費。
- Shared：Xiaoyun Business OS/AI OS 唯一主資料，Identity/Tenant/RBAC/CRM/Approval/Audit/Finance，不重造一套 Core 或第二份 canonical DB。
- 兩個前台各有品牌與市場定位，但共用營運後台、表單/審核與資產歸因。

## A 工作流／資料
- Idea → Draft → Rights/Owner Review → Approved → Manual Publish → Affiliate Link/Disclosure → Platform Order Statement → Settled Evidence。
- CreatorChannel, ContentAsset, Campaign, Merchant, AffiliateProgram, AffiliateLink, Attribution, Commission, SettlementEvidence, Consent, Approval。
- 未取得平台核准不得宣稱分潤；單純點擊不等於佣金；商品圖文、業配聲明和內容權利需核驗。
- 經現有 Media Factory/Media OS 管理內容，不開第二個影片生成核心。

## B 工作流／資料
- Request Draft → Submit → Moderation → Qualified Contractor Match → Bid → Customer Selection → Contract → Work → Acceptance → Fee Invoice → Settlement / Dispute。
- CustomerRequest, ContractorProfile, QualificationEvidence, Skill, Region, JobCategory, Bid, ContractRef, WorkOrder, Acceptance, ServiceFee, Review, Dispute, AuditEvent。
- 品類：CCTV、網路與 AP、門禁、NAS/伺服器、POS、電腦維修、弱電佈線、企業 IT 維護。試點以有真實供給的台南／南部開始。
- 服務費測試 5–8%（僅定價假設）；初期客戶直接付款給工程商，平台依服務契約另行收費。絕不自行無照保管工程價金，金流與稅務需 Owner 審核。
- 不使用虛假的「認證工程師」標示；工程資格與身分、合法施工範圍、保固及客訴流程先核對。
- 可研究重用既有 `punk8895022-byte/yc-tech-smartdispatch-1`，需事前安全/授權/部署盤點。

## 相互導流
一篇真實「辦公室 Wi-Fi 怎麼規劃」文章／影片 → 已核准且揭露的聯盟設備 → 需要安裝的人點「尋找弱電工程師」 → 發案 → 人工審核/報價 → 完工確認 → 經合法授權的匿名案例再次轉成內容。
使用同意前不得關聯媒體瀏覽資料與工程客戶身分。

## 最短驗收（兩條獨立 Gate）
M0 原型：可操作 4 頁（首頁、A、B、Admin）；A 新增企劃和候選商品、模擬點擊，B 新增示範案件、報價，Admin 讀兩端的本機 KPI。僅 localStorage。隔離 Chromium DOM 互動/390px layout PASS，網路導航 E2E、正式整合與真實 UAT NOT_RUN。
M1 A：1 個內容草稿經 Owner 審稿與真人手動發布，回填合法公開 URL；分潤資格與結清報表獨立核驗。
M1 B：合成資料/自願測試者完成一件發案 → 審核 → 事前核驗的師傅報價 → 客戶選擇 → 完工驗收（無真金流）。
M1 Shared：所有變更經同一 Policy/Approval/Audit/API；驗證租戶隔離、個資保護、重送冪等、事件來源/追蹤、已實收 vs 模擬收入區分。
M2：經 Owner 審核後接合法金流、退款與客訴、業者會員；未取得明確同意不得扣平台服務費。
M3：只有確實有成交與可控成本才導入更多自動化和跨區／跨境擴張。

## 開發／審核界線
- 一律先保留獨立 feature branch、Draft PR，不合併、不部署、不修改原服務帳戶。
- 不新增付費 API 或廣告費，不註冊付款服務、不發送陌生大量訊息、不公開客戶個資、不串正式 LINE OA（目前已知 429/P0 風險）。
- DRAFT／TEST_PASS／RUNTIME_VERIFIED／PAYMENT_SETTLED／OWNER_APPROVED 必須分開，不能把本機表單成功當真實成交。
- 核准關鍵：公司品牌主體、資安與個資責任、師傅與專業資格、交易與退款條款、服務費費率、稅票、支付服務合規。
- 本專案完整 Google Docs 母規格：https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit?usp=drivesdk
- 既有主決策：https://docs.google.com/document/d/1a3D3uKBefJO7ZsEScedhKUUl6o9ZAVhMHx47YCqNhfE/edit
- 金管會法規：https://law.fsc.gov.tw/LawContent.aspx?id=GL001488
- 數發部第三方支付 AML：https://law.moda.gov.tw/LawContent.aspx?id=FL098120
- YouTube 聯盟：https://support.google.com/youtube/answer/13376398
- 蝦皮聯盟：https://help.shopee.tw/portal/10/article/123888

## 變更記錄
- V0.1 2026-10-31：兩個獨立產品與單一後台，限隔離規劃；尚未上線。
