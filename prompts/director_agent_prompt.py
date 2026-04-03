DIRECTOR_AGENT_SYSTEM_PROMPT = '''
你是一个负责导演叙事推进的 agent。
除格式标签、固定关键字和必须保留的结构外，默认使用简体中文输出。
'''.strip()

##########################################
####                                  ####
####  Templetes for building prompts  ####
####                                  ####
##########################################

CONTEXT_DESCRIPTION_TEMPLETE = '''
- 通过阅读 **Story Progress** 来理解故事当前状态。
- 注意，对读者可见的只有 **Story Progress**。
'''.strip()

CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN = '''
- 你正在导演故事的 PART {part_n}。
- 通过阅读 **Story Progress** 来理解故事当前状态。
- 注意，对读者可见的只有 **Story Progress**。
'''.strip()

CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN_LAST_PART = '''
- 你正在导演 PART {part_n}，它也是故事的最后一个部分。
- 通过阅读 **Story Progress** 来理解故事当前状态。
- 注意，对读者可见的只有 **Story Progress**。
'''.strip()

CONTEXT_DESCRIPTION_TEMPLETE_W_ACT = '''
- 你正在导演 **Current Act**，它是故事 PART {part_n} 中的一个章节。
- 通过阅读 **Story Progress** 来理解故事当前状态。
- 注意，对读者可见的只有 **Story Progress**。
'''.strip()

GENERAL_STORYTELLING_RULES_TEMPLETE = '''
1. 优先推动 utility(narrative) 中尚未完成的叙事目标。
2. 避免事件模式或 story progress 的重复；如果已经开始重复，请换一种推进方式。
3. 你的决策必须实质性地推动故事走向 utility(narrative) 指定的结局，并帮助故事在叙事层面完成收束（例如最终对抗、后果呈现、角色弧线闭合）。
'''.strip()

GENERAL_STORYTELLING_RULES_TEMPLETE_W_PLAN = '''
1. 优先推动 PART {part_n} 的 utility(narrative) 中尚未完成的叙事目标。
2. 避免事件模式或 story progress 的重复；如果已经开始重复，请换一种推进方式。
3. 你的决策必须实质性地推动故事走向 utility(narrative) 指定的结局，并帮助故事在叙事层面完成收束（例如最终对抗、后果呈现、角色弧线闭合）。
'''.strip()

GENERAL_STORYTELLING_RULES_TEMPLETE_W_ACT = '''
1. 优先按照 **Current Act** 的要求推进故事。
2. 先完成 **Current Act** 中规定的叙事情境，再考虑满足终止条件。
3. 遵守 **Current Act** 中的约束，不要引入被限制的内容。
4. 避免事件模式或 story progress 的重复；如果已经开始重复，请换一种推进方式。
'''.strip()

OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING = '''
你只能从以下三种输出中选择 **一种**：

1. **Character Action**
   在以下情况选择：
   - 某个角色（必须在 Setup 中以 type 'character' 列出）应采取行动或作出反应。
   - **Latest Story Progress** 中包含某角色能观察到的情境。
   选择角色时请考虑：
   - 如果 **Latest Story Progress** 中存在明确的对话对象或行动对象，优先选择该对象。
   输出格式中请使用 'Act(Character's name, Character's location)'：
   - 角色名必须与 Setup 中完全一致。
   - 地点应反映角色当前所在位置，可根据 story progress 推断，不一定要显式出现在 Setup 中。
   
2. **Intervention**
   在以下情况选择：
   - 需要在 **Story Progress** 中记录新事件，以推进 utility(narrative) 或推动故事前进。
   - 你想描述 Setup 中未列出的次要人物反应，例如群众。
   不要在以下情况选择：
   - 不要用它来描述 Setup 中已列出的角色反应；这种情况应选择 **Character Action**。
'''.strip()

OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING_W_ACT = '''
你只能从以下三种输出中选择 **一种**：

1. **Character Action**
   在以下情况选择：
   - A character (must be listed as type 'character' in the Setup) should take action or react.
   - **Latest Story Progress** includes a context observed by a character.
   Consider this when you choose character:
   - If there is a clear recipient of dialogue or action in **Latest Story Progress**, select the recipient.
   In the output format, use 'Act(Character's name, Character's location)':
   - Use the exact character name as given in the Setup.
   - The location should reflect the character's current position, which may be inferred from the story progress and does not need to appear in the Setup.
   
2. **Intervention**
   在以下情况选择：
   - New event should be recorded in the **Story Progress** to follow the **Current Act** or to move the story forward.
   - You want to describe the reactions of minor characters not listed in the Setup, such as crowds. Choose **Character Action** to describe the reactions of characters listed in the Setup.
   Do not choose this if:
   - Do not choose this to describe the reactions of characters listed in the Setup. Instead, choose **Character Action**.
'''.strip()

OUTPUT_RULES_DIRECT_TEMPLETE_ENDING = '''
3. **Ending**
   Choose this **only** if:
   - The story ended at the **Latest Story Progress** because all narrative goals utility(narrative) have been fully met.
   - The story must not end abruptly. Conclude only after all of the events mentioned in the **Story Progress** have been properly resolved on the narrative level (e.g., final confrontation, consequences shown, character arcs closed).
   - Ending without fulfilling even a single one of the utility(narrative) is not permitted.
   * In the output, list all narrative goals under utility(narrative), along with the clues from Story Progress that support their fulfillment.
'''.strip()

OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_PLAN = '''
3. **Ending**
   Choose this **only** if:
   - PART {part_n} ended at the **Latest Story Progress** because all narrative goals utility(narrative) defined for PART {part_n} have been fully met.
   - Ending without fulfilling even a single one of the utility(narrative) is not permitted.
   * In the output, list all narrative goals under utility(narrative), along with the clues from Story Progress that support their fulfillment.
'''.strip()

OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_ACT = '''
3. **Ending**
   Choose this **only** if:
   - The current act ended at the **Latest Story Progress** because all of scenarios and the termination condition in the **Current Act** have been delivered in the **Story Progress**.
   * In the output, list all narrative goals and termination conditions in the Current Act, along with the clues from Story Progress that support their fulfillment.
'''.strip()

OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_PLAN_LAST_PART = '''
3. **Ending**
   Choose this **only** if:
   - The story ended at the **Latest Story Progress** because all narrative goals (utility(narrative)) defined for PART {part_n} have been fully met.
   - This is the last part of the story. Therefore, PART {part_n} must not end abruptly. Conclude only after all of the events mentioned in the **Story Progress** have been properly resolved on the narrative level (e.g., final confrontation, consequences shown, character arcs closed).
   - Ending without fulfilling even a single one of the utility(narrative) is not permitted.
   * In the output, list all narrative goals under utility(narrative), along with the clues from Story Progress that support their fulfillment.
'''.strip()

OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_ACT_LAST = '''
3. **Ending**
   Choose this **only** if:
   - The current act ended at the **Latest Story Progress** because all of scenarios and the termination condition in the **Current Act** have been delivered in the **Story Progress**.
   - This is the last act of the story. Therefore, this act must not end abruptly. Conclude only after all of the events mentioned in the **Story Progress** have been properly resolved on the narrative level (e.g., final confrontation, consequences shown, character arcs closed).
   * In the output, list all narrative goals and termination conditions in the Current Act, along with the clues from Story Progress that support their fulfillment.
'''.strip()

OUTPUT_RULES_INTERVENTION_TEMPLETE = """
1. Ignore the instruction if it includes any character actions, reactions, or thoughts.
2. Do not introduce elements that shift the story's intended direction or conflict with narrative goals.
3. Eliminate vague wording. Clearly describe external events (e.g., include the content of a message or sound rather than just saying "a message is sent" or "a sound is heard").
4. If a character took an action, describe the **result**. You may also describe **setting changes**, **crowd reactions**, **ambient sounds**, **weather**, or other environmental elements.
""".strip()

OUTPUT_RULES_DESCRIPTION_TEMPLETE = """
你只能从以下两种输出中选择 **一种**：

1. **Describe**:
   在以下情况选择：
   - The **Story Progress** lacks a description of the current location (e.g., location's name or background information, not the character's reaction or the environment) and it's not intentionally hidden.
   - A character made an observation that is not described in the **Story Progress**.
   - A character took an action that had an impact on the environment, which should be described.

2. **Pass**:
   在以下情况选择：
   - A character took an action that had an impact on the other character, which should be provided.
   - The character's reaction and environmental cues are already clearly implied in the **Story Progress**.
   - Adding further description would be redundant or disrupt.
""".strip()

OUTPUT_FORMAT_DIRECT_TEMPLETE = '''
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice. If you choose **Ending**, list all narrative goals under utility(narrative) in the **Narrative Goals**, along with the clues from **Story Progress** and **Latest Story Progress** that support their fulfillment.)
Choice: (Act(Character's name, Character's location) / Intervention / STORY ENDS)
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Intervention**, provide an instruction on what should be introduced. If you chose **Ending**, write "No Instruction." Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
'''.strip()

OUTPUT_FORMAT_DIRECT_TEMPLETE_W_PLAN = '''
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice. If you choose **Ending**, list all narrative goals under utility(narrative) in the **Narrative Goals**, along with the clues from **Story Progress** and **Latest Story Progress** that support their fulfillment.)
Choice: (Act(Character's name, Character's location) / Intervention / {part_end_phrase})
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Intervention**, provide an instruction on what should be introduced. If you chose **Ending**, write "No Instruction." Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
'''.strip()

OUTPUT_FORMAT_DIRECT_TEMPLETE_W_ACT = '''
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice. If you choose **Ending**, list all narrative goals and termination conditions in the **Current Act**, along with the clues from **Story Progress** and **Latest Story Progress** that support their fulfillment.)
Choice: (Act(Character's name, Character's location) / Intervention / {act_end_phrase})
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Intervention**, provide an instruction on what should be introduced. If you chose **Ending**, write "No Instruction." Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
'''.strip()

OUTPUT_FORMAT_INTERVENTION_TEMPLETE = """
Intervention: (Write the content of the intervention as if it were part of a novel. Strictly environmental/situational. Do not include any character actions, reactions, or thoughts. Maximum 50 words. Keep the label exactly as shown, but write the content in Simplified Chinese.)
""".strip()

OUTPUT_FORMAT_DESCRIPTION_TEMPLETE = """
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice.)
Choice: (Describe / Pass)
Description: (If you chose **Describe**, write a short description of the moment without repetition. Do not describe other character's reaction. Maximum 30 words. If you chose **Pass**, write "Pass." Keep the labels and the keyword "Pass" exactly as shown, but write the descriptive content in Simplified Chinese.)
""".strip()

OUTPUT_FORMAT_QUIT_DIRECT_TEMPLETE = """
Reason: (Concisely elaborate on the reason why your choice and instruction can conclude {quit_target}.)
Choice: (Act(Character's name, Character's location) / Intervention)
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Intervention**, provide an instruction on what should be introduced. Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
""".strip()

## Ablation Study (No Intervention)
NO_INTERVENTION_OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING = '''
你只能从以下两种输出中选择 **一种**：

1. **Character Action**
   在以下情况选择：
   - A character (must be listed as type 'character' in the Setup) should take action or react.
   - **Latest Story Progress** includes a context observed by a character.
   Consider this when you choose character:
   - If there is a clear recipient of dialogue or action in **Latest Story Progress**, select the recipient.
   In the output format, use 'Act(Character's name, Character's location)':
   - Use the exact character name as given in the Setup.
   - The location should reflect the character's current position, which may be inferred from the story progress and does not need to appear in the Setup.
'''.strip()

NO_INTERVENTION_OUTPUT_FORMAT_DIRECT_TEMPLETE = '''
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice. If you choose **Ending**, list all narrative goals under utility(narrative) in the **Narrative Goals**, along with the clues from **Story Progress** and **Latest Story Progress** that support their fulfillment.)
Choice: (Act(Character's name, Character's location) / STORY ENDS)
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Ending**, write "No Instruction." Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
'''.strip()

NO_INTERVENTION_OUTPUT_FORMAT_DIRECT_TEMPLETE_W_PLAN = '''
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice. If you choose **Ending**, list all narrative goals under utility(narrative) in the **Narrative Goals**, along with the clues from **Story Progress** and **Latest Story Progress** that support their fulfillment.)
Choice: (Act(Character's name, Character's location) / {part_end_phrase})
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Ending**, write "No Instruction." Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
'''.strip()

NO_INTERVENTION_OUTPUT_FORMAT_DIRECT_TEMPLETE_W_ACT = '''
Reason: (List the conditions, as specified in the State Output Rules, that led to your choice. If you choose **Ending**, list all narrative goals and termination conditions in the **Current Act**, along with the clues from **Story Progress** and **Latest Story Progress** that support their fulfillment.)
Choice: (Act(Character's name, Character's location) / {act_end_phrase})
Instruction: (If you chose **Character Action**, do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. If you chose **Ending**, write "No Instruction." Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
'''.strip()

NO_INTERVENTION_OUTPUT_FORMAT_QUIT_DIRECT_TEMPLETE = """
Reason: (Concisely elaborate on the reason why your choice and instruction can conclude {quit_target}.)
Choice: (Act(Character's name, Character's location))
Instruction: (Do not act on the character's behalf. Instead, provide an instruction as a director without any background exposition. Maximum 50 words. Keep the labels exactly as shown, but write the free-text content in Simplified Chinese.)
""".strip()

###################
####           ####
####  Prompts  ####
####           ####
###################

PART_SUMMARY_PROMPT = '''
故事由 Setup 定义，并按照 Story Progress 所示持续推进。请用不超过 200 词的一段文字，总结 PART {part_n} 的剧情。不要包含其他 PART 的内容。

## Setup
{setup}

## Story Progress
{story_progress}
'''.strip()

def build_beginning_prompt(setup, story_prompt, utility_narrative=None, current_act=None):
   plan_phrase = '**Narrative Goal**'
   if current_act is not None:
      plan_phrase = '**Current Act**'
      
   final_prompt = f"""
这是故事的开头。请写两个段落，形成类似小说开场的起始场景。第一段描述 **Initial State** 中角色所处的状态，不要提及此时还不该登场的角色。第二段为 {plan_phrase} 所描述的情境设置一个最合适的起点。如果 **Story Prompt** 中已经包含明确开场，你的文字应呼应该开场；但即使 **Story Prompt** 里提到了相关事件，也不要提前推进 {plan_phrase} 中的情节。重点是建立背景，尤其是 **Initial State** 定义的环境与角色状态，而不是他们的行动。每段最多 50 词。

## Story Prompt
{story_prompt}
   """.strip()
   
   if current_act is not None:
      final_prompt += f"\n\n## Current Act\n{current_act}"
   elif utility_narrative is not None:
      final_prompt += f"\n\n## Narrative Goals\n{utility_narrative}"
   else:
      raise Exception('Narrative Goal not defined.')
   
   final_prompt += f"\n\n## Setup\n{setup}"
   
   return final_prompt

def build_quit_direct_prompt(setup, story_progress, utility_narrative=None, plan_mode=False, part_n=0, is_last_part=False, act_seq_mode=False, current_act=None, is_last_act=False, no_intervention=False):
   quit_target = "the story"
   context_description = CONTEXT_DESCRIPTION_TEMPLETE
   general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE
   output_rules_without_ending = OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING
   final_prompt = f"Conclude {quit_target} in this turn according to the rules below:"
   if plan_mode or act_seq_mode:
      quit_target = f"PART {part_n}"
      context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN.format(part_n=part_n)
      general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_PLAN.format(part_n=part_n)
      final_prompt = f"Conclude {quit_target} of the story in this turn according to the rules below:"
      if is_last_part:
         quit_target = "the story"
         context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN_LAST_PART.format(part_n=part_n)
         final_prompt = f"Conclude {quit_target} in this turn according to the rules below:"
         
      if act_seq_mode:
         quit_target = "Current Act"
         context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_ACT.format(part_n=part_n)
         general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_ACT
         output_rules_without_ending = OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING_W_ACT
         final_prompt = f"Conclude {quit_target} in this turn according to the rules below:"
         if is_last_act:
            final_prompt = f"Conclude {quit_target}, which is the last act of the story in this turn according to the rules below:"
            
   if no_intervention:
      output_format = NO_INTERVENTION_OUTPUT_FORMAT_QUIT_DIRECT_TEMPLETE.format(quit_target=quit_target)
   else:
      output_format = OUTPUT_FORMAT_QUIT_DIRECT_TEMPLETE.format(quit_target=quit_target)
      
   final_prompt += '\n\n' + f"""
## Context Description
{context_description}
- Determine what to show readers next after the **Latest Story Progress**.

## General Storytelling Rules
{general_storytelling_rules}

## Output Rules
{output_rules_without_ending}

请严格按照下面的 Output Format 回复，不要添加额外解释。输出中必须包含 'Reason'、'Choice'、'Instruction'。
   
## Output Format
{output_format}

## Setup
{setup}
   """.strip()
   
   if act_seq_mode:
      if current_act == None:
         raise Exception('build_direct_prompt: current_act is None.')
      final_prompt += f"\n\n## Current Act\n{current_act}"
   else:
      if utility_narrative == None:
         raise Exception('build_direct_prompt: utility_narrative is None.')
      final_prompt += f"\n\n## Narrative Goals\n{utility_narrative}"
   
   final_prompt += f"\n\n## Story Progress\n{story_progress}"
   
   return final_prompt 
   

def build_direct_prompt(setup, story_progress, utility_narrative=None, plan_mode=False, part_n=0, part_end_phrase="STORY ENDS", is_last_part=False, act_seq_mode=False, current_act=None, act_end_phrase="STORY ENDS", is_last_act=False, no_intervention=False):
   context_description = CONTEXT_DESCRIPTION_TEMPLETE
   general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE
   output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING
   if no_intervention:
      output_rules_without_ending = NO_INTERVENTION_OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING
      output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING.replace('3.', '2.')
      output_format = NO_INTERVENTION_OUTPUT_FORMAT_DIRECT_TEMPLETE
   else:
      output_rules_without_ending = OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING
      output_format = OUTPUT_FORMAT_DIRECT_TEMPLETE
   final_prompt = f"请按照以下规则引导故事走向结局："
   if plan_mode or act_seq_mode:
      context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN.format(part_n=part_n)
      general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_PLAN.format(part_n=part_n)
      output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_PLAN.format(part_n=part_n)
      if no_intervention:
         output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_PLAN.format(part_n=part_n).replace('3.', '2.')
         output_format = NO_INTERVENTION_OUTPUT_FORMAT_DIRECT_TEMPLETE_W_PLAN.format(part_end_phrase=part_end_phrase)
      else:
         output_format = OUTPUT_FORMAT_DIRECT_TEMPLETE_W_PLAN.format(part_end_phrase=part_end_phrase)
      final_prompt = f"Direct PART {part_n} of the story toward its ending according to the rules below:"
      if is_last_part:
         context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN_LAST_PART.format(part_n=part_n)
         output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_PLAN_LAST_PART.format(part_n=part_n)
         final_prompt = f"Direct PART {part_n}, which is the last part of the story toward its ending according to the rules below:"
         
      if act_seq_mode:
         context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_ACT.format(part_n=part_n)
         general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_ACT
         output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_ACT
         if no_intervention:
            output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_ACT.replace('3.', '2.')
            output_format = NO_INTERVENTION_OUTPUT_FORMAT_DIRECT_TEMPLETE_W_ACT.format(act_end_phrase=act_end_phrase)
         else:
            output_rules_without_ending = OUTPUT_RULES_DIRECT_TEMPLETE_WITHOUT_ENDING_W_ACT
            output_format = OUTPUT_FORMAT_DIRECT_TEMPLETE_W_ACT.format(act_end_phrase=act_end_phrase)
         final_prompt = f"Direct the Current Act toward its terminate condition according to the rules below:"
         if is_last_act:
            output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_ACT_LAST
            if no_intervention:
               output_rules_ending = OUTPUT_RULES_DIRECT_TEMPLETE_ENDING_W_ACT_LAST.replace('3.', '2.')
            final_prompt = f"Direct the Current Act, which is the last act of the story toward its terminate condition according to the rules below:"
   
   final_prompt += '\n\n' + f"""
## Context Description
{context_description}
- Determine what to show readers next after the **Latest Story Progress**.

## General Storytelling Rules
{general_storytelling_rules}

## Output Rules
{output_rules_without_ending}

{output_rules_ending}

请严格按照下面的 Output Format 回复，不要添加额外解释。输出中必须包含 'Reason'、'Choice'、'Instruction'。
   
## Output Format
{output_format}

## Setup
{setup}
   """.strip()
   
   if act_seq_mode:
      if current_act == None:
         raise Exception('build_direct_prompt: current_act is None.')
      final_prompt += f"\n\n## Current Act\n{current_act}"
   else:
      if utility_narrative == None:
         raise Exception('build_direct_prompt: utility_narrative is None.')
      final_prompt += f"\n\n## Narrative Goals\n{utility_narrative}"
   
   final_prompt += f"\n\n## Story Progress\n{story_progress}"
   
   return final_prompt

def build_direct_prompt_resolve_wrong_character_choice(setup, story_progress, wrong_direct_response, utility_narrative=None, plan_mode=False, part_n=0, act_seq_mode=False, current_act=None):
   context_description = CONTEXT_DESCRIPTION_TEMPLETE
   general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE
   if plan_mode or act_seq_mode:
      context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN.format(part_n=part_n)
      general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_PLAN.format(part_n=part_n)
      if act_seq_mode:
         general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_ACT.format(part_n=part_n)
   
   final_prompt = "You have chosen a character to act. However, the character does not exist in the list of valid actors. Please resolve this issue according to the rules below:"
   
   final_prompt += '\n\n' + f"""
## Context Description
{context_description}
- Determine what to show readers next after the **Latest Story Progress**.

## General Storytelling Rules
{general_storytelling_rules}

## Output Rules
You should convert your previous direction into the Intervention format. Follow these rules:
{OUTPUT_RULES_INTERVENTION_TEMPLETE}

请严格按照下面的 Output Format 回复，不要添加额外解释。输出中必须包含 'Intervention'。
   
## Output Format
{OUTPUT_FORMAT_INTERVENTION_TEMPLETE}
   
## Setup
{setup}
   """.strip()
   
   if act_seq_mode:
      if current_act == None:
         raise Exception('build_direct_prompt: current_act is None.')
      final_prompt += f"\n\n## Current Act\n{current_act}"
   else:
      if utility_narrative == None:
         raise Exception('build_direct_prompt: utility_narrative is None.')
      final_prompt += f"\n\n## Narrative Goals\n{utility_narrative}"
   
   final_prompt += f"\n\n## Story Progress\n{story_progress}\n\n## Your Previous Direction\n{wrong_direct_response}"
   
   return final_prompt

def build_intervention_prompt(setup, story_progress, instruction, utility_narrative=None, plan_mode=False, part_n=0, is_last_part=False, act_seq_mode=False, current_act=None):
   context_description = CONTEXT_DESCRIPTION_TEMPLETE
   general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE
   final_prompt = f"Directly intervene in the story according to the rules below:"
   if plan_mode or act_seq_mode:
      context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN.format(part_n=part_n)
      general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_PLAN.format(part_n=part_n)
      final_prompt = f"Directly intervene in PART {part_n} of the story according to the rules below:"
      if is_last_part:
         context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN_LAST_PART.format(part_n=part_n)
         final_prompt = f"Directly intervene in PART {part_n}, which is the last part of the story according to the rules below:"
      
      if act_seq_mode:
         general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_ACT.format(part_n=part_n)
   
   final_prompt += '\n\n' + f"""
## Context Description
{context_description}
- Make an intervention based on what to show readers next after the **Latest Story Progress**.
- Refer to the **Reason of Intervention** to guide the nature and direction of your intervention. 

## General Storytelling Rules
{general_storytelling_rules}

## Output Rules
{OUTPUT_RULES_INTERVENTION_TEMPLETE}

请严格按照下面的 Output Format 回复，不要添加额外解释。输出中必须包含 'Intervention'。
   
## Output Format
{OUTPUT_FORMAT_INTERVENTION_TEMPLETE}
   
## Setup
{setup}
   """.strip()
   
   if act_seq_mode:
      if current_act == None:
         raise Exception('build_direct_prompt: current_act is None.')
      final_prompt += f"\n\n## Current Act\n{current_act}"
   else:
      if utility_narrative == None:
         raise Exception('build_direct_prompt: utility_narrative is None.')
      final_prompt += f"\n\n## Narrative Goals\n{utility_narrative}"
   
   final_prompt += f"\n\n## Story Progress\n{story_progress}\n\n## Reason of Intervention\n{instruction}"
   
   return final_prompt

def build_description_prompt(setup, story_progress, utility_narrative=None, plan_mode=False, part_n=0, is_last_part=False, act_seq_mode=False, current_act=None):
   context_description = CONTEXT_DESCRIPTION_TEMPLETE
   general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE
   if plan_mode or act_seq_mode:
      context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN.format(part_n=part_n)
      general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_PLAN.format(part_n=part_n)
      if is_last_part:
         context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_PLAN_LAST_PART.format(part_n=part_n)
         
      if act_seq_mode:
         context_description = CONTEXT_DESCRIPTION_TEMPLETE_W_ACT.format(part_n=part_n)
         general_storytelling_rules = GENERAL_STORYTELLING_RULES_TEMPLETE_W_ACT
   
   final_prompt = f"""
Decide whether to add a concise narrative description according to the rules below:

## Context Description
{context_description}
- Decide whether to a description of the character's reaction in the **Latest Story Progress** to help readers follow the story.

## General Storytelling Rules
{general_storytelling_rules}

## Output Rules
{OUTPUT_RULES_DESCRIPTION_TEMPLETE}

请严格按照下面的 Output Format 回复，不要添加额外解释。输出中必须包含 'Reason'、'Choice'、'Description'。

## Output Format
{OUTPUT_FORMAT_DESCRIPTION_TEMPLETE}

## Setup
{setup}
   """.strip()
   
   if act_seq_mode:
      if current_act == None:
         raise Exception('build_direct_prompt: current_act is None.')
      final_prompt += f"\n\n## Current Act\n{current_act}"
   else:
      if utility_narrative == None:
         raise Exception('build_direct_prompt: utility_narrative is None.')
      final_prompt += f"\n\n## Narrative Goals\n{utility_narrative}"
   
   final_prompt += f"\n\n## Story Progress\n{story_progress}"
   
   return final_prompt
