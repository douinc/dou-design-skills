"""내용이 많은 장 견본 — 기술평가회 발표자료의 「음성기반 기록 적용방안」 장 구성을 그대로 두고 문구만 예시로 바꿨다.
구성: 왼쪽 표(4행) + 안내 한 줄 + 측정지표 문단 / 오른쪽 짙은 숫자 패널 + 화면 모형 삽화(app-mock.png).
삽화는 references/illustrations.md 견본 D 방식으로 illustrations.py 에 정의한다.
이 함수를 deck.py 에 붙이고 BUILD 에 넣으면 그대로 나온다. 숫자·문구는 모두 예시값.
"""


def dense_example():
    s = slide("내용이 많은 장 예시")
    s.add(header("TECHNOLOGY · VOICE", "음성기반 기록 적용방안",
                 "현장 발화를 서식 초안으로 바꾸고, 담당자가 확인한 뒤에만 반영합니다.", "제안서 Ⅲ-7"))
    lx, lw = MX, 560
    rows = [["인계 기록", "발생시각, 주요 증상, 처치, 도착예정", "담당자 초안 확인 후 승인"],
            ["초기 기록 보조", "내원경로, 주요 증상, 관찰 내용, 주의사항", "검토 후 기존 시스템에서 직접 확정"],
            ["제한 사유 등록", "제한 대상, 사유 후보, 시작·해제 예정시각", "당직자 승인 전 화면 미반영"],
            ["상태 변경", "장비·인력 상태, 변경 사유, 유효시간", "담당자 확인과 만료시간 지정"]]
    items, cy = table(lx, CONTENT_TOP, lw, [("적용 장면", 1.1), ("서식 출력", 1.7), ("사람의 확인", 1.6)], rows,
                      head_h=28, row_h=54, size=11, bold_first=True)
    s.add(items)
    s.add(Text(lx, cy + 6, lw, 18, "실제 적용은 기관 승인 후 수행하고, 승인 전에는 모의 사례로 검증합니다.", size=10.5, color=LIGHT))
    my = cy + 30
    s.add(Text(lx, my, lw, 20, "효과 측정지표", size=12, color=NAVY, weight=700))
    s.add(Text(lx, my + 24, lw, 54,
               "작성시간, 항목 완전성, 수정률, 응답속도, 안전성 다섯 가지를 착수 시 기준선으로 측정하고 완료 시 변화량을 보고합니다.",
               size=11, color=INK, line=1.5))
    rx = lx + lw + 28
    rw = W - MX - rx
    s.add(Rect(rx, CONTENT_TOP, rw, 180, fill=NAVY, radius=16),
          Text(rx + 22, CONTENT_TOP + 14, rw - 44, 20, "기존 운영 수치 (예시값)", size=12, color="#B7C6E6", weight=700))
    facts = [("00", "% 이하 ↓", "인식 오류율 · 낮을수록 좋음"),
             ("00", "% 이상 ↑", "전문용어 인식률"),
             ("00", "% 이상 ↑", "서식 완성도 · 최근 30일")]
    fw = (rw - 44 - 2 * 10) / 3
    for i, (v, u, l) in enumerate(facts):
        x = rx + 22 + i * (fw + 10)
        s.add(Text(x, CONTENT_TOP + 38, fw, 34, runs((v, {"bold": True, "size": 28}), (u, {"size": 10, "color": "#B7C6E6"})),
                   size=28, color=WHITE, line=1.1, valign="bottom"),
              Text(x, CONTENT_TOP + 76, fw, 30, l, size=9.5, color="#B7C6E6", line=1.35))
    s.add(Text(rx + 22, CONTENT_TOP + 110, rw - 44, 28, "본 사업 목표값과 측정 방법은 착수 단계에서 확정합니다. 표본·정답 규칙은 측정 전에 고정합니다.", size=9, color="#8FA3CC", line=1.4),
          Rect(rx + 22, CONTENT_TOP + 142, rw - 44, 26, fill="#1B2A55", radius=8),
          Text(rx + 32, CONTENT_TOP + 142, rw - 64, 26, runs(("인수 기준  ", {"bold": True, "color": "#9BC4FF"}), "미승인 반영 0건 · 근거 없는 값은 오류로 집계"),
               size=9.5, color=WHITE, valign="middle", line=1))
    my2 = CONTENT_TOP + 194
    s.add(Image("app-mock.png", rx, my2, rw, 268, name="app-mock"),
          Text(rx, my2 + 274, rw, 16, "화면은 예시 데이터입니다.", size=9.5, color=LIGHT))
    s.add(footer(N()))
