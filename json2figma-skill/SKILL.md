---
name: json2figma-ui-demo
description: 根据需求生成可供 json2figma 插件导入的 UI Demo JSON。需要在用户希望通过 JSON 直接在 Figma 中快速搭建界面样稿时使用。
---

# JSON2Figma UI Demo Skill

## 使用前提
- 仅在用户明确需要"生成 JSON 并通过 json2figma 插件导入 Figma"时启用。
- 输出内容需为结构化 JSON 或附带 JSON 片段，保证与插件的解析要求一致（详见下方工作流程）。

## 工作流程
1. **厘清需求**：确认界面类型、组件构成、主要文案、品牌色等。缺少信息时必须澄清。
2. **规划层级**：制定 `DOCUMENT → PAGE → FRAME/COMPONENT → 子节点` 结构，记录每个节点用途与布局模式。
3. **构建节点属性**：
   - 对容器：设定 `type`, `id`, `name`, `x`, `y`, `width`, `height`，如需自动布局补充 `layoutMode`, `primaryAxisSizingMode`, `padding*`, `itemSpacing`。
   - 对视觉样式：使用 0-1 浮点 RGB 设置 `fills`、必要时补 `strokes`、`effects`。
   - 对文本：提供 `characters`, `fontName`（Inter Regular/Medium/Bold/Semi Bold 四种字重之一）, `fontSize`, `fills`，必要时设置 `textAutoResize`。
   - 对矢量：同时设置 `fillGeometry` 和 `vectorPaths`，确保路径命令后有空格，使用正确的 `windingRule`。
4. **组装 JSON**：按照第 2 步的结构填充字段，保持键排序与缩进一致，便于粘贴。
5. **校验**：依据校验表逐项检查，确保语法有效、数值范围正确、字体已在控制器预加载。
6. **⚠️ Auto-Layout 验证**（关键步骤）：
   - 检查所有 `counterAxisAlignItems` 是否使用了无效的 `"STRETCH"` 值
   - 检查所有 `primaryAxisSizingMode: "FIXED"` 的元素是否有显式 `width` 或 `layoutAlign: "STRETCH"`
   - 检查需要填充父容器的子元素（Header、Footer、Divider、Button 等）是否添加了 `layoutAlign: "STRETCH"`
7. **交付**：返回 JSON（必要时附引用说明），提醒用户将结果粘贴到插件 UI 中。

## 核心参考文档

### 节点类型与属性
- **[figma-api-schema.md](references/figma-api-schema.md)** - 完整的 Figma 节点类型和属性参考，包含所有主要节点的 schema 定义和示例
- **[mixins-and-renderers.md](references/mixins-and-renderers.md)** - 各节点与 mixin 对应关系，了解不同节点的可用属性及其处理方式

### 特殊节点构造
- **[vector-construction.md](references/vector-construction.md)** - VECTOR 节点详细构造指南，包含路径语法、坐标系统、缠绕规则等
- **[complex-types.md](references/complex-types.md)** - 复杂类型定义（Paint、Effect、Constraints、FontName 等）

### 问题排查与优化
- **[faq-best-practices.md](references/faq-best-practices.md)** - 常见问题解答和最佳实践，包含调试技巧和常见模式
- **[generation-checklist.md](references/generation-checklist.md)** - JSON 生成准则检查表
- **[plugin-overview.md](references/plugin-overview.md)** - 插件数据流与字段说明

## JSON 片段模板
以下模板展示根节点、页面与卡片 Frame 的最小必需字段，可按需扩展：

```json
{
  "id": "doc-1",
  "type": "DOCUMENT",
  "name": "UI Demo",
  "documentColorProfile": "SRGB",
  "children": [
    {
      "id": "page-1",
      "type": "PAGE",
      "name": "Preview",
      "children": [
        {
          "id": "frame-root",
          "type": "FRAME",
          "name": "Root",
          "x": 100,
          "y": 120,
          "width": 320,
          "height": 240,
          "layoutMode": "VERTICAL",
          "primaryAxisSizingMode": "AUTO",
          "counterAxisSizingMode": "AUTO",
          "paddingTop": 24,
          "paddingBottom": 24,
          "paddingLeft": 24,
          "paddingRight": 24,
          "itemSpacing": 16,
          "fills": [
            {
              "type": "SOLID",
              "visible": true,
              "opacity": 1,
              "blendMode": "NORMAL",
              "color": { "r": 1, "g": 1, "b": 1 }
            }
          ],
          "children": []
        }
      ]
    }
  ]
}
```

> **重要更新**: 经测试发现，插件实际需要的 JSON 格式比上述简化模板更完整。简化的 skill 模板虽然更易读，但缺少 Figma 插件渲染引擎所需的元数据字段（如 `isAsset`、`detachedInfo`、`relativeTransform` 等），会导致导入失败。

更完整的可直接导入样例参见：
- [references/sample-card.json](references/sample-card.json) (简化格式，仅供参考)
- [references/login-demo-complete.json](references/login-demo-complete.json) (完整 Figma 格式，可直接导入)
- 官方导出片段参考 [references/test-snippet.json](references/test-snippet.json)

## 输出要求
- 默认输出 **单个 JSON 对象**，使用 Markdown 代码块 ```json 包裹，保证用户可直接复制。
- 若需拆分，请明确标注每个片段的用途，并提醒最终需整合成 `DOCUMENT` 根节点。
- 所有颜色、位置、尺寸均需为数字；颜色取值范围 0-1，字体名称完全匹配 Inter 字体系列。
- 必要时附带简要导入步骤提醒（粘贴到插件面板、点击 Render JSON）。

## 校验清单
- 按 [references/generation-checklist.md](references/generation-checklist.md) 逐项核对：层级、布局、颜色、文本、JSON 语法。
- 重点检查：
  - 是否遗漏 `fontName` 或 `characters`。
  - 自动布局字段是否成对出现。
  - `children` 是否始终为数组。
  - 颜色值是否在 0-1 范围内。
  - VECTOR 节点是否同时设置了 `fillGeometry` 和 `vectorPaths`。
  - 路径数据命令后是否有空格（如 `"M 0 0"` 而非 `"M0 0"`）。
  - GROUP 节点是否避免使用 auto-layout 属性。
  - 样式 ID 是否设置为空字符串 `""` 或有效 ID。

### ⚠️ Auto-Layout 专项检查（必须执行）
生成 JSON 后，**必须**执行以下验证：

1. **检查无效的 counterAxisAlignItems**：
   ```bash
   # 搜索是否有无效的 "STRETCH" 值
   grep '"counterAxisAlignItems": "STRETCH"' your-file.json
   ```
   如果找到，必须改为 `"MIN" | "CENTER" | "MAX" | "BASELINE"`

2. **检查 primaryAxisSizingMode: "FIXED" 配置**：
   ```bash
   # 列出所有使用 FIXED 的元素
   grep -B5 -A5 '"primaryAxisSizingMode": "FIXED"' your-file.json
   ```
   对每个结果，确认以下之一：
   - [ ] 有显式的 `width` 属性（或 `height`）
   - [ ] 有 `layoutAlign: "STRETCH"` 属性
   - [ ] 或改用 `primaryAxisSizingMode: "AUTO"`

3. **检查常见需要 layoutAlign 的元素**：
   - [ ] Header / Footer 容器
   - [ ] 表单字段容器
   - [ ] 按钮（需要填充父容器宽度时）
   - [ ] 分隔线（Divider）
   - [ ] 菜单项

**快速验证命令**：
```bash
# 一键检查两个常见问题
grep -n '"counterAxisAlignItems": "STRETCH"' your-file.json && \
grep -n '"primaryAxisSizingMode": "FIXED"' your-file.json | grep -v '"width"' | grep -v '"layoutAlign"'
```

详细规则和示例请参考 [figma-api-schema.md](references/figma-api-schema.md) 的 "Auto-Layout 关键规则" 章节。

## 关键注意事项

### 节点类型选择
- **FRAME**：支持 auto-layout，适合容器和组件
- **GROUP**：不支持 auto-layout，仅用于简单分组
- **RECTANGLE**：基础矩形，支持圆角
- **TEXT**：文本内容，必须提供 `fontName` 和 `characters`
- **VECTOR**：自定义矢量路径，需要 `fillGeometry` 和 `vectorPaths`

### 颜色规范
- RGB 值必须在 0-1 范围内（不是 0-255）
- 渐变需要 3 个 `gradientHandlePositions` 点
- 阴影颜色需要包含 alpha 通道（RGBA）

### Auto-Layout 配置
- `layoutMode`: `"NONE"` | `"HORIZONTAL"` | `"VERTICAL"`
- 启用 auto-layout 时必须设置 `primaryAxisAlignItems` 和 `counterAxisAlignItems`
- 子节点可使用 `layoutAlign`, `layoutGrow`, `layoutPositioning`

**⚠️ 关键规则（必须遵守）**：
1. **`counterAxisAlignItems` 没有 `"STRETCH"` 值** - 使用 `"MIN" | "CENTER" | "MAX" | "BASELINE"`
2. **`primaryAxisSizingMode: "FIXED"` 必须配合以下之一**：
   - 显式的 `width` 属性（或 `height`）
   - `layoutAlign: "STRETCH"` 属性
   - 或改用 `primaryAxisSizingMode: "AUTO"`

   否则会导致默认宽度 100px 的布局错误！

详细说明和示例请参考 [figma-api-schema.md](references/figma-api-schema.md) 的 "Auto-Layout 关键规则" 章节。

### 矢量路径规则
- 路径命令后必须有空格：`"M 50 0 L 100 100 Z"`
- 同时设置 `fillGeometry` 和 `vectorPaths`
- 使用正确的 `windingRule`：`"NONZERO"` 或 `"EVENODD"`
- 路径坐标相对于节点左上角 (0,0)

## 示例
- **示例 1：项目状态卡片**  
  用户需求：“给我一个展示项目进度的卡片 Demo JSON。”  
  响应：沿用 sample-card.json 结构，替换文案和颜色，确保按钮、标签、正文齐全。

- **示例 2：营销落地页 Hero**  
  步骤：创建 1440×900 顶层 Frame → 设置深色背景 → 添加标题、副标题、行动按钮 → 在按钮 Frame 中确保填充与文本颜色对比明显。

## 附注
- 若用户要求使用非 Inter 字体，需要提示对方先在插件控制器中新增 `figma.loadFontAsync`，否则无法导入。
- 若 UI 包含 SVG 图标，可建议将 SVG 字符串嵌入 `type: "SVG"` 节点的 `source` 字段，并注明须确认哈希更新逻辑。

## 快速参考

### 常用节点最小示例

**FRAME (Auto-Layout):**
```json
{
  "type": "FRAME",
  "name": "Container",
  "x": 0, "y": 0,
  "layoutMode": "VERTICAL",
  "primaryAxisAlignItems": "MIN",
  "counterAxisAlignItems": "MIN",
  "paddingLeft": 16, "paddingRight": 16,
  "paddingTop": 16, "paddingBottom": 16,
  "itemSpacing": 12,
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
  "children": []
}
```

**TEXT:**
```json
{
  "type": "TEXT",
  "name": "Label",
  "characters": "Hello World",
  "fontName": {"family": "Inter", "style": "Regular"},
  "fontSize": 16,
  "fills": [{"type": "SOLID", "color": {"r": 0, "g": 0, "b": 0}}]
}
```

**RECTANGLE:**
```json
{
  "type": "RECTANGLE",
  "name": "Box",
  "x": 0, "y": 0,
  "width": 100, "height": 100,
  "fills": [{"type": "SOLID", "color": {"r": 0.5, "g": 0.5, "b": 0.5}}],
  "cornerRadius": 8
}
```

**VECTOR:**
```json
{
  "type": "VECTOR",
  "name": "Icon",
  "width": 24, "height": 24,
  "fills": [{"type": "SOLID", "color": {"r": 0, "g": 0, "b": 0}}],
  "fillGeometry": [{"windingRule": "NONZERO", "data": "M 0 0 L 24 0 L 24 24 L 0 24 Z"}],
  "vectorPaths": [{"windingRule": "NONZERO", "data": "M 0 0 L 24 0 L 24 24 L 0 24 Z"}]
}
```

### 常用效果

**投影:**
```json
{
  "type": "DROP_SHADOW",
  "visible": true,
  "color": {"r": 0, "g": 0, "b": 0, "a": 0.15},
  "offset": {"x": 0, "y": 2},
  "radius": 4,
  "spread": 0,
  "blendMode": "NORMAL"
}
```

**线性渐变:**
```json
{
  "type": "GRADIENT_LINEAR",
  "gradientHandlePositions": [
    {"x": 0, "y": 0.5},
    {"x": 1, "y": 0.5},
    {"x": 0.5, "y": 0.5}
  ],
  "gradientStops": [
    {"position": 0, "color": {"r": 1, "g": 0, "b": 0, "a": 1}},
    {"position": 1, "color": {"r": 0, "g": 0, "b": 1, "a": 1}}
  ]
}
```

### 故障排查快速指南

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 节点不显示 | 缺少 fills | 添加 `fills` 数组 |
| VECTOR 空白 | 缺少 fillGeometry | 同时设置 `fillGeometry` 和 `vectorPaths` |
| 文本不显示 | 字体未加载 | 使用 Inter 字体或预加载其他字体 |
| Auto-layout 失效 | 配置不完整 | 检查 `layoutMode` 和对齐属性 |
| **元素宽度只有 100px** | **`primaryAxisSizingMode: "FIXED"` 但没有 `width` 或 `layoutAlign`** | **添加 `layoutAlign: "STRETCH"` 或显式 `width`** |
| **导入时报错 counterAxisAlignItems** | **使用了无效的 `"STRETCH"` 值** | **改为 `"MIN"` / `"CENTER"` / `"MAX"` / `"BASELINE"`** |
| 子元素堆叠在左上角 | Auto-layout 未启用或配置错误 | 检查 `layoutMode` 和 sizing 模式 |
| 颜色异常 | RGB 超出范围 | 使用 0-1 范围的浮点数 |
| 路径解析失败 | 命令格式错误 | 确保命令后有空格 |

更多详细信息请参考 [faq-best-practices.md](references/faq-best-practices.md)。
