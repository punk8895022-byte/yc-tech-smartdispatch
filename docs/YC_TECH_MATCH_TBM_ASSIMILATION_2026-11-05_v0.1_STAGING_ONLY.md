# YC Tech Match｜TBM 公開流程吸收 × 案源證據品質模組｜2026-11-05 v0.1

**狀態：STAGING_ONLY / RESEARCH_ONLY。** 本次研究依據 TBM 公開網站的 FAQ/條款與小雲現有 YC Tech Match PRD。只吸收資訊結構與 Gate 設計模式，沒有取得／反編譯 TBM 程式或登入、抓取會員案件與資料。

## 來源

- 帳號與免費／付費額度：https://www.taiwanbm.com.tw/faq/list-6
- 發包附件、規格、時程與真偽非平台保證：https://www.taiwanbm.com.tw/faq/list-7?page=2
- 廠商驗證：https://www.taiwanbm.com.tw/faq/list-8
- 媒合非履約保證：https://taiwanbm.com.tw/terms/3-%E6%9C%83%E5%93%A1%E6%A2%9D%E6%AC%BE
- 既有深度競品研究：https://github.com/punk8895022-byte/yc-tech-smartdispatch/blob/feature/asset-os-dual-platforms-20261031/docs/research/YC_TECH_MATCH_TBM_COMPETITOR_2026-11-02_v1.0_RESEARCH_ONLY.md

## 實際吸收（Draft PR #1 非正式）

程式：pocs/cloudlink-staging-api/lead_quality.py
測試：pocs/cloudlink-staging-api/tests/test_lead_quality.py

- 接受的只有「人工整理公開案源 metadata」或「合成測試 metadata」，不存文字描述、電話、Email／LINE 或客戶姓名，不能自動爬取。僅允許明確白名單的 9 項鍵：source_mode/source_url/observed_on/posted_on/category/region/scope_confirmed/budget_known/deadline_known。
- 對服務類別、台南區域、日期新鮮度、需求範圍、預算、時程給 0–100 分；這是**完整度與服務適配度**，不是案源真偽、信用、成交率或投標價值。
- 服務範圍初期僅 CCTV/Wi-Fi 與台南；NAS、門禁及非台南案件 OUT_OF_SCOPE。30 日以上、日期缺失或需求不完整均要人工補證。
- 公開資料來源只要求安全 HTTPS URL，拒絕 userinfo、query tokens、fragments、localhost、IP literal、非公開測試主機；不能由 URL 推定來源真實可信。
- 所有結果皆不可執行：executable、can_contact、can_bid、can_publish、can_sync 恆為 False，financial_status 恆為 NOT_AVAILABLE；即使 100 分也僅 REVIEW_CANDIDATE。未驗證客戶身份／合法同意與來源內容權利。
- 未接線到正式 Business OS、每日案源排程或 FastAPI 端點；目前是可重用的 staging 純函數。小雲既有 G2 投影與 Owner Gate 保持原狀；沒有建立第二套資料庫。

## 可追溯執行證據

- 模組提交：28413d6c7e6137851e6f73421786f9994526f5da
- 測試提交：88e6fb305eed5bb725272a0f4605c5a477d99841
- GitHub Actions Run #41876061597：https://github.com/punk8895022-byte/yc-tech-smartdispatch/actions/runs/41876061597
- Runner head 88e6fb305eed5bb725272a0f4605c5a477d99841；completed/success。Job logs：**69 passed、1 warning、17 subtests passed**，CCTV_REAL_LOOPBACK_HTTP_PASS、CCTV_WORKORDER_REAL_LOOPBACK_HTTP_PASS、M1CB_REAL_SOCKET_PASS、SOURCE_PARSE_PASS。
- 尚有 Starlette/httpx 棄用與 GitHub Node20/Actions 維護警示；CI PASS 不等於真人 Reviewer / CVE / Canonical E2E / Production PASS。

## 下一 Gate（維持 HOLD）

1. 獨立 Reviewer 安全審查：外部資料 URL / PII / 惡意資料／來源驗證／品質打分偏差、既有測試隔離。
2. 先取得 Business OS 已授權 canonical Identity/Tenant/RBAC、Lead/Request/Quote、WorkOrder/Acceptance/Evidence/Audit 的 schema/身份權源；建議欄位非正式權威。
3. 核准後才在隔離 staging 做「人工匯入→只讀候選卡→Reviewer」閉環；不得外聯/投標/發布/付款/正式同步。
4. TBM 是否付費：最新確認價目、台南工程可投有效案件密度與真實轉換率皆未核實，**PAID_JOIN_HOLD**。

最終狀態：PUBLIC_UX_RESEARCH_PASS_SCOPED / G4_LEAD_QUALITY_MODULE_CI_PASS_SCOPED / PRODUCTION_ADAPTER_NOT_CONNECTED / INDEPENDENT_REVIEW_NOT_RUN / G4_CANONICAL_SCHEMA_UNVERIFIED / TBM_PAID_JOIN_HOLD / OWNER_GATE_CLOSED。

正式 main、LINE、AI Gateway、三台主機、Production DB、金流未變；未新增付費 API。
