# Media Commerce 作品展示 MVP｜Owner 一次驗收與證據邊界

版本 2026-11-01 v0.1｜狀態 INTERNAL_REVIEW / DRAFT_ONLY / OWNER_GATE_CLOSED

## 1. 本輪可驗證交付
- 可直接以本機 HTTP 開啟的列表 `index.html`、詳情 `xy-hd-001.html`、`cloudlink.html`。
- 原創 CSS 與合成 HTML 示意，沒有外部 Script/圖片/API/登入/金流，手機 breakpoint 設 790px、390px。
- `projects.json` 列出恰好兩項，`public_approved:false`，`payment_enabled:false`。
- Python stdlib 14 項 contract tests；**在 GitHub CI 真實結果出來前不宣稱 GitHub CI PASS**。
- 內部審核取原專案證據，**不能將本展示頁標為 CloudLink 或 XY-HD-001 的真實 runtime 已驗收**。

## 2. 作品 A｜XY-HD-001（E-XY-001）
- 商品定位與買家預覽：既有 [Draft PR #68](https://github.com/punk8895022-byte/xiaoyun-ai-skills/pull/68)，截至本輪查核 Head `e811573227473d7abc1db2d846d871723c6294cb`；該 Repo 為私有，僅授權者可讀。
- [Business OS PRD](https://docs.google.com/document/d/1otVSuymPm7JBoJsSZSvBBK9b0jo6LsREL3zbBQ8h838/edit) 2026-11-01 附錄記錄：CI Run 41287572640 completed/success，Windows/macOS/Ubuntu 3/3，離線 unittest 58/58，各平台內部 ZIP checksum 一致；另有內部 reviewer package 解包測試。
- 真正 Claude→Codex 雙獨立會話 E2E、買家乾淨安裝、商業授權、KYC/退款、公開販售：NOT_RUN / HOLD / CLOSED。
- UI 的 terminal 為合成畫面，不是這個 CI 或真實 AI 模型執行截圖。

## 3. 作品 B｜CloudLink（E-CL-001）
- [既有工程媒合 Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1)；[原版 React Draft PR #1](https://github.com/punk8895022-byte/yuntech-prototype/pull/1)。
- [10M 執行報告 V3.4](https://docs.google.com/document/d/1J_lTqVI4r1iulZXs0cJyPDMUT3AcE28su7NNs42JkNM/edit) 記錄本機 pytest 18/18 PASS、loopback socket/HTTP 合成資料流程 PASS，以及原版 React handler 接線。
- 原版 React 完整 browser E2E：BLOCKED_NOT_RUN。真實登入、RBAC、多租戶、服務資格、金流與正式部署未通過。
- UI 的工單畫面為合成資料，不是已接真實客戶的派工平台。

## 4. Reviewer Gate 一次驗收清單（未經真人/實機簽核前一律待驗）
- [ ] 390px／桌面實際瀏覽器視覺：無溢位、無裁切、鍵盤與 VoiceOver 能導覽。
- [ ] 點通三頁連結，證據文字與來源日期對得上。
- [ ] Source/PII/Secrets/IP：公開 Repo 不包含機密、真實客資、客戶照片或授權不明素材。
- [ ] 流量／金流／表單：無遠端傳輸與付費入口。
- [ ] Owner 最終核准內容與未來對外品牌；如未核准，維持 Draft。
- [ ] 正式公開、IdeaX 投稿、部署與 merge，另行核准，不在本 PR 執行。

## 5. 此 PR 的精確限制
`STATIC_SHOWCASE_COMPLETE` 僅指兩個 HTML 作品頁與導覽；**不是 `PRODUCT_E2E_PASS`、`COMMERCIAL_READY` 或 `PUBLIC_LIVE`。**
PR base 為既有 `feature/asset-os-dual-platforms-20261031`，不直接以 main 為 base，避免夾帶未審的原平台改動。測試或契約變更不得自動 merge。

## 6. 本輪實際讀回契約檢核（2026-11-01）
- GitHub 實際 branch 提交及 fetch_file 讀回：7 個關鍵檔案皆可讀；PR #12 顯示共 10 個變更檔。
- 同一輪從 GitHub 讀回最新 HTML／CSS／Manifest／測試檔／Evidence 後，執行 18 項 JS 結構與安全邊界核對：**18/18 PASS**，內部相對連結缺失 **0**。
- 檢核範圍：HTML doctype、viewport、noindex、兩筆 manifest、兩個詳情 route、關閉付款/表單/追蹤、首頁導覽、證據區、合成標示、無 script/form/iframe/input/img、無對外 URL、CSS focus/390px/reduced motion、證據索引、Python 測試案例數、Drive 母文件增量與內部連結完整性。
- **此 18/18 是 connector 讀回與文字契約核對，不是 Python unittest 的執行結果，也不是 Chromium、iPhone 或 VoiceOver 的視覺測試。**
- GitHub Actions workflow 已新增，但截至本檢查 commit 尚無 workflow run；**CI_NOT_RUN**。
- 因此 G2 `STATIC_SOURCE_READBACK_PASS`，G3 `CI_AND_BROWSER_PENDING`，G5 `OWNER_GATE_CLOSED`。未獲 Owner 正式發布核准。

## 7. 2026-11-01 最新 G3 自動驗收增量（覆蓋第 6 節過往 CI_NOT_RUN 快照）
- **最終成功 Run**：https://github.com/punk8895022-byte/yc-tech-smartdispatch/actions/runs/41293584631 。該 run 的 `offline-contract` job COMPLETED/SUCCESS，並非僅檔案讀回。
- **Python unittest**：`python3 -m unittest discover -s pocs/media-commerce-showcase/tests -v`，14/14 PASS。
- **Chromium CDP 實際版面檢查**：`index.html`、`xy-hd-001.html`、`cloudlink.html` × 390px（mobile emulation）／1280px（desktop）= **6/6 PASS**；讀取當次 checked-out HTML 與 CSS，測試載入、viewport 寬、主要內容、CSS grid 欄數與無水平溢出；沒有網路端到端導航。為避開檔案/回圈位址環境政策，測試使用 `about:blank` + `document.write` 載入**相同的本機 HTML/CSS bytes**，不是部署網站功能測試。
- **截圖**：GitHub Actions Artifact `media-commerce-showcase-browser-shots` ID `13078621441`，6 張 PNG，保存 7 日，預計 2026-11-08 到期；入口：https://github.com/punk8895022-byte/yc-tech-smartdispatch/actions/runs/41293584631/artifacts/13078621441 。
- **字型修正**：首輪截圖 CJK 缺字方框，已於 GitHub CI Runner 安裝 `fonts-noto-cjk` 並在 CSS 補 `Noto Sans CJK TC` fallback；重新產生最新截圖後，已人工查看首頁、XY-HD-001、CloudLink 的桌面與 390px 截圖，中文字型、首頁 Hero、CTA 及產品狀態可讀，未見首屏裁切／橫向溢位。
- **CI 失敗歷史**：先前 Run #41293314661 為 Chromium Profile 暫存清理競態；#41293373550 為冷啟動 DevTools 逾時，後續在隔離分支修復並以最終 SUCCESS run 為準，不刪除失敗紀錄。
- **Gate 精確判定**：G2 `STATIC_SOURCE_READBACK_PASS`；G3 `AUTOMATED_CONTRACT_AND_CHROMIUM_LAYOUT_PASS_SCOPED`；真人 iPhone Safari／VoiceOver、正式服務 E2E／公開 IP 授權／真實商業權限仍 `NOT_VERIFIED`；G5 `OWNER_GATE_CLOSED`。
- **限制**：6/6 截圖證明示範頁本機渲染/版面，**不代表原 XY-HD-001 真人 Claude/Codex 交接或 CloudLink 原版 React E2E 已通過，更不代表 Production、真人付款或 IdeaX 投稿通過**。
