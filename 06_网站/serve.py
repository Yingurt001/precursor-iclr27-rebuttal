#!/usr/bin/env python3
"""本地服务：静态文件 + 编辑存盘。

    python3 serve.py [端口]      # 默认 8778（Klein 的工作台占 8777）

比 `python3 -m http.server` 多两个接口，让网页上的编辑落到真文件上：

    GET  /api/edits   读 edits/store.json
    POST /api/edits   写 edits/store.json，并把每条线程导出成 edits/<线程>.md

网页每次改动 0.6 秒后自动 POST 一次。关浏览器、换端口、清缓存都不丢。
没起这个服务时（双击 index.html 或用线上链接），网页自动退回浏览器 localStorage。
"""
import json
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
EDITS = HERE / "edits"
STORE = EDITS / "store.json"
API = "/api/edits"
MAX_BODY = 8 * 1024 * 1024
SAFE_NAME = re.compile(r"^[\w.-]+$")


def write_markdown_mirror(data: dict) -> None:
    """除了 store.json，再按线程写一份可读 markdown，方便直接复制回 00_提交/。"""
    for tid, v in data.items():
        if not isinstance(v, dict) or not SAFE_NAME.match(str(tid)):
            continue
        posts = v.get("posts")
        if not isinstance(posts, list):
            continue
        done = v.get("done") or []
        n = len(posts)
        out = [f"# {tid} · 网页工作台编辑版", "",
               f"> 由 06_网站 自动保存，共 {n} 条。**不要手改这个文件**，它每次编辑都会被覆盖。", ""]
        for i, p in enumerate(posts):
            p = p if isinstance(p, str) else ""
            flag = "  ✅ 已发" if i < len(done) and done[i] else ""
            over = "  ⚠️ 超 5000 字符" if len(p) > 5000 else ""
            out += ["---", "", f"## 第 {i + 1}/{n} 条 · {len(p)} 字符{flag}{over}", "",
                    ">>>>> COPY FROM HERE", "", p, "", "<<<<< COPY TO HERE", ""]
        (EDITS / f"{tid}.md").write_text("\n".join(out), encoding="utf-8")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(HERE), **kw)

    def _json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _is_api(self):
        return self.path.split("?")[0].rstrip("/") == API

    def do_GET(self):
        if not self._is_api():
            return super().do_GET()
        try:
            return self._json(200, json.loads(STORE.read_text(encoding="utf-8")))
        except FileNotFoundError:
            return self._json(200, {})
        except Exception as e:
            return self._json(200, {"__error": f"store.json 读不动：{e}"})

    def do_POST(self):
        if not self._is_api():
            return self._json(404, {"error": "no such endpoint"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return self._json(400, {"error": "bad Content-Length"})
        if n <= 0 or n > MAX_BODY:
            return self._json(413, {"error": "body 为空或过大"})
        try:
            data = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception as e:
            return self._json(400, {"error": str(e)})
        if not isinstance(data, dict):
            return self._json(400, {"error": "顶层必须是 object"})

        EDITS.mkdir(exist_ok=True)
        tmp = STORE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(STORE)                       # 原子替换，中途挂掉不会剩半个文件
        try:
            write_markdown_mirror(data)
        except Exception as e:
            return self._json(200, {"ok": True, "warn": f"markdown 镜像失败：{e}"})
        return self._json(200, {"ok": True})

    def log_message(self, *args):
        pass                                      # 别把每个请求都刷到终端上


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8778
    EDITS.mkdir(exist_ok=True)
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"▸ http://localhost:{port}/index.html")
    print(f"▸ 编辑存到 {STORE}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
