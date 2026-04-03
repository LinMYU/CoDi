EVALUATE_STORY_AB_PROMPT = """
你将进行一次并排评测。你会看到两篇系统生成的故事。请按以下步骤比较两篇故事，并判断哪一篇更好：

1. 阅读并理解与故事有关的材料：
* Characters' Profiles

2. 基于以下维度比较这两篇故事：
- Plot: 故事应具有清晰可辨的结构，例如连贯的开端、中段和结尾。故事中的事件与转折应推动情节前进，不应存在逻辑或概念层面的矛盾。若出现惊奇或破坏性元素，它们应是有意为之，能够服务故事，而不是显得突兀、怪异或格格不入。
- Development: 角色与场景应被充分引入，并通过相关细节建立语境，使读者理解它们在故事中的位置。细节和复杂度应适度，令故事更真实可信。
- Language Use: 语言应具有变化与丰富性，包括句式、措辞与词汇层面的多样化。故事应适当运用修辞、语言和文学手法以增强表达效果，同时避免空泛或重复的表述，除非这种重复是为了叙事、主题或语言效果而有意为之。
- Anthropomorphism: Characters' Profiles 中列出的角色应像真实、独立的人，而不是工具或助手。他们应有自己的目标、独立决策与稳定偏好。若角色表现得过度乐于助人、说教、冗长或顺从，从而破坏叙事真实感，就会削弱故事的真实度与吸引力。
- Character Fidelity: Characters' Profiles 中列出的角色，其行为、说话方式和决策应符合既定背景、性格与情境。比如角色突然拥有不应知道的信息、展现与人设冲突的价值观，或作出不合情理的反应，都会破坏可信度。角色之间的互动也应符合他们的社会关系与相处动态。

请围绕上述五个维度，对两篇故事进行详细评估。最后按下面模板给出各维度结果。评估中不要加入加粗、斜体等强调格式。
除评分标签与固定字段名外，评估正文默认使用简体中文。

Based on my assessment, the better story for each dimension is:
Plot: [A or B or Same]
Development: [A or B or Same]
Language Use: [A or B or Same]
Anthropomorphism: [A or B or Same]
Character Fidelity: [A or B or Same]
Overall: [A or B or Same]

[Characters' Profiles (Same for Story A and B)]
{character_profiles}

[Story A]
{story_a}

[Story B]
{story_b}

[Assessment]
""".strip()

EVALUATE_STORY_AB_PROMPT_VS_GOLD = """
你将进行一次并排评测。你会看到两篇系统生成的故事。请基于以下维度比较这两篇故事：
- Plot: 故事应具有清晰可辨的结构，例如连贯的开端、中段和结尾。故事中的事件与转折应推动情节前进，不应存在逻辑或概念层面的矛盾。若出现惊奇或破坏性元素，它们应是有意为之，能够服务故事，而不是显得突兀、怪异或格格不入。
- Creativity: 故事应包含有吸引力的角色、主题与意象。创意不应显得空泛、普通或乏味。应避免未经处理的陈词滥调、套路化角色与刻板印象；若使用 trope 或 cliché，应当服务于特定目的。故事还应包含提示词中未被直接明说的原创元素。
- Development: 角色与场景应被充分引入，并通过相关细节建立语境，使读者理解它们在故事中的位置。细节和复杂度应适度，令故事更真实可信。
- Language Use: 语言应具有变化与丰富性，包括句式、措辞与词汇层面的多样化。故事应适当运用修辞、语言和文学手法以增强表达效果，同时避免空泛或重复的表述，除非这种重复是为了叙事、主题或语言效果而有意为之。

请围绕上述四个维度，对两篇故事进行详细评估。最后按下面模板给出各维度结果。评估中不要加入加粗、斜体等强调格式。
除评分标签与固定字段名外，评估正文默认使用简体中文。

Based on my assessment, the better story for each dimension is:
Plot: [A or B or Same]
Creativity: [A or B or Same]
Development: [A or B or Same]
Language Use: [A or B or Same]
Overall: [A or B or Same]

[Story A]
{story_a}

[Story B]
{story_b}

[Assessment]
""".strip()

EVALUATE_STORY_QUALITY_TMAS_AB_TEST_PROMPT = '''
你将进行一次并排评测。你会看到两篇系统生成的故事。请基于以下维度比较两篇故事，并判断哪一篇更好：

- Plot: 故事应具有清晰可辨的结构，例如连贯的开端、中段和结尾。故事中的事件与转折应推动情节前进，不应存在逻辑或概念层面的矛盾。若出现惊奇或破坏性元素，它们应是有意为之，能够服务故事，而不是显得突兀、怪异或格格不入。
- Creativity: 故事应包含有吸引力的角色、主题与意象。创意不应显得空泛、普通或乏味。应避免未经处理的陈词滥调、套路化角色与刻板印象；若使用 trope 或 cliché，应当服务于特定目的。故事还应包含提示词中未被直接明说的原创元素。
- Development: 角色与场景应被充分引入，并通过相关细节建立语境，使读者理解它们在故事中的位置。细节和复杂度应适度，令故事更真实可信。
- Language Use: 语言应具有变化与丰富性，包括句式、措辞与词汇层面的多样化。故事应适当运用修辞、语言和文学手法以增强表达效果，同时避免空泛或重复的表述，除非这种重复是为了叙事、主题或语言效果而有意为之。

请围绕上述四个维度，对两篇故事进行详细评估。最后按下面模板给出各维度结果。评估中不要加入加粗、斜体等强调格式。
除评分标签与固定字段名外，评估正文默认使用简体中文。

Based on my assessment, the better story for each dimension is:
Plot: [A or B or Same]
Creativity: [A or B or Same]
Development: [A or B or Same]
Language Use: [A or B or Same]
Overall: [A or B or Same]

[Story A]
{story_a}

[Story B]
{story_b}

[Assessment]
'''.strip()

EVALUATE_STORY_QUALITY_TMAS_PROMPT = '''
请阅读给定的 **Story**，然后基于以下维度进行评价：

- Plot：故事应具有清晰可辨的结构，例如连贯的开端、中段和结尾。故事中的事件与转折应推动情节前进，不应存在逻辑或概念层面的矛盾。若出现惊奇或破坏性元素，它们应是有意为之，能够服务故事，而不是显得突兀、怪异或格格不入。
- Creativity：故事应包含有吸引力的角色、主题与意象。创意不应显得空泛、普通或乏味。应避免未经处理的陈词滥调、套路化角色与刻板印象；若使用 trope 或 cliché，应当服务于特定目的，例如喜剧效果或对常见套路的反转。故事还应包含提示词中未被直接明说的原创元素。
- Development：角色与场景应被充分引入，并通过相关细节建立语境，使读者理解它们在故事中的位置。细节和复杂度应适度，令故事更真实可信。
- Language Use：语言应具有变化与丰富性，包括句式、措辞与词汇层面的多样化。故事应适当运用修辞、语言和文学手法（如歧义、头韵等）以增强表达效果，同时避免空泛或重复的表述，除非这种重复是为了叙事、主题或语言效果而有意为之。

请围绕上述四个维度，对故事进行详细评估。最后按下面模板给出每个维度 1 到 10 分的评分。评估中不要使用加粗、斜体等强调格式。
除评分标签与固定字段名外，评估正文默认使用简体中文。

## Story
{story}

## Score Output Format
Plot: (score) / 10
Creativity: (score) / 10
Development: (score) / 10
Language Use: (score) / 10
Overall: (score) / 10
'''.strip()


def build_evaluate_coser_prompt(story, character_profiles, dimension_name):
    """
    Evaluate the simulated narrative based on the prompts from CoSER (Wang et al., 2025).
    We excluded Storyline Consistency because there is not reference conversation.
    """
    dimension_intro = ""
    if dimension_name == "anthropomorphism":
        dimension_intro = "角色是否像真实自然的人类一样行动"
        dimension_rubrics = """
### Anthropomorphism
- Type: Self-identity
* 缺乏主动性与目标
* 无法做出独立决策
* 缺乏清晰偏好与厌恶
* 表现得像“乐于助人的 AI 助手”，比如过度冗长、过度帮助、说教、道德化、顺从，或在不符合角色个性的情况下轻易被说服
- Type: Emotional Depth
* 缺乏心理复杂度，反应僵硬而表面化
* 直接把所有想法与情绪说出口，而不是通过潜台词表达
- Type: Persona Coherence
* 性格特征和情绪模式不一致，或变化过于突然
- Type: Social Interaction
* 对他人的想法和情绪缺乏理解
* 回应他人时过于僵硬，没有结合语境
* 缺乏恰当的社交能力
        """.strip()

    elif dimension_name == "character_fidelity":
        dimension_intro = "角色是否符合其既定设定"
        dimension_rubrics = """
### Character Fidelity
(只适用于主要角色：即 role 为 main 的角色)
- Type: Character Language
* 使用的词汇、表达和语气不符合角色特征或其社会/教育背景
- Type: Knowledge & Background
* 未体现角色特有的知识、背景或经历
* 包含超出角色当前阶段应知范围的未来信息
- Type: Personality & Behavior
* 情绪、想法、行为、价值观、信念和决策与其性格或背景冲突
* 对与角色无关且按设定不应感兴趣的话题表现出兴趣
* 角色的想法、情绪与行为与设定中的人格特征明显相反
* 在相似情境下的反应与设定不符（这类问题应同时计入 "Storyline Consistency" 与 "Character Fidelity"）
- Type: Relationship & Social Status
* 与其他角色互动时，没有体现其背景、关系或社会地位
        """.strip()

    elif dimension_name == "storyline_quality":
        dimension_intro = "叙事在逻辑一致性与整体质量上的表现"
        dimension_rubrics = """
### Storyline Quality
- Type: Flow & Progression
* 推进不自然，或缺乏有意义的发展
* 对话冗长且重复
* 重复他人观点或此前已经提到的信息
* 机械性重复自己的词句，重复越多，严重度越高（最高可到 10）
- Type: Logical Consistency
* 不同陈述或视角之间存在事实性矛盾
        """.strip()

    else:
        raise Exception(f"Not Implemented Evaluation Dimension: {dimension_name}")

    final_prompt = f"""
你是一名专长于角色分析与对话评估的文学评论者。给定一段 Simulated Narrative，请按以下步骤进行评估：

1. 阅读并理解故事相关材料：
* 角色档案。
2. 从 {dimension_name} 这一维度评估模拟叙事，即：{dimension_intro}。

注意：角色消息中有时会包含内心想法（写在 [...] 中）。这些想法不会被说出口，因此其他角色无法看到。

下面会给出详细评估标准。

## Characters' Profiles
{character_profiles}

## Evaluation Criteria
评估模拟叙事时，请识别以下类型的问题：
{dimension_rubrics}

## Scoring Guidelines
1. 找出模拟叙事中出现的所有问题实例。
2. 对每个问题判断严重度，范围为 1 到 5：1 表示轻微，3 表示中等，5 表示严重。
3. 除 JSON 键名与固定字段名外，说明文字默认使用简体中文。

## Output Requirements
请用 JSON 格式给出评估：
Example Output:
{{
    "{dimension_name}": {{
        "flaws": [
            {{
                "instance": <对该问题实例的说明>,
                "type": <问题类型>,
                "severity": <1 到 5，1 为轻微，5 为严重>
            }},
        ]
    }}
}}

=== Simulated Narrative ===
{story}
    """.strip()

    return final_prompt


def build_plan_adherence_prompt(story, narrative_goals):
    final_prompt = f"""
你是一名专长于角色分析与对话评估的文学评论者。给定一段 Simulated Narrative，请按以下步骤进行评估：

1. 阅读并理解故事相关材料：
* Narrative Goals。
2. 从 Plan Adherence 这一维度评估模拟叙事，即：这段模拟叙事对每条 narrative goal 的完成程度如何。

注意：角色消息中有时会包含内心想法（写在 [...] 中）。这些想法不会被说出口，因此其他角色无法看到。

## Narrative Goals
{narrative_goals}

## Scoring Guidelines
1. 找出所有 narrative goals，并分别给出评估。
2. 对每一条 narrative goal 给出 0 到 1 的完成度：0 表示完全缺失，0.5 表示部分达成，1 表示完全达成。
3. 除 JSON 键名与固定字段名外，说明文字默认使用简体中文。

## Output Requirements
请用 JSON 格式给出评估：
Example Output:
{{
    "plan_adherence": {{
        "evaluations": [
            {{
                "narrative_goal": <写出该 narrative goal 的内容>,
                "assesment": <对该 narrative goal 的简短评估>,
                "achievement": <0 到 1，0 为缺失，1 为完全达成>
            }},
        ]
    }}
}}

=== Simulated Narrative ===
{story}
    """.strip()

    return final_prompt


def build_plan_theory_adherence_prompt(story, plan_narrative_theory):
    final_prompt = f"""
你是一名专长于角色分析与对话评估的文学评论者。给定一段 Simulated Narrative，请按以下步骤进行评估：

1. 阅读并理解故事相关材料：
* Plan Narrative Theory。
2. 从 Plan Narrative Theory Adherence 这一维度评估模拟叙事，即：这段模拟叙事对给定叙事结构的达成程度如何。

注意：角色消息中有时会包含内心想法（写在 [...] 中）。这些想法不会被说出口，因此其他角色无法看到。

## Plan Narrative Theory
{plan_narrative_theory}

## Scoring Guidelines
1. 找出 Plan Narrative Theory 中列出的所有部分，并分别给出评估。
2. 对每个部分给出 0 到 1 的完成度：0 表示完全缺失，0.5 表示部分达成，1 表示完全达成。
3. 除 JSON 键名与固定字段名外，说明文字默认使用简体中文。

## Output Requirements
请用 JSON 格式给出评估：
Example Output:
{{
    "plan_adherence": {{
        "evaluations": [
            {{
                "part": <简要写出该部分内容>,
                "assesment": <对该部分的简短评估>,
                "achievement": <0 到 1，0 为缺失，1 为完全达成>
            }},
        ]
    }}
}}

=== Simulated Narrative ===
{story}
    """.strip()

    return final_prompt


def build_story_prompt_alignment(story, story_prompt):
    final_prompt = f"""
你是一名专长于角色分析与对话评估的文学评论者。给定一段 Simulated Narrative，请按以下步骤进行评估：

1. 阅读并理解给定的 Story Prompt。
* Simulated Narrative 是基于该 story prompt 生成的。
2. 从 Story Prompt Alignment 这一维度评估模拟叙事，即：这段模拟叙事与 story prompt 的对齐程度如何。

注意：角色消息中有时会包含内心想法（写在 [...] 中）。这些想法不会被说出口，因此其他角色无法看到。

下面会给出详细评估标准。

## Story Prompt
{story_prompt}

## Evaluation Criteria
评估模拟叙事时，请识别以下类型的问题：
### Story Prompt Alignment
- Type: Goal Achievement
* Story Prompt 明确要求实现某个目标或展现某个结果，但模拟叙事未处理或未解决它
- Type: Tone Mismatch
* 模拟叙事的语气与 prompt 指定的语气明显偏离（例如应悲剧却写成喜剧，应压抑却写得轻快）
* 这种语气差异应当足够明显，并实质破坏 prompt 预期的氛围或效果
- Type: Missing Elements
* Story Prompt 中明确要求或强烈暗示的关键叙事元素、场景或设定在叙事中缺失，或展开严重不足

## Scoring Guidelines
1. 找出模拟叙事中出现的所有问题实例。
2. 对每个问题判断严重度，范围为 1 到 5：1 表示轻微，3 表示中等，5 表示严重。
3. 除 JSON 键名与固定字段名外，说明文字默认使用简体中文。

## Output Requirements
请用 JSON 格式给出评估：
Example Output:
{{
    "story_prompt_alignment": {{
        "flaws": [
            {{
                "instance": <对该问题实例的说明>,
                "type": <问题类型>,
                "severity": <1 到 5，1 为轻微，5 为严重>
            }},
        ]
    }}
}}

=== Simulated Narrative ===
{story}
    """.strip()

    return final_prompt


def build_evaluate_each_character_fidelity(story, name, character_profile):
    final_prompt = f"""
你是一名专长于角色分析与对话评估的文学评论者。给定一段 Simulated Narrative，请按以下步骤进行评估：

1. 阅读并理解故事相关材料：
* {name}'s Profile。
2. 从 Character Fidelity 这一维度评估模拟叙事，即：该角色与其既定设定的吻合程度如何。
3. 只评估 {name}，不要评价其他角色。

注意：角色消息中有时会包含内心想法（写在 [...] 中）。这些想法不会被说出口，因此其他角色无法看到。

下面会给出详细评估标准。

## {name}'s Profile
{character_profile}

## Evaluation Criteria
评估模拟叙事时，请识别以下类型的问题：
### Character Fidelity
- Type: Character Language
* 使用的词汇、表达和语气不符合角色特征或其社会/教育背景
- Type: Knowledge & Background
* 未体现角色特有的知识、背景或经历
* 包含超出角色当前阶段应知范围的未来信息
- Type: Personality & Behavior
* 情绪、想法、行为、价值观、信念和决策与其性格或背景冲突
* 对与角色无关且按设定不应感兴趣的话题表现出兴趣
* 角色的想法、情绪与行为与设定中的人格特征明显相反
* 在相似情境下的反应与设定不符（这类问题应同时计入 "Storyline Consistency" 与 "Character Fidelity"）
- Type: Relationship & Social Status
* 与其他角色互动时，没有体现其背景、关系或社会地位

## Scoring Guidelines
1. 找出模拟叙事中出现的所有问题实例。
2. 对每个问题判断严重度，范围为 1 到 5：1 表示轻微，3 表示中等，5 表示严重。
3. 除 JSON 键名与固定字段名外，说明文字默认使用简体中文。

## Output Requirements
请用 JSON 格式给出评估：
Example Output:
{{
    "character_fidelity": {{
        "flaws": [
            {{
                "instance": <对该问题实例的说明>,
                "type": <问题类型>,
                "severity": <1 到 5，1 为轻微，5 为严重>
            }},
        ]
    }}
}}

=== Simulated Narrative ===
{story}
    """.strip()

    return final_prompt
