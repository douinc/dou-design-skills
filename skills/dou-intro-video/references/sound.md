# 효과음과 음악

소리는 전부 코드로 만든다. 효과음은 earshot 뱅크(시드를 고정하면 다시 만들어도 같은 소리), 음악은 `tools/audio/music.py`의 120 BPM 베드. 그래서 시각을 옮기면 소리도 같이 옮겨진다.

## 원칙

- **화면 사건마다 소리 하나.** 탭, 결과가 뜸, 칩이 붙음, 화면이 넘어감, 록스타 착지. 소리가 사건을 짚어 주면 보는 사람이 어디를 봐야 하는지 안다.
- **사건과 ±1프레임(33ms).** 큐 시트가 시각의 기준이고 장면이 거기에 맞춘다. 사건을 옮기고 싶으면 장면 파일 머리 주석에 `큐 변경: 13.6 → 13.9 tap/soft`로 적고 큐 시트를 함께 고친다.
- 같은 종류가 연달아 나면(목록 줄 넷, 칸 넷) **음정을 한 단계씩 올린다**(C5 → D5 → E5 …). 쌓여 가는 느낌이 난다.
- 좌우(pan)를 화면 위치에 맞춘다: 왼쪽 폰의 탭은 −0.3, 오른쪽 칩은 +0.3. 제목·엔딩은 0.
- 작은 UI 소리는 음악 아래(−24 ~ −15 dB), 장 바뀜은 위(−12 ~ −6 dB).
- 록스타를 화면에서 뺐어도 그 순간의 소리는 남긴다.

## 큐 시트 — `data/cues.<id>.json`

```json
{
 "video": "yakmeokja",
 "music": {"bpm": 120, "start": 0.1, "intro_until": 8, "stop": 96.975, "final_hit": 97.175, "end": 101.575, "level_db": -19, "variant": "A"},
 "ducks": [[92.575, 92.875, -10], [96.975, 97.175, -14]],
 "cues": [
  {"t": 13.6, "id": "tap/soft", "gain": -15, "pan": -0.3, "scene": 4, "note": "바코드 스캔 탭"},
  {"t": 12.3, "id": "ui_pop/step", "gain": -16, "pan": 0.2, "pitch": "C5", "scene": 4, "note": "목록 첫 줄"}
 ]
}
```

- `t`는 **영상 절대 시각(초)**. 컷 로컬 시각 = t − 컷 시작.
- `seed`(같은 소리 고정), `pitch`(음정), `dur`(리저 길이) 선택.
- `note`에 화면 사건을 적는다 — 나중에 고칠 사람이 이걸로 찾는다.
- 컷 길이를 바꿀 때는 `tools/retime.js`를 쓴다. 큐 시트·음악 끝맺음·덕이 함께 옮겨진다.

## 효과음 팔레트 — 새록·미리봄에서 쓴 것

| 사건 | id | gain(dB) |
|---|---|---|
| 목록 줄·칸이 하나씩 들어옴(음정 상행) | `ui_pop/step`, `ui_pop/soft` | −18 ~ −15 |
| 글자·받아쓰기가 찍힘(아주 작게) | `pro_hover_tick/soft` | −27 ~ −24 |
| 버튼 탭 | `tap/soft` | −15 |
| 작은 칩·배지가 붙음 | `ui_pop/blip` | −19 ~ −15 |
| 결과 확인·응답 도착 | `ui_pop/boop` | −15 |
| 완료(생성 완료·저장 완료·Day 1 배지) | `ui_pop/wide` | −14 ~ −12 |
| 록스타 웃는 눈·눈 뜸 | `mallet/glock` | −17 ~ −14 |
| 기억됨·완성 | `mallet/celesta` | −15 |
| 패널이 미끄러져 들어옴 | `swish/flick` | −16 |
| 봉투·호가 날아감 | `swish/bright` | −19 ~ −16 |
| 종이가 내려옴·넘김 | `swipe/paper` | −17 ~ −16 |
| 더미에 닿음 | `knock/desk`, `knock/plastic` | −12 |
| 녹음 시작·알림 도착 | `notify/mid_tine`, `notify/mid_wood` | −18 ~ −15 |
| 토글·탭 전환 | `toggle/on` | −16 |
| 말로 입력 시작 | `pluck/kalimba` | −14 |
| 사진 찍기·화면 캡처 | `shutter/dslr`, `shutter/quick`, `shutter/snap` | −13 ~ −10 |
| 붙여넣기·채팅 입력 | `pro_typing_run/soft` | −20 |
| 체크 | `pro_click/tink` | −16 |
| 록스타 팝인·착지 | `pro_pop_in/round` | −10 ~ −8 |
| 와이프·줌아웃 | `whoosh_fast/whip`, `whoosh_fast/crisp` | −18 ~ −16 |
| 기기 여러 대가 한꺼번에 | `cut_hit/kick` | −8 |
| 제목 직전(0.8초 리저 → 컷에서 멈춤) | `riser/dark` | −12 |
| 제목 첫 줄 | `cut_hit/sub` + `pro_logo_sting/swell_sting` | −8 / −12 |
| 엔딩 직전(1초 리저) | `riser/build` | −11 |
| 엔딩 마지막 코드 | `pro_impact/short` + `pro_sub_drop/soft` + `shimmer/m0` | −6 / −10 / −16 |

목록에 없는 소리를 쓰려면 `tools/audio/.venv/bin/python -c "from earshot.forge import bank; print(*bank.ids(), sep='\n')"`로 고른다.

## 음악 끝맺음

`music.py` 구조: 처음 ~ `intro_until`(제목 컷 시작) 가볍게 → 제목부터 비트 → `stop`에서 멈춤(스톱다운) → 0.2초 뒤 `final_hit`에 마지막 코드 → `end`에서 끝.

- `final_hit`은 엔딩 컷의 착지 순간(엔딩 컷 시작 + 0.3)과 같은 프레임, `stop`은 그 0.2초 앞, `end`는 영상 끝 0.3초 앞.
- 엔딩 직전 리저(`riser/build`)는 `stop`에서 끝나게.
- `ducks`: 스톱다운 구간 `[stop, final_hit, −14]`. 리저 같은 큰 소리 앞에서 음악을 잠깐 낮추려면 `[t0, t1, −10]`.
- `variant`: 같은 음악의 다른 편집 — 새록 A, 미리봄 B. 새 영상은 둘 중 제품 톤에 맞게.
- 라이선스 음악으로 바꾸려면 `mix.py --music track.wav`.

## 만들기와 점검

```bash
PY=tools/audio/.venv/bin/python
$PY tools/audio/mix.py --video <id> --stems      # out/audio/<id>.wav (+ 효과음·음악 따로)
$PY tools/audio/sheet.py --video <id>            # 파형·음량·스펙트로그램 위에 큐 시각 — out/audio/<id>-sheet.png
```

- 출력 JSON의 `missing`이 비어 있어야 한다(틀린 id).
- 음량: 통합 −14 LUFS, 트루피크 약 −1 dBTP(믹서가 맞춘다). `first_sound_s`가 0.1초 안 — 첫 프레임부터 소리가 있어야 시작이 힘 있다.
- 미리보기(`preview.html`)는 마지막으로 믹스한 WAV를 함께 튼다. 큐를 고쳤으면 믹스를 다시 돌려야 들린다.

## 내레이션(선택)

자막만이 기본이다. 성우 녹음을 받으면 영상 타임라인에 맞춘 WAV(0초 = 영상 0초) 하나로 받고 `mix.py --video <id> --vo vo.wav`. 말하는 동안 음악이 5dB 내려간다(`--vo-duck`). 줄별 시작 시각 = 컷 시작 + 0.25초(자막이 뜨는 시각).
