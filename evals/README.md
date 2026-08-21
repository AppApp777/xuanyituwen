# 评测说明

这里存放可重复运行的轻量评测合同。它们检查阶段边界、稳定编号、文件绑定和终局图验收字段，不把一次联网生图当成持续集成的前置条件。完整成片示例的 `manifest.json` 还记录了终局图的主体框、缩略图规格和单一焦点结果。

## 当前覆盖

- `direction-gate-v1`：用户只要方向时，先给三个方向并停下等待选择。
- `control-sheet-v1`：已选方向时，先形成可审的控制稿和伏笔账本。
- `frame-interface-v1`：控制稿确认后，逐图卡片使用 `FACT-*`、`EVID-*`、`CLUE-*`、`ANCHOR-*`、`FRAME-*` 编号。
- `caption-delivery-v1`：七张图与第一人称配文、提示词、图片路径互相绑定。
- `ending-gate-v1`：终局图检查主体占比、缩略图识别度、单一焦点和前文证据回收。

## 本地运行

在仓库根目录执行：

```bash
python scripts/validate_evals.py
python scripts/validate_artifact_package.py examples/cat-eye-person --strict
python -m pytest -q
```

`evals/results/` 只记录已经实际运行过的结果。当前版本的结果是结构校验通过；模型主观评分和联网生图没有伪装成自动化通过项。这里也刻意不评测技能触发准确率，以免把路由实验混进生产流程。

当交付合同发生变化时，先更新 `evals/evals.json` 与对应 fixture，再更新脚本或测试。每个评测都应说明允许动作、禁止动作、机器断言和人工判断边界。
