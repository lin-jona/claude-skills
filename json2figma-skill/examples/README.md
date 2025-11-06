# JSON2Figma 示例集合

本目录包含完整的、可直接导入的 Figma JSON 示例，展示各种常见的 UI 模式和最佳实践。

## 📁 示例列表

### 1. login-page.json - 登录页面
**复杂度**: ⭐⭐⭐⭐
**节点数**: 32
**适用场景**: Web 应用登录界面

**包含元素**:
- Logo 和品牌区域（渐变背景）
- 表单输入框（Email、Password）
- 记住我复选框
- 忘记密码链接
- 主要操作按钮（带阴影）
- 分隔线（"or"）
- 第三方登录按钮（Google）
- 注册链接

**学习要点**:
- ✅ 完整的 auto-layout 嵌套结构
- ✅ 表单元素的标准布局
- ✅ 渐变填充的使用
- ✅ 阴影效果的应用
- ✅ 间距和对齐的最佳实践
- ✅ 按钮状态的视觉层次

**尺寸**: 400px 宽，自适应高度

---

### 2. dashboard-card.json - 仪表板卡片
**复杂度**: ⭐⭐⭐⭐⭐
**节点数**: 19
**适用场景**: 数据展示、仪表板、统计面板

**包含元素**:
- 卡片容器（圆角、阴影）
- 图标背景区域
- 标题和副标题
- 大数值显示
- 增长指标（带箭头图标）
- 图表占位区域（渐变背景）
- 查看详情链接（带箭头）
- 分隔线

**学习要点**:
- ✅ 数据可视化布局
- ✅ VECTOR 节点的使用（箭头图标）
- ✅ 描边样式（strokeCap, strokeJoin）
- ✅ 渐变背景的高级应用
- ✅ 视觉层次和信息架构
- ✅ 微交互提示（链接样式）

**尺寸**: 320px 宽，自适应高度

---

### 3. mobile-profile.json - 移动端个人资料页
**复杂度**: ⭐⭐⭐⭐⭐
**节点数**: 34
**适用场景**: 移动应用、用户中心、个人资料

**包含元素**:
- 顶部导航栏（返回、标题、设置）
- 头像（圆形、渐变、阴影）
- 用户信息（姓名、邮箱）
- 统计数据卡片（关注者、关注中、帖子）
- 菜单列表项（图标、标签、箭头）
- 分隔线
- 退出登录按钮

**学习要点**:
- ✅ 移动端标准尺寸（375x812）
- ✅ 安全区域处理（顶部 padding）
- ✅ ELLIPSE 节点的使用
- ✅ 列表项的可复用结构
- ✅ 图标和文本的对齐
- ✅ 视觉反馈设计（按钮颜色）
- ✅ layoutGrow 的灵活使用

**尺寸**: 375x812px（iPhone X/11/12 标准尺寸）

---

## 🎯 使用方法

### 方法 1: 直接导入
1. 复制整个 JSON 文件内容
2. 在 Figma 中打开 json2figma 插件
3. 粘贴 JSON 到插件面板
4. 点击 "Render JSON"

### 方法 2: 作为模板修改
1. 复制示例文件
2. 根据需求修改节点属性：
   - 文本内容（`characters`）
   - 颜色值（`fills`, `strokes`）
   - 尺寸（`width`, `height`, `padding`）
   - 间距（`itemSpacing`）
3. 保持结构完整性
4. 导入到 Figma

### 方法 3: 提取部分组件
1. 找到需要的组件节点
2. 复制该节点及其 children
3. 创建新的 DOCUMENT/PAGE 结构
4. 将组件节点放入其中
5. 导入使用

## 📚 学习路径

### 初学者
推荐顺序：
1. **dashboard-card.json** - 学习基础卡片布局
2. **login-page.json** - 理解表单结构
3. **mobile-profile.json** - 掌握移动端布局

### 进阶学习
重点关注：
1. **Auto-Layout 嵌套** - 观察 login-page 中的多层嵌套
2. **VECTOR 图标** - 研究 dashboard-card 中的箭头和图标
3. **渐变和效果** - 分析各示例中的视觉效果

### 高级技巧
深入研究：
1. **layoutGrow 的使用** - mobile-profile 中的弹性布局
2. **视觉层次** - 通过颜色、大小、间距建立层次
3. **可复用组件** - 提取通用模式创建组件库

## 🔧 自定义指南

### 修改颜色
```json
// 找到 fills 数组
"fills": [{
  "type": "SOLID",
  "color": {
    "r": 0.4,  // 红色通道 (0-1)
    "g": 0.5,  // 绿色通道 (0-1)
    "b": 1     // 蓝色通道 (0-1)
  }
}]
```

### 修改文本
```json
// 找到 TEXT 节点
{
  "type": "TEXT",
  "characters": "你的文本内容",
  "fontName": {"family": "Inter", "style": "Bold"},
  "fontSize": 16
}
```

### 修改尺寸
```json
// 容器尺寸
{
  "type": "FRAME",
  "width": 400,  // 修改宽度
  "height": 300  // 修改高度（如果是 FIXED）
}
```

### 修改间距
```json
// Auto-layout 间距
{
  "layoutMode": "VERTICAL",
  "itemSpacing": 16,        // 子项间距
  "paddingLeft": 24,        // 内边距
  "paddingRight": 24,
  "paddingTop": 24,
  "paddingBottom": 24
}
```

## ⚠️ 常见问题

### Q: 导入后节点位置不对？
A: 检查 `x` 和 `y` 坐标，确保在画布可见范围内（建议从 100, 100 开始）

### Q: 文本不显示？
A: 确保使用了 Inter 字体，或在插件控制器中预加载其他字体

### Q: 颜色看起来不对？
A: 检查 RGB 值是否在 0-1 范围内，不是 0-255

### Q: Auto-layout 不生效？
A: 确保设置了 `layoutMode` 和对齐属性（`primaryAxisAlignItems`, `counterAxisAlignItems`）

### Q: 图标不显示？
A: VECTOR 节点需要同时设置 `fillGeometry` 和 `vectorPaths`，路径命令后要有空格

## 🎨 设计系统建议

基于这些示例，你可以构建自己的设计系统：

### 颜色系统
```json
// 主色
"primary": {"r": 0.4, "g": 0.5, "b": 1}
// 成功色
"success": {"r": 0.13, "g": 0.7, "b": 0.29}
// 错误色
"error": {"r": 0.9, "g": 0.3, "b": 0.3}
// 中性色
"gray-50": {"r": 0.98, "g": 0.98, "b": 0.98}
"gray-100": {"r": 0.95, "g": 0.95, "b": 0.95}
"gray-500": {"r": 0.5, "g": 0.5, "b": 0.5}
```

### 间距系统
```
4px, 8px, 12px, 16px, 20px, 24px, 32px, 48px, 64px
```

### 圆角系统
```
4px (小), 8px (中), 12px (大), 16px (超大)
```

### 阴影系统
```json
// 小阴影
{"offset": {"x": 0, "y": 2}, "radius": 4, "color": {"a": 0.1}}
// 中阴影
{"offset": {"x": 0, "y": 4}, "radius": 8, "color": {"a": 0.1}}
// 大阴影
{"offset": {"x": 0, "y": 8}, "radius": 16, "color": {"a": 0.15}}
```

## 📖 相关文档

- [SKILL.md](../SKILL.md) - 技能使用指南
- [figma-api-schema.md](../references/figma-api-schema.md) - 节点类型参考
- [faq-best-practices.md](../references/faq-best-practices.md) - 最佳实践
- [IMPORTANT-NOTES.md](../IMPORTANT-NOTES.md) - 重要注意事项

## 🤝 贡献示例

如果你创建了有价值的示例，欢迎贡献！

**示例要求**:
- 完整的 DOCUMENT → PAGE → 节点结构
- 清晰的命名（节点 name 属性）
- 合理的布局和间距
- 符合最佳实践
- 包含注释说明（在 README 中）

---

最后更新: 2024-11-03
示例数量: 3
总节点数: 85
