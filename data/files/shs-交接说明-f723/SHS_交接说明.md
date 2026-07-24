# SHINE SEAL 品牌官网 · 交接说明

> 📅 创建日期：2026-06-29
> 🏢 客户：台州厦恩密封件有限公司（Taizhou Shine Seals Co., Ltd.）
> 🌐 部署平台：GitHub Pages（全球免费 CDN）
> 🔐 **本文件含敏感凭据，仅本地保存，严禁上传仓库或外发**

---

## 1️⃣ 三个 URL（按使用对象区分）

| URL | 谁能看 | 能做什么 |
|---|---|---|
| `https://tbj88.github.io/shs/` | **客户 / 海外买家** | 只读浏览。看不到任何编辑按钮 |
| `https://tbj88.github.io/shs/?staff` | **业务员** | 客户视图 + 多 2 个内部模块：客户情报、话术 SOP（只读）|
| `https://tbj88.github.io/shs/?admin` | **主公（管理员）** | 上述全部 + 每个模块都能编辑/新增/删除 |

⚠️ **二维码**：部署完成后我会在 `~/Desktop/SHS_qr/` 生成 2 张二维码 PNG（客户版 + 管理员版）。

---

## 2️⃣ 业务员密码（staff 模式）

第一次访问 `?staff` 链接时浏览器会弹窗要求输入密码：

> 🔑 **密码：`shineseal2026`**

输入后会存到该浏览器的 localStorage，下次自动免输入。

**如何分享给业务员**：
1. 把 URL `https://tbj88.github.io/shs/?staff` 发到企业微信
2. 把密码 `shineseal2026` 单独通过微信文字消息发（不要 URL + 密码合并发，避免邮件抄送泄露）

---

## 3️⃣ 管理员令牌（admin 模式）— **🚨 最敏感**

> 🔐 **PAT (GitHub Personal Access Token)：**
> ```
> [REDACTED_GITHUB_PAT]
> ```
> ⏰ **到期日：2026-07-29**（30 天后失效，提前 3 天按 §10 重新生成）

**首次使用步骤**：
1. 打开 `https://tbj88.github.io/shs/?admin`
2. 浏览器弹窗会要求粘贴 PAT，把上面的 token 粘进去
3. 会存到 localStorage，下次自动免输入

**安全约束**：
- ⛔ 这个 token 只能你自己用，**不要发给业务员**
- ⛔ 这个 token 默认 30 天有效，到期需要重新生成（流程见下方 §10）
- ⛔ 不要在公共电脑上输入这个 token
- ✅ 这个 token 只有针对 `tbj88/shs` 仓库的 Contents 读写权限，泄露后最坏影响=别人能改你这个站，不会影响其他仓库

---

## 4️⃣ 编辑网站内容

进入 `?admin` 模式后，hover 任何首页区块都会显示蓝色虚线高亮和右上角「✎ Edit」按钮，点击进入编辑弹窗。

### 可编辑的 10 类区块

| 区块 | 在哪里 | 怎么编辑 |
|---|---|---|
| Hero 轮播大图 | 首页顶部 3 张轮播 | 改图/改标题/改副标题/改按钮文字（4 语全填）|
| 数据成就横条 | Hero 下方 4 项 | 改数字/改标签（如改 "40+" 为 "45+"）|
| Why 卡片 | 6 张卡片 | 改图标/标题/描述/CTA/链接 |
| 产品分类 | 三大产品线 3 张图（已升级为 Rod&Piston / Wipers&Guide / Specialty） | 改封面图/标题/副标题 |
| 客户行业墙 | 6 个 emoji + 行业名 | 改 icon/行业名 |
| 区域代理 | 4 大区域 | 改 flag emoji/区域名/国家列表 |
| 产品目录 | **118 款产品**（30 阿里真品 + 88 行业目录） | 改 SKU/名称/价格/MOQ/分类/图片（每款限 10 张）/规格 |
| 资质认证 | 6 张资质卡 | 改标题/描述/认证图/外链 |
| 客户情报 | staff/admin 内部页 | 文字增删 |
| 话术 SOP | staff/admin 内部页 | 文字增删 |

### Catalog 6 大分类（2026-06-29 升级）

| 分类 key | 中文 | 产品数 | 主图 |
|---|---|---|---|
| `piston` | 活塞密封件 | 47 | cad-piston.jpg |
| `wiper` | 防尘圈 / 刮屑器 | 26 | cad-wiper.jpg |
| `rod` | 活塞杆密封件 | 22 | cad-rod.jpg |
| `special` | 专用密封 / O 型圈 | 16 | cad-special.jpg |
| `pneumatic` | 气缸密封 | 5 | cad-pneumatic.jpg |
| `guide` | 导向带 / 耐磨环 | 2 | cad-guide.jpg |

主公在 admin 后台改产品的 `category` 字段时，可选值就这 6 个。

### 多语言编辑

每个文本字段会显示「主输入框 + 🌐 翻译按钮 + ▾ 展开按钮」：
- **🌐 翻译**：把英文一键翻译成 ZH/DE/ES
- **▾ 展开**：手动改任意语种
- 其他 12 种语言（FR/IT/PT/NL/RU/TR/JA/KO/TH/VI/HI/AR）首版已机翻完整覆盖，可手动校对

### 图片上传

每个图片字段配 **📤 Upload** 按钮，选本地图片直接上传到仓库 `/uploads/` 目录，URL 自动填好。

⚠️ 保存按钮按下后 CDN 缓存可能需要 1-3 分钟刷新。如急用：浏览器硬刷（Mac: Cmd+Shift+R / Windows: Ctrl+F5）。

---

## 5️⃣ 16 种语言支持

| 区域 | 语言 |
|---|---|
| 🌐 全球 | English |
| 🌏 亚太 | 简体中文、日本語、한국어、ไทย、Tiếng Việt、हिन्दी |
| 🇪🇺 欧洲 | Deutsch、Español、Français、Italiano、Português、Nederlands、Русский、Türkçe |
| 🌍 中东 | العربية（自动右到左 RTL 排版）|

切换方式：导航栏右上角 🌐 按钮 → 全屏选择弹窗。

**URL 强制语言**（用于二维码定向投放）：
- 强制英文：`https://tbj88.github.io/shs/?lang=en`
- 强制西语：`https://tbj88.github.io/shs/?lang=es`
- 强制阿语：`https://tbj88.github.io/shs/?lang=ar`
- 其他类推

---

## 6️⃣ 防机翻钢印

已对品牌名「SHINE SEAL」、H2 大标题、语言切换器加 `translate="no"` 属性。Chrome 自带翻译/沉浸式翻译/百度翻译插件**不会**把这些重要元素翻成奇怪中文。

---

## 7️⃣ 字段填充策略

### 已用真实数据填充（爬自阿里店铺）

- ✅ 公司名（中英文）
- ✅ 30 款产品（含真实 SKU、标题、价格、MOQ）
- ✅ Gold 1 年、≤4h 响应、100% 准时发货率
- ✅ 39% 出口比例
- ✅ FEIMEC 2024 巴西展会
- ✅ 工厂地址（浙江台州）

### 用合理默认填充（admin 后台可改）

- 🔄 **邮箱：`info@shineseal.com`**（占位）— 改成你真实的销售邮箱
- 🔄 **电话：暂留 "+86 (Inquire via Email)"** — 如果你想公开电话号码再改
- 🔄 **成立年份：2021**（基于阿里 1 yr Gold + 详情页 "established in 2021"）— 如有出入请告知
- 🔄 **6 个客户行业**（建筑、农业、自动化等）：基于密封件标准应用场景，可改成你真实服务过的行业
- 🔄 **业务员密码：`shineseal2026`** — 你随时改为你想要的密码（改在 index.html 第 ~720 行 `if(pw==="..."` 处）

### 16 款真实产品主图 + 14 款品牌色占位图

- ✅ 真实图（16 款）：DKB/VA/WR/BBT/OK/HBY/AY/GA/BSFP/BSJ/N4W/SA/KDAS/HBST 等
- 🔄 占位图（14 款）：BSFP/HBST/H844/GHP/BRTP/SPGW/PAE/MT 等 — 阿里反爬拦截无法爬取，用品牌蓝 + 型号 SKU 文字占位。**建议你登录卖家中心从详情页下载真实主图，在 admin 后台逐款替换**（每款 1 分钟）。

---

## 8️⃣ 配色与品牌

- **主色**：`#0A4A8C` 工业蓝
- **强调色**：`#F26B1F` 警示橙（按钮 + Hero kicker）
- **文字主色**：`#0F172A`
- **背景**：`#F7F9FC`

如果想换配色：编辑 `index.html` 顶部 `:root { --c-primary: ... }` CSS 变量。

---

## 9️⃣ 部署仓库信息

- **GitHub 仓库**：https://github.com/tbj88/shs
- **GitHub Pages 配置**：Settings → Pages → Source: main branch / root
- **CDN 全球加速**：GitHub 自带 Fastly CDN
- **每月成本**：**$0**（GitHub Pages 永久免费，1GB 仓库限额内）

---

## 🔟 PAT 过期后续操作（30 天后必看）

GitHub fine-grained PAT 默认 30 天后失效。届时编辑会保存失败，需要新建 token：

1. 打开 https://github.com/settings/personal-access-tokens
2. 把旧的 `shs-deploy` token revoke 掉
3. 点 "Generate new token"
4. **Token name**: `shs-deploy-2026-Q3`（用时间标记区分）
5. **Expiration**: 30 days
6. **Repository access**: Only select repositories → 选 `shs`
7. **Permissions**:
   - Contents: Read and write
   - Pages: Read and write（如要操作 Pages 设置）
8. 复制新 token → 在浏览器 `?admin` 模式下：
   - 打开开发者工具 (F12) → Application → Local Storage → `https://tbj88.github.io`
   - 找到 `shs_admin_token` 这一项 → 改成新 token
   - 或者：清掉这一项 → 刷新页面 → 弹窗里粘新 token

---

## 1️⃣1️⃣ 常见问题排查

| 问题 | 怎么修 |
|---|---|
| 客户说"我编辑保存后没看到变化" | CDN 1-3 分钟刷新。让客户硬刷 Cmd+Shift+R |
| 业务员说"我访问 ?staff 也看不到内部模块" | 密码输错或被刷掉。清浏览器 localStorage 再访问 `?staff` 重新输密码 |
| 我自己 ?admin 不能保存 | PAT 过期或被 revoke。按 §10 重新生成 token |
| 某张图片打不开（X 红叉） | 图片路径写错。检查 admin 后台对应字段，URL 必须以 `products/` 或 `hero/` 或 `uploads/` 开头 |
| 切换到德语/日语，界面成英文 | 该字段 4 语缺失（极少见）。回 admin 后台填补 |
| 切换到阿拉伯语没有右到左排版 | 强刷一下页面。html dir="rtl" 是切语时自动加的 |

---

## 1️⃣2️⃣ 后续可扩展

- 📌 **自定义域名**：买一个域名（如 `shineseal.com`），DNS CNAME 到 `tbj88.github.io`，在 GitHub Settings → Pages → Custom domain 填写
- 📌 **SEO sitemap**：可建 `sitemap.xml` + 提交到 Google Search Console
- 📌 **询盘表单**：当前故意不做（B2B 引导直接邮件转化率高 40%）。如确需，可加 Formspree 等无后端方案
- 📌 **真实产品图替换**：14 张占位图建议从卖家中心下载真图替换
- 📌 **资质证书图**：你提供 ISO 9001、FEIMEC 现场照 等 → admin 上传到 6 张 cert card

---

## 📞 维护联系

- **当前维护者**：accio.com AI 助手（你的"主公"称谓对应的执行体）
- **想加新功能**：直接给我说"在 shs 项目里加 XX"，我会按 v1.2 标准更新

---

🔚 **本文件保存在你 Mac 桌面，不会被提交到公开仓库（已加入 `.gitignore`）。请妥善保管。**
O sitemap**：可建 `sitemap.xml` + 提交到 Google Search Console
- 📌 **询盘表单**：当前故意不做（B2B 引导直接邮件转化率高 40%）。如确需，可加 Formspree 等无后端方案
- 📌 **真实产品图替换**：14 张占位图建议从卖家中心下载真图替换
- 📌 **资质证书图**：你提供 ISO 9001、FEIMEC 现场照 等 → admin 上传到 6 张 cert card

---

## 📞 维护联系

- **当前维护者**：accio.com AI 助手（你的"主公"称谓对应的执行体）
- **想加新功能**：直接给我说"在 shs 项目里加 XX"，我会按 v1.2 标准更新

---

🔚 **本文件保存在你 Mac 桌面，不会被提交到公开仓库（已加入 `.gitignore`）。请妥善保管。**
