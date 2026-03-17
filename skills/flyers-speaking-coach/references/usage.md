# flyers-speaking-coach 使用说明

## 用途

当用户要做以下事情时，使用 `flyers-speaking-coach`：

- 设计孩子口语陪练 prompt
- 继续完善 Flyers speaking 教练规则
- 生成 ChatGPT 版口语陪练 prompt
- 生成 ChatGPT Live 版口语陪练 prompt
- 生成 Gemini 版口语陪练 prompt
- 生成 Claude 版口语陪练 prompt
- 生成 Claude Live 版口语陪练 prompt
- 调整入门版 / 标准版 / 冲刺版规则
- 优化提示、纠错、复述机制
- 维护训练结束后的 Session Summary / Session Record 模板

## 工作顺序

1. 先读取 speaking coach 总规范：
   - `../../specs/FLYERS_SPEAKING_COACH_SPEC.md`
2. 再根据任务决定是否生成：
   - ChatGPT 版 prompt
   - ChatGPT Live 版 prompt
   - Gemini 版 prompt
   - Claude 版 prompt
   - Claude Live 版 prompt
   - 家长使用说明

## 关键原则

- 一次一个问题
- 语音优先
- 句子短
- 鼓励式纠错
- 卡住时给逐级提示
- 每次结束输出 Session Summary

## 图片策略

优先级：
1. 模型生成图片
2. 家长上传图片
3. 文字场景模式

## 默认难度

- 入门版（Beginner）
