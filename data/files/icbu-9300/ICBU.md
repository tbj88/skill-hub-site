---
name: ICBU 主管组季度报告生成 
version: 1.6.0
description: 每当用户提到「季度报告」「业务健康度」「主管组复盘」「新签/续签/营收数据」「ICBU业务策略/产品规则」「客户效果/行业流量/」等关键词时，务必优先调用此 Skill。本 Skill 支持四大模块：📊报告生成（21页PPT，包含季度目标进展、业务健康度、预测营收路径与策略建议）、🔍信息查询（直接查询 ICBU 业务策略与产品规则，无需安装 icbuqa skill）、📈数据查询（7类结构化指标，秒级返回）、📋规划复盘（数据+建议组合输出）。即使用户只是问「xx组这个季度怎么样」也应触发此 Skill，而非手写 SQL 或调用其他数据工具。
---

# 主管组季度报告生成 Skill
前置条件
Python 3.12+：必需。macOS 通常预装；Windows 需手动安装（https://www.python.org/downloads/ ，安装时勾选 “Add Python to PATH”）

> ⚠️ **授权引导硬规则（所有模块必须遵守）**
>
> 任何需要用户完成 SSO 的场景，**禁止只说"请执行 xxx initiate"**——必须**同时输出可点击的授权 URL**：
> 1. 优先通过 `python scripts/authorize.py initiate` 输出 JSON 中的 `authorization_url` 字段，**原样展示给用户**并提示"请在浏览器打开此链接完成 SSO"
> 2. 无法执行脚本时（如 icbuqa 单独授权、脚本未安装），按下方"URL 构造公式"直接拼接 URL 展示
> 3. **URL 必须以 markdown 链接形式呈现**，让用户一眼看到、一点即开

## 功能路由

**先判断意图，再选执行路径**：

| 用户意图 | 模块 | 执行方式 |
|---------|------|---------|
| 生成季度PPT报告 | 📊 报告生成 | `generate_report.py` |
| 查询ICBU业务策略/产品规则 | 🔍 信息查询 | `POST /api/v1/icbuqa/query` |
| 查询具体指标数据（营收/续签/新签） | 📈 数据查询 | `query_data.py`（异步任务：提交→轮询→结果） |
| 季度复盘规划、行动计划 | 📋 规划复盘 | 数据查询 + 信息查询组合 |

> ⚡ 用户只问数据或策略时，**禁止生成 PPT**——直接调 API 返回，响应更快，避免浪费用户等待时间（PPT 生成约 5-6 分钟）。

---

## 前置条件

### 服务地址

默认：`https://icbu-manager-report.alibaba.net`（无需配置）

自定义：`export REPORT_API_BASE_URL="http://127.0.0.1:8000"`

### 授权（两套独立 OAuth，不可混用）

| OAuth | 用途 | Token 位置 | 有效期 | 授权命令 | 授权 URL 构造公式 |
|-------|------|-----------|-------|---------|------------------|
| 报告服务（**必装**） | 查 ODPS 数据、生成 PPT、信息查询 | `~/.report-api-server/token.json` | **约 3 天** | `python scripts/authorize.py initiate` | `{BASE_URL}/oauth/authorize?skill_instance_id={iid}` |
| icbuqa（**可选**） | 让 PPT 策略建议更个性化 | `~/.huadong-qa/token.json` | 约 3 天 | `cd ~/.qoder/skills/icbuqa && python scripts/authorize.py initiate` | `https://icbuqa.alibaba.net/oauth/authorize` |

- 两套 OAuth **都没有 refresh_token**，过期后**必须手动**执行 `python scripts/authorize.py initiate` 重新 SSO 授权
- **报告服务 Token 过期**时：数据查询、报告生成、规划复盘都不可用，会直接报 401，**必须立即重新授权**
- **icbuqa Token 过期**时：信息查询仍能通过「全员 token 池」复用团队内其他成员的 token，**不会立刻中断**
- 两套 OAuth 域名不同，**切勿混用 Token**——Token 用错会导致鉴权静默失败
- **信息查询开箱即用**：服务端维护「全员 token 池」，团队内任一成员 3 天内生成过报告，全团队信息查询都能自动复用该 token
- **全团队 3 天无人生成报告时**，信息查询会返回 `token_source: "none"` 和 `reauth_hint` 字段，**必须按下述流程引导用户 SSO**：
  1. 执行 `python scripts/authorize.py initiate`，从输出 JSON 提取 `authorization_url` 展示给用户
  2. 若脚本不可用，直接拼 URL：`{BASE_URL}/oauth/authorize?skill_instance_id={instance_id}`（`instance_id` 取自 `~/.report-api-server/instance_id`）
  3. 以 markdown 链接展示："👉 [点击完成 SSO 授权](URL)"

---

## 报告生成

### 权限自适应

服务端自动识别权限级别，**主管组权限用户无需输入主管组名称**：

```bash
# 主管组权限用户（最常见）- 自动获取主管组
python scripts/generate_report.py FY27Q1

# 大区/区域/全国权限用户 - 必须指定主管组
python scripts/generate_report.py FY27Q1 --group-name "浦东-三组"

# 查询自己的权限级别
python scripts/generate_report.py --check-permission
```

### 主管组名称校验规则

- 接受格式：`浦东-三组`（带中划线）或 `郑州九组`（不带中划线）
- **用户输入格式不规范时（如「北京二组」「北京 二组」「宝安3一组」），先做 ODPS 模糊匹配确认，禁止跳过直接生成**——用错组名会导致报告数据全部出错：
  ```sql
  SELECT partner_comp_name, crnt_org_id
  FROM icbubi.dwm_icbu_yms_local_partner_all_d
  WHERE ds = (SELECT MAX(ds) FROM icbubi.dwm_icbu_yms_local_partner_all_d)
    AND partner_comp_name LIKE '%{地区}%' AND partner_comp_name LIKE '%{组别}组%'
  ```
  将匹配结果展示给用户确认，确认后再发起生成请求。
- **重要**：`partner_comp_name` 比 `org_name` 更可靠（`org_name` 可能不含完整组名如"宝安3一组"）
- 匹配到多个候选时**列出所有让用户选择**，禁止自行猜测；匹配无结果时告知"该主管组不存在"

### 生成流程

```bash
python scripts/generate_report.py FY27Q1 --group-name "浦东-三组"
# → 提交任务，返回 task_id；主管组权限用户省略 --group-name

python scripts/generate_report.py --status <task_id>
# → 轮询进度，约 5-6 分钟完成

python scripts/generate_report.py --download <task_id>
# → 下载到 ~/Desktop/主管组报告_xxx_FY27Q1.pptx
```

> 任务提交后立即告知用户 task_id 和预计时间，**不要让用户干等**——可先用数据查询回答其他问题。

### 策略建议（icbuqa 注入）

PPT 生成前自动并发拉取（约 12 秒），按数据短板融合到各页原有解读/建议中——**确保 icbuqa Token 有效再生成，否则策略内容会降级为通用建议**：
Slide 4（关键行动）、6（产品策略）、8（目标达成路径）、11（团队计划）、13（续签生命周期）、14（大洲流量）、15（行业流量）、16（客户行为）、17（行业效果）、18（拜访量）。

策略内容必须与原有建议融合展示，禁止在PPT里出现「知识库」字样，也不要额外新增突兀的“策略建议”独立板块。覆盖方向包括：新签、续签、金品/客单价、P4P、品广/品牌广告、小满/OKKI、客户效果、国家/行业流量。

---

## 信息查询（直接查 ICBU 业务知识）

用户询问 ICBU 产品规则、策略方法、运营政策时，**优先调用此接口而非搜索网络**——知识库内容为内部最新规则，比公开资料更准确。

> ✨ **无需安装 icbuqa skill**：服务端维护「全员 token 池」自动共享，本 Skill 用户开箱即用。响应中的 `token_source` 字段含义：
> - `"user"`: 用户个人已同步的 token
> - `"pool"`: 复用团队内其他成员最近同步的 token（最常见）
> - `"public"`: 服务端公共 token 兜底
> - `"none"`: 全团队 token 已过期，按 `reauth_hint` 字段执行 OAuth 重新授权即可恢复

```bash
BEARER=$(cat ~/.report-api-server/token.json | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")

curl -s -X POST https://icbu-manager-report.alibaba.net/api/v1/icbuqa/query \
  -H "Authorization: Bearer $BEARER" -H "Content-Type: application/json" \
  -d '{"question": "你的问题"}' > /tmp/qa.json
python3 -c "import json; d=json.load(open('/tmp/qa.json')); print(d.get('answer') or d.get('error'))"
```

适用场景：P4P策略、新签/续签提升方法、星级保效规则、风控政策、运营规则等。

### 信息查询 OAuth 失败处理（`token_source: "none"`）

响应中 `token_source` 字段含义：

| token_source | 含义 | Agent 动作 |
|-------------|------|-----------|
| `"user"` | 用户个人 token | 无需处理 |
| `"pool"` | 全员池复用（最常见） | 无需处理 |
| `"public"` | 服务端公共 token 兜底 | 无需处理 |
| **`"none"`** | **全团队 token 已过期** | **必须按以下流程引导用户 SSO** ⬇️ |

**`none` 场景标准处理流程**（必须完整执行，禁止只告知命令）：

```bash
# 1. 执行 initiate 获取授权 URL
python scripts/authorize.py initiate
# 输出 JSON 中包含 "authorization_url": "https://..."
```

Agent 必须给用户的**标准话术**（照抄即可）：

> ⚠️ 团队内所有人的 icbuqa token 都已过期，需要您完成一次 SSO 授权恢复信息查询。
>
> 👉 **[点击这里完成 SSO 授权](从 initiate 输出提取的 authorization_url)**
>
> 在浏览器完成登录后，脚本会自动轮询并完成授权，之后即可正常查询。
>
> 若链接无法点击，请手动复制：`<authorization_url>`

> ⚡ **不要让用户去"找命令执行"**——直接给链接，体验最佳。

---

## 数据查询（直接获取结构化指标）

用户询问某一具体指标时，**按需传 `metric_types` 缩小范围**——避免拉全量数据导致响应慢、信息过载。

> ⚠️ **v1.6.0 起数据查询为异步任务模式**：`POST /api/v1/data/query` 只创建任务并立即返回 `task_id`，禁止同步等待 ODPS 结果；必须轮询状态，完成后再拉取结果，避免网关 60 秒 504。

**推荐使用脚本（自动提交、轮询、取结果）**：

```bash
# 查询核心健康度并等待结果；主管组权限用户可省略 --group-name
python scripts/query_data.py FY27Q1 --group-name "浦东-三组" --metrics health --wait

# 只提交任务，不等待
python scripts/query_data.py FY27Q1 --group-name "浦东-三组" --metrics health forecast

# 查询进度
python scripts/query_data.py --status <task_id>

# 获取完整 JSON 结果
python scripts/query_data.py --result <task_id>
```

**底层 API 流程**：

```bash
# 1. 提交任务，立即返回 task_id/status_url/result_url
curl -s -X POST https://icbu-manager-report.alibaba.net/api/v1/data/query \
  -H "Authorization: Bearer $BEARER" -H "Content-Type: application/json" \
  -d '{"quarter": "FY27Q1", "group_name": "浦东-三组", "metric_types": ["health"]}'

# 2. 轮询状态
curl -s https://icbu-manager-report.alibaba.net/api/v1/data/<task_id> \
  -H "Authorization: Bearer $BEARER"

# 3. 完成后拉取结果
curl -s https://icbu-manager-report.alibaba.net/api/v1/data/<task_id>/result \
  -H "Authorization: Bearer $BEARER"
```

> `group_name` 仅大区/区域/全国权限用户需要传；主管组权限用户省略（服务端自动注入）。

### 数据查询主管组名称校验（与报告生成同一规则）

> ⚠️ **数据查询同样适用 §报告生成-主管组名称校验规则**——禁止跳过模糊匹配直接调 API。
>
> 用户输入格式不规范（如「北京二组」「北京 二组」「宝安3一组」）时，**必须先做 ODPS 模糊匹配，再调 `/api/v1/data/query`**，否则可能拿到空数据或 504。

**标准处理流程**（4 步）：

**Step 1：判断用户输入是否规范**

| 规范格式 | 不规范格式（需模糊匹配） |
|---------|----------------------|
| `浦东-三组`（地区-数字组，带中划线） | `北京二组`（缺中划线） |
| `郑州九组`（地区+中文数字组，不带中划线） | `北京 二组`（含空格） |
|  | `宝安3一组`（含阿拉伯数字） |

**Step 2：不规范时执行 ODPS 模糊匹配**

> 关键经验：`partner_comp_name` 比 `org_name` 更可靠，优先用 `LIKE` 模糊匹配。

```sql
SELECT partner_comp_name, crnt_org_id
FROM icbubi.dwm_icbu_yms_local_partner_all_d
WHERE ds = (SELECT MAX(ds) FROM icbubi.dwm_icbu_yms_local_partner_all_d)
  AND partner_comp_name LIKE '%{地区}%'
  AND partner_comp_name LIKE '%{组别}组%'
```

**Step 3：匹配结果处理**

| 匹配结果 | Agent 动作 |
|---------|-----------|
| 唯一匹配 | 直接用该标准名称提交 data/query 异步任务 |
| 多个匹配 | 列出所有候选让用户选择，**禁止猜测** |
| 无匹配 | 告知"该主管组不存在，请提供正确名称"，**禁止继续查询** |

**Step 4：复用标准名称提交 data/query 异步任务**

```bash
# 用模糊匹配确认的标准名称（如「北京-一组」而非「北京一组」）
python scripts/query_data.py FY27Q1 --group-name "北京-一组" --metrics health --wait
```

> 🔑 **核心原则**：模糊匹配得到的标准名称必须**严格复用**（包括中划线），禁止自行简化或修改格式（如把 `浦东-三组` 写成 `浦东三组`）。

| metric_type | 包含指标 |
|-------------|---------|
| `health` | 营收/续签率/新签/金品占比（核心健康度） |
| `renewal` | 首年/次年/多年续签率对比 |
| `org_product` | 金品/P4P/品广/OKKI 产品营收明细 |
| `sales_product` | 各销售人员分产品营收排行 |
| `customer` | 星级客户/拜访活跃度 |
| `visit` | 人均拜访客户数全国/大区/主管组对比 |
| `forecast` | 新签+续签+各产品全口径营收预测 |
| `all` | 全部（默认） |

### 数据查询 OAuth 失败处理（HTTP 401）

数据查询接口返回 **HTTP 401** 表示**报告服务 Token 已过期**，**必须立即引导用户完成 SSO**：

**Step 1：执行 initiate 拿授权 URL**

```bash
python scripts/authorize.py initiate
# 输出示例：
# {
#   "success": true,
#   "mode": "auto_poll",
#   "authorization_url": "https://icbu-manager-report.alibaba.net/oauth/authorize?skill_instance_id=xxx",
#   ...
# }
```

**Step 2：以 markdown 链接形式展示 URL 给用户**（标准话术，照抄即可）：

> ⚠️ 报告服务 Token 已过期，数据查询暂不可用。需要您在浏览器完成一次 SSO 授权。
>
> 👉 **[点击这里完成 SSO 授权](从 initiate 输出提取的 authorization_url)**
>
> 在浏览器完成登录后，脚本会自动轮询并完成授权，完成后我会立刻帮您重新查询数据。
>
> 若链接无法点击，请手动复制：`<authorization_url>`

**Step 3：授权完成后自动重试原查询**（不要再让用户发一遍问题）。

> ⚡ **核心原则**：用户问的是数据，授权只是障碍。**给链接 → 等授权 → 自动续查**，不要让用户重复描述需求。

---

## 常见问题速查

| 问题 | 解决方案（**必须输出授权 URL**） |
|------|---------|
| 报告服务 Token 过期（401） | 执行 `python scripts/authorize.py initiate` 并**提取 `authorization_url` 以 markdown 链接展示给用户** |
| icbuqa Token 过期 | 不紧急，可复用全员池；要恢复个性化策略时执行 `python scripts/authorize.py initiate` 并**展示授权 URL** |
| 信息查询返回 `token_source: none` | **必须**按 §信息查询 OAuth 失败处理 章节的标准话术引导，含可点击授权链接 |
| 不知道自己权限级别 | 执行 `python scripts/generate_report.py --check-permission` 查看 `is_group_level` |
| PPT 策略建议为空 | 服务端公共 token 可能过期，联系管理员刷新；或自己安装 icbuqa skill 重新授权并**展示授权 URL** |
| icbuqa 查询返回「token 未同步」 | 服务端公共 token 未配置，联系管理员或安装 icbuqa skill 并完成授权（**展示授权 URL**） |
| 信息查询返回 `token_source: public` | 正常现象，表示使用服务端公共 token 兜底，无需任何操作 |
| 主管组名称不确定 | 跑 ODPS 模糊匹配（`partner_comp_name LIKE '%地区%' AND '%组别%组%'`）确认后再生成/查询，**禁止猜名称** |
| 数据查询返回全 0 / 空数组 | 极可能是组名不规范→先做模糊匹配确认标准名称（含中划线），再提交异步任务 |
| 数据查询任务长时间 running | 正常等待 ODPS 长查询；继续用 `python scripts/query_data.py --status <task_id>` 轮询，完成后 `--result <task_id>` 拉结果 |
| 数据查询不再直接返回 data | v1.6.0 起为异步任务模式：先拿 `task_id`，再轮询状态和结果，禁止按旧同步模式等待 |
| 切换账号 | 删除 `~/.report-api-server/token.json` 后重新授权（**展示授权 URL**） |

> 🔑 **记住**：任何需要用户 SSO 的场景，**链接 > 命令 > 口头描述**。用户一点即开，远比复制命令体验好。
