# CloudLink Staging-only Matching API v0.1

## 目的／現況
- 舊 `yuntech-prototype` 只有前端，本 POC 用 FastAPI＋SQLite 示範 **發案→後台審查→工程師報價→客戶選擇**。
- **本機隔離測試 3/3 PASS**（2026-10-31，`python -m pytest -q`），**Production FAIL / STAGING_NOT_DEPLOYED**。Google Sheets 雙平台戰情表僅是資料追蹤，**並未連接本 API**。
- 完全不含銀行帳戶、訂金、平台抽成、收款、退款、使用者真實身分、工程師資格核驗或 LINE 推播；`/health` 的 `payments_enabled:false` 不等於資安通過。
- 資料為隔離測試環境的假資料；請勿放任何真實客戶姓名/電話/地址/金鑰。
- **不可對外開放**：範例 token 只是單客戶/單師傅/單審核員的測試 stub，未提供 OAuth/SSO、多租戶隔離、RLS、正式稽核、配額限制、備份或資安掃描。

## 最小重現
```bash
cd pocs/cloudlink-staging-api
python -m pip install -r requirements.txt
python -m pytest -q
# 僅在本機自行設定 3 組彼此不同的 20 字以上亂數 token，勿提交儲存庫
export XY_ALLOW_DEMO_API=1
export XY_DEMO_CUSTOMER_TOKEN='<unique-local-only-long-token>'
export XY_DEMO_CONTRACTOR_TOKEN='<unique-local-only-long-token>'
export XY_DEMO_REVIEWER_TOKEN='<unique-local-only-long-token>'
export XY_DEMO_DB_PATH=/tmp/xy_cloudlink_local_only.sqlite
uvicorn app:create_app --factory --host 127.0.0.1 --port 8765
```
API docs: `http://127.0.0.1:8765/docs` (local only). `Authorization: Bearer <token>`，三種測試角色權限分離。

## 已測
1. 未登入 401、工程師不能替客戶發案 403；發案之後 PENDING。
2. 未審核不可報價 409；Reviewer 核准才可顯示和報價。
3. 客戶選擇後不得第二次選擇 409；錯誤角色不可閱讀報價。
4. 拒絕案不可報價、負價被驗證拒絕、未開啟 demo flag 拒絕啟動。

## Gate
- 下一步：將 `CloudLink` React 前端表單對齊 API contract，加入真正 Identity/多租戶、證據審核/通知/排程、SQLite→既有可隔離 PostgreSQL 方案，以及工程師驗證；先做獨立 staging UAT。
- **不合併、不部署、不實際收款、不自動通知。** Reviewer 與 Owner 必須分別核准。
- GitHub Issue #10／#3；千萬營收母件 Issue #5。
