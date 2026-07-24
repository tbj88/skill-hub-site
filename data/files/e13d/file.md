---
name: 长筒丝袜
description: >
  阿里国际站/亚马逊 B2B「长筒丝袜（性感情趣袜类）」爆品主图 + 附图 + A+ 信息图一键出图与归档技能包。
  专为「包芯丝 Core-Spun Silk / 几何图案 / 过膝长筒袜」品类打造，避坑「材质错认成网眼」「图案错画成绷带缠绕」
  「双腿不对称」「色深不均匀」四大典型翻车点。用户提供一张长筒丝袜原图 → 自动产出 6 张成品图（01 模特主图 + 
  02 材质细节 + 03 多配色 + 04 场景 + 05 工厂 + 06 A+ 信息图）+ 5 条中英爆品标题 + 9 条中英卖点 + 桌面归档。
  触发关键词：长筒丝袜、过膝袜、包芯丝、Core-Spun、Fishnet、Thigh-High、Stockings、Over-Knee、
  性感丝袜、情趣袜、Hosiery、绷带袜、几何丝袜、出图、做主图、做一套图。
  适用场景：用户提供长筒丝袜产品图（1688/阿里/自拍）并要求"出图/做主图/做一套国际站图"时触发。
license: 私人使用（导出于 2026-07-12，未装入智能体系统）
---

# 长筒丝袜 · B2B 爆品出图 + 归档一体化 SKILL

> **一句话定位**：给一张长筒丝袜原图 → 产出 6 张 jpg + 1 份中英文案 txt → 桌面归档。
> **来源**：从主公 2026-07-12 实战调优提炼（含 4 次翻车纠错），避坑 4 大典型误区。

---

## 0. 触发协议

**必触发**：用户上传长筒丝袜产品图（含 1688 链接/自拍图/成品图）+ 关键词：
- "出图" / "做主图" / "生成主图" / "做一套图" / "国际站图"
- "长筒袜" / "过膝袜" / "丝袜" / "stockings" / "thigh-high" / "over-knee"

**不触发**：其他品类（户外垫/工业品/五金/机械等），走 `汤 1主图+5附图+标题` 或其他专属 skill。

---

## 1. 执行前 4 大避坑铁律（血泪教训）

### 🚫 铁律 1：材质术语必须精确
| ❌ 错误描述 | ✅ 正确描述 |
|-----------|-----------|
| Sheer Mesh / Fishnet / Nylon Mesh | **Core-Spun Silk Yarn / Core-Spun Yarn (Nylon-Covered Spandex Core)** |
| Open Weave / Woven Grid | **Silky Semi-Sheer / Ultra-Thin Silky Matte Finish** |

**原理**：包芯丝是"氨纶芯 + 尼龙丝外包"，视觉上是**丝面光滑、无网眼、雾面半透**，像高档丝袜；写成 mesh/fishnet 会被 AI 画成粗糙网眼粗腿感，档次瞬间掉。

### 🚫 铁律 2：图案术语必须精确
| ❌ 错误描述 | ✅ 正确描述 |
|-----------|-----------|
| Cross Bandage / Wrapping Bandage | **3 Segments divided by Horizontal Bars + V-Triangle Blocks** |
| Spiral / Wrapped Ribbon | **Thick Straight Diagonal Stripes forming V / Inverted-V / Diamond blocks** |

**原理**：AI 看到 "bandage" 会画成"木乃伊绷带缠绕"（一圈圈螺旋），但实际几何图案是**分段块状**（横带切成 3 截，每截内部是三角形），必须显式写 `NOT wrapping bandages, NOT spirals`。

### 🚫 铁律 3：双腿必须对称等粗
必写关键词组：
```
BOTH legs wear IDENTICAL stockings, same slender proportion, perfectly mirror-symmetric.
Pattern crisp and mirror-symmetric between two legs.
```
不写会翻车成"左腿粗右腿细 + 图案不对称"。

### 🚫 铁律 4：袜色必须均匀无渐变
必写关键词组：
```
uniform deep solid black color throughout, NO gradient, NO fading, NO patches.
Silky yarn evenly semi-transparent everywhere.
Soft even frontal studio lighting eliminating all shadows and gradients.
```
不写会翻车成"上深下浅 + 左右阴影不均"。

---

## 2. 6 张标准图集结构（长筒丝袜专属）

| # | 类型 | 内容 | task_type | aspect |
|---|------|------|-----------|--------|
| 01 | 主图·模特站立 | 双腿并立展示袜身全长 + 灰色无缝背景 + OEM Available 角标 | complex_generation | 1:1 |
| 02 | 附图·材质细节 | 3 段特写：顶部硅胶防滑带 / 丝面纹理特写 / 无缝脚趾 | complex_generation | 1:1 |
| 03 | 附图·多配色 | 4 色平铺（Black/Nude/Coffee/Wine）+ 绿色横幅标题 | complex_generation | 1:1 |
| 04 | 附图·应用场景 | 双场景：精品店陈列 + 派对夜店穿着 | complex_generation | 1:1 |
| 05 | 附图·工厂 OEM | 工厂堆叠 + 私标包装样 + ISO/OEKO-TEX 徽标 | complex_generation | 1:1 |
| 06 | A+ 信息图 | 5 模块浓缩：Hero/Customize/Interior/Scenes/Feature Strip | complex_generation | 1:1 |

**02 和 06 之前必被 AI 画错**（材质+图案），本 skill 已通过 4 次实战纠正，prompt 模板已锁死正确画法。

---

## 3. Prompt 模板（照抄即用，占位符替换即可）

> 所有 prompt 通用工具：`image_edit` · `task_type="complex_generation"` · `aspect_ratio="1:1"` · `resolution="2K"` · `preserve_product=true`。
> 所有 prompt 通用参考图：`reference_images=[原产品图 URL 或 alicdn URL]`。

### 3.1 主图 01（模特站立）

```
Create a professional B2B main hero image using this exact CORE-SPUN YARN thigh-high stockings as reference.

CRITICAL MATERIAL: The fabric is CORE-SPUN SILK YARN (nylon-covered spandex core yarn), NOT mesh, NOT 
fishnet, NOT open weave. The surface must look ULTRA-THIN, SMOOTH, SILKY, semi-transparent matte finish 
(like premium hosiery), NO visible mesh holes, NO fishnet grid. Skin tone subtly visible through the smooth 
silky fabric.

CRITICAL PATTERN ACCURACY: {IF SEGMENTED: The stockings pattern is divided into 3 SEGMENTS by THICK 
HORIZONTAL SOLID BLACK BARS (about 3cm wide horizontal bars around upper thigh, above knee, mid-calf). 
Inside EACH segment there are 2-3 THICK STRAIGHT BLACK DIAGONAL STRIPES forming LARGE V-SHAPE / INVERTED-V 
TRIANGLES / DIAMOND SHAPES (tribal geometric blocks). Segments' triangles alternate pointing direction 
(down/up/down). One thick solid black elastic band at top of thigh and one thick solid black cuff at toe. 
Keep this segmented tribal V-triangle geometry 100% consistent with reference — the black stripes sit FLAT 
on the smooth silky yarn surface, NOT wrapped, NOT spiraled.}
{IF LACE: Describe the lace pattern precisely (floral / geometric / scallop edge / etc.).}
{IF PLAIN: Skip and write "pure solid silky black" or the actual color.}

BOTH legs wear IDENTICAL stockings with uniform deep solid black stripes, same slender proportion, 
perfectly mirror-symmetric. Silky yarn evenly semi-transparent everywhere, no color patches.

Pose: young Western female model, ONLY LEGS visible from mid-thigh down, STANDING facing camera, legs 
straight together and parallel, one leg slightly forward showing the pattern, wearing nude pointed 
stiletto pumps. Pure clean light-grey seamless studio backdrop, soft even frontal studio lighting 
eliminating shadows and gradients, professional catalog product shot.

Right-top corner clean white rounded badge with black text "OEM Available". Photorealistic high-end 
lingerie catalog photography, square 1:1, English only correctly spelled.
```

**姿势备选**（按需替换 Pose 段）：
- 座椅并腿：`seated elegantly on a modern grey velvet armchair, legs straight parallel side by side, knees together, nude stiletto pumps`
- 沙发前伸：`sitting on the edge of a modern beige boucle sofa facing camera, both legs together stretched slightly forward, feet resting on wooden floor in nude pointed stilettos`
- 跪姿背视：`kneeling elegantly on a plush ivory bed with both knees down and calves stretched back symmetrically (frog pose from behind view)`

### 3.2 材质细节 02（3 段特写）

```
Create a B2B material detail close-up image using this exact Core-Spun Silk thigh-high stockings as 
reference.

CRITICAL MATERIAL: CORE-SPUN SILK YARN, ULTRA-THIN SMOOTH SILKY semi-transparent matte finish, NO mesh 
holes, NO fishnet.

CRITICAL PATTERN: {同 3.1 段落}

Show 3 macro close-up sections stitched into one square 1:1 frame with clean thin dividers:
(1) LEFT: Top elastic waist band close-up on skin showing silicone anti-slip grip strips inside the wide 
    black elastic band, natural skin tone visible;
(2) CENTER: Extreme macro of the core-spun silk fabric texture stretched over skin, showing the ultra-thin 
    smooth SILKY yarn surface (NO mesh holes, NO fishnet), with one thick flat black diagonal stripe 
    crossing the frame, subtle skin tone glowing through;
(3) RIGHT: Toe area seamless finish close-up in nude pointed heel, showing reinforced toe cuff.

Clean light-grey gradient studio background. Add clean English caption at bottom "Core-Spun Silk Yarn · 
Silky Ultra-Thin · Non-Slip Silicone Top · Seamless Toe". Photorealistic professional textile product 
photography, square 1:1, English only correctly spelled.
```

### 3.3 多配色规格 03

```
Create a B2B spec/variant display image using this exact Core-Spun Silk thigh-high stockings as reference. 
Keep the product design 100% unchanged - only change the base color. Show the SAME stockings in 4 color 
variants displayed side by side flat-lay on pure clean white background: black, skin/nude beige, coffee 
brown, wine red. Each pair folded neatly showing the {V-triangle / lace / geometric} pattern clearly. 
Above the display add a green header bar with white bold text "MULTIPLE COLORS AVAILABLE". Below each pair 
add small clean label "Black / Nude / Coffee / Wine". Add small text "Free Size · Fits 40-75kg" at bottom. 
Photorealistic, catalog product photography, square 1:1, English only correctly spelled.
```

### 3.4 应用场景 04（双场景切割）

```
Create a B2B lifestyle scene image using this exact Core-Spun Silk thigh-high stockings as reference. 
Keep the product 100% unchanged - same pattern, silky yarn, over-knee length. Split the frame into 2 
elegant scenes side by side: 
LEFT — a Western fashion boutique display with 3 pairs neatly hung on chrome hangers under warm 
       spotlights, luxury retail mood; 
RIGHT — a young woman styled in a chic little black dress and nude heels stepping into a upscale 
        nightclub/lounge, only legs from mid-thigh down visible, soft bokeh purple neon background. 
Add clean English caption "Wide Application - Boutique · Party · Club · Lingerie Brand". Photorealistic, 
high-end commercial fashion photography, square 1:1.
```

### 3.5 工厂 OEM 05

```
Create a B2B factory-endorsement image using this exact Core-Spun Silk thigh-high stockings as reference. 
Keep the product 100% unchanged. Split the frame: 
LEFT — many pairs of the same stockings neatly folded and stacked in clean rows of polybags on a modern 
       factory packing table with rolls of nylon yarn and knitting machines blurred in the background, 
       conveying mass production capability; 
RIGHT — three OPP/polybag retail packaging samples with clean minimal white label ("Your Brand Logo Here" 
        placeholder) plus a small color hangtag. 
Top-right small ISO 9001 and OEKO-TEX badge icons. Add clean English caption "OEM/ODM Service - Custom 
Packaging - Certified Factory". Photorealistic, industrial textile photography, square 1:1, English only 
correctly spelled.
```

### 3.6 A+ 信息图 06（5 模块）

```
Create a professional Amazon A+ style multi-module infographic for Sexy Thigh-High Core-Spun Silk 
Stockings, English only, square 1:1 layout. STYLE: clean white background with green and dark-navy accent 
colors.

CRITICAL MATERIAL: The fabric is CORE-SPUN SILK YARN (nylon-covered spandex core yarn) — ULTRA-THIN, 
SMOOTH, SILKY semi-transparent matte finish (like premium hosiery). NOT mesh, NOT fishnet, NOT open weave. 
Black geometric stripes sit FLAT on the smooth silky yarn surface.

CRITICAL PATTERN: {同 3.1 段落，保持 100% 一致}

TOP-LEFT HERO MODULE: Bold dark-navy headline "SEXY THIGH-HIGH" with green sub-headline "Core-Spun Silk 
Stockings", small tagline "Wholesale OEM/ODM · Free Size · Fast Delivery". A row of 4 small circular 
feature icons with labels: "Core-Spun Silk", "Non-Slip Top", "Free Size", "Seamless Toe". Large hero 
photo of a Western model wearing the stockings, only legs from mid-thigh down visible, seated elegantly, 
both legs symmetric showing the segmented pattern clearly on smooth silky fabric.

TOP-RIGHT CUSTOMIZE MODULE: Green header bar "CUSTOMIZE YOUR STOCKINGS". "COLOR OPTIONS" with 4 flat solid 
swatches labeled: "Black", "Nude", "Coffee", "Wine". "PATTERN OPTIONS" row of 3 small flat pattern swatches 
labeled: "V-Triangle", "Diamond", "Zigzag". "SIZE OPTIONS" in green text "Free Size / Plus Size / Custom" 
with line "More sizes available upon request".

RIGHT-MIDDLE INTERIOR MODULE: Photo showing the stocking stretched over a hand demonstrating silky sheer 
transparency and elastic recovery, showing the same pattern on ultra-thin core-spun yarn.

BOTTOM-LEFT SCENES MODULE: Green header bar "PERFECT FOR VARIOUS SCENES" with 4 photo thumbnails labeled 
"Boutique", "Party", "Club Night", "Lingerie Brand".

BOTTOM FEATURE STRIP: Row of 6 grey circular close-up detail shots with captions: "Core-Spun Silk / 
Ultra-Thin", "Non-Slip Band / Silicone Grip", "V-Triangle Pattern / Tribal Sexy", "Seamless Toe / 
Comfort", "High Elastic / Skin-Fit", "Reinforced Sole / Durable". At bottom-right dark-navy block with 3 
white icons and labels: "OEM/ODM / Custom Logo", "MOQ 100 pairs / Small Orders OK", "7-Day Delivery / 
Fast Shipping".

All text clear, correctly spelled, legible English, well-positioned no overlap. Clean professional 
balanced infographic layout. Do NOT add any text or elements not specified.
```

---

## 4. 执行节奏（并行三批）

- **第 1 批（并行 3 张）**：01 主图 · 02 材质 · 03 多配色
- **第 2 批（并行 3 张）**：04 场景 · 05 工厂 · 06 A+ 信息图
- 每张拿到 URL 立即记录，6 张齐了统一归档
- 单张失败（gpt-image-2 空流）直接重跑一次，别改 prompt

---

## 5. 配套文案交付铁律

> **数量硬约束**（不达标不许交付）：
> - **爆品标题 5 条**（中英对照，含"主推 / 词序变体 / 长尾 / 定制 / 场景"5 种切入）
> - **卖点 ≥ 9 条**（中英对照，含"品质/功能/规格/定制/服务/批发/交期/认证"维度标注）

### 5.1 长筒丝袜专属标题模板

| # | 切入 | 英文模板 | 中文对应 |
|---|------|---------|---------|
| ★ | 主推 | Sexy Core-Spun Silk Geometric Thigh High Stockings Wholesale OEM Silky Sheer Over Knee Socks | 女式性感包芯丝几何图案过膝长袜·批发 OEM·真丝质感过膝袜 |
| ② | 词序 | Thigh High Stockings Core-Spun Silk Geometric Pattern Sexy Over Knee Nylon Silky Socks Wholesale | 过膝长袜·包芯丝几何图案·性感尼龙真丝袜·批发 |
| ③ | 长尾 | Ultra Thin Non Slip Silky Sheer Core-Spun Thigh High Stockings Geometric Sexy Club Party Hosiery | 超薄防滑真丝质感包芯丝过膝长袜·几何图案·夜店派对丝袜 |
| ④ | 定制 | Custom Logo OEM ODM Sexy Core-Spun Silk Stockings Free Size Wholesale Thigh High Silky Socks | 定制 Logo OEM ODM 性感包芯丝长袜·均码批发·过膝真丝袜 |
| ⑤ | 场景 | Sexy Lingerie Silky Core-Spun Thigh High Socks for Boutique Nightclub Party Bridal Wholesale Hosiery | 精品店/夜店/派对/婚庆用性感真丝过膝袜·内衣袜类批发 |

### 5.2 长筒丝袜专属卖点模板（9 条）

1. **【品质】** Core-Spun Silk Yarn (Nylon-Covered Spandex Core) — Ultra-thin silky matte finish, skin-friendly / 包芯丝纱线（尼龙+氨纶芯）—— 超薄真丝质感·亲肤透气
2. **【功能】** Unique Geometric Pattern — Sexy tribal V-triangle blocks, no fade after washing / 独家几何图案 —— 性感 V 字三角块·多次水洗不褪色
3. **【功能】** Non-Slip Silicone Elastic Top Band — Stays put all night, no falling down / 顶部硅胶防滑弹力收口·整晚不下滑
4. **【品质】** Seamless Toe & Reinforced Sole — Comfortable for long wear / 无缝脚趾+加固脚底·久穿舒适
5. **【规格】** Free Size (Fits 40-75kg / 155-175cm) — Covers 90% adult women / 均码适配 40-75kg·覆盖 90% 成年女性
6. **【定制】** 4 Stock Colors + Custom Colors on Bulk Orders / 4 色现货 + 大货支持定制配色
7. **【服务】** OEM/ODM Full Service — Custom logo hangtag, polybag, retail box / OEM/ODM 全案定制
8. **【批发】** Low MOQ 100 pairs per color — Small trial orders welcome / 起订量 100 双/色·支持试单
9. **【认证】** OEKO-TEX Standard 100 Compliant — Skin-safe dyes, EU/US ready / OEKO-TEX 100 认证·直供欧美

---

## 6. 归档规范（沿用「汤 1主图+5附图+标题」§4）

- **根目录**：`~/Desktop/图片优化/主图/`
- **子文件夹**：`NN_长筒丝袜-<款式关键词>`（NN 自动递增两位数）
- **图片格式**：默认 jpg（png 下载后 `sips -s format jpeg` 转 jpg）
- **图片命名**：`长筒丝袜_<序号>_<类型>_<YYYYMMDD>.jpg`
- **文案 txt**：`长筒丝袜_文案_<YYYYMMDD>.txt`

### 归档脚本骨架（bash · Mac 专用）

```bash
BASE="$HOME/Desktop/图片优化/主图"
mkdir -p "$BASE"
# 1) 计算下一个序列号
seq=1
for d in "$BASE"/[0-9][0-9]_*/; do
  [ -d "$d" ] || continue
  n=$(basename "$d" | cut -d_ -f1); n=$((10#$n))
  [ "$n" -ge "$seq" ] && seq=$((n+1))
done
SEQ=$(printf "%02d" "$seq")
FOLDER="$BASE/${SEQ}_长筒丝袜-<款式>"
mkdir -p "$FOLDER"
DATE=$(date +%Y%m%d)

# 2) 逐张下载 URL → 转 jpg
declare -a URLS=(
  "<主图URL>|01_主图_模特站立"
  "<细节URL>|02_附图_材质细节"
  "<配色URL>|03_附图_多配色"
  "<场景URL>|04_附图_应用场景"
  "<工厂URL>|05_附图_工厂OEM"
  "<A+URL>|06_A+信息图"
)
for item in "${URLS[@]}"; do
  URL="${item%%|*}"
  NAME="${item##*|}"
  PNG="$FOLDER/长筒丝袜_${NAME}_${DATE}.png"
  JPG="$FOLDER/长筒丝袜_${NAME}_${DATE}.jpg"
  curl -fsSL "$URL" -o "$PNG"
  sips -s format jpeg "$PNG" --out "$JPG" >/dev/null 2>&1
  rm -f "$PNG"
done
```

---

## 7. 上架前 7 条自检提醒

1. AI 生成英文小字（尤其 A+ 卖点条 / 场景标签）人工逐字核对拼写
2. 认证徽标（ISO 9001 / OEKO-TEX）按工厂真实持有情况保留或删除
3. 尺码文案「Free Size · Fits 40-75kg」按实测替换，防退货纠纷
4. MOQ / 交期按贵司实际能力改写（默认 100 双 / 7 天）
5. 情趣袜类目在中东/东南亚部分国家有合规红线，模特图坚持"仅腿部构图"
6. 阿里国际站首图禁角标，01 主图上架前用 PS 移除"OEM Available"
7. 04 场景图若目标市场保守（中东/印度），把"夜店紫色霓虹"换成"婚庆现场 / 家居派对"

---

## 8. 4 大典型翻车 · 快速诊断表

| 症状 | 根因 | 补救 |
|------|------|------|
| 袜子变成粗糙网眼（像渔网） | prompt 写了 mesh / fishnet | 改 "Core-Spun Silk Yarn, NO mesh holes, NO fishnet" |
| 图案变成螺旋绷带缠腿 | prompt 写了 bandage / wrapping | 改 "3 segments + horizontal bars + V-triangle blocks, NOT wrapped, NOT spiraled" |
| 左腿粗右腿细 / 图案不对称 | 缺 symmetric 强约束 | 加 "BOTH legs IDENTICAL, mirror-symmetric" |
| 袜色上深下浅（渐变） | 侧光 / 姿势遮挡 | 改 "even frontal lighting, NO gradient, uniform solid black" |

---

## 9. 版本记录

- **v1.0（2026-07-12）**：从主公实战调优提炼首版。4 次纠错沉淀（材质术语/图案术语/双腿对称/袜色均匀），A+ 信息图和主图 prompt 已锁死正确画法。
- **导出位置**：`~/Desktop/长筒丝袜/`（未装入智能体系统 skill 库，属主公私人便携版）

---

## 10. 附录

### 10.1 references/ 目录
- `references/pattern_reference.md` — 4 种典型图案术语速查（V-Triangle / Lace / Fishnet / Plain）
- `references/material_reference.md` — 长筒袜 6 种材质术语对照表

### 10.2 examples/ 目录
- `examples/v-triangle-example.md` — V 字三角块款完整交付案例（含 6 张成品图 URL + 文案）
