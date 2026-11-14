#!/bin/bash
# 双击这个文件 → 用最新的 00_提交/ 内容重建网站，起本地服务，开浏览器。
# 关掉终端窗口 = 关掉服务。
cd "$(dirname "$0")" || exit 1

PY=/usr/bin/python3
PORT=8778

echo "▸ 重建网站（读取 ../00_提交/ 和 ../REVIEWS.md）"
$PY build_site.py || { echo "构建失败"; read -r -p "按回车关闭"; exit 1; }

if lsof -ti tcp:$PORT >/dev/null 2>&1; then
  echo "▸ 端口 $PORT 已有服务，直接用"
else
  echo "▸ 起本地服务（带存盘）http://localhost:$PORT"
  $PY serve.py $PORT >/dev/null 2>&1 &
  sleep 1
fi

open "http://localhost:$PORT/index.html"

echo
echo "✅ 已打开 http://localhost:$PORT/index.html"
echo "   这个终端窗口关掉，服务就停了。"
echo
read -r -p "按回车停止服务并关闭…"
lsof -ti tcp:$PORT | xargs kill 2>/dev/null
