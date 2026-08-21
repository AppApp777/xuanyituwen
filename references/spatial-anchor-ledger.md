# 场景空间锚点账本

这份账本解决的不是“画面风格像不像”，而是“同一个物件在连续图中到底属于哪里”。它是场景的空间真相源，必须在第一张图生成前建立。

## 两层空间模型

不要把场景拓扑和镜头投影混成一个坐标合同：

### 场景拓扑（必须保持）

- `scene_id`：场景母版的稳定编号。
- `ANCHOR-*`：物件身份。
- `parent_surface`：门扇、门框、墙面、地面、柜体或设备。
- `local_relation`：左／右／上／下、贴合、同轴、相邻和连接关系。
- `orientation`、`scale`、`allowed_state_changes`、`forbidden_changes`。

### 镜头投影（可以变化）

- `shot_id`：本张镜位编号。
- `coordinate_space`：`scene-topology` 或 `shot-projection`。
- `source_asset`：场景母版或上一张合格参考图。
- `shot_class`：远景、近景、俯视、门内、门外等。
- `image_bbox`：只在同镜位或可比较镜位时填写的图像平面框。
- `crop_allowance`：允许的裁切和遮挡范围。

镜头改变后，优先比较父面、局部拓扑、朝向、身份和状态，不机械要求物件永远位于屏幕同一个像素。

## 锚点定义

每个会影响叙事、方向或识别的物件都登记一个唯一的 `ANCHOR-*`。优先登记门、窗、墙缝、猫眼、门链、铰链、开关、柜子、镜子、电视、楼梯和设备接口。

| 锚点 ID | 物件 | 所属父面／载体 | 局部拓扑 | 母版坐标 | 相邻锚点 | 朝向／尺度 | 允许变化 | 禁止变化 |
|---|---|---|---|---|---|---|---|---|
| `ANCHOR-01` |  |  |  | `x=，y=，w=，h=` |  |  |  |  |

不能只记“右边”或“靠下”。默认记录两个相邻锚点；稀疏场景只有一个合理邻居时，写明“单邻居例外”及原因。屏幕坐标随裁切和镜头变化时可以改变，但父面、局部关系、上下顺序、朝向、尺度和物件身份不能改变。

## 每张 prompt 必须携带的合同

```text
Spatial topology contract: use scene <scene_id> and do not mirror or redesign the layout. Anchor <ANCHOR-ID> <object> is physically attached to <parent surface>. Preserve its local relation to <neighbor anchors>, orientation, scale, and identity. Camera angle or crop may change the screen projection, but must not change the parent surface, side, height, neighboring relations, or object identity. Do not relocate it, flip it, duplicate it, or move it to an alternative parent.
Shot projection: use shot <shot_id>, coordinate space <scene-topology or shot-projection>, source asset <path>, shot class <class>, and crop allowance <allowed crop or occlusion>. Compare image-plane boxes only when the shot class is comparable.
```

## 铰链示例

不要写：

```text
There is a hinge somewhere near the door.
```

要写成：

```text
Spatial topology contract: ANCHOR-03 is the vertical column of three brass hinges attached to the fixed door-frame side, not the wooden door leaf. It stays on the left edge of the door assembly, below ANCHOR-02 and beside ANCHOR-04, with the same vertical order and scale. The camera may move closer, but must not mirror the doorway, move a hinge onto the door leaf, or invent a second hinge column.
Shot projection: this is shot SHOT-04, a close interior evidence view. The hinge column may be partially occluded by the door edge; its scene-topology relation remains the same.
```

这段不是装饰性描述，而是生成前的硬约束。若模型仍然改变锚点，必须把失败原因记录在验收表中，并用场景母版或上一张合格图作为参考图重新生成；不能把错误图当作新的连续性真相源。

## 每张图的检查记录

| FRAME ID | shot_id | 锚点 ID | 是否可见 | 父面是否正确 | 局部拓扑是否正确 | 投影框是否可比较 | 是否镜像或漂移 | 处理 |
|---|---|---|---|---|---|---|---|---|
| `FRAME-01` | `SHOT-01` | `ANCHOR-01` |  |  |  |  |  |  |

如果锚点被遮挡，必须明确写“本张被遮挡”，下一张重新出现时仍必须回到账本的父面和局部关系；“这一张没看清”不能成为重新摆放的理由。
