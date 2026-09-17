"""
pptx 안에 글꼴을 심는다(font embedding).

구글 슬라이드는 자기가 가진 Noto Sans KR 을 쓰고, 파워포인트(맥·윈도우)는
파일에 심어 둔 글꼴을 쓴다. 그래서 어느 쪽에서 열어도 같은 모양이 나온다.

용량을 줄이려고 실제 쓰인 글자만 남겨서 심는다(subset).
파워포인트는 굵기를 regular / bold 두 가지로만 저장하므로 두 벌만 심으면 된다.
"""
from __future__ import annotations

import os
import re
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
FONT_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"

# 화면에 안 보여도 넣어 두는 기본 글자 — 나중에 슬라이드에서 직접 타이핑할 때 대비
BASE_CHARS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    " .,:;!?'\"()[]{}<>/\\|-–—_+=*&%#@~`^$·…①②③④⑤⑥⑦⑧⑨⑩"
    "가각간갈감갑값강개객거건걸검것게겨격견결경계고곡곤골공과관광교구국군권귀규균그극근글금급기긴길김"
    "나낙난날남내너넣년노논높놓뇌누는능니다단달담답당대댁더던데도독돈동되된두드득든들등디따딸때또"
    "라락란람랑래략량러런럴럼렁레려력련렬령례로록론료룡루류륙륜률르른를름리린링마막만많말망매맥먼멀메며"
    "면명몇모목몫못무문물미민밀바박반받발밤방배백뱀버번벌범법베변별병보복본볼봄부북분불붙브비빈빌빠빨"
    "사삭산살삼상새색생서석선설섬섭성세소속손솔송쇄수숙순술숨쉬스슬습승시식신실심십싶쌓써쓰씨"
    "아악안앉않알암압앞애액야약양어억언얻얼업없엇엉에여역연열염엽영예오옥온올옮옵와완외요욕용우운울움웃원월"
    "위유육윤율은을음응의이익인일임입있잇자작잔잘잠잡장재쟁저적전절점접정제조족존종좌죄주죽준줄중즉즐증지직진질집짓"
    "차착찬참창찾채책처척천철첨청체초촉총최추축출충취측층치칙친침칭"
    "카커컨컴켜코콘쿠크클키타탁탄탈탐탑태택터턴테통투트특틀틱팀파판팔패퍼페편평폐포폭표품풍프플피필하학한할함합항해핵행향허험헤현혈협형혜호혹혼홀화확환활황회획횡효후훈휘휴흐흔흡흥희"
)


def _subset(src: str, dst: str, chars: str) -> None:
    from fontTools import subset

    opts = subset.Options()
    opts.name_IDs = ["*"]
    opts.name_legacy = True
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    opts.recommended_glyphs = True
    opts.layout_features = ["*"]
    opts.drop_tables = []
    opts.hinting = True
    font = subset.load_font(src, opts)
    ss = subset.Subsetter(options=opts)
    ss.populate(text=chars)
    ss.subset(font)
    subset.save_font(font, dst, opts)
    font.close()


def embed(pptx_path: str, typeface: str, used_chars: set[str], quiet: bool = False) -> bool:
    """성공하면 True. 준비물이 없으면 원본을 그대로 두고 False."""
    reg_src = os.path.join(FONT_DIR, "NotoSansKR-400.ttf")
    bold_src = os.path.join(FONT_DIR, "NotoSansKR-700.ttf")
    if typeface != "Noto Sans KR" or not (os.path.exists(reg_src) and os.path.exists(bold_src)):
        return False
    try:
        from fontTools import subset  # noqa: F401
    except ImportError:
        return False

    chars = "".join(sorted(set(used_chars) | set(BASE_CHARS)))
    tmp_dir = os.path.join(HERE, ".fontcache")
    os.makedirs(tmp_dir, exist_ok=True)
    reg_out = os.path.join(tmp_dir, "reg.ttf")
    bold_out = os.path.join(tmp_dir, "bold.ttf")
    _subset(reg_src, reg_out, chars)
    _subset(bold_src, bold_out, chars)

    with open(reg_out, "rb") as f:
        reg_data = f.read()
    with open(bold_out, "rb") as f:
        bold_data = f.read()

    src = zipfile.ZipFile(pptx_path, "r")
    infos = src.infolist()
    data = {i.filename: src.read(i.filename) for i in infos}
    src.close()

    # 1) [Content_Types].xml — fntdata 확장자 등록
    ct = data["[Content_Types].xml"].decode("utf-8")
    if "fntdata" not in ct:
        ct = ct.replace(
            "<Types ",
            "<Types ", 1)
        ct = re.sub(r"(<Types[^>]*>)",
                    r'\1<Default Extension="fntdata" ContentType="application/x-fontdata"/>',
                    ct, count=1)
        data["[Content_Types].xml"] = ct.encode("utf-8")

    # 2) 관계 파일 — 새 rId 두 개
    rels_name = "ppt/_rels/presentation.xml.rels"
    rels = data[rels_name].decode("utf-8")
    used_ids = [int(n) for n in re.findall(r'Id="rId(\d+)"', rels)] or [0]
    rid_reg, rid_bold = f"rId{max(used_ids) + 1}", f"rId{max(used_ids) + 2}"
    add = (f'<Relationship Id="{rid_reg}" Type="{FONT_REL}" Target="fonts/font1.fntdata"/>'
           f'<Relationship Id="{rid_bold}" Type="{FONT_REL}" Target="fonts/font2.fntdata"/>')
    rels = rels.replace("</Relationships>", add + "</Relationships>")
    data[rels_name] = rels.encode("utf-8")

    # 3) presentation.xml — embeddedFontLst 삽입 (스키마 순서상 notesSz 다음)
    pres_name = "ppt/presentation.xml"
    pres = data[pres_name].decode("utf-8")
    if "<p:embeddedFontLst>" in pres:
        return False
    block = (
        "<p:embeddedFontLst><p:embeddedFont>"
        f'<p:font typeface="{typeface}" pitchFamily="34" charset="-127"/>'
        f'<p:regular r:id="{rid_reg}"/><p:bold r:id="{rid_bold}"/>'
        "</p:embeddedFont></p:embeddedFontLst>"
    )
    m = re.search(r"<p:notesSz[^>]*/>", pres)
    if not m:
        return False
    pres = pres[:m.end()] + block + pres[m.end():]
    if "saveSubsetFonts=" not in pres:
        pres = re.sub(r"(<p:presentation\b)", r'\1 saveSubsetFonts="1"', pres, count=1)
    data[pres_name] = pres.encode("utf-8")

    # 4) 글꼴 파트 추가 후 다시 압축
    data["ppt/fonts/font1.fntdata"] = reg_data
    data["ppt/fonts/font2.fntdata"] = bold_data

    order = [i.filename for i in infos] + ["ppt/fonts/font1.fntdata", "ppt/fonts/font2.fntdata"]
    tmp = pptx_path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for name in order:
            out.writestr(name, data[name])
    shutil.move(tmp, pptx_path)

    if not quiet:
        print(f"글꼴 embed: {typeface} · 글자 {len(chars)}자 · "
              f"regular {len(reg_data) // 1024}KB + bold {len(bold_data) // 1024}KB")
    return True
