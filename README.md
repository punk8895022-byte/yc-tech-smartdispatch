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
