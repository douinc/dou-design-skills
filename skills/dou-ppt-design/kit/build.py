"""빌드: python3 build.py  →  <TITLE>.pptx (한 단계 위 폴더) + preview/index.html
EMBED_FONT=1 python3 build.py  → 파워포인트에서도 같은 글꼴이 보이게 글꼴을 파일에 심는다."""
import json, os, subprocess, sys
from engine import Icon, build
from icons import ICONS
import deck

HERE = os.path.dirname(os.path.abspath(__file__))
for fn in deck.BUILD:
    fn()

# 슬라이드에 쓴 아이콘 중 PNG 가 없는 것만 구워 둔다 (파워포인트에는 그림으로 들어간다)
need = {}
for s in deck.SLIDES:
    for it in s.items:
        if isinstance(it, Icon):
            if it.name not in ICONS:
                sys.exit(f"[오류] 없는 아이콘: {it.name}  (icons.py 목록에서 고르거나 추가)")
            out = os.path.join(HERE, "assets", "icons", f"{it.name}-{it.color.lstrip('#').lower()}.png")
            if not os.path.exists(out):
                need[out] = (ICONS[it.name], it.color)
if need:
    job = os.path.join(HERE, "preview", "_icons.json")
    os.makedirs(os.path.dirname(job), exist_ok=True)
    json.dump([{"out": o, "svg": v[0], "color": v[1]} for o, v in need.items()], open(job, "w"))
    subprocess.run(["node", os.path.join(HERE, "render.mjs"), "icons", job], check=True)

# 삽화: 정의가 바뀌었거나 PNG 가 없으면 다시 굽는다
import hashlib
from illustrations import ILLUSTRATIONS
stamp_path = os.path.join(HERE, "assets", ".illustrations.json")
stamps = json.load(open(stamp_path)) if os.path.exists(stamp_path) else {}
todo = []
for name, spec in ILLUSTRATIONS.items():
    h = hashlib.md5(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    out = os.path.join(HERE, "assets", f"{name}.png")
    if stamps.get(name) != h or not os.path.exists(out):
        todo.append({"out": out, **spec})
        stamps[name] = h
if todo:
    job = os.path.join(HERE, "preview", "_images.json")
    os.makedirs(os.path.dirname(job), exist_ok=True)
    json.dump(todo, open(job, "w"), ensure_ascii=False)
    subprocess.run(["node", os.path.join(HERE, "render.mjs"), "images", job], check=True)
    json.dump(stamps, open(stamp_path, "w"))

# 로고: assets/logos/*.svg 중 PNG 가 없거나 SVG 가 더 새것이면 원래 색·흰색 두 벌을 굽는다
logo_dir = os.path.join(HERE, "assets", "logos")
jobs = []
for fn in sorted(os.listdir(logo_dir)) if os.path.isdir(logo_dir) else []:
    if not fn.endswith(".svg"):
        continue
    src = os.path.join(logo_dir, fn)
    for white in (False, True):
        out = os.path.join(logo_dir, fn[:-4] + ("-white" if white else "") + ".png")
        if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
            jobs.append({"out": out, "svg": open(src, encoding="utf-8").read(), "white": white})
if jobs:
    job = os.path.join(HERE, "preview", "_logos.json")
    os.makedirs(os.path.dirname(job), exist_ok=True)
    json.dump(jobs, open(job, "w"), ensure_ascii=False)
    subprocess.run(["node", os.path.join(HERE, "render.mjs"), "logos", job], check=True)

os.makedirs(os.path.join(HERE, "preview"), exist_ok=True)
out_pptx = os.path.abspath(os.path.join(HERE, "..", f"{deck.TITLE}.pptx"))
build(deck.SLIDES, out_pptx, os.path.join(HERE, "preview", "index.html"), ICONS)
print(f"built {len(deck.SLIDES)} slides → {out_pptx}")
