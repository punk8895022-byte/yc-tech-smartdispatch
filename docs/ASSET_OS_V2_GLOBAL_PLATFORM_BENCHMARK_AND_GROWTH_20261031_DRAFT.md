# 小雲 Asset OS V2.0｜全球平台商業模式比較、可行性與複利成長架構
**研究日期：2026-10-31｜狀態：DRAFT / RESEARCH_ONLY / OWNER_GATE_CLOSED｜禁止擅自合併與部署**
**文件類型：** 平台投資委員會戰略 PRD / 商業模式與決策矩陣 / 90 天試點。
**既有基線：** [雙平台 V0.1](https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit)；[Asset OS V1.0](https://docs.google.com/document/d/1a3D3uKBefJO7ZsEScedhKUUl6o9ZAVhMHx47YCqNhfE/edit)；[舊 CloudLink 前端](https://github.com/punk8895022-byte/yuntech-prototype)。
**一頁決策：** 不追求沒有經濟基礎的「無限指數成長」。以「垂直 B2B 弱電/資訊交易網路」為高信任的商務楔子，先由現有專長人工媒合；以「原創技術內容 × 已核准聯盟」降低獲客成本；以「工程商工作流工具」提供重複收入；以「供應商/創作者/同業夥伴」在成交後分潤擴大流量。兩個前台/一套營運和審核規範，正式資料與個人 AI OS 資料須租戶/權限隔離。首期不自行代收保管全額工程款，不開新付費 API，不買廣告，不上線假金流。

## 目錄
01 全球標竿與不可照搬之處
02 競爭位置和分期市場選擇
03 六大收益引擎及採取順序
04 四個成長飛輪及複利前提
05 業務單位經濟模型/情境
06 可行性評分/停損風險
07 兩前台 × 共用 Core 的系統模組
08 30/60/90 天可驗收的路線
09 營運指標/Evidence/Gate
10 法規、授權、資安與平台限制
11 資料來源/待驗證
12 變更紀錄

## 01 全球標竿：按變現機制學習，不做外形模仿
| 範式 | 平台/市場 | 實際可借鏡商業機制 | 對小雲的建議 / 不照搬 |
| --- | --- | --- | --- |
| 需求線索付費 | PRO360（台灣） | 專家免費瀏覽、有效聯繫/報價費，分一般報價、保證回覆和推廣服務；一般專家完成後不再抽成 | 先引進「合格需求」與師傅供給，等實際成交率足夠才測試收費；避免把不良案源收費 |
| 高意圖直接詢問 | Thumbtack（美國） | 專家免會員費，依聯繫/線索預算獲客 | 較適合即時需求、成交前無法證明成交之早期市場 |
| 交易與信任服務 | Taskrabbit（多國） | 工作服務費/信任支援費；費用隨市場與訂單條件不同 | 平台有履約/客服與信任成本，只有真實提供保障才能合理收這類費 |
| 工程商會員/工具 | Checkatrade（英國） | 免費專頁及付費驗證/目錄/管理工具訂閱 | 工程商月費必須提供獨立於媒合的 CRM/報價/工單實用性 |
| 窄品類雙向媒合 | MyBuilder（英國） | 客戶免費發案→技師表達興趣→比價/評價→承攬 | 一個地區 × 三個相近技術類別先建立配對流動性 |
| 混合線索/廣告/合作夥伴 | Angi（美國等） | 線索、專家會員、服務，以及合作夥伴引流；2025 年度 10-K 總收入低於 2024，成長不可假設 | 建立通路混合但避免付費買流量燒錢；監控需求品質與多邊市場成本 |
| 工程商經營 SaaS | Jobber / ServiceTitan（北美） | 工程商CRM、報價、派工、付款與長期客戶管理 | 做服務商工作台以提高使用頻率，不能只靠一次性成交 |
| 創作者商品分潤 | LTK、impact.com（全球） | 內容→產品→佣金、品牌合作、歸因；平台多方互連 | 小雲 Media Commerce 最先只是自用/內部內容與聯盟分析，不自行打造全球創作者市集 |
| 商家/創作者合作 | Shopify Collabs（全球） | 商家邀創作者，追蹤推薦成交；**目前停止新創作者直接註冊** | 商家邀請及適用資格先確認，不能假設可立即開帳戶 |
| 台灣內容聯盟 | 蝦皮分潤、YouTube Shopping | 需審核/頻道資格，成交/退貨/請款規則各異 | 先確認帳戶 eligibility 和佣金資料；點擊不等於已結清收入 |
| 創作者訂閱 | Patreon（全球） | 會員和一次性付費；零起始月費但收入抽成及金流費 | 在真的有忠誠讀者與獨特內容後才做會員，避免空社群 |
| 合作型專業網路 | Airbnb Co-Host Network | 區域專家提供專業服務，靠審核/信任與匹配 | 建立「地域＋技能＋績效」可信工程師池，而不是無差別廣撒案源 |

研究原則：官方價格／資格會變，以上是資料收集時點快照，不以競品財務數字或廣告宣稱代表小雲績效。

## 02 定位與先打的市場
- **核心人群**：台南、南部 5–30 人資訊弱電、監視器、網路 AP、門禁、NAS、POS、設備維護供應商；買方為有維護/工單/據點需求的中小企業、店家、社區、管理方。
- **最小可行地理/品類單元**：先台南及可實際服務的鄰近範圍，先「商用網路/AP」、「監視器/NVR」、「門禁/弱電維護」三類；每類先建立 5–10 位待核驗合作工程師（驗證目標，不是現況）。
- **差異化**：專門的技術需求問卷、勘場/BOM、透明報價範本、實際驗收、設備履歷、保固維護、可重複訂單，不與綜合型平台在所有類別打廣告戰。
- **不要**第一天就設全台 100 類、跨境實體工程、交易托管、物流、工人保險承諾或自建大型創作者社群。跨境先做數位教學/範本與 SaaS 類型測試。

## 03 六大收益引擎與動態採用
A. **高意圖合格商機費（先人工驗證）**：有效需求=願意被聯繫+可服務地區+有清楚需求/預算/期限+非重複/偽造。可先免費，品質足夠才試 1 個清楚標價的聯繫費，不以每次點擊算錢；不雙重向同一案件收不透明費用。
B. **完成交易服務費（選擇性）**：僅在平台能證明訂單及提供實質媒合/驗收服務、收費契約清楚時，試收已完成可核對案件 3–8% 的**假設定價區間**，平台不直接持有工程價款，實際費率須扣售後/退費/稅費測試。與 A 不能未揭露重複收費。
C. **專業工具訂閱**：工程師公司可選 CRM、報價、工單、設備資產履歷、保固提醒；假設 490/990/1990 元月費階梯，靠工具價值而不是買排名，不保證案源。
D. **合法聯盟/產品推薦**：以原創施工教學、工具測試、比較文章、設備清單導購；由有資格的外部聯盟付款（蝦皮、YouTube Shopping、impact.com 等），待官方核對結清，不算平台 GMV；商品推薦需揭露利益關係。
E. **供應商夥伴分銷**：與設備經銷商、原廠、系統整合商、創作者簽書面合作，按被驗證的新成交有效行動分潤；避免先行支付大額廣告費或不合法回扣。
F. **企業維護/白標與授權**：在 3 家以上付費工程商的工具流程確實可用後，擴展多據點/企業會員、維護合約、可授權 SaaS 模組；先拿訂單再擴功能。

採用節奏：D0–30 不要求任何正式收費；D31–60 以經 Owner 核准的單一收費機制為主；D61–90 若有足夠真實交易與續約，再測第二收入引擎。禁止「六項收費同時啟動」造成用戶不信任。

## 04 四個複利飛輪（每個要有可稽核事件）
**飛輪 1：內容→需求→完工→可授權案例→更精準內容**
技術實測文章/影片 → 需求類別頁/發案 → 工程師完成 → 經客戶與師傅同意的匿名案例 → 口碑/自然搜尋。指標：非付費合格詢問/每篇、內容到有效發案轉換、合法授權案例數。
**飛輪 2：供需密度→報價速度→成交率→師傅收益→更多供給**
一個「地區×技術類別」至少能在 48h 得到 2 份合格報價，驗證後再擴相鄰類別/地區。指標：有報價覆蓋率、2 報價比率、平均首回覆時間、實際完工率、爭議率。
**飛輪 3：接案→工單/保固履歷→長期管理→再購/訂閱**
每筆案件留下合法、受限的設備、保固與維護日程，使工程商能向原客戶提供續約與技術回訪。指標：付費工程商月留存、每戶有效工單、人時節省、重複採購。
**飛輪 4：合作夥伴→增量案源→可驗證佣金→更多夥伴**
設備供應商、同行、社群創作者只對可核實增量價值分潤，設唯一來源 ID、防重複歸因、退款追回與合法揭露。指標：合作夥伴每月新合格需求、每筆貢獻、夥伴留存。
**指數成長前提**：網路效應要大於服務/客服/獲客成本的增加。以同一區域、同一類別的媒合流動性證據做 Gate；不得承諾必達指數曲線，也不得靠 AI 生成大量低品質 SEO 頁面冒充網路效應。

## 05 單位經濟模型（以下全是決策測試假設）
定義：Q=每月經審核合格需求；m=有實質可服務報價的覆蓋率；w=已報價案件完工率；A=平均完成工程合約額；t=契約可收平台費率。
可收服務費毛額 = Q×m×w×A×t（僅適用有正式服務費契約、完成且收費權可驗證的案件）；平台 GMV = Q×m×w×A，不是營收。
訂閱營收 = 付費工程商×每戶實際月費；已核准聯盟佣金 = 淨合格成交×有效訂單佣金，不可用點擊估算為收入。
平台淨貢獻 = 實際已結清平台收款 − 手續費 − 退款與服務補貼 − 可變客服/審核/驗收人時成本 − 相關直接費用。經濟利潤再扣固定成本與 Owner 人力估值。
範例（非預測）：Q=40、m=70%、w=45%、A=NT$25,000、t=5%，成交案件期望數 12.6（統計期望，不是可成交半筆），平台服務費毛額約 NT$15,750；假設有 10 戶工具訂閱 × NT$790 = NT$7,900；假設聯盟已結清 20 單 × NT$1,500 × 3%=NT$900；總**情境毛收入**約 NT$24,550，完全不等於實收或淨利，且三項收入均須分別符合資格、避免雙計與另外扣成本。
壓力測試：若 40 件需求只有 25% 有報價且 20% 完工、A 15,000、t 5%，服務費毛額僅 NT$1,500；因此如果低媒合流動性，不能靠擴流量解決。
不得以「完工總額」充作平台營業收入，不得把訂金/技師收入/模擬錢包加進平台現金流，不得承諾 20% 月成長複利可持續。

## 06 可行性（內部研判分數，非市場統計）
評分因素：創始人資源與技能貼合度 25%、零新增固定成本可試程度 20%、驗證速度 15%、貢獻毛利潛力 15%、長期網路效應/防禦 15%、風險可控性 10%。每項 1–5 越高越好；先用質性排序，沒有數據時不產出虛假精確總分。
**高**：台南資訊弱電「經審核的免費發案＋人工高品質媒合」；既有工程知識/CloudLink 前端可直接重用；無需先控制金流。
**高**：工程商輕量 CRM/維護管理；即使沒有大量市場需求，也能對已有客戶提供具體工具價值。
**中高**：原創資訊工程教學 × 合法設備聯盟導購；省廣告但仍需內容實作、聯盟審核、受眾和流量時間。
**中**：合作渠道按成交後分潤；初期靠人工建立幾個真實可信夥伴，不能假設擁有大量經銷商網路。
**中低**：完成工程抽 5–8% 並自行驗證訂單；可能被繞單，客訴成本高、收費權與契約待驗。
**低（現在不做）**：一開始跨全台/所有類別做 C2C Marketplace、自營錢包託管/放款、全球創作者社群及自建分潤金流網路。
殺手風險：雙邊市場無足夠供給、假工程師、工作資格不明、客戶私下交易、假成交、低毛利、金流/稅務/個資違規、平台評論舞弊、即時客服過度消耗。

## 07 技術架構：兩前台，公共治理，嚴格隔離
- Public Front A（Media Commerce）：Content Library、Affiliate Catalog、Disclosures、UTM/Attribution、Creator/Brand Approval、Commission Import（不碰外部憑證，先人工 CSV/明細）。
- Public Front B（YC Tech Match）：Visitor Request Wizard、Contractor Search、Qualification, Quotation/Comparison、WorkOrder/Acceptance、Dispute、Equipment Warranty、Subscription。
- Business Control Plane：Identity/Org/Tenant/Role/Policy、Approval、Audit、CRM/Lead、ServiceCatalog、Referral、Attribution、Billing/SettlementReference、Support Case、KPI。
- **安全邊界**：現有私人小雲 AI OS 與公開多租戶平台不能直接共用其私有任務/憑證/資料表；可借用受審的 shared contract/治理元件，另設隔離的公用 SaaS 資料域及租戶 RLS/Backend RBAC；同一 domain 每個環境只有一個 canonical 主資料。正式 DB/Schema 拓撲要先盤點決定，不能因追求「共用」就讓個人秘密暴露。
- **既有 CloudLink**：保留客戶/技師/管理頁及報價、進場、完工、照片、驗收的 UI 模型；移除 Demo 明文密碼、瀏覽器錢包、假的「已付訂金/放款」以及在 localStorage 存個資、銀行照/照片作正式功能。舊版沒有真正的多家報價/比價、平台計費 API、金流簽核。
- 後端 MVP API（staging）：POST /requests; GET /requests/{id}; POST /contractor-profiles; POST /quotes; POST /quotes/{id}/select; POST /work-orders/{id}/evidence; POST /acceptances; GET /dashboard; POST /content/drafts; POST /referrals; POST /settlement-evidence/import（需 RBAC/驗證/冪等/稽核）。
- 資料模型最小集合：Organization、User、ContractorProfile、QualificationEvidence、ServiceRegion、Request、Quote、QuoteVersion、WorkOrder、Acceptance、Dispute、ReferralPartner、AttributionEvent、ContentAsset、AffiliateProgram、CommissionStatement、Subscription、FeeInvoice、PaymentEvidence、AuditEvent。每個款項需要 issuer、contract、currency、source、actual_settlement_at、evidence、status；不得自動標記 paid。
- 成本：沿用 Netlify、現有 GitHub/Drive、既有主機和本地模型；必須量測流量、資料庫、郵件/通知和支援人時，免費額度可能不足，不得新增付費資源。

## 08 三個月路線和推進 Gate
**M0（D1–D14）｜市場與安全**：只讀盤點舊 CloudLink UI + 後端 stub、重用清單/安全 FAIL；從真實管道招募 5–10 位自願測試合格工程師，訪談 10 個有實際需求/痛點的商家；基於假資料完成前端 mock→可信 staging 合約規格。流量不是 PASS，必須能核對供需雙方。
**M1（D15–D30）｜本地流動性試點**：1 個地區/3 類；先免費，人工服務台；10 個有效需求為初步樣本、目標 70% 在 48 小時有 2 份以上合格報價；留存源與時效。無法達成就縮小服務區/類別，不盲目投廣告。
**M2（D31–D60）｜真實有界服務與內容引擎**：完成 3 筆有證據工程驗收的試單（非保證），允許的公開匿名案例 → 5 篇原創、實用深度內容/短片改編；合法聯盟資格查核；在有願付費意向的工程商中測 1 套 CRM 月費價值主張。發布需 Owner Gate。
**M3（D61–D90）｜小額定價試驗**：僅在真實交易、用戶同意、服務條款/發票/資格/資安都 PASS 時，選擇單一已揭露收費：合格線索或可驗證媒合服務費，試 3–5 付費帳號。驗證 recurring usage、客訴成本、單案貢獻、30/60/90 天重複需求；再決定是否擴類別/城市。
**擴張門檻（先作假設）**：同一地區×類別連續 2 個月，每月 >=30 合格需求、>=70% 在 48h 有 2 份有效報價、媒合後完工比例 >=30%、每筆實收淨貢獻 >0、無重大安全缺陷和未處理客訴；達不到不得複製城市。指標的樣本量和門檻需依實際試點修訂。

## 09 控制台與 Evidence
每天：合法來源內容 impressions/合法點擊、有效需求、重複/假案率、地區與類別、可用工程師、48h 報價率、案件選擇/完工/驗收、爭議、首次詢問到結束時間。
每週：有用內容導入「合格需求」比率、兩份報價覆蓋率、平台獲客成本（含人工）、每筆有效請求人工分鐘、工程師月活、工程商使用工具的節省時間（實測）、合作夥伴貢獻。
每月：分開顯示 GMV、服務費應收、實收、佣金待驗、實收、退款、平台維護訂閱 MRR、平台費/金流費/售後人力、現金與負債、經濟利潤。真實 bank/partner statement 才標 SETTLED_VERIFIED。
資料判定：IDEA / EVIDENCE_FOUND / DESIGN_DRAFT / STAGING_TESTED / USER_ACCEPTED / OWNER_APPROVED / PAYMENT_SETTLED / PRODUCTION_VERIFIED；不可互相替代。
資料需附 source_uri、snapshot_at、owner、environment、consent/license、status、request_id/job_id/partner_id、audit_trace；外部發案自動發送一律需 Owner 核准。

## 10 法遵、資安與商業倫理
- 以台灣個資法當時已生效條文為準；2025 修法部分條文仍待施行，不能直接假設全部已生效。
- 平台若實際提供代理收付網路交易款項，須評估第三方支付 AML 規定、發票/會計及持款責任；M0-M2 不自行托管工程款，不用自製錢包。
- 交易是否只能靠兩邊口頭報「已成交」？**不可以直接認列為已收服務費**；先讓平台以「合格線索＋獨立 SaaS」成長；實際抽成需契約、可核驗收款和對帳證據。
- 工程資格依類別核實必要登記/證照、保固/責任與現場安全；不允許憑自述就顯示認證徽章。
- 所有推薦/帶貨明確揭露佣金或合作關係、允許聯盟鏈接的投放渠道、退貨後佣金調整；假評價與未授權素材禁止。
- Google 明確反對以操縱排名為目的的海量、無新增價值內容；不得把 AI 批量複製當作可持續流量策略。
- 既有 LINE 429/管理權限、Koala 資安 WARN 與 Agent Runtime NOT_CONNECTED 不因新企劃被視為 PASS；禁止直接借用正式帳號與金鑰。
- 任何公開文章/招募/外部聯絡/支付/部署/權限變更都保留 Owner Gate；只完成本文件不等於取得執行授權。

## 11 官方案例與查核來源（依 2026-10-31 抓取）
- PRO360 模式：https://www.pro360.com.tw/pro/guide/memebrship/ ； FAQ：https://www.pro360.com.tw/pro/faq/
- Thumbtack：https://www.thumbtack.com/pro
- Taskrabbit 官方費：https://support.taskrabbit.com/hc/en-us/articles/46260411872155-What-s-the-Taskrabbit-Service-Fee
- MyBuilder：https://www.mybuilder.com/how-it-works
- Checkatrade：https://join.checkatrade.com/pricing/
- Angi 2025 10-K：https://www.sec.gov/Archives/edgar/data/1705110/000170511026000011/angi-20251231.htm
- Jobber：https://www.getjobber.com/features/client-hub/
- ServiceTitan：https://www.sec.gov/Archives/edgar/data/1638826/000095017025005456/ttan-20241031.htm
- LTK：https://company.shopltk.com/en-gb/how-it-works-creators
- impact.com：https://impact.com/Partners/
- Shopify Collabs creator signups：https://help.shopify.com/en/manual/promoting-marketing/collabs
- 蝦皮分潤：https://help.shopee.tw/portal/10/article/123888-%E8%9D%A6%E7%9A%AE%E5%88%86%E6%BD%A4%E8%A8%88%E7%95%AB%E4%BB%8B%E7%B4%B9
- YouTube Shopping 台灣資格：https://support.google.com/youtube/answer/13376398
- Patreon：https://www.patreon.com/pricing
- Airbnb Co-Host：https://www.airbnb.com/help/article/3378
- Google SEO：https://developers.google.com/search/docs/essentials/spam-policies
- 台灣第三方支付規範：https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0080060
- 台灣個資法：https://law.moj.gov.tw/LawClass/LawAll.aspx?PCode=I0050021

## 12 變更紀錄
- V2.0（2026-10-31）：首次整合全球多模式 Benchmark、收費模式選擇、四大飛輪、壓力測試、平台技術和審核門檻；**不覆蓋 V0.1，V0.1 保留為雙平台產品初稿**。