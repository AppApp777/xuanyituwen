# 《猫眼里面的人》场景空间锚点账本

这份账本是下一版重生成的空间真相源。当前旧试跑图中部分视角已经发生漂移，不能反过来当作锚点参考；后续必须以本账本和场景母版为准。

## 场景母版

- **母版**：`base/frame-01.png` 的门内视角，仅作为门体结构参考，不作为人物姿势参考。
- **坐标系**：画布左上角为 `x=0，y=0`，右下角为 `x=1，y=1`；坐标相对于整张 9∶16 画面。
- **固定视角事实**：深棕色门体位于画面右侧，门扇、门框、猫眼和门链必须保持同一套父子关系；镜头可以靠近或从门内外切换，但不能镜像门体。

## 固定锚点

| 锚点 ID | 物件 | 所属父面／载体 | 母版归一化位置 | 相邻关系 | 朝向／尺度 | 允许变化 | 禁止变化 |
|---|---|---|---|---|---|---|---|
| ANCHOR-01 | 深棕色门扇 | 门体总成中的木质门扇 | `x=0.41，y=0.02，w=0.50，h=0.91` | 左邻 ANCHOR-02，右邻 ANCHOR-03、ANCHOR-04 | 竖直，最大结构面 | 开合角度、门缝宽度 | 变成门框、镜像到画面左侧、改变木纹方向 |
| ANCHOR-02 | 门框与右侧旧划痕 | 墙体门洞，不属于门扇 | `x=0.36，y=0.00，w=0.61，h=0.96` | 包围 ANCHOR-01，划痕位于右侧边框中段 | 竖直，窄条结构 | 被门边或人物局部遮挡 | 跑到门扇上、换到下边、消失后在另一侧出现 |
| ANCHOR-03 | 黄铜猫眼 | ANCHOR-01 门扇 | `x=0.67，y=0.23，w=0.05，h=0.04` | 在 ANCHOR-04 上方，位于 ANCHOR-01 上半部 | 圆形，固定小尺度 | 起雾、拆下、出现湿痕 | 移到门框、移到下半部、变成第二个猫眼 |
| ANCHOR-04 | 门链固定板与链条 | 固定板分别属于 ANCHOR-01 与 ANCHOR-02，链条连接两者 | 固定板位于 ANCHOR-01 右缘 `y=0.30–0.44`，链条只在两固定板之间 | ANCHOR-03 在其上方，ANCHOR-05 在其下方 | 水平跨过门缝，黄铜 | 松动、弯折、被手抓住 | 固定板互换父面、链条跑到门底、镜像到左侧 |
| ANCHOR-05 | 锁具与把手 | ANCHOR-01 门扇右缘 | `x=0.83，y=0.36，w=0.09，h=0.18` | 在 ANCHOR-04 下方，贴近 ANCHOR-01 右缘 | 竖直金属件 | 被手遮挡、反光变化 | 变成门框配件、跑到门中央或底部 |
| ANCHOR-06 | 猫眼后检修腔入口 | ANCHOR-01 与 ANCHOR-02 交界后的门体内部 | 入口中心必须与 ANCHOR-03 同轴，不能独立漂移 | 与 ANCHOR-03 同轴，与 ANCHOR-04 在同一门体平面 | 狭窄、沿门体厚度向后延伸 | 被黑暗遮挡、开口扩大 | 变成房间、走廊或门外新洞口 |
| ANCHOR-07 | 林峥红线手腕 | 林峥身体 | 只记录相对关系，不固定屏幕坐标：位于伸入镜头的左手腕 | 与 ANCHOR-04、ANCHOR-06 同一威胁路径 | 细红线，近景可放大 | 从线头到完整手腕 | 换到右手、换色、脱离人物身体 |

## 每张 prompt 必须携带的合同

```text
Spatial topology contract: use the same scene master and do not mirror the doorway. ANCHOR-01 is the dark walnut door leaf, ANCHOR-02 is the fixed door frame and right-side scratch, ANCHOR-03 is the brass peephole mounted in the upper half of ANCHOR-01, ANCHOR-04 is the brass chain connecting hardware on ANCHOR-01 and ANCHOR-02, ANCHOR-05 is the lockset on the right edge of ANCHOR-01, and ANCHOR-06 is the narrow service cavity coaxial with ANCHOR-03 behind the door assembly. Preserve these parent surfaces, local positions, left-right orientation, vertical order, neighboring relations, and scale. Camera angle or crop may change screen projection, but must not move ANCHOR-03 onto ANCHOR-02, move ANCHOR-04 to the bottom edge, move ANCHOR-05 to the center, mirror the doorway, or turn ANCHOR-06 into a separate room. Do not duplicate or relocate any anchor.
```

若某个锚点本张不可见，prompt 要写明“occluded by hand／door edge／darkness”，下一张重新出现时仍必须回到本账本的父面和局部关系。
