# 生图 prompt 预设库

这份文件把首次完整试跑中验证有效的提示词结构固化为可复用模块。它不是一条适用于所有故事的固定长 prompt，而是由“全局基底＋记录载体＋角色与场景连续性锁定＋空间锚点合同＋本张证据＋物理关系＋负面约束”拼成每一张底图的实际 prompt。

## 目录

1. [使用原则](#使用原则)
2. [全局基底](#全局基底)
3. [连续性锁定段](#连续性锁定段)
4. [空间锚点合同段](#空间锚点合同段)
5. [记录载体预设](#记录载体预设)
6. [物理关系与证据段](#物理关系与证据段)
7. [负面约束段](#负面约束段)
8. [终局惊吓段](#终局惊吓段)
9. [拼装顺序与示例](#拼装顺序与示例)

## 使用原则

- 每张图只选择一个主要记录载体，必要时才混合第二个载体。
- 固定段负责风格、人物、场景和禁止项，变化段只负责本张新的证据与状态变化。
- 不要为了“更恐怖”擅自增加没有出现在故事控制稿里的怪物、尸体、血迹、超能力或新人物。
- 涉及空间关系时，必须同时写出两个参照物、关系方向和光源条件，不要只写“诡异”“不协调”。
- 生成第一张图前先建立场景母版和空间锚点合同；关键物件的父面、局部坐标、相邻关系和朝向必须成为每张 prompt 的固定段。
- 画面换角度时保持场景坐标系和父子关系，不把屏幕坐标的变化误当成物件可以移动；严禁镜像、换父面、上下顺序改变或同类物件重复。
- 涉及手机、监控或门铃画面时，必须明确屏幕可以显示什么、绝对不能显示什么。
- 画面内不生成任何可读文字，底图统一写 `no readable text, no subtitles, no generated Chinese characters`；抖音发布页第一人称配文写入独立的 `captions.md`，绝不嵌入图片。
- 每张实际发送的完整 prompt 保存到输出包的 `prompts/frame-XX.txt`，便于回看哪一段导致了问题。

## 全局基底

默认真实记录感使用下面的固定段。将尖括号内容替换为故事中的具体值，不要删除最后的格式与界面限制。

```text
Use case: photorealistic-natural.
Asset type: vertical pseudo-documentary still for a suspenseful social-media photo story.
Style/medium: ordinary handheld smartphone photography, imperfect framing, subtle compression, realistic low-production texture, natural imperfect light, restrained documentary realism, not a cinematic poster and not polished horror illustration.
Format: vertical 9:16 composition, intended for a 1080x1920 final raster image.
```

如果故事明确使用档案、监控或都市传说图鉴，不要把所有画面都强行写成手机照片。保留上面的真实质感原则，但换用对应的记录载体预设。

## 连续性锁定段

每张图都重复注入本组图的角色、场景和道具真相。只允许变化字段发生变化。

```text
Continuity lock: the same protagonist <name>, <age and identity>, <body type>, <face and hair markers>, wearing <fixed clothing>, with <fixed identifying detail>. Preserve the same <location>, <spatial layout>, <lighting source>, and <camera relationship> from the previous frame. Recurring prop: <prop name>, <shape/color/material/unique mark>; its current state is <state> and its position is <position>. Do not change the protagonist's face, hair, age, clothing, room layout, prop identity, or time relationship unless the frame card explicitly states the change.
```

### 连续性变化段

把变化写成可观察的状态迁移，不要写成抽象剧情：

```text
Frame change: compared with the previous frame, <one visible state change>. Keep <all unchanged anchors> unchanged. The change must be physically visible in the same space and must not introduce an unexplained new object.
```

## 空间锚点合同段

这段必须紧跟在连续性锁定段之后，不能被省略，也不能每张图临时改写。具体数值来自 `references/spatial-anchor-ledger.md` 和输出包的场景母版。

```text
Spatial anchor contract: use the same scene master and do not mirror or redesign the layout. Anchor <ID> <object> is physically attached to <parent surface>, not to <alternative surface>. In the scene-master coordinate system it occupies x=<value>, y=<value>, w=<value>, h=<value>. Locally it stays <left/right/upper/lower relation> to <neighbor anchor A> and <neighbor anchor B>, with the same orientation and scale. Camera angle or crop may change the screen projection, but must not change the parent surface, side, height, neighboring relations, or object identity. Do not relocate it, flip it, duplicate it, or move it from <parent> to <alternative parent>.
```

对于一组图中的多个固定物件，逐项列出合同，不要用一句“保持场景一致”代替。铰链、门链、猫眼、门把手这类附着在不同父面上的物件，要分别写清“属于门扇”还是“属于门框”。

示例：

```text
Spatial anchor contract: the three brass hinges belong to the fixed door-frame side, not the wooden door leaf. In the scene master, the hinge column is on the left edge of the door assembly, with the top hinge at y=0.21, the middle hinge at y=0.49, and the bottom hinge at y=0.77; each hinge is vertically aligned with the same narrow frame strip. Keep the peephole on the upper-right area of the door leaf and the chain plate below it. Preserve the parent surfaces, left-right orientation, vertical order, spacing, and scale across every frame. Do not mirror the doorway, move a hinge onto the door leaf, place a hinge on the bottom edge, or invent a second hinge column.
```

## 记录载体预设

每张图从下面选择一个主要载体，再接上本张画面内容。

### 一、手机室内随手拍

```text
Record carrier: a candid handheld phone photo taken by <recorder> inside <location> at <time>. Use a natural eye-level or slightly awkward handheld angle, ordinary room light, believable distance, and imperfect framing. The camera should feel like evidence captured quickly, not a staged photoshoot.
```

适合：房间、门口、人物反应、第一次发现异常、道具状态变化。

### 二、门口与门内证据

```text
Record carrier: a low or over-the-shoulder phone photo taken from <inside/outside> the same door. Show the threshold, the door edge, the peephole or door chain, and enough of both sides of the threshold to prove where the evidence is located. Keep the hallway depth and room-side objects consistent.
```

适合：空走廊、猫眼、门链、脚印、门下阴影、门内外方向关系。

### 三、现场近距离证据照

```text
Record carrier: a close documentary evidence photo taken immediately after <action>. Make <decisive object or mark> the sharpest visual fact while keeping one or two familiar background anchors visible for continuity. Use ordinary phone exposure and surface texture; do not turn the evidence into a horror illustration.
```

适合：墙缝、钥匙、纸条、抓痕、血迹以外的物件状态、调查动作。

### 四、设备或维修空间记录

```text
Record carrier: a phone-lit evidence photo inside <specific service space or device-recorded location>. Make the space physically plausible, narrow, damp, and connected to the previously established building. Keep the foreground evidence large enough to identify and use the distant area only for a restrained silhouette, reflection, or movement cue.
```

适合：维修通道、楼梯间、监控盲区、门铃摄像头、设备背面空间。

### 五、反光与终局记录

```text
Record carrier: a shaky candid phone photo that accidentally captures <reflection or secondary view> while the protagonist is focused on <ordinary action>. The threat must be physically present in the reflection or background, not a graphic overlay. Preserve enough ordinary room detail for the viewer to discover the threat on a second look.
```

适合：电视反光、镜面、窗户、黑屏设备、最后一张的贴身揭示。

### 六、档案与都市传说图鉴

```text
Record carrier: a low-production field archive photograph or an amateur urban-legend documentation image. Include only the paper, numbering, location marker, or capture artifact that already exists in the story control sheet. Keep the evidence sparse and concrete; do not replace event progression with a long explanatory board.
```

适合：调查档案、现场打印件、旧照片、民间流传的地点记录。

## 物理关系与证据段

这是首次试跑最需要固化的部分。每当故事依赖“谁在什么位置”“影子朝哪边”“脚印从哪里到哪里”时，使用下面结构。

```text
Required visual evidence: show <element A> and <element B> in the same frame. Their spatial relationship must be unmistakable: <A is inside/outside/behind/in front of/closer to/farther from B>. Show the direction of <movement, footprint, gaze, shadow, light, or water trail> as <explicit direction>. The viewer must be able to verify this relationship from the image alone, without relying on the caption.
```

### 光源与影子

```text
Lighting relation: the light source is visibly coming from <direction and source>. The shadow of <object> must fall toward <direction>, while <contradictory or anomalous relation> remains visible. Show the source, the object, and the shadow in one coherent composition. Do not use supernatural glow or cinematic fog to imply the anomaly.
```

### 脚印、液体与移动轨迹

```text
Trace relation: show a continuous, readable trail beginning at <origin> and pointing toward <destination>. The trail is <inside/outside>, crosses or does not cross <threshold>, and stops at <specific object or wall>. Do not add extra footprints, extra shoes, or a second unexplained source.
```

### 反光、视线与背后人物

```text
Reflection relation: the secondary figure is physically present in <mirror/television/window/metal surface> and occupies the space behind <protagonist>. The reflection must be consistent with the room layout and camera position. Keep the protagonist unaware if the frame card requires it. Do not render the threat as a floating face, collage, or post-production graphic.
```

## 负面约束段

每张图都使用基础界面负面段。设备类画面再追加对应的屏幕负面段。

### 基础负面段

```text
No platform interface, no avatar, no username, no likes, no comments, no title, no share button, no watermark, no logo, no readable text, no subtitles, no generated Chinese characters, no decorative horror illustration, no cinematic poster treatment, no unexplained new character, no unexplained new prop, no random costume change, no fantasy architecture, no exaggerated gore.
```

### 手机与设备屏幕负面段

```text
The phone or device screen may show only a black screen, a soft glow, or an abstract unreadable waveform. No app layout, no thumbnails, no buttons, no icons, no status bar, no notification cards, no profile image, no interface panels, no readable words, and no social-media screen design.
```

### 真实记录感负面段

```text
Avoid polished film stills, centered poster composition, beauty lighting, symmetrical horror staging, CGI monster anatomy, floating supernatural effects, excessive fog, artificial red color grading, and an obviously staged actor pose. Keep ordinary spatial imperfections, believable materials, and the evidence legible.
```

## 终局惊吓段

只有最后一张或明确的提前揭示图使用，不要让前几张提前消耗终局冲击。

```text
Ending beat: reveal the established threat by reinterpreting <at least two earlier details>. The final threat must be connected to <existing prop, shadow, footprint, voice, clothing, or location> and must leave a visible consequence. Make the scare discoverable in the image before the creator's publish-page caption explains it. Do not introduce a new identity, ability, object, or world rule in the final frame.
```

如果需要突然惊吓：

```text
Jump-scare constraint: keep the frame ordinary at first glance, then place the threat close to the protagonist through a physically plausible background, reflection, doorway, or blind spot. Use proximity, occlusion, and delayed recognition rather than gore or a monster close-up.
```

## 拼装顺序与示例

### 推荐拼装顺序

按下面顺序拼成实际发送给 `image_gen` 的完整 prompt：

1. 全局基底。
2. 主要记录载体预设。
3. 连续性锁定段。
4. 空间锚点合同段。
5. 本张场景、人物动作和构图。
6. 本张必须出现的视觉证据。
7. 物理关系、光源或反光关系段。
8. 终局段（只在需要时）。
9. 基础负面段和设备屏幕负面段。

### 第二张的拼装示例

```text
Use case: photorealistic-natural.
Asset type: vertical pseudo-documentary still for a suspenseful social-media photo story.
Style/medium: ordinary handheld smartphone photography, imperfect framing, subtle compression, realistic low-production texture, natural imperfect light, restrained documentary realism.
Format: vertical 9:16 composition, intended for a 1080x1920 final raster image.
Record carrier: an over-the-shoulder phone photo taken from inside the apartment, looking through the same chained door into the empty hallway.
Continuity lock: the same 22-year-old slim Chinese male with pale tired face, straight black hair over the forehead, tiny mole under the left eye, charcoal-gray hoodie, old white T-shirt, black sweatpants, and black canvas shoes. Preserve the same dark brown door, brass peephole, brass chain, green hallway, and red fire-hose cabinet.
Required visual evidence: show the empty hallway beyond the chain and no person outside the threshold. The voice claims someone is at the door, but the visual evidence must contradict that claim.
Composition/framing: the protagonist holds a black phone close to his ear while keeping the chain latched; keep the door gap and hallway depth visible.
Lighting/mood: cold hallway light against warmer room light, quiet contradiction, realistic phone exposure.
The phone screen may show only an abstract unreadable waveform. No readable text.
No platform interface, no avatar, no username, no likes, no comments, no title, no share button, no watermark, no logo, no subtitles, no generated Chinese characters, no decorative horror illustration, no cinematic poster treatment, no unexplained new prop or character.
```

### 第七张的拼装示例

```text
Use case: photorealistic-natural.
Asset type: vertical pseudo-documentary jump-scare still.
Record carrier: a shaky candid phone photo that accidentally captures the black television reflection while the protagonist sits at the desk.
Continuity lock: preserve the same protagonist, same charcoal-gray hoodie, same room, same black television, same dark brown door, same displaced coat rack, and the previously established maintenance-hatch seam.
Required visual evidence: the protagonist is unaware, while a figure in the established roommate's dark jacket stands inches behind him and is visible in the television reflection. The figure must connect to the earlier distant back-facing silhouette, not appear as a new monster.
Reflection relation: the figure is physically present in the television reflection and occupies the space behind the protagonist, consistent with the room layout and camera position.
Ending beat: reinterpret the earlier footprint, wall seam, recurring key fob, and dark jacket. Leave the protagonist facing the wrong direction with a visible new threat behind him.
Jump-scare constraint: keep the room ordinary at first glance; use proximity, shadow, and delayed recognition instead of gore.
The phone screen may show only a black screen or soft unreadable glow. No app layout, thumbnails, buttons, icons, status bar, notification cards, profile image, interface panels, or readable words.
No platform interface, no avatar, no username, no likes, no comments, no title, no share button, no watermark, no logo, no readable text, no subtitles, no generated Chinese characters, no decorative horror illustration, no cinematic poster treatment.
```
