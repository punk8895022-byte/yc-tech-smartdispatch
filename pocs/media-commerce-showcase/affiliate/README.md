# MEDIA-COMMERCE Affiliate Revenue Engine｜2026-11-05 v0.1 STAGING_ONLY

## 目的
接入既有 Media Commerce showcase 的隔離擴充頁。保留原有兩作品及 release gate 不變；本切片不引入新套件／資料庫／外部 API／額外平台。

## 入口
- `affiliate/index.html`：單頁推薦展示 + 3 組不同 SubID 的本地模擬按鈕
- `affiliate/offers.json`：明確標記 `SYNTHETIC_NOT_APPROVED`、空目的地與假設佣金，禁止當作真實聯盟商品
- `affiliate/sandbox.js`：瀏覽器記憶體中的 click 計數；無外部請求、Cookie、localStorage、持久資料。
- `affiliate/tests/test_affiliate_contract.py`：無依賴 Python 契約測試。

## 測試
`python3 -m unittest discover -s pocs/media-commerce-showcase/affiliate/tests -v`
本機：`python3 -m http.server 8765 --bind 127.0.0.1 --directory pocs/media-commerce-showcase`，開啟 `http://127.0.0.1:8765/affiliate/`。

## 歸因與真實接入 Gate
三組合成 SubID：`xy_art_ig_001`、`xy_nas_yt_001`、`xy_travel_blog_001`；未生成 Travelpayouts 真實追蹤連結。正式串接前依序要求：官方 Program 核准、目的地/品牌書面授權、SubID 格式核對、商業揭露、合規隱私政策、退貨/拒付處理、以 provider 報表校正佣金，經 Reviewer 與 Owner 簽核。

## 資料口徑
「模擬點擊」與「假設佣金」均非實際收益；實際已結算固定 NT$0。合法真實點擊須由第一方服務端事件與官方報表對帳後方能採認，無資料禁止猜估。此版僅能模擬點擊，尚無模擬訂單輸入介面，預估佣金因此固定零；後續可在下一 Gate 使用合成訂單資料測試計算。

## Gate
G2: SOURCE_COMMITTED；G3: CI_PENDING；G4: PROVIDER_NOT_CONNECTED；G5: OWNER_GATE_CLOSED。頁面 noindex，但 GitHub Repo 為公開，禁止加入 Credentials、客資或未核准的真實推廣連結。

## 來源
Google Drive Asset OS 雙平台 PRD（既有主規格）；GEM-05 MEDIA-COMMERCE 工作室規格；GitHub 原 Draft PR #12（不更動）；Travelpayouts 官方合作規則與方案頁待正式 Program 核准後逐項核對。
