# mixins 与渲染器速查表

以下内容根据 `@elemental-figma/object-bridge` 库整理，帮助在生成 JSON 时了解不同节点的可用属性及其处理方式。对应源码位于 `node_modules/@elemental-figma/object-bridge/src/`。

## renderer 映射

| 节点类型 | 渲染器文件 | 关键 mixin |
| --- | --- | --- |
| `FRAME` / `INSTANCE` | `renderers/frame.ts` | `baseNodeMixin`, `layoutMixin`, `geometryMixin`, `cornerMixin`, `rectangleNodeMixin`, `constraintsMixin`, `autoLayoutMixin`, `frameMixin`, `frameSpecificMixin`, `sceneNodeMixin` |
| `COMPONENT` / `COMPONENTSET` | `renderers/component.ts`, `renderers/componentset.ts` | 同 Frame，额外 `publishableMixin` |
| `TEXT` | `renderers/text.ts` | `baseNodeMixin`, `layoutMixin`, `geometryMixin`, `exportMixin`, `blendMixin`, `sceneNodeMixin`, `constraintsMixin` |
| `RECTANGLE` / `ELLIPSE` / `STAR` 等基础形状 | 对应 `renderers/*.ts` | `baseNodeMixin`, `layoutMixin`, `geometryMixin`, `cornerMixin`, `rectangleNodeMixin`, `exportMixin`, `blendMixin`, `sceneNodeMixin`, `constraintsMixin` |
| `GROUP` | `renderers/group.ts` | `baseNodeMixin`, `layoutMixin`, `exportMixin`, `blendMixin`, `frameMixin`, `sceneNodeMixin` |
| `PAGE` | `renderers/page.ts` | `baseNodeMixin`, `exportMixin`, `pageMixin` |
| `SVG` | `renderers/svg.ts` | `baseNodeMixin`, `layoutMixin`, `exportMixin`, `blendMixin`, `frameMixin`, `sceneNodeMixin`, `constraintsMixin` |

## 常用 mixin 行为摘要

- **`layoutMixin`** (`mixins/layoutMixin.ts`)  
  支持设置 `relativeTransform`、`x`、`y`、`rotation`、`width`、`height`、`layoutAlign`、`layoutGrow`。对自动布局节点，结合 `autoLayoutMixin` 控制尺寸。

- **`autoLayoutMixin`** (`mixins/autoLayoutMixin.ts`)  
  接收 `layoutMode`（`NONE` / `HORIZONTAL` / `VERTICAL`）、`primaryAxisSizingMode`、`counterAxisSizingMode`、`primaryAxisAlignItems`、`counterAxisAlignItems`、`paddingLeft/Right/Top/Bottom`、`itemSpacing`。若提供 `horizontalPadding`/`verticalPadding` 会转换为具体 padding 字段。

- **`geometryMixin`** (`mixins/geometryMixin.ts`)  
  负责 `fills`, `strokes`, `strokeWeight`, `strokeAlign`, `strokeCap`, `strokeJoin`, `dashPattern`, `fillStyleId`, `strokeStyleId`。默认为空填充，需要显式提供背景色。

- **`constraintsMixin`** (`mixins/constraintsMixin.ts`)  
  默认 `{"horizontal": "MIN", "vertical": "MIN"}`，如需居中等必须覆盖该字段。

- **`frameSpecificMixin`** (`mixins/frameSpecificMixin.ts`)  
  控制 `clipsContent`, `guides`, `layoutGrids`, `gridStyleId`，缺省 `clipsContent: false`。

- **`rectangleNodeMixin`** (`mixins/rectangleNodeMixin.ts`)  
  管理四个角半径字段 `topLeftRadius` 等。

- **`blendMixin`** (`mixins/blendMixin.ts`)  
  读取 `opacity`, `blendMode`, `isMask`, `effects`, `effectStyleId`。阴影、模糊等必须在 `effects` 中定义。

- **`pageMixin`** (`mixins/pageMixin.ts`)  
  设置页面背景，默认淡灰色。若需自定义画布背景，请提供 `backgrounds` 数组。

- **`publishableMixin`** (`mixins/publishableMixin.ts`)  
  允许为组件设置 `description`、`documentationLinks`。

- **`text` 渲染特殊逻辑** (`renderers/text.ts`)  
  - 在创建节点前调用 `figma.loadFontAsync(props.fontName)`，因此 JSON 必须提供合法 `fontName`。
  - 属性映射包括 `characters`, `fontSize`, `textAlign*`, `lineHeight`, `textCase`, `textDecoration`, `letterSpacing`, `textAutoResize`, `hyperlink`。
  - 若 `props.hasDefinedWidth` 且 `textAutoResize` 不是 `WIDTH_AND_HEIGHT`，会尝试 `resize` 设置。

- **`svg` 渲染特殊逻辑** (`renderers/svg.ts`)  
  - `props.source` 为 SVG 字符串；通过 `hashCode` 与 `setPluginData('svgHash')` 判断是否需要重新创建节点。
  - 若内容变更，会先清空旧子节点再导入新 SVG。

## 生成 JSON 时的实践要点

1. **布局**：在容器节点至少提供 `layoutMode` 与 `primaryAxisSizingMode`，避免默认 `NONE` 导致自动排版失效。
2. **颜色**：所有视觉元素显式提供 `fills`；对于透明背景可将 `opacity` 设为 0。
3. **约束**：针对需要对齐的元素（如按钮栏对齐底部），通过 `constraints` 指定行为。
4. **字体**：限定使用 Inter Regular/Medium/Bold/Semi Bold（控制器已预加载）。如需其它字重先调整插件控制器。
5. **SVG**：为图标提供完整 SVG 文本；更新图标时修改 `source` 字符串即可触发重渲染。

通过以上速查表，可快速将设计需求映射到 JSON 字段，减少查阅源码的负担。
