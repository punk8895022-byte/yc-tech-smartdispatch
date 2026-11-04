# XY Engineering RFQ｜Zyxel 設備詢價反向工程與小雲吸收 v0.1

日期：2026-11-05｜狀態：RESEARCH_ONLY / ISOLATED_POLICY_POC / OWNER_GATE_CLOSED

## 目的
在既有 Business OS → Engineering CRM → YC Tech Match 中補上供應商詢價、技術相容性、成本與毛利試算，重用現有 Quote / Approval / Audit / Finance；不另建 CRM、資料庫或新 LINE Bot。

## 來源與映射
- 使用者提供的真實需求品項（**數量已知，價格未知**）：USG FLEX 100H × 1、GS1915-8EP × 1、NWA50AX × 4，共 6 台。
- Business OS PRD：https://docs.google.com/document/d/1otVSuymPm7JBoJsSZSvBBK9b0jo6LsREL3zbBQ8h838/edit
- Asset OS × YC Tech Match PRD：https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit
- 既有隔離 Draft PR #1：https://github.com/punk8895022-byte/yc-tech-smartdispatch/pull/1
- Zyxel NWA50AX 官方規格（802.3at PoE 16W）：https://www.zyxel.com/cn/sc/products/wireless/nwa50ax/specifications
- Zyxel GS1915-8EP 官方 PoE 總預算（60W）：https://www.zyxel.com/sites/zyxel/files/library/assets/tech-library/solution-guide/sg_nebula.pdf

## 逆向拆解：資料契約
輸入（匿名化）：RFQ_ID、項次、品牌、型號、數量、PoE 額定功率、安裝/授權選項與詢價截止。
廠商回覆（先人工收集）：Vendor_ID、報價日期、幣別、未稅單價與總價、營業稅與含稅價、報價效期、現貨、交期、運費、保固、保固起算、替代機種、授權版本/期限/續約費、附件原始來源。
衍生：PoE 安全檢查、未稅成本/售價、毛利與毛利率、稅款、客戶報價草稿、尚缺證據欄位及 Owner Gate。
正式來源唯一權威為既有 Business OS Canonical CRM；GitHub 只保存匿名化流程/程式/合成測試。真實供應商單價與客戶識別資料不得進 Git。

## 規格風險
4 台 AP × 16W = 64W，GS1915-8EP 額定 PoE 總預算僅 60W，差 4W：BOM 必須顯示 BLOCK。
替代型號需廠商重新確認總 PoE 預算、每埠 802.3at、實際電源配置、網路埠與線材；純功率 PASS 不等於實機連線已 PASS。
防火牆須詢問硬體-only 與包含資安授權版本，查年限與續約成本；未確認不可把授權視為包含。
設備/運費/施工/設定/維護分項。不能將對客售價誤稱採購成本或將未稅毛利誤稱淨利。

## 可直接複製的廠商 LINE 詢價草稿
您好，麻煩協助提供 Zyxel 設備經銷報價：
1. USG FLEX 100H 防火牆 × 1 台
2. GS1915-8EP PoE 交換器 × 1 台
3. NWA50AX Wi-Fi 6 AP × 4 台
共計 6 台。
請分列未稅單價、小計、5%稅額及含稅總價，並註明現貨、交期、保固、報價效期、運費與發票條件。
防火牆請分報純硬體與含資安授權版本、內容及續約費。
四台 AP 的額定 PoE 合計 64W，超過 GS1915-8EP 的 60W，煩請另報供電足夠的替代交換器與價格。
本案僅詢價，尚未下單，感謝！

## 工作流與 Gate
DRAFT → RFQ_READY（人工複製給廠商）→ VENDOR_REPLY_RECEIVED（附書面來源）→ TECH_CHECKED → COST_REVIEWED → OWNER_APPROVED → CUSTOMER_QUOTE_READY_FOR_MANUAL_SEND。
- 價格、稅、授權、交期或 PoE 未核實：HOLD；Owner 未核准：HOLD。
- 對外送出詢價、報價、簽約、下單、付款、資料入庫、部署各自需額外權限；程式沒有訊息發送/付款/資料庫功能。
- 只允許合成案例；真實客戶和廠商資料若後續使用，須先完成隱私/權限/來源審核。

## 驗收與狀態
- G0：現有雲端文件及 GitHub 分支、設備官方規格已核對。
- G1：本文件建立詢價欄位與規格檢查契約；正式 CRM schema 未驗證。
- G2：Python stdlib 純函數、本地 13/13 unittest PASS；遠端 CI 尚未驗證。
- G3：真實廠商書面報價、授權/PoE、庫存交期核對 NOT_RUN。
- G4：與共用 Quote/Approval/Audit/Finance 的 Staging HTTP / IAM E2E NOT_RUN。
- G5：客戶正式報價、採購下單與 Production OWNER_GATE_CLOSED。

## 下一步
先取得含有效期限的廠商書面報價，核對可行替代交換器；經銷價、對客價、毛利與授權分開驗證。核准前保持 DRAFT、不對外承諾價格、不新增付費 API、不接正式 LINE/資料庫。
版本：v0.1（2026-11-05 首次收斂）。

## Drive 閱讀鏡像（2026-11-05）
https://docs.google.com/document/d/1VmVVcbLBjqSryraGcJW4Gjd1Ekia7AukIaVgSGl3SQY/edit?usp=drivesdk
