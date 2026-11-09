# YC Tech Match｜G4 CI 實證 × Business OS Canonical Interface Gate｜2026-11-02 v0.1

**用途**：交付獨立 GitHub Runner 對 CCTV 隔離合成流程的真實執行證據，並界定進入正式 Business OS 實際對接前必須滿足的資料契約、權限、證據驗真與 Owner Gate。此文件為 **RESEARCH_ONLY / STAGING_ONLY**，不是 Production PRD 或已實作 canonical adapter。

## 0. 單一權威來源與審查入口

- [Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1)：既有開發分支 `feature/asset-os-dual-platforms-20261031`；Owner Gate CLOSED，未合併 main。
- [既有 Google Drive Asset OS 主 PRD](https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit)；[2026-11-02 CCTV HTTP 工單證據](https://docs.google.com/document/d/1R0xeURNW8QXQjS2DYEO3CjX5joqvnFxlqFtqyfc1c10/edit)。
- [本次 GitHub Actions workflow](../.github/workflows/yc-tech-match-cctv-staging-ci.yml) 的 Repo 實際檔案位於 `.github/workflows/yc-tech-match-cctv-staging-ci.yml`；工作流加入既有 Draft feature branch，不是 main。
- [G3 來源和程式證據](YC_TECH_MATCH_CCTV_HTTP_WORKORDER_G3_2026-11-02_v0.1_STAGING_ONLY.md)。

## 1. G3 Clean Runner 實際驗證

- GitHub Actions Run ID **41380419911**：https://github.com/punk8895022-byte/yc-tech-smartdispatch/actions/runs/41380419911
- event=`push`；workflow=`YC Tech Match CCTV isolated regression`；run head SHA **`2cfe7ef4519561050c5ba9a03bae4a51c3a4caa1`**；completed / **success**。
- Job ID **125069798755**，job `cctv-staging-only`：Ubuntu 24.04／Python 3.12.15，`contents:read`，checkout credentials 不留存，timeout 10 分鐘；不帶正式憑證、不部署、不使用正式資料。
- 從 GitHub Job Logs 實際核對：
  - `python -m pytest -q` → **59 passed, 1 warning, 3 subtests passed in 2.03s**
  - `python scripts_tbm_cctv_loopback_http.py` → `CCTV_REAL_LOOPBACK_HTTP_PASS`，含 synthetic issue/create/moderate/quote/select/SQLite/403/404/redacted audit/no-payment
  - `python scripts_tbm_workorder_loopback_http.py` → `CCTV_WORKORDER_REAL_LOOPBACK_HTTP_PASS`，模擬狀態最終為 `SIMULATED_ACCEPTED`（非真實驗收）
  - `python scripts_m1cb_session_socket_smoke.py` → `M1CB_REAL_SOCKET_PASS`
  - 來源 AST 解析完成，無 `exec()` 呼叫；**此檢查不能代表安全掃描或依賴/CVE 審查。**
- 非零警告：`StarletteDeprecationWarning`（httpx/testclient）；GitHub runner 提醒 `actions/checkout@v4`、`setup-python@v5` Node.js 20 已棄用、被強制使用 Node.js 24；另有 Node API deprecation。CI 此次成功但不能標記「完全零警告」，後續需安排相容性/版本治理。
- 不可過度宣稱：這個 Run 是 GitHub-hosted 乾淨 Runner 的 **synthetic test/HTTP** 成功；**不是獨立人工 Reviewer、真實客戶、真實身份、完整前端 React E2E、實機工程驗收、實際收付款**。
- 本輪對 G3 階段更新：`G3_CI_PASS_SCOPED`（限上述 SHA 與來源），不是 `G4_CANONICAL_INTEGRATION_PASS`。

## 2. 真正現有系統與 canonical 缺口（已觀察 vs 需要證據）

| 領域 | 目前 Repo / Drive 真實可驗證內容 | 正式 canonical contract 下一步必要條件 |
|---|---|---|
| Identity | `app.py` 以本機合成 bootstrap token / `staging_sessions.py` 短效 token 綁定測試 actor | 取得正式 Business OS 可驗證登入主體、發行者、受眾、撤銷、有效期及非測試憑證的 `subject_id`；不可直接套用 LINE 單人白名單 |
| Tenant/RBAC | staging actor 名稱與客戶案主比對，跨帳號 404、錯角色 403，SQLite 無 tenant policy | 權威 Tenant/Member/Role/Permission domain + database RLS 或等價 server-side 隔離測試，包含跨 tenant 403/404、撤銷後拒絕；未找到已被核准之多租戶正式 schema |
| CustomerRequest/Quote | `requests`／`quotes` SQLite demo 表；CCTV 在台南可透過 HTTP 模擬 | 正式 request/quote canonical ID、tenant_id、author_id、審核/同意版本、時間與寫入稽核；不得讓 demo DB 成第二主庫 |
| WorkOrder | `workorder_demo.py` staging_workorders、staging_workorder_events，僅 opt-in synthetic | 正式 work_order_id、tenant_id、request_id、selected_quote_id、服務範圍與施工方資格、狀態機、冪等鎖、併發與事件不變性；可逆狀態不可誤記已履約 |
| Evidence | demo 只收 `synthetic:...` 字串，非照片／文件本人同意或來源驗真 | 正式 evidence_id、source_hash、content_type、owner/subject、consent_version、授權範圍、簽收時間、storage_ref、保留/刪除政策、惡意檔案掃描，簽名與驗真證據 |
| Acceptance | `SIMULATED_ACCEPTED` 只由測試客戶選擇，無合約/現場/身分證明 | 正式 acceptance_id、acceptor_subject_id、work_order_version、accepted_scope、timestamp、可復核/異議/保固、審核證據與有效授權；禁止自動轉正 |
| Audit/Finance | staging_audit 記錄路由模板與合成 actor；`payments_enabled=false` | 正式不可竄改事件鏈、tenant scope、證據生命週期；發票/匯款/對帳前 Finance 與交易收款狀態一律 `NOT_AVAILABLE` |

以上右欄為 **PROPOSED_REQUIRED_FIELDS / NOT_AUTHORITY_CONFIRMED**，不是聲稱 Business OS 正式資料庫已有這些欄位。現有 Business OS Drive PRD 屬規劃；本次 GitHub repo、Drive 唯讀探索沒有發現經 Owner 核准的可供公共多租戶工程系統接用之正式 Identity/Tenant/RBAC/WorkOrder/Acceptance schema 或 Runtime 端點。

## 3. 第一階段唯讀 Adapter 合約（提議，不授權接線）

- 只能在**明示核准的合成 Staging** 執行，輸入為具 `source_type=synthetic_staging`、`tenant_ref`、`actor_ref`、`request_ref`、`quote_ref`、`workorder_ref` 及可驗證 `consent_evidence_ref` / `moderation_evidence_ref` 的受控映射；真正欄位名須以 canonical schema 為準。
- 輸出只能是 `REVIEW_ONLY`、`executable=false`、`financial_status=NOT_AVAILABLE`，不得直接寫 Production、發邀請、寄訊息、建立正式合約、收款或標記履約。
- 使用現有 `g2_projection.assert_live_sync_enabled()` 的 fail-closed 原則；取得**簽署/可驗證的同意與審核 evidence** 前不可把 `evidence:` 字串視為真。
- 風險測試：跨租戶、跨角色、撤銷/過期 session、重複工單/驗收、遺失照片權利、合約/報價版本漂移、重播/亂序事件、非法付款狀態，任何一項不通過即拒絕同步。
- 需求設計不可引入新的付費服務、外部憑證或持久性第二資料庫；正式環境 Gate 明確關閉。

## 4. 尚需「獨立 Reviewer」的可檢核清單

1. 與本次作者**不同的人或獨立核准的審查主體**，使用 GitHub PR #1 固定 SHA 核對源碼、測試覆蓋、actions 權限、相依套件與授權／CVE。
2. 在乾淨 Runner 的 CI logs 驗證 59/59、3 subtests、兩種 loopback smoke，以及警告與 Node upgrade 升級計畫。
3. 審核 `workorder_demo.py` 的跨租戶、併發建立/狀態轉換、rework、證據引用濫用、日誌去識別、付款隔離；確認 `SIMULATED_ACCEPTED` 絕不能升成正式 `ACCEPTED`。
4. 對接 canonical 前提供可追溯的正式 schema／OpenAPI、Owner 核准的 read-only 入口和最小授權及變更稽核，否則保持 `CANONICAL_RUNTIME_BLOCKED`。
5. 審查紀錄須保存 Reviewer 身份（可匿名化 ID）、日期、commit、Run ID、檢查清單、缺失、獨立 verdict；**本文件沒有真實 Reviewer 簽核，`INDEPENDENT_REVIEW_NOT_RUN`**。

## 5. Gate 與變更歷史

`G3_CI_PASS_SCOPED / G4_CANONICAL_SCHEMA_UNVERIFIED / G4_CANONICAL_RUNTIME_BLOCKED / INDEPENDENT_REVIEW_NOT_RUN / TBM_PAID_JOIN_HOLD / OWNER_GATE_CLOSED`

- 2026-11-02 v0.1：於既有 Draft 分支新增最小 GitHub Actions CI，確認第一次真正 clean Runner Run #41380419911 success，並留下 Business OS canonical 對接契約與 Reviewer Checklist。
- 本輪沒有正式登入、商戶身分、Public 會員、金流、LINE、AI Gateway、三台主機或 Production 操作，也不新增付費 API。Owner 核准前不得 merge/deploy/外聯。
