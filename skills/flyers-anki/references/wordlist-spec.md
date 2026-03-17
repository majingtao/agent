# Wordlist Spec

## 目标

从 Cambridge 官方 PDF 中提取并整理 **Pre A1 Starters + A1 Movers + A2 Flyers** 全范围词库，作为后续两个牌组的数据上游：

1. 听写牌组（全范围内筛选后的词库）
2. 全量背词牌组（Pre A1 → A2 全范围词库）

官方 PDF：
- `source/flyers_2025_wordlist.pdf`
- 来源：<https://www.cambridgeenglish.org/images/506166-starters-movers-flyers-word-list-2025.pdf>

---

## 组织原则

单词库作为数据资产，单独维护，但仍属于 `flyers_anki/` 项目。

建议目录：

```text
flyers_anki/
  source/
    flyers_2025_wordlist.pdf
  specs/
    WORDLIST_SPEC.md
    DICTATION_DECK_SPEC.md
    FULL_VOCAB_DECK_SPEC.md
  data/
    flyers_a2_raw.csv
    flyers_a2_selected.csv
    flyers_a2_classified.csv
    flyers_a2_full_vocab.csv
```

---

## 筛选范围

- 处理 **Pre A1 Starters + A1 Movers + A2 Flyers** 全范围
- 保存原始 PDF 以便审计和复核

---

## 筛选口径

### 口径 A：官方明确需要书写的项目
优先保留 PDF 中明确归到：
- 需要理解并书写
- 需要识别并书写
的项目

适用范围：**Starters + Movers + Flyers 全范围**

### 口径 B：考前训练实用扩展
在口径 A 基础上，再补入：
- 高频核心词
- 适合第一次考试训练的核心词
- 易错词
- 词组/短语
- 特殊项目（名字、数字、月份、时间等）

适用范围：**Starters + Movers + Flyers 全范围**

规则：
- **A + B 同时保留**
- **单词不重复**

---

## 多维分类要求

每个词建议包含以下维度：

- word
- phrase_type（单词 / 词组）
- level（A2 Flyers）
- official_write（是否属于口径 A）
- training_include（是否纳入口径 B）
- write_priority（must_write / core / extended / tricky）
- topic（主题分类）
- pos（词性）
- special_type（名字 / 数字 / 月份 / 时间 / 无）
- notes
- source_page

---

## 分类方式

### 1. 按训练用途
- 必写核心词
- 扩展词
- 易错词
- 特殊项目

### 2. 按词性
- 名词
- 动词
- 形容词
- 副词
- 介词 / 短语
- 固定表达

### 3. 按主题
例如：
- 家庭
- 学校
- 食物
- 动物
- 衣物
- 天气
- 时间
- 交通
- 身体
- 房屋
- 运动娱乐

---

## 输出结果

至少输出以下文件：

- `data/flyers_a2_raw.csv`：A2 原始提取词表
- `data/flyers_a2_selected.csv`：按口径 A + B 去重后的筛选结果
- `data/flyers_a2_classified.csv`：多维分类后的听写用词库
- `data/flyers_a2_full_vocab.csv`：完整 A2 词库，供全量背词牌组使用

---

## 与两个牌组的协同关系

### 上游
`WORDLIST_SPEC.md` 输出结构化词库

### 下游1：听写牌组
由 `DICTATION_DECK_SPEC.md` 使用筛选后的听写词库

### 下游2：全量牌组
由 `FULL_VOCAB_DECK_SPEC.md` 使用全部 A2 词库
