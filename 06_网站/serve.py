#!/usr/bin/env python3
"""本地服务：静态文件 + 编辑存盘。

    python3 serve.py [端口]      # 默认 8778（Klein 的工作台占 8777）

比 `python3 -m http.server` 多两个接口，让网页上的编辑落到真文件上：

    GET  /api/edits   读 edits/store.json
    POST /api/edits   写 edits/store.json，并把每条线程导出成 edits/<线程>.md
    GET  /api/notes        读全部批注（批注/*.json）、people.json、以及「我是谁」
    POST /api/notes        新写一条批注 / 回复 / 已解决 / 重新打开（各存成一个新文件）
    POST /api/notes/sync   提交自己的批注 → git pull --rebase → git push

批注每条一个文件，三个人各写各的，git 合并时不会冲突。「我是谁」由本机 git config user.name
对上 people.json 里的 match 决定，认不出时网页里手动选。

网页每次改动 0.6 秒后自动 POST 一次。关浏览器、换端口、清缓存都不丢。
没起这个服务时（双击 index.html 或用线上链接），网页自动退回浏览器 localStorage。
"""
import datetime
import json
import re
import secrets
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
EDITS = HERE / "edits"
STORE = EDITS / "store.json"
API = "/api/edits"
MAX_BODY = 8 * 1024 * 1024
SAFE_NAME = re.compile(r"^[\w.-]+$")

NOTES_DIR = HERE / "批注"
PEOPLE = HERE / "people.json"
REPO = HERE.parent
NOTES_API, SYNC_API = "/api/notes", "/api/notes/sync"
NOTE_TYPES = {"note", "reply", "resolve", "reopen"}


def git(*args, timeout=60):
    try:
        r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)


def load_people():
    try:
        return json.loads(PEOPLE.read_text(encoding="utf-8")).get("people", [])
    except Exception:
        return []


def whoami(people):
    """本机 git 的 user.name 对上 people.json 的 match（只在本地比对，不存不传）。"""
    rc, name = git("config", "user.name", timeout=5)
    name = name.strip().lower() if rc == 0 else ""
    for p in people:
        if name and any(m.lower() == name or m.lower() in name for m in p.get("match", [])):
            return p.get("id")
    return None


def read_notes():
    out = []
    if NOTES_DIR.is_dir():
        for f in sorted(NOTES_DIR.glob("*.json")):
            try:
                out.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass
    return out


def write_note(d):
    if d.get("type") not in NOTE_TYPES:
        raise ValueError("type 只能是 note / reply / resolve / reopen")
    author = str(d.get("author") or "")
    if author not in {p.get("id") for p in load_people()}:
        raise ValueError("author 不在 people.json 里")
    now = datetime.datetime.now(datetime.timezone.utc)
    eid = f"{now:%Y%m%dT%H%M%SZ}_{author}_{secrets.token_hex(3)}"
    ev = {"id": eid, "type": d["type"], "author": author, "time": now.isoformat(timespec="seconds"),
          "thread": str(d.get("thread", ""))[:64], "key": str(d.get("key", ""))[:32],
          "quote": str(d.get("quote", ""))[:200], "text": str(d.get("text", ""))[:4000],
          "parent": str(d.get("parent", ""))[:80]}
    NOTES_DIR.mkdir(exist_ok=True)
    (NOTES_DIR / f"{eid}.json").write_text(json.dumps(ev, ensure_ascii=False, indent=1), encoding="utf-8")
    return ev


def sync_notes(me):
    """只提交 批注/ 目录，再 pull --rebase（自动暂存别的改动）和 push。"""
    log = []
    rel = str(NOTES_DIR.relative_to(REPO))
    NOTES_DIR.mkdir(exist_ok=True)
    git("add", "--", rel)
    rc, _ = git("diff", "--cached", "--quiet", "--", rel)
    if rc == 1:
        rc, out = git("commit", "-m", f"notes: annotations by {me or 'unknown'}", "--", rel)
        log.append(out)
        if rc:
            return False, log
    rc, out = git("pull", "--rebase", "--autostash", timeout=120)
    log.append(out)
    if rc:
        return False, log
    rc, out = git("push", timeout=120)
    if rc:
        rc, out = git("push", "-u", "origin", "HEAD", timeout=120)
    log.append(out)
    return rc == 0, log


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

    def _route(self):
        return self.path.split("?")[0].rstrip("/")

    def _is_api(self):
        return self._route() == API

    def do_GET(self):
        if self._route() == NOTES_API:
            people = load_people()
            return self._json(200, {"me": whoami(people), "people": people, "events": read_notes()})
        if not self._is_api():
            return super().do_GET()
        try:
            return self._json(200, json.loads(STORE.read_text(encoding="utf-8")))
        except FileNotFoundError:
            return self._json(200, {})
        except Exception as e:
            return self._json(200, {"__error": f"store.json 读不动：{e}"})

    def do_POST(self):
        if self._route() == SYNC_API:
            ok, log = sync_notes(whoami(load_people()))
            return self._json(200 if ok else 500, {"ok": ok, "log": [x for x in log if x]})
        if self._route() == NOTES_API:
            try:
                n = int(self.headers.get("Content-Length") or 0)
                d = json.loads(self.rfile.read(n).decode("utf-8")) if 0 < n <= 64 * 1024 else None
                if not isinstance(d, dict):
                    return self._json(400, {"error": "body 必须是 object"})
                return self._json(200, {"ok": True, "event": write_note(d)})
            except Exception as e:
                return self._json(400, {"error": str(e)})
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
