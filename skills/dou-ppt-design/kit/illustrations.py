"""삽화 정의 — 화면 코드(SVG 또는 HTML)로 그리고 build.py 가 PNG 로 구워 assets/ 에 넣는다.
슬라이드에서는  Image("<이름>.png", x, y, w, h)  로 쓴다.
내용이 바뀌면 다음 빌드 때 자동으로 다시 굽는다."""
from theme import PRIMARY, PRIMARY_DK, NAVY, INK, MUTED, LIGHT, BORDER, CARD, TINT, TINT2, ORANGE, WHITE  # noqa

FONT_CSS = "<defs><style>.t{font-family:'Noto Sans KR';font-weight:700}.r{font-family:'Noto Sans KR'}</style></defs>"


def scene(inner, w=320, h=180, bg=True):
    """옅은 파란 둥근 판 위에 도형을 올리는 기본 틀. 좌표는 w×h 기준."""
    base = f'<rect width="{w}" height="{h}" rx="16" fill="{TINT}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{FONT_CSS}{base}{inner}</svg>'


# ---- 예시: 흩어진 기록 → 하나로 정리 (지워도 되는 견본)
EXAMPLE = scene(f"""
<g transform="translate(28,40)">
  <rect x="8" y="8" width="70" height="92" rx="8" fill="#fff" stroke="{TINT2}" transform="rotate(-8 43 54)"/>
  <rect width="70" height="92" rx="8" fill="#fff" stroke="{TINT2}"/>
  <rect x="12" y="16" width="34" height="6" rx="3" fill="{TINT2}"/>
  <rect x="12" y="32" width="46" height="5" rx="2.5" fill="{TINT}"/><rect x="12" y="44" width="40" height="5" rx="2.5" fill="{TINT}"/>
  <rect x="12" y="56" width="46" height="5" rx="2.5" fill="{TINT}"/>
</g>
<path d="M122 90 H178" stroke="{PRIMARY}" stroke-width="3" stroke-linecap="round"/>
<path d="M170 82 L180 90 L170 98" fill="none" stroke="{PRIMARY}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(196,34)">
  <rect width="100" height="112" rx="10" fill="#fff" stroke="{TINT2}"/>
  <rect width="100" height="24" rx="10" fill="{NAVY}"/><rect y="14" width="100" height="10" fill="{NAVY}"/>
  <text x="50" y="16" text-anchor="middle" class="t" font-size="9" fill="#fff">정리된 기록</text>
  <circle cx="18" cy="44" r="6" fill="{PRIMARY}"/><rect x="30" y="41" width="56" height="6" rx="3" fill="{TINT2}"/>
  <circle cx="18" cy="66" r="6" fill="{PRIMARY}"/><rect x="30" y="63" width="50" height="6" rx="3" fill="{TINT2}"/>
  <circle cx="18" cy="88" r="6" fill="{ORANGE}"/><rect x="30" y="85" width="44" height="6" rx="3" fill="{TINT2}"/>
</g>
""")

# 이름: dict(html=..., w=폭, h=높이, transparent=True면 바깥 배경 투명)
ILLUSTRATIONS = {
    "ill-example": dict(html=EXAMPLE, w=320, h=180, transparent=True),
}
