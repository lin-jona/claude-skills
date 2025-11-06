# Figma 复杂类型定义

本文档详细说明了 Figma Plugin API 中使用的复杂类型结构,用于 json-to-figma 插件的 JSON 构造。

## Paint 类型

Paint 定义了填充和描边的样式。

### SOLID - 纯色填充

```json
{
  "type": "SOLID",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "color": {
    "r": 1,
    "g": 0.5,
    "b": 0
  },
  "boundVariables": {}
}
```

**属性说明：**
- `type`: `"SOLID"` - 纯色类型
- `visible`: `boolean` - 是否可见（默认 true）
- `opacity`: `number` - 不透明度 0-1（默认 1）
- `blendMode`: `BlendMode` - 混合模式（默认 "NORMAL"）
- `color`: `RGB` - RGB 颜色对象
  - `r`: `number` - 红色通道 0-1
  - `g`: `number` - 绿色通道 0-1
  - `b`: `number` - 蓝色通道 0-1
- `boundVariables`: `object` - 绑定的变量（可选）

### GRADIENT_LINEAR - 线性渐变

```json
{
  "type": "GRADIENT_LINEAR",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "gradientHandlePositions": [
    { "x": 0, "y": 0.5 },
    { "x": 1, "y": 0.5 },
    { "x": 0.5, "y": 0.5 }
  ],
  "gradientStops": [
    {
      "position": 0,
      "color": { "r": 1, "g": 0, "b": 0, "a": 1 }
    },
    {
      "position": 1,
      "color": { "r": 0, "g": 0, "b": 1, "a": 1 }
    }
  ]
}
```

**属性说明：**
- `type`: `"GRADIENT_LINEAR"` - 线性渐变类型
- `gradientHandlePositions`: `Vector[]` - 渐变控制点位置（3个点）
  - 第1个点：渐变起点
  - 第2个点：渐变终点
  - 第3个点：渐变宽度控制点
- `gradientStops`: `ColorStop[]` - 渐变色标数组
  - `position`: `number` - 色标位置 0-1
  - `color`: `RGBA` - RGBA 颜色（包含 alpha 通道）

### GRADIENT_RADIAL - 径向渐变

```json
{
  "type": "GRADIENT_RADIAL",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "gradientHandlePositions": [
    { "x": 0.5, "y": 0.5 },
    { "x": 1, "y": 0.5 },
    { "x": 0.5, "y": 0 }
  ],
  "gradientStops": [
    {
      "position": 0,
      "color": { "r": 1, "g": 1, "b": 1, "a": 1 }
    },
    {
      "position": 1,
      "color": { "r": 0, "g": 0, "b": 0, "a": 0 }
    }
  ]
}
```

### GRADIENT_ANGULAR - 角度渐变

```json
{
  "type": "GRADIENT_ANGULAR",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "gradientHandlePositions": [
    { "x": 0.5, "y": 0.5 },
    { "x": 1, "y": 0.5 },
    { "x": 0.5, "y": 0 }
  ],
  "gradientStops": [
    {
      "position": 0,
      "color": { "r": 1, "g": 0, "b": 0, "a": 1 }
    },
    {
      "position": 0.5,
      "color": { "r": 0, "g": 1, "b": 0, "a": 1 }
    },
    {
      "position": 1,
      "color": { "r": 0, "g": 0, "b": 1, "a": 1 }
    }
  ]
}
```

### IMAGE - 图片填充

```json
{
  "type": "IMAGE",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "scaleMode": "FILL",
  "imageHash": "abc123...",
  "imageTransform": [
    [1, 0, 0],
    [0, 1, 0]
  ],
  "scalingFactor": 1,
  "rotation": 0,
  "filters": {
    "exposure": 0,
    "contrast": 0,
    "saturation": 0,
    "temperature": 0,
    "tint": 0,
    "highlights": 0,
    "shadows": 0
  }
}
```

**属性说明：**
- `scaleMode`: `"FILL" | "FIT" | "CROP" | "TILE"` - 缩放模式
- `imageHash`: `string` - 图片哈希值（需要先上传图片）
- `imageTransform`: `Transform` - 图片变换矩阵
- `scalingFactor`: `number` - 缩放因子
- `rotation`: `number` - 旋转角度（弧度）
- `filters`: `ImageFilters` - 图片滤镜

## Effect 类型

Effect 定义了阴影、模糊等视觉效果。

### DROP_SHADOW - 投影

```json
{
  "type": "DROP_SHADOW",
  "visible": true,
  "color": {
    "r": 0,
    "g": 0,
    "b": 0,
    "a": 0.25
  },
  "offset": {
    "x": 0,
    "y": 4
  },
  "radius": 8,
  "spread": 0,
  "blendMode": "NORMAL",
  "showShadowBehindNode": false
}
```

**属性说明：**
- `type`: `"DROP_SHADOW"` - 投影类型
- `visible`: `boolean` - 是否可见
- `color`: `RGBA` - 阴影颜色（包含透明度）
- `offset`: `Vector` - 阴影偏移
  - `x`: `number` - X轴偏移
  - `y`: `number` - Y轴偏移
- `radius`: `number` - 模糊半径
- `spread`: `number` - 扩展距离
- `blendMode`: `BlendMode` - 混合模式
- `showShadowBehindNode`: `boolean` - 是否在节点后显示阴影

### INNER_SHADOW - 内阴影

```json
{
  "type": "INNER_SHADOW",
  "visible": true,
  "color": {
    "r": 0,
    "g": 0,
    "b": 0,
    "a": 0.5
  },
  "offset": {
    "x": 0,
    "y": 2
  },
  "radius": 4,
  "spread": 0,
  "blendMode": "NORMAL"
}
```

### LAYER_BLUR - 图层模糊

```json
{
  "type": "LAYER_BLUR",
  "visible": true,
  "radius": 10
}
```

**属性说明：**
- `type`: `"LAYER_BLUR"` - 图层模糊类型
- `visible`: `boolean` - 是否可见
- `radius`: `number` - 模糊半径

### BACKGROUND_BLUR - 背景模糊

```json
{
  "type": "BACKGROUND_BLUR",
  "visible": true,
  "radius": 20
}
```

## Constraints 类型

Constraints 定义了节点的响应式约束行为。

```json
{
  "horizontal": "MIN",
  "vertical": "MIN"
}
```

**属性说明：**
- `horizontal`: `"MIN" | "CENTER" | "MAX" | "STRETCH" | "SCALE"` - 水平约束
  - `MIN`: 固定左边距
  - `CENTER`: 居中
  - `MAX`: 固定右边距
  - `STRETCH`: 拉伸（固定左右边距）
  - `SCALE`: 按比例缩放
- `vertical`: `"MIN" | "CENTER" | "MAX" | "STRETCH" | "SCALE"` - 垂直约束
  - `MIN`: 固定顶部边距
  - `CENTER`: 居中
  - `MAX`: 固定底部边距
  - `STRETCH`: 拉伸（固定上下边距）
  - `SCALE`: 按比例缩放

### 常见约束组合示例

```json
// 固定左上角
{ "horizontal": "MIN", "vertical": "MIN" }

// 居中
{ "horizontal": "CENTER", "vertical": "CENTER" }

// 固定右下角
{ "horizontal": "MAX", "vertical": "MAX" }

// 水平拉伸,固定顶部
{ "horizontal": "STRETCH", "vertical": "MIN" }

// 按比例缩放
{ "horizontal": "SCALE", "vertical": "SCALE" }
```

## FontName 类型

FontName 定义了字体名称和样式。

```json
{
  "family": "Inter",
  "style": "Regular"
}
```

**常见字体样式：**
- `"Regular"` - 常规
- `"Bold"` - 粗体
- `"Italic"` - 斜体
- `"Bold Italic"` - 粗斜体
- `"Light"` - 细体
- `"Medium"` - 中等
- `"SemiBold"` - 半粗体
- `"Black"` - 特粗体

### 字体示例

```json
// Inter Regular
{ "family": "Inter", "style": "Regular" }

// Inter Bold
{ "family": "Inter", "style": "Bold" }

// Roboto Medium
{ "family": "Roboto", "style": "Medium" }

// Arial
{ "family": "Arial", "style": "Regular" }
```

**注意**：字体必须在 Figma 中可用,否则会回退到默认字体。

## LetterSpacing 类型

LetterSpacing 定义了字符间距。

```json
{
  "unit": "PERCENT",
  "value": 0
}
```

**单位类型：**
- `"PERCENT"`: 百分比（相对于字体大小）
- `"PIXELS"`: 像素

### 字符间距示例

```json
// 无字符间距
{ "unit": "PERCENT", "value": 0 }

// 2% 字符间距
{ "unit": "PERCENT", "value": 2 }

// 5% 字符间距（较宽）
{ "unit": "PERCENT", "value": 5 }

// -2% 字符间距（紧凑）
{ "unit": "PERCENT", "value": -2 }

// 2 像素字符间距
{ "unit": "PIXELS", "value": 2 }
```

## LineHeight 类型

LineHeight 定义了行高。

```json
{
  "unit": "AUTO"
}
```

**单位类型：**
- `"AUTO"`: 自动行高
- `"PIXELS"`: 像素
- `"PERCENT"`: 百分比（相对于字体大小）

### 行高示例

```json
// 自动行高
{ "unit": "AUTO" }

// 24 像素行高
{ "unit": "PIXELS", "value": 24 }

// 150% 行高
{ "unit": "PERCENT", "value": 150 }

// 120% 行高（紧凑）
{ "unit": "PERCENT", "value": 120 }
```

## BlendMode 类型

BlendMode 定义了混合模式。

**可用值：**
- `"NORMAL"` - 正常（默认）
- `"DARKEN"` - 变暗
- `"MULTIPLY"` - 正片叠底
- `"COLOR_BURN"` - 颜色加深
- `"LIGHTEN"` - 变亮
- `"SCREEN"` - 滤色
- `"COLOR_DODGE"` - 颜色减淡
- `"OVERLAY"` - 叠加
- `"SOFT_LIGHT"` - 柔光
- `"HARD_LIGHT"` - 强光
- `"DIFFERENCE"` - 差值
- `"EXCLUSION"` - 排除
- `"HUE"` - 色相
- `"SATURATION"` - 饱和度
- `"COLOR"` - 颜色
- `"LUMINOSITY"` - 明度

### 混合模式示例

```json
// 正常混合
"blendMode": "NORMAL"

// 正片叠底（常用于阴影）
"blendMode": "MULTIPLY"

// 滤色（常用于高光）
"blendMode": "SCREEN"

// 叠加（常用于纹理）
"blendMode": "OVERLAY"
```

## VectorPath 类型

VectorPath 定义了矢量路径。

```json
{
  "windingRule": "NONZERO",
  "data": "M 0 0 L 100 0 L 100 100 L 0 100 Z"
}
```

**属性说明：**
- `windingRule`: `"NONZERO" | "EVENODD"` - 缠绕规则
- `data`: `string` - SVG 路径数据

详细的路径语法请参考 `vector-construction.md` 文档。

## 完整节点示例

### 带所有复杂类型的完整示例

```json
{
  "id": "1:1",
  "type": "RECTANGLE",
  "name": "Complex Rectangle",
  "visible": true,
  "locked": false,
  "opacity": 0.9,
  "blendMode": "MULTIPLY",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 150,
  "rotation": 15,
  "fills": [
    {
      "type": "GRADIENT_LINEAR",
      "visible": true,
      "opacity": 1,
      "blendMode": "NORMAL",
      "gradientHandlePositions": [
        { "x": 0, "y": 0 },
        { "x": 1, "y": 1 },
        { "x": 0, "y": 1 }
      ],
      "gradientStops": [
        {
          "position": 0,
          "color": { "r": 1, "g": 0.5, "b": 0, "a": 1 }
        },
        {
          "position": 1,
          "color": { "r": 1, "g": 0, "b": 0.5, "a": 1 }
        }
      ]
    }
  ],
  "strokes": [
    {
      "type": "SOLID",
      "visible": true,
      "opacity": 1,
      "blendMode": "NORMAL",
      "color": { "r": 0, "g": 0, "b": 0 }
    }
  ],
  "strokeWeight": 3,
  "strokeAlign": "OUTSIDE",
  "strokeCap": "ROUND",
  "strokeJoin": "ROUND",
  "cornerRadius": 16,
  "cornerSmoothing": 0.6,
  "effects": [
    {
      "type": "DROP_SHADOW",
      "visible": true,
      "color": { "r": 0, "g": 0, "b": 0, "a": 0.3 },
      "offset": { "x": 0, "y": 8 },
      "radius": 16,
      "spread": 0,
      "blendMode": "NORMAL"
    },
    {
      "type": "INNER_SHADOW",
      "visible": true,
      "color": { "r": 1, "g": 1, "b": 1, "a": 0.5 },
      "offset": { "x": 0, "y": 1 },
      "radius": 2,
      "spread": 0,
      "blendMode": "NORMAL"
    }
  ],
  "constraints": {
    "horizontal": "CENTER",
    "vertical": "CENTER"
  }
}
```

## 类型速查表

| 类型 | 用途 | 主要属性 |
|------|------|----------|
| `Paint` | 填充/描边 | `type`, `color`, `gradientStops` |
| `Effect` | 视觉效果 | `type`, `radius`, `offset`, `color` |
| `Constraints` | 响应式约束 | `horizontal`, `vertical` |
| `FontName` | 字体 | `family`, `style` |
| `LetterSpacing` | 字符间距 | `unit`, `value` |
| `LineHeight` | 行高 | `unit`, `value` |
| `BlendMode` | 混合模式 | 字符串枚举 |
| `VectorPath` | 矢量路径 | `windingRule`, `data` |

此文档涵盖了 json-to-figma 插件中最常用的复杂类型。更多详细信息请参考 Figma Plugin API 官方文档。
