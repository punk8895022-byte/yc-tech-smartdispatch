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
