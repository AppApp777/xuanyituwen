# 贡献指南

感谢参与 `xuanyituwen`。这个项目的重点不是堆叠更长的提示词，而是让悬疑图文的因果、证据和视觉连续性可以被复盘。

## 提交前检查

先创建 Python 3.9 或更高版本的虚拟环境：

~~~bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
~~~

然后运行：

~~~bash
python -m json.tool evals/evals.json > /dev/null
python -m py_compile scripts/normalize_raster.py scripts/validate_artifact_package.py
python scripts/validate_artifact_package.py examples/cat-eye-person --strict
python -m pytest
~~~

提交前请确认：

- 没有个人聊天记录、账号信息、API 密钥或未授权素材。
- 修改了主流程时，也同步更新对应的 references 文件和 README。
- 新增规则说明了它解决的具体失败模式。
- 修改输出合同时，同时新增或更新一个 `evals/fixtures/` 夹具和机器断言。
- 任何示例图、字体、声音和文本都有明确的使用权。
- 第一人称发布配文仍然独立于图片，不把文字重新嵌回底图。

## 适合提交的问题

- 角色、场景或关键物件在连续图中发生了可复现的漂移。
- 伏笔在前文没有公平埋设，或结尾没有回收。
- 信息权限越界，角色使用了自己不可能知道的内容。
- `captions.md` 与画面事实不一致。
- 归一化脚本在特殊输入比例、透明通道或边界尺寸下失败。
- 产物包的 `FRAME-*`、`EVID-*`、图片、prompt 或配文绑定不一致。

## 提交方式

请先创建 issue 描述问题和复现条件，再提交小而集中的 pull request。不要把生成图片、个人素材或整个评测工作区提交进仓库。
