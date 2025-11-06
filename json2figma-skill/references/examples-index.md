# JSON 示例索引

本文档提供了 json2figma 插件可用的 JSON 示例文件索引和说明。

## 可用示例文件

### test-fixed.json
完整的 Figma 文档结构示例，包含所有必需的内部字段。

**包含内容：**
- DOCUMENT 根节点
- PAGE 节点配置
- FRAME 容器示例
- 完整的元数据字段（isAsset, detachedInfo, relativeTransform 等）

**适用场景：**
- 需要导入完整文档结构时
- 参考 Figma 内部字段格式
- 调试导入问题时的对照

### test-visible.json
简化的可见性测试示例。

**包含内容：**
- 基础节点结构
- 可见性控制示例

**适用场景：**
- 测试节点可见性
- 快速验证基础结构

## 使用建议

### 从示例开始
1. 复制相关示例文件
2. 根据需求修改节点属性
3. 保持必需字段完整
4. 逐步添加自定义内容

### 最小化示例
如果不需要完整的 Figma 内部字段，可以使用简化版本：

```json
{
  "id": "0:0",
  "type": "DOCUMENT",
  "name": "My Design",
  "documentColorProfile": "SRGB",
  "children": [
    {
      "id": "0:1",
      "type": "PAGE",
      "name": "Page 1",
      "children": [
        {
          "id": "1:1",
          "type": "FRAME",
          "name": "Container",
          "x": 0,
          "y": 0,
          "width": 320,
          "height": 240,
          "layoutMode": "VERTICAL",
          "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
          "children": []
        }
      ]
    }
  ]
}
```

## 常见组合模式

### 卡片列表
```json
{
  "type": "FRAME",
  "name": "Card List",
  "layoutMode": "VERTICAL",
  "itemSpacing": 16,
  "children": [
    // 多个卡片节点
  ]
}
```

### 导航栏
```json
{
  "type": "FRAME",
  "name": "Navigation",
  "layoutMode": "HORIZONTAL",
  "primaryAxisAlignItems": "SPACE_BETWEEN",
  "counterAxisAlignItems": "CENTER",
  "children": [
    // Logo, 菜单项, 按钮
  ]
}
```

### 表单布局
```json
{
  "type": "FRAME",
  "name": "Form",
  "layoutMode": "VERTICAL",
  "itemSpacing": 24,
  "children": [
    // 标题, 输入框, 按钮
  ]
}
```

## 参考文档

- [figma-api-schema.md](figma-api-schema.md) - 完整节点类型参考
- [faq-best-practices.md](faq-best-practices.md) - 最佳实践和常见模式
- [complex-types.md](complex-types.md) - 复杂类型定义

## 注意事项

1. **ID 字段**：导入后 Figma 会重新分配 ID，JSON 中的 ID 主要用于建立引用关系
2. **必需字段**：确保包含 `type`, `name`, `id` 等基础字段
3. **颜色格式**：始终使用 0-1 范围的浮点数
4. **字体可用性**：确保使用的字体在 Figma 中可用或已预加载
5. **路径格式**：VECTOR 节点的路径命令后必须有空格
