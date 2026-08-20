# 场景空间锚点账本

这份账本解决的不是“画面风格像不像”，而是“同一个物件在连续图中到底属于哪里”。它是场景的空间真相源，必须在第一张图生成前建立，并在每一张实际 prompt 中重复携带。

## 锚点定义

每个会影响叙事、方向或识别的物件都要登记一个唯一的锚点编号。优先登记门、窗、墙缝、猫眼、门链、铰链、开关、柜子、镜子、电视、楼梯、设备接口等不会凭空移动的结构或道具。

| 锚点 ID | 物件 | 所属载体／父面 | 参考坐标 | 相邻锚点与关系 | 朝向 | 允许变化 | 禁止变化 |
|---|---|---|---|---|---|---|---|
| A01 |  |  | `x=，y=，w=，h=`，以场景母版为准 |  |  |  |  |

### 坐标规则

- 先选一张“场景母版”，在母版上以 0 到 1 的归一化坐标记录锚点的包围框，坐标相对于整张画面。
- 不能只记“右边”或“靠下”。至少同时记录父面、局部位置、上下左右边界、尺寸等级和两个相邻锚点。
- 对门、墙、柜体等平面物件，额外记录局部坐标，例如“在门扇右边缘内侧、位于猫眼下方、距门底约三分之一高度”。
- 屏幕坐标会随裁切和镜头变化，但父子关系不能变化。画面换角度时，优先保持“铰链属于门框、位于门扇左侧边缘、在上铰链下方”这类局部关系，不要机械地把它搬到画面同一个像素位置。

## 必须写进每张 prompt 的锚点合同

```text
Spatial anchor contract: use the same scene master and do not mirror or redesign the layout. Anchor A01 <object> is physically attached to <parent surface>, not to <alternative surface>. In the scene-master coordinate system it occupies x=<value>, y=<value>, w=<value>, h=<value>. Locally it stays <left/right/upper/lower relation> to <neighbor A02> and <neighbor A03>, with the same orientation and scale. Camera angle or crop may change the screen projection, but must not change the parent surface, side, height, neighboring relations, or object identity. Do not relocate it, flip it, duplicate it, or move it from <parent> to <alternative parent>.
```

## 铰链示例

不要写：

```text
There is a hinge somewhere near the door.
```

要写成：

```text
Spatial anchor contract: the three brass hinges belong to the fixed door-frame side, not the wooden door leaf. In the scene master, the hinge column is on the left edge of the door assembly, with the top hinge at y=0.21, the middle hinge at y=0.49, and the bottom hinge at y=0.77; each hinge is vertically aligned with the same narrow frame strip. Keep the peephole on the upper-right area of the door leaf and the chain plate below it. Preserve the parent surfaces, left-right orientation, vertical order, spacing, and scale across every frame. Do not mirror the doorway, move a hinge onto the door leaf, place a hinge on the bottom edge, or invent a second hinge column.
```

这段不是装饰性描述，而是生成前的硬约束。若模型仍然改变锚点，必须把失败原因记录在验收表中，并用场景母版或上一张合格图作为参考图重新生成；不能把错误图当成新的连续性真相源。

## 每张图的检查记录

| 图号 | 锚点 ID | 是否可见 | 父面是否正确 | 局部坐标／相邻关系是否正确 | 是否镜像或漂移 | 处理 |
|---:|---|---|---|---|---|---|
| 1 | A01 |  |  |  |  |  |

如果锚点被遮挡，必须明确写“本张被遮挡”，并在下次可见时回到同一个父面和局部关系；“这一张没看清”不能成为重新摆放的理由。
