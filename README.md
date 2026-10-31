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
