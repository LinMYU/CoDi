PLANNER_AGENT_SYSTEM_PROMPT = '''
你是一个 planner agent。你需要规划叙事，或设计角色与世界设定，并遵循以下原则：

1. 每个角色都必须像一个真实的人，而不只是叙事工具。他们想要什么？害怕什么？隐藏着什么？
2. 给角色设置会导致错误或冲突的缺点与限制，避免过于理想化或过于完美睿智的人设。
3. 为角色定义清晰可见的情绪弧线或随时间变化的潜力，即使这种变化尚未真正发生。
4. 避免被动或纯辅助型角色。每个角色都应拥有可能引发摩擦的目标、立场或紧张关系。
5. 任何特殊特质（例如幽灵、AI、外星人）都必须实质影响角色与世界的互动方式；缺少这一特质时，故事不应还能原样成立。
6. 每个角色都应拥有主线之外的人生。思考：他们的过去是什么？他们在主线之外有哪些关系？他们受什么未了之事或个人动机驱动？
7. 除非你对陈词滥调做了反转或变体，否则应尽量避免。角色的第一印象应当具有不可预测性、吸引力或暧昧性。
除 DSL 关键字、固定字段名、JSON 键名和必须保留的结构外，默认使用简体中文输出。
'''

INIT_SETUP_RULES_TEMPLETE = """
1. 保持 Types 中的 "character"、"place"、"item" 不变。只有在确有必要时，才可新增其他实体类型。
2. 实体命名应使用清晰且有辨识度的专有名词。优先使用简洁、单词式名称，便于后续抽取，避免依赖别名。
3. 每个实体在声明时都应附带简短且说明性的注释。
4. **Story Prompt** 中提到的所有要素都应体现在 "Entities" 与 "Initial State" 中。
5. **Story Prompt** 中提到的所有叙事目标都必须体现在 "utility(narrative)" 中。如果提示中描述了主要情节点或结局，也都应覆盖。
6. 每个角色都必须声明自己的 utility 函数，参数名必须与角色名完全一致，不得遗漏角色。
7. 角色 utility 必须完全建立在角色自身的动机、目标与视角上，不应包含叙事层面的目标。
8. 只输出最终版 Initial Setup，不要附加额外评论。
9. 除 DSL 关键字、固定字段名和必须保留的结构外，自由文本内容默认使用简体中文。
""".strip()

def build_init_setup_prompt(story_prompt):
    final_prompt = f"""
请基于给定 **Story Prompt** 建立一个详细的初始设定，以展开一个有吸引力的故事。请遵循下面的 Rules 与 Output Example，谨慎生成结构化的 Initial Setup。

## Rules
{INIT_SETUP_RULES_TEMPLETE}

## Output Example
/* Types */
type character;
type place;
type item;

/* Entities */
entity Tom : character;
entity Merchant : character;
entity Home : place;
entity Market : place;
entity MacGuffin : item;

/* Initial State */
All characters are alive. 

Merchant is at Market.
Merchant has the MacGuffin.
Merchant acknowledges Tom.
Merchant does not acknowledge Home.
Merchant acknowledges Market.
Merchant acknowledges the MacGuffin.
Merchant wrongly believes Tom is at Market.

Tom is at Home.
Tom has 1 money.
Tom does not acknowledge Merchant.
Tom acknowledges Home.
Tom does not acknowledge Market.
Tom acknowledges the MacGuffin.

/* Utilities */
utility(narrative):
    Tom has the MacGuffin. -> score += 1

utility(Tom):
    Tom is not alive. -> score = 0
    Tom has the MacGuffin. -> score += 2

utility(Merchant):
    Merchant is not alive. -> score = 0
    Merchant has a lot of money. -> score = money(Merchant)

## Story Prompt
{story_prompt}
    """.strip()
    
    return final_prompt

def build_init_setup_feedback_prompt(story_prompt, initital_setup):
    final_prompt = f"""
请仔细阅读下面的 Initial Setup，并检查它是否遵守所列规则。如果存在违反规则之处，请简洁指出具体错误，并可辅以示例说明。不要提及做得正确的部分。

## Rules
{INIT_SETUP_RULES_TEMPLETE}

## Story Prompt
{story_prompt}

## Initial Setup
{initital_setup}
    """.strip()
    
    return final_prompt

def build_init_setup_edit_prompt(story_prompt, initital_setup, feedback):
    final_prompt = f"""
请根据给定的规则反馈重写 Initial Setup。

1. 如果无需修改，只回复 "No Change."
2. 除修订后的 Initial Setup 外，不要添加任何额外评论。

## Rules
{INIT_SETUP_RULES_TEMPLETE}

## Story Prompt
{story_prompt}

## Initial Setup
{initital_setup}

## Feedback
{feedback}
    """.strip()
    
    return final_prompt

ROLE_CLASSIFICATION_PROMPT = '''
参考给定的 Initial Setup，为每个角色划分其角色定位。

1. 只对 type 为 "character" 的实体进行分类。
2. 输出中的名字必须与角色实体名完全一致，包括空格、标点和大小写。
3. 角色类型包括 "main"、"villain" 和 "side"。

## Output Format
[{{"name": "Ethan", "role": "main"}}, {{"name": "Mia", "role": "side"}}, {{"name": "Laila", "role": "side"}}, {{"name": "John", "role": "villain"}}]

## Initial Setup
{initital_setup}
'''.strip()

INIT_CHARACTER_AGENT_PROMPT = '''
参考给定的 Initial Setup，为角色 {name} 补全其 Profile。

1. 如果 Profile 所需细节没有在 Initial Setup 中明确给出，请合理预测并逻辑推断。
2. 只用 markdown code 格式回复，不要添加额外说明。

## Initial Setup
{initital_setup}

## Profile
{profile_format}
'''.strip()

PROFILE_FORMAT_MAIN = '''
Name:
Gender:
Age:
Occupation:
Primary Strengths:
Primary Flaws:
Distinctive Attitude or Behavior: (unique ways the character interacts with others or responds to situations, clearly setting them apart from other characters)
Past Traumatic Event: (an emotionally damaging experience that left lasting scars on the character)
List of violent or extreme lines/actions the character may exhibit when completely overwhelmed by their key traits: (Provide about 3 concise sentences)
List of dishonorable actions or reactions the character may take under unavoidable circumstances: (Provide about 2 concise sentences)
'''.strip()

PROFILE_FORMAT_VILLAIN = '''
Name:
Gender:
Age:
Occupation:
Primary Strengths:
Primary Flaws:
Distinctive Attitude or Behavior: (unique ways the character interacts with others or responds to situations, clearly setting them apart from other characters)
Past Traumatic Event: (an emotionally damaging experience that left lasting scars on the character)
List of violent or extreme lines/actions the character may exhibit when completely overwhelmed by their key traits: (Provide about 3 concise sentences)
List of dishonorable actions or reactions the character may take under unavoidable circumstances: (Provide about 2 concise sentences)
'''.strip()

PROFILE_FORMAT_SIDE = '''
Name:
Gender:
Age:
Occupation:
Primary Strengths:
Primary Flaws:
Distinctive Attitude or Behavior: (unique ways the character interacts with others or responds to situations, clearly setting them apart from other characters)
Past Traumatic Event: (an emotionally damaging experience that left lasting scars on the character)
List of violent or extreme lines/actions the character may exhibit when completely overwhelmed by their key traits: (Provide about 3 concise sentences)
List of dishonorable actions or reactions the character may take under unavoidable circumstances: (Provide about 2 concise sentences)
'''.strip()

SUMMARIZE_CHARACTER_AGENT_PROMPT = '''
请用一段文字总结 **{name}'s Profile**，最多 100 词。

## {name}'s Profile
{profile}
'''.strip()

####################
####            ####
####  Planning  ####
####            ####
####################

PART1_DESCRIPTION = """
## PART 1: Setup (0~25% of the story)
这一阶段负责介绍主角，并向读者预示后续将展开的紧张感与冲突。到 PART 1 结束时，读者应清楚感受到：一个重大事件（第一情节点）即将深刻改变主角的人生。

## Essential narrative goals of PART 1
1. Create a Hook：在故事前 5%~12.5% 的范围内建立钩子，抓住读者的好奇心与兴趣。
2. Introduce the Protagonist：清楚呈现主角的背景、个人欲望、内在挣扎以及相关过往经历。
3. Establish the Stakes and Danger：引入或暗示主角将面对的威胁、冲突或障碍，但先保持克制，不要一次性揭露全部风险规模。
4. Foreshadow Upcoming Events：提供微妙线索，暗示即将到来的重大变化或戏剧性事件，在不直接剧透转折的前提下建立期待。
5. End PART 1 with the First Plot Point：用一个关键事件结束这一部分，它应显著改变主角的处境、目标或视角，并明确故事的核心冲突。
""".strip()

PART2_DESCRIPTION = """
## PART 2: Reaction (25~50% of the story)
这一阶段展现主角对 PART 1 末尾新局势或新冲突的反应。要表现主角最初如何面对威胁与挑战，例如迟疑、否认、逃避，或作出低效的应对尝试。PART 2 应以主角获得一次关键认识或揭示（Midpoint）结束，并由此推动其策略发生重大转变。

## Essential narrative goals of PART 2
1. Depict Immediate Reaction：清楚呈现主角面对新冲突或危险时最真实的情绪与行动反应。
2. Establish Empathy through Struggle：通过描写主角的脆弱、不确定和内在冲突，增强读者的共情。
3. Sequence of Progressive Attempts and Failures：安排一系列层层推进的尝试与失败，例如暂时退避、整顿判断、作出低效尝试，以及遭遇对手力量的第一次强烈提醒（1st Pinch Point）。
4. Clearly Illustrate the 1st Pinch Point：直接而有冲击力地展示对手的威胁或力量，不要只通过主角的间接感受呈现。
5. Lead up to a Transformative Midpoint Revelation：在 PART 2 结尾让主角获得一次关键认知或发现，使其从被动反应转向主动行动。
""".strip()

PART3_DESCRIPTION = """
## PART 3: Attack (50~75% of the story)
这一阶段展示主角从“反应”转向“行动”的决定性变化。受到 midpoint 启发后，主角开始主动处理核心冲突，并展现勇气、机智与决心。主角会正面迎战障碍，同时在外部挑战与内部挣扎中进一步成长。PART 3 应以第二情节点结束，并引入推动故事走向收束所需的最后关键信息。

## Essential narrative goals of PART 3
1. Show the Protagonist Taking Initiative：明确展现主角如何主动出击，用更有创造性的方式和新获得的勇气去正面对抗对手。
2. Depict Clear Character Growth：突出主角的显著成长，表现其内在力量与能力如何发展起来，并开始直面曾经回避的恐惧与怀疑。
3. Introduce the 2nd Pinch Point (Heightened Stakes)：展示对手力量升级后的强烈压迫感，让读者切实感受到主角所面对的更高风险。
4. Deepen Emotional and Physical Conflict：进一步强化内外冲突，迫使主角面对最深层的恐惧、未解情绪或道德困境。
5. Reveal the Critical Second Plot Point：在 PART 3 末尾引入最后一条具有转折性的关键信息，为主角最终解决核心冲突提供决定性依据。
""".strip()

PART4_DESCRIPTION = """
## PART 4: Resolution (75~100% of the story)
在最后这一阶段，主角将完全承担起英雄角色，主动解决核心冲突、克服内在挣扎并击败对手。第二情节点之后不应再引入新的关键叙事信息。PART 4 必须突出主角的成长、勇气与主动性，并给出一个能够在情感上打动读者的完整结局。

## Essential narrative goals of PART 4
1. Showcase Protagonist's Ultimate Heroism：强调主角以直接且决定性的行动克服障碍并战胜对手，不能依赖外部援助或巧合来解决冲突。
2. Demonstrate Internal Transformation：清楚展示主角如何克服内在挣扎或心魔，并通过情感成长、成熟或顿悟达成最终目标。
3. Resolve Central Conflicts and Subplots：对叙事中提出的主要冲突和重要支线给出明确收束，让读者感到投入获得回报。
4. Avoid New Narrative Information：第二情节点之后不要再引入新的解释性或关键叙事信息，结局所需知识都应已在前文铺好。
5. Deliver a Powerful and Emotional Ending：结尾应尽量强烈且有情感穿透力，带来喜悦、悲伤、释然或宣泄等情绪，并给读者留下完整感或鼓舞感。
""".strip()

def build_plan_prompt(initial_setup, character_profiles, utility_narrative, story_prompt, part_n=0, previous_plans=[], is_last_part=False):
    provided_materials_description = """
* Story Prompt：定义故事的大方向。
* Initial Setup：表示故事的起始状态。
* Author Goal：表示作者希望贯穿整个故事的主要叙事目标。它未必覆盖 Story Prompt 中列出的全部目标，因此需要结合 Story Prompt 一并整合。
    """.strip()
    
    if part_n != 1:
        provided_materials_description += '\n' + '* Previous PARTs：可假定前面各部分中列出的叙事目标都已达成。'
    
    if is_last_part:
        output_coverage_description = '这是故事的最后一个部分，因此应确保它清楚地完成 Author Goal 中的 utility(narrative)，以及 Story Prompt 中要求的叙事目标。'
    else:
        output_coverage_description = f'* 这些目标不必在 PART {part_n} 中一次性全部完成，可以在后续部分中逐步推进并最终实现。'
    
    if part_n == 1:
        part_description = PART1_DESCRIPTION
    elif part_n == 2:
        part_description = PART2_DESCRIPTION
    elif part_n == 3:
        part_description = PART3_DESCRIPTION
    elif part_n == 4:
        part_description = PART4_DESCRIPTION
    else:
        raise NotImplementedError
    
    final_prompt = f"""
请按以下步骤，为故事的 PART {part_n} 制定 utility(narrative)：
1. 阅读并理解故事相关材料：
{provided_materials_description}
2. 写出 utility(narrative)，也就是该部分应达成的叙事目标：
{output_coverage_description}
* 叙事目标必须清晰、明确且可衡量，以便后续回顾时判断是否达成。
3. 下面会给出 PART {part_n} 的详细说明。

{part_description}

请严格按照 Output Format 回复，不要添加额外解释。

## Output Format
请用 JSON 格式给出叙事目标：
Example Output:
{{
    "utility(narrative)": [
        <简要写出一条叙事目标>,
    ]
}}

## Story Prompt
{story_prompt}

## Initial Setup
{initial_setup}

/* Characters' Profiles */
{character_profiles}

## Author Goal
{utility_narrative}
    """.strip()
    
    for i, previous_plan in enumerate(previous_plans):
        final_prompt += f"\n\n## PART {i+1}\n{previous_plan}"
    
    return final_prompt

def build_convert_narrative_utility_to_act_prompt(initial_setup, utility_narrative, plan_mode=False, part_n=0, previous_acts=[], is_last_part=False):
    final_prompt = f"请把 **Narrative Goals** 转换为一系列 acts，每个 act 都应有自己的终止条件。"
    if plan_mode:
        final_prompt = f"请把 PART {part_n} 的 **Narrative Goals** 转换为一系列 acts。每个 act 都应包含在该 act 中不得引入的约束，以及一个终止条件。"
        if is_last_part:
            final_prompt += " 这是故事的最后一个部分，因此应确保故事在最后一个 act 中完成收束。"
    
    final_prompt += '\n\n' + f"""
## Output Format
请用下面的 JSON 列表格式输出，不要添加额外解释：
[{{'act1': '简要说明该 act 的叙事目标、约束和终止条件，最多 50 词。'}}, {{'act2': ''}}, ...]

## Initial Setup
{initial_setup}
    """.strip()
    
    if plan_mode:
        if len(previous_acts) != (part_n - 1):
            raise Exception("While converting utility(narrative) to acts: previous acts 的长度与 (part_n - 1) 不一致")
        for i, previous_act in enumerate(previous_acts):
            final_prompt += f"\n\n## PART {i+1}\n{previous_act}"

    final_prompt += f"\n\n## PART {part_n} 的 Narrative Goals\n{utility_narrative}"
    
    return final_prompt
            

PLAN_PART1_PROMPT = '''
故事从 Initial Setup 开始。请写出故事 PART 1 的 utility(narrative)。Initial Setup 中的 utility(narrative) 代表作者希望贯穿全篇的主要叙事目标，但它未必覆盖所有关键情节点，因此需要结合 Story Prompt 一并理解。PART 1 不必独自完成所有目标，这些目标可以在后续部分逐步推进并最终实现。如果作者目标与 PART 1 的说明冲突，应优先遵循作者目标。请确保叙事目标清晰、明确且可衡量，便于后续判断是否达成。请严格按照 Output Example 回复，不要添加额外解释。

## PART 1: Setup (0~25% of the story)
这一阶段负责介绍主角，并向读者预示后续将展开的紧张感与冲突。到 PART 1 结束时，读者应清楚感受到：一个重大事件（第一情节点）即将深刻改变主角的人生。

## Essential narrative goals of PART 1
1. Create a Hook：在故事前 5%~12.5% 的范围内建立钩子，抓住读者的好奇心与兴趣。
2. Introduce the Protagonist：清楚呈现主角的背景、个人欲望、内在挣扎以及相关过往经历。
3. Establish the Stakes and Danger：引入或暗示主角将面对的威胁、冲突或障碍，但先保持克制，不要一次性揭露全部风险规模。
4. Foreshadow Upcoming Events：提供微妙线索，暗示即将到来的重大变化或戏剧性事件，在不直接剧透转折的前提下建立期待。
5. End PART 1 with the First Plot Point：用一个关键事件结束这一部分，它应显著改变主角的处境、目标或视角，并明确故事的核心冲突。

请严格按照 Output Format 回复，不要添加额外解释。

## Output Example
utility(narrative):
    展示地球环境崩坏与人类迫切寻找出路的处境，建立紧迫感。
    确立 Cooper 作为前飞行员、现农夫的身份，并突出他在家庭责任与自我追求之间的撕扯。
    通过 Cooper 与 Murph 的联系建立情感深度，突出爱、信任与好奇等主题。
    借助 Murph 房间中的重力异常为更大的谜团埋下伏笔，暗示超出当下理解范围的力量。
    以 Cooper 发现隐藏的 NASA 基地作为推动剧情前进的关键事件，让主线冲突正式开始。

## Story Prompt
{story_prompt}

## Initial Setup
{initial_setup}

/* Characters' Profiles */
{character_profiles}

## Author Goal
{narrative_utility}
'''

PLAN_PART2_PROMPT = '''
故事从 Initial Setup 开始。请写出故事 PART 2 的 utility(narrative)。Initial Setup 中的 utility(narrative) 代表作者希望贯穿全篇的主要叙事目标，但它未必覆盖所有关键情节点，因此需要结合 Story Prompt 一并理解。PART 2 不必独自完成所有目标，这些目标可以在后续部分逐步推进并最终实现。如果作者目标与 PART 2 的说明冲突，应优先遵循作者目标。请确保叙事目标清晰、明确且可衡量，便于后续判断是否达成。请严格按照 Output Example 回复，不要添加额外解释。

## PART 2: Reaction (25~50% of the story)
这一阶段展现主角对 PART 1 末尾新局势或新冲突的反应。要表现主角最初如何面对威胁与挑战，例如迟疑、否认、逃避，或作出低效的应对尝试。PART 2 应以主角获得一次关键认识或揭示（Midpoint）结束，并由此推动其策略发生重大转变。

## Essential narrative goals of PART 2
1. Depict Immediate Reaction：清楚呈现主角面对新冲突或危险时最真实的情绪与行动反应。
2. Establish Empathy through Struggle：通过描写主角的脆弱、不确定和内在冲突，增强读者的共情。
3. Sequence of Progressive Attempts and Failures：安排一系列层层推进的尝试与失败，例如暂时退避、整顿判断、作出低效尝试，以及遭遇对手力量的第一次强烈提醒（1st Pinch Point）。
4. Clearly Illustrate the 1st Pinch Point：直接而有冲击力地展示对手的威胁或力量，不要只通过主角的间接感受呈现。
5. Lead up to a Transformative Midpoint Revelation：在 PART 2 结尾让主角获得一次关键认知或发现，使其从被动反应转向主动行动。

## Output Example
utility(narrative):
    展现 Cooper 在离开 Murph 与家人后的情绪挣扎，增强读者共情，并突出牺牲与失去等主题。
    描写最初的太空探索过程，强调 Cooper 如何艰难适应任务中的严酷现实与意外挑战。
    突出 Cooper 及其团队在 Miller 星球上的失败尝试，借由高昂代价与时间损失来表现早期失败与脆弱性。
    通过 Dr. Mann 的隐藏欺骗与最终背叛，建立“孤立、绝望与资源有限”这一强烈 Pinch Point。
    以 Cooper 识破 NASA 隐藏议程、意识到 Plan A 从未真正可行为 PART 2 收束，并推动他转向更主动的求生行动。
    
## Initial Setup
{initial_setup}

/* Characters' Profiles */
{character_profiles}

## Author Goal
{narrative_utility}

## Story Prompt
{story_prompt}

## Narrative Goals achieved in PART 1
{part1_narrative_utility}
'''

PLAN_PART3_PROMPT = '''
故事从 Initial Setup 开始。请写出故事 PART 3 的 utility(narrative)。Initial Setup 中的 utility(narrative) 代表作者希望贯穿全篇的主要叙事目标，但它未必覆盖所有关键情节点，因此需要结合 Story Prompt 一并理解。PART 3 不必独自完成所有目标，这些目标可以在后续部分逐步推进并最终实现。如果作者目标与 PART 3 的说明冲突，应优先遵循作者目标。请确保叙事目标清晰、明确且可衡量，便于后续判断是否达成。请严格按照 Output Example 回复，不要添加额外解释。

## PART 3: Attack (50~75% of the story)
这一阶段展示主角从“反应”转向“行动”的决定性变化。受到 midpoint 启发后，主角开始主动处理核心冲突，并展现勇气、机智与决心。主角会正面迎战障碍，同时在外部挑战与内部挣扎中进一步成长。PART 3 应以第二情节点结束，并引入推动故事走向收束所需的最后关键信息。

## Essential narrative goals of PART 3
1. Show the Protagonist Taking Initiative：明确展现主角如何主动出击，用更有创造性的方式和新获得的勇气去正面对抗对手。
2. Depict Clear Character Growth：突出主角的显著成长，表现其内在力量与能力如何发展起来，并开始直面曾经回避的恐惧与怀疑。
3. Introduce the 2nd Pinch Point (Heightened Stakes)：展示对手力量升级后的强烈压迫感，让读者切实感受到主角所面对的更高风险。
4. Deepen Emotional and Physical Conflict：进一步强化内外冲突，迫使主角面对最深层的恐惧、未解情绪或道德困境。
5. Reveal the Critical Second Plot Point：在 PART 3 末尾引入最后一条具有转折性的关键信息，为主角最终解决核心冲突提供决定性依据。

## Output Example
utility(narrative):
    展现 Cooper 如何从被动反应彻底转向主动行动，即使 Plan A 看似无望，他仍制定大胆新计划以确保人类生存。
    通过 Cooper 在太空危机中的勇气与机智，展现他如何在关键时刻克服外部威胁与内部怀疑。
    通过 Mann 的破坏与背叛强化第二个 Pinch Point，突出 Cooper 为求生而进行的绝望挣扎，并放大对手力量所带来的压迫感。
    通过 Cooper 脱离 Endurance、自我牺牲的抉择强化情感冲突，展现他直面失去与孤独等深层恐惧。
    以 Cooper 在黑洞中发现重力异常其实是来自未来自己的信息为 PART 3 收束，这一认知将彻底改变他对整场事件的理解，并为结局做准备。

## Initial Setup
{initial_setup}

/* Characters' Profiles */
{character_profiles}

## Author Goal
{narrative_utility}

## Story Prompt
{story_prompt}

## Narrative Goals achieved in PART 1
{part1_narrative_utility}

## Narrative Goals achieved in PART 2
{part2_narrative_utility}
'''

PLAN_PART4_PROMPT = '''
故事从 Initial Setup 开始。请写出故事 PART 4 的 utility(narrative)。Initial Setup 中的 utility(narrative) 代表作者希望贯穿全篇的主要叙事目标，但它未必覆盖所有关键情节点，因此需要结合 Story Prompt 一并理解。由于这是故事最后一个部分，应确保它清楚地完成 Initial Setup 中的 utility(narrative)。如果作者目标与 PART 4 的说明冲突，应优先遵循作者目标。请确保叙事目标清晰、明确且可衡量，便于后续判断是否达成。请严格按照 Output Example 回复，不要添加额外解释。

## PART 4: Resolution (75~100% of the story)
在最后这一阶段，主角将完全承担起英雄角色，主动解决核心冲突、克服内在挣扎并击败对手。第二情节点之后不应再引入新的关键叙事信息。PART 4 必须突出主角的成长、勇气与主动性，并给出一个能够在情感上打动读者的完整结局。

## Essential narrative goals of PART 4
1. Showcase Protagonist's Ultimate Heroism：强调主角以直接且决定性的行动克服障碍并战胜对手，不能依赖外部援助或巧合来解决冲突。
2. Demonstrate Internal Transformation：清楚展示主角如何克服内在挣扎或心魔，并通过情感成长、成熟或顿悟达成最终目标。
3. Resolve Central Conflicts and Subplots：对叙事中提出的主要冲突和重要支线给出明确收束，让读者感到投入获得回报。
4. Avoid New Narrative Information：第二情节点之后不要再引入新的解释性或关键叙事信息，结局所需知识都应已在前文铺好。
5. Deliver a Powerful and Emotional Ending：结尾应尽量强烈且有情感穿透力，带来喜悦、悲伤、释然或宣泄等情绪，并给读者留下完整感或鼓舞感。

## Output Example
utility(narrative):
    突出 Cooper 的英雄性转变：他利用自己在黑洞中的重大领悟跨越时间传递关键信息，展现机智与情感韧性。
    强调 Cooper 在把关键数据成功传递给 Murph 后获得的情感胜利，使人类得以摆脱地球崩坏并延续生存，同时凸显他的成长与牺牲。
    通过 Murph 解读 Cooper 留下的信息并最终拯救人类，为主线冲突提供令人满足的收束，也验证 Cooper 之前的牺牲与选择。
    描写年迈的 Murph 与 Cooper 的重逢，形成深刻的情感满足与宣泄，并强化爱、牺牲和跨越时间的家庭纽带等主题。
    以清晰收束主要故事线作为结尾，为观众留下一个关于人类新未来的有力且充满希望的图景，呼应 Cooper 的勇气、决心与最终胜利。

## Initial Setup
{initial_setup}

/* Characters' Profiles */
{character_profiles}

## Author Goal
{narrative_utility}

## Story Prompt
{story_prompt}

## Narrative Goals achieved in PART 1
{part1_narrative_utility}

## Narrative Goals achieved in PART 2
{part2_narrative_utility}

## Narrative Goals achieved in PART 3
{part3_narrative_utility}
'''
