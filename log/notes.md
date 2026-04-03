# 每次启动codex时，先对它说：
# 先读 log/START_HERE.md，然后继续。后面我说“更新关键记录”时，按项目协议执行。
› 帮我解释这个仓库的结构，并说明如何在 Windows 上运行（especially generate.sh 部分）


• 我先看仓库目录、关键脚本和 README，重点定位 generate.sh 的职责，以及这个项目在 Windows 下的可行运行方式。

• Running Get-ChildItem -Force

• Running rg -n "generate\.sh|Windows|README|install|usage|run|setup" -S .

• Ran Get-ChildItem -Force
  └

    … +25 lines



• Ran rg --files
  └ generation.py
    editor_agent_utils.py
    … +22 lines
    outputs\generation\example\gen_d_gemini-2.0-flash_c_gemini-2.0-flash.json
    outputs\generation\example\example_000_d_gemini-2.0-flash_c_gemini-2.0-flash_screenplay.txt

• Ran rg -n "generate\.sh|Windows|README|install|usage|run|setup" -S .
  └ .\director_agent_utils.py:7:from global_utils import setup_logger
    .\director_agent_utils.py:9:#### setup logger ####
    … +289 lines
    .\prompts\planner_agent_prompt.py:433:{initial_setup}
    .\prompts\planner_agent_prompt.py:473:{initial_setup}

─ Worked for 2m 07s ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• 我已经定位到入口文件和脚本了。下一步我会直接读 README.md、scripts/*.sh 和 generation.py 的参数定义，把仓库结构和 Windows 运行路径对应起来。

• Running Get-Content README.md

• Running Get-Content scripts\generate.sh

• Running Get-Content scripts\env.sh

• Running Get-Content scripts\evaluate.sh

• Running Get-Content scripts\stat.sh

• Ran Get-Content README.md
  └ # CoDi: A Director-Actor Framework for Goal-Driven Interactive Story Generation with LLMs

    … +75 lines
    }
    ```

• Ran Get-Content scripts\generate.sh
  └ #!/bin/bash
    source scripts/env.sh

    python generation.py --data-file $DATA_FILE_PATH --out-dir $GEN_DIR \
        --planner-agent-base-model gpt-4o-2024-11-20 --director-agent-base-model gemini-2.0-flash --character-agent-base-model gemini-2.0-flash --editor-agent-base-model gemini-2.0-flash

• Ran Get-Content scripts\env.sh
  └ ## path to data file
    DATA_FILE_PATH=./data/example.jsonl
    … +11 lines
    export DEEPSEEK_API_KEY='Your API Key'
    export GOOGLE_API_KEY='Your API Key'

• Ran Get-Content scripts\evaluate.sh
  └ #!/bin/bash
    source scripts/env.sh
    … +4 lines
        --data-file ./outputs/generation/gen_d_gemini-2.0-flash_c_gemini-2.0-flash.json \
        --evaluator-agent-base-model gemini-1.5-pro

• Ran Get-Content scripts\stat.sh
  └ #!/bin/bash
    source scripts/env.sh
    … +2 lines
        --gen-data-file ./outputs/generation/gen_d_gemini-2.0-flash_c_gemini-2.0-flash.json \
        --eval-data-file ./outputs/evaluation/eval_d_gemini-2.0-flash_c_gemini-2.0-flash.json \

• Ran Get-Content generation.py
  └ import sys
    sys.path.insert(0, '.')
    … +532 lines
    if __name__ == "__main__":
        main()

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• 结构已经比较清楚了。现在补一层运行依赖和 generate.sh 实际调用链，尤其看它依赖哪些环境变量、输出文件名怎么生成，以及在 PowerShell / Git Bash / WSL 下分别怎么替代。

• Running Get-Content requirements.txt

• Running rg -n "def run_llm|output_story|save_wip_data|LOG_DIR|OPENAI_API_KEY|GOOGLE_API_KEY|DEEPSEEK_API_KEY|read_jsonl|read_json" *.py prompts -S

• Ran Get-Content requirements.txt
  └ annotated-types==0.7.0
    anyio==4.9.0
    … +167 lines
    wrapt==1.16.0
    zipp==3.20.2

• Ran rg -n "def run_llm|output_story|save_wip_data|LOG_DIR|OPENAI_API_KEY|GOOGLE_API_KEY|DEEPSEEK_API_KEY|read_jsonl|read_json" *.py prompts -S
  └ rg: *.py: 文件名、目录名或卷标语法不正确。 (os error 123)

• Ran Get-Content global_utils.py
  └ import logging.handlers
    import sys
    … +209 lines
            logger.error(f"Invalid model card: {model}")
            raise KeyError

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• 我补查一下辅助函数的位置，刚才那个 rg *.py 在 PowerShell 下通配方式不兼容，但这不影响理解；我会直接按目录重新搜。

• Running Get-Content generation_utils.py

• Ran Get-Content generation_utils.py
  └ import copy

    … +391 lines

        return bool(re.match(r"^[^:]+(?: \([^)]+\))?: .+", story_progress_list[-1]))

• Ran rg -n "def output_story|def save_wip_data|LOG_DIR|OPENAI_API_KEY|GOOGLE_API_KEY|DEEPSEEK_API_KEY|def read_jsonl|def read_json|def run_llm" . -S
  └ .\character_agent_utils.py:12:log_file_path = os.path.join(os.environ['LOG_DIR'], 'character_agent_utils.log')
    .\director_agent_utils.py:10:log_file_path = os.path.join(os.environ['LOG_DIR'], 'director_agent_utils.log')
    … +18 lines
    .\scripts\env.sh:14:export DEEPSEEK_API_KEY='Your API Key'
    .\scripts\env.sh:15:export GOOGLE_API_KEY='Your API Key'

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• 我再取一遍关键文件的行号，方便把入口、参数和 Windows 运行方式准确指到具体位置。

• Running Select-String -Path README.md -Pattern "Install Dependencies|Configure API Keys|generate.sh|Arguments|setting-file|load-file"

• Running Select-String -Path scripts\generate.sh -Pattern ".*"

• Running Select-String -Path scripts\env.sh -Pattern ".*"

• Running Select-String -Path generation.py -Pattern "parser.add_argument|def main\(|log_file_path =|generate_narrative\(|edit_simulated_narrative|output_story\("

• Running Select-String -Path global_utils.py -Pattern "def run_gpt|def run_deepseek|def run_gemini|def run_llm|os.environ\['LOG_DIR'\]|OPENAI_API_KEY|GOOGLE_API_KEY|DEEPSEEK_API_KEY"

• Ran Select-String -Path README.md -Pattern "Install Dependencies|Configure API Keys|generate.sh|Arguments|setting-file|load-file"
  └
    README.md:11:### Install Dependencies
    … +6 lines



• Ran Select-String -Path scripts\generate.sh -Pattern ".*"
  └
    scripts\generate.sh:1:#!/bin/bash
    … +4 lines



• Ran Select-String -Path scripts\env.sh -Pattern ".*"
  └
    scripts\env.sh:1:## path to data file
    … +14 lines



• Ran Select-String -Path generation.py -Pattern "parser.add_argument|def main\(|log_file_path =|generate_narrative\(|edit_simulated_narrative|output_story\("
  └
    generation.py:22:    parser.add_argument('--data-file', type=str, required=True)
    … +22 lines



• Ran Select-String -Path generation_utils.py -Pattern "def out_file_name|def save_wip_data|def output_story|def init_narrative_generation|def build_context_start_of_new_part"
  └
    generation_utils.py:15:def out_file_name(args):
    … +5 lines



• Ran Select-String -Path global_utils.py -Pattern "def run_gpt|def run_deepseek|def run_gemini|def run_llm|os.environ\['LOG_DIR'\]|OPENAI_API_KEY|GOOGLE_API_KEY|DEEPSEEK_API_KEY"
  └
    global_utils.py:46:log_file_path = os.path.join(os.environ['LOG_DIR'], 'global_utils.log')
    … +7 lines



────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• 还有一个实际问题要确认：requirements.txt 看起来混了不少 Linux/Conda 固定包，Windows 上直接 pip install -r requirements.txt 很可能会失败。我补查项目真实 import，给你一个更稳的 Windows 安装方案。

• Running Select-String -Path requirements.txt -Pattern "file:///|linux|croot|opt/conda"

• Ran rg -n "^(import |from )" *.py prompts\*.py scripts -g "*.py"
  └ rg: *.py: 文件名、目录名或卷标语法不正确。 (os error 123)
    rg: prompts\*.py: 文件名、目录名或卷标语法不正确。 (os error 123)

• Ran Select-String -Path requirements.txt -Pattern "file:///|linux|croot|opt/conda"
  └
    requirements.txt:12:Bottleneck @ file:///croot/bottleneck_1731058641041/work
    … +25 lines



• Ran rg -n "^(import |from )" -g "*.py" .
  └ .\character_agent_utils.py:1:import sys
    .\character_agent_utils.py:3:import re
    … +76 lines
    .\score_stat.py:13:from global_utils import *
    .\score_stat.py:14:from generation_utils import is_character_reaction

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• 仓库结构

  这个仓库的主入口是 /E:/Projects/CoDi/generation.py:443。整体可以按 4 层理解：

  - scripts/
      - /E:/Projects/CoDi/scripts/generate.sh:1 是“生成故事”的壳脚本。
      - /E:/Projects/CoDi/scripts/env.sh:1 放数据路径、输出目录、日志目录、API Key。
      - evaluate.sh / stat.sh 是后处理，不是主运行入口。
  - 根目录核心 Python
      - /E:/Projects/CoDi/generation.py:22 解析参数并串起完整流程。
      - /E:/Projects/CoDi/planner_agent_utils.py、/E:/Projects/CoDi/director_agent_utils.py、/E:/Projects/CoDi/character_agent_utils.py、/E:/Projects/CoDi/editor_agent_utils.py 分别对应 planner / director / character / editor 四
        类 agent。
      - /E:/Projects/CoDi/global_utils.py:110 负责 OpenAI / DeepSeek / Gemini 调用和 JSON/日志等通用能力。
      - /E:/Projects/CoDi/generation_utils.py:15 负责输出命名、保存中间结果、导出最终文本等。
  - prompts/
      - prompt 模板都在这里，按 agent 分文件。
  - 数据和输出
      - data/ 输入 prompt，默认示例是 /E:/Projects/CoDi/data/example.jsonl
      - outputs/ 生成结果
      - log/ 运行日志
      - images/ 论文图
      - README.md 是简要使用说明，见 /E:/Projects/CoDi/README.md:11

  运行流程

  generate.sh 本质上只做两件事：

  1. source scripts/env.sh，把路径和 API key 注入当前 shell
  2. 调用 python generation.py ...，并传入默认模型组合，见 /E:/Projects/CoDi/scripts/generate.sh:1

  generation.py 的实际流程是：

  1. 读 --data-file 和 --out-dir 等参数，/E:/Projects/CoDi/generation.py:22
  2. 生成 initial setup
  3. 生成 character agents
  4. 如果开了 --plan-mode，再生成 plan
  5. 逐 turn 生成 narrative，/E:/Projects/CoDi/generation.py:87
  6. 做 edit phase
  7. 输出最终 screenplay / novel 文本，/E:/Projects/CoDi/generation.py:528

  输出文件名规则在 /E:/Projects/CoDi/generation_utils.py:15 和 /E:/Projects/CoDi/generation_utils.py:68。

  Windows 上怎么跑，尤其是 generate.sh

  关键点：generate.sh 是 Bash 脚本，不是 PowerShell 脚本。
  它里面用了这些 Bash 语法：

  - #!/bin/bash
  - source scripts/env.sh
  - $DATA_FILE_PATH
  - 反斜杠续行 \

  所以它不能直接在 PowerShell 里运行。

  最稳的 Windows 方案有两种。

  1. 用 Git Bash 或 WSL 跑原始脚本

  先改 /E:/Projects/CoDi/scripts/env.sh:12 里的 key，然后在 Git Bash / WSL 里执行：

  cd /e/Projects/CoDi
  bash scripts/generate.sh

  这是最接近作者原始用法的方式。

  2. 在 PowerShell 里手动等价执行

  先说一个很重要的细节：
  /E:/Projects/CoDi/global_utils.py:46 在 import 时就直接读取 os.environ['LOG_DIR']。所以 LOG_DIR 必须在运行 python generation.py 之前就设好，否则程序会在启动早期直接报错。

  PowerShell 里可这样跑：

  cd E:\Projects\CoDi

  $env:LOG_DIR = ".\log"
  $env:OPENAI_API_KEY = "你的 OpenAI Key"
  $env:DEEPSEEK_API_KEY = "你的 DeepSeek Key"
  $env:GOOGLE_API_KEY = "你的 Google Key"

  python .\generation.py `
    --data-file .\data\example.jsonl `
    --out-dir .\outputs\generation `
    --planner-agent-base-model gpt-4o-2024-11-20 `
    --director-agent-base-model gemini-2.0-flash `
    --character-agent-base-model gemini-2.0-flash `
    --editor-agent-base-model gemini-2.0-flash

  这就是 /E:/Projects/CoDi/scripts/generate.sh:4 的 PowerShell 等价版本。

  如果你想开 plan-mode：

  python .\generation.py `
    --data-file .\data\example.jsonl `
    --out-dir .\outputs\generation `
    --plan-mode `
    --planner-agent-base-model gpt-4o-2024-11-20 `
    --director-agent-base-model gemini-2.0-flash `
    --character-agent-base-model gemini-2.0-flash `
    --editor-agent-base-model gemini-2.0-flash

  Windows 安装依赖的注意点

  README 里写的是 pip install -r requirements.txt，见 /E:/Projects/CoDi/README.md:11。
  但这个仓库的 /E:/Projects/CoDi/requirements.txt 明显是从 Linux/Conda 环境直接导出的，里面有很多 file:///croot/...、linux_x86_64.whl 之类的条目，在 Windows 上大概率装不起来。

  所以在 Windows 上更建议：

  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  pip install openai==1.64.0 google-genai==1.15.0 google-generativeai==0.8.5 tiktoken==0.8.0 numpy==1.26.4 tqdm==4.66.5

  如果你后面还要跑评测脚本，再按报错补包会更实际；直接照 requirements.txt 在 Windows 装，风险很高。

  一句话总结 generate.sh

  generate.sh 只是一个很薄的 Bash 包装层：先加载 env.sh，再调用 generation.py。
  在 Windows 上，推荐要么用 Git Bash/WSL 直接跑它，要么在 PowerShell 里手动设置环境变量后执行等价的 python generation.py ... 命令。

  如果你要，我可以下一步直接给你一份 generate.ps1，把这个仓库改成 Windows 一键运行。