#!/bin/bash
# 双击这个文件 → 核对引用、把 00_提交/ 重新分条、重建网站、开浏览器工作台。
# 改完 00_提交/ 里任何一份，双击一次就行。
# 用 /usr/bin/python3：anaconda 的 python3 曾经一启动就被杀（exit 137）。
cd "$(dirname "$0")" || exit 1

PY=/usr/bin/python3
PORT=8778          # Klein 的工作台占 8777，两边可以同时开

$PY sync.py --no-site || echo "⚠️ 同步报了问题（见上），网站照样重建，贴之前要修好"

echo
echo "▸ 重建网站并打开工作台"
cd 06_网站 || exit 1
$PY build_site.py || { echo "❌ 网站构建失败"; read -r -p "按回车关闭"; exit 1; }

if lsof -ti tcp:$PORT >/dev/null 2>&1; then
  echo "▸ 端口 $PORT 已有服务，直接用"
else
  $PY serve.py $PORT >/dev/null 2>&1 &
  sleep 1
fi

open "http://localhost:$PORT/index.html"

echo
echo "✅ http://localhost:$PORT/index.html"
echo "   这个终端窗口关掉，服务就停了。"
echo
read -r -p "按回车停止服务并关闭…"
lsof -ti tcp:$PORT | xargs kill 2>/dev/null
