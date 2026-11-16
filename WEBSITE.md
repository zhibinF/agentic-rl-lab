## 在线阅读网站

个人站点：https://zhibinf.github.io/agentic-rl-lab/

网站使用 MkDocs Material，从仓库现有 Markdown 生成，不需要安装训练依赖。

```bash
python -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt
python scripts/prepare_docs.py
.venv-docs/bin/mkdocs build --strict
.venv-docs/bin/mkdocs serve
```

`scripts/prepare_docs.py` 将文档和引用的图片复制到临时 `.docs/` 目录，转换 README 路由并适配链接。原始教程保持不变。中文首页位于站点根目录，英文首页位于 `en/`，实验章节位于 `experiments/<name>/`。代码链接指向 fork 的 GitHub 源文件。

GitHub Settings → Pages 的发布来源为 `gh-pages` 分支根目录。更新网站时，在已安装文档依赖的环境中执行：

```bash
python scripts/prepare_docs.py
.venv-docs/bin/mkdocs build --strict
.venv-docs/bin/mkdocs gh-deploy --force
```

当前发布凭证不含 GitHub OAuth 的 workflow scope，因此采用分支发布，不添加无法推送的 Actions 工作流。上述命令仅更新生成网站的 gh-pages 分支，教程源码仍位于 main。
