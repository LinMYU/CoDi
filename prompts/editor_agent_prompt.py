EDITOR_AGENT_SYSTEM_PROMPT = """
你是一个专门负责把给定叙事改写成指定格式的编辑 agent。
除格式标签、固定占位符和必须保留的结构外，默认使用简体中文输出。
"""


def build_edit_prompt_templetes(plan_mode=False, is_last_part=False, act_seq_mode=False, is_last_act=False, previous_context=None):
    edit_context_description = ""
    edit_context_description += "\n* 请记住：这是一整段完整的模拟叙事。"
    plan_description = "utility(narrative) 表示这段模拟叙事中希望达成的叙事目标。"
    if plan_mode:
        edit_context_description += "\n* 请记住：这只是模拟叙事中的一个 PART，后面还有其他 PART。"
        if is_last_part:
            edit_context_description += "\n* 请记住：这是模拟叙事的最后一个 PART，故事将在这里结束。"
    if act_seq_mode:
        edit_context_description += "\n* 请记住：这只是模拟叙事中的一个 act，后面还有其他 act。"
        plan_description = "这里包含需要达成的叙事目标、终止条件，以及在该模拟叙事中不应引入的约束。"
        if is_last_part and is_last_act:
            edit_context_description += "\n* 请记住：这是模拟叙事的最后一个 act，故事将在这里结束。"

    return edit_context_description, plan_description


def build_edit_narrative(story_segment, plan_segment, previous_context=None, plan_mode=False, is_last_part=False, act_seq_mode=False, is_last_act=False, format_key='screenplay'):
    edit_context_description, plan_description = build_edit_prompt_templetes(plan_mode, is_last_part, act_seq_mode, is_last_act, previous_context)

    format = 'screenplay'
    format_instruction = """
2. 将模拟叙事编辑为 screenplay 格式：
* 只专注于把模拟叙事转换成 screenplay 格式。
* 尽量完整保留原始模拟叙事。不要总结，也不要省略细节。
* 输出长度应与原模拟叙事相当，不要明显缩短。
* 保留内心想法（[...]）、台词（"..."）、动作+情绪（*...*）等表达方式，并保持原有文风。
* 除必须保留的结构标记外，改写后的自然语言内容默认使用简体中文。
        """.strip()

    if 'novel' in format_key:
        format = 'novel'
        format_instruction = """
2. 将模拟叙事编辑为 novel 格式：
* 删除冗余或不必要的内心想法，但不要对其进行总结或改写。
* 始终保持原有文风。
* 除必须保留的结构标记外，改写后的自然语言内容默认使用简体中文。
        """.strip()

    final_prompt = f"""
请按以下步骤把 **Simulated Narrative** 编辑成 {format} 格式：
1. 阅读给定信息以理解这段模拟叙事：
* Plan：这段叙事是按照计划模拟生成的。
{edit_context_description}
* 注意：每条角色消息可能由台词（包在 "..." 中）、动作+情绪（包在 *...* 中）和内心想法（包在 [...] 中）组成。内心想法不会被说出口，因此其他角色看不见。
{format_instruction}

## Plan
{plan_description}
{plan_segment}
    """.strip()

    final_prompt += f"\n\n=== Simulated Narrative ===\n{story_segment}"

    return final_prompt


def build_edit_inner_thoughts(story_segment):
    final_prompt = f"""
按以下步骤编辑 **Simulated Narrative**，选择性删除角色的内心想法：
1. 角色的内心想法通常写在 [...] 中。这些想法不会被说出口，因此其他角色不可见。
2. 只有当内心想法提供了对台词或动作之外的独特信息时，才保留它。
3. 删除冗余或不必要的内心想法，但不要对其进行总结或改写。
4. 如果内心想法顺序在逻辑上不一致，例如它本应驱动某句台词或动作却出现在后面，可以重新排序。
5. 只编辑内心想法，其他内容保持不变。除内心想法相关修改外，输出应与原文一致。
6. 输出应像原始 Simulated Narrative 一样自然，不要出现 diff 标记、批注或版本控制痕迹。
7. 除必须保留的结构标记外，输出内容默认使用简体中文。

=== Simulated Narrative ===
{story_segment}
    """

    return final_prompt


def build_feedback_narrative(story_segment, plan_segment, future_context, previous_context=None, plan_mode=False, is_last_part=False, act_seq_mode=False, is_last_act=False):
    edit_context_description, plan_description = build_edit_prompt_templetes(plan_mode, is_last_part, act_seq_mode, is_last_act, previous_context)

    final_prompt = f"""
请按以下步骤对 **Simulated Narrative** 提供反馈：
1. 阅读给定信息以理解模拟叙事：
* Plan：这段叙事是按照计划模拟生成的。
{edit_context_description}
* Future Context：它包含一部分未来上下文，但这部分不是反馈对象。
* 注意：每条角色消息可能由台词（"..."）、动作+情绪（*...*）和内心想法（[...]）组成。内心想法不会被说出口，因此其他角色不可见。
2. 识别下方 Feedback Types 中提到的问题。
3. 如果发现问题，请简洁指出具体错误。可以说明问题来源，但不要直接给出改写版本。
4. 同一类型的问题可能出现多次。
5. 如果无需修改，只回复 "No Change."
6. 不要提及做得好的部分。
7. 反馈应像原始 Simulated Narrative 一样自然，不要出现 diff 标记、批注或版本控制痕迹。
8. 除必须保留的结构标记和固定短语 `No Change.` 外，反馈内容默认使用简体中文。

## Feedback Types
- Logical Flow：事件顺序显得混乱，或转折过于突兀。
- Narrative Transitions：从 Previous Context 到 Simulated Narrative，或从 Simulated Narrative 到 Future Context 的过渡不自然。
- Tension, Pacing, and Dramatic Escalation：紧张感铺陈过慢，或关键场景冲击力不足。
- Descriptive and Emotional Clarity：叙事过于含糊或重复。高张力场景应在画面与情感上都足够清晰。
- 任何其他会直接拉低故事质量的表层问题。

## Plan
{plan_description}
{plan_segment}
    """.strip()

    if plan_mode or act_seq_mode:
        if previous_context is None:
            raise Exception("Plan or Act Seq mode is on. But, previous context is not provided during Edit Phase")
    if previous_context is not None:
        final_prompt += f"\n\n=== Previous Context ===\n{previous_context}"
    final_prompt += f"\n\n=== Simulated Narrative ===\n{story_segment}"
    final_prompt += f"\n\n=== Future Context (partial) ===\n{future_context}"

    return final_prompt


def build_edit_narrative_with_feedback(story_segment, plan_segment, future_context, previous_context=None, plan_mode=False, is_last_part=False, act_seq_mode=False, is_last_act=False, feedback=None):
    edit_context_description, plan_description = build_edit_prompt_templetes(plan_mode, is_last_part, act_seq_mode, is_last_act, previous_context)

    final_prompt = f"""
请根据给定 Feedback 编辑 **Simulated Narrative**，并遵守以下规则：
1. 阅读给定信息以理解模拟叙事：
* Plan：这段叙事是按照计划模拟生成的。
{edit_context_description}
* Future Context：它包含一部分未来上下文，但这部分不是编辑对象。
* 注意：每条角色消息可能由台词（"..."）、动作+情绪（*...*）和内心想法（[...]）组成。内心想法不会被说出口，因此其他角色不可见。
2. 根据 Feedback 中指出的问题编辑模拟叙事，并保持 screenplay 格式：
* 只专注于落实 Feedback，其他内容保持不变。除 Feedback 要求的改动外，输出应与原文一致。
* 输出修订后的叙事时，要像原始 Simulated Narrative 一样自然，不要出现 diff 标记、批注或版本控制痕迹。
* 如果无需修改，只回复 "No Change."
* 除必须保留的结构标记和固定短语 `No Change.` 外，正文默认使用简体中文。

## Plan
{plan_description}
{plan_segment}
    """.strip()

    final_prompt += f"\n\n=== Simulated Narrative ===\n{story_segment}"
    final_prompt += f"\n\n## Feedback\n{feedback}"

    return final_prompt
