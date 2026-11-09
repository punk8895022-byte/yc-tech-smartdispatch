# YC Tech Match｜G2 來源收斂 × 欄位契約驗證｜2026-11-01 v0.1

Status: G2_SOURCE_RECONCILED / G2_PROJECTION_LOCAL_PASS_SCOPED / CANONICAL_RUNTIME_NOT_CONNECTED / OWNER_GATE_CLOSED.

## 決策：共用一條工程實作主線，勿再建第四個原型

- **現有較成熟的隔離 API/SQLite/三角色路徑**：本 repo 的 [Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1)，路徑 `pocs/cloudlink-staging-api/`。已可核對 `app.py`、`legacy_schema.py`、M1c 測試與 loopback 腳本，仍非 Production。
- **舊 CloudLink 真正 React 發案 handler**：[yuntech-prototype Draft PR #1](https://github.com/punk8895022-byte/yuntech-prototype/pull/1)。其餘舊版密碼、假錢包、CDN/Babel 仍存在，整頁不得公開。
- **較早的獨立派工/離線 policy repo**：[yc-tech-smartdispatch-1 Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch-1/pull/1)。本輪將該 PR 的兩個安全契約與測試檔，**逐位文字讀回一致**重用到本 repo 的 `pocs/cloudlink-staging-api/`。保留原 PR 供差異追蹤，不直接合併兩個專案或搬正式資料庫。
- **規劃層 Business OS**：[小雲 Business OS PRD](https://docs.google.com/document/d/1otVSuymPm7JBoJsSZSvBBK9b0jo6LsREL3zbBQ8h838/edit)、[雙平台權威 PRD](https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit)。目前為設計契約，不代表已有可用獨立平台 API/主資料庫。
- **個人 LINE AI OS**：`punk8895022-byte/xiaoyun-ai-os` 具有私人 LINE 單人白名單的 User/Task 模型。不得直接充當公開平台多租戶 Identity/Customer 主資料。

## 實際實作與權威域對照

| Business OS 擬用領域 | 已核對實際程式 | G2 邊界／缺口 |
| --- | --- | --- |
| Identity/Tenant/RBAC | `app.py` 環境變數演示 Bearer tokens + customer/contractor/reviewer actor | 不是真實登入；沒有 tenant claim、正式租戶隔離、撤銷/登入會話或 DB RLS；**BLOCKED** |
| Customer/Opportunity/Request | SQLite `requests`: id/customer/category/region/description/state/selected_quote | 只是 POC 的主資料，不能成為 Business OS canonical；正式 consent/Evidence 不在 schema 中，**BLOCKED** |
| Service taxonomy | `NewRequest.Category = network/cctv/access`、Legacy: net/cctv/access | 本輪僅 P0 台南 CCTV、Wi-Fi 簽入只讀 projection；**NAS 目前未實作**，不得向客戶開放 |
| Contractor/Qualification | demo actor token；`quotes.contractor` | 身分、技術資格、地區服務覆蓋、保險沒有 verified registry；不可標認證或自動邀請 |
| Quote/Approval/Contract | `quotes.price_ntd/scope`、`SELECTED` 客戶選報價 | 無正式 Owner price approval、合同版本、履約證據；不能標成交 |
| WorkOrder/Acceptance | 無有證據的真實後端履約／驗收狀態機 | G3 待設計，不能宣稱本輪已實作 |
| Fee/Finance/Settlement | `/health` 回 `payments_enabled:false` | 無付款、發票、銀行對帳。費率只是離線試算，不保管工程全額款項 |
| Audit/Evidence | staging request/quote 現況未有 server-side immutable audit ledger | 事件可追蹤與權限寫入未接 Business OS，**BLOCKED** |
| Public Portfolio | `marketplace_contract.py` 提供純函數發佈 Gate | 尚未接實際資料、客戶授權、照片去識別及公開頁面，**NOT_RUN** |

## 本輪新增技術切片（不碰正式 API）

1. `pocs/cloudlink-staging-api/marketplace_contract.py`、`tests/test_marketplace_contract.py`：移入既有作品授權、合格候選、平台費試算及對帳 policy；完整原始來源可交叉核對。
2. `pocs/cloudlink-staging-api/g2_projection.py`：只讀 `requests` 到提案審查 DTO 的純函數；必需獨立客戶同意與 moderation evidence；CCTV/network 映射；地區只允許台南；NAS/access/外縣市 fail-closed。產出永遠 `REVIEW_ONLY`、`executable=False`。
3. `tests/test_g2_projection.py`：12 項 synthetic positive/negative 檢核：類別、地區、審核、同意證據、無資料、live-sync 永遠拒絕。
4. **Runtime 仍斷開**：`assert_live_sync_enabled()` 無論傳入什麼旗標都拒絕。禁止把偽造 `evidence:...` 字串視為合法有效的客戶同意證據；該工具只測欄位結構與缺值拒絕，不驗證真實簽署或 tenant IAM。
5. 本次未修改 `app.py` 的任何路由與 DB schema，故「policy 已存在」不等於「API 已強制採用」。

## Gate 與測試證據

- 先前在本地 ZIP 針對 `marketplace_contract.py`、`pilot_flow.py` 執行 `unittest` 25/25 PASS，仍非 GitHub Actions 或正式 API 測試。本輪在獨立本地檔案對新 `g2_projection.py` 執行 12/12 PASS，GitHub 原始檔各自讀回比對一致。
- 兩個被重用的 policy 檔自 `yc-tech-smartdispatch-1` 讀取並逐位文字比對，GitHub 目標檔讀回 2/2 一致。
- 從本 repo 的 `pocs/cloudlink-staging-api` 執行：`python -m pytest -q tests/test_marketplace_contract.py tests/test_g2_projection.py`。此命令為下一步可重現 CI 所需；**本次尚無 GitHub Actions Run ID**，不可宣稱該 checkout 已全套 PASS。
- 原 M1c 多 actor 25/25 PASS 為此前 Drive/local 實驗紀錄；本次未重新做具正式 IAM 的 E2E、未開外網或連三台主機。

## G2 完成定義與阻塞

- **本輪達成**：G2_SOURCE_RECONCILED 與 G2_STATIC_PROJECTION_PASS_SCOPED；重用現有 source，沒有另建重複資料庫。
- **尚未達成**：G2_CANONICAL_RUNTIME PASS。必要 Evidence：真正 Business OS 的原始碼位置、版本化 schema、Identity/Tenant/RBAC 驗證、同意證據驗真、審核 Audit 交易、費用與支付資料界線、跨租戶 403/404 與回歸測試。
- **安全規則**：未核實的 Core 端點或身份不得透過本地純函數解鎖。Owner Gate CLOSED，PR 保留 Draft，不 merge、不 deploy、不外聯、不收款、不上架。
- **下一個可執行技術關卡**：取得 Core canonical 的 read-only schema/interface，建立在受控 staging 的 adapter（只合成資料），用 1 筆 CCTV 案件驗證 requester/reviewer/contractor/Owner/RBAC/audit，才考慮設計 G3 真實流程。

## 變更
2026-11-01 v0.1：以成熟的 POC 分支為技術整合主線；對照其他兩個 repo，去重並交付 2 個 policy 檔及 2 個 G2 projection 檔／測試。原 PR、所有 production/開發環境不刪不動。
