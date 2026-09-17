# 삽화 만들기

사진이나 그림 파일이 없어도, 도형을 코드로 그려 **슬라이드에 넣을 그림(PNG)** 을 만들 수 있습니다.
기술평가회 발표자료의 문제 카드 삽화·지역 지도·제품 화면 모형이 이 방식입니다.

## 목차
1. 흐름
2. 스타일 규칙
3. 무엇을 그리기 좋은가 / 안 좋은가
4. 견본 A — 카드 3개 비교 (SVG)
5. 견본 B — 사물 조합: 서류·전화·구급차 (SVG)
6. 견본 C — 양식화한 지도 + 위치 핀 (SVG)
7. 견본 D — 제품 화면 모형 (HTML)

---

## 1. 흐름

1. `build/illustrations.py` 에 그림을 정의하고 `ILLUSTRATIONS` 에 이름을 등록합니다.
   ```python
   ILL_PROBLEM = scene(f"""...도형...""")            # 기본 320×180, 옅은 파란 판 포함
   ILLUSTRATIONS = {
       "ill-problem": dict(html=ILL_PROBLEM, w=320, h=180, transparent=True),
       "app-screen":  dict(html=APP_HTML, w=564, h=268),   # HTML 화면 모형
   }
   ```
2. `python3 build.py` — 새로 생기거나 바뀐 그림만 `assets/<이름>.png` 로 굽습니다(2배 해상도).
3. 슬라이드에서 `Image("ill-problem.png", x, y, w, h)` — **w:h 비율을 정의한 크기와 같게** 둡니다(찌그러짐 방지).
4. `node render.mjs preview` 로 그림이 들어간 장을 눈으로 확인합니다. 그림 속 글자가 슬라이드에서 너무 작으면(실제 표시 9px 미만) 그림을 키우거나 글자를 뺍니다.

## 2. 스타일 규칙 — 슬라이드와 한 몸처럼

- 색은 `theme` 토큰만: 판 TINT, 선 TINT2, 주요 도형 PRIMARY, 짙은 면 NAVY, 흰 카드 #fff, **문제·경고 한 곳만 ORANGE**.
- 납작한 도형(둥근 사각형·원·선)만. 그라디언트·그림자·사실적 묘사 없음.
- 둥근 모서리 8~16, 선 두께 1(테두리) / 2.5~3(강조선), `stroke-linecap="round"`.
- 글씨는 `class="t"`(굵게) / `class="r"`(보통), 9~22px. 그림 속 글자는 짧은 라벨만 — 설명은 슬라이드 글자로.
- 한 그림에 사물 2~3개. 빈 공간을 남겨 둡니다.
- 화면 모형 속 숫자·이름은 **예시값**입니다. 실제 수치처럼 보이면 슬라이드에 "표시값은 예시입니다"를 적습니다.

## 3. 무엇을 그리기 좋은가

| 잘 맞음 | 맞지 않음 → 대안 |
|---|---|
| 비교 카드, 흐름·전후 대비, 서류·기기·건물 같은 단순 사물 | 사람 얼굴·몸짓, 사실적 장면 → 아이콘 카드 또는 실제 사진 요청 |
| 양식화한 지도·위치 핀 | 정확한 행정 지도 → 받은 지도 이미지 사용 |
| 제품 화면 모형(대시보드·입력 화면) | 실제 제품 화면을 그대로 보여줘야 할 때 → 스크린샷 요청 |
| 간단한 막대·게이지 느낌의 장식 | 실제 데이터 차트 → 표나 `stat` 숫자로 |

---

## 4. 견본 A — 카드 3개 비교

```python
# ---- 삽화 1: 기관별 정의 불일치 — 병원 세 곳, 같은 항목 다른 표기
ILL_1 = scene(f"""
<defs><style>.t{{font-family:'Noto Sans KR';font-weight:700}}</style></defs>
<rect x="0" y="0" width="320" height="180" rx="16" fill="{TINT}"/>
<g transform="translate(24,34)">
  <rect width="82" height="112" rx="10" fill="#fff" stroke="{TINT2}"/>
  <rect x="31" y="-10" width="20" height="20" rx="4" fill="{PRIMARY}"/><rect x="39" y="-6" width="4" height="12" fill="#fff"/><rect x="35" y="-2" width="12" height="4" fill="#fff"/>
  <text x="41" y="42" text-anchor="middle" class="t" font-size="11" fill="{MUTED}">가용병상</text>
  <text x="41" y="72" text-anchor="middle" class="t" font-size="22" fill="{NAVY}">27</text>
  <text x="41" y="94" text-anchor="middle" font-size="10" fill="{MUTED}">15분 전</text>
</g>
<g transform="translate(119,34)">
  <rect width="82" height="112" rx="10" fill="#fff" stroke="{TINT2}"/>
  <rect x="31" y="-10" width="20" height="20" rx="4" fill="{PRIMARY}"/><rect x="39" y="-6" width="4" height="12" fill="#fff"/><rect x="35" y="-2" width="12" height="4" fill="#fff"/>
  <text x="41" y="42" text-anchor="middle" class="t" font-size="11" fill="{MUTED}">빈 침상</text>
  <text x="41" y="72" text-anchor="middle" class="t" font-size="22" fill="{NAVY}">8/62</text>
  <text x="41" y="94" text-anchor="middle" font-size="10" fill="{MUTED}">어제 기준</text>
</g>
<g transform="translate(214,34)">
  <rect width="82" height="112" rx="10" fill="#fff" stroke="{TINT2}"/>
  <rect x="31" y="-10" width="20" height="20" rx="4" fill="{PRIMARY}"/><rect x="39" y="-6" width="4" height="12" fill="#fff"/><rect x="35" y="-2" width="12" height="4" fill="#fff"/>
  <text x="41" y="42" text-anchor="middle" class="t" font-size="11" fill="{MUTED}">병상</text>
  <text x="41" y="72" text-anchor="middle" class="t" font-size="22" fill="#F97316">?</text>
  <text x="41" y="94" text-anchor="middle" font-size="10" fill="{MUTED}">유선 확인</text>
</g>
""")
```

## 5. 견본 B — 사물 조합

```python
# ---- 삽화 3: 유선 확인·반복 입력 — 종이 서식, 전화기, 구급차
ILL_3 = scene(f"""
<defs><style>.t{{font-family:'Noto Sans KR';font-weight:700}}</style></defs>
<rect x="0" y="0" width="320" height="180" rx="16" fill="{TINT}"/>
<g transform="translate(24,40)">
  <rect x="10" y="10" width="86" height="104" rx="8" fill="#fff" stroke="{TINT2}" transform="rotate(-6 53 62)"/>
  <rect x="0" y="0" width="86" height="104" rx="8" fill="#fff" stroke="{TINT2}"/>
  <rect x="14" y="18" width="40" height="7" rx="3" fill="{TINT2}"/><rect x="14" y="34" width="58" height="6" rx="3" fill="{TINT}"/>
  <rect x="14" y="48" width="58" height="6" rx="3" fill="{TINT}"/><rect x="14" y="62" width="44" height="6" rx="3" fill="{TINT}"/>
  <rect x="14" y="76" width="58" height="6" rx="3" fill="{TINT}"/>
</g>
<g transform="translate(132,50)">
  <rect width="40" height="76" rx="10" fill="{NAVY}"/><rect x="5" y="8" width="30" height="52" rx="4" fill="#fff"/>
  <circle cx="20" cy="68" r="4" fill="#fff" opacity=".6"/>
  <path d="M52 18 q12 16 0 32" fill="none" stroke="#F97316" stroke-width="3" stroke-linecap="round"/>
  <path d="M62 8 q20 26 0 52" fill="none" stroke="#F97316" stroke-width="3" stroke-linecap="round" opacity=".5"/>
</g>
<g transform="translate(212,80)">
  <rect x="34" y="-7" width="12" height="7" rx="3" fill="#F97316"/>
  <path d="M8 0 H48 V10 H64 L78 22 H84 Q88 22 88 26 V34 Q88 38 84 38 H8 Q0 38 0 30 V8 Q0 0 8 0 Z"
        fill="#fff" stroke="{PRIMARY}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M66 13 L76 22 H66 Z" fill="{TINT2}"/>
  <rect x="14" y="8" width="20" height="20" rx="5" fill="{PRIMARY}"/>
  <rect x="22" y="12" width="4" height="12" rx="1" fill="#fff"/><rect x="18" y="16" width="12" height="4" rx="1" fill="#fff"/>
  <circle cx="24" cy="38" r="8" fill="{NAVY}"/><circle cx="24" cy="38" r="3" fill="#fff"/>
  <circle cx="72" cy="38" r="8" fill="{NAVY}"/><circle cx="72" cy="38" r="3" fill="#fff"/>
</g>
""")
```

## 6. 견본 C — 양식화한 지도 + 핀

```python
# ---- 섬 지도 (양식화) + 기관 6곳 핀 — 맺음/기대효과용
JEJU = scene(f"""
<g transform="translate(0,-26)">
<defs><style>.t{{font-family:'Noto Sans KR';font-weight:700}}</style></defs>
<path d="M60 150 C 40 110, 90 60, 190 52 C 300 44, 400 60, 450 100 C 500 140, 440 200, 340 210 C 240 220, 120 230, 80 195 C 60 178, 66 164, 60 150 Z" fill="{TINT}" stroke="{TINT2}" stroke-width="2"/>
<path d="M60 150 C 40 110, 90 60, 190 52 C 300 44, 400 60, 450 100 C 500 140, 440 200, 340 210 C 240 220, 120 230, 80 195 C 60 178, 66 164, 60 150 Z" fill="none" stroke="{PRIMARY}" stroke-width="1.5" stroke-dasharray="4 5" opacity=".6"/>
<circle cx="250" cy="140" r="34" fill="{TINT2}" opacity=".7"/>
<g class="t" font-size="10" fill="{NAVY}">
  <g transform="translate(214,80)"><circle r="9" fill="{PRIMARY}"/><circle r="3.5" fill="#fff"/><text x="14" y="4">기관 A</text></g>
  <g transform="translate(180,108)"><circle r="9" fill="{PRIMARY}"/><circle r="3.5" fill="#fff"/><text x="-14" y="4" text-anchor="end">기관 B</text></g>
  <g transform="translate(150,84)"><circle r="7" fill="{TINT2}" stroke="{PRIMARY}" stroke-width="2"/><text x="-12" y="4" text-anchor="end" fill="{MUTED}">2027</text></g>
  <g transform="translate(300,96)"><circle r="7" fill="{TINT2}" stroke="{PRIMARY}" stroke-width="2"/><text x="12" y="4" fill="{MUTED}">2027</text></g>
  <g transform="translate(360,150)"><circle r="7" fill="{TINT2}" stroke="{PRIMARY}" stroke-width="2"/><text x="12" y="4" fill="{MUTED}">2027</text></g>
  <g transform="translate(250,196)"><circle r="7" fill="{TINT2}" stroke="{PRIMARY}" stroke-width="2"/><text x="12" y="4" fill="{MUTED}">2027</text></g>
</g>
</g>
""", 520, 214)
```
등록할 때 `w=520, h=240`.

## 7. 견본 D — 제품 화면 모형 (HTML)

SVG 대신 HTML 로 그리면 표·버튼·글 줄바꿈이 쉬워집니다. `scene()` 없이 `<div>` 를 바로 씁니다.

```python
# ---- 새록 라이브 「바로 서식」 화면 (구급대 → 응급실 인계) · 표시값은 예시
_SA = PRIMARY  # 프라이머리 하나로 통일 (보라 사용 안 함)
_F = [
    ("발생시각", "2026-09-10 14:10", "0.96", False),
    ("주호소", "가슴 통증 (흉통)", "0.94", False),
    ("의식·활력징후", "명료 · BP 150/90 · HR 102", "0.95", False),
    ("처치", "니트로글리세린 설하 · 12유도 심전도", "0.74", True),
    ("도착예정", "약 15분 뒤 (14:38)", "0.91", False),
]
_ROWS = "".join(
    f'<div style="display:flex;align-items:center;gap:7px;padding:4px 0;border-bottom:1px solid #EEF1F6">'
    f'<div style="width:64px;flex:none;font-size:9px;color:{MUTED}">{lab}</div>'
    f'<div style="flex:1;min-width:0;font-size:9.5px;color:{NAVY};font-weight:500;background:#F7F9FC;'
    f'border:1px solid {BORDER};border-radius:5px;padding:4px 7px;white-space:nowrap;overflow:hidden;'
    f'text-overflow:ellipsis">{val}</div>'
    f'<div style="flex:none;width:46px;text-align:center;font-size:8.5px;font-weight:700;border-radius:9px;padding:3px 0;'
    + (f'background:#FFF3E8;color:#F97316">{conf}' if warn else f'background:{TINT};color:#2A5FD0">{conf}')
    + '</div></div>'
    for lab, val, conf, warn in _F)

APP_MOCK = f"""
<div style="position:absolute;inset:0;background:#fff;border-radius:10px;overflow:hidden;border:1px solid {BORDER}">
  <div style="height:26px;background:#F5F7FA;border-bottom:1px solid {BORDER};display:flex;align-items:center;padding:0 11px;gap:8px">
    <div style="display:flex;gap:4px"><span style="width:7px;height:7px;border-radius:50%;background:#E0E5EE"></span>
      <span style="width:7px;height:7px;border-radius:50%;background:#E0E5EE"></span>
      <span style="width:7px;height:7px;border-radius:50%;background:#E0E5EE"></span></div>
    <div style="font-size:9.5px;font-weight:700;color:{NAVY};white-space:nowrap">새록 라이브 · 구급대 → 응급실 인계</div>
    <div style="margin-left:auto;font-size:8.5px;font-weight:700;color:#F97316;background:#FFF3E8;border-radius:9px;padding:3px 8px;white-space:nowrap">승인 전 · 미반영</div>
  </div>
  <div style="display:flex;height:calc(100% - 26px)">
    <div style="width:196px;flex:none;padding:10px 11px;border-right:1px solid {BORDER};display:flex;flex-direction:column">
      <div style="display:flex;align-items:center;gap:6px">
        <div style="width:19px;height:19px;flex:none;border-radius:50%;background:{_SA};display:flex;align-items:center;justify-content:center">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/></svg></div>
        <div style="font-size:9.5px;font-weight:700;color:{NAVY};white-space:nowrap">현장 발화 <span style="font-weight:400;color:{MUTED}">14:23</span></div>
        <div style="margin-left:auto;display:flex;align-items:flex-end;gap:1.5px;height:13px">
          {''.join(f'<span style="width:2px;height:{h}px;background:{_SA};opacity:.55;border-radius:1px"></span>' for h in (5,9,13,7,11,4,8))}
        </div>
      </div>
      <div style="margin-top:8px;background:#F7F9FC;border:1px solid {BORDER};border-radius:7px;padding:8px 9px;
                  font-size:9px;line-height:1.6;color:{INK};flex:1">
        58세 남성, 14시 10분경 <b style="color:{NAVY}">가슴 통증</b>으로 쓰러졌습니다.
        의식 명료, <b style="color:{NAVY}">혈압 150/90</b>, 맥박 102.
        <b style="color:{NAVY}">니트로글리세린 설하</b> 투여하고 12유도 심전도 시행했습니다. 약 15분 뒤 도착 예정입니다.
      </div>
      <div style="margin-top:8px">
        <div style="display:flex;align-items:center;gap:6px">
          <div style="font-size:8.5px;color:{MUTED};white-space:nowrap">발화 종료 → 초안 표시</div>
          <div style="margin-left:auto;font-size:10px;font-weight:700;color:{NAVY}">1.2초</div>
        </div>
        <div style="margin-top:4px;position:relative;height:5px;background:#EEF1F6;border-radius:3px">
          <div style="position:absolute;left:0;top:0;height:5px;width:40%;background:{_SA};border-radius:3px"></div>
          <div style="position:absolute;left:78%;top:-2px;width:2px;height:9px;background:#F97316;border-radius:1px"></div>
        </div>
        <div style="margin-top:4px;font-size:8px;color:{LIGHT}">주황 눈금 = 목표선. 표시값은 예시입니다.</div>
      </div>
    </div>
    <div style="flex:1;min-width:0;padding:10px 11px;display:flex;flex-direction:column">
      <div style="display:flex;align-items:baseline;gap:6px">
        <div style="font-size:9.5px;font-weight:700;color:{NAVY};white-space:nowrap">「바로 서식」 초안</div>
        <div style="font-size:8.5px;color:{LIGHT};white-space:nowrap">필드별 수정 · 근거 원문 대조</div>
        <div style="margin-left:auto;font-size:8px;color:{LIGHT};white-space:nowrap">확신도</div>
      </div>
      <div style="margin-top:5px">{_ROWS}</div>
      <div style="margin-top:auto;display:flex;align-items:center;gap:7px;padding-top:8px">
        <div style="font-size:8px;color:{MUTED};line-height:1.45;flex:1;min-width:0">승인 전에는 운영 데이터와<br>의무기록에 반영되지 않습니다.</div>
        <div style="flex:none;font-size:8.5px;font-weight:700;color:{MUTED};border:1px solid {BORDER};border-radius:6px;padding:6px 8px;white-space:nowrap">원문 대조</div>
        <div style="flex:none;font-size:8.5px;font-weight:700;color:#fff;background:{_SA};border-radius:6px;padding:6px 10px;white-space:nowrap">확인하고 승인</div>
      </div>
    </div>
  </div>
</div>
"""
```
등록할 때 `"app-mock": dict(html=APP_MOCK, w=564, h=268)` (배경이 흰색이라 transparent 불필요).
