# 小雲 10M｜逐案單位經濟 G1 Gate｜2026-11-01 v1.0

**狀態：G1_OFFLINE_SCOPED_PASS / FINANCE_EVIDENCE_BLOCKED / OWNER_GATE_CLOSED / NOT_PRODUCTION。**
本輪沿用既有資料與 Draft PR #1；不新增付款、API、對外投標、真客戶資料或獨立主資料庫。

## 唯一帳務入口與本輪實際變更

- 唯一權威仍為現有 Google Sheets「10M商機與實收」：https://docs.google.com/spreadsheets/d/1xvE5zR1FEmiFgYcloNrPVJmF7ulDPaX84EOQ1x_5zZE/edit
- 新增「10M逐案單位經濟」原生頁籤，僅輸入主台帳現有商機 ID（A4:A53），不重複維護營收／實收／直接成本。
- B:G 連動主表 J/R/N/O/P/S：階段、Owner、營收、實收、直接成本、證據；空白來源保留空白（ISBLANK+INDEX），UNKNOWN 不變成 0。
- H 為 PRINCIPAL／AGENT；AGENT 必須填 I 他方工程 GMV，並檢查 GMV >= 可認列服務費收入。GMV 不加入可認列收入。
- J 為逐案 CAC、K 為逐案變動客服/保固成本（需自行核實，不可空白代 0）；L = D−F−J−K，M = L/D。
- N Gate：不存在或重複的 ID、未到 RECOGNIZED/SETTLED、Owner 未 APPROVED、證據缺漏、成本不完整、模式/GMV 不符，均不顯示 L/M。
- N=CALCULABLE_UNVERIFIED 只代表輸入可試算，不是會計認列核可或實際完成驗收。
- 右側 Q:Y 的 SYNTHETIC 範例與正式台帳隔離：PRINCIPAL GMV=200000、收入=200000、直接成本120000、CAC10000、售後5000，貢獻65000（32.5%）；AGENT GMV=40000、服務費收入3200、直接成本1000、CAC300、售後200，貢獻1700（53.125%）。兩者不計入真實營收。
- 原本的「10M戰情總覽」「10M商機與實收」及另外六張表均未覆寫；本表不自動回填真實獲利。

## 可重現的獨立程式檢核

- business/10m/unit_economics.py：Python 標準函式庫 Decimal；讀取匿名 JSON list，輸出每筆狀態、貢獻、貢獻率；不連線、不存客戶資料。
- business/10m/test_unit_economics.py：12 項合成測試；包含 PRINCIPAL/AGENT、Gate、缺值、負值、異常值、現金與營收獨立。
- 在隔離本機執行 python -m unittest discover -s business/10m -p 'test_unit_economics.py' -v → **12/12 PASS**（2026-11-01；不是 GitHub CI PASS）。
- Python 與 Sheets 的 CALCULABLE_UNVERIFIED 僅為計算條件檢查，無法證明原始憑證真實。

## CFO 阻塞及下一關

1. 真實財務仍未知：需授權的 12 個月合約、驗收、發票、銀行與成本來源；未提供不得把空白填成 0。
2. 主理人與代理人：逐案核實主承攬責任、發票及帳務準則，必要時交專業會計判斷。
3. 缺客戶留存 cohort、LTV、固定薪資、資本成本和真實 CAC；此模型不是淨利表。
4. 下一個 Gate G2：Owner 核准之唯讀帳務證據下，核對至少 1 筆真實合同→交付→驗收→認列→實收，然後再驗證 N Gate。之前 CFO Issue #6 不關閉。
5. 對外 Gate：不發案、不報價、不發布、不付款；PR 持續 Draft，不合併 main。

相關來源：[10M War Room](https://docs.google.com/document/d/1kt7J5Kbl8K16PPuLv10FxzjzBKB6Tnar-I88GrI81eM/edit) · [CFO Issue #6](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/6) · [Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1)

## 變更紀錄
2026-11-01 v1.0：新增原生逐案驗算及離線 Python 測試，合成案例計算通過，保留既有正式資料與 Owner Gate。
