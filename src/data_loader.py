"""데이터 로딩.

두 가지 소스 지원:
- source="csv" : data_list.csv 의 '텍스트' 컬럼 사용 (빠르지만 원문 일부만, 문서당 ~3.8천자)
- source="raw" : 원본 hwp/pdf 를 직접 파싱 (전체 본문, 문서당 수만 자). 메타데이터는 CSV에서 매칭.
소스는 config.DATA_SOURCE 기본값을 따르며, load_documents(source=...) 로 덮어쓸 수 있다.
"""
from __future__ import annotations
import re
import struct
import zlib
import pandas as pd
import config

META_COLUMNS = [
    "공고 번호", "공고 차수", "사업명", "사업 금액", "발주 기관",
    "공개 일자", "입찰 참여 시작일", "입찰 참여 마감일", "사업 요약",
    "파일형식", "파일명",
]


def _build_meta(row) -> dict:
    meta = {}
    for col in META_COLUMNS:
        val = row.get(col)
        meta[col] = "" if pd.isna(val) else (val if isinstance(val, (int, float, bool)) else str(val))
    return meta


def _make_doc_id(row, i, seen: dict) -> str:
    raw = row.get("공고 번호")
    if pd.isna(raw) or not str(raw).strip():
        doc_id = f"row{i}"
    elif isinstance(raw, float) and float(raw).is_integer():
        doc_id = str(int(raw))
    else:
        doc_id = str(raw).strip()
    if doc_id in seen:
        seen[doc_id] += 1
        doc_id = f"{doc_id}-{seen[doc_id]}"
    else:
        seen[doc_id] = 0
    return doc_id


def _is_empty(t) -> bool:
    if t is None:
        return True
    if not isinstance(t, str):
        return bool(pd.isna(t))
    return not t.strip()


def load_documents(source: str = None) -> list[dict]:
    """CSV를 기준으로 문서 리스트 반환. source="raw"면 원본 파일 본문을 파싱해 사용."""
    source = source or getattr(config, "DATA_SOURCE", "csv")
    df = pd.read_csv(config.CSV_PATH)
    docs, seen = [], {}
    n_raw_ok = 0
    for i, row in df.iterrows():
        text = _load_raw_text(row) if source == "raw" else row.get("텍스트")
        if source == "raw" and not _is_empty(text):
            n_raw_ok += 1
        if _is_empty(text):                      # raw 실패 시 CSV 텍스트로 폴백
            text = row.get("텍스트")
        if _is_empty(text):
            continue
        docs.append({
            "doc_id": _make_doc_id(row, i, seen),
            "text": str(text),
            "metadata": _build_meta(row),
        })
    if source == "raw":
        print(f"   (원본 파싱 성공 {n_raw_ok}건, 나머지는 CSV 텍스트로 폴백)")
    return docs


def _load_raw_text(row) -> str | None:
    """행의 파일명으로 원본 파일을 찾아 본문을 파싱한다. 실패하면 None."""
    fn = str(row.get("파일명", "")).strip()
    if not fn:
        return None
    path = config.FILES_DIR / fn
    if not path.exists():
        return None
    try:
        if fn.lower().endswith(".pdf"):
            return parse_pdf(path)
        if fn.lower().endswith(".hwp"):
            return parse_hwp(path)
    except Exception:
        return None
    return None


# ---------------------------------------------------------------------------
# 원본 파서
# ---------------------------------------------------------------------------
def parse_pdf(path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    txt = "\n".join((p.extract_text() or "") for p in reader.pages)
    return _clean(txt)


# HWP 본문 텍스트의 인라인 컨트롤(8 워드 차지) / 무시 컨트롤 문자 코드
_CTRL_8WORD = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23}
_CTRL_SKIP = {10, 24, 25, 26, 27, 28, 29, 30, 31}


def parse_hwp(path) -> str:
    """HWP 5.x(OLE) 본문 텍스트 추출. 인라인 컨트롤 문자를 제대로 건너뛰어 잡음을 제거한다."""
    import olefile
    f = olefile.OleFileIO(str(path))
    dirs = f.listdir()
    if ["FileHeader"] not in dirs:
        f.close()
        raise ValueError("올바른 HWP 파일 아님")
    header = f.openstream("FileHeader").read()
    is_compressed = (header[36] & 1) == 1
    sections = sorted(
        int(d[1][len("Section"):]) for d in dirs
        if d[0] == "BodyText" and d[1].startswith("Section")
    )
    out = []
    for sec in sections:
        data = f.openstream(f"BodyText/Section{sec}").read()
        if is_compressed:
            data = zlib.decompress(data, -15)
        i, size = 0, len(data)
        while i < size:
            hv = struct.unpack_from("<I", data, i)[0]
            tag = hv & 0x3FF
            length = (hv >> 20) & 0xFFF
            if tag == 67:  # HWPTAG_PARA_TEXT
                raw = data[i + 4:i + 4 + length]
                units = struct.unpack_from("<%dH" % (len(raw) // 2), raw, 0)
                j, buf = 0, []
                n = len(units)
                while j < n:
                    c = units[j]
                    if c == 13:            # 문단 끝
                        buf.append("\n"); j += 1
                    elif c in _CTRL_8WORD:  # 인라인/확장 컨트롤 = 8 워드
                        j += 8
                    elif c in _CTRL_SKIP:
                        j += 1
                    elif 0xD800 <= c <= 0xDBFF and j + 1 < n and 0xDC00 <= units[j + 1] <= 0xDFFF:
                        # 상위+하위 서로게이트 쌍 → BMP 밖 문자로 결합
                        cp = 0x10000 + ((c - 0xD800) << 10) + (units[j + 1] - 0xDC00)
                        buf.append(chr(cp)); j += 2
                    elif 0xD800 <= c <= 0xDFFF:
                        j += 1              # 외톨이 서로게이트는 버림
                    else:
                        buf.append(chr(c)); j += 1
                out.append("".join(buf))
            i += 4 + length
    f.close()
    return _clean("\n".join(out))


def _clean(text: str) -> str:
    text = text.replace("\x00", " ")
    # 외톨이 서로게이트 등 UTF-8 인코딩 불가 문자 제거 (OpenAI API 전송 안전 보장)
    text = text.encode("utf-8", "ignore").decode("utf-8", "ignore")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
