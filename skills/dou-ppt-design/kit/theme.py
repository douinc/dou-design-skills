"""공통 디자인 토큰과 레이아웃 조각."""
from engine import Rect, Text, Line, Icon, Image, Run, runs, fs, W, H

# ---- 색
PRIMARY = "#4083F7"
PRIMARY_DK = "#2F66D6"
NAVY = "#0F1B3D"
INK = "#1A2233"
MUTED = "#5B6472"
LIGHT = "#8A94A6"
BORDER = "#E3E8F0"
CARD = "#F5F7FA"
TINT = "#EDF3FE"
TINT2 = "#D9E6FD"
ORANGE = "#F97316"
ORANGE_T = "#FFF3E8"
GREEN = "#16A34A"
GREEN_T = "#EAF7EE"
RED = "#DC2626"
RED_T = "#FDECEC"
WHITE = "#FFFFFF"
# ---- 브랜드 색 (회사 구분에만 쓴다)
DOU = "#1E77E0"        # 도우 공식 블루 (logo-dou.svg)
DOU_T = "#E9F1FC"      # 도우 옅은 배경

ICON_COLORS = [PRIMARY, NAVY, MUTED, ORANGE, GREEN, RED, WHITE, LIGHT, "#6FA2FF", "#FF9B6B", "#9BC4FF", TINT2, "#C4CEDD", DOU]

MX = 64  # 좌우 여백
CONTENT_TOP = 158
CONTENT_BOTTOM = 664
FOOT = "주식회사 도우"  # deck.py 에서 theme.FOOT = "..." 로 바꾼다


def header(label: str, title, subtitle: str = "", ref: str = ""):
    """섹션 라벨 + 제목 + 부제 + 우상단 제안서 참조."""
    items = [
        Rect(MX, 46, 3, 14, fill=PRIMARY),
        Text(MX + 11, 43, 600, 20, label, size=12, color=PRIMARY, weight=700, letter=0.5),
        Text(MX, 66, 1000, 46, title, size=32, color=NAVY, weight=700, line=1.2),
    ]
    if subtitle:
        items.append(Text(MX, 112, 1010, 46, subtitle, size=15, color=MUTED, line=1.4))
    if ref:
        items.append(Text(W - MX - 470, 46, 470, 20, ref, size=10, color=LIGHT, align="right"))
    return items


def _foot():
    import theme
    return theme.FOOT


def footer(n: int, total: int = 0):
    return [
        Line(MX, 676, W - MX, 676, color=BORDER, w=1),
        Text(MX, 684, 800, 16, _foot(), size=10, color=LIGHT),
        Text(W - MX - 120, 684, 120, 16, f"{n:02d}", size=10, color=LIGHT, align="right", weight=700),
    ]


def pill(x, y, text, fill=TINT, color=PRIMARY, size=12, w=None, h=24, bold=True, stroke=None):
    w = w or (len(text) * fs(size) * 0.98 + 24)
    return [
        Rect(x, y, w, h, fill=fill, radius=h / 2, stroke=stroke),
        Text(x, y, w, h, text, size=size, color=color, weight=700 if bold else 500, align="center", valign="middle", line=1),
    ]


def card(x, y, w, h, fill=CARD, radius=14, stroke=None, shadow=False):
    return Rect(x, y, w, h, fill=fill, radius=radius, stroke=stroke, shadow=shadow)


def icon_badge(x, y, name, size=44, bg=TINT, color=PRIMARY, radius=12):
    ic = size * 0.55
    return [
        Rect(x, y, size, size, fill=bg, radius=radius),
        Icon(name, x + (size - ic) / 2, y + (size - ic) / 2, ic, color),
    ]


def photo_placeholder(x, y, w, h, label):
    """사진 자리 — 점선 빈칸 + 카메라 아이콘 + 안내 문구."""
    return [
        Rect(x, y, w, h, fill="#FAFBFD", radius=12, stroke="#B9C4D6", stroke_w=1.5, dash=True),
        Icon("camera", x + w / 2 - 14, y + h / 2 - 26, 28, LIGHT),
        Text(x + 12, y + h / 2 + 6, w - 24, 22, label, size=12, color=LIGHT, align="center", weight=500),
    ]


def nlines(text, w, size, bump=1.2):
    """실제 렌더 줄 수. 글자 수로 어림잡지 말고 이걸 쓴다."""
    import math
    sz = size + bump
    px = 0.0
    for ch in str(text):
        o = ord(ch)
        px += sz * (0.30 if ch == " " else 0.55 if o < 0x2000 else 0.45 if o < 0x2E80 else 1.0)
    return max(1, math.ceil(px / max(w, 1)))


def bullet(x, y, w, text, size=13, color=INK, dot=PRIMARY, line=1.45, h=None):
    """작은 점 + 한 줄 텍스트(런 리스트 가능)."""
    h = h or size * line + 2
    return [
        Rect(x, y + size * line / 2 - 2.5, 5, 5, fill=dot, shape="ellipse"),
        Text(x + 14, y, w - 14, h, text, size=size, color=color, line=line),
    ]


def numbered(x, y, n, size=26, bg=NAVY, color=WHITE, fs=12):
    return [
        Rect(x, y, size, size, fill=bg, shape="ellipse"),
        Text(x, y, size, size, str(n), size=fs, color=color, weight=700, align="center", valign="middle", line=1),
    ]


def table(x, y, w, cols, rows, head_h=30, row_h=34, size=12, head_fill=CARD, head_color=MUTED,
          zebra=False, col_align=None, row_lines=True, bold_first=False, cell_color=INK, row_hs=None,
          cell_valign="middle", head_colors=None):
    """가벼운 표 — 도형+텍스트로 그려 슬라이드에서 바로 편집 가능.
    cols: [(label, width_ratio)] ; rows: list of list[str|runs]"""
    items = []
    total = sum(c[1] for c in cols)
    xs = [x]
    for c in cols:
        xs.append(xs[-1] + w * c[1] / total)
    col_align = col_align or ["left"] * len(cols)
    items.append(Rect(x, y, w, head_h, fill=head_fill, radius=6))
    for i, (label, _) in enumerate(cols):
        hc = (head_colors[i] if head_colors and i < len(head_colors) and head_colors[i] else head_color)
        items.append(Text(xs[i] + 10, y, xs[i + 1] - xs[i] - 20, head_h, label, size=size - 1, color=hc, weight=700, valign="middle", align=col_align[i], line=1.2))
    cy = y + head_h
    for r, row in enumerate(rows):
        rh = (row_hs[r] if row_hs else row_h)
        if zebra and r % 2 == 1:
            items.append(Rect(x, cy, w, rh, fill="#FAFBFD"))
        for i, cell in enumerate(row):
            wt = 700 if (bold_first and i == 0) else 400
            items.append(Text(xs[i] + 10, cy + (6 if cell_valign == "top" else 0), xs[i + 1] - xs[i] - 20, rh - (6 if cell_valign == "top" else 0), cell, size=size, color=cell_color, weight=wt, valign=cell_valign, align=col_align[i], line=1.3))
        cy += rh
        if row_lines:
            items.append(Line(x, cy, x + w, cy, color=BORDER, w=1))
    return items, cy


def stat(x, y, w, value, unit, label, color=NAVY, vsize=34, align="left"):
    return [
        Text(x, y, w, vsize + 8, runs((value, {"bold": True, "size": vsize, "color": color}), (" " + unit, {"size": 13, "color": MUTED, "weight": 500})), size=vsize, color=color, line=1.1, valign="bottom", align=align),
        Text(x, y + vsize + 12, w, 36, label, size=12, color=MUTED, line=1.35, align=align),
    ]
