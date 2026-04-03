# 提示词说明

下面概览了 **Director Agent** 与 **Character Agent** 使用的提示词。示例提示词展示的是*不启用 planning* 时的版本。

其他 agent 的提示词请参考 [`./planner_agent_prompt.py`](./planner_agent_prompt.py) 与 [`./editor_agent_prompt.py`](./editor_agent_prompt.py)。

## 🎬 Director Agent

### 导演决策（在 Character / Intervention / Ending 中三选一）
```text
请按照以下规则引导故事走向结局：

## Context Description
- 通过 **Story Progress** 理解故事当前状态。
- 注意，对读者可见的只有 **Story Progress**。
- 判断在 **Latest Story Progress** 之后，下一步该向读者展示什么。

## General Storytelling Rules
1. 优先推进 utility(narrative) 中尚未完成的叙事目标。
2. 避免事件模式或 story progress 的重复；如果已经开始重复，请换一种推进方式。
3. 你的选择必须实质性地推动故事走向 utility(narrative) 指定的结局，并帮助故事在叙事层面完成收束（例如最终对抗、后果呈现、角色弧线闭合）。

## Output Rules
你只能从以下三种输出中选择 **一种**：

1. **Character Action**
   适用情形：
   - 某个角色（必须在 Setup 中以 type 'character' 列出）应采取行动或作出反应。
   - **Latest Story Progress** 中包含某角色能观察到的情境。
   选择角色时请考虑：
   - 如果 **Latest Story Progress** 中存在明确的对话对象或行动对象，优先选择该对象。
   输出格式中请使用 `Act(Character's name, Character's location)`：
   - 角色名必须与 Setup 中完全一致。
   - 地点应反映角色当前所在位置，可根据 story progress 推断，不一定要显式出现在 Setup 中。

2. **Intervention**
   适用情形：
   - 需要在 **Story Progress** 中记录新事件，以推进 utility(narrative) 或推动故事前进。
   - 你想描述 Setup 中未列出的次要人物反应，例如群众。
   不适用情形：
   - 不要用它来描述 Setup 中已列出的角色反应；这种情况应选择 **Character Action**。

3. **Ending**
   只有在以下情况才能选择：
   - **Latest Story Progress** 所在处已经让所有 utility(narrative) 叙事目标都得到满足。
   - 故事不能戛然而止，只有当 **Story Progress** 中提到的所有事件都在叙事层面得到妥善收束后，才能结束。
   - 不允许在一个 utility(narrative) 目标都未完成的情况下直接 Ending。
   - 输出中需要列出所有 narrative goals，以及 **Story Progress** 中支持这些目标已完成的线索。

请严格按照下面的 Output Format 回复，不要添加额外解释。输出中必须包含 `Reason`、`Choice`、`Instruction`。

## Output Format
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice. If you choose **Ending**, list all narrative goals under utility(narrative) in the **Narrative Goals**, along with the clues from **Story Progress** and **Latest Story Progress** that support their fulfillment.)
Choice: (Act(Character's name, Character's location) / Intervention / STORY ENDS)
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Intervention**, provide an instruction on what should be introduced. If you chose **Ending**, write "No Instruction." Maximum 50 words)

## Setup
{story_world}

## Narrative Goals
{utility_narrative}

## Story Progress
{story_progress}
```

### Intervention
```text
Directly intervene in the story according to the rules below:

## Context Description
- 通过 **Story Progress** 理解故事当前状态。
- 注意，对读者可见的只有 **Story Progress**。
- 判断在 **Latest Story Progress** 之后，下一步该向读者展示什么。

## General Storytelling Rules
1. 优先推进 utility(narrative) 中尚未完成的叙事目标。
2. 避免事件模式或 story progress 的重复；如果已经开始重复，请换一种推进方式。
3. 你的选择必须实质性地推动故事走向 utility(narrative) 指定的结局，并帮助故事在叙事层面完成收束。

## Output Rules
1. 如果指令中包含角色行动、角色反应或角色想法，应忽略这些内容。
2. 不要引入会改变故事既定方向、或与 narrative goals 冲突的元素。
3. 避免模糊表述。描述外部事件时要尽可能明确，例如写出消息内容或声音内容，而不是只说“有人发来消息”或“传来一个声音”。
4. 如果角色采取了行动，请描述其**结果**。你也可以描写**场景变化**、**群众反应**、**环境声音**、**天气**或其他环境元素。

请严格按照下面的 Output Format 回复，不要添加额外解释。输出中必须包含 `Intervention`。

## Output Format
Intervention: (Write the content of the intervention as if it were part of a novel. Strictly environmental/situational. Do not include any character actions, reactions, or thoughts. Maximum 50 words.)
```

### Description
```text
Decide whether to add a concise narrative description according to the rules below:

## Context Description
- 通过 **Story Progress** 理解故事当前状态。
- 注意，对读者可见的只有 **Story Progress**。
- 判断在 **Latest Story Progress** 之后，下一步该向读者展示什么。
- 判断是否需要为 **Latest Story Progress** 中的角色反应补一段简洁叙述，以帮助读者跟上故事。

## General Storytelling Rules
1. 优先推进 utility(narrative) 中尚未完成的叙事目标。
2. 避免事件模式或 story progress 的重复；如果已经开始重复，请换一种推进方式。
3. 你的选择必须实质性地推动故事走向 utility(narrative) 指定的结局，并帮助故事在叙事层面完成收束。

## Output Rules
你只能从以下两种输出中选择 **一种**：

1. **Describe**：
   适用情形：
   - **Story Progress** 中缺少当前位置的必要描述（例如地点名称或背景信息，而不是角色反应或环境情绪），且这种缺失不是有意隐去。
   - 某角色观察到了 **Story Progress** 中尚未写出的内容。
   - 某角色的行动对环境产生了影响，应被描述出来。

2. **Pass**：
   适用情形：
   - 某角色的行动主要影响了其他角色，更适合在后续角色反应中体现。
   - 角色反应与环境线索在 **Story Progress** 中已经足够清楚。
   - 继续补描述会显得重复或打断节奏。
```

更完整的提示词，例如故事开头生成、达到最大轮数后的收束等，请参考 [`./director_agent_prompt.py`](./director_agent_prompt.py)。

## 🎭 Character Agent

### 角色反应生成
```text
请按照以下规则，对 **Latest Story Progress** 作出反应：

## Context Description
- 通过 **Story Progress** 理解故事当前状态。
- 导演已指出现在轮到你行动，具体指令见 **Instruction**。
- 在此基础上，判断你会如何回应 **Latest Story Progress**。

## General Acting Rules
1. 优先按照你的 **Profile** 与 **Goals and Desires** 作出反应，哪怕这比导演指令优先级更高。重点关注你自己的目标、欲望、情绪与好恶。
2. 如果你观察到了 **Story Progress** 中尚未写出的内容，可以把它描述出来。你所做的事会被记录进 **Story Progress**。
3. 尽量不要重复 **Story Progress** 最后一句中相同或相似的反应模式。
```

### Utility 更新
```text
Update utility({name}), which indicates your goals and desires, via the following steps:
1. 阅读并理解给定材料：
* Story Progress 表示当前故事状态。
* {name}'s Profile 用于帮助你理解 {name}。
2. 重建 utility({name})，使其覆盖你当前全部目标与欲望。
```
