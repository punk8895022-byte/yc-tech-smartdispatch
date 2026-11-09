# YC Tech Match｜台南 CCTV 真正 Loopback HTTP＋工單模擬驗收｜2026-11-02 v0.1

- **狀態**：`G3_LOCAL_REAL_HTTP_PASS_SCOPED / G3_SYNTHETIC_WORKORDER_HTTP_PASS_SCOPED / CANONICAL_RUNTIME_BLOCKED / OWNER_GATE_CLOSED`
- **範圍**：沿用既有 `pocs/cloudlink-staging-api` FastAPI + SQLite、`staging_sessions.py`；不新建正式 Business OS 主資料庫、不註冊 TBM、不新增付費 API。
- **來源 PR**：[Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1)，基礎分支 `feature/asset-os-dual-platforms-20261031`（非 main）。
- **限制**：所有內容為虛構 CCTV、短效合成身份與 SQLite 隔離資料；不得上 Production、公開登入、接真實案主或視為工程驗收、合同、付款證據。

## 一、完成的技術切片

1. 在本輪隔離執行容器，由 GitHub 以 Blob SHA-1 驗證 23 份既有原始碼一致，再執行當時全套 `python -m pytest -q`：**55 passed，3 subtests passed**。
2. 新增 `scripts_tbm_cctv_loopback_http.py`：**真實 127.0.0.1 TCP/HTTP** 進行合成 CCTV request→moderate→quote→select，含短效 session、失敗權限/跨租戶 404、SQLite SELECTED 持久讀回、精簡 audit 去識別、payment false；輸出 `CCTV_REAL_LOOPBACK_HTTP_PASS`。
3. TDD 先寫 `tests/test_workorder_demo.py`，確認 opt-in 新 API 未實作時有 **3 failing tests、1 passing baseline**，再新增 `workorder_demo.py` 與 `app.py` opt-in 接線。驗收：新增測試 **4 passed**、完整現有測試 **59 passed，3 subtests passed**。
4. 新增 `scripts_tbm_workorder_loopback_http.py`：**真實 127.0.0.1 TCP/HTTP** 執行合成 CCTV 工單：
`ASSIGNED → SUBMITTED_FOR_REVIEW → REWORK_REQUESTED → SUBMITTED_FOR_REVIEW → SIMULATED_ACCEPTED`；驗證 SQLite 持久、HTTP 403 拒絕錯角色、審核紀錄去識別、付款未啟用；輸出 `CCTV_WORKORDER_REAL_LOOPBACK_HTTP_PASS`。
5. 所有新增／修改五份程式與隔離容器已測原始碼之 Git Blob SHA-1 讀回完全一致，測試無需新安裝相依套件。

## 二、工作單 API（**預設關閉**）

需同時具備 `XY_ALLOW_DEMO_API=1`、`XY_STAGING_SESSIONS=1`、`XY_ENABLE_WORKORDER_DEMO=1`，合成 20+ 字元測試 token、明確存在的 SQLite 絕對路徑；僅 `127.0.0.1` 或 `::1` 可連入。

| 方法／路徑 | 角色與條件 | 結果 |
| --- | --- | --- |
| `POST /staging/workorders` | 客戶持有已審核＋已選報價的**台南 CCTV** 案件 | 建立 `ASSIGNED`，相同案件重覆 409 |
| `GET /staging/workorders/{id}` | 該案件客戶或獲選承包人 | 僅回傳模擬狀態及 `synthetic:` 參照 |
| `POST /staging/workorders/{id}/complete` | 獲選承包人；`ASSIGNED`／`REWORK_REQUESTED` | 回 `SUBMITTED_FOR_REVIEW` |
| `POST /staging/workorders/{id}/decide` | 案件客戶；`SUBMITTED_FOR_REVIEW` | `REQUEST_REWORK` 或 `SIMULATED_ACCEPTED` |
| `GET /staging/workorders/{id}/events` | 當事客戶／承包人 | 僅事件類型、合成 actor 與時間戳，不回傳照片、token、報價 |

- Evidence 僅接受格式 `synthetic:[a-z0-9-]{...}`，不是實際文件／影像授權驗證；非合規完成證據。
- 不支援 NAS 或台南以外、未選報價或未審核案件；跨帳號回 404，錯角色回 403，不合法輸入回 422、非法狀態轉移回 409。
- `/health` 維持 `payments_enabled:false`；沒有付款、發票、放款、簽約、退款、平台抽成交易。
- 工單驗收欄位刻意使用 **`SIMULATED_ACCEPTED`** 而不是商用 `ACCEPTED`，杜絕將示範視作客戶正式簽收。

## 三、重跑指令與驗證證據

```bash
cd pocs/cloudlink-staging-api
# 使用既有 requirements.txt 相依；隔離環境才能啟動，不得使用正式 token。
python -m pytest -q
python scripts_tbm_cctv_loopback_http.py
python scripts_tbm_workorder_loopback_http.py
```

本輪隔離容器結果（2026-11-02）：
- `GITHUB_SOURCE_PARITY_PASS 23 files`（初始原始碼快照）
- `55 passed, 3 subtests passed`（功能修改前 baseline）
- `3 failed, 1 passed`（TDD RED：新工單路由不存在／無 session guard）
- `4 passed`（新工單測試 TDD GREEN）
- `59 passed, 3 subtests passed`（完整 pytest）
- `CCTV_REAL_LOOPBACK_HTTP_PASS`
- `CCTV_WORKORDER_REAL_LOOPBACK_HTTP_PASS`
- 提交後五份源檔讀回 Git Blob SHA-1 全數一致。

## 四、剩餘阻塞

- 本輪只驗證 **本機 HTTP / Uvicorn / SQLite / 虛構角色**，沒有在 GitHub Actions Runner 或原版 React 全頁瀏覽器執行新功能。
- `workorder_demo.py` 為**新隔離 POC 狀態機**，不是正式 Business OS 的 WorkOrder/Acceptance 契約、正式 Identity/Tenant/RBAC/DB RLS 或真實工程商資格核驗。
- `staging_audit` 紀錄為示意事件，不是不可竄改的正式稽核帳本；缺真正附件簽名、審核鏈與保固、工安法規/契約條款、通知及費用對帳。
- 尚無獨立 Reviewer / Owner UAT、正式壓測、安全測試、遷移、應用端 RBAC/日誌保留控制、現場照片授權驗證。
- **正式 PR 仍 Draft、不得合併、部署或啟用金流；TBM 加入／付費 HOLD**。

## 五、下一 Gate

1. Reviewer 再次於 GitHub checkout/CI 隔離 runner 依此文件重跑，記錄 Run ID、測試版本、失敗與 Log redaction；沒有 CI Run ID 不標 `CI_PASS`。
2. 核對 Business OS canonical Identity/Tenant/RBAC、WorkOrder/Acceptance/Evidence/Audit 真正 schema；設計 staging adapter，未核對之前不可將此 POC 當正式 service。
3. 以手機瀏覽器完成原 React 端到端操作、正式權限/資料保護測試，Owner 一次性審查；Owner Gate 未核准，不公開、接客戶、收費。

**變更紀錄**：2026-11-02 v0.1 新增真實 localhost HTTP CCTV 驗收和工單示意後端；`supersedes` 前次文件中「HTTP 尚未跑」的**本地執行狀態**，不改動正式 Runtime HOLD 結論。
