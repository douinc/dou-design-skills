"""발표자료 내용 — 이 파일만 고친다. 빌드: python3 build.py"""
import theme
from engine import Slide, Rect, Text, Line, Icon, Image, Run, runs, paras, W, H
from theme import *  # noqa
from layouts import cover, agenda, divider, closing, appendix_divider, apx_header, stat_row, org_chart, gantt, logo, logo_width, app_flow, app_callouts, phone_slot, browser_slot

TITLE = "발표자료"                     # 결과 파일 이름 (.pptx)
theme.FOOT = "발표 제목 · 주식회사 도우"  # 모든 장 아래 한 줄

SLIDES: list[Slide] = []


def slide(title, section=""):
    s = Slide(title)
    SLIDES.append(s)
    return s


def N():
    return len(SLIDES)


SECTIONS = [("01", "첫 번째 섹션", "FIRST"), ("02", "두 번째 섹션", "SECOND")]


# ---------------------------------------------------------------- 장 정의
def s_cover():
    s = slide("표지")
    cover(s, "발표 제목을 여기에", subtitle="부제 한 줄", label="행사명 · 2026. 1. 1.",
          accent="제목", meta=[("일시", "2026. 1. 1."), ("장소", "본사"), ("발표", "주식회사 도우")])
    s.notes = "발표자 노트: 이 장에서 실제로 말할 문장."


def s_agenda():
    s = slide("발표 순서")
    agenda(s, SECTIONS, N())


def s_div1():
    s = slide("간지 · 첫 번째 섹션")
    divider(s, SECTIONS, 0, N())


def s_example():
    s = slide("예시 본문")
    s.add(header("FIRST", "한 장에 메시지 하나", "제목 아래 한 문장으로 이 장의 결론을 먼저 말합니다."))
    stat_row(s, CONTENT_TOP, [("3", "개", "핵심 숫자 설명"), ("100", "%", "두 번째 숫자"), ("12", "주", "세 번째 숫자")])
    s.add(footer(N()))


def s_closing():
    s = slide("맺음")
    closing(s, [("check-circle", "약속 한 문장")], paras("요약 문단 하나."))


BUILD = [s_cover, s_agenda, s_div1, s_example, s_closing]
