---
name: 国际站智能发品
version: 3.4.0
description: |
  支持 URL 发品、素材包发品和草稿发品三种模式，将商品发布到 Alibaba.com 国际站。
  覆盖素材解析、发布前预检、批量发布和基于轮询机制的异步任务状态追踪；不处理商品字段编辑、卖点优化或市场分析。
enabled: true

triggers:
  - URL 发品
  - 链接发品
  - 素材包发品
  - 国际站发布商品
  - 批量发品
  - 草稿发布
  - 草稿商品上线
  - 发品进度查询

examples:
  - 基于这个 1688 链接帮我发布到国际站
  - 用附件里的图片和 Excel 帮我发品
  - 把这个草稿商品上线
  - 查询一下刚才发品任务的结果

excludes:
  - skill: alibaba-product-information-optimization
    when: 用户要修改、编辑或优化已存在商品/草稿商品的标题、价格、卖点、图片、属性等字段
  - skill: alibaba-hot-product-insight
    when: 用户要分析热销原因、爆品趋势、热卖特征或市场榜单
  - skill: alibaba-blue-ocean-finder
    when: 用户要基于供需错配、低竞争或差异化机会决定发布什么商品

workflow: |
  1. 识别入参类型（URL、素材文件或草稿商品）
  2. 根据入参类型，一次性创建完整 DAG（task_create 全部 → task_update addBlockedBy 串依赖）
  3. 按 DAG 顺序推进：task_update(in_progress) → 执行 → task_update(completed) → 下一个
  4. URL 发品 DAG：url_validate → precheck → start → poll → present
  5. 素材包发品 DAG：plan_select → [url_fetch?] → [image_edit?] → parse_collect → parse_analyze → [auto_merge?] → confirm → [merge?] → publish → poll → present
  6. 草稿发品 DAG：draft_input → publish_draft → present

renderers:
  icbu-publish-preview-render:
    description: icbu-publish-preview 富文本渲染页面
    url: https://air.alibaba.com/app/bc/aw-product-publish-preview/index.html

tool_triggers:
  - tool: bash
    args:
      command: '/workctl\s+icbu\s+product\s+(?:material-extract|material-analysis|list-material-analysis-result|material-collect|publish|precheck-url-product-generate|start-url-product-generate|list-task-list|publish-draft)\b/i'
---

# ICBU 国际站智能发品

> **⚠️ 最高优先级指令（必须无条件遵守）：**
> 本 skill 每次被唤醒/触发时，无论通过何种路径唤醒（包括 tool_triggers 拦截），**第一个动作必须是执行下方「判断规则」**，根据用户输入内容判断发品模式。
> - 能判断 → 直接进入对应链路的第一步
> - 不能判断 → 输出固定引导文案，等待用户选择
>
> **禁止跳过判断规则直接调用任何 workctl 工具。禁止从链路中间步骤开始执行。**
>
> **内置渲染协议执行规则：**
> 素材包发品链路需要商品预览时，必须读取并遵循当前 skill 内置的 `reference/icbu-publish-preview/protocol.md`，按其协议构造 `SkillPayload`，并运行 `reference/icbu-publish-preview/scripts/render.ts` 生成 slot。该预览能力已作为当前 skill 的 renderer 暴露，最终必须返回 `slot.skillId = "国际站智能发品"`、`slot.renderer = "icbu-publish-preview-render"`。宿主通过拦截 `bun run render.ts` 的 stdout 输出获取 slot 元数据，并在工具结果末尾追加渲染指令（含 `:::slot[<id>]` 标记）。脚本成功执行后（退出码 0），本轮 assistant 回复**必须**先按工具结果中宿主追加的指令逐字输出 `:::slot[<id>]` 标记（独占一行，id 从指令中原样复制），再紧跟输出「渲染后引导话术」（发品总结 1-2 句 + 固定操作引导模板，详见 protocol.md），输出后立即结束本轮。禁止在 Bash 命令中追加 `>/dev/null`、`2>&1`、`> file`、`| cat`、`| tee` 或任何 stdout 重定向/管道；禁止追加 `--output-file` 参数。禁止引用或转述 stdout 原始 JSON 内容；禁止手动构造 slot JSON、slot 摘要或自拟 id 的占位串（id 只能从宿主指令中复制）；禁止再输出引导话术之外的自然语言、成功说明、解析摘要或确认提示。禁止把 `success`、`data`、错误格式的 slot 占位串、代码块、Markdown 表格、HTML/网页截图式预览、文本说明、链接、图片、Markdown 图片或 `#image:` 作为普通文本展示给用户。如果脚本执行失败（非零退出码），应说明失败原因，禁止降级输出 slot 文本或图文说明。禁止依赖同级目录中已安装的外部 skill。脚本成功执行后必须等待用户在下一轮明确确认，禁止在同一轮或未确认状态下进入 `publish` / `poll` / `present`。
>
> **tool_triggers 激活场景的特殊指令：**
> 当本 skill 通过 `tool_triggers`（即拦截 workctl 工具调用）被激活时：
> 1. **立即丢弃**被拦截的那次工具调用，不得继续执行它
> 2. **忽略**所有从 memory 文件、缓存文件、历史会话中读取的上下文数据（包括但不限于 `memory/queries.json`、`TASK_HISTORY.json` 中与发品相关的历史记录）
> 3. **仅以用户当前消息内容**作为输入，从「判断规则」开始执行
> 4. 如果用户当前消息中无法判断发品模式，输出引导文案等待用户选择

在 Alibaba.com 国际站（ICBU）发布商品，支持 **URL 发品**、**素材包发品** 和 **草稿发品** 三种模式。

## 入参识别与链路路由

根据用户输入内容识别发品模式，路由到对应的子技能，与唤醒路径无关：

### 判断规则

1. **URL 发品** — 满足以下任一条件：
   - 用户输入中包含 `1688.com`、`taobao.com`、`tmall.com`、`aliexpress.com`、`amazon.com` 域名的链接
   - 用户明确表示使用 URL/链接发品（如"用链接发品"、"URL 发品"）
   - → 读取 [reference/url-publish.md](reference/url-publish.md)，按 DAG 结构创建任务并执行

2. **素材包发品** — 满足以下任一条件：
   - 用户上传了素材文件（图片、ZIP 包、Excel、Word、PowerPoint、Markdown、PDF 等）
   - 用户明确表示使用素材包发品（如"素材包发品"、"上传文件发品"、"解析素材"）
   - → 读取 [reference/material-publish.md](reference/material-publish.md)，按 DAG 结构创建任务并执行

3. **草稿发品** — 满足以下任一条件：
   - 用户明确提及"发布草稿"、"草稿发布"、"将草稿商品上线"、"草稿态商品发布"、"草稿上线"
   - 用户表示商品已在草稿箱中，需要发布到线上
   - → 读取 [reference/draft-publish.md](reference/draft-publish.md)，按 DAG 结构创建任务并执行

4. **无法判断** — 若无法通过用户输入判断发品方式（既不包含 URL、也未上传文件、也未明确表达发品模式），**必须**输出以下固定引导文案，等待用户明确选择后再进入对应链路。**禁止自行推断、禁止跳过引导直接执行。**

   > 我是 ICBU 国际站智能发品助手，可以帮您将商品发布到 Alibaba.com 国际站。请选择您的发品方式：
   > 1. **URL 发品** — 提供商品链接（支持 1688、淘宝、天猫、AliExpress、Amazon），我将自动抓取商品信息并发布
   > 2. **素材包发品** — 上传素材文件（图片、ZIP、Excel、Word 等），我将解析素材内容并发布
   > 3. **草稿发品** — 将已保存的草稿态商品发布到线上

## Task-Based Execution Protocol（任务执行协议）

路由判断完成后，按以下协议执行发品流程。本 skill 的所有工作流均通过 **DAG（有向无环图）任务系统**驱动；plan 仍以 session 内存对象为权威（用于 `mode` / `category_key` / `delegate` / `subtasks` 等任务系统不承载的字段），task 系统承载所有 step 的持久化状态、依赖关系与用户可见的任务面板渲染。**禁止跳过本协议直接调用 workctl 工具。**

### Step 1: Plan — 一次性创建完整 DAG（2-pass init）

根据判断规则确定的发品模式，读取对应的 reference 文档，找到 DAG 结构定义；条件性 step（预处理 / `auto_merge`）按 reference 文档「DAG 规划判定」章节的判定规则决定是否纳入。本平台 task API（旧版本）**不支持在 `task_create` 时内联声明 `blockedBy`**，因此 plan 必须用 **2-pass** 模式初始化：

1. **Pass 1（并行 task_create）**：在一个 response 中并行调用所有 `task_create`，按 plan.steps 顺序逐个创建；不传依赖字段。记录每次返回的 `task.id`（即 task 系统的字符串数字 id）回写到 `plan.steps[i].taskId`。
2. **Pass 2（并行 task_update 串依赖）**：在下一个 response 中并行调用 `task_update`，对每个 step 用 `addBlockedBy: [<上一个 step.taskId>]` 串起线性依赖；分支或条件 step 的依赖另行处理（详见 reference 文档）。
3. **Pass 3（task_list 验证）**：调用一次 `task_list` 核对所有 task 已创建、依赖关系符合 DAG 结构。

```
// Pass 1
task_create({ subject: "...", description: "..." })   ← 不传 blockedBy
task_create({ subject: "...", description: "..." })
...

// Pass 2
task_update({ taskId: "2", addBlockedBy: ["1"] })
task_update({ taskId: "3", addBlockedBy: ["2"] })
...

// Pass 3
task_list({})
```

**禁止分批创建（小步发多轮 task_create）、禁止用模型记忆替代 task_list 验证。** 条件性任务（如素材包模式的 `merge`、`auto_merge`、`url_fetch` / `image_edit` 预处理 step）按 reference 文档的 DAG 规划判定规则**在 Pass 1 一次性纳入或排除**；其中 `merge` 是占位任务，必须在 Pass 1 创建，用户确认无修改时只允许标记为 `[SKIPPED]` archived，禁止 confirm 后再补建。唯一例外是 `image_edit` 的 B 类兜底：需要先抓图、再询问是否修改时，允许运行时 `task_create` + `task_update(addBlocks)` 动态加入。

### Step 2: Execute — 按 plan.steps 顺序推进

进入主循环，按 plan.steps **数组顺序**推进（DAG 几乎是线性的，分支只有素材包模式的 confirm 后是否走 merge 这一处）：

1. 从 plan.steps 中取下一个 status 为 `pending` 的 step（`plan.steps[i]`）
2. `task_update({ taskId: plan.steps[i].taskId, status: "in_progress" })`
3. 读取该 step 对应 reference 文档章节（按 step.id 锚点定位），按文档要求执行（调用 workctl、轮询、ask_user 等）
4. 执行成功：`task_update({ taskId, status: "completed" })`；将关键产出写入 `plan.steps[i].output`
5. 执行失败：**老 API 没有 `failed` / `skipped` 状态**——统一用 `task_update({ taskId, status: "archived", description: "[FAILED] <原 description> — 错误: <摘要+traceId>" })` 标识废止，错误原因放在 description 前缀里；plan.steps[i].status 在内存中仍可标 `failed` / `skipped` 用于紧凑视图与控制流，但落到 task 系统统一是 `archived`
6. `i++`，回到步骤 1

**条件分支处理（素材包 confirm 后是否 merge）：** 用户在 confirm 节点选择"无修改"时，直接把预先创建的 `merge` task 标 `archived`（description 前缀加 `[SKIPPED]`），i 推进到 `publish`；用户选择"修改"时，正常推进 `merge`。**禁止在 confirm 之后才补建 `merge` task**——Pass 1 已创建。

**用户交互：** 需要用户输入的 step 默认通过 `ask_user` 获取输入，task status 仍按上述节奏推进。但素材包发品的 `confirm` 预览是例外：首次进入 `confirm` 时只能生成并交付 `icbu-publish-preview-render` slot，然后立即停止本轮回复，保持 `confirm` task 为 `in_progress`，等待用户下一轮明确回复。只有收到「确认发布」或等价自然语言确认后，才能将 `confirm` task 标为 `completed` 并推进 `publish`；未收到确认前禁止执行 `publish` / `poll` / `present`。

### Step 3: Verify — 验证所有任务完成

整个 plan 跑完后（i 越界），调用 `task_list` 检查：
- 所有 task 都是 `completed` 或 `archived`（没有遗留 `pending` / `in_progress`）
- 依赖关系按 plan 预期被遵守

若发现遗留 `pending` / `in_progress`，按下文『取消分支兜底』统一处理。

### 取消分支兜底

用户在任意 step 主动取消（点击「取消」按钮、自然语言取消如"取消 / 不发了 / 放弃"），或检测到上游不可恢复错误时：

1. 当前 step 的 task → `task_update({ taskId, status: "archived", description: "[CANCELLED] <原 description> — 原因: <用户取消 / 错误摘要>" })`
2. 所有下游尚未完成的 task（`pending` / `in_progress`）→ 并行 `task_update({ taskId, status: "archived", description: "[CANCELLED] <原 description> — 原因: 上游 <stepId> 取消" })`
3. 内存 plan：标当前 step.status = `cancelled`，下游 step.status 全部置 `cancelled`
4. 若已创建工作目录（`analysis_<YYYYMMDD_HHMMSS>/`），删除该目录
5. 向用户输出一行确认文案：`✅ 已取消本次发品流程。` 不再发起任何 ask_user

### ask_user 渲染规范

SKILL.md 及 reference 文档中所有"向用户展示 / 等待用户确认 / 提示用户 / 输出引导文案"等节点，默认必须通过 `ask_user` 工具实现而非纯文本输出。

> **例外：`icbu-publish-preview-render` 预览 slot 是强交互边界，不适用本节 ask_user 渲染规范。** 素材包发品第 2 步与修改合并后的预览确认步骤，必须提交 `icbu-publish-preview-render` slot 给宿主渲染，紧跟输出 `protocol.md` 定义的「渲染后引导话术」，然后立即结束本轮回复；禁止再调用 `ask_user`，禁止追加按钮、Markdown 表格、超时兜底说明或"当前状态"文本。确认必须来自用户下一轮回复；禁止同一轮自动确认或继续发布。

其他需要 `ask_user` 的节点遵循以下要点：

- **`message` 字段支持完整 Markdown 与自定义组件**（如 `<product-preview>{"id": "..."}</product-preview>`），格式必须与对话直接输出一致；reference 文档要求出现该组件的位置**必须原样包含**，禁止简化为纯文本或普通链接
- **快速操作按钮**（reference 文档以表格形式列出 label / description 的小节，如 [material-publish.md](reference/material-publish.md) 第 2 步 3 按钮规范）：必须翻译为 `ask_user` 调用的 `options` 数组，每个按钮一项，`label` 与 `description` **逐字**取自表格，不得改名、改顺序或省略
- **未传 `options` 的违规风险**：若某次 `ask_user` 未传 `options`，前端会渲染默认的"跳过 / 取消 / 确认"兜底按钮，覆盖文档规定的语义——这是违规实现
- **自由输入并存**：按钮存在的同时**仍允许用户直接打字输入**（不要在 question 文案里写"必须点按钮"之类限制）

### Task 系统与 reference 文档的边界

**Task 系统是编排层，不是业务层。**

- ✅ Task 系统决定：任务创建、依赖管理、状态推进、用户可见的任务面板渲染
- ❌ Task 系统不决定：每步调什么 workctl、入参怎么构造、轮询多少秒、状态字段怎么判断、最终展示怎么排版 —— 这些一律按 SKILL.md / reference 执行
- ❌ Task 系统**不能**用来绕过 reference 文档里的禁令（如 `material-publish.md §6` 禁止展示商品标题与类目、`material-publish.md` 第 4 步「前置禁止动作」清单、SKILL.md §会话隔离 禁止读 memory、`material-edit-merge.md` 3.4.2 禁止 while 循环包装等）

## workctl 工具速查表

所有业务工具均通过 `workctl ... --format json` 调用。

### 素材包发品专用

| workctl 命令 | 用途 | 入参 |
|----------|------|------|
| `workctl icbu product material-extract` | 从素材文件中提取图片和文本（支持 xlsx/docx/pptx/xls/ppt/txt/md/pdf），输出 `result/` 目录含 `image_list.json`、`extracted_texts.json`；如有 PDF 则额外输出 `result/pdf_pages/` 子目录 + `pdf_pages_local.json`（PDF 按页 200 DPI rasterize 为 JPEG，独立于 image_list）。自动解压 ZIP、处理中文文件名。**只扫描 `--work_dir` 根下的文件，不递归子目录**——所有原始素材必须直接平铺到工作目录根，禁止额外创建 `input/` 等子目录。**若返回 `unknown_command`（exit 32）则回退到 `python reference/scripts/extractor.py`** | `--work_dir <工作目录> --format json` |
| `workctl icbu product material-collect` | **一次性完成素材打包+上传 OSS**（内部串：zip → MCP 上传 → 返回 `data.ossUrl`）。两种模式：**analysis**（默认）打包 `<work_dir>/result/` 下的 JSON 用于初次解析；**patch** 打包 `<work_dir>/merge_patch.json` 用于用户修改合并。**若返回 `unknown_command`（exit 32）则回退到 `pack_and_upload.py`** | `--work_dir <工作目录> [--mode analysis\|patch] --format json` |
| `workctl icbu product material-analysis` | 提交云端 AI 素材分析/合并任务（初次解析与用户修改合并均为异步，提交后返回 `unique_key`，需配合 `list-material-analysis-result` 轮询） | `--material <OSS URL> --uniqueRequestId null --format json` |
| `workctl icbu product list-material-analysis-result` | 轮询云端分析任务结果 | `--uniqueRequestId <unique_key> --format json` |
| `workctl icbu product publish` | 属性映射+预检+启动发品 | `--material <category_key> --publishType <draft/product> --extInfo '{}' --yes --format json` |

### 旧版本回退工具（仅当新命令返回 `unknown_command` 时使用）

| 工具 | 用途 | 调用方式 |
|------|------|----------|
| `python reference/scripts/extractor.py` | 旧版素材提取脚本（支持 xlsx/xls/docx/txt/zip/pdf，PDF 需 pypdfium2+Pillow） | `python reference/scripts/extractor.py <工作目录>` |
| `python3 reference/scripts/pack_and_upload.py` | 旧版打包+上传 OSS 脚本 | `python3 reference/scripts/pack_and_upload.py --work-dir <工作目录> --mode analysis\|patch` |

### URL 发品专用

| workctl 命令 | 用途 | 入参 |
|----------|------|------|
| `workctl icbu product precheck-url-product-generate` | URL 发品预检 | `--totalCount <N> --format json` |
| `workctl icbu product start-url-product-generate` | 启动 URL 发品 | `--urlList <逗号分隔URL> --publishType <draft/product> --format json` |

### 草稿发品专用

| workctl 命令 | 用途 | 入参 |
|----------|------|------|
| `workctl icbu product publish-draft` | 将草稿态商品发布到线上 | `--productId <草稿商品ID> --yes --format json` |

### 两种模式共用

| workctl 命令 | 用途 | 入参 |
|----------|------|------|
| `workctl icbu product list-task-list` | 发品结果轮询 | `--taskId <taskId> --format json` |

# 会话隔离

每次执行本 skill 都是独立任务，必须遵守以下隔离规则：

1. **必须从判断规则开始执行**（详见文档顶部最高优先级指令）：每次本 skill 被唤醒/触发时，第一个动作必须是执行「判断规则」。禁止跳过判断规则直接调用 workctl 工具，禁止从链路中间步骤开始，禁止跳过任何步骤，禁止假设之前的步骤已完成。即使用户声称"之前已经解析过了"或"直接帮我发品就行"，也必须从判断规则开始重新执行，不得跳步。
2. **taskId 仅来自当前会话**：轮询所用的 taskId 只能从当前会话中上游步骤的返回值获取，禁止从 memory 或其他来源读取。
3. **不复用历史结果**：即使用户发布的商品与之前会话相似，也必须重新执行完整流程，不得跳步或复用之前的解析/预测结果。
4. **禁止读取记忆/缓存文件**：本 skill 被激活时，禁止读取 `memory/queries.json`、`TASK_HISTORY.json`、`MERCHANT_PROFILE.json` 等文件中与发品任务相关的历史数据作为执行依据。本 skill 的所有输入只能来自用户当前消息和当前会话中上游步骤的返回值。
5. **每次从零开始执行完整流程**：本 skill 不依赖历史追问记录，每次被激活时都从零开始执行。

## 错误处理

- **网络/workctl 调用错误:** 调用处如无规定，则默认自动重试一次。若仍失败，向用户报告错误并终止流程。
- **轮询超时:** 明确告知用户超时情况，并提供手动跟进指引（如提供 taskId）。
- **预检不通过:** 以结构化列表展示所有不通过原因，方便用户逐项处理。（`publish` 内部执行预检，不通过时从返回结果中获取错误信息）

## 轮询实现规范

所有轮询步骤均遵循以下模式：

0. 确认 taskId 来源：taskId **只能**从当前会话中上游启动步骤（`start-url-product-generate` 或 `publish`）的返回值中提取。禁止使用 memory、历史会话、用户口述或任何其他来源的 taskId。
1. 初始化计数器为 0。
2. 调用对应的轮询 workctl 命令。
3. 若返回结果表示已完成（成功或失败），返回结果。
4. 若仍在处理中，等待 **20 秒**（默认间隔；用户修改合并轮询例外，间隔 **10 秒**，详见 material-publish.md 3.4.2），计数器加 1，回到步骤 2。
5. 若计数器超过最大次数，返回超时结果。
