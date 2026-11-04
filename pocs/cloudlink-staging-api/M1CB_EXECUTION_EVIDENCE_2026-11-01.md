# 小雲 YC Tech Match｜M1c-B 執行驗收證據（2026-11-01）

## 階段目標
基於 M1c-A 多客戶合成身份，建立**預設停用的隔離短效 session、明確撤銷與最小化 audit**，避免長期示範權杖被當作業務 API 憑證。

## 本輪實測
- 前一階段基線 `python -m pytest -q`：25/25 PASS。
- 本輪 `python -m pytest -q`：**30/30 PASS**（隔離環境，本機）。
- `python scripts_m1cb_session_socket_smoke.py`：**M1CB_REAL_SOCKET_PASS**（真正 127.0.0.1 TCP/HTTP＋SQLite）。
- 測試情況：核發、到期拒絕、重啟持續有效、撤銷立即失效、bootstrap 無法直接存取業務 API、角色限定稽核、稽核去除 token/body/URL UUID、TTL 無效時拒絕啟動。
- **GitHub Actions CI：NOT_VERIFIED；原始 CloudLink React 全頁瀏覽器 E2E：NOT_RUN。**

## 隔離設定與保護
- 必須額外設定 `XY_STAGING_SESSIONS=1`；TTL 5–900 秒，預設 600 秒。
- `POST /staging/session`：以現有*合成* bootstrap Bearer 換隨機短效憑證，業務 API 需短效 Bearer。
- `POST /staging/session/revoke`：撤銷目前 session。
- `GET /staging/audit`：只允許 reviewer 測試身份；只保存時間、合成 actor、HTTP method、路由模板、狀態碼。
- SQLite 只保存高熵隨機 token 的 SHA-256 摘要、到期與撤銷時間；不保存原始 token、請求 body 或真實客戶資訊。
- 不設定 `XY_STAGING_SESSIONS` 時，維持先前 demo 相容模式；不代表正式 IAM 已安全。
- 無任何真實客戶、工程商身份驗證、支付/錢包、正式部署、修改 LINE、額外付費 API。

## 仍未完成的 Gate
- 原始 React 介面尚未改用短效 session；真實 IAM/SSO/MFA、租戶資料庫 RLS、登入防暴力破解/限流、傳輸 TLS、備份/還原、稽核隱私保留策略、工程商資格審核、正式瀏覽器 E2E、安全審查均 `NOT_VERIFIED`。
- 兩個 PR 維持 Draft，不合併，不發布，不收款；Owner Gate CLOSED。
- 商業目標年營收 1,000 萬元未產生本輪真實商機/收款證據，財務達成率仍需 CFO 對帳。
