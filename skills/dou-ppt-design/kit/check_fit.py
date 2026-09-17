"""글 상자보다 글이 넘치는 곳을 찾는다: python3 check_fit.py"""
import math
from engine import Text, Run
import deck

for fn in deck.BUILD:
    fn()


def cw(ch, size):
    o = ord(ch)
    if ch == " ": return size * 0.30
    if o < 0x2000: return size * 0.55
    if o < 0x2E80: return size * 0.45
    return size * 1.0


def paras_of(t):
    r = t.runs
    if isinstance(r, str): return [[Run(r)]]
    if not r: return []
    if all(isinstance(x, Run) for x in r): return [r]
    return [x if isinstance(x, list) else [x] for x in r]


rows = []
for i, s in enumerate(deck.SLIDES, 1):
    for t in s.items:
        if not isinstance(t, Text): continue
        ps = paras_of(t)
        if not ps: continue
        h = 0
        widest = 0
        for p in ps:
            wpx = sum(cw(c, r.size or t.size) for r in p for c in r.text)
            h += max(1, math.ceil(wpx / max(t.w, 1))) * (t.size * t.line)
        h += t.para_gap * max(0, len(ps) - 1)
        if h - t.h > 1:
            txt = " ".join(r.text for p in ps for r in p)[:40]
            rows.append((h - t.h, i, s.title[:18], txt))
for over, i, title, txt in sorted(rows, reverse=True):
    print(f"{over:>5.0f}px  {i:>2}장 {title:<18}  {txt}")
print(f"넘침 {len(rows)}건" if rows else "넘침 없음")
