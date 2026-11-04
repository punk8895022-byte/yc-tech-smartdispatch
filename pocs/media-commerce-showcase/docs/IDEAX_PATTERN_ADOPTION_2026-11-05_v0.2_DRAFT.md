# IdeaX 作品牆設計模式｜小雲 Media Commerce 吸收與治理 v0.2 DRAFT
日期：2026-11-05｜Owner：小雲 Media Commerce｜來源狀態：PUBLIC_REFERENCE_SCOPED
追蹤入口：https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/12

## 1. 目的
把公開作品牆的「作品被發現 → 了解價值 → 檢查證據 → 取得下一步」信息架構，轉為**小雲現有 Media Commerce 的兩作品靜態切片**。本研究是公開資訊與使用者提供的截圖分析，不涉及 IdeaX 原始碼、私有 API、會員、反爬、付費資料或受著作權保護的圖片移植。沒有另建平台。

## 2. 來源可信度分級
- S1 使用者提供之 IdeaX / VibeCoding 作品牆截圖：可見作品牆定位、作品卡及 Like 介面、宣傳「被看見」訴求；是截圖可見資訊，不是官方 API 或流量證據。
- S2 IdeaX 官方網站 https://www.ideax.tw/ ：本輪直接讀取失敗。未知：作品牆完整投稿規則、審核機制、收費、API、使用者數、演算法、轉換率。**所有未知皆維持 UNVERIFIED**。
- S3 可核對之公開活動：IdeaX 創星季 https://www.accupass.com/event/2610072231045277062380 。此活動條款涉及創意提案與活動帳號，**不得推定等同 VibeCoding 作品牆投稿條款**。
- S4 其他平台「獨立比較樣本」（不是 IdeaX）：
  - https://vibecoding.is/submit/ ：示範 project name / live URL / pitch / category / prototype status / editor review 等投稿欄位。
  - https://vibecoding.tw/ ：作品、案例、技能、商品等資訊架構與免費上架宣傳。
  - https://vibecodingbox.cn/ ：作品試玩、評論概念。
  - 這些僅用於市場分類和設計模式參考，不複製 UI 素材/Logo/文案，也不將其條款套用於 IdeaX。

## 3. 反向工程（黑箱功能觀察）→ 小雲可吸收的最小能力

| 公開模式 | 使用者價值 | 小雲 v0.2 實際落地 | 故意不做 |
| --- | --- | --- | --- |
| 主題/用途探索 | 新客能快速理解作品類別 | 兩個語義化 `#case-ai` / `#case-service` 主題捷徑；manifest 兩種分類 | 無虛構熱度、無排行榜 |
| 作品卡片 | 不需看程式碼先了解價值 | 同卡展示適用對象、問題、證據邊界、目前限制 | 無未驗收「可立即使用」文案 |
| 作品詳細頁 | 建立信任 | 保留 XY-HD-001、CloudLink 合成示範及來源清楚的測試範圍 | 不公開私有 GitHub/客戶資料 |
| 投稿/曝光 | 透過外部入口吸引受眾 | manifest 的 `external_submission_status=NOT_SUBMITTED`、離線審核稿 | 無 IdeaX 自動登入、投稿、API |
| 商業轉換 | 找到詢問/成交流程 | 未來與 Business OS 同步的抽象資料契約（待 Owner Gate） | 現階段無 CRM、金流、實際追蹤 |
| 審核 | 合法、安全且避免誤導 | `release_gate.py` 兩種檢核：內部預覽 PASS、公開發布 BLOCKED | 程式不能冒充 Owner 身分/核准 |

## 4. 已落地的程式／資料
- `projects.json` schema v0.2.0：新增 `discovery.categories`、兩作品 `positioning.problem/audience/proof_statement`、`review_requirements`，及外部平台分發的停用狀態。
- `index.html` + `assets/styles.css`：帶 aria-label 的主題導覽；卡片的真實用途與證據邊界；390px/1280px 繼續自動檢查。
- `scripts/release_gate.py --mode internal`：在不讀外網、無 API 的情況下校驗狀態與兩個頁面；通過不代表可發布。
- `scripts/release_gate.py --mode packet`：輸出兩作品**內部審核文字稿**，不自動提交或外連。
- `scripts/release_gate.py --mode public`：必然回傳阻止狀態（exit=2），因為實際 Owner 核准需在工具外獨立驗證。不能靠改 JSON 自我核准。
- `tests/test_release_gate.py`：不允許公開、虛構熱度、提交成功宣稱、第三方追蹤、路徑穿越或忽略權利/個資審查。

## 5. 權威資料與安全界線
- 本 `projects.json` 只是內部展示白名單；正式 Product / CRM / Lead / Finance 不在此 Repo 建新的主資料域。
- 本 Repo 可公開讀取，因此任何文字、示意畫面、測試檔、截圖都只放不具個資、商業機密或 Secrets 的合成資料。
- HTML `noindex` 並非存取管控。公開發布需經正式網站 Repo 核對、資安、權利授權、iPhone Safari/VoiceOver、原產品 E2E、Owner 核准。
- 不新增付費 API、不使用真實客戶資料、不登入 IdeaX、不解析內部 endpoint、不蒐集 Like、評論或假流量。
- Github CI 的 `internal` 合約 PASS 和 Chromium 靜態 DOM 測試不會推導成真人雙模型/CloudLink 真實瀏覽器產品 E2E PASS。

## 6. 驗收與下一步
- G2：新資料契約與文字/版面落地，需以當次 GitHub commit + CI run 證明。
- G3：只對 GitHub Python 契約、內部發布狀態檢查與 Chromium 390px/1280px 靜態頁面測試作出 PASS 判定；真人手機、無障礙、產品 E2E 尚待執行。
- G4：IdeaX 作品牆官方投稿/費率/API、合法素材與商品資格均 UNVERIFIED，不對外傳送。
- G5：OWNER_GATE_CLOSED，Draft PR #12 不合併、不部署、不中介真實用戶、不收費。
- 最小後續試驗：Owner 一次審核兩作品類別/一句話價值、權利與證據；核准後再評估正式官網靜態發佈、手動對外投稿，並用站內**合法且已核准的**歸因方式追蹤合格詢問，不增新平台。
