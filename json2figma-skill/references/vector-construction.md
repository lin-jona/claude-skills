# VECTOR 节点 JSON 构造指南

为了确保通过 json-to-figma 插件将 JSON 导入 Figma 时,VECTOR 节点能够正确渲染,请遵循以下 JSON 结构构造指南。

## 坐标系统说明

### 相对坐标 vs 绝对坐标

- **相对坐标**：节点的 `x`、`y` 属性是相对于其父容器的坐标
- **绝对坐标**：`absoluteBoundingBox` 是相对于画布原点的绝对位置（只读属性）
- **VECTOR 路径坐标**：`vectorPaths` 和 `fillGeometry` 中的路径坐标是相对于 VECTOR 节点自身的本地坐标系,原点 (0,0) 位于节点的左上角

### 坐标系示例

```json
{
  "type": "FRAME",
  "x": 100,
  "y": 100,
  "children": [
    {
      "type": "RECTANGLE",
      "x": 20,  // 相对于父 FRAME,实际画布位置为 120
      "y": 30   // 相对于父 FRAME,实际画布位置为 130
    }
  ]
}
```

## 路径数据格式

- **SVG 路径语法**：`vectorPaths.data` 和 `fillGeometry.data` 必须是有效的 SVG 路径字符串。
- **间距**：在每个命令字母后使用空格：`"M 50 0 L 100 100 L 0 100 Z"`
  - 正确：`"M 50 0 L 100 100 L 0 100 Z"`
  - 错误：`"M50 0L100 100L0 100Z"`（命令后无空格）
  - 错误：`"M50,0 L100,100 L0,100 Z"`（使用逗号而非空格）
- **坐标**：相对于 VECTOR 节点的本地坐标系,其中 (0,0) 为节点的左上角。
- **闭合路径**：对于填充形状,确保路径以 `Z` 闭合。

## 必需属性

- **`fillGeometry`**：定义填充形状的路径对象数组。这是渲染视觉形状的关键。
- **`vectorPaths`**：用于 Figma UI 中编辑手柄的路径对象数组。可选,但建议用于可编辑性。
- **`width` 和 `height`**：VECTOR 节点边界框的尺寸。
- **`fills`**：填充对象数组（纯色、渐变等）以使形状可见。

## 样式 ID

- **`fillStyleId`**：设置为 `""`（空字符串）,除非引用共享填充样式。
- **`strokeStyleId`**：设置为 `""`，除非引用共享描边样式。
- **`effectStyleId`**：设置为 `""`，除非引用共享效果样式。

## 缠绕规则

- **`windingRule`**：大多数形状使用 `"NONZERO"`，复杂重叠路径使用 `"EVENODD"`。
  - **NONZERO**：非零规则,路径方向决定填充区域,适用于大多数简单形状
  - **EVENODD**：奇偶规则,交叉次数决定填充,适用于镂空效果和复杂重叠路径

### 缠绕规则示例

```json
// NONZERO - 实心圆环
{
  "windingRule": "NONZERO",
  "data": "M 50 10 A 40 40 0 1 1 50 90 A 40 40 0 1 1 50 10 Z M 50 30 A 20 20 0 1 0 50 70 A 20 20 0 1 0 50 30 Z"
}

// EVENODD - 镂空圆环
{
  "windingRule": "EVENODD",
  "data": "M 50 10 A 40 40 0 1 1 50 90 A 40 40 0 1 1 50 10 Z M 50 30 A 20 20 0 1 1 50 70 A 20 20 0 1 1 50 30 Z"
}
```

## 完整示例

```json
{
  "id": "1:1",
  "type": "VECTOR",
  "name": "Red Triangle",
  "visible": true,
  "opacity": 1,
  "blendMode": "NORMAL",
  "isMask": false,
  "effects": [],
  "effectStyleId": "",
  "x": 100,
  "y": 100,
  "width": 100,
  "height": 100,
  "rotation": 0,
  "layoutAlign": "INHERIT",
  "constrainProportions": false,
  "layoutGrow": 0,
  "layoutPositioning": "AUTO",
  "exportSettings": [],
  "fills": [
    {
      "type": "SOLID",
      "visible": true,
      "opacity": 1,
      "blendMode": "NORMAL",
      "color": {
        "r": 1,
        "g": 0,
        "b": 0
      },
      "boundVariables": {}
    }
  ],
  "fillStyleId": "",
  "strokes": [],
  "strokeStyleId": "",
  "strokeWeight": 1,
  "strokeAlign": "INSIDE",
  "strokeJoin": "MITER",
  "strokeCap": "NONE",
  "strokeMiterLimit": 4,
  "fillGeometry": [
    {
      "windingRule": "NONZERO",
      "data": "M 50 0 L 100 100 L 0 100 Z"
    }
  ],
  "strokeGeometry": [],
  "vectorPaths": [
    {
      "windingRule": "NONZERO",
      "data": "M 50 0 L 100 100 L 0 100 Z"
    }
  ],
  "handleMirroring": "NONE",
  "constraints": {
    "horizontal": "MIN",
    "vertical": "MIN"
  }
}
```

此 JSON 将在位置 (100,100) 创建一个尺寸为 100x100 的红色三角形 VECTOR 节点。插件将正确渲染它,并具有可编辑的矢量路径。

## 复杂路径示例

### 贝塞尔曲线路径

```json
{
  "type": "VECTOR",
  "name": "Curved Path",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 100,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 0.2, "g": 0.6, "b": 1 }
  }],
  "fillStyleId": "",
  "fillGeometry": [{
    "windingRule": "NONZERO",
    "data": "M 0 50 C 50 0 150 0 200 50 C 150 100 50 100 0 50 Z"
  }],
  "vectorPaths": [{
    "windingRule": "NONZERO",
    "data": "M 0 50 C 50 0 150 0 200 50 C 150 100 50 100 0 50 Z"
  }]
}
```

**路径命令说明：**
- `M x y` - 移动到点 (x, y)
- `L x y` - 直线到点 (x, y)
- `C x1 y1 x2 y2 x y` - 三次贝塞尔曲线,控制点 (x1,y1) 和 (x2,y2),终点 (x,y)
- `Q x1 y1 x y` - 二次贝塞尔曲线,控制点 (x1,y1),终点 (x,y)
- `A rx ry rotation large-arc sweep x y` - 椭圆弧
- `Z` - 闭合路径

### 多路径组合（镂空效果）

```json
{
  "type": "VECTOR",
  "name": "Donut Shape",
  "x": 0,
  "y": 0,
  "width": 100,
  "height": 100,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 1, "g": 0.5, "b": 0 }
  }],
  "fillStyleId": "",
  "fillGeometry": [{
    "windingRule": "EVENODD",
    "data": "M 50 0 A 50 50 0 1 1 50 100 A 50 50 0 1 1 50 0 Z M 50 25 A 25 25 0 1 0 50 75 A 25 25 0 1 0 50 25 Z"
  }],
  "vectorPaths": [{
    "windingRule": "EVENODD",
    "data": "M 50 0 A 50 50 0 1 1 50 100 A 50 50 0 1 1 50 0 Z M 50 25 A 25 25 0 1 0 50 75 A 25 25 0 1 0 50 25 Z"
  }]
}
```

### 带描边的矢量

```json
{
  "type": "VECTOR",
  "name": "Stroked Star",
  "x": 0,
  "y": 0,
  "width": 100,
  "height": 100,
  "fills": [{
    "type": "SOLID",
    "color": { "r": 1, "g": 1, "b": 0 }
  }],
  "fillStyleId": "",
  "strokes": [{
    "type": "SOLID",
    "color": { "r": 0, "g": 0, "b": 0 }
  }],
  "strokeStyleId": "",
  "strokeWeight": 3,
  "strokeAlign": "CENTER",
  "strokeCap": "ROUND",
  "strokeJoin": "ROUND",
  "fillGeometry": [{
    "windingRule": "NONZERO",
    "data": "M 50 0 L 61 35 L 98 35 L 68 57 L 79 91 L 50 70 L 21 91 L 32 57 L 2 35 L 39 35 Z"
  }],
  "vectorPaths": [{
    "windingRule": "NONZERO",
    "data": "M 50 0 L 61 35 L 98 35 L 68 57 L 79 91 L 50 70 L 21 91 L 32 57 L 2 35 L 39 35 Z"
  }]
}
```

## handleMirroring 属性说明

`handleMirroring` 控制矢量节点编辑时控制柄的镜像行为：

- **`"NONE"`**（默认）：控制柄独立移动,不镜像
- **`"ANGLE"`**：控制柄角度镜像,但长度独立
- **`"ANGLE_AND_LENGTH"`**：控制柄角度和长度都镜像

```json
{
  "type": "VECTOR",
  "handleMirroring": "ANGLE_AND_LENGTH"
}
```

## 常见陷阱

- **无效路径数据**：Figma 的解析器很严格；使用上述确切的间距。
- **坐标边界**：保持坐标在 0 到 width/height 之间以避免裁剪。
- **缺少 fillGeometry**：没有此属性,VECTOR 可能不会视觉渲染。
- **异步样式 ID 设置**：插件自动处理,但确保样式 ID 为字符串。

## 异步操作处理

插件在处理某些属性时会进行异步操作：

1. **样式 ID 设置**：`fillStyleId`、`strokeStyleId`、`effectStyleId` 等样式 ID 的设置是异步的
2. **字体加载**：TEXT 节点的字体加载需要异步完成
3. **图片加载**：IMAGE 填充需要异步加载图片数据

**最佳实践**：
- 始终将样式 ID 设置为字符串类型（空字符串 `""` 或有效的样式 ID）
- 确保字体在 Figma 中可用,否则会回退到默认字体
- 图片填充需要提供有效的 `imageHash` 或 `imageRef`
