# Figma Plugin API Node Schema

本文档整理了Figma Plugin API中主要节点类型的属性schema，用于json-to-figma插件导入时的JSON构造参考。

## 节点类型概览

### 基础节点类型
- **DocumentNode** - 文档根节点,包含所有页面
- **PageNode** - 页面节点,包含场景节点
- **SceneNode** - 场景节点基类,所有可见节点的基础

### 容器节点
- **FrameNode** - 支持auto-layout的容器,可调整大小
- **GroupNode** - 基本分组,不支持auto-layout
- **ComponentNode** - 可重用组件
- **ComponentSetNode** - 组件变体集合
- **InstanceNode** - 组件实例

### 形状节点
- **RectangleNode** - 矩形形状
- **EllipseNode** - 椭圆/圆形
- **PolygonNode** - 多边形
- **StarNode** - 星形
- **VectorNode** - 自定义矢量路径
- **LineNode** - 直线

### 其他节点
- **TextNode** - 文本内容
- **SliceNode** - 导出切片区域
- **BooleanOperationNode** - 布尔操作结果

## 共享属性 (Shared Properties)

所有节点都支持的通用属性（按类别分组）：

### 基础标识属性
- `id: string` [readonly] - 节点的唯一标识符
- `name: string` - 节点显示名称
- `type: NodeType` [readonly] - 节点类型字符串
- `parent: (BaseNode & ChildrenMixin) | null` [readonly] - 父节点引用

### 可见性和交互
- `visible: boolean` - 是否可见 (默认: true)
- `locked: boolean` - 是否锁定编辑 (默认: false)
- `opacity: number` - 不透明度 (0-1)
- `blendMode: BlendMode` - 混合模式

### 几何和变换
- `x: number` - X坐标位置
- `y: number` - Y坐标位置
- `width: number` - 节点宽度
- `height: number` - 节点高度
- `rotation: number` - 旋转角度（度）

### 样式和效果
- `effects: Effect[]` - 效果数组
- `effectStyleId: string` - 效果样式ID

## FrameNode Schema

FrameNode是最常用的容器类型,支持auto-layout布局。

### 最小可用示例

```json
{
  "id": "1:1",
  "type": "FRAME",
  "name": "My Frame",
  "visible": true,
  "locked": false,
  "opacity": 1,
  "blendMode": "NORMAL",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 150,
  "rotation": 0,
  "layoutMode": "NONE",
  "fills": [],
  "strokes": [],
  "effects": [],
  "children": []
}
```

### Auto-Layout Frame 示例

```json
{
  "id": "1:2",
  "type": "FRAME",
  "name": "Auto Layout Frame",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "x": 0,
  "y": 0,
  "width": 300,
  "height": 200,
  "rotation": 0,
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
  "layoutWrap": "NO_WRAP",
  "clipsContent": true,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 1, "g": 1, "b": 1 }
  }],
  "strokes": [],
  "strokeWeight": 1,
  "strokeAlign": "INSIDE",
  "cornerRadius": 8,
  "effects": [],
  "children": []
}
```

### 特有属性

**填充和背景：**
- `fills: Paint[]` - 填充
- `fillStyleId: string` - 填充样式ID

**描边：**
- `strokes: Paint[]` - 描边
- `strokeStyleId: string` - 描边样式ID
- `strokeWeight: number` - 描边宽度
- `strokeAlign: "INSIDE" | "OUTSIDE" | "CENTER"` - 描边对齐
- `strokeJoin: "MITER" | "BEVEL" | "ROUND"` - 描边连接
- `strokeCap: "NONE" | "ROUND" | "SQUARE"` - 描边端点

**圆角：**
- `cornerRadius: number` - 统一圆角半径
- `cornerSmoothing: number` - 圆角平滑度
- `topLeftRadius: number` - 左上圆角
- `topRightRadius: number` - 右上圆角
- `bottomLeftRadius: number` - 左下圆角
- `bottomRightRadius: number` - 右下圆角

**Auto-Layout属性：**
- `layoutMode: "NONE" | "HORIZONTAL" | "VERTICAL"` - 布局方向
- `primaryAxisAlignItems: "MIN" | "CENTER" | "MAX" | "SPACE_BETWEEN"` - 主轴对齐
- `counterAxisAlignItems: "MIN" | "CENTER" | "MAX" | "BASELINE"` - 副轴对齐（⚠️ 注意：没有 "STRETCH" 值）
- `primaryAxisSizingMode: "AUTO" | "FIXED"` - 主轴尺寸模式
- `counterAxisSizingMode: "AUTO" | "FIXED"` - 副轴尺寸模式
- `paddingLeft: number` - 左内边距
- `paddingRight: number` - 右内边距
- `paddingTop: number` - 上内边距
- `paddingBottom: number` - 下内边距
- `itemSpacing: number` - 子项间距
- `layoutWrap: "NO_WRAP" | "WRAP"` - 是否换行
- `clipsContent: boolean` - 是否裁剪超出内容

### ⚠️ Auto-Layout 关键规则（必读）

#### 规则 1: counterAxisAlignItems 没有 "STRETCH" 值

如果想让子元素在副轴方向填充满容器（类似 CSS 的 `align-items: stretch`），应该：
1. 在**容器**上设置 `counterAxisAlignItems: "MIN"` (或其他有效值)
2. 在**子元素**上设置 `layoutAlign: "STRETCH"`

❌ **错误示例**：
```json
{
  "layoutMode": "VERTICAL",
  "counterAxisAlignItems": "STRETCH"  // ❌ 错误：STRETCH 不是有效值
}
```

✅ **正确示例**：
```json
{
  "layoutMode": "VERTICAL",
  "counterAxisAlignItems": "MIN",  // ✅ 正确：容器使用 MIN
  "children": [{
    "layoutAlign": "STRETCH"  // ✅ 正确：子元素使用 STRETCH
  }]
}
```

#### 规则 2: primaryAxisSizingMode: "FIXED" 必须配合 width 或 layoutAlign

**关键规则**：当子元素使用 `primaryAxisSizingMode: "FIXED"` 但没有显式指定 `width`（或 `height`）时，**必须**添加 `layoutAlign: "STRETCH"` 来填充父容器。

否则，Figma 会使用默认宽度 **100px**，导致布局错误。

❌ **错误示例**（会导致宽度只有 100px）：
```json
{
  "type": "FRAME",
  "name": "Header",
  "layoutMode": "HORIZONTAL",
  "primaryAxisSizingMode": "FIXED",  // ❌ FIXED 但没有 width
  "counterAxisSizingMode": "AUTO"
  // ❌ 缺少 layoutAlign: "STRETCH"
  // 结果：宽度只有 100px！
}
```

✅ **正确示例 1**（使用 layoutAlign）：
```json
{
  "type": "FRAME",
  "name": "Header",
  "layoutMode": "HORIZONTAL",
  "primaryAxisSizingMode": "FIXED",
  "counterAxisSizingMode": "AUTO",
  "layoutAlign": "STRETCH",  // ✅ 填充父容器宽度
  "children": [...]
}
```

✅ **正确示例 2**（使用显式 width）：
```json
{
  "type": "FRAME",
  "name": "Header",
  "layoutMode": "HORIZONTAL",
  "primaryAxisSizingMode": "FIXED",
  "counterAxisSizingMode": "AUTO",
  "width": 375,  // ✅ 显式指定宽度
  "children": [...]
}
```

✅ **正确示例 3**（使用 AUTO）：
```json
{
  "type": "FRAME",
  "name": "Header",
  "layoutMode": "HORIZONTAL",
  "primaryAxisSizingMode": "AUTO",  // ✅ AUTO 会自动适应内容
  "counterAxisSizingMode": "AUTO",
  "children": [...]
}
```

**适用范围**：
- 所有使用 auto-layout 的容器（FRAME、COMPONENT、COMPONENTSET）
- RECTANGLE、ELLIPSE 等形状节点作为 auto-layout 子元素时

**常见场景**：
- 移动端 UI 的全宽元素（Header、Footer、Button）
- 表单字段容器
- 卡片内的分隔线（Divider）
- 菜单项

#### 规则 3: 生成 JSON 后必须验证

**强烈建议**：在生成 JSON 后，使用以下检查清单验证配置：

**自动化检查脚本**（推荐）：
```bash
# 检查是否有无效的 counterAxisAlignItems: "STRETCH"
grep -n '"counterAxisAlignItems": "STRETCH"' your-file.json

# 检查可能有问题的 primaryAxisSizingMode: "FIXED"
# （需要人工确认是否有 width 或 layoutAlign）
grep -B5 -A5 '"primaryAxisSizingMode": "FIXED"' your-file.json
```

**手动检查清单**：
- [ ] 所有 `counterAxisAlignItems` 的值都是 `"MIN" | "CENTER" | "MAX" | "BASELINE"`
- [ ] 所有使用 `primaryAxisSizingMode: "FIXED"` 的元素都有以下之一：
  - 显式的 `width` 属性
  - `layoutAlign: "STRETCH"` 属性
  - 或者改用 `primaryAxisSizingMode: "AUTO"`
- [ ] 所有需要填充父容器的子元素都有 `layoutAlign: "STRETCH"`
- [ ] 分隔线（Divider）等装饰性元素有 `layoutAlign: "STRETCH"`

**验证工具**（未来计划）：
- 创建 JSON schema 验证器
- 集成到插件中，导入前自动检查
- 提供友好的错误提示和修复建议

## GroupNode Schema

GroupNode用于将多个节点组合在一起,不支持auto-layout。

### 最小可用示例

```json
{
  "id": "2:1",
  "type": "GROUP",
  "name": "My Group",
  "visible": true,
  "locked": false,
  "opacity": 1,
  "blendMode": "NORMAL",
  "x": 0,
  "y": 0,
  "rotation": 0,
  "effects": [],
  "children": [
    {
      "id": "2:2",
      "type": "RECTANGLE",
      "name": "Rectangle 1",
      "x": 0,
      "y": 0,
      "width": 100,
      "height": 100,
      "fills": [{"type": "SOLID", "color": {"r": 1, "g": 0, "b": 0}}]
    }
  ]
}
```

**注意**：GROUP 的 `width` 和 `height` 由子节点自动计算,不应在 JSON 中直接设置。

### 不支持的属性
- `layoutPositioning` - GROUP不支持auto-layout定位
- `layoutAlign` - 不适用
- `constrainProportions` - 不适用
- `layoutGrow` - 不适用
- 所有auto-layout相关的填充和间距属性

## RectangleNode Schema

RectangleNode创建矩形形状。

### 最小可用示例

```json
{
  "id": "3:1",
  "type": "RECTANGLE",
  "name": "Rectangle",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "x": 0,
  "y": 0,
  "width": 100,
  "height": 100,
  "rotation": 0,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 0.5, "g": 0.5, "b": 0.5 }
  }],
  "strokes": [],
  "strokeWeight": 1,
  "strokeAlign": "INSIDE",
  "cornerRadius": 0,
  "effects": []
}
```

### 圆角矩形示例

```json
{
  "id": "3:2",
  "type": "RECTANGLE",
  "name": "Rounded Rectangle",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "x": 0,
  "y": 0,
  "width": 120,
  "height": 80,
  "rotation": 0,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 0.2, "g": 0.6, "b": 1 }
  }],
  "strokes": [{
    "type": "SOLID",
    "color": { "r": 0, "g": 0, "b": 0 }
  }],
  "strokeWeight": 2,
  "strokeAlign": "INSIDE",
  "cornerRadius": 12,
  "cornerSmoothing": 0.6,
  "effects": [{
    "type": "DROP_SHADOW",
    "visible": true,
    "color": { "r": 0, "g": 0, "b": 0, "a": 0.25 },
    "offset": { "x": 0, "y": 4 },
    "radius": 8,
    "spread": 0,
    "blendMode": "NORMAL"
  }]
}
```

## TextNode Schema

TextNode处理文本内容。

### 最小可用示例

```json
{
  "id": "5:1",
  "type": "TEXT",
  "name": "Text",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 40,
  "rotation": 0,
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
  }],
  "strokes": [],
  "effects": []
}
```

### 特有属性

**文本内容：**
- `characters: string` - 文本内容

**字体属性：**
- `fontName: FontName` - 字体名称和样式
- `fontSize: number` - 字体大小
- `textCase: "ORIGINAL" | "UPPER" | "LOWER" | "TITLE"` - 文本大小写
- `textDecoration: "NONE" | "UNDERLINE" | "STRIKETHROUGH"` - 文本装饰
- `letterSpacing: LetterSpacing` - 字符间距
- `lineHeight: LineHeight` - 行高

**文本对齐：**
- `textAlignHorizontal: "LEFT" | "CENTER" | "RIGHT" | "JUSTIFIED"` - 水平对齐
- `textAlignVertical: "TOP" | "CENTER" | "BOTTOM"` - 垂直对齐
- `textAutoResize: "NONE" | "WIDTH_AND_HEIGHT" | "HEIGHT"` - 自动调整大小

**段落属性：**
- `paragraphIndent: number` - 段落缩进
- `paragraphSpacing: number` - 段落间距

## VectorNode Schema

VectorNode用于自定义矢量形状。详细的矢量路径构造请参考 `vector-construction.md`。

### 特有属性

**矢量路径：**
- `vectorPaths: VectorPath[]` - 矢量路径数据
- `fillGeometry: Path[]` - 填充几何路径
- `strokeGeometry: Path[]` - 描边几何路径

**其他：**
- `handleMirroring: HandleMirroring` - 控制柄镜像
- `windingRule: "NONZERO" | "EVENODD"` - 缠绕规则

## 属性默认值参考

以下是常用属性的默认值,构造JSON时可以省略这些属性或使用默认值：

### 基础属性默认值
- `visible: true` - 节点默认可见
- `locked: false` - 节点默认未锁定
- `opacity: 1` - 完全不透明
- `blendMode: "NORMAL"` - 正常混合模式
- `rotation: 0` - 无旋转
- `effects: []` - 无效果

### 填充和描边默认值
- `fills: []` - 无填充（透明）
- `strokes: []` - 无描边
- `strokeWeight: 1` - 描边宽度1像素
- `strokeAlign: "INSIDE"` - 描边内对齐
- `fillStyleId: ""` - 无填充样式引用
- `strokeStyleId: ""` - 无描边样式引用

### Auto-Layout 默认值
- `layoutMode: "NONE"` - 无自动布局
- `primaryAxisAlignItems: "MIN"` - 主轴起始对齐
- `counterAxisAlignItems: "MIN"` - 副轴起始对齐
- `paddingLeft: 0` - 无左内边距
- `paddingRight: 0` - 无右内边距
- `paddingTop: 0` - 无上内边距
- `paddingBottom: 0` - 无下内边距
- `itemSpacing: 0` - 子项间距为0

### 文本默认值
- `textAlignHorizontal: "LEFT"` - 左对齐
- `textAlignVertical: "TOP"` - 顶部对齐
- `textAutoResize: "WIDTH_AND_HEIGHT"` - 自动调整宽高
- `textCase: "ORIGINAL"` - 保持原始大小写
- `textDecoration: "NONE"` - 无文本装饰

## 注意事项

1. **属性兼容性**：不同节点类型支持不同属性集,构造JSON时需根据节点类型选择相应属性。GROUP节点不支持auto-layout属性。

2. **必填属性**：`id`、`name`、`type` 是所有节点的基本必填属性。

3. **样式ID**：`fillStyleId`、`strokeStyleId` 等用于引用共享样式。如果不使用共享样式,应设置为空字符串 `""`。

4. **约束**：`constraints` 定义节点在不同屏幕尺寸下的行为。

5. **混合模式**：`blendMode` 影响节点如何与其下层内容混合。

6. **效果**：`effects` 数组包含阴影、模糊等视觉效果。

此schema基于Figma Plugin API v1.0+,涵盖主要节点类型和属性。实际使用时请参考最新官方文档。
