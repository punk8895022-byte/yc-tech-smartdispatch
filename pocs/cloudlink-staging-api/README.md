# CloudLink × YC Tech Match｜隔離媒合前後端 v0.2

**目前關卡：M1a LOCAL_INTERACTIVE_FLOW_PASS（2026-10-31）**。不代表 M1 完成、合約交易已成立、正式上線或真實身分/安全驗證通過。

## 真正已實作
- 沿用先前同一份 FastAPI + SQLite 隔離原型，新增 `GET /my/requests`（客戶自己的案件）及 `GET /review/requests`（審核員待審案件）。
- 新增與 API 同源的 `/demo` 前端及 `/ui/*` 靜態資源：客戶建立示範需求 → 審核員核准／退回 → 工程師報價 → 客戶選擇報價。
- 所有輸入必須是虛構資料；同一資料庫重新開啟 API／重新渲染畫面後仍可讀回案件與選擇狀態。
- `web/app.js` 不用 localStorage/sessionStorage 保存認證資訊；測試權杖只存在瀏覽器暫存記憶體內（切換角色時各有測試欄位）。**這不是正式登入**。
- `/health` 返回 `payments_enabled: false`，無金流、電子錢包、訂金與請款 API。

## 開啟本機示範
```bash
cd pocs/cloudlink-staging-api
python -m pip install -r requirements.txt
# 在你的本機終端先設定三組互異、長度 >= 20 的測試權杖；不得進 git。
export XY_ALLOW_DEMO_API=1
export XY_DEMO_CUSTOMER_TOKEN='<random-local-customer-token>'
export XY_DEMO_CONTRACTOR_TOKEN='<random-local-contractor-token>'
export XY_DEMO_REVIEWER_TOKEN='<random-local-reviewer-token>'
export XY_DEMO_DB_PATH=/tmp/xy_cloudlink_isolated_demo.sqlite
uvicorn app:create_app --factory --host 127.0.0.1 --port 8765
```
- 僅在自己的電腦開 `http://127.0.0.1:8765/demo`，依角色輸入該角色的本機測試權杖，先發案、再核准、再報價、最後由客戶選擇。
- 不允許 `0.0.0.0`、公網、隧道、真實客戶資料、正式平台登入資料、公司機密或真實銀行金流；無 HTTPS/SSO/限流／存取審計。
- 若未設定 `XY_ALLOW_DEMO_API=1` 與正確測試權杖，API 預設拒絕啟動。

## 實測與誠實界線
- 在隔離工作區執行 `python -m pytest -q`：**5/5 PASS**，測試涵蓋完整流程、401/403/409/422、待審核隱藏、資料持久、同源 UI 資源。
- Chromium 手機寬 390px 的三角色互動測試已於本機隔離執行通過（經 ASGI TestClient 橋接到真實 API＋SQLite），包含跨角色發案/審查/報價/選擇、重新掛載後資料讀回、無水平溢出。
- **執行環境禁止 Chromium 連線到本機 TCP / HTTP 頁面**，故瀏覽器互動使用 in-process ASGI fetch bridge。它**不是**正式 HTTP 網路瀏覽器 E2E、也不是原本 `yuntech-prototype` 的 React 前端對接測試。
- `scripts_browser_e2e.py` 附可重跑的同類別測試程式；執行需額外 `pip install playwright` 與 `playwright install chromium`（請先核准依賴來源），不納入基本 `requirements.txt`。
- **GitHub Actions CI：NOT_VERIFIED；真實跨裝置 UAT：NOT_RUN；Production：BLOCKED。**
- 與原 CloudLink 單檔 React 前端尚未融合；本輪先交付可驗證的薄前台、不是重新上線原平台。

## 下一步（下一道 Gate M1b）
1. 在隔離分支對接舊 `yuntech-prototype` React 發案/報價表單，不保留原明文密碼/假錢包。
2. 正式 Identity／tenant RBAC、工程師資格與業主隱私、資料庫遷移/備份、審核稽核與冪等。
3. 經獨立 Reviewer 測試/Owner 核准後，才可進入實際 staging；不得自行上 Production。

相關：[GitHub Issue #3](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/3)、[Issue #10](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/10)、[10M War Room](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/5)。

## 版本
- v0.1：FastAPI / SQLite 純 API 示範。
- v0.2 2026-10-31：同源可操作前端、角色清單查詢、五項測試與三角色 Chromium 隔離實驗；所有正式 Gate 仍關閉。

## M1b-B：真正原版 React 發案處理器整合（2026-10-31）
- **原版來源**：`punk8895022-byte/yuntech-prototype` 的 [Draft PR #1](https://github.com/punk8895022-byte/yuntech-prototype/pull/1)，在獨立分支修改實際執行的 `index.html` 及對照 `app.jsx` 內 `ClientCreateJob.handleSubmit`，取消該路徑瀏覽器錢包扣款與假付款提示，改送 `POST /legacy/requests`。
- **安全**：原本 `master` 完全不變；新發案路徑只有本機 `/legacy-react` 且 `XY_ALLOW_LEGACY_REACT=1`、`XY_CLOUDLINK_LEGACY_HTML_PATH` 指向**下載自上述 feature 分支的 index.html 絕對路徑**才會開啟。需手動在表單輸入臨時 customer 測試 token；不儲存權杖。原始舊登入/其他假錢包仍存在，整頁不得對外公開。
- **運作**：在執行本文前面的必要環境變數後加上兩項（請勿放真實客戶資料）：
```bash
export XY_ALLOW_LEGACY_REACT=1
export XY_CLOUDLINK_LEGACY_HTML_PATH=/absolute/path/to/modified-yuntech-prototype/index.html
# 限定 loopback：uvicorn app:create_app --factory --host 127.0.0.1 --port 8765
# /legacy-react 原始 React UI（需可載入 React/CDN，僅供隔離驗證）
```
- **驗收**：`python -m pytest -q` 本機 **18/18 PASS**；`python scripts_realtime_loopback_smoke.py` 實際 localhost TCP/HTTP 連線跨角色全流程 PASS；原 M1b Chromium 390px 相容表單 DOM/API/SQLite PASS（瀏覽器 fetch bridge）。**注意：原始 React 完整頁面 Chromium E2E NOT_RUN，因外部 CDN/localhost 的隔離限制。**
- **剩餘風險**：真實 IAM/多租戶、工程商資格、現場履約、法律金流、用戶資安、原始整頁其他示範付款尚未修正；本地測試不能作 Production 依據。

## M1c-A｜多客戶／多工程師權限隔離（2026-11-01）

**修復的真實阻塞：** GitHub 的 `tests/test_workflow.py` 曾有一行未閉合 `assert`（語法錯誤）；已在本分支修復。故先前 GitHub HEAD 所聲稱的「18/18」不能當 CI 驗證，修正後本機重建測試結果如下。

- **新增 `XY_DEMO_ACTORS_JSON` 受控測試配置**：最多 12 組環境變數合成客戶／工程師，明確檢查 ID、身分、互異長權杖；配置無效時拒絕啟動。既有 3 組測試權杖保留向下相容。所有身分都只是 **staging-only**。
- **新增身份歸屬**：客戶案件以 actor ID 儲存；客戶 A 與 B 的 `GET /my/requests` 各自隔離，`GET /requests/{id}/quotes` 與 `POST /quotes/{id}/select` 對他人案回 404。
- **新增工程師自己的報價**：`GET /my/quotes` 按工程師 actor ID 讀取，工程師 B 無法看到工程師 A 的私有報價清單。審核員可審核待審案件，此為設計的角色授權範圍。
- **測試來源**：`tests/test_m1c_identity_isolation.py`（2 客戶×2 工程師，含拒絕錯誤身分、跨客戶/報價、重複選擇）；`scripts_m1c_multi_actor_socket_smoke.py`（真正的本機 TCP/HTTP＋SQLite 寫讀）。
- **實際本機**：在前次已驗證的 M1b 本機包套用與 GitHub 相同的 M1c 變更，`python -m pytest -q` **25/25 PASS**；`python scripts_m1c_multi_actor_socket_smoke.py` **M1C_LOOPBACK_SOCKET_PASS**。
- **重要區分**：這是 M1c-A **LOCAL PASS**，**不是** GitHub Actions CI；此次 GitHub 完整 checkout CI／原始 React 39 萬字整頁瀏覽器 E2E 仍 **NOT_VERIFIED**。無正式 IAM、註冊/帳號管理、撤銷/密碼安全、多租戶資料庫級政策、客服稽核、真實工程師核驗。舊版其他明文 demo 及假金融入口未清理，不可上線。
- **Gate**：Owner APPROVAL CLOSED；兩個 Draft PR 不合併、無 Production／LINE／金流變更，所有資料必須是虛構。下一關 M1c-B 為真實 Identity 設計及隔離 Staging 安全審核。
