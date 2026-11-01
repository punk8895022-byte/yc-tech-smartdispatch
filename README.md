# yc-tech-smartdispatch｜雙平台工程／內容入口（規劃分支）

原 main repo README 僅有「智慧派工系統」。本分支在不改原有 Main 的情況下，規劃把資訊弱電媒合（YC Tech Match）與自媒體分潤（Media Commerce）整合至既有 Xiaoyun Business OS。

## 入口與版本
- **Owner**：待核准；**Gate**：RESEARCH_ONLY / DRAFT_PR / NOT_DEPLOYED。
- **目前方案**：兩獨立前台 + 共用 CRM/Approval/Audit/Finance。
- **需求/架構**：[`docs/YC_DUAL_PLATFORMS_PRD_2026-10-31_v0.1_DRAFT.md`](docs/YC_DUAL_PLATFORMS_PRD_2026-10-31_v0.1_DRAFT.md)
- **Google Drive 母文件**：[雙平台整合 PRD](https://docs.google.com/document/d/1r8n5EFnImrTQYIAZw8_HkK-SEJqGSTVROFkhWMMJe5g/edit?usp=drivesdk)
- **Asset OS 戰略**：[V1.0](https://docs.google.com/document/d/1a3D3uKBefJO7ZsEScedhKUUl6o9ZAVhMHx47YCqNhfE/edit)
- **重用候選**：[既有派工程式](https://github.com/punk8895022-byte/yc-tech-smartdispatch-1) / [AI OS](https://github.com/punk8895022-byte/xiaoyun-ai-os)。
- **程式碼原型**：本輪完整互動示範已另以 ChatGPT ZIP 附件交付；ZIP 尚未提交到此 GitHub 分支，不能將本 branch 視為已包含可部署程式。
- **阻塞**：金流/收款責任、工程商資格、正式 Identity/PII 資安、既有 AI OS Runtime/LINE P0。
- **下一步**：Owner 審方案 → 從附件逐檔提交經測試的 source 到獨立分支 → Reviewer 驗收 M0 → staging 綁接共用後端 M1 → 受限測試 → 另行核准 Production。

## 變更
- 2026-10-31：首次建立雙平台規劃入口，未對 Production 造成異動。

## V2.0 全球平台研究與成長策略（2026-10-31｜DRAFT）
- **唯一 V2.0 戰略／Benchmark 入口：** [全球平台比較 × 四大飛輪 × 收益模型 × 90 天驗收](docs/ASSET_OS_V2_GLOBAL_PLATFORM_BENCHMARK_AND_GROWTH_20261031_DRAFT.md)
- **Google Drive 對照版：** https://docs.google.com/document/d/1T-iSjJ-IluVboCRnLVTQ_dfLSi_eHBwEm92V1_0Cq00/edit
- **V0.1 範圍：** 保留原雙平台 PRD，V2.0 為新商業研究與 Gate 增量，不取代已存在的功能規格。
- **商業結論：** 高品質地方弱電/資訊 B2B 需求入口 → 工程商工具訂閱/合法聯盟導流 → 條件成熟後才啟用明示費率的收費模式；不託管工程款、不預設「指數成長必達」。
- **證據等級：** 市場來源已核對；尚無真實平台合格需求、報價、付費、收入、部署驗收，維持 `RESEARCH_ONLY / OWNER_GATE_CLOSED`。

## V3.0｜年營收 NT$10,000,000 董事會作戰室（DRAFT）
- [十席 AI 經營團隊與 12 個月三情境收入模型](https://github.com/punk8895022-byte/yc-tech-smartdispatch/blob/feature/asset-os-dual-platforms-20261031/docs/ASSET_OS_10M_REVENUE_WAR_ROOM_20261031_V3_DRAFT.md)
- [Google Drive 證據與戰略決策文件](https://docs.google.com/document/d/1kt7J5Kbl8K16PPuLv10FxzjzBKB6Tnar-I88GrI81eM/edit?usp=drivesdk)
- [董事會主工作任務 #5](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/5)；分工 [CFO #6](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/6)、[Sales #7](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/7)、[COO #8](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/8)、[Growth #9](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/9)、[Product #10](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/10)、[Risk #11](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/11)。
- **注意**：AI「十席」是可重複使用的模擬決策角色，未聘真人、未啟動 Agent、不代表已有訂單或千萬營收。

## V3.1｜執行成果（2026-10-31｜隔離／未部署）
- [10M 戰情工作簿](https://docs.google.com/spreadsheets/d/1xvE5zR1FEmiFgYcloNrPVJmF7ulDPaX84EOQ1x_5zZE/edit)：新增 `10M戰情總覽`、`10M商機與實收`；未建帳時不把未知報成 0，舊六頁保留。
- [第一輪實際執行 Drive 報告](https://docs.google.com/document/d/1J_lTqVI4r1iulZXs0cJyPDMUT3AcE28su7NNs42JkNM/edit)。
- [三項企業解決方案與提案草稿](business/10m/SOW_OFFER_SALES_PLAYBOOK_2026-10-31_v0.1_DRAFT.md)：假設定價、驗收、排除、SOW 和外聯 Gate；尚未對外發送。
- [CloudLink staging-only 後端 POC](pocs/cloudlink-staging-api/README.md)：FastAPI、SQLite、客戶發案→Reviewer 審核→工程師報價→客戶選擇，測試 `python -m pytest -q` 3/3 PASS（**僅本機隔離，未跑 GitHub Actions**）。關閉付款；未用正式 IAM、多租戶或私人客戶資料。
- **Next Gate**：前後端 staging 合成 E2E、真實業務需求與成本來源核驗、Owner 核准對外商務聯絡；不得合併 main 或部署 Production。

## M1a｜工程媒合三角色互動關卡（2026-10-31｜LOCAL PASS）
- 程式：[CloudLink staging-only API + 三角色前端](pocs/cloudlink-staging-api/README.md)，原本的 v0.1 後端已增加 `/demo`、`/my/requests`、`/review/requests`；使用 FastAPI + SQLite，沒有正式登入與金流。
- 隔離測試：`python -m pytest -q` **5/5 PASS**；Chromium 390px 介面以 in-process ASGI 橋接完成測試發案、審核、報價、選擇、資料讀回。環境封鎖真實 localhost browser navigation，**不能當作完整 HTTP E2E 或正式 CloudLink React 對接通過**。
- Google Drive [執行報告 V3.2 增量](https://docs.google.com/document/d/1J_lTqVI4r1iulZXs0cJyPDMUT3AcE28su7NNs42JkNM/edit)；[M1 媒合 Issue #3](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/3)；[Product/CTO Issue #10](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/10)。
- **下一關 M1b**：舊版 `yuntech-prototype` 真正 React 前端與新 API 的安全整合；正式 OAuth/IAM、多租戶、工程師審核、報價明細、驗收和實際 staging UAT 全部仍 BLOCKED。
- PR 仍 Draft；Production／真實客戶／金流／新增付費 API：未執行、未授權。

## V3.3｜CloudLink M1b-A 舊分類相容性驗收（2026-10-31）
- [Drive V3.3 隔離驗收來源](https://docs.google.com/document/d/1J_lTqVI4r1iulZXs0cJyPDMUT3AcE28su7NNs42JkNM/edit)；[Issue #3](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/3) / [Issue #10](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/10)。
- **本機完整原型（ChatGPT 附件）**：FastAPI + SQLite + legacy category bridge，pytest 15/15，Chromium 390px 擷取（API bridge，非正式網路 E2E）。
- **GitHub 目前只同步部分原始碼**：[`legacy_schema.py`](pocs/cloudlink-staging-api/legacy_schema.py)、[`test_legacy_schema.py`](pocs/cloudlink-staging-api/tests/test_legacy_schema.py)、[`legacy.html`](pocs/cloudlink-staging-api/web/legacy.html)；`legacy.html` 尚未正式接上 GitHub 目前的 `app.py` / `legacy.js`，不能只從 Repo 啟動 M1b，源碼完整同步待辦。
- **M1b-A LOCAL_PASS / GITHUB_SOURCE_PARITY BLOCKED / M1b-B NOT_RUN / PRODUCTION OWNER_GATE_CLOSED**。不得把舊 React 39 萬字元介面視為已完成連線，亦沒有真實收入。

## M1b-B｜原版 CloudLink React 真實發案表單 API 接線（DRAFT）
- [舊專案原始 React feature 分支 Draft PR](https://github.com/punk8895022-byte/yuntech-prototype/pull/1)：`index.html` 與 `app.jsx` 都改為 `ClientCreateJob` 送出 `POST /legacy/requests`；保留 master 不變，取消該流程「假訂金已付款」與錢包扣款。
- [本專案 staging-only 後端](pocs/cloudlink-staging-api/README.md)：`/legacy-react` 必須本機 loopback、明確設定功能旗標及獨立原版 index 路徑。測試資料只允許虛構資料、類別 `net/cctv/access`、縣市級地區。
- **Gate**：FastAPI/SQLite 本機 18/18 PASS，另有 Python 127.0.0.1 實際 socket/HTTP 跨角色測試 PASS；舊版原始 React 的完整瀏覽器操作未通過驗收（CDN/React runtime 不可在本環境完整重現）；不代表 IAM/多租戶/金流或 Production 可用。

## V3.5｜M1c-A 多帳號隔離本機驗收（2026-11-01）
- [後端代碼／測試規格](pocs/cloudlink-staging-api/README.md)：修復先前測試語法阻塞，合成客戶 A/B、工程師 A/B 隔離、非法身分拒絕、工程師私有報價 API。
- **本機實測**：重建 M1b 已驗證包後，`pytest` 25/25 PASS，真正 127.0.0.1 TCP/HTTP＋SQLite 跨客戶、跨工程師隔離 `M1C_LOOPBACK_SOCKET_PASS`。
- [Drive V3.5 實際執行證據](https://docs.google.com/document/d/1J_lTqVI4r1iulZXs0cJyPDMUT3AcE28su7NNs42JkNM/edit)；[經營主 Issue #5](https://github.com/punk8895022-byte/yc-tech-smartdispatch/issues/5)。
- **未解**：GitHub CI 未驗證、原版 React 完整瀏覽器 E2E 未完成、正式 IAM/租戶 DB 權限與法律金流未實作；所有訂單/收入依舊沒有新成交驗證。M1c-A LOCAL_PASS；M1c-B NOT_RUN；Production Owner Gate CLOSED。
