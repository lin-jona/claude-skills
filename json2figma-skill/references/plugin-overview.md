# JSON2Figma 插件工作流概览

## 组件与职责

- **UI 前端（`packages/plugin/src/app/components/App.tsx`）**  
  React 表单收集 JSON 文本，通过 `parent.postMessage` 发送 `type: "create-components"` 消息给插件控制器。示例代码见该文件第 56-111 行。

- **插件控制器（`packages/plugin/src/plugin/controller.tsx`）**  
  监听 UI 消息，预加载 Inter Regular/Medium/Bold/Semi Bold 字体，然后调用 `renderJSON(data.document || data)`。位置：26-48 行。

- **渲染核心（`@elemental-figma/object-bridge`）**  
  `renderJSON` 由 `node_modules/@elemental-figma/object-bridge/src/index.ts` 暴露，本质执行 `renderJSONRootToFigma`：遍历文档 → 页面 → 子节点，依据 `type` 选择 renderer 并递归创建 Figma 节点。渲染逻辑入口位于 `src/render.ts:1-43`。

## 节点类型与渲染器

支持的节点类型（`renderers/index.ts:1-23`）：

```
RECTANGLE | TEXT | PAGE | FRAME | COMPONENT | COMPONENTSET
INSTANCE | STAR | VECTOR | LINE | GROUP | ELLIPSE | SVG | SLICE
```

每种类型都对应一个 mixin 组合，确保布局、几何、填充等属性正确映射到 Figma API。例如：

- `frame` 渲染器：`renderers/frame.ts` 使用 `baseNodeMixin`, `layoutMixin`, `geometryMixin`, `autoLayoutMixin` 等。
- `text` 渲染器：`renderers/text.ts` 先 `figma.loadFontAsync(props.fontName)`，再设置 `characters`、`fontSize`、`textAutoResize` 等。

若 JSON 中包含 renderer 未覆盖的属性，mixin 会忽略或应用默认值（详见 `src/mixins`）。

## 数据流

```mermaid
flowchart TD
    UI[React UI<br/>App.tsx] -->|JSON 对象| Controller[controller.tsx]
    Controller -->|加载字体| FigmaAPI[(Figma Plugin API)]
    Controller -->|renderJSON| Bridge[@elemental-figma/object-bridge]
    Bridge -->|递归创建节点| FigmaAPI
```

## JSON 结构最低要求

> JSON 根对象必须遵循 Document → Page → Node 的层级，数值字段使用 0-1 浮点（颜色）或像素单位。

- **Document**  
  ```json
  {
    "id": "0:0",
    "type": "DOCUMENT",
    "name": "Demo",
    "documentColorProfile": "SRGB",
    "children": [ /* Page 数组 */ ]
  }
  ```
- **Page**  
  ```json
  {
    "id": "0:1",
    "type": "PAGE",
    "name": "Page 1",
    "children": [ /* Frame/Component 等 */ ]
  }
  ```
- **常见节点字段**
  - `id`: 任意字符串，Figma 导入后会重新分配；用于引用关系。
  - `type`: 支持的类型名称（大写）。
  - `name`: 图层名。
  - `x`, `y`, `width`, `height`: 绝对位置与尺寸。
  - `visible`, `locked`, `opacity`, `blendMode`: 可选状态属性。
  - `fills`: `[{ "type": "SOLID", "color": { "r": 0.12, "g": 0.34, "b": 0.56 }, "opacity": 1 }]`。
  - `children`: 嵌套节点数组；没有子节点时留空数组或省略。

### 文本节点特别要求

`renderers/text.ts` 需要以下字段：

```json
{
  "type": "TEXT",
  "characters": "按钮文案",
  "fontName": { "family": "Inter", "style": "Regular" },
  "fontSize": 16,
  "fills": [
    {
      "type": "SOLID",
      "visible": true,
      "opacity": 1,
      "blendMode": "NORMAL",
      "color": { "r": 1, "g": 1, "b": 1 }
    }
  ]
}
```

缺少 `fontName` 或 `characters` 会导致 `figma.loadFontAsync` 或赋值抛错。

## 属性处理要点

- **布局尺寸**：`layoutMixin` 支持 `layoutAlign`, `layoutGrow`, `relativeTransform`。当提供 `layoutMode` 为 `HORIZONTAL` / `VERTICAL` 时，还可添加 `primaryAxisSizingMode`, `paddingLeft` 等自动布局属性（`mixins/autoLayoutMixin.ts`）。
- **颜色/填充**：`geometryMixin` 默认空填充，若需背景色必须显式提供 `fills`。
- **约束**：`constraintsMixin` 默认最小值；如要中心对齐，设置 `"constraints": { "horizontal": "CENTER", "vertical": "CENTER" }`。
- **SVG**：传入 `type: "SVG"`，字段 `source` 为 SVG 字符串，插件会比对哈希决定是否重建（`renderers/svg.ts`）。

## 参考示例

- **完整样例**：`packages/plugin/src/plugin/data/test.ts` 提供了复杂页面结构，可作为字段全集参考。
- **简化样例**：见 `sample-card.json`（后续文档）。

## 调试建议

1. 在 Figma Dev 模式启动插件后，从控制台观察 `renderJSON` 抛出的日志。
2. 如果文本未显示，优先检查字体是否在 `loadFonts` 列表中及 JSON 是否声明 `fontName`。
3. 逐步构建树：先导入最小 Document/Page/Frame，再逐层添加子节点，便于定位字段错误。
