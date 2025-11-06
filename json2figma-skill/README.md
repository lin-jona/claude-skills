# JSON2Figma UI Demo Skill

根据需求生成可供 json2figma 插件导入的 UI Demo JSON。

## 概述

这个 skill 帮助 Claude 生成符合 Figma Plugin API 规范的 JSON 结构，可以直接通过 json2figma 插件导入到 Figma 中，快速搭建界面原型。

## 使用场景

- 快速生成 UI 原型的 JSON 结构
- 批量创建 Figma 设计组件
- 自动化设计系统搭建
- 从数据生成可视化界面

## 文档结构

```
json2figma-skill/
├── SKILL.md                          # 主要技能说明文档
├── LICENSE.txt                       # 许可证
├── README.md                         # 本文件
├── CHANGELOG.md                      # 版本更新日志
├── IMPORTANT-NOTES.md                # 重要注意事项
├── examples/                         # 完整示例目录
│   ├── README.md                    # 示例使用指南
│   ├── login-page.json              # 登录页面示例
│   ├── dashboard-card.json          # 仪表板卡片示例
│   └── mobile-profile.json          # 移动端个人资料示例
└── references/                       # 参考文档目录
    ├── figma-api-schema.md          # Figma API 节点架构参考
    ├── vector-construction.md       # VECTOR 节点构造指南
    ├── complex-types.md             # 复杂类型定义
    ├── faq-best-practices.md        # 常见问题与最佳实践
    ├── generation-checklist.md      # JSON 生成检查清单
    ├── mixins-and-renderers.md      # Mixins 与渲染器速查
    ├── plugin-overview.md           # 插件工作流概览
    ├── examples-index.md            # 示例索引
    ├── test-fixed.json              # 完整示例
    └── test-visible.json            # 简化示例
```

## 核心功能

### 1. 节点类型支持

- **容器节点**: FRAME, GROUP, COMPONENT, INSTANCE
- **形状节点**: RECTANGLE, ELLIPSE, VECTOR, LINE, STAR, POLYGON
- **内容节点**: TEXT
- **特殊节点**: PAGE, DOCUMENT

### 2. 布局系统

- Auto-Layout (水平/垂直布局)
- 绝对定位
- 约束系统 (Constraints)
- 响应式尺寸

### 3. 样式系统

- 纯色填充
- 渐变填充 (线性、径向、角度、菱形)
- 描边样式
- 阴影效果
- 模糊效果

### 4. 文本系统

- 字体配置 (Inter 字体系列)
- 文本对齐
- 字符间距
- 行高设置

## 快速开始

### 完整示例

查看 [examples/](examples/) 目录获取完整的可导入示例：
- **login-page.json** - 完整的登录页面（32个节点）
- **dashboard-card.json** - 数据展示卡片（19个节点）
- **mobile-profile.json** - 移动端个人资料页（34个节点）

详细说明请查看 [examples/README.md](examples/README.md)

### 基础示例

生成一个简单的按钮：

```json
{
  "type": "FRAME",
  "name": "Button",
  "layoutMode": "HORIZONTAL",
  "primaryAxisAlignItems": "CENTER",
  "counterAxisAlignItems": "CENTER",
  "paddingLeft": 24,
  "paddingRight": 24,
  "paddingTop": 12,
  "paddingBottom": 12,
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.2, "g": 0.4, "b": 1}
  }],
  "cornerRadius": 8,
  "children": [
    {
      "type": "TEXT",
      "name": "Label",
      "characters": "Click Me",
      "fontName": {"family": "Inter", "style": "Medium"},
      "fontSize": 16,
      "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}]
    }
  ]
}
```

## 关键注意事项

### ✅ 必须遵守

1. **颜色值范围**: RGB 值必须在 0-1 之间（不是 0-255）
2. **字体可用性**: 默认仅支持 Inter 字体（Regular, Medium, Bold, Semi Bold）
3. **路径格式**: VECTOR 节点路径命令后必须有空格
4. **必需字段**: 所有节点必须包含 `type`, `name`, `id`
5. **Auto-Layout**: 启用时必须设置对齐属性

### ❌ 常见错误

1. 使用 0-255 范围的颜色值
2. GROUP 节点使用 auto-layout 属性
3. VECTOR 节点缺少 `fillGeometry`
4. 文本节点缺少 `fontName` 或 `characters`
5. 路径命令格式错误（如 `"M0 0"` 而非 `"M 0 0"`）

## 文档导航

### 新手入门
1. 阅读 [SKILL.md](SKILL.md) 了解基本工作流程
2. 查看 [examples/](examples/) 学习完整示例
3. 参考 [generation-checklist.md](references/generation-checklist.md) 检查清单

### 深入学习
1. [figma-api-schema.md](references/figma-api-schema.md) - 完整的节点类型参考
2. [complex-types.md](references/complex-types.md) - 复杂类型详解
3. [vector-construction.md](references/vector-construction.md) - 矢量节点专题

### 问题排查
1. [faq-best-practices.md](references/faq-best-practices.md) - 常见问题解答
2. [plugin-overview.md](references/plugin-overview.md) - 插件工作原理
3. [mixins-and-renderers.md](references/mixins-and-renderers.md) - 技术细节

## 支持的 Figma 版本

- Figma Plugin API v1.0+
- 基于 @elemental-figma/object-bridge 库

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT License - 详见 [LICENSE.txt](LICENSE.txt)

## 相关资源

- [Figma Plugin API 官方文档](https://www.figma.com/plugin-docs/)
- [json2figma 插件项目](https://github.com/your-repo/json2figma)
- [Claude Code Skills](https://github.com/anthropics/claude-skills)
