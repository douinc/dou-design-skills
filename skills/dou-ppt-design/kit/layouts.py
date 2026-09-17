"""자주 쓰는 장 구성 — 표지 · 목차 · 간지 · 맺음 · 숫자 요약 · 조직도 · 앱/웹 화면 자리.

모든 함수는 이미 만든 Slide 에 요소를 붙인다. 좌표는 1280×720 px 기준.
"""
from engine import Rect, Text, Line, Image, runs, paras, W, H
from theme import *  # noqa


def cover(s, title, subtitle="", label="", meta=(), org_line="주식회사 도우", accent=""):
    """표지 — 위 흰 바탕에 제목, 아래 파란 띠에 회사명과 기본 정보.
    title 안의 accent 문구만 파란색으로 칠한다.
    meta: [("사업기간", "2026. 10. ~ 12."), ...] 최대 3개 — 띠 맨 아래 한 줄에 깔린다."""
    s.balance = False
    if accent and accent in title:
        a, b = title.split(accent, 1)
        head = paras((a, (accent, {"color": PRIMARY}), b))
    else:
        head = title
    s.add(Image("hero.png", 0, 300, W, 460))
    if label:
        s.add(pill(MX, 56, label, fill=TINT, color=PRIMARY, size=12, h=26))
    s.add(Text(MX, 104, 960, 64, head, size=42, color=NAVY, weight=700, line=1.25),
          Image("logo-dou.png", W - MX - 61, 58.5, 61, 26.7, name="logo-dou"))
    if subtitle:
        s.add(Text(MX, 168, 960, 40, subtitle, size=17, color=MUTED, line=1.4, weight=500))
    s.add(Text(MX, 422, 900, 40, org_line, size=25, color=WHITE, weight=700, line=1.25))
    if meta:
        s.add(Line(MX, 620, W - MX, 620, color=WHITE, w=1))
        cw = (W - 2 * MX) / len(meta)
        for i, (k, v) in enumerate(meta):
            al = "left" if i == 0 else ("right" if i == len(meta) - 1 and len(meta) > 1 else "center")
            s.add(Text(MX + i * cw, 632, cw, 40, paras(k, (v, {"bold": True})), size=12, color=WHITE, line=1.4, align=al))


def agenda(s, sections, n, note=""):
    """목차 — sections: [("01", "사업 이해", "UNDERSTANDING"), ...] 최대 6개."""
    s.add(header("AGENDA", "발표 순서"))
    top = 154
    rh = min(110, 470 / max(len(sections), 1))  # 섹션이 적으면 줄 간격을 넓혀 아래가 비지 않게
    for i, (no, title, tag) in enumerate(sections):
        y = top + i * rh
        y += (rh - 78) / 2
        s.add(Text(MX, y, 52, 42, no, size=17, color=PRIMARY, weight=700, valign="middle", line=1),
              Text(MX + 62, y, 640, 42, title, size=23, color=NAVY, weight=700, valign="middle", line=1.2),
              Text(W - MX - 420, y, 420, 42, tag, size=11.5, color=LIGHT, weight=500, align="right", valign="middle", letter=0.5, line=1),
              Line(MX, y + 58, W - MX, y + 58, color=BORDER, w=1))
    if note:
        s.add(Text(MX, top + len(sections) * rh + 4, W - 2 * MX, 20, note, size=11.5, color=MUTED, valign="middle"))
    s.add(footer(n))


def divider(s, sections, idx, n):
    """섹션 간지 — 목차를 다시 띄우고 지금 섹션만 크게 강조."""
    s.balance = False
    no = sections[idx][0]
    s.add(Rect(MX, 46, 3, 14, fill=PRIMARY),
          Text(MX + 11, 43, 600, 20, "AGENDA", size=12, color=PRIMARY, weight=700, letter=0.5),
          Text(W - MX - 200, 43, 200, 20, runs((no, {"bold": True, "color": NAVY}), (f" / {len(sections):02d}", {"color": LIGHT})),
               size=12, align="right", valign="middle", line=1))
    y = 168
    for i, (num, t, g) in enumerate(sections):
        on = i == idx
        rh = 92 if on else 66
        if on:
            s.add(Rect(MX - 18, y + 4, W - 2 * MX + 36, rh - 8, fill=TINT, radius=14))
        s.add(Text(MX, y, 60, rh, num, size=20 if on else 14, color=PRIMARY if on else "#C6D0DE", weight=700, valign="middle", line=1),
              Text(MX + 72, y, 700, rh, t, size=34 if on else 19, color=NAVY if on else "#A6B1C2", weight=700, valign="middle", line=1.2),
              Text(W - MX - 440, y, 420, rh, g, size=12.5 if on else 11, color=PRIMARY if on else "#C6D0DE",
                   weight=500, align="right", valign="middle", letter=0.5, line=1))
        y += rh
    s.add(footer(n))


def closing(s, points, summary, sign="주식회사 도우", sub=""):
    """맺음 — 파란 전면 배경, 왼쪽 약속 목록(아이콘, 문장), 오른쪽 흰 카드 요약 + 감사합니다.
    points: [("check-circle", "문장"), ...] 최대 7개. summary: paras(...) 또는 문자열."""
    s.balance = False
    s.add(Image("hero-wide.png", 0, 0, W, H), Rect(0, 0, W, H, fill=NAVY, opacity=0.12),
          Rect(MX, 50, 3, 14, fill=WHITE),
          Text(MX + 11, 47, 600, 20, "CLOSING", size=12, color=WHITE, weight=700, letter=0.5),
          Text(MX, 76, 1000, 50, "맺음", size=34, color=WHITE, weight=700, line=1.2))
    k = len(points)
    step = 52 if k >= 6 else 62
    y = 146 + (440 - (k * step - 8)) / 2           # 약속이 적으면 카드 높이 안에서 가운데로
    for ic, t in points:
        s.add(Rect(MX, y, 700, step - 8, fill=WHITE, radius=10, opacity=0.14),
              Icon(ic, MX + 14, y + (step - 8) / 2 - 10, 20, WHITE),
              Text(MX + 46, y, 640, step - 8, t, size=12.5, color=WHITE, valign="middle", line=1.35))
        y += step
    rx = MX + 730
    rw = W - MX - rx
    s.add(Rect(rx, 146, rw, 440, fill=WHITE, radius=16),
          Text(rx + 26, 176, rw - 52, 22, "요약", size=12, color=PRIMARY, weight=700),
          Text(rx + 26, 206, rw - 52, 300, summary, size=16, color=NAVY, weight=500, line=1.6, para_gap=14),
          Line(rx + 26, 506, rx + rw - 26, 506, color=BORDER, w=1),
          Text(rx + 26, 522, rw - 52, 40, "감사합니다.", size=24, color=NAVY, weight=700, valign="middle"))
    s.add(Text(MX, 600, 700, 20, sign, size=13, color=WHITE, weight=700))
    if sub:
        s.add(Text(MX, 624, 900, 20, sub, size=11.5, color="#DCE8FD"))


def stat_row(s, y, items, h=74):
    """숫자 요약 줄 — items: [("25.2", "M/M", "설명"), ...] 2~5개, 회색 카드."""
    gap = 16
    sw = (W - 2 * MX - (len(items) - 1) * gap) / len(items)
    for i, (v, u, l) in enumerate(items):
        x = MX + i * (sw + gap)
        s.add(Rect(x, y, sw, h, fill=CARD, radius=12),
              Text(x + 18, y + 12, sw - 36, 36, runs((v, {"bold": True, "size": 26}), (" " + u, {"size": 11, "color": MUTED})),
                   size=26, color=NAVY, line=1.1, valign="bottom"),
              Text(x + 18, y + 48, sw - 36, 18, l, size=10.5, color=MUTED))
    return y + h


def org_chart(s, head, members, top=166, bottom=650, logo=True):
    """조직도 — 왼쪽 남색 대표 카드, 오른쪽 구성원 줄. 선만으로 연결(점·강조 없음).
    head: (이름, 직책, 한 줄 역할)
    members: [(이름, 직책, 전문분야, 경력, 담당), ...] 3~6명"""
    name, role, desc = head
    cw, ch = 300, 170
    cy = (top + bottom) / 2 - ch / 2
    s.add(Rect(MX, cy, cw, ch, fill=NAVY, radius=16))
    if logo:
        s.add(Image("logo-dou-white.png", MX + 26, cy + 26, 55, 24, name="logo-dou"))
    s.add(Text(MX + 26, cy + 62, cw - 52, 40, runs((name, {"bold": True, "size": 26}), ("  " + role, {"size": 14, "color": "#B7C6E6", "weight": 500})),
               size=26, color=WHITE, line=1.2, valign="bottom"),
          Text(MX + 26, cy + 112, cw - 52, 30, desc, size=14, color=WHITE, weight=500, valign="middle"))
    k = len(members)
    gap = 14
    rh = (bottom - top - gap * (k - 1)) / k
    spine = MX + cw + 48
    mx = spine + 40
    mw = W - MX - mx
    lc = "#C4CEDD"
    s.add(Line(MX + cw, cy + ch / 2, spine, cy + ch / 2, color=lc, w=2),
          Line(spine, top + rh / 2, spine, top + (k - 1) * (rh + gap) + rh / 2, color=lc, w=2))
    for i, (nm, rl, field, career, prod) in enumerate(members):
        y = top + i * (rh + gap)
        s.add(Line(spine, y + rh / 2, mx, y + rh / 2, color=lc, w=2),
              Rect(mx, y, mw, rh, fill=CARD, radius=14),
              Rect(mx, y + 18, 4, rh - 36, fill=lc, radius=2),
              Text(mx + 28, y, 180, rh, nm, size=20, color=NAVY, weight=700, valign="middle"),
              pill(mx + 112, y + rh / 2 - 12, rl, fill=WHITE, color=MUTED, size=11, w=64, h=24),
              Line(mx + 200, y + 22, mx + 200, y + rh - 22, color=BORDER, w=1),
              Text(mx + 224, y + rh / 2 - 34, mw - 250, 28, runs((field, {"bold": True, "color": INK}), ("   " + career, {"color": MUTED, "size": 12})), size=14, valign="middle"),
              Text(mx + 224, y + rh / 2 + 6, mw - 250, 28, runs(("담당  ", {"bold": True, "color": PRIMARY, "size": 12}), (prod, {"color": INK})), size=14, valign="middle"))


# ---------------------------------------------------------------- 앱·웹 화면 자리
PHONE_RATIO = 19.5 / 9  # 세로 / 가로 (요즘 휴대폰 화면 비율)


def phone_slot(x, y, w, label="앱 화면", image=None):
    """휴대폰 화면 자리. image 가 없으면 점선 빈칸 + 라벨, 있으면 그 이미지를 넣는다.
    image 는 assets/ 에 넣은 캡처 파일명 (세로 19.5:9 비율 권장). 높이는 w 로 자동."""
    h = w * PHONE_RATIO
    items = [Rect(x - 6, y - 6, w + 12, h + 12, fill=WHITE, radius=30, stroke="#D5DCE8", stroke_w=1.5)]
    if image:
        items.append(Image(image, x, y, w, h, name=f"app:{label}"))
    else:
        items += [Rect(x, y, w, h, fill="#F7F9FC", radius=24, stroke="#B9C4D6", stroke_w=1.5, dash=True, name=f"자리:{label}"),
                  Icon("smartphone", x + w / 2 - 13, y + h / 2 - 30, 26, LIGHT),
                  Text(x + 8, y + h / 2 + 4, w - 16, 40, label, size=12, color=LIGHT, weight=500, align="center", line=1.35)]
    return items, h


def browser_slot(x, y, w, h, label="웹 화면", image=None):
    """웹(PC) 화면 자리 — 위에 창 막대가 있는 틀."""
    bar = 26
    items = [Rect(x, y, w, h, fill=WHITE, radius=12, stroke="#D5DCE8", stroke_w=1.5),
             Rect(x + 1, y + 1, w - 2, bar, fill="#F1F4F9", radius=11),
             Rect(x + 1, y + bar - 8, w - 2, 8, fill="#F1F4F9")]
    for i in range(3):
        items.append(Rect(x + 14 + i * 13, y + bar / 2 - 4, 8, 8, fill="#D5DCE8", shape="ellipse"))
    iy, ih = y + bar + 1, h - bar - 2
    if image:
        items.append(Image(image, x + 1, iy, w - 2, ih, name=f"web:{label}"))
    else:
        items += [Rect(x + 12, iy + 10, w - 24, ih - 20, fill="#F7F9FC", radius=8, stroke="#B9C4D6", stroke_w=1.5, dash=True, name=f"자리:{label}"),
                  Icon("monitor", x + w / 2 - 13, iy + ih / 2 - 30, 26, LIGHT),
                  Text(x + 20, iy + ih / 2 + 4, w - 40, 24, label, size=12, color=LIGHT, weight=500, align="center")]
    return items


def app_flow(s, steps, top=CONTENT_TOP + 6, bottom=648):
    """앱 흐름 — 휴대폰 화면 3~5개를 화살표로 잇고 아래에 단계 번호·제목·설명.
    steps: [(제목, 설명, 이미지파일 또는 None), ...]"""
    k = len(steps)
    text_h = 78
    gap = 56                                  # 화살표 자리
    ph = bottom - top - text_h - 12
    pw = min(ph / PHONE_RATIO, (W - 2 * MX - gap * (k - 1)) / k - 12)
    ph = pw * PHONE_RATIO
    col = (W - 2 * MX - gap * (k - 1)) / k
    for i, (title, desc, img) in enumerate(steps):
        cx = MX + i * (col + gap)
        px = cx + (col - pw) / 2
        items, _ = phone_slot(px, top + 6, pw, f"{i + 1}. {title}", img)
        s.add(items)
        ty = top + 6 + ph + 18
        s.add(numbered(cx + (col - 180) / 2, ty, i + 1, size=22, bg=PRIMARY, fs=11),
              Text(cx + (col - 180) / 2 + 30, ty - 2, 180, 26, title, size=14, color=NAVY, weight=700, valign="middle"),
              Text(cx, ty + 28, col, 40, desc, size=11.5, color=MUTED, line=1.4, align="center"))
        if i < k - 1:
            s.add(Icon("arrow-right", cx + col + gap / 2 - 12, top + 6 + ph / 2 - 12, 24, PRIMARY))


def app_callouts(s, image, label, points, top=CONTENT_TOP + 6, bottom=648, side="left"):
    """화면 한 장 설명 — 휴대폰 하나 + 번호 붙은 설명 목록.
    points: [(제목, 설명, 화면 위 표시 y비율 0~1 또는 None), ...] 3~5개.
    y비율을 주면 화면 위에 같은 번호 동그라미를 찍어 어느 부분인지 짚는다."""
    ph = bottom - top - 12
    pw = ph / PHONE_RATIO
    px = MX + 90 if side == "left" else W - MX - 90 - pw
    items, _ = phone_slot(px, top + 6, pw, label, image)
    s.add(items)
    lx = px + pw + 90 if side == "left" else MX
    lw = (W - MX - lx) if side == "left" else (px - 90 - MX)
    k = len(points)
    rh = min(112, (bottom - top) / k)
    y0 = top + (bottom - top - rh * k) / 2
    for i, (t, d, yr) in enumerate(points):
        y = y0 + i * rh
        s.add(numbered(lx, y + 4, i + 1, size=28, bg=PRIMARY, fs=13),
              Text(lx + 44, y, lw - 44, 34, t, size=17, color=NAVY, weight=700, valign="middle"),
              Text(lx + 44, y + 36, lw - 44, rh - 48, d, size=12.5, color=MUTED, line=1.5))
        if i < k - 1:
            s.add(Line(lx + 44, y + rh - 8, lx + lw, y + rh - 8, color=BORDER))
        if yr is not None:
            my = top + 6 + ph * yr
            edge = px + pw if side == "left" else px
            s.add(Line(edge - 10, my, edge + (24 if side == "left" else -24), my, color=PRIMARY, w=1.5),
                  numbered(edge - 22 if side == "left" else edge - 2, my - 12, i + 1, size=24, bg=PRIMARY, fs=11))
