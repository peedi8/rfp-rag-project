from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_loader import parse_hwp, parse_pdf


DEFAULT_BATCH = Path(
    "eval/parallel_runs/20260707_152625_L121-selected-project-scripted-batch-builder/"
    "batch/questions_l121_selected_project_secondary_variants.json"
)
DEFAULT_CORPUS = Path("data/원본 데이터/data_list.csv")

NOT_FOUND_MARKERS = (
    "확인할 수 없습니다",
    "확인되지",
    "확인 불가",
    "문서에 없습니다",
    "명시되어 있지",
    "찾을 수 없습니다",
)

GLOBAL_NOT_FOUND_MARKERS = (
    "그 외 항목",
    "나머지 항목",
    "위 항목 외",
    "문서에 없는 항목",
)

FIELD_GROUPS: dict[str, list[dict[str, Any]]] = {
    "Q046": [
        {"id": "external_integration", "label": "외부 시스템 연계", "tokens": ["연계", "연동", "인터페이스", "망간", "망간전송"]},
        {"id": "api", "label": "API", "tokens": ["API", "OpenAPI", "REST", "SOAP", "웹서비스"]},
        {"id": "data_migration", "label": "데이터 이관", "tokens": ["데이터 이관", "마이그레이션", "연동모듈", "재개발"]},
    ],
    "Q047": [
        {"id": "server", "label": "서버", "tokens": ["서버", "인프라", "H/W", "하드웨어"]},
        {"id": "database", "label": "DB", "tokens": ["DB", "DBMS", "데이터베이스"]},
        {"id": "network", "label": "네트워크", "tokens": ["네트워크", "망간", "소내망", "트래픽", "VPN"]},
        {"id": "cloud", "label": "클라우드", "tokens": ["클라우드", "Cloud", "CSAP"]},
        {"id": "security_equipment", "label": "보안장비", "tokens": ["보안장비", "방화벽", "침입방지", "IPS", "DLP", "안티바이러스"]},
    ],
    "Q048": [
        {"id": "database", "label": "데이터베이스", "tokens": ["DB", "DBMS", "데이터베이스"]},
        {"id": "code", "label": "코드", "tokens": ["코드", "소스코드", "프로그램"]},
        {"id": "statistics", "label": "통계", "tokens": ["통계", "현황", "집계"]},
        {"id": "log_history", "label": "로그/이력관리", "tokens": ["로그", "이력", "기록", "사용이력", "인증이력"]},
    ],
    "Q049": [
        {"id": "user_screen", "label": "사용자 화면", "tokens": ["사용자 화면", "사용자 웹페이지", "웹페이지", "화면"]},
        {"id": "admin_screen", "label": "관리자 화면", "tokens": ["관리자 화면", "관리자", "관리화면"]},
        {"id": "responsive_web", "label": "반응형 웹", "tokens": ["반응형", "웹 표준", "모바일"]},
        {"id": "accessibility", "label": "접근성", "tokens": ["접근성", "웹 접근성", "장애인"]},
        {"id": "usability", "label": "편의성", "tokens": ["편의성", "사용성", "간소화"]},
    ],
    "Q050": [
        {"id": "privacy", "label": "개인정보", "tokens": ["개인정보", "개인 정보"]},
        {"id": "permission_management", "label": "권한관리", "tokens": ["권한", "접근권한", "소유권한", "권한관리"]},
        {"id": "log_management", "label": "로그관리", "tokens": ["로그", "이력", "기록"]},
        {"id": "encryption", "label": "암호화", "tokens": ["암호화", "암호", "OTP"]},
        {"id": "vulnerability", "label": "취약점 점검", "tokens": ["취약점", "보안약점", "점검"]},
    ],
    "Q051": [
        {"id": "test", "label": "테스트", "tokens": ["테스트", "시험", "검증"]},
        {"id": "performance", "label": "성능검증", "tokens": ["성능", "응답시간", "동시", "지연"]},
        {"id": "stability", "label": "안정성", "tokens": ["안정성", "안정화", "무중단"]},
        {"id": "failure_response", "label": "장애 대응", "tokens": ["장애", "복구", "오류", "재시도"]},
    ],
    "Q052": [
        {"id": "deployment", "label": "배포", "tokens": ["배포", "설치", "납품", "적용"]},
        {"id": "operation_transition", "label": "운영 전환", "tokens": ["운영 전환", "전환", "안정화"]},
        {"id": "monitoring", "label": "모니터링", "tokens": ["모니터링", "감시", "상시운영"]},
        {"id": "disaster_recovery", "label": "장애 복구", "tokens": ["장애 복구", "복구", "백업", "DR"]},
    ],
    "Q053": [
        {"id": "data_migration", "label": "기존 데이터 이관/마이그레이션", "tokens": ["데이터 이관", "마이그레이션", "기존 데이터", "이관"]},
    ],
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_corpus(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def raw_text_for(row: dict[str, str], corpus_csv: Path) -> tuple[str, str]:
    filename = (row.get("파일명") or "").strip()
    if not filename:
        return row.get("텍스트", ""), "csv_text_no_filename"
    path = corpus_csv.parent / "files" / filename
    if not path.exists():
        return row.get("텍스트", ""), "csv_text_raw_missing"
    try:
        if filename.lower().endswith(".hwp"):
            text = parse_hwp(path)
        elif filename.lower().endswith(".pdf"):
            text = parse_pdf(path)
        else:
            text = ""
    except Exception:
        return row.get("텍스트", ""), "csv_text_raw_parse_failed"
    if text.strip():
        return text, "raw_file_text"
    return row.get("텍스트", ""), "csv_text_raw_empty"


def find_source_text(
    corpus: list[dict[str, str]],
    corpus_csv: Path,
    org: str,
    title: str,
) -> tuple[dict[str, str] | None, str, str]:
    for row in corpus:
        if row.get("발주 기관") == org and row.get("사업명") == title:
            text, source_basis = raw_text_for(row, corpus_csv)
            return row, text, source_basis
    for row in corpus:
        if org in row.get("발주 기관", "") and title in row.get("사업명", ""):
            text, source_basis = raw_text_for(row, corpus_csv)
            return row, text, source_basis
    return None, "", "source_not_found"


def snippets(text: str, tokens: list[str], limit: int = 3, radius: int = 48) -> list[str]:
    found: list[str] = []
    seen = set()
    for token in tokens:
        pattern = re.escape(token)
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            start = max(0, match.start() - radius)
            end = min(len(text), match.end() + radius)
            snippet = " ".join(text[start:end].split())
            if snippet not in seen:
                found.append(snippet)
                seen.add(snippet)
            if len(found) >= limit:
                return found
    return found


def token_hits(text: str, tokens: list[str]) -> list[str]:
    return [token for token in tokens if re.search(re.escape(token), text, flags=re.IGNORECASE)]


def has_not_found_near(answer: str, tokens: list[str], label: str) -> bool:
    normalized = " ".join((answer or "").split())
    if not normalized:
        return False
    if any(marker in normalized for marker in GLOBAL_NOT_FOUND_MARKERS) and any(
        marker in normalized for marker in NOT_FOUND_MARKERS
    ):
        return True
    needles = list(dict.fromkeys([label, *tokens]))
    for needle in needles:
        for match in re.finditer(re.escape(needle), normalized, flags=re.IGNORECASE):
            window = normalized[max(0, match.start() - 120) : match.end() + 160]
            if any(marker in window for marker in NOT_FOUND_MARKERS):
                return True
    return False


def answer_padding_issues(answer: str, groups: list[dict[str, Any]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for group in groups:
        if group["source_status"] != "not_found_expected":
            continue
        hits = token_hits(answer, group["tokens"])
        caveat = has_not_found_near(answer, group["tokens"], group["label"])
        if hits and not caveat:
            issues.append(
                {
                    "field_group": group["id"],
                    "issue": "unsupported_padding_risk",
                    "detail": f"answer mentions absent tokens without a nearby not-found caveat: {', '.join(hits)}",
                }
            )
        elif not caveat:
            issues.append(
                {
                    "field_group": group["id"],
                    "issue": "missing_not_found_caveat",
                    "detail": "field was requested but source text has no matching evidence and answer has no explicit absence caveat",
                }
            )
    return issues


def analyze_case(case: dict[str, Any], corpus: list[dict[str, str]], corpus_csv: Path) -> dict[str, Any]:
    source_case_id = case["source_case_id"]
    org = (case.get("target_orgs") or [""])[0]
    title = case.get("target_biz", "")
    row, source_text, source_basis = find_source_text(corpus, corpus_csv, org, title)
    csv_text = row.get("텍스트", "") if row else ""
    groups = []
    for spec in FIELD_GROUPS.get(source_case_id, []):
        hits = token_hits(source_text, spec["tokens"])
        csv_hits = token_hits(csv_text, spec["tokens"])
        status = "source_visible" if hits else "not_found_expected"
        groups.append(
            {
                "field_group": spec["id"],
                "label": spec["label"],
                "tokens": spec["tokens"],
                "source_status": status,
                "csv_source_status": "source_visible" if csv_hits else "not_found_expected",
                "hit_tokens": hits,
                "csv_hit_tokens": csv_hits,
                "hit_count": len(hits),
                "snippets": snippets(source_text, spec["tokens"]),
                "expected_answer_behavior": (
                    "answer may summarize only with cited source text"
                    if status == "source_visible"
                    else "answer should explicitly say this field is not found in the provided document"
                ),
            }
        )
    absent = sum(1 for g in groups if g["source_status"] == "not_found_expected")
    present = len(groups) - absent
    return {
        "id": case["id"],
        "source_case_id": source_case_id,
        "question": case.get("resolved_one_turn") or (case.get("turns") or [""])[-1],
        "target_org": org,
        "target_biz": title,
        "source_found": row is not None,
        "source_filename": row.get("파일명", "") if row else "",
        "source_text_length": len(source_text),
        "source_basis": source_basis,
        "field_groups": groups,
        "present_group_count": present,
        "absent_group_count": absent,
        "diagnostic_label": "secondary_sparse_technical_guarded_diagnostic",
        "promotion_blocker": (
            "diagnostic_only; do not aggregate into ordinary EDD unless sparse-field scorer is explicitly enabled"
        ),
        "guard_pass_condition": (
            "For every not_found_expected group, the answer must either give a nearby not-found caveat "
            "or use a clear global not-found statement for all remaining requested fields."
        ),
    }


def run_fixtures(analyzed_cases: list[dict[str, Any]]) -> dict[str, Any]:
    sample = next((c for c in analyzed_cases if c["absent_group_count"] > 0), None)
    rows = []
    groups = []
    if sample:
        groups = [
            {
                "id": group["field_group"],
                "label": group["label"],
                "tokens": group["tokens"],
                "source_status": group["source_status"],
            }
            for group in sample["field_groups"]
        ]
    else:
        groups = [
            {
                "id": "synthetic_absent_api",
                "label": "API",
                "tokens": ["API", "REST", "SOAP"],
                "source_status": "not_found_expected",
            },
            {
                "id": "synthetic_absent_cloud",
                "label": "클라우드",
                "tokens": ["클라우드", "CSAP"],
                "source_status": "not_found_expected",
            },
        ]

    if groups:
        absent_groups = [g for g in groups if g["source_status"] == "not_found_expected"]
        absent_label = absent_groups[0]["label"]
        unsupported_answer = f"{absent_label} 요구사항은 REST API 엔드포인트와 클라우드 운영 구조로 제공됩니다."
        caveated_answer = "\n".join(
            f"- {group['label']}: 제공된 문서에서 확인할 수 없습니다."
            for group in absent_groups
        )
        rows.append(
            {
                "id": "unsupported_absent_field_is_flagged",
                "passed": bool(answer_padding_issues(unsupported_answer, groups)),
                "observed": answer_padding_issues(unsupported_answer, groups),
            }
        )
        rows.append(
            {
                "id": "all_absent_fields_with_not_found_caveats_pass",
                "passed": not answer_padding_issues(caveated_answer, groups),
                "observed": answer_padding_issues(caveated_answer, groups),
            }
        )
        rows.append(
            {
                "id": "global_not_found_caveat_passes",
                "passed": not answer_padding_issues("확인된 항목은 근거로 정리하고, 그 외 항목은 제공된 문서에서 확인할 수 없습니다.", groups),
                "observed": answer_padding_issues(
                    "확인된 항목은 근거로 정리하고, 그 외 항목은 제공된 문서에서 확인할 수 없습니다.",
                    groups,
                ),
            }
        )
    passed = sum(1 for row in rows if row["passed"])
    return {
        "schema": "rfp_rag_sparse_field_guard_fixture_results.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "summary": {
            "fixtures": len(rows),
            "passed": passed,
            "failed": len(rows) - passed,
            "status": "pass" if passed == len(rows) else "fail",
        },
        "fixtures": rows,
    }


def write_csv(path: Path, analyzed_cases: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = [
            "id",
            "source_case_id",
            "target_org",
            "target_biz",
            "field_group",
            "label",
            "source_status",
            "csv_source_status",
            "hit_tokens",
            "csv_hit_tokens",
            "snippets",
            "expected_answer_behavior",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for case in analyzed_cases:
            for group in case["field_groups"]:
                writer.writerow(
                    {
                        "id": case["id"],
                        "source_case_id": case["source_case_id"],
                        "target_org": case["target_org"],
                        "target_biz": case["target_biz"],
                        "field_group": group["field_group"],
                        "label": group["label"],
                        "source_status": group["source_status"],
                        "csv_source_status": group["csv_source_status"],
                        "hit_tokens": ";".join(group["hit_tokens"]),
                        "csv_hit_tokens": ";".join(group["csv_hit_tokens"]),
                        "snippets": " || ".join(group["snippets"]),
                        "expected_answer_behavior": group["expected_answer_behavior"],
                    }
                )


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# L122 Sparse-Field Guard",
        "",
        result["claim"],
        "",
        "## Summary",
    ]
    for key, value in result["summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Policy",
            "- This is a no-API preflight and scoring guard, not an answer-quality or EDD point.",
            "- Secondary technical variants remain diagnostic-only.",
            "- A not-found field is not a model failure by itself. It becomes a failure only if the answer fills the empty field with unsupported detail or omits the required absence caveat.",
            "",
            "## Cases",
            "| case | source | basis | present | not-found expected |",
            "|---|---|---|---:|---:|",
        ]
    )
    for case in result["cases"]:
        lines.append(
            f"| {case['id']} | {case['source_case_id']} | {case['source_basis']} | {case['present_group_count']} | {case['absent_group_count']} |"
        )
    lines.extend(["", "## Not-Found Field Groups", "| case | field | status | hit tokens |", "|---|---|---|---|"])
    for case in result["cases"]:
        for group in case["field_groups"]:
            if group["source_status"] == "not_found_expected":
                lines.append(
                    f"| {case['id']} | {group['label']} | {group['source_status']} | {', '.join(group['hit_tokens']) or '-'} |"
                )
    return "\n".join(lines).rstrip() + "\n"


def write_svg(path: Path, cases: list[dict[str, Any]]) -> None:
    width = 980
    height = 80 + len(cases) * 34
    max_value = max((len(c["field_groups"]) for c in cases), default=1)
    rows = []
    for i, case in enumerate(cases):
        y = 56 + i * 34
        present_w = int(420 * case["present_group_count"] / max_value)
        absent_w = int(420 * case["absent_group_count"] / max_value)
        label = html.escape(case["source_case_id"])
        rows.extend(
            [
                f'<text x="18" y="{y + 18}" font-size="13" font-family="Arial">{label}</text>',
                f'<rect x="120" y="{y}" width="{present_w}" height="20" fill="#2f7d62" rx="3" />',
                f'<rect x="{120 + present_w}" y="{y}" width="{absent_w}" height="20" fill="#bf6b3d" rx="3" />',
                f'<text x="560" y="{y + 15}" font-size="12" font-family="Arial">present {case["present_group_count"]} / not-found {case["absent_group_count"]}</text>',
            ]
        )
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#f8f8f5" />',
            '<text x="18" y="28" font-size="18" font-family="Arial" font-weight="700">L122 Sparse-Field Guard</text>',
            '<rect x="120" y="38" width="18" height="10" fill="#2f7d62" /><text x="144" y="47" font-size="12" font-family="Arial">source-visible groups</text>',
            '<rect x="300" y="38" width="18" height="10" fill="#bf6b3d" /><text x="324" y="47" font-size="12" font-family="Arial">not-found expected groups</text>',
            *rows,
            "</svg>",
        ]
    )
    path.write_text(svg + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a no-API sparse-field guard preflight.")
    parser.add_argument("--batch", type=Path, default=DEFAULT_BATCH)
    parser.add_argument("--corpus-csv", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    cases = read_json(args.batch)
    corpus = load_corpus(args.corpus_csv)
    target_cases = [
        case
        for case in cases
        if case.get("variant_claim") == "secondary sparse-technical seed to test not-found behavior"
    ]
    analyzed_cases = [analyze_case(case, corpus, args.corpus_csv) for case in target_cases]
    status_counts = Counter(
        group["source_status"]
        for case in analyzed_cases
        for group in case["field_groups"]
    )
    csv_status_counts = Counter(
        group["csv_source_status"]
        for case in analyzed_cases
        for group in case["field_groups"]
    )
    fixture_result = run_fixtures(analyzed_cases)
    result = {
        "schema": "rfp_rag_sparse_field_guard.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "claim": "No-API sparse-field readiness guard; not an answer run and not an EDD point.",
        "source_batch": str(args.batch),
        "source_corpus_csv": str(args.corpus_csv),
        "summary": {
            "case_count": len(analyzed_cases),
            "field_group_count": sum(len(c["field_groups"]) for c in analyzed_cases),
            "source_visible_groups": status_counts.get("source_visible", 0),
            "not_found_expected_groups": status_counts.get("not_found_expected", 0),
            "csv_source_visible_groups": csv_status_counts.get("source_visible", 0),
            "csv_not_found_expected_groups": csv_status_counts.get("not_found_expected", 0),
            "cases_with_not_found_expected": sum(1 for c in analyzed_cases if c["absent_group_count"] > 0),
            "fixture_status": fixture_result["summary"]["status"],
        },
        "scoring_policy": {
            "diagnostic_only": True,
            "ordinary_edd_exclusion": True,
            "failure_when": [
                "answer invents unsupported detail for a not_found_expected group",
                "answer omits an absence caveat for a requested group that is not found in the selected source document",
            ],
            "non_failure_when": [
                "source text has no evidence for a requested group and the answer clearly says it is not found",
                "answer gives present groups with source grounding and groups the remaining absent fields under a clear not-found statement",
            ],
            "source_basis_warning": (
                "Sparse-field labels must use raw_file_text or retrieval trace where available. CSV-only text can mark fields absent "
                "that are visible in the raw HWP/PDF body."
            ),
        },
        "cases": analyzed_cases,
        "fixtures": fixture_result,
    }

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "sparse_field_guard_results.json", result)
    write_json(out_dir / "sparse_field_guard_fixtures.json", fixture_result)
    write_csv(out_dir / "sparse_field_guard_results.csv", analyzed_cases)
    (out_dir / "sparse_field_guard_results.md").write_text(render_markdown(result), encoding="utf-8")
    write_svg(out_dir / "sparse_field_guard_chart.svg", analyzed_cases)

    enriched = []
    by_id = {case["id"]: case for case in analyzed_cases}
    for case in target_cases:
        guard = by_id[case["id"]]
        enriched.append(
            {
                **case,
                "diagnostic_label": guard["diagnostic_label"],
                "promotion_blocker": guard["promotion_blocker"],
                "sparse_field_guard": {
                    "source_visible_groups": [
                        group for group in guard["field_groups"] if group["source_status"] == "source_visible"
                    ],
                    "not_found_expected_groups": [
                        group for group in guard["field_groups"] if group["source_status"] == "not_found_expected"
                    ],
                    "guard_pass_condition": guard["guard_pass_condition"],
                },
            }
        )
    write_json(out_dir / "questions_l122_secondary_technical_guarded.json", enriched)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0 if fixture_result["summary"]["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
