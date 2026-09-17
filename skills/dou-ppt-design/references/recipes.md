# 본문 장 레시피

기술평가회 발표자료(29장)에서 실제로 쓰고 검증한 배치들입니다.
그대로 복사해 문구·개수만 바꾸세요. 모든 좌표는 1280×720, 본문 영역은 `CONTENT_TOP`(158) ~ 664.

## 목차
1. 기본 뼈대 (모든 본문 장)
2. 왼쪽 강조 카드 + 오른쪽 항목 3개
3. 사진·삽화 카드 3열 (+ 사진 없을 때 아이콘 카드)
4. 표 + 오른쪽 짙은 패널
5. 아이콘 목록 + 연도별 로드맵
6. 단계 흐름 (화살표)
7. 조직도
8. 글 넘침 막는 법
9. 내용이 많은 장 견본
10. 앱·웹 화면 (흐름 / 화면 설명 / 앱+웹)
11. 로고와 여러 기관 색 구분

---

## 1. 기본 뼈대

```python
def s_something():
    s = slide("장 이름(파일 안에서만 보임)")
    s.add(header("SECTION TAG", "큰 제목", "제목 아래 한 문장 결론", ref="오른쪽 위 작은 출처(선택)"))
    # ... 본문 ...
    s.add(footer(N()))
```

- `header` 라벨은 영문 대문자 섹션 이름, 제목은 짧게(한 줄), 부제는 한 문장.
- **본문은 아래 y≈620~640 까지 채웁니다.** 아래 레시피 좌표는 예시라서 항목 수가 적으면 끝이 y≈500 근처에서 멈춥니다.
  그럴 땐 카드 높이·간격을 늘려 채우고, 카드 속 내용은 `valign="middle"` 이나 좌표 계산으로 카드 안 세로 가운데에 둡니다(위에 붙이면 카드가 텅 비어 보임).
- `balance=True`(기본)는 최대 26px 만 내려 주는 미세 조정이지, 빈 아래쪽을 해결해 주지 않습니다.
- 내용이 모자라면 칸을 지어낸 말로 채우지 말고, 이미 받은 사실(담당자·연도·대상)로 채우거나 칸 자체를 뺍니다.

## 2. 왼쪽 강조 카드 + 오른쪽 항목 3개

목표·원칙·핵심 메시지를 말할 때.
`paras()` 는 문단 목록입니다. 한 문단 안에서 일부만 색을 바꾸려면 `("앞 ", ("강조", {"color": ...}), " 뒤")` 처럼 **튜플 하나로 묶어** 넘깁니다.

```python
gx, gy, gw, gh = MX, CONTENT_TOP, 470, 316
s.add(card(gx, gy, gw, gh, fill=NAVY, radius=16),
      Icon("quote", gx + 28, gy + 26, 26, "#60A5FA"),
      Text(gx + 28, gy + 66, gw - 56, 150, paras(
          ("핵심 문장 앞부분 ", ("강조할 말", {"color": "#93C5FD"}), " 뒷부분"),
      ), size=21, color=WHITE, weight=700, line=1.5),
      Text(gx + 28, gy + 236, gw - 56, 48, "보충 한 문장", size=12.5, color="#B7C6E6", line=1.5))
px = MX + 500; pw = W - MX - px
y = CONTENT_TOP
for i, (ic, t, d, tag) in enumerate(items):          # 3개
    s.add(card(px, y, pw, 104, fill=CARD, radius=14),
          icon_badge(px + 18, y + 18, ic, size=40, bg=WHITE, color=PRIMARY, radius=10),
          Text(px + 74, y + 14, pw - 90, 24, runs((f"원칙 {i+1}  ", {"color": PRIMARY, "size": 12}), (t, {"bold": True})), size=16, color=NAVY, weight=700),
          Text(px + 74, y + 38, pw - 90, 40, d, size=12, color=INK, line=1.45),
          Text(px + 74, y + 78, pw - 90, 18, runs(("→ ", {"color": PRIMARY, "bold": True}), tag), size=11.5, color=MUTED))
    y += 113
```
아래 남는 자리(y≈500~)에는 `Line` 한 줄 + `stat(...)` 4개를 가로로 두면 숫자 요약이 됩니다.

## 3. 사진·삽화 카드 3열

문제 → 해결처럼 같은 구조 3개를 나란히.

```python
gap = 20; cw = (W - 2*MX - 2*gap) / 3
for i, (img, t, d, sol) in enumerate(cards):
    x = MX + i * (cw + gap); ih = cw * 180 / 320
    s.add(card(x, CONTENT_TOP, cw, 330, fill=WHITE, radius=16, stroke=BORDER),
          Image(img, x + 1, CONTENT_TOP + 1, cw - 2, ih),      # 이미지 없으면 photo_placeholder(...)
          Text(x + 18, CONTENT_TOP + ih + 12, cw - 36, 24, t, size=15, color=NAVY, weight=700),
          Text(x + 18, CONTENT_TOP + ih + 38, cw - 36, 40, d, size=12, color=MUTED, line=1.45),
          pill(x + 18, CONTENT_TOP + ih + 84, "해결", size=10.5, w=44, h=22),
          Text(x + 70, CONTENT_TOP + ih + 82, cw - 88, 36, sol, size=12, color=INK, weight=500))
```
이미지는 `build/assets/` 에 넣고 파일명만 적습니다. 사진이 없으면 `illustrations.py` 로 삽화를 그려 넣거나(references/illustrations.md), 3-1 아이콘 카드를 씁니다. `photo_placeholder` 는 나중에 사진을 받을 초안에만 씁니다.

### 3-1. 사진이 없을 때 — 아이콘 카드 3열

사진 자리 점선은 미완성처럼 보여서 외부 발표에는 쓰지 않습니다. 대신 아이콘 카드를 씁니다.

```python
gap = 20; cw = (W - 2*MX - 2*gap) / 3; ch = 400
for i, (ic, tag, t, d) in enumerate(cards):
    x = MX + i * (cw + gap)
    s.add(card(x, CONTENT_TOP, cw, ch, fill=WHITE, radius=16, stroke=BORDER),
          icon_badge(x + 24, CONTENT_TOP + 28, ic, size=52, bg=TINT, color=PRIMARY, radius=14),
          pill(x + 24, CONTENT_TOP + 104, tag, size=10.5, h=22),
          Text(x + 24, CONTENT_TOP + 138, cw - 48, 30, t, size=20, color=NAVY, weight=700),
          Text(x + 24, CONTENT_TOP + 176, cw - 48, 120, d, size=13, color=MUTED, line=1.55))
```

## 4. 표 + 오른쪽 짙은 패널

범위·일정·인력처럼 행이 있는 정보 + "하지 않는 것/확약" 같은 대비.

```python
lw = 700
items, cy = table(MX, CONTENT_TOP, lw, [("구분", 1.1), ("내용", 3.6), ("담당", 1.5)], rows,
                  head_h=30, row_h=52, size=12.5, bold_first=True)
s.add(items)
rx = MX + lw + 28; rw = W - MX - rx
s.add(card(rx, CONTENT_TOP, rw, 432, fill=NAVY, radius=16),
      Icon("ban", rx + 24, CONTENT_TOP + 22, 22, "#FF9B6B"),
      Text(rx + 54, CONTENT_TOP + 18, rw - 70, 30, "패널 제목", size=17, color=WHITE, weight=700, valign="middle"))
y = CONTENT_TOP + 66
for t in lines:
    th = nlines(t, rw - 66, 13) * 13 * 1.45 + 4          # 줄 수를 계산해 높이를 맞춘다
    s.add(Icon("x-circle", rx + 24, y + 3, 16, "#FF9B6B"),
          Text(rx + 48, y, rw - 66, th, t, size=13, color=WHITE, line=1.45))
    y += th + 18
```
표만 넓게 쓸 때는 `lw = W - 2*MX`. 머리글 옆 칸 비율(`("내용", 3.6)`)로 칸 폭을 정하고, 칸 글이 두 줄이면 `row_hs=[...]` 로 그 행만 높입니다. 특정 칸 글자에 색·굵기를 주려면 문자열 대신 `runs(...)` 를 넣습니다.
표는 5~7행까지. 그 이상이면 장을 나누세요 — 빽빽한 표는 발표장에서 안 읽힙니다.

## 5. 아이콘 목록 + 연도별 로드맵

```python
lx, lw = MX, 520; y = CONTENT_TOP
for ic, a, b in effects:                               # 최대 5개
    s.add(Rect(lx, y, lw, 78, fill=CARD, radius=12),
          icon_badge(lx + 14, y + 17, ic, size=44, bg=WHITE, color=PRIMARY, radius=11),
          Text(lx + 72, y, lw - 88, 78, [runs((a, {"bold": True, "color": NAVY, "size": 13})),
                                          runs((b, {"color": INK, "size": 11}))], size=11, line=1.45, para_gap=4, valign="middle"))
    y += 86
rx = lx + lw + 28; rw = W - MX - rx; y = CONTENT_TOP
for yr, tag, c, d in years:                            # c: PRIMARY → PRIMARY_DK → NAVY 순으로 짙게
    s.add(Rect(rx, y, 6, 74, fill=c, radius=3),
          Text(rx + 18, y - 2, 60, 26, yr, size=18, color=c, weight=700, valign="middle"),
          pill(rx + 80, y + 2, tag, color=c, size=10, w=64, h=20),
          Text(rx + 18, y + 26, rw - 30, 44, d, size=10.5, color=INK, line=1.4))
    y += 90
```

## 6. 단계 흐름 (화살표)

```python
steps = ["1단계", "2단계", "3단계", "결과"]
sw = (W - 2*MX - 3*36) / 4
for i, t in enumerate(steps):
    x = MX + i * (sw + 36); last = i == len(steps) - 1
    s.add(Rect(x, 300, sw, 56, fill=PRIMARY if last else TINT, radius=10),
          Text(x, 300, sw, 56, t, size=14, color=WHITE if last else PRIMARY, weight=700, align="center", valign="middle"))
    if not last:
        s.add(Icon("arrow-right", x + sw + 9, 319, 18, LIGHT))
```

## 7. 조직도

`layouts.org_chart` 를 씁니다. 대표 카드 + 구성원 줄, 선으로만 연결합니다(점·특정인 강조 없음 — 반려됨).

```python
s.add(header("ORGANIZATION", "조직도", "대표이사 아래 팀장 1명과 연구원 3명이 ... 나눠 맡습니다."))
org_chart(s, ("홍길동", "대표이사", "영업 · 연구 · 개발 총괄"),
          [("김철수", "팀장", "소프트웨어 개발", "10년 이상", "제품 A · 제품 B"), ...])
```
부제에서 인원을 셀 때는 직책을 구분해 셉니다(팀장이 섞였는데 "연구원 4명"이라고 쓰지 않기).

## 8. 글 넘침 막는 법

- 글 상자 높이는 `nlines(text, w, size) * size * line` 으로 계산하고, 글자 수로 어림잡지 않습니다.
- 빌드 후 `python3 check_fit.py` → "넘침 없음"이 나올 때까지 문구를 줄이거나 상자를 키웁니다.
- 22px 미만 글자는 엔진이 자동으로 1.2px 키웁니다(`TEXT_BUMP`). 좌표는 원래 크기로 잡으면 됩니다.
- 쓸 수 있는 아이콘 이름은 `python3 list_icons.py` 로 봅니다. 없으면 Lucide 아이콘 SVG path 를 추가합니다.
- 색은 `theme.py` 토큰만 씁니다: PRIMARY, PRIMARY_DK, NAVY, INK, MUTED, LIGHT, BORDER, CARD, TINT, ORANGE(경고 1곳), GREEN, RED, WHITE.

## 9. 내용이 많은 장 견본
10. 앱·웹 화면 (흐름 / 화면 설명 / 앱+웹)
11. 로고와 여러 기관 색 구분

제안·기술평가처럼 한 장에 표·숫자·화면을 같이 보여줘야 할 때는 **references/examples/dense_slide.py** 를 봅니다.
왼쪽 표(4행)와 측정지표 문단, 오른쪽 짙은 숫자 패널과 제품 화면 모형이 한 장에 들어갑니다. 화면 모형은 illustrations.md 견본 D 를 `app-mock` 이름으로 등록해 씁니다.

- 좌우를 560 : 나머지로 나누고, 사이 간격은 28px.
- 같은 장 안에서 글자 크기는 3단계만: 제목급 28(숫자), 본문 11~12, 보조 9~10.5.
- 짙은 패널 안 보조 글은 #B7C6E6 / #8FA3CC, 강조 라벨은 #93C5FD.
- 복잡해도 부제는 한 문장. 출처는 header 의 `ref` 로 오른쪽 위에 작게.
- "예시 데이터입니다", "보장값 아님" 같은 단서는 해당 요소 바로 아래 LIGHT 색 한 줄로 붙입니다.

## 10. 앱·웹 화면

캡처 파일이 없으면 `None` 으로 두면 점선 빈칸(라벨 포함)으로 자리만 잡힙니다. 파워포인트에서 빈칸 도형 이름이 `자리:<라벨>` 이라 찾아 바꾸기 쉽습니다.
캡처가 생기면 `build/assets/` 에 넣고 `None` 자리에 파일명을 넣습니다. 휴대폰 캡처는 세로 19.5:9 비율이 맞습니다(다르면 잘라서 맞춤).

**흐름 (휴대폰 3~5개 + 화살표 + 단계 설명)**
```python
s.add(header("APP FLOW", "말하면 기록이 완성됩니다", "녹음부터 확인까지 네 단계로 끝납니다."))
app_flow(s, [("녹음 시작", "환자를 고르고 녹음 버튼을 누릅니다", None),
             ("말로 기록", "평소 말하듯 상태를 말합니다", "app-02.png"),
             ("초안 확인", "정리된 서식을 훑어보고 고칩니다", None)])
```

**화면 한 장 설명 (휴대폰 하나 + 번호 설명 3~5개)**
세 번째 값은 화면 위 번호 위치(0=맨 위, 1=맨 아래). `None` 이면 화면에 번호를 찍지 않습니다. `side="right"` 면 휴대폰이 오른쪽.
```python
app_callouts(s, None, "초안 확인 화면", [
    ("환자 정보", "지금 기록 중인 환자를 맨 위에 고정합니다.", 0.12),
    ("항목별 초안", "말한 내용이 서식 칸에 나눠 들어갑니다.", 0.45),
    ("확인 버튼", "확인 전에는 기록이 저장되지 않습니다.", 0.9)])
```

**앱 + 웹 나란히**
```python
items, ph = phone_slot(MX + 60, CONTENT_TOP + 20, 210, "앱 · 기록 화면")
s.add(items)
s.add(Icon("arrow-right", MX + 330, CONTENT_TOP + 20 + ph / 2 - 14, 28, PRIMARY))
s.add(browser_slot(MX + 400, CONTENT_TOP + 20, W - 2 * MX - 400, ph, "웹 콘솔 · 기록 목록"))
```
`phone_slot` 은 (도형 목록, 높이) 를 돌려주고, `browser_slot` 은 도형 목록만 돌려줍니다. 휴대폰 폭 210 이면 높이 455 — 본문 영역에 맞추려면 폭 230 이하.

## 11. 로고와 여러 기관 색 구분

**서비스 로고 줄 세우기**
```python
names = ["새록", "미리봄", "약먹자"]
gap = 20; cw = (W - 2*MX - (len(names)-1)*gap) / len(names)
for i, n in enumerate(names):
    x = MX + i * (cw + gap)
    s.add(card(x, CONTENT_TOP, cw, 260, fill=CARD, radius=16),
          logo(n, x + cw / 2, CONTENT_TOP + 50, 80, align="center"),
          Text(x, CONTENT_TOP + 160, cw, 30, n, size=20, color=NAVY, weight=700, align="center"))
```
짙은 바탕 위에는 `logo("도우", x, y, 36, white=True)`.

**도우 + 협력 기관 역할 나누기** (기관 색은 brand_color.py 로 뽑은 값)
```python
HOSP, HOSP_TEXT, HOSP_T = brand("#9CA800")          # 예: 로고에서 뽑은 색
orgs = [("도우", DOU, PRIMARY_DK, DOU_T, "logos/ci.png"), ("OO병원", HOSP, HOSP_TEXT, HOSP_T, "hospital-logo.png")]
cw = (W - 2*MX - 24) / 2
for i, (name, fill, text, tint, img) in enumerate(orgs):
    x = MX + i * (cw + 24)
    s.add(Rect(x, CONTENT_TOP, cw, 300, fill=tint, radius=16),
          Rect(x, CONTENT_TOP, 6, 300, fill=fill, radius=3),
          Text(x + 28, CONTENT_TOP + 22, cw - 56, 30, name, size=20, color=text, weight=700))
    # 로고: 도우 서비스는 logo(...), 외부 기관은 Image(파일, x, y, w, h) — w:h 는 원본 비율 그대로
```
표 안에서 담당 기관을 표시할 때는 칸에 `runs(("도우", {"color": PRIMARY_DK, "bold": True}))`, `runs(("OO병원", {"color": HOSP_TEXT, "bold": True}))` 처럼 **글자색(둘째 값)** 을 씁니다.
