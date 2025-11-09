# JSON2Figma 生成准则检查表

## 结构层级
- 文档根节点必须为 `type: "DOCUMENT"`，包含 `children` 数组。
- 每个页面使用 `type: "PAGE"`，不可直接将 Frame 掛在 Document 下。
- 所有节点需包含唯一 `id` 与 `name`，避免后续引用混乱。

## 布局与尺寸
- 容器节点（`FRAME`、`COMPONENT`、`GROUP`）建议显式设置 `x`/`y`/`width`/`height`，或搭配 `layoutMode`、`primaryAxisSizingMode` 等自动布局字段。
- 自动布局启用后同步提供 `padding*`、`itemSpacing`，保持 Figma 渲染一致。
- 不需要约束时可省略 `constraints`，若需固定定位请设置 `"horizontal": "CENTER"` 等具体值。

### ⚠️ Auto-Layout 关键规则（必须遵守）
1. **`counterAxisAlignItems` 只能使用 `"MIN" | "CENTER" | "MAX" | "BASELINE"`**
   - ❌ 错误：`"counterAxisAlignItems": "STRETCH"`
   - ✅ 正确：`"counterAxisAlignItems": "MIN"` + 子元素使用 `"layoutAlign": "STRETCH"`

2. **`primaryAxisSizingMode: "FIXED"` 必须配合以下之一**：
   - 显式的 `width` 属性（或 `height`）
   - `layoutAlign: "STRETCH"` 属性
   - 或改用 `primaryAxisSizingMode: "AUTO"`
   - ⚠️ 否则会导致默认宽度 100px 的布局错误！

3. **常见需要 `layoutAlign: "STRETCH"` 的元素**：
   - Header / Footer 容器
   - 表单字段容器
   - 全宽按钮
   - 分隔线（Divider）
   - 菜单项

## 颜色与视觉
- 所有填充、描边使用 0-1 浮点 RGB：`{ "r": 0.12, "g": 0.34, "b": 0.56 }`。
- 背景色或按钮色必须通过 `fills` 声明；未设置将继承透明背景。
- 投影、模糊等效果写入 `effects` 数组，结构同 Figma API (`type`, `opacity`, `radius`, `offset`)。

## 文本节点注意事项
- 必填：`characters`, `fontName`, `fontSize`, `fills`。
- 字体仅预加载 Inter Regular/Medium/Bold/Semi Bold；若采用其它字重，需在控制器中同步添加 `loadFontAsync`。
- 文案可能含标点，推荐使用双引号括起并转义必要字符。

## 构建流程建议
1. 生成 Document → Page → 根 Frame，确保基本结构合法。
2. 按组件拆分：标题、正文、按钮等分别建 Frame 或 Text 节点，渐进叠加。
3. 每新增节点时补齐关键属性（类型、尺寸、填充、字体），保持 JSON 自描述。
4. 输出前使用 JSON 校验工具（VSCode/`jq`）验证格式。
5. **⚠️ 执行 Auto-Layout 验证**（关键步骤）：
   ```bash
   # 检查无效的 counterAxisAlignItems
   grep '"counterAxisAlignItems": "STRETCH"' your-file.json

   # 检查可能有问题的 primaryAxisSizingMode: "FIXED"
   grep -B5 -A5 '"primaryAxisSizingMode": "FIXED"' your-file.json
   ```
6. 在 Figma 开发模式中粘贴并导入，检查图层结构与视觉效果。

## 常见问题排查

遇到问题时，请参考以下文档获取详细解决方案：

- **文本不显示** → [faq-best-practices.md#4-文本节点字体显示不正确](faq-best-practices.md)
- **自动布局失效** → [faq-best-practices.md#6-auto-layout-不生效](faq-best-practices.md)
- **元素宽度只有 100px** → [faq-best-practices.md#61-元素宽度只有-100px](faq-best-practices.md)
- **VECTOR 节点空白** → [faq-best-practices.md#2-vector-节点显示为空白](faq-best-practices.md)
- **颜色异常** → [faq-best-practices.md#2-颜色值规范](faq-best-practices.md)
- **路径解析失败** → [faq-best-practices.md#21-vector-路径解析失败](faq-best-practices.md)

完整的最佳实践和调试技巧请参考 [faq-best-practices.md](faq-best-practices.md)。
