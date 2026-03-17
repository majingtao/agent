# Skills Index

当前已整理的私有 skills：

## 1. flyers-anki

位置：
- `skills/private/flyers-anki/`（本地工作区）
- `skills/flyers-anki/`（agent 仓库）

用途：
- Cambridge Young Learners 词库处理
- 听写词库与全量词库生成
- Anki 听写牌组 / 全量背词牌组生成
- review PDF / CSV / JSON 导出
- 最终产物发布到下载目录

---

## 2. flyers-speaking-coach

位置：
- `flyers_anki/skills/flyers-speaking-coach/`（项目内）
- `skills/flyers-speaking-coach/`（agent 仓库）

用途：
- Cambridge Flyers speaking 口语陪练
- ChatGPT 版 prompt
- ChatGPT Live 版 prompt
- Gemini 版 prompt
- Claude 版 prompt
- Claude Live 版 prompt
- 家长使用说明
- 默认入门版训练流程、session summary 与 session record 机制

---

## 3. flyers-speaking-bank

位置：
- `skills/private/flyers-speaking-bank/`（本地工作区）

用途：
- Cambridge Flyers speaking 真题/教材脚本整理
- 从 PDF / teacher notes 提取 speaking 题库
- 按 `parts / exchanges / story_frames` 结构整理 JSON
- 为 `flyers-speaking-coach` 或 bank coach 提供题库数据

---

## 4. flyers-speaking-bank-coach

位置：
- `skills/private/flyers-speaking-bank-coach/`（本地工作区）

用途：
- 基于 speaking bank JSON 直接带孩子练口语
- 支持整套练、按 part 练、按 exchange 续练
- 优先使用题库里的官方/参考答案
- 无答案时再按规则 fallback 生成 A2 级答案

---

## 建议使用方式

- 做词库、Anki、导出文件 → 用 `flyers-anki`
- 做孩子口语陪练 prompt / speaking 流程 → 用 `flyers-speaking-coach`
- 做 speaking 真题脚本提取 / 结构化题库 → 用 `flyers-speaking-bank`
- 基于现成 speaking bank 直接练习 → 用 `flyers-speaking-bank-coach`
