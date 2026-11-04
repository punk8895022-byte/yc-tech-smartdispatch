# 小雲 Engineering RFQ｜隔離 PoC v0.1

用途：補上既有 Engineering CRM 的供應商詢價前段，不另外建立 CRM、資料庫、平台或 LINE Bot。

- 入口：quote_policy.py（匿名 BOM → LINE 待複製草稿；PoE 額定預算；成本/售價/毛利/5%營業稅計算；人工 Owner Gate）。
- 測試：tests/test_quote_policy.py（13 項 stdlib 離線單測）。
- 唯一規格與證據：../../docs/research/XY_ENGINEERING_RFQ_ZYXEL_2026-11-05_v0.1_RESEARCH_ONLY.md
- 本機執行：python -m unittest discover -s pocs/engineering-rfq/tests -v
- 目前：本地 13/13 PASS（合成資料）；GitHub CI、實際 LINE、真實廠商報價、正式 CRM/Finance、實機供電、正式收款/部署全部 NOT_RUN。
- Owner：Owner Gate CLOSED。所有對外訊息均需人工確認；程式本身不連外、不寄送、不儲存任何客戶資訊。
