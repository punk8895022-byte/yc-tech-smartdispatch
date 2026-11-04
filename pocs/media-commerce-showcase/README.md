# 小雲 Media Commerce｜作品展示 MVP v0.1（2026-11-01）

**狀態：INTERNAL_PREVIEW_ONLY / G3 AUTOMATED_CI_CHROMIUM_PASS_SCOPED / G5 OWNER_GATE_CLOSED / NOT_DEPLOYED**

## 目的與定位
基於現有 [Asset OS 雙平台 PRD](../../docs/YC_DUAL_PLATFORMS_PRD_2026-10-31_v0.1_DRAFT.md) 與既有 Media Commerce 方向新增第一個**純靜態、可本機審核**的展示切片，不建立第二套 CRM、DB、會員、金流或 AI Agent Runtime。本切片放在現有 `yc-tech-smartdispatch` 的獨立 feature branch；**來源 Repo 為公開 Repo**，因此本目錄只存不含 Secrets／PII 的合成資訊與公開適用的內容。

## 一次驗收入口
- [作品列表](index.html)：兩張作品卡與公開狀態說明
- [XY-HD-001 跨 AI 交接工具包](xy-hd-001.html)：功能、限制、原專案離線測試證據摘要
- [CloudLink 智慧派工](cloudlink.html)：合成發案→審核→報價→選擇與實際欠缺功能
- [公開安全的作品 Manifest](projects.json)：兩筆皆明確 `public_approved: false`
- [證據與 Owner 驗收表](evidence/OWNER_REVIEW_2026-11-01_v0.1_DRAFT.md)

## 本機啟動（不需 API／資料庫／安裝前端相依）
在本 Repository 根目錄執行：

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory pocs/media-commerce-showcase
```

然後開啟 `http://127.0.0.1:8765/`，可點入兩個詳情頁。僅在本機 loopback 測試；不要用 `0.0.0.0` 對外開放。

## 離線契約測試
```bash
python3 -m unittest discover -s pocs/media-commerce-showcase/tests -v
```
本分支以 Python stdlib 針對兩頁、索引、Gate、安全邊界、連結完整性、390px breakpoint 與 evidence 狀態執行靜態契約檢查。**這不等於 Chromium 實測或真實外部平台流量／產品 E2E。** 要發布需再執行真實裝置視覺、資安、授權、Owner Gate。

## 素材與資料治理
- 所有 UI 中的 terminal/工單畫面均為 **STATIC_SYNTHETIC**，不是截取真實客戶或實際 Agent。
- 所有 CTA 只在本機作品頁間跳轉，沒有表單、聯絡資訊送出、付款、埋碼、外部腳本、遠端 API。
- 所有 HTML 設 `noindex,nofollow,noarchive`，**但 noindex 不是存取控制；公開 Repo 的檔案可被存取**，不得加入未公開內容。
- XY-HD-001 和 CloudLink 的離線結果引用既有 PR/Drive 紀錄，不冒充新測試。
- Product/CRM/Finance 仍以既有 Business OS canonical domain 為準；`projects.json` 只是本次展示白名單，不是正式主資料。

## 待驗收與變更
- G0：原 Media Commerce 規劃與兩產品來源已唯讀查核；引用證據必須保留版本。
- G1：本切片的展示文案與合成資料已完成，公開 IP 與商業資格 **未放行**。
- G2：靜態程式已提交到隔離分支，待 CI + 真實瀏覽器視覺驗收。
- G3：僅能對完成的靜態／CSS／連結測試標 PASS；真實產品 E2E 不變。
- G4：正式網站/IdeaX 投稿資格 NOT_VERIFIED。
- G5：OWNER_GATE_CLOSED。
- 2026-11-01 v0.1：第一版兩個詳細頁與列表，尚未部署、發文、合併或收費。


## 2026-11-01 G3 自動測試結果
- GitHub Actions [成功 Run #41293584631](https://github.com/punk8895022-byte/yc-tech-smartdispatch/actions/runs/41293584631)，Python 契約 14/14 PASS；Chromium 真實渲染 390px/1280px 共 6/6 PASS。
- [6 張校正中文字型後的截圖 Artifact](https://github.com/punk8895022-byte/yc-tech-smartdispatch/actions/runs/41293584631/artifacts/13078621441)，7 日保留；詳細範圍及修正歷史見 [Owner Evidence](evidence/OWNER_REVIEW_2026-11-01_v0.1_DRAFT.md)。
- 仍缺正式 iPhone Safari/VoiceOver 使用驗證、產品實際 E2E、外部公開授權及 G5 Owner Gate；沒有合併 main 或部署。

## 2026-11-05 v0.2：作品牆黑箱設計模式吸收（IdeaX-inspired）
- [研究及取捨](docs/IDEAX_PATTERN_ADOPTION_2026-11-05_v0.2_DRAFT.md)：分清 IdeaX 截圖可見、公開活動資訊與其它平台比較樣本；官方作品牆投稿/API/費用未驗證。
- 新增首頁「AI 開發效率／資訊工程服務」**主題捷徑**（靜態錨點，不虛稱動態篩選），卡片標示適用對象與測試證據限制。
- `projects.json` 提升為 schema v0.2.0：新增作品問題/受眾/證據、editorial 類別、投稿未完成狀態；不是 CRM/Lead 權威主庫。
- [審核腳本](scripts/release_gate.py) 使用 Python stdlib：`--mode internal` 驗證兩作品、資料/權利/公開 Gate；`--mode packet` 僅輸出內部審核文案；`--mode public` 必定回傳 exit 2 阻止外部公開。腳本**不能**認證 Owner 身分或代替正式部署管控。
- [負測與回歸測試](tests/test_release_gate.py)：覆蓋 fake likes、冒稱外部投稿、路徑穿越、開放追蹤、提前核准、證據缺漏等，GitHub CI 已接入，實際 PASS 以本次 head 的 run 為準。
- 分工不變：Google Drive Asset OS 原 PRD 為唯一產品整合主規格；GitHub PR #12 為程式與驗收證據；正式 Business OS 維持 Product/CRM/Finance 唯一權威來源。
- Gate 不變：`PUBLIC_RELEASE_BLOCKED`、`NOT_SUBMITTED`、`OWNER_GATE_CLOSED`。本輪未部署、未投稿 IdeaX、未新增付費 API 或處理實際客戶資料。
