"""로고 파일에서 CI 색을 뽑는다: python3 brand_color.py <로고.svg|png|jpg>
흰색·검정·회색은 빼고 가장 넓게 쓰인 색을 대표색으로 고른다. 결과는 theme.brand() 에 넣어 쓴다."""
import colorsys, re, sys
from collections import Counter


def neutral(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return s < 0.18 or l > 0.93 or l < 0.08


def from_svg(path):
    t = open(path, encoding="utf-8").read()
    cols = re.findall(r'(?:fill|stroke|stop-color)\s*[:=]\s*"?\s*#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b', t)
    c = Counter()
    for h in cols:
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        c[h.upper()] += 1
    return [(n, tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))) for h, n in c.most_common()]


def from_raster(path):
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    im.thumbnail((200, 200))
    c = Counter()
    px = im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()
    for r, g, b, a in px:
        if a < 200:
            continue
        c[(r // 12 * 12, g // 12 * 12, b // 12 * 12)] += 1
    return [(n, rgb) for rgb, n in c.most_common()]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("사용법: python3 brand_color.py <로고 파일>")
    p = sys.argv[1]
    found = from_svg(p) if p.lower().endswith(".svg") else from_raster(p)
    picks = [(n, rgb) for n, rgb in found if not neutral(*rgb)]
    if not picks:
        sys.exit("무채색(흰색·검정·회색)만 있는 로고입니다 — 사용자에게 CI 색을 물어보세요.")
    total = sum(n for n, _ in picks)
    from theme import brand
    print("후보 (많이 쓰인 순):")
    for n, rgb in picks[:5]:
        print(f"  #{''.join(f'{v:02X}' for v in rgb)}  {n / total:.0%}")
    main = "#" + "".join(f"{v:02X}" for v in picks[0][1])
    fill, text, tint = brand(main)
    print(f"\nbrand(\"{main}\") → 채움 {fill} · 글자 {text} · 옅은 배경 {tint}")
