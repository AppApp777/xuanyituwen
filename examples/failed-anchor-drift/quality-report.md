# 失败验收报告

```yaml
severity: hard
result: fail
evidence: FRAME-06，ANCHOR-04，door-chain-parent-surface
reviewer: human-1
artifact: failed-frame.md
fix_target: frame-card-and-image-generation
```

## 不通过项

- `ANCHOR-04` 的父面从“门扇与门框之间”变成了“门扇内部”。
- 门体发生镜像，破坏了 `ANCHOR-02`、`ANCHOR-03` 的左右关系。
- 失败图不能进入 `base/` 的连续性参考，也不能被复制到下一张 prompt。

## 通过条件

- 回到 `spatial-anchor-ledger.md` 的 `scene-topology` 合同。
- 用上一张合格图或场景母版重生成。
- 重新检查父面、局部拓扑、镜位类别和 `EVID-*` 绑定。
