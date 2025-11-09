# Changelog

All notable changes to the json2figma-skill will be documented in this file.

## [1.0.0] - 2024-11-03

### Added
- 初始版本发布
- 完整的 Figma API 节点架构参考文档
- VECTOR 节点详细构造指南
- 复杂类型定义参考（Paint, Effect, Constraints 等）
- 常见问题与最佳实践文档
- 快速参考和故障排查指南
- 示例 JSON 文件（test-fixed.json, test-visible.json）
- 完整的文档索引系统

### Documentation Structure
- `SKILL.md` - 主要技能说明和工作流程
- `README.md` - 项目概述和快速开始
- `references/figma-api-schema.md` - 节点类型完整参考
- `references/vector-construction.md` - 矢量路径构造指南
- `references/complex-types.md` - 复杂类型定义
- `references/faq-best-practices.md` - FAQ 和最佳实践
- `references/generation-checklist.md` - 生成检查清单
- `references/mixins-and-renderers.md` - Mixins 技术参考
- `references/plugin-overview.md` - 插件工作流程
- `references/examples-index.md` - 示例索引

### Features
- 支持所有主要 Figma 节点类型
- Auto-Layout 完整支持
- 矢量路径和 SVG 支持
- 渐变和效果系统
- 文本样式系统
- 响应式约束系统

### Notes
- 基于 Figma Plugin API v1.0+
- 使用 @elemental-figma/object-bridge 库
- 默认支持 Inter 字体系列

## [1.1.0] - 2025-11-05

### Added - Validation and Conversion Tools

#### 新增验证脚本 (validate_json.py)
- ✅ 自动检测无效的 `counterAxisAlignItems: "STRETCH"` 值
- ✅ 检测缺少 `layoutAlign` 的 `primaryAxisSizingMode: "FIXED"` 元素
- ✅ 检测不支持的 SVG 路径命令（Arc、相对命令、H/V/S/T 等）
- ✅ 提供详细的错误位置和修复建议
- ✅ 支持批量验证多个文件

#### 新增 SVG 路径转换脚本 (convert_svg_paths.py)
- ✅ 自动将 Arc 命令 (A) 转换为 Cubic Bezier 曲线 (C)
- ✅ 转换相对命令为绝对命令（m→M, l→L, c→C 等）
- ✅ 转换 H/V 命令为 L 命令
- ✅ 转换 S/T 命令为 C/Q 命令
- ✅ 支持单个路径字符串转换
- ✅ 支持整个 JSON 文件批量转换
- ✅ 完整的椭圆弧到贝塞尔曲线转换算法

#### 新增脚本文档
- 📄 `scripts/README.md` - 详细的脚本使用指南
- 📄 包含常见问题和解决方案
- 📄 推荐的验证工作流程

### Enhanced - Documentation

#### 更新 FAQ 文档 (faq-best-practices.md)
- 📝 新增 "VECTOR 路径解析失败 - Arc 命令错误" 章节
  - 详细说明 Figma 支持和不支持的 SVG 命令
  - 提供手动和自动转换方法
  - 包含圆形路径转换示例
- 📝 新增 "元素宽度只有 100px" 问题章节
  - 解释 `primaryAxisSizingMode: "FIXED"` 的默认行为
  - 提供三种解决方案（layoutAlign、显式宽度、AUTO 模式）
  - 列出常见需要 layoutAlign 的元素类型
- 📝 新增 "counterAxisAlignItems 验证错误" 章节
  - 说明有效值和无效值
  - 对比 CSS Flexbox 的差异
  - 提供正确的配置示例

#### 更新主技能文档 (SKILL.md)
- 📝 工作流程第 6 步增加验证脚本推荐
- 📝 新增 "验证和转换工具" 章节
  - 介绍两个脚本的功能和用法
  - 提供推荐的验证工作流程
  - 链接到详细文档
- 📝 附注中强调运行验证脚本的重要性

### Fixed - Based on Testing Logs

#### 修复 1: Vector Arc 命令问题 (LOG_2025-11-05_figma-vector-arc-command-fix.md)
- 🐛 修复 mobile-profile.json 中 Settings Icon 的 Arc 命令
- 🔧 将 `A 10 10 0 1 1` 转换为四段 Cubic Bezier 曲线
- 📚 在文档中明确说明 Figma API 限制
- 🔗 添加官方文档链接

#### 修复 2: Auto-Layout 宽度问题 (LOG_2025-11-05_json2figma-layout-width-fix.md)
- 🐛 修复 Content 框架宽度超出 Mobile Screen 边界
- 🐛 修复 Menu Items 容器宽度不符合预期
- 🔧 添加 `layoutAlign: "STRETCH"` 到需要填充父容器的元素
- 📚 在文档中说明 layoutAlign 的作用和使用场景

#### 修复 3: Auto-Layout 配置错误 (LOG_2025-11-04_json2figma-autolayout-bug-fix.md)
- 🐛 修复所有示例文件中的 `counterAxisAlignItems: "STRETCH"` 错误
- 🔧 批量替换为有效值 `"MIN"`
- 🔧 添加缺失的 `layoutAlign: "STRETCH"` 到 23 个元素：
  - login-page.json: 7 个元素
  - login-page-fixed-height.json: 7 个元素
  - dashboard-card.json: 3 个元素
  - mobile-profile.json: 6 个元素
- 📚 更新文档明确说明 Auto-Layout 规则

### Improved - Example Files

#### 更新示例文件
- ✅ `examples/mobile-profile.json` - 修复 Settings Icon 路径和布局
- ✅ `examples/login-page.json` - 修复 Auto-Layout 配置
- ✅ `examples/login-page-fixed-height.json` - 修复 Auto-Layout 配置
- ✅ `examples/dashboard-card.json` - 修复 Auto-Layout 配置
- ✅ 所有示例文件现在都能正确导入 Figma

### Technical Improvements

#### 代码质量
- 🔧 Python 脚本使用标准库，无外部依赖
- 🔧 完整的错误处理和用户友好的输出
- 🔧 支持命令行参数和批量处理
- 🔧 详细的注释和文档字符串

#### 测试覆盖
- ✅ 基于实际测试日志验证所有修复
- ✅ 所有示例文件通过验证脚本检查
- ✅ 路径转换算法经过数学验证

### Breaking Changes
- 无破坏性变更
- 所有现有 JSON 文件保持向后兼容

### Migration Guide
如果你有使用旧版本生成的 JSON 文件：

1. 运行验证脚本检查问题：
   ```bash
   python scripts/validate_json.py your-old-file.json
   ```

2. 修复 counterAxisAlignItems 错误：
   ```bash
   sed -i 's/"counterAxisAlignItems": "STRETCH"/"counterAxisAlignItems": "MIN"/g' your-old-file.json
   ```

3. 转换 Arc 命令（如果有）：
   ```bash
   python scripts/convert_svg_paths.py --file your-old-file.json --output your-fixed-file.json
   ```

4. 手动添加缺失的 `layoutAlign: "STRETCH"` 属性

### Known Issues
- 路径转换脚本生成的浮点数精度较高，可能导致 JSON 文件较大
- 验证脚本的父容器上下文检测是简化版本，可能产生误报

### Future Plans
- 添加更多验证规则（字体检查、颜色范围检查等）
- 支持 JSON Schema 验证
- 开发可视化预览工具
- 集成到 CI/CD 流程

## [Unreleased]

### Planned
- 更多实际项目示例
- 组件库模板
- 设计系统生成器
- 交互式示例生成工具
- 更多字体支持指南
- 图片处理指南
- 组件变体系统文档
- JSON Schema 定义文件
- 自动化测试套件

---

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
