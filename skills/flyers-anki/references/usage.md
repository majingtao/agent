# flyers-anki 使用说明

## 适用场景

当用户提出以下需求时，优先使用 `flyers-anki`：

- 继续维护 `flyers_anki/` 项目
- 从 Cambridge Young Learners 官方 PDF 提取词库
- 生成或调整：
  - 听写词库
  - 全量背词词库
- 生成或重建 Anki 牌组：
  - 听写模板
  - 听写完整版
  - 全量背词完整版
- 导出核对 PDF / CSV / JSON
- 把最终产物发布到下载目录 `/var/www/html`

## 推荐工作顺序

### 1. 先确认目标类型
先判断用户要的是：

1. 词库处理
2. 听写牌组
3. 全量背词牌组
4. 规范/结构调整

### 2. 读取对应 spec
按任务只读必要 spec：

- 词库 → `references/wordlist-spec.md`
- 听写牌组 → `references/dictation-deck-spec.md`
- 全量背词牌组 → `references/full-vocab-deck-spec.md`
- 双发音/卡面规则 → `references/dual-accent-spec.md`

### 3. 优先复用现有脚本
不要手工重复造轮子，优先使用：

- `scripts/build_wordlists.py`
- `scripts/build_dictation_template.py`
- `scripts/build_dictation_full.py`
- `scripts/build_full_vocab_full.py`

### 4. 常见输入/输出位置

#### 输入
- 项目根目录：`/root/.openclaw/workspace/flyers_anki`
- 原始 PDF：`flyers_anki/source/`
- 结构化数据：`flyers_anki/data/`

#### 输出
- 最终产物：`flyers_anki/out/`
- 下载目录：`/var/www/html/`

## 发布规则

如果用户需要下载链接：

1. 先生成文件到 `flyers_anki/out/`
2. 再复制到 `/var/www/html/`
3. 最后给出：
   - `https://down.beizao.com/<文件名>`

## 维护规则

- 优先更新现有流水线，不新开第二套并行脚本
- 若需求变了，先更新 spec，再重建产物
- 对范围、词库数量、筛选规则变更，优先落到 spec 文件和 `data/` 结果中
