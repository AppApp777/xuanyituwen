# 方法来源与改写边界

本 skill 参考了公开 GitHub 项目的方法论，但没有复制受许可证约束的原文、模板、知识库、Agent 文件或代码。

## 本次核对记录

- 核对日期：2026-08-21。
- 核对范围：参考项目公开主页、仓库说明和本项目实际采用的抽象原则。
- 版本政策：发布新版本时，维护者应把参考项目的具体 commit 或 tag、检查日期和许可证状态补进本节；没有固定版本号时，不把“当前主分支”写成永久事实。
- 选择原则：只吸收因果控制、信息权限、伏笔管理和场景连续性等抽象方法；本项目的六张以上节奏、`EVID-*`／`ANCHOR-*` 合同、无字图与独立配文交付、终局主体验收和产物校验器均为本项目自建。

## 参考项目

- [wgwtest/novel-writing](https://github.com/wgwtest/novel-writing)，MIT。吸收因果链、角色知识、观察权限、场景进入与退出状态和连续性检查的思路。
- [zhougz520/novel-architect](https://github.com/zhougz520/novel-architect)，Apache-2.0。吸收伏笔、读者期待、行动代价和节奏门禁的轻量化思路。
- [mushroomfk/long-novel-agent-kit](https://github.com/mushroomfk/long-novel-agent-kit)，MIT。只吸收事实、角色、物件、地点、时间线和未偿剧情债分离管理的状态思想。
- [modoojunko/awesome-novel-agent](https://github.com/modoojunko/awesome-novel-agent)，GPL-3.0。只参考信息差、逐场景钩子和公平反转方法，不直接复制其文件或大段文字。
- [YangsonHung/awesome-agent-skills](https://github.com/YangsonHung/awesome-agent-skills) 的 `novel-writer`，MIT。吸收场景五要素和线索公平原则。
- [xcrrr/claude-skills](https://github.com/xcrrr/claude-skills) 的 `storyteller`，MIT。吸收核心情绪问题、角色欲望与恐惧、以及“回看时必然，初读时意外”的结尾原则。

## 本项目自建部分

以下能力不是上述项目现成提供的，由本项目独立设计：

- 六张以上、默认七张的竖屏伪记录节奏。
- 记录来源切换的时间、权限和证据理由。
- 角色外观、场景结构、物件位置和画面来源的视觉真相源。
- 9∶16、1080×1920、平台覆盖安全区和无平台界面的成片约束。
- 生图模型只生成无字底图，最终图像只做尺寸、色彩模式和 PNG 归一化；第一人称发布页配文另存为 `captions.md`，不嵌入图片。
