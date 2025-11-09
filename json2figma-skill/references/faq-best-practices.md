# JSON to Figma - 常见问题与最佳实践

本文档提供了使用 json-to-figma 插件时的常见问题解答和最佳实践指南。

## 常见问题 (FAQ)

### 1. 为什么我的节点没有显示出来？

**可能原因：**

- **缺少填充**：节点可能是透明的。确保设置了 `fills` 数组：
  ```json
  "fills": [{
    "type": "SOLID",
    "color": { "r": 1, "g": 0, "b": 0 }
  }]
  ```

- **尺寸为零**：检查 `width` 和 `height` 是否大于 0

- **不可见**：确保 `visible: true`

- **在画布外**：检查 `x` 和 `y` 坐标是否在可见范围内

- **透明度为零**：确保 `opacity` 大于 0

### 2. VECTOR 节点显示为空白

**解决方案：**

- 确保设置了 `fillGeometry` 属性（不仅仅是 `vectorPaths`）
- 检查路径数据格式是否正确（命令后需要空格）
- 确保路径坐标在节点的 `width` 和 `height` 范围内
- 添加填充颜色：
  ```json
  "fills": [{
    "type": "SOLID",
    "color": { "r": 1, "g": 0, "b": 0 }
  }]
  ```

### 2.1 VECTOR 路径解析失败 - Arc 命令错误

**错误信息：**
```
Failed to set vector properties: in set_vectorPaths: Failed to convert path. Invalid command at A
```

**原因：**

Figma 的 vectorPaths API 不支持 SVG 的弧形命令 (Arc command `A`)。Figma 仅支持以下命令：
- `M x y` - 绝对"移动到"命令
- `L x y` - 绝对"画线到"命令
- `Q x0 y0 x y` - 绝对"二次贝塞尔曲线"命令
- `C x0 y0 x1 y1 x y` - 绝对"三次贝塞尔曲线"命令
- `Z` - "闭合路径"命令

**不支持的命令：**
- ❌ `A` (arc) - 弧形命令
- ❌ `S`, `T` - 平滑曲线简写命令
- ❌ `H`, `V` - 水平/垂直线命令
- ❌ 小写命令（相对坐标）- 如 `m`, `l`, `c`, `q` 等

**解决方案：**

使用提供的转换脚本自动转换路径：

```bash
# 转换单个路径
python scripts/convert_svg_paths.py "M 12 2 A 10 10 0 1 1 12 22 Z"

# 转换整个 JSON 文件
python scripts/convert_svg_paths.py --file examples/your-file.json --output examples/your-file-fixed.json
```

**手动转换示例：**

对于圆形，可以使用四段三次贝塞尔曲线来近似：

```json
// 原始路径（使用 Arc 命令）
"data": "M 12 2 A 10 10 0 1 1 12 22 A 10 10 0 1 1 12 2 Z"

// 转换后（使用 Cubic Bezier）
"data": "M 12 2 C 17.523 2 22 6.477 22 12 C 22 17.523 17.523 22 12 22 C 6.477 22 2 17.523 2 12 C 2 6.477 6.477 2 12 2 Z"
```

**参考资源：**
- [vector-construction.md](vector-construction.md) - 详细的路径构造指南
- [Figma VectorPath API 文档](https://developers.figma.com/docs/plugins/api/properties/VectorPath-data/)

### 3. GROUP 节点在 auto-layout 中位置不对

**原因：**

GROUP 节点不支持 auto-layout 属性,在 auto-layout 容器中会被视为绝对定位。

**解决方案：**

- 使用 FRAME 代替 GROUP
- 或者使用绝对定位（`x`、`y`）手动设置位置
- 移除 GROUP 上的 `layoutPositioning`、`layoutAlign` 等属性

### 4. 文本节点字体显示不正确

**可能原因：**

- **字体不可用**：Figma 中没有安装指定的字体
- **字体样式错误**：字体样式名称不匹配（如 "Bold" vs "700"）

**解决方案：**

- 使用 Figma 中可用的字体（如 "Inter", "Roboto"）
- 检查字体样式名称是否正确
- 使用标准样式名称：`"Regular"`, `"Bold"`, `"Italic"` 等

### 5. 样式 ID 设置后没有效果

**原因：**

样式 ID 必须引用 Figma 文件中已存在的样式。

**解决方案：**

- 如果不使用共享样式,将样式 ID 设置为空字符串 `""`
- 确保引用的样式 ID 在当前文件中存在
- 直接使用 `fills`、`strokes`、`effects` 数组而不是样式 ID

### 6. Auto-layout 不生效

**检查清单：**

- `layoutMode` 是否设置为 `"HORIZONTAL"` 或 `"VERTICAL"`
- 是否设置了 `primaryAxisAlignItems` 和 `counterAxisAlignItems`
- 子节点是否正确设置了 `layoutAlign` 和 `layoutGrow`
- 确保节点类型支持 auto-layout（FRAME、COMPONENT、INSTANCE）

### 6.1 元素宽度只有 100px（Auto-Layout 宽度问题）

**现象：**

导入后，某些元素（如 Header、Footer、Button、Divider）的宽度只有 100px，而不是填充父容器的宽度。

**原因：**

当元素使用 `primaryAxisSizingMode: "FIXED"` 但没有显式指定 `width` 属性，且缺少 `layoutAlign: "STRETCH"` 时，Figma 会使用默认宽度 100px。

**解决方案：**

有三种方法可以解决：

1. **添加 layoutAlign: "STRETCH"**（推荐）：
   ```json
   {
     "type": "FRAME",
     "name": "Header",
     "layoutMode": "HORIZONTAL",
     "primaryAxisSizingMode": "FIXED",
     "layoutAlign": "STRETCH"  // ← 添加此行
   }
   ```

2. **显式指定宽度**：
   ```json
   {
     "type": "FRAME",
     "name": "Header",
     "layoutMode": "HORIZONTAL",
     "primaryAxisSizingMode": "FIXED",
     "width": 375  // ← 添加此行
   }
   ```

3. **改用 AUTO 模式**：
   ```json
   {
     "type": "FRAME",
     "name": "Header",
     "layoutMode": "HORIZONTAL",
     "primaryAxisSizingMode": "AUTO"  // ← 改为 AUTO
   }
   ```

**常见需要 layoutAlign: "STRETCH" 的元素：**
- Header / Footer 容器
- 表单字段容器
- 按钮（需要填充父容器宽度时）
- 分隔线（Divider / RECTANGLE）
- 菜单项

**验证脚本：**

使用提供的验证脚本检查：

```bash
python scripts/validate_json.py examples/your-file.json
```

### 6.2 counterAxisAlignItems 验证错误

**错误信息：**
```
Property "counterAxisAlignItems" failed validation:
Invalid enum value. Expected 'MIN' | 'MAX' | 'CENTER' | 'BASELINE', received 'STRETCH'
```

**原因：**

`counterAxisAlignItems` 不支持 `"STRETCH"` 值。这是一个常见的误解，因为 CSS Flexbox 的 `align-items` 支持 `stretch`。

**有效值：**
- `"MIN"` - 对齐到起始位置（左/上）
- `"MAX"` - 对齐到结束位置（右/下）
- `"CENTER"` - 居中对齐
- `"BASELINE"` - 基线对齐（主要用于文本）

**解决方案：**

如果想让子元素在副轴方向填充满容器，应该：

1. 在**容器**上设置 `counterAxisAlignItems: "MIN"` (或其他有效值)
2. 在**子元素**上设置 `layoutAlign: "STRETCH"`

**错误示例：**
```json
{
  "layoutMode": "VERTICAL",
  "counterAxisAlignItems": "STRETCH"  // ❌ 错误
}
```

**正确示例：**
```json
{
  "layoutMode": "VERTICAL",
  "counterAxisAlignItems": "MIN",  // ✅ 正确：容器使用 MIN
  "children": [{
    "layoutAlign": "STRETCH"  // ✅ 正确：子元素使用 STRETCH
  }]
}
```

### 7. 圆角不显示

**可能原因：**

- 节点类型不支持圆角（如 ELLIPSE、TEXT）
- `cornerRadius` 值为 0
- 节点尺寸太小,圆角被裁剪

**解决方案：**

- 确保节点类型支持圆角（RECTANGLE、FRAME）
- 设置合适的 `cornerRadius` 值
- 检查 `width` 和 `height` 是否足够大

### 8. 渐变填充显示不正确

**常见错误：**

- `gradientHandlePositions` 数组不是 3 个点
- `gradientStops` 位置不在 0-1 范围内
- 颜色缺少 alpha 通道

**正确示例：**

```json
{
  "type": "GRADIENT_LINEAR",
  "gradientHandlePositions": [
    { "x": 0, "y": 0.5 },
    { "x": 1, "y": 0.5 },
    { "x": 0.5, "y": 0.5 }
  ],
  "gradientStops": [
    { "position": 0, "color": { "r": 1, "g": 0, "b": 0, "a": 1 } },
    { "position": 1, "color": { "r": 0, "g": 0, "b": 1, "a": 1 } }
  ]
}
```

### 9. 阴影效果不显示

**检查清单：**

- `effects` 数组中的效果 `visible` 是否为 `true`
- 阴影颜色的 alpha 通道是否大于 0
- `radius` 是否大于 0
- 节点是否有足够的空间显示阴影（检查父容器的 `clipsContent`）

### 10. JSON 导入后节点 ID 改变了

**说明：**

这是正常行为。Figma 会为新创建的节点分配新的 ID。JSON 中的 `id` 主要用于建立父子关系和引用关系。

**最佳实践：**

- 使用 `name` 属性来标识节点
- 不要依赖 JSON 中的 `id` 值在导入后保持不变

## 最佳实践

### 1. JSON 结构组织

**推荐结构：**

```json
{
  "type": "PAGE",
  "name": "My Page",
  "children": [
    {
      "type": "FRAME",
      "name": "Container",
      "layoutMode": "VERTICAL",
      "children": [
        // 子节点...
      ]
    }
  ]
}
```

**建议：**

- 使用有意义的 `name` 属性
- 保持合理的嵌套层级（不超过 10 层）
- 将相关节点组织在 FRAME 或 GROUP 中

### 2. 颜色值规范

**推荐：**

```json
// RGB 值使用 0-1 范围
"color": { "r": 1, "g": 0.5, "b": 0 }

// RGBA 包含 alpha 通道
"color": { "r": 1, "g": 0.5, "b": 0, "a": 0.8 }
```

**避免：**

```json
// 错误：使用 0-255 范围
"color": { "r": 255, "g": 128, "b": 0 }
```

**转换公式：**

```javascript
// 从 0-255 转换到 0-1
const r = 255 / 255; // 1
const g = 128 / 255; // 0.5019607843137255
const b = 0 / 255;   // 0
```

### 3. 尺寸和位置

**推荐：**

- 使用整数值以避免亚像素渲染问题
- 使用 8 的倍数（8px 网格系统）
- 为响应式设计设置合适的 `constraints`

```json
{
  "x": 0,
  "y": 0,
  "width": 320,
  "height": 240,
  "constraints": {
    "horizontal": "CENTER",
    "vertical": "CENTER"
  }
}
```

### 4. Auto-Layout 最佳实践

**推荐配置：**

```json
{
  "type": "FRAME",
  "layoutMode": "VERTICAL",
  "primaryAxisAlignItems": "MIN",
  "counterAxisAlignItems": "MIN",
  "primaryAxisSizingMode": "AUTO",
  "counterAxisSizingMode": "FIXED",
  "paddingLeft": 16,
  "paddingRight": 16,
  "paddingTop": 16,
  "paddingBottom": 16,
  "itemSpacing": 12,
  "layoutWrap": "NO_WRAP"
}
```

**子节点配置：**

```json
{
  "type": "RECTANGLE",
  "layoutAlign": "STRETCH",
  "layoutGrow": 0,
  "layoutPositioning": "AUTO"
}
```

**建议：**

- 使用 `"AUTO"` 尺寸模式让内容决定大小
- 使用 `"STRETCH"` 让子节点填充可用空间
- 合理设置 `itemSpacing` 和 padding
- 避免在 auto-layout 中使用绝对定位（除非必要）

### 5. 文本节点最佳实践

**推荐配置：**

```json
{
  "type": "TEXT",
  "characters": "Hello World",
  "fontName": {
    "family": "Inter",
    "style": "Regular"
  },
  "fontSize": 16,
  "textAlignHorizontal": "LEFT",
  "textAlignVertical": "TOP",
  "textAutoResize": "WIDTH_AND_HEIGHT",
  "letterSpacing": { "unit": "PERCENT", "value": 0 },
  "lineHeight": { "unit": "AUTO" },
  "fills": [{
    "type": "SOLID",
    "color": { "r": 0, "g": 0, "b": 0 }
  }]
}
```

**建议：**

- 使用 `textAutoResize: "WIDTH_AND_HEIGHT"` 让文本自动调整大小
- 使用 `lineHeight: { "unit": "AUTO" }` 获得最佳行高
- 选择 Figma 中常见的字体（Inter、Roboto、Arial）
- 为多语言支持选择支持 Unicode 的字体

### 6. 矢量路径最佳实践

**推荐：**

```json
{
  "type": "VECTOR",
  "fillGeometry": [{
    "windingRule": "NONZERO",
    "data": "M 0 0 L 100 0 L 100 100 L 0 100 Z"
  }],
  "vectorPaths": [{
    "windingRule": "NONZERO",
    "data": "M 0 0 L 100 0 L 100 100 L 0 100 Z"
  }]
}
```

**建议：**

- 同时设置 `fillGeometry` 和 `vectorPaths`
- 路径命令后使用空格：`"M 0 0"` 而不是 `"M0 0"`
- 使用 `Z` 闭合填充路径
- 保持路径坐标在节点尺寸范围内
- 简化复杂路径以提高性能

### 7. 效果使用建议

**推荐的阴影配置：**

```json
{
  "effects": [
    {
      "type": "DROP_SHADOW",
      "visible": true,
      "color": { "r": 0, "g": 0, "b": 0, "a": 0.15 },
      "offset": { "x": 0, "y": 2 },
      "radius": 4,
      "spread": 0,
      "blendMode": "NORMAL"
    }
  ]
}
```

**建议：**

- 使用较低的 alpha 值（0.1-0.3）获得自然阴影
- 阴影偏移通常为正值（向下和向右）
- 模糊半径通常是偏移的 2-4 倍
- 避免过度使用效果（影响性能）
- 按从外到内的顺序排列多个阴影

### 8. 性能优化

**建议：**

- **减少节点数量**：合并相似的形状
- **简化路径**：移除不必要的路径点
- **优化图片**：使用适当的分辨率和压缩
- **避免过度嵌套**：保持层级结构扁平
- **复用样式**：使用样式 ID 而不是重复定义
- **批量操作**：一次导入多个节点而不是逐个导入

### 9. 可维护性建议

**命名规范：**

```json
{
  "name": "Button/Primary/Default",
  "type": "FRAME"
}
```

**建议：**

- 使用描述性名称
- 采用一致的命名约定（如 BEM、组件/变体/状态）
- 为复杂节点添加描述性前缀
- 使用分隔符组织层级（如 `/` 或 `-`）

### 10. 调试技巧

**逐步验证：**

1. 先创建最简单的节点（如纯色矩形）
2. 逐步添加属性（填充、描边、效果）
3. 验证每个属性是否生效
4. 添加子节点和布局

**使用最小示例：**

```json
{
  "type": "RECTANGLE",
  "name": "Test",
  "x": 0,
  "y": 0,
  "width": 100,
  "height": 100,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 1, "g": 0, "b": 0 }
  }]
}
```

**检查清单：**

- [ ] 节点类型正确
- [ ] 必填属性都已设置
- [ ] 颜色值在 0-1 范围内
- [ ] 尺寸大于 0
- [ ] 路径数据格式正确
- [ ] 样式 ID 为空字符串或有效 ID
- [ ] 子节点正确嵌套

## 常见模式

### 1. 卡片组件

```json
{
  "type": "FRAME",
  "name": "Card",
  "layoutMode": "VERTICAL",
  "primaryAxisAlignItems": "MIN",
  "counterAxisAlignItems": "MIN",
  "primaryAxisSizingMode": "AUTO",
  "counterAxisSizingMode": "FIXED",
  "width": 320,
  "paddingLeft": 16,
  "paddingRight": 16,
  "paddingTop": 16,
  "paddingBottom": 16,
  "itemSpacing": 12,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 1, "g": 1, "b": 1 }
  }],
  "cornerRadius": 12,
  "effects": [{
    "type": "DROP_SHADOW",
    "visible": true,
    "color": { "r": 0, "g": 0, "b": 0, "a": 0.1 },
    "offset": { "x": 0, "y": 4 },
    "radius": 8,
    "spread": 0,
    "blendMode": "NORMAL"
  }],
  "children": [
    {
      "type": "TEXT",
      "name": "Title",
      "characters": "Card Title",
      "fontName": { "family": "Inter", "style": "Bold" },
      "fontSize": 20
    },
    {
      "type": "TEXT",
      "name": "Description",
      "characters": "Card description text",
      "fontName": { "family": "Inter", "style": "Regular" },
      "fontSize": 14
    }
  ]
}
```

### 2. 按钮组件

```json
{
  "type": "FRAME",
  "name": "Button",
  "layoutMode": "HORIZONTAL",
  "primaryAxisAlignItems": "CENTER",
  "counterAxisAlignItems": "CENTER",
  "primaryAxisSizingMode": "AUTO",
  "counterAxisSizingMode": "AUTO",
  "paddingLeft": 24,
  "paddingRight": 24,
  "paddingTop": 12,
  "paddingBottom": 12,
  "itemSpacing": 8,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 0.2, "g": 0.4, "b": 1 }
  }],
  "cornerRadius": 8,
  "children": [
    {
      "type": "TEXT",
      "name": "Label",
      "characters": "Click Me",
      "fontName": { "family": "Inter", "style": "Medium" },
      "fontSize": 16,
      "fills": [{
        "type": "SOLID",
        "color": { "r": 1, "g": 1, "b": 1 }
      }]
    }
  ]
}
```

### 3. 图标

```json
{
  "type": "VECTOR",
  "name": "Icon/Check",
  "width": 24,
  "height": 24,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 0, "g": 0.8, "b": 0 }
  }],
  "fillGeometry": [{
    "windingRule": "NONZERO",
    "data": "M 9 16.17 L 4.83 12 L 3.41 13.41 L 9 19 L 21 7 L 19.59 5.59 Z"
  }],
  "vectorPaths": [{
    "windingRule": "NONZERO",
    "data": "M 9 16.17 L 4.83 12 L 3.41 13.41 L 9 19 L 21 7 L 19.59 5.59 Z"
  }]
}
```

## 相关文档

- `figma-api-schema.md` - 完整的节点类型和属性参考
- `vector-construction.md` - 矢量节点构造指南
- `complex-types.md` - 复杂类型详细定义
- [Figma Plugin API 官方文档](https://www.figma.com/plugin-docs/)

## 总结

遵循这些最佳实践可以帮助你：

- ✅ 避免常见错误
- ✅ 创建高质量的 Figma 节点
- ✅ 提高 JSON 的可维护性
- ✅ 优化性能
- ✅ 加快开发速度

记住：从简单开始,逐步添加复杂性,始终验证每一步的结果。
