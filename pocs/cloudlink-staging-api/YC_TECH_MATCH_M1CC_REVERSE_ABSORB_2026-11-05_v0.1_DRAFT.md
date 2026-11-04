# YC Tech Match × 小雲 AI OS｜反向工程吸收／M1c-C｜2026-11-05 v0.1 DRAFT
**狀態**：`REACT_HANDLER_UNIT_PASS` ／ `ORIGINAL_REACT_BROWSER_E2E_NOT_RUN` ／ `GITHUB_CI_NOT_VERIFIED` ／ `OWNER_GATE_CLOSED`

## 實際逆向驗證
- 原 CloudLink `ClientCreateJob` [舊分支 Draft PR #1](https://github.com/punk8895022-byte/yuntech-prototype/pull/1) 原先直接把長效 demo 測試 Bearer 傳至 `POST /legacy/requests`，但新 FastAPI `XY_STAGING_SESSIONS=1` 會要求短效 token，因此前後端存在真實的 401 介接斷點。
- 已在舊專案 feature 分支同步修改**實際執行** `index.html` 和對照 `app.jsx`，由 `POST /staging/session` 換短效 session → POST /legacy/requests → finally `POST /staging/session/revoke`。功能旗標只容許 loopback + /legacy-react，虛構縣市、合法網路/監控/門禁分類；移除該提交路徑假錢包及付款暗示。
- 安全輸入：提交鎖避免同次雙點重複建案；bootstrap 權杖從表單立即清除；短效 token 只在局部記憶體、不存 localStorage；失敗也嘗試撤銷，撤銷失敗不顯示完整成功。
- 實際以 GitHub connector 讀回 **兩份來源同一份 handler**，在隔離 V8 直接執行原始 handler 進行 **11/11 邏輯 PASS**，包括 session 交換、業務短效 token、成功、401、提交失敗仍撤銷、撤銷 500、flag 關閉、非法分類、真實街道地址拒絕、同時送件鎖及釋放。
- 新增可重跑 [原 React Node 測試](https://github.com/punk8895022-byte/yuntech-prototype/blob/feature/cloudlink-m1b-react-api-20261031/tests/m1cc_legacy_session_flow.test.mjs)，以及此 Repo 的 [FastAPI short-session legacy contract 測試](pocs/cloudlink-staging-api/tests/test_m1cc_react_legacy_session_contract.py)，但這兩個 repo 版本**尚未取得 GitHub CI 通過證據**。本輪 11/11 是直接 handler 沙盒檢驗，不是原始 React 整頁 Chromium E2E。
- GitHub 目前另含 [CCTV 工單合成狀態機](pocs/cloudlink-staging-api/workorder_demo.py)，資料狀態為 `ASSIGNED→SUBMITTED_FOR_REVIEW↔REWORK_REQUESTED→SIMULATED_ACCEPTED`，只接受 `synthetic:` 假資料，不可代表正式施工驗收、可認列收入。

## 吸收到小雲 AI OS 的分界
已在 [小雲 AI OS 獨立 Draft PR #35](https://github.com/punk8895022-byte/xiaoyun-ai-os/pull/35) 建立**RESEARCH_ONLY** 研究契約，映射「短效可撤銷能力」「跨帳號 Scope」「Reviewer/Owner Gate」「Evidence 分類」「metadata-only audit」到現有 Agent Registry / Task Ledger 方向。**沒有移植 Demo Token/SQLite、沒有修改正式 LINE/Calendar/AI OS 程式或資料庫，也沒有新增管理平台**。

## 風險與下一關
1. 原始 React 依賴瀏覽器 CDN/Babel，整頁 UI 還沒有真實 Chromium/手機跨角色網路 E2E；故 `STAGING_UAT=BLOCKED`。
2. Demo bootstrap 暫未限制頻率及防暴力破解，長期權杖仍存在；原版其他 localStorage 明文帳號/假金融入口未解決。新提交功能只是隔離頁專用，不是正式身分平台。
3. 正式 Auth/SSO/MFA、租戶資料庫級 RLS、工程師真實資格、資料留存、金流、合約、人工客服和法律審查皆未驗證。
4. 下一關應先將原始 React 以無外部 CDN 的隔離構建方式完成真實 browser E2E，然後才進入 IAM/tenancy 安全方案 Review；**不得直接把模擬驗收映射為 10M 商機／收款**。

## Gate 與追蹤
原 [YC Tech Match Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1)、[CloudLink React Draft PR #1](https://github.com/punk8895022-byte/yuntech-prototype/pull/1) 及 [AI OS Research Draft PR #35](https://github.com/punk8895022-byte/xiaoyun-ai-os/pull/35) **全部未合併**。Owner Gate CLOSED；程式不接受真實客戶資料、不啟用 Production/LINE/金流、不新增付費 API。Google Drive 舊版 10M 執行證據以同一主文件增量更新。
