# 小雲 10M｜Business OS 財務流反向工程 G1.1

日期：2026-11-05｜版本：G1.1-DRAFT｜執行範圍：既有 Google Sheets + GitHub Draft PR #1

**Gate：SHEET_SCHEMA_AND_FORMULA_READBACK_PASS / PYTHON_OFFLINE_19_19_PASS / G2_REAL_FINANCE_BLOCKED / GITHUB_CI_NOT_VERIFIED / OWNER_PRODUCTION_GATE_CLOSED。**

## 反向工程觀察

原始「10M戰情總覽」只依據原台帳 J=RECOGNIZED/SETTLED、R=APPROVED、S 證據欄非空，對 N/O 進行加總。
已確定的風險：
1. 沒有認列日期/結清日期，不能隔離 12 個月目標期間，可能混入歷史資料。
2. 沒有主台帳全域唯一 ID Gate，重複商機可能被加總。
3. 未核實會計收入責任模式，agent-only 可能把工程總額 GMV 當成平台營收。
4. 空白金額、成本、憑證，或未人工複核的紀錄，不應顯示成已核可財務實績。
5. 逐案單位經濟原 N Gate 並未依賴來源主台帳的財務審查欄位，導致兩張表的核准狀態可能失聯。

## 已實際吸收的變更（現有原生 Sheet，不新增新主資料庫）

現有工作簿：https://docs.google.com/spreadsheets/d/1xvE5zR1FEmiFgYcloNrPVJmF7ulDPaX84EOQ1x_5zZE/edit

- 「10M商機與實收」新增 U:AA：U 認列日期、V 結清日期、W PRINCIPAL/AGENT、X CFO 內部審查 PENDING/REVIEWED、Y 審查來源/參考、Z 認列 Gate、AA 結清 Gate。日期/下拉表單驗證已建立。
- Z4 / AA4 為 ARRAYFORMULA，對原資料做 ID 重複、Owner、來源 URL、原驗收證據、內部複核狀態、日期、數值/直接成本、代理人預估合約與營收比例合理性檢查；輸出 REPORTING_PROVISIONAL / CASH_REPORTING_PROVISIONAL 或阻塞原因，**不能聲稱銀行或會計師已驗證**。
- 來源 H 欄為「預估合約金額」，只用於 AGENT_GMV_RISK 的初步合理性檢查，**不是已核實 GMV**；是否可按淨額認列仍需契約/會計判定。
- 「10M戰情總覽」C4:D8 改為只有 Z/AA 暫列 Gate、U/V 落在 B13:B14 的紀錄才可進入年度暫列；期間暫定 2026-11-01 ~ 2027-10-31，Owner 可按目標窗口修改。C9/D9 在未建帳／待核對時不混作 0。原五項 NT$10M 年度挑戰目標不變。
- 「10M逐案單位經濟」P3:P53 連結主台帳 Z 狀態；N4:N53 加入 MASTER_GATE_BLOCKED、DUPLICATE_IN_UNIT_ECONOMICS、REVENUE_MODE_MISMATCH，防止兩張表核准模式不一致卻產生獲利試算。
- 原主台帳 A:T 的所有既有欄位、八張原工作表及 SYNTHETIC 示例未覆寫。實際 A4:T1000 在本輪唯讀查核時無資料列；「未建帳」不表示整個公司實收為零。

## GitHub 隔離實作與真實驗收邊界

- business/10m/ledger_integrity.py：純 Python 標準函式庫，輸入匿名列表，輸出分開的 revenue_gate、cash_gate、provisional_revenue、provisional_cash；非同步/無連線/無 DB 與正式 Google 寫入。
- business/10m/test_ledger_integrity.py：19 項合成測試，涵蓋 duplicate（大小寫）、missing fields、未認列、未核准、虛構憑證、日期錯誤、數字異常、代理人總額與費收入區別、收現與認列分離、未知不得填 0。
- 本機在隔離目錄執行：python -m unittest discover -p test_ledger_integrity.py -v → **19/19 PASS**；GitHub 讀回兩檔 SHA 與本機 Git blob SHA 一致。
- 尚無這兩個新增測試的 **GitHub CI PASS**；也沒有在 Google Sheet 主台帳寫入假交易進行即時 E2E，所以現有公式只有 metadata/計算結果讀回、尚未涵蓋真實案件驗收。

## Owner Gate 及下一階段

CFO Issue #6 保持 OPEN。G2 需授權且遮蔽個資的一筆「契約→驗收→發票／認列→銀行結清」來源交叉驗證，再做真實工作表 E2E。任何證據 URI、REVIEWED 或公式 PASS 都不等於來源真實。須由專業會計核實主理人／代理人收入認列、稅票和收款主體。不得從此文件推算現有年收入、已賺淨利或客戶回購率。

**本輪不合併 PR、不進 Production、不對外發文/報價、不啟用付款/付費 API、不動正式 LINE / AI OS Runtime。**

關聯：[GitHub Draft PR #1](https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1)｜[CFO Issue #6](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/6)｜[10M War Room](https://docs.google.com/document/d/1kt7J5Kbl8K16PPuLv10FxzjzBKB6Tnar-I88GrI81eM/edit)

## 變更紀錄
2026-11-05 G1.1：反向工程並修補年度口徑、對帳 Gate、主帳與逐案一致性；本機 19/19 合成測試通過。
