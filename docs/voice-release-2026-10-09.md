# 双音色与越南语辅助 · 2026-10-09

本次在原有七场景网页中替换对话音频并补充越南语学习辅助。手机优先的多轮剧情重构仍是后续设计工作。

## 音频来源与范围

- 模型：MLX IndexTTS 2.5 8-bit，版本修订 `d0aa86e75bb6f3437f3831e95056fa72842d89ef`，朗读语言 `zh`。
- NPC 28 段及话题引导 3 段：`vanch.m4a` 的克隆音色。
- 玩家选项 21 段：`Bạn khỏe không .m4a` 的克隆音色。
- 本次共 52 段，源音频总时长约 364.87 秒。用命名情感权重区分迎客、解释、议价、轻快回应；玩家使用平稳示范语气。
- 原始参考录音不在仓库或 HTML 内；仅发布合成语音。原始 WAV、参考信息及完整回读报告保留在本地忽略目录。
- MP3：单声道、24 kHz、64 kbps；双遍响度处理目标 -18 LUFS / -2 dBTP。处理报告的输出响度范围 -18.42 至 -16.92 LUFS，最高真峰值 -2 dBTP。

## 验证记录

| 检查 | 结果 | 证据与范围 |
|---|---|---|
| 角色与参考录音映射 | pass | 52/52 生成记录核查；版本 2.5、中文、手动情感权重一致 |
| 独立 ASR 回读 | pass（文本/读音核查） | Confucius 对 48/52 句逐字匹配（忽略标点）；Whisper 对另 3 句逐字匹配；剩余 1 句仅 Confucius 将“得”写成同音“的”，Whisper 在该位置写为“得” |
| 音色相似度、情感自然度 | pending | 自动回读无法替代人工试听；提供本地双人试听片段 |
| 文件解码 | pass | 151 段网页 MP3 与 1 段本地试听均可解码，无错误 |
| 单文件构建 | pass | 图片、151 段音频、数据内嵌；不存在系统语音回退或本地参考录音路径 |
| 越南语覆盖 | pass | 7 开场、21 玩家回复、21 NPC 回应均有翻译及解释；21 商品有词义/句型说明 |
| 连续播放 | pass | Chromium 记录玩家 playing → ended → NPC playing → ended；慢速为 0.85×；离场停止原台词 |
| 移动端显示 | pass（浏览器尺寸检查） | 320×568、390×844：地图标签不越界，商品弹窗可滚动无横向溢出；768×1024 平板截图复核 |
| 手机真机 Safari | pending | 未使用实体手机；不能等同于真机播放验收 |

## 播放与界面

- 选项旁的喇叭用于试听，点选回复会先播放玩家，再继续 NPC。
- 朗读按钮始终跟随当前显示的台词；播放失败时可以手动重试。
- 复用一个音频播放器；切换场景或隐藏页面时停止旧音频。
- 翻译贴近对应台词；用法解释按需展开；拼音和越南语可分别开关。
- 小屏地图位置单独适配，触摸标签至少 44px 高；手机商品标签停止上下漂浮。

## 发布音频清单

下列哈希用于确认实际发布的 MP3，不包含参考录音信息。

| 音频键 | 角色 | 生成语气 | MP3 SHA-256（前 16 位） |
|---|---|---|---|
| `npc_shangchang` | NPC | 亲切迎客，轻松、有邀请感 | `6016d1d9039ec6ea` |
| `reply_shangchang_0` | NPC | 耐心解释，语调稳定，词语清楚 | `a0aa8f9504a5a157` |
| `choice_shangchang_0` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `e82e6a53afabe0ef` |
| `reply_shangchang_1` | NPC | 耐心解释，语调稳定，词语清楚 | `66961ecab887d17d` |
| `choice_shangchang_1` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `8fac86139c05cd5f` |
| `reply_shangchang_2` | NPC | 亲切迎客，轻松、有邀请感 | `6b40d5e7495acd8e` |
| `choice_shangchang_2` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `3cccbffa16f0556e` |
| `npc_chaoshi` | NPC | 亲切迎客，轻松、有邀请感 | `2f8c864bfbfcb32a` |
| `reply_chaoshi_0` | NPC | 耐心解释，语调稳定，词语清楚 | `514242aff7e129aa` |
| `choice_chaoshi_0` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `6109bee6285942b9` |
| `reply_chaoshi_1` | NPC | 耐心解释，语调稳定，词语清楚 | `d1ba3e279d782792` |
| `choice_chaoshi_1` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `b872cb0af71a426c` |
| `reply_chaoshi_2` | NPC | 亲切迎客，轻松、有邀请感 | `c08e2780499040a2` |
| `choice_chaoshi_2` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `57bdbfef768e7c03` |
| `npc_yeshi` | NPC | 轻快回应，热情但不喊叫 | `b91a34e1dead8506` |
| `reply_yeshi_0` | NPC | 耐心解释，语调稳定，词语清楚 | `7c030a01dc31b602` |
| `choice_yeshi_0` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `0cf4bc12431a2564` |
| `reply_yeshi_1` | NPC | 温和议价，坚定但不生硬 | `5318bff214015d03` |
| `choice_yeshi_1` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `7edc48c04b232565` |
| `reply_yeshi_2` | NPC | 轻快回应，热情但不喊叫 | `2e44775eb30da4dc` |
| `choice_yeshi_2` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `e4fcc1a00cf44677` |
| `npc_dianzi` | NPC | 亲切迎客，轻松、有邀请感 | `d5213aa43475e191` |
| `reply_dianzi_0` | NPC | 耐心解释，语调稳定，词语清楚 | `29c3e47f3a8f026f` |
| `choice_dianzi_0` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `db226cc1127848c7` |
| `reply_dianzi_1` | NPC | 耐心解释，语调稳定，词语清楚 | `a2b5d978e2418a8a` |
| `choice_dianzi_1` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `8c6817d552fd13c4` |
| `reply_dianzi_2` | NPC | 亲切迎客，轻松、有邀请感 | `64dcc5d280a5d23e` |
| `choice_dianzi_2` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `62ed1ca13a95435b` |
| `npc_shichang` | NPC | 亲切迎客，轻松、有邀请感 | `6fd25e787663b4a4` |
| `reply_shichang_0` | NPC | 耐心解释，语调稳定，词语清楚 | `95bd289f8dc8433a` |
| `choice_shichang_0` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `fff7f02ab8c05b6a` |
| `reply_shichang_1` | NPC | 耐心解释，语调稳定，词语清楚 | `8b63d322cbbe996f` |
| `choice_shichang_1` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `d4a6711bbc9f84c4` |
| `reply_shichang_2` | NPC | 亲切迎客，轻松、有邀请感 | `8d72859c231d38ca` |
| `choice_shichang_2` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `b6792182a9a835dd` |
| `npc_xiaomaibu` | NPC | 亲切迎客，轻松、有邀请感 | `d4b2e0fc54b849e9` |
| `reply_xiaomaibu_0` | NPC | 耐心解释，语调稳定，词语清楚 | `213b12e2fb4904bd` |
| `choice_xiaomaibu_0` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `814182339ae37e73` |
| `reply_xiaomaibu_1` | NPC | 耐心解释，语调稳定，词语清楚 | `9c11c95bf48812a9` |
| `choice_xiaomaibu_1` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `0c501294c5f4119f` |
| `reply_xiaomaibu_2` | NPC | 轻快回应，热情但不喊叫 | `3504be1c3ed05ba7` |
| `choice_xiaomaibu_2` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `34d6898c80831988` |
| `npc_wangzhan` | NPC | 亲切迎客，轻松、有邀请感 | `a2ee018f79ced333` |
| `reply_wangzhan_0` | NPC | 耐心解释，语调稳定，词语清楚 | `1d31119d2ef2735c` |
| `choice_wangzhan_0` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `c61b93020d1fa83b` |
| `reply_wangzhan_1` | NPC | 耐心解释，语调稳定，词语清楚 | `b745b0a5feeae1a7` |
| `choice_wangzhan_1` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `a0bc22da168b23d3` |
| `reply_wangzhan_2` | NPC | 亲切迎客，轻松、有邀请感 | `a25dd578dcf1d3b4` |
| `choice_wangzhan_2` | 玩家 | 自然示范，平稳清晰，供学习者跟读 | `a303d7ac693111dd` |
| `topic_0` | 话题引导 | 自然示范，平稳清晰，供学习者跟读 | `b32e54909dda1e41` |
| `topic_1` | 话题引导 | 自然示范，平稳清晰，供学习者跟读 | `2a88f1ba01a6984e` |
| `topic_2` | 话题引导 | 自然示范，平稳清晰，供学习者跟读 | `bb0f4ac31956fc3f` |
