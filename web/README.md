# 网页版工作台（Vercel）

三个人不用 git，打开网址就能改回复稿、写批注。数据仍在这个 GitHub 仓库里，和本地 `00_提交/*.md`、`06_网站/批注/` 是同一份。

- `api/data.js`：登录后返回全部回复稿和批注（每次从 GitHub 现读）。
- `api/post.js`：保存一份回复稿。先读 GitHub 上的最新版，按条合并别人同时的改动，再提交；提交作者是「名字（网页）」。
- `api/notes.js`：写一条批注，一条一个文件。
- `api/_lib.js`：口令、GitHub 读写、md 分条文件的解析与重建（格式与 `sync.py` 一致）、合并规则。
- `index.html`、`api/_static.js`：由 `06_网站/build_site.py` 生成（跑 `sync.py` 时自动更新），不进 git。页面里不含任何稿件内容和论文信息，登录后才取。

需要的两个环境变量（只在 Vercel 上，不进仓库）：`GITHUB_TOKEN`（只对本仓库有 Contents 读写权限的 fine-grained token）、`PASSCODE`（共用口令）。

部署：`/usr/bin/python3 sync.py` → `cd web && vercel deploy --prod`。
