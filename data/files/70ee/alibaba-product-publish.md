---
name: alibaba-smart-publish
description: 阿里巴巴国际站智能发品端口 —— 解决 AI 发品时属性乱写、价格乱定的两大痛点。通过「属性锚定三源交叉」和「价格三角定位」两大机制，产出可直接复制到 ICBU 后台的字段清单（属性表 + 阶梯价 + 6 版标题 + 关键词矩阵 + 5 张主图脚本 + 8 模块详情页文案）。触发词：发品、智能发品、上架、发新品、发这个产品、把这个发到国际站、alibaba publish、ICBU listing。适用场景：主公给一个 1688 URL / 竞品 URL / 产品名 + 目标市场，要求生成一套可直接上架的国际站发品方案。
---

# 阿里巴巴国际站智能发品端口 (alibaba-smart-publish)

> 版本 v1.0 · 服务对象：爱以思等 ICBU 卖家
> 定位：**替代 AI 拍脑袋发品**，用数据锚定属性与价格

---

## 🎯 核心痛点 & 解决路径

| 痛点 | 传统 AI 做法 | 本 Skill 做法 |
|---|---|---|
| 属性乱写 | AI 自由发挥编字段 | **三源交叉锚定**：1688 抓取 + 竞品 Top10 分布 + ICBU 类目字典 |
| 价格乱定 | AI 编个整数 | **三角定位**：成本锚 + 市场锚 + 关税物流 → 数学计算 |
| 缺数据仍硬答 | AI 编造置信度 | 缺失字段一律标 `[需人工确认]`，禁止编造 |

---

## 🚦 三种触发方式

主公在对话框说 **"发品：..."** 即触发，按输入类型自动路由：

### 触发 A：URL 全自动模式
```
发品：https://detail.1688.com/offer/xxx.html
发品：https://www.alibaba.com/product-detail/xxx.html
```
→ 自动抓真实数据 → 属性锚定 → 定价 → 全套输出

### 触发 B：产品名 + 市场模式
```
发品：Outdoor Patio Umbrella + 欧洲中东
发品：户外庭院伞 目标市场：欧洲
```
→ 走市场调研路径（product_supplier_search 拉竞品）→ 定价 → 全套输出

### 触发 C：手动填表模式
```
发品：
产品：户外庭院伞
类目：Outdoor Umbrella
材质：3m 铝杆 UV
MOQ：100
交期：25-35 天
认证：CE, UV test
```
→ 只做价格 + 文案增强，不重新抓属性

---

## 📋 完整工作流（5 阶段）

### 阶段 1：输入解析与源数据抓取（30-90 秒）

**执行动作：**
1. 判断输入类型（URL / 产品名 / 表单），选择对应触发路径
2. **触发 A**：`web_fetch` 抓 1688 或竞品详情页
   - 提取字段：产品名、类目、材质、规格（尺寸/重量）、工艺、包装、认证、MOQ、交期、原价、图片URL
   - 抓取失败 → 降级到触发 B
3. **触发 B**：调 `product_supplier_search`
   - `intent_type="product"`, `query="<产品名>"`, `query_language="en"`
   - 拉 Top 10-20 条同类目商品，抽取属性分布 + FOB 价格带
4. **触发 C**：直接进阶段 2

**输出：** 一份"源数据摘要"，标注每个字段的来源和置信度（HIGH/MID/LOW）

---

### 阶段 2：属性锚定三源交叉（1-2 分钟）

**核心机制：属性值必须命中至少 1 个数据源，禁止 AI 自由编造**

```
┌─────────────────────────────────────────────┐
│ 属性字段              数据源优先级             │
├─────────────────────────────────────────────┤
│ 材质 Material         1688抓取 > 竞品Top10 > 用户填 │
│ 尺寸 Size             1688抓取 > 用户填              │
│ 颜色 Color            1688抓取 > 竞品Top10          │
│ 认证 Certificate      用户填 > 1688抓取             │
│ MOQ                   用户填 > 1688抓取             │
│ 应用场景 Application  竞品Top10 > 类目字典           │
│ 卖点 Selling Points   竞品Top10 分析 > 用户填        │
│ 包装 Packaging        1688抓取 > 用户填              │
│ 交期 Lead Time        用户填 > 行业默认              │
│ OEM/ODM               用户填（默认 Yes）             │
└─────────────────────────────────────────────┘
```

**输出格式（示例）：**

| 属性字段 | 建议值 | 数据源 | 置信度 |
|---|---|---|---|
| Material | Aluminum pole + Polyester canopy 180g | 1688抓取 | HIGH |
| Size | Ø3m / Ø2.7m / Ø2.5m | 竞品Top10 高频规格 | HIGH |
| Color | Beige / Grey / Green / Navy | 竞品Top10 | HIGH |
| UV Protection | UPF 50+ | 用户填 (CE, UV test) | HIGH |
| Frame Material | Aluminum | 1688抓取 | HIGH |
| Windproof Design | Yes | 竞品Top10 高频卖点 | MID |
| Base Weight | **[需人工确认]** | 无数据源 | ⚠️ |
| Warranty | 1 year | 类目字典 | MID |

**红线：** 任何字段找不到 ≥1 个数据源 → 标 `[需人工确认]`，不填任何默认值

---

### 阶段 3：价格三角定位（1 分钟）

**输入：**
- 成本锚：1688 原价（或用户填的成本）
- 市场锚：ICBU 同类目 Top10 FOB 价格带（min / median / max）
- 目标市场：影响关税加成

**计算逻辑（爱以思实测系数）：**

```python
# 类目加价系数
category_multiplier = {
    "户外垫 / Outdoor Mat / Rug":      2.3,
    "庭院伞 / Patio Umbrella":         2.0,
    "储物 / Storage / Shed":           2.2,
    "五金机械 / Hardware / Machinery": 2.5,
    "纺织服饰 / Textile / Apparel":    2.4,
    "默认":                            2.2,
}

# FOB 建议价 = 1688成本 × 系数
suggested_fob = cost_1688 * multiplier

# 与市场锚校验
if suggested_fob < market_min:
    warning = "低于市场底价，检查成本或提高定位"
elif suggested_fob > market_max:
    warning = "高于市场顶价，需要差异化卖点支撑"
else:
    warning = "位于市场合理区间"

# 阶梯价（3 档）
tier_prices = {
    "100-499 pcs":  suggested_fob * 1.00,
    "500-999 pcs":  suggested_fob * 0.93,
    ">=1000 pcs":   suggested_fob * 0.87,
}
```

**输出格式：**

```
【价格三角定位报告】

📌 成本锚（1688 原价）: $18.50 / pcs
📌 市场锚（ICBU 同类 Top10）:
   - 最低: $32
   - 中位: $52
   - 最高: $95
📌 类目系数: 2.0x（庭院伞）
📌 建议 FOB: $37.00 / pcs
📌 校验: ✅ 位于市场合理区间（32-95）

【阶梯价建议】
| MOQ 段位      | 单价 (FOB) | 毛利率 (估) |
|---------------|-----------|-------------|
| 100-499 pcs   | $37.00    | ~50%        |
| 500-999 pcs   | $34.40    | ~46%        |
| >=1000 pcs    | $32.20    | ~43%        |

【竞品参考】
- Top1 竞品: $45.00 (12年金牌, 5星) - URL
- Top2 竞品: $38.50 (8年金牌, 4星) - URL
- Top3 竞品: $52.00 (15年金牌, 5星) - URL

⚠️ 红线：
- 低于 $28 亏本（成本+基础费用）
- 高于 $65 需强差异化支撑
```

**红线：**
- 缺 1688 成本 → 不给建议价，只输出市场锚，让主公补成本
- 缺市场锚 → 只按系数算，标注"未做市场校验"
- **禁止拍脑袋定价**

---

### 阶段 4：全套发品包生成（2-3 分钟）

调用现有技能 `icbu-bestseller-listing` 的输出结构：

**4.1 六版爆品标题**

针对不同关键词维度，各出 1 版（共 6 版）：
- V1 材质工艺型：`3m Aluminum Pole Polyester Outdoor Patio Umbrella with UV Protection`
- V2 场景应用型：`Garden Restaurant Hotel Outdoor Cantilever Patio Umbrella 3m`
- V3 认证背书型：`CE Certified UV50+ Windproof Outdoor Umbrella for Backyard Pool`
- V4 长尾场景型：`Custom Logo Commercial Grade Outdoor Umbrella for Cafe Terrace`
- V5 目标市场型：`European Standard Patio Umbrella with EU Compliance Aluminum Frame`
- V6 差异化卖点：`Wind Resistant Foldable Outdoor Umbrella with Reinforced Ribs`

**4.2 关键词矩阵**

| 类型 | 关键词 | 月搜索量参考 |
|---|---|---|
| 核心大词 | outdoor umbrella | 高 |
| 类目词 | patio umbrella / garden umbrella | 高 |
| 材质词 | aluminum umbrella / polyester umbrella | 中 |
| 功能词 | windproof umbrella / UV umbrella | 中 |
| 场景词 | restaurant umbrella / hotel umbrella | 中 |
| 长尾词 | 3m outdoor patio umbrella with base | 低但精准 |

**4.3 五张主图脚本**

- 主图 1（白底）：产品 45° 正面 + 撑开状态 + 突出 3m 尺寸标注
- 附图 1（尺寸）：产品与身高 1.7m 人物对比图 + 3m Ø 尺寸线标
- 附图 2（材质细节）：铝杆截面 + 涤纶布面 UV50+ 特写 + 缝线工艺
- 附图 3（场景应用）：欧美庭院/餐厅露台真实场景多图拼接
- 附图 4（功能演示）：抗风测试演示图 + Windproof 图标标签
- 附图 5（认证包装）：CE + UV test 证书 + 出口纸箱包装

**4.4 八模块详情页文案结构**

01. Banner：产品全景 + 一句话 slogan
02. 核心卖点 4 卡片：材质 / 抗风 / UV / 定制
03. 材质工艺细节：引线标注爆炸图
04. 多场景应用：4-6 张场景大图
05. 尺寸规格：多尺寸对照表 + Ø3m / Ø2.7m / Ø2.5m
06. 生产实力：工厂 / 产能 / 认证
07. 包装物流：出口包装 + 交期
08. 服务保障：MOQ + OEM + 售后

---

### 阶段 5：交付报告 + 后台可复制清单（30 秒）

**输出物：**

1. **完整分析报告** `.md` → 写入 `${workspace}/deliverables/smart-publish-<产品名>-<日期>.md`
2. **后台字段快速填入清单**（主公一键复制到 ICBU 后台）：

```
======================
📋 一键填入 ICBU 后台
======================

【标题】(选用 V1)
3m Aluminum Pole Polyester Outdoor Patio Umbrella with UV Protection for Garden Restaurant

【类目】Home & Garden > Furniture > Outdoor Furniture > Outdoor Umbrellas

【关键词 Top 3】
outdoor umbrella / patio umbrella / garden umbrella

【属性表】
- Material: Aluminum + Polyester
- Size: Ø3m
- Color: Beige / Grey / Green / Navy
- UV Protection: UPF 50+
- Frame Material: Aluminum
- Windproof: Yes
- Warranty: 1 year
- [需人工确认]: Base Weight

【MOQ 阶梯价】
100-499 pcs: $37.00
500-999 pcs: $34.40
>=1000 pcs:  $32.20

【交期】25-35 days
【OEM/ODM】Yes
【包装】Export carton, 1 pc/carton
【认证】CE, UV test

【主图脚本】见完整报告
【详情页文案】见完整报告
```

---

## ⚠️ 铁律清单

1. **属性禁止编造**：无数据源 → 必标 `[需人工确认]`
2. **价格禁止拍脑袋**：无 1688 成本 → 不给建议价
3. **每个字段带来源**：HIGH/MID/LOW 置信度必须标
4. **主公可否决**：所有 AI 建议均为草案，主公改字段后重跑
5. **数据保鲜**：市场锚数据 >7 天需重新拉
6. **爱以思专属**：户外垫走 2.3x、庭院伞走 2.0x、其他默认 2.2x

---

## 🔧 工具调用清单

| 阶段 | 工具 | 用途 |
|---|---|---|
| 阶段 1 | `web_fetch` | 抓 1688 / 竞品详情页 |
| 阶段 1 | `product_supplier_search` | 拉 ICBU 同类竞品 Top10 |
| 阶段 3 | `tariff-search` (可选) | 目标市场关税查询 |
| 阶段 4 | `icbu-bestseller-listing` (可选) | 完整发品包生成参考 |
| 阶段 5 | `write` | 落地报告文件 |

---

## 📁 输出目录约定

- 完整报告：`deliverables/smart-publish-<产品英文名>-YYYYMMDD.md`
- 后台清单：报告末尾附「一键填入 ICBU 后台」段落
- 主图脚本：如需真出图，追加调 `image_generate`（不默认执行，主公另说）

---

## 🎬 首次使用示例

主公输入：
```
发品：Outdoor Patio Umbrella，欧洲中东市场，铝杆 3m，CE + UV test
```

Skill 自动执行：
1. 识别为「触发 B（产品名 + 市场）」路径
2. 调 `product_supplier_search` 拉 ICBU Top10 竞品
3. 属性锚定 + 三角定价
4. 生成全套发品包
5. 写文件 + 输出后台清单

预计耗时：3-5 分钟

---

（Skill v1.0，创建于 2026-07-03，供爱以思店铺发品优化端口使用）
