# 重要注意事项和补充说明

本文档列出使用 json2figma-skill 时需要特别注意的关键点和潜在问题。

## 🔴 关键限制和约束

### 1. 字体限制
**问题**: 插件默认只预加载了 Inter 字体的 4 个字重
- ✅ 支持: Inter Regular, Medium, Bold, Semi Bold
- ❌ 不支持: 其他字体需要在插件控制器中手动添加 `figma.loadFontAsync()`

**解决方案**:
```javascript
// 在 controller.tsx 中添加
await figma.loadFontAsync({ family: "Roboto", style: "Regular" });
```

### 2. 颜色值范围
**问题**: Figma API 使用 0-1 范围，而非常见的 0-255
- ❌ 错误: `{"r": 255, "g": 128, "b": 0}`
- ✅ 正确: `{"r": 1, "g": 0.5, "b": 0}`

**转换公式**:
```javascript
const figmaColor = {
  r: rgb255.r / 255,
  g: rgb255.g / 255,
  b: rgb255.b / 255
};
```

### 3. 填充对象属性限制 ⚠️ **重要**
**问题**: 填充对象（fills/backgrounds/strokes）不能包含某些属性
- ❌ 错误: 在填充对象中使用 `visible`, `opacity`, `blendMode`
- ✅ 正确: 这些属性应该在节点级别设置，而非填充对象内

**错误示例**:
```json
{
  "fills": [{
    "type": "SOLID",
    "visible": true,      // ❌ 错误：填充对象不支持
    "opacity": 1,         // ❌ 错误：填充对象不支持
    "blendMode": "NORMAL", // ❌ 错误：填充对象不支持
    "color": {"r": 1, "g": 0, "b": 0}
  }]
}
```

**正确示例**:
```json
{
  "visible": true,      // ✅ 正确：在节点级别
  "opacity": 1,         // ✅ 正确：在节点级别
  "blendMode": "NORMAL", // ✅ 正确：在节点级别
  "fills": [{
    "type": "SOLID",
    "color": {"r": 1, "g": 0, "b": 0}
  }]
}
```

**影响**: 包含这些属性会导致 Figma API 验证失败，节点无法正确渲染

### 4. 渐变格式转换 ⚠️ **重要**
**问题**: Figma 导出使用 `gradientHandlePositions`，但导入需要 `gradientTransform`
- 插件已自动处理此转换
- JSON 中可以使用 `gradientHandlePositions` 格式
- 插件会自动转换为 `gradientTransform` 矩阵

**支持的格式**:
```json
{
  "type": "GRADIENT_LINEAR",
  "gradientHandlePositions": [
    {"x": 0, "y": 0},    // 起点
    {"x": 1, "y": 1},    // 终点
    {"x": 0, "y": 1}     // 宽度控制点
  ],
  "gradientStops": [
    {"position": 0, "color": {"r": 1, "g": 0, "b": 0, "a": 1}},
    {"position": 1, "color": {"r": 0, "g": 0, "b": 1, "a": 1}}
  ]
}
```

### 5. GROUP 节点限制
**问题**: GROUP 不支持 auto-layout 属性
- ❌ 不能使用: `layoutMode`, `layoutAlign`, `layoutGrow`, `padding*`, `itemSpacing`
- ✅ 可以使用: `x`, `y`, `rotation`, `opacity`, `blendMode`

**解决方案**: 需要 auto-layout 时使用 FRAME 代替 GROUP

### 6. VECTOR 节点必需字段
**问题**: VECTOR 节点需要同时设置两个路径属性
- ❌ 只设置 `vectorPaths` - 节点可能不可见
- ✅ 同时设置 `fillGeometry` 和 `vectorPaths`

**原因**:
- `fillGeometry`: 用于实际渲染
- `vectorPaths`: 用于编辑器中的控制柄

### 7. 路径数据格式严格
**问题**: SVG 路径命令格式必须精确
- ❌ 错误: `"M50 0L100 100Z"` (命令后无空格)
- ❌ 错误: `"M50,0 L100,100 Z"` (使用逗号)
- ✅ 正确: `"M 50 0 L 100 100 Z"` (命令后有空格)

## ⚠️ 常见陷阱

### 1. 异步操作问题
某些属性设置是异步的，可能导致时序问题：
- 样式 ID 设置 (`fillStyleId`, `strokeStyleId`)
- 字体加载 (`figma.loadFontAsync`)
- 图片加载 (IMAGE 填充)

**最佳实践**: 始终将样式 ID 设置为空字符串 `""` 或确保引用的样式存在

### 2. 节点 ID 不持久
**问题**: JSON 中的 `id` 在导入后会被 Figma 重新分配

**影响**:
- 不能依赖 ID 进行跨会话引用
- ID 主要用于建立 JSON 内部的父子关系

**解决方案**: 使用 `name` 属性来标识和查找节点

### 3. 尺寸计算问题
**GROUP 节点**: `width` 和 `height` 由子节点自动计算，不应手动设置

**TEXT 节点**:
- 使用 `textAutoResize: "WIDTH_AND_HEIGHT"` 让文本自动调整
- 手动设置尺寸可能导致文本被裁剪

### 4. 渐变配置复杂
**问题**: 渐变需要精确的 3 个控制点
```json
"gradientHandlePositions": [
  {"x": 0, "y": 0.5},    // 起点
  {"x": 1, "y": 0.5},    // 终点
  {"x": 0.5, "y": 0.5}   // 宽度控制点
]
```

**常见错误**:
- 只提供 2 个点
- 点的位置超出 0-1 范围
- `gradientStops` 的 position 不在 0-1 范围

### 5. 效果不显示
**阴影不显示的原因**:
- `visible: false`
- `color.a` (alpha) 为 0
- `radius` 为 0
- 父容器 `clipsContent: true` 裁剪了阴影

## 🎯 性能优化建议

### 1. 节点数量控制
- 避免创建过多嵌套层级（建议不超过 10 层）
- 合并相似的形状节点
- 使用组件实例而非重复创建

### 2. 路径优化
- 简化复杂的矢量路径
- 移除不必要的路径点
- 使用基础形状（RECTANGLE, ELLIPSE）而非 VECTOR

### 3. 样式复用
- 使用样式 ID 引用共享样式
- 避免重复定义相同的填充和效果
- 考虑使用组件和变体系统

### 4. 批量操作
- 一次导入完整的文档结构
- 避免逐个节点导入
- 使用 JSON 数组批量创建相似节点

## 📋 调试检查清单

当导入失败或结果不符合预期时，按以下顺序检查：

### 基础结构
- [ ] JSON 语法是否有效（使用 JSON 验证器）
- [ ] 是否有 DOCUMENT → PAGE → 节点的层级结构
- [ ] 所有节点是否有 `type`, `name`, `id` 字段

### 节点属性
- [ ] 颜色值是否在 0-1 范围内
- [ ] 尺寸值是否大于 0
- [ ] `children` 是否为数组（即使为空）
- [ ] 样式 ID 是否为字符串（`""` 或有效 ID）

### 特定节点类型
- [ ] TEXT: 是否有 `fontName` 和 `characters`
- [ ] VECTOR: 是否同时有 `fillGeometry` 和 `vectorPaths`
- [ ] FRAME: auto-layout 配置是否完整
- [ ] GROUP: 是否避免了 auto-layout 属性

### 视觉效果
- [ ] 节点是否有 `fills`（否则透明）
- [ ] `visible` 是否为 `true`
- [ ] `opacity` 是否大于 0
- [ ] 效果的 `visible` 是否为 `true`

### 路径和字体
- [ ] 路径命令后是否有空格
- [ ] 路径是否以 `Z` 闭合（填充形状）
- [ ] 字体是否在 Figma 中可用
- [ ] 字体样式名称是否正确

## 🔧 高级技巧

### 1. 使用变量绑定
```json
{
  "fills": [{
    "type": "SOLID",
    "color": {"r": 1, "g": 0, "b": 0},
    "boundVariables": {
      "color": {
        "type": "VARIABLE_ALIAS",
        "id": "VariableID:123"
      }
    }
  }]
}
```

### 2. 组件属性定义
```json
{
  "type": "COMPONENT",
  "componentPropertyDefinitions": {
    "variant": {
      "type": "VARIANT",
      "defaultValue": "Default",
      "variantOptions": ["Default", "Hover", "Active"]
    }
  }
}
```

### 3. 约束系统
```json
{
  "constraints": {
    "horizontal": "CENTER",  // 水平居中
    "vertical": "MIN"        // 固定顶部
  }
}
```

### 4. 混合模式
```json
{
  "blendMode": "MULTIPLY",  // 正片叠底
  "opacity": 0.8
}
```

## 📚 进阶学习路径

### 初级（1-2天）
1. 掌握基础节点类型（FRAME, RECTANGLE, TEXT）
2. 理解颜色和尺寸系统
3. 学会使用 auto-layout

### 中级（3-5天）
1. 掌握 VECTOR 节点和路径语法
2. 理解复杂类型（渐变、效果）
3. 学会组件和实例系统

### 高级（1-2周）
1. 掌握约束和响应式设计
2. 理解变量和样式系统
3. 优化性能和可维护性

## 🆘 获取帮助

### 文档优先级
1. **快速问题**: [faq-best-practices.md](references/faq-best-practices.md)
2. **节点参考**: [figma-api-schema.md](references/figma-api-schema.md)
3. **矢量问题**: [vector-construction.md](references/vector-construction.md)
4. **类型定义**: [complex-types.md](references/complex-types.md)

### 调试流程
1. 从最小示例开始
2. 逐步添加属性
3. 每次添加后验证
4. 使用检查清单排查

### 常见错误代码
- **字体加载失败**: 检查 `fontName` 和预加载列表
- **路径解析失败**: 检查路径格式和空格
- **节点不可见**: 检查 `fills`, `visible`, `opacity`
- **布局错误**: 检查 auto-layout 配置完整性

## 🔄 持续更新

本文档会随着插件更新和用户反馈持续改进。如发现新的问题或有改进建议，请提交 issue。

---

最后更新: 2024-11-03
版本: 1.0.0
