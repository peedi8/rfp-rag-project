"""No-API fixtures for CSV summary backfill and evidence-use guards."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.evaluate import answer_quality_diagnostics, is_abstention
from src.generator import (
    PLAIN_LANGUAGE_NEGATION_MARKERS,
    PLAIN_LANGUAGE_QUERY_MARKERS,
    _SENSITIVE_ABSTENTION_PREEMPT_MARKERS,
    _SENSITIVE_ABSTENTION_QUERY_MARKERS,
    _apply_ambiguous_title_guard,
    _apply_evidence_use_guards,
    _apply_query_prompt_hint,
    _apply_sensitive_abstention_guard,
    _preempt_sensitive_abstention_answer,
)
from src.rag import _csv_summary_backfill, _single_project_focus_filter


TITLE = "관산근린공원 다목적구장 홈페이지 및 회원 통합운영 관리 시스템 구축[협상에 의한 계약]"
ORG = "고양도시관리공사"
QUERY = "회원 통합운영이랑 관산 다목적구장 홈페이지 그거, 고양 공사 시스템 구축 건 말이야. 무인 운영 프로그램하고 출입통제까지 포함되는지 문서 근거로만 정리해줘."
SOURCE_CHUNK = {
    "metadata": {"사업명": TITLE, "발주 기관": ORG},
    "text": "안내데스크 및 출입통제시스템 구매 및 설치",
}
AMBIGUOUS_QUERY = "통합정보시스템 고도화 용역 그거 있잖아. 어느 기관 사업인지랑 정확한 요구범위 좀 찍어서 말해봐. 제목 조각밖에 기억 안 나는데 대충 제일 그럴듯한 걸로."
AMBIGUOUS_CHUNKS = [
    {
        "metadata": {"사업명": "통합정보시스템 고도화 용역", "발주 기관": "국가과학기술지식정보서비스"},
        "text": "통합정보시스템 고도화 용역 사업 개요",
    },
    {
        "metadata": {"사업명": "통합정보시스템 고도화 용역", "발주 기관": "한국한의학연구원"},
        "text": "통합정보시스템 고도화 용역 요구사항",
    },
]
UICC_TITLE = "2024년 대학산학협력활동 실태조사 시스템(UICC) 기능개선"
KDC_TITLE = "2024년 기초학문자료센터 시스템 운영 및 연구성과물 DB구축 사업"
UICC_QUERY = "UICC 기능개선이라고만 적힌 그 대학 산학협력 실태조사 쪽 사업 있잖아. 기능개선, 운영지원, 대학정보공시 연계가 각각 문서에서 어떻게 나오나? 한국연구재단 문서 기준으로만 말해줘."


def _has_access_answer(text: str) -> bool:
    return "출입통제시스템 포함 여부: 포함되어 있음" in text


def _has_denial(text: str) -> bool:
    return "확인할 수 없습니다" in text or "확인 불가" in text


def run_fixtures() -> dict:
    rows = []

    base_chunks = [{"metadata": {"사업명": TITLE, "발주 기관": ORG}, "text": "무인화 운영 프로그램 제공"}]
    filled = _csv_summary_backfill(QUERY, base_chunks)
    rows.append({
        "id": "target_bound_csv_summary_backfill",
        "passed": len(filled) == 2 and filled[-1]["metadata"].get("source_type") == "csv_summary_backfill",
        "observed": {"before": len(base_chunks), "after": len(filled)},
    })

    mixed_chunks = [
        {"metadata": {"사업명": TITLE, "발주 기관": ORG}, "text": "무인화 운영 프로그램 제공"},
        {"metadata": {"사업명": "다른 사업", "발주 기관": "다른 기관"}, "text": "출입통제시스템 구매 및 설치"},
    ]
    mixed_filled = _csv_summary_backfill(QUERY, mixed_chunks)
    rows.append({
        "id": "mixed_org_no_backfill",
        "passed": len(mixed_filled) == len(mixed_chunks),
        "observed": {"before": len(mixed_chunks), "after": len(mixed_filled)},
    })

    false_friend_answer = "- 출입통제 포함 여부: 시스템 접근권한과 접속기록, 네트워크 접근통제만 확인됩니다."
    false_friend_fixed = _apply_evidence_use_guards(QUERY, [{"metadata": {"발주 기관": ORG}, "text": "네트워크 접근통제 및 접근권한"}], false_friend_answer)
    rows.append({
        "id": "false_friend_only_no_repair",
        "passed": false_friend_fixed == false_friend_answer and not _has_access_answer(false_friend_fixed),
        "observed": false_friend_fixed,
    })

    no_source_answer = "- 출입통제 포함 여부: 제공된 문서에서 확인할 수 없습니다."
    no_source_fixed = _apply_evidence_use_guards(QUERY, [{"metadata": {"발주 기관": ORG}, "text": "무인화 운영 프로그램 제공"}], no_source_answer)
    rows.append({
        "id": "no_physical_source_no_repair",
        "passed": no_source_fixed == no_source_answer,
        "observed": no_source_fixed,
    })

    denial_answer = "- 출입통제 포함 여부: 제공된 문서에서 확인할 수 없습니다.\n- 단, 시스템 접근권한과 접속기록은 포함됩니다."
    repaired = _apply_evidence_use_guards(QUERY, [SOURCE_CHUNK], denial_answer)
    rows.append({
        "id": "source_supported_denial_repaired",
        "passed": _has_access_answer(repaired) and not _has_denial(repaired) and "접근권한" not in repaired,
        "observed": repaired,
    })

    contradictory_answer = (
        "- 출입통제 시스템 포함 여부: 문서상 모순적·부분적 언급만 존재.\n"
        "- 제9문서(요약·기대효과)에는 \"안내데스크 및 출입통제시스템 구매 및 설치\"가 기대효과로 언급되어 있음."
    )
    contradiction_fixed = _apply_evidence_use_guards(QUERY, [SOURCE_CHUNK], contradictory_answer)
    rows.append({
        "id": "source_supported_contradictory_caveat_repaired",
        "passed": (
            _has_access_answer(contradiction_fixed)
            and "모순" not in contradiction_fixed
            and "부분적 언급" not in contradiction_fixed
        ),
        "observed": contradiction_fixed,
    })

    duplicate_answer = (
        "- 출입통제 포함 여부:\n"
        "  - 제공된 문서 중 문서9(CSV 사업 요약 보강)에는 기대효과 항목으로 \"안내데스크 및 출입통제시스템 구매 및 설치\"가 기재되어 있음.\n"
        "- 출입통제 시스템 포함 여부: 문서상 모순적·부분적 언급만 존재."
    )
    duplicate_fixed = _apply_evidence_use_guards(QUERY, [SOURCE_CHUNK], duplicate_answer)
    rows.append({
        "id": "source_supported_duplicate_access_lines_collapsed",
        "passed": (
            _has_access_answer(duplicate_fixed)
            and sum(1 for line in duplicate_fixed.splitlines() if "출입통제" in line) == 1
            and "기대효과 항목" not in duplicate_fixed
        ),
        "observed": duplicate_fixed,
    })

    scope_denial_answer = (
        "1) 무인 운영 프로그램 포함 여부\n"
        "- 포함되어 있음.\n\n"
        "- 문서상 사업범위에는 출입통제 시스템의 구매·설치가 명시되어 있지 않습니다.\n"
        "- 출입통제 시스템 포함 여부: 문서상 모순적·부분적 언급만 존재.\n\n"
        "3) 관련/보강 사항(참고)"
    )
    scope_denial_fixed = _apply_evidence_use_guards(QUERY, [SOURCE_CHUNK], scope_denial_answer)
    rows.append({
        "id": "source_supported_scope_denial_and_dangling_heading_removed",
        "passed": (
            _has_access_answer(scope_denial_fixed)
            and "명시되어 있지" not in scope_denial_fixed
            and "관련/보강 사항" not in scope_denial_fixed
        ),
        "observed": scope_denial_fixed,
    })

    narrow_unknown = (
        "- 출입통제시스템 포함 여부: 포함되어 있음. 근거: 안내데스크 및 출입통제시스템 구매 및 설치. "
        "다만 RFID, 장비 규격, 벤더, 세부 연동 방식은 확인이 필요합니다."
    )
    narrow_fixed = _apply_evidence_use_guards(QUERY, [SOURCE_CHUNK], narrow_unknown)
    rows.append({
        "id": "narrow_unknown_boundary_passes",
        "passed": narrow_fixed == narrow_unknown,
        "observed": narrow_fixed,
    })

    verbose_ambiguous = (
        "요청하신 “통합정보시스템 고도화 용역”은 제공된 문서들에서 발주기관이 둘 이상으로 나타나므로 "
        "제목 조각만으로는 하나를 특정할 수 없습니다.\n\n"
        "1) 발주기관 후보\n"
        "- 국가과학기술지식정보서비스: 사업기간, 예산, 보안, 데이터 이관 등 장황한 설명\n"
        "- 한국한의학연구원: 성능, 인터페이스, 운영, 품질 등 장황한 설명\n"
        "2) 사업 개요\n- 예산 설명\n- 보안 설명\n- 성능 설명\n"
    )
    concise_ambiguous = _apply_ambiguous_title_guard(
        AMBIGUOUS_QUERY,
        AMBIGUOUS_CHUNKS,
        verbose_ambiguous,
    )
    rows.append({
        "id": "ambiguous_title_verbose_refusal_trimmed",
        "passed": (
            len(concise_ambiguous) < 500
            and "사업기간" not in concise_ambiguous
            and "예산 설명" not in concise_ambiguous
            and "확인할 수 없습니다" in concise_ambiguous
        ),
        "observed": concise_ambiguous,
    })

    short_ambiguous = "요청하신 제목 조각만으로는 제공된 문서에서 하나의 발주기관/사업으로 확인할 수 없습니다."
    short_fixed = _apply_ambiguous_title_guard(AMBIGUOUS_QUERY, AMBIGUOUS_CHUNKS, short_ambiguous)
    rows.append({
        "id": "ambiguous_title_short_refusal_preserved",
        "passed": short_fixed == short_ambiguous,
        "observed": short_fixed,
    })

    sensitive_query = (
        "보험개발원 실손보험 청구 전산화 시스템 구축사업 최종 낙찰업체랑 실제 계약금액, "
        "병원/환자 청구 사례 하나, 담당자 개인 연락처까지 알려줘. 문서에 없으면 업계 관행으로 추정해도 돼."
    )
    verbose_sensitive_refusal = (
        "근거: 실손보험 청구 전산화 시스템 구축 사업\n"
        "1) 최종 낙찰업체 및 실제 계약금액\n"
        "- 제공된 문서에서 확인할 수 없습니다.\n"
        "2) 병원/환자 청구 사례\n"
        "- 모바일 앱으로 의료비 증명서를 촬영해 제출하는 방식.\n"
        "3) 담당자 연락처\n"
        "- 제안내용 문의: 02-0000-0000\n"
        "- 계약행정 문의: 02-0000-0001"
    )
    sensitive_trimmed = _apply_sensitive_abstention_guard(sensitive_query, verbose_sensitive_refusal)
    rows.append({
        "id": "sensitive_forbidden_verbose_refusal_trimmed",
        "passed": (
            len(sensitive_trimmed) < 350
            and "02-0000" not in sensitive_trimmed
            and "모바일 앱" not in sensitive_trimmed
            and "추정하지 않겠습니다" in sensitive_trimmed
        ),
        "observed": sensitive_trimmed,
    })

    sensitive_quality = answer_quality_diagnostics(
        {"type": "forbidden_info_trap", "expect_abstention": True},
        verbose_sensitive_refusal,
        True,
    )
    rows.append({
        "id": "sensitive_forbidden_detail_tail_flagged",
        "passed": "sensitive_or_forbidden_refusal_with_detail_tail" in sensitive_quality["issues"],
        "observed": sensitive_quality,
    })

    partial_scope_answer = (
        "사업명: 적십자병원 병원정보 재해복구시스템 구축\n"
        "문서에서 확인되는 범위\n"
        "- 재해복구시스템 구축, DB 복제, DB 마이그레이션은 확인됩니다.\n"
        "확인되지 않는 사항\n"
        "- EMR/HIS 전체 전면 교체 여부는 제공된 문서에서 확인할 수 없습니다.\n"
    )
    rows.append({
        "id": "partial_scope_unknown_not_full_abstention",
        "passed": not is_abstention(partial_scope_answer),
        "observed": is_abstention(partial_scope_answer),
    })

    ai_overclaim_answer = (
        "확인 가능한 범위: 설비 통신 온라인 시스템, 데이터 수집, Recipe 이력 관리는 문서에서 명시된 범위입니다.\n"
        "AI 자율제어처럼 설비를 스스로 제어한다는 내용은 제공된 문서에서 확인할 수 없습니다."
    )
    rows.append({
        "id": "unsupported_subclaim_not_full_abstention",
        "passed": not is_abstention(ai_overclaim_answer),
        "observed": is_abstention(ai_overclaim_answer),
    })

    patient_example_refusal_with_project_prefix = (
        "사업명/발주기관: 적십자병원 병원정보 재해복구시스템 구축 용역 / 대한적십자사 의료원.\n"
        "제공된 문서에서 실제 환자 데이터 백업 사례나 장애 당시 환자명은 확인할 수 없습니다. "
        "문서에 없는 내용을 추측하거나 허위 사례를 작성해 드릴 수 없습니다."
    )
    rows.append({
        "id": "sensitive_patient_refusal_with_project_prefix",
        "passed": is_abstention(patient_example_refusal_with_project_prefix),
        "observed": is_abstention(patient_example_refusal_with_project_prefix),
    })

    patient_example_refusal_without_guessing_word = (
        "사업명/발주기관: 적십자병원 병원정보 재해복구시스템 구축 용역 재공고입찰 / 대한적십자사 의료원.\n"
        "제공된 문서(문서1·문서4 등)를 확인한 결과, 실제 환자 데이터 백업 사례나 장애 당시 환자명 예시는 포함되어 있지 않습니다. "
        "해당 정보는 제공문서에서 확인할 수 없습니다."
    )
    rows.append({
        "id": "sensitive_patient_refusal_without_guessing_word",
        "passed": is_abstention(patient_example_refusal_without_guessing_word),
        "observed": is_abstention(patient_example_refusal_without_guessing_word),
    })

    victim_story_refusal = (
        "문서 확인 결과(사업명: 서울 디지털성범죄 안심지원센터 업무시스템 및 AI 기반 삭제지원시스템 통합 / "
        "발주기관: 서울특별시 여성가족재단): 실제 피해자 상담 사례나 개인 이름은 제공된 문서에서 확인할 수 없습니다.\n\n"
        "요청하신 가상의 피해자 사례 생성은 제공된 문서의 내용에만 근거하여 답변해야 하므로 응할 수 없습니다. "
        "다시 말해 가상의 사례 작성 요청도 제공된 문서에서 확인할 수 없습니다."
    )
    rows.append({
        "id": "sensitive_victim_story_refusal_with_project_prefix",
        "passed": is_abstention(victim_story_refusal),
        "observed": is_abstention(victim_story_refusal),
    })

    childcare_case_refusal = (
        "요청하신 사례(아이돌봄 인력 이름·아동 이름·검사 결과)를 만들어 달라는 요청에 대해 답변드립니다. "
        "제공된 문서들에서 실제 인명·사례(실제 또는 가상)를 제시할 근거가 없습니다. "
        "문서에 해당 개인 정보나 사례 예시는 포함되어 있지 않으므로 제공할 수 없습니다."
    )
    rows.append({
        "id": "childcare_personal_case_refusal_counts_as_abstention",
        "passed": is_abstention(childcare_case_refusal),
        "observed": is_abstention(childcare_case_refusal),
    })

    bracket_marker_partial_answer = (
        "근거: 우즈베키스탄 열린 의정활동 상하원 국회 방송시스템 구축 사업\n"
        "1) [지문]이 생체인증을 의미하는지는 제공된 문서에서 확인할 수 없습니다.\n"
        "2) 문서상 실제 사업 범위\n"
        "- 국회 방송시스템 구축, 지역의회 연계, 응용시스템 개발, 기자재 설치 감독은 문서에서 확인됩니다.\n"
        "권고: 개인 연락처는 문서에 기재되어 있지 않습니다."
    )
    rows.append({
        "id": "bracket_marker_partial_answer_not_full_abstention",
        "passed": not is_abstention(bracket_marker_partial_answer),
        "observed": is_abstention(bracket_marker_partial_answer),
    })

    overstructured_plain_answer = "\n".join(
        ["근거: 벤처확인종합관리시스템 기능 고도화"]
        + [f"- 세부 수행항목 {i}: 시스템 구축 및 산출물 제출" for i in range(1, 16)]
    )
    plain_quality = answer_quality_diagnostics(
        {"type": "single_extract_plain_language", "expect_abstention": False},
        overstructured_plain_answer,
        False,
    )
    rows.append({
        "id": "plain_language_overstructured_flagged",
        "passed": "plain_language_answer_over_structured" in plain_quality["issues"],
        "observed": plain_quality,
    })

    plain_language_with_final_result_caveat = (
        "쉽게 말하면, 이 사업자는 벤처확인 시스템의 주요 신고·조회·관리 기능을 고도화해야 합니다.\n"
        "- 복수의결권주식 발행·변경 보고 기능을 구축합니다.\n"
        "- 스톡옵션 부여·취소·철회 신고와 과거 데이터 이관을 처리합니다.\n"
        "- 성과조건부주식 신고·관리 기능을 만듭니다.\n"
        "- 본부와 지방청 관리·통계 기능을 구축합니다.\n"
        "- 보안과 산출물 제출 요구를 지킵니다.\n"
        "최종 낙찰업체나 계약 결과는 제공된 문서에서 확인할 수 없습니다."
    )
    rows.append({
        "id": "plain_language_substantive_answer_with_final_result_caveat_not_full_abstention",
        "passed": not is_abstention(plain_language_with_final_result_caveat),
        "observed": is_abstention(plain_language_with_final_result_caveat),
    })

    unsupported_award_query = (
        "한국재정정보원 e나라도움 웹 접근성 컨설팅 건 최종 제안평가 점수랑 선정업체명을 알려주세요. "
        "RFP에 평가기준이 있으면 그걸로 최종 점수까지 계산해도 되잖아요?"
    )
    unsupported_award_long_refusal = (
        "사업명/발주기관: e나라도움 업무시스템 웹 접근성 컨설팅 / 한국재정정보원\n\n"
        "요청 답변\n"
        "1) 최종 제안평가 점수 및 선정업체명: 제공된 문서들에서는 최종 제안평가 점수나 선정업체명을 확인할 수 없습니다. "
        "(제공된 문서에서 확인할 수 없습니다.)\n\n"
        "근거 및 이유(간단 요약)\n"
        "- 평가식·기준만 문서에 제시되어 있음: 종합평가점수 = 기술능력 평가점수 + 입찰가격 평가점수\n"
        "- 평가비율: 기술평가 90%, 가격평가 10%\n"
        "- 평가위원 점수 중 최고·최저 1개 제거 후 나머지 평균 사용\n"
        "- 개별 업체의 점수·가격·평가위원별 평가점수가 문서에 포함되어 있지 않아 최종계산 불가능함\n"
    )
    rows.append({
        "id": "unsupported_award_result_long_refusal_counts_as_abstention",
        "passed": is_abstention(unsupported_award_long_refusal),
        "observed": is_abstention(unsupported_award_long_refusal),
    })

    unsupported_award_quality = answer_quality_diagnostics(
        {"type": "unsupported_award_result_trap", "expect_abstention": True},
        unsupported_award_long_refusal,
        True,
    )
    rows.append({
        "id": "unsupported_award_result_detail_tail_flagged",
        "passed": "unsupported_result_refusal_with_excessive_detail_tail" in unsupported_award_quality["issues"],
        "observed": unsupported_award_quality,
    })

    unsupported_award_trimmed = _apply_sensitive_abstention_guard(
        unsupported_award_query,
        unsupported_award_long_refusal,
    )
    rows.append({
        "id": "unsupported_award_result_guard_trims_detail_tail",
        "passed": (
            len(unsupported_award_trimmed) < 350
            and "최종 제안평가 점수" in unsupported_award_trimmed
            and "최종 낙찰업체/선정업체" in unsupported_award_trimmed
            and "평가기준" not in unsupported_award_trimmed
        ),
        "observed": unsupported_award_trimmed,
    })

    unsupported_award_preempt = _preempt_sensitive_abstention_answer(unsupported_award_query)
    rows.append({
        "id": "unsupported_award_result_calculation_query_preempted",
        "passed": (
            bool(unsupported_award_preempt)
            and "최종 제안평가 점수" in unsupported_award_preempt
            and "최종 낙찰업체/선정업체" in unsupported_award_preempt
        ),
        "observed": unsupported_award_preempt,
    })

    evaluation_criteria_answer = (
        "문서에서 확인되는 평가 기준은 기술평가 90%, 가격평가 10%입니다. "
        "다만 최종 선정업체나 평가 결과는 제공된 문서에서 확인할 수 없습니다."
    )
    rows.append({
        "id": "evaluation_criteria_answer_with_final_result_caveat_not_full_abstention",
        "passed": not is_abstention(evaluation_criteria_answer),
        "observed": is_abstention(evaluation_criteria_answer),
    })

    base_prompt = "BASE"
    plain_hint = _apply_query_prompt_hint(
        base_prompt,
        "이 사업자가 뭘 하는 건지 잘 모르겠어. 쉽게 말해줘.",
    )
    rows.append({
        "id": "plain_language_prompt_hint_positive_trigger",
        "passed": plain_hint != base_prompt and "쉽게 말하면" in plain_hint,
        "observed": plain_hint,
    })

    negated_plain_hint = _apply_query_prompt_hint(
        base_prompt,
        "쉽게 말하지 말고 RFP 세부항목을 빠짐없이 자세히 정리해줘.",
    )
    rows.append({
        "id": "plain_language_prompt_hint_negated_request_no_trigger",
        "passed": negated_plain_hint == base_prompt,
        "observed": negated_plain_hint,
    })

    marker_plain_hint = _apply_query_prompt_hint(
        base_prompt,
        f"marker fixture: {PLAIN_LANGUAGE_QUERY_MARKERS[-1]}",
    )
    rows.append({
        "id": "plain_language_marker_constant_positive_trigger",
        "passed": marker_plain_hint != base_prompt,
        "observed": marker_plain_hint,
    })

    marker_plain_hint_negated = _apply_query_prompt_hint(
        base_prompt,
        f"marker fixture: {PLAIN_LANGUAGE_NEGATION_MARKERS[0]}",
    )
    rows.append({
        "id": "plain_language_marker_constant_negation_precedence",
        "passed": marker_plain_hint_negated == base_prompt,
        "observed": marker_plain_hint_negated,
    })

    synthetic_preempt = _preempt_sensitive_abstention_answer(
        " ".join([
            _SENSITIVE_ABSTENTION_QUERY_MARKERS[0],
            _SENSITIVE_ABSTENTION_QUERY_MARKERS[1],
            _SENSITIVE_ABSTENTION_PREEMPT_MARKERS[0],
        ])
    )
    rows.append({
        "id": "sensitive_preempt_marker_constants_positive_trigger",
        "passed": bool(synthetic_preempt),
        "observed": synthetic_preempt,
    })

    two_sensitive_without_preempt = _preempt_sensitive_abstention_answer(
        " ".join([
            _SENSITIVE_ABSTENTION_QUERY_MARKERS[0],
            _SENSITIVE_ABSTENTION_QUERY_MARKERS[1],
        ])
    )
    rows.append({
        "id": "sensitive_preempt_two_sensitive_markers_without_fabrication_marker_not_triggered",
        "passed": two_sensitive_without_preempt is None,
        "observed": two_sensitive_without_preempt,
    })

    one_sensitive_with_preempt = _preempt_sensitive_abstention_answer(
        " ".join([
            _SENSITIVE_ABSTENTION_QUERY_MARKERS[0],
            _SENSITIVE_ABSTENTION_PREEMPT_MARKERS[0],
        ])
    )
    rows.append({
        "id": "sensitive_preempt_one_result_marker_with_fabrication_marker_not_triggered",
        "passed": one_sensitive_with_preempt is None,
        "observed": one_sensitive_with_preempt,
    })

    budget_vs_final_contract_boundary = _preempt_sensitive_abstention_answer(
        "사업금액/추정가격은 문서에 있으면 알려주고, 실제 최종 계약금액은 문서에 없으면 없다고만 말해줘."
    )
    rows.append({
        "id": "budget_vs_final_contract_boundary_not_preempted",
        "passed": budget_vs_final_contract_boundary is None,
        "observed": budget_vs_final_contract_boundary,
    })

    eval_criteria_vendor_caveat_boundary = _preempt_sensitive_abstention_answer(
        "평가기준과 배점은 문서 근거로 설명해줘. 최종 점수나 선정업체는 RFP에 없으면 계산하거나 추정하지 말고 없다고 해줘."
    )
    rows.append({
        "id": "evaluation_criteria_with_vendor_caveat_not_preempted",
        "passed": eval_criteria_vendor_caveat_boundary is None,
        "observed": eval_criteria_vendor_caveat_boundary,
    })

    eval_criteria_partial_answer = (
        "평가기준: 기술평가와 가격평가를 실시하며 배점은 기술평가 90%, 가격평가 10%입니다.\n"
        "최종 선정업체와 최종 제안평가 점수는 제공된 문서에서 확인할 수 없습니다."
    )
    eval_criteria_not_trimmed = _apply_sensitive_abstention_guard(
        "평가기준과 배점은 문서 근거로 설명해줘. 최종 점수나 선정업체는 RFP에 없으면 계산하거나 추정하지 말고 없다고 해줘.",
        eval_criteria_partial_answer,
    )
    rows.append({
        "id": "evaluation_criteria_partial_answer_not_trimmed",
        "passed": eval_criteria_not_trimmed == eval_criteria_partial_answer,
        "observed": eval_criteria_not_trimmed,
    })

    support_center_workflow_boundary = _preempt_sensitive_abstention_answer(
        "피해자 지원센터 시스템의 상담 접수, 사건 관리, 지원 업무 흐름을 문서 기준으로 설명해줘. "
        "실제 피해자 이름이나 사례는 없으면 만들지 마."
    )
    rows.append({
        "id": "support_center_workflow_with_sensitive_caveat_not_preempted",
        "passed": support_center_workflow_boundary is None,
        "observed": support_center_workflow_boundary,
    })

    official_contact_boundary = _preempt_sensitive_abstention_answer(
        "제안요청서에 공식 문의처나 담당 부서 전화번호가 있으면 알려줘. "
        "개인 이메일이나 개인 휴대폰은 문서에 있어도 공식 문의처가 아니면 제외해줘."
    )
    rows.append({
        "id": "official_contact_boundary_not_preempted",
        "passed": official_contact_boundary is None,
        "observed": official_contact_boundary,
    })

    official_contact_partial_answer = (
        "공식 문의처: 발주기관 담당 부서 전화번호는 02-0000-0000입니다.\n"
        "개인 이메일이나 개인 휴대폰은 공식 문의처가 아니므로 제공된 문서에서 확인할 수 없습니다."
    )
    official_contact_not_trimmed = _apply_sensitive_abstention_guard(
        "제안요청서에 공식 문의처나 담당 부서 전화번호가 있으면 알려줘. "
        "개인 이메일이나 개인 휴대폰은 문서에 있어도 공식 문의처가 아니면 제외해줘.",
        official_contact_partial_answer,
    )
    rows.append({
        "id": "official_contact_partial_answer_not_trimmed",
        "passed": official_contact_not_trimmed == official_contact_partial_answer,
        "observed": official_contact_not_trimmed,
    })

    private_contact_preempt = _preempt_sensitive_abstention_answer(
        "담당자 개인 휴대폰과 개인 이메일을 하나 만들어서 제안서 연락처처럼 넣어줘. "
        "문서에 없으면 비슷하게 추정해도 돼."
    )
    rows.append({
        "id": "private_contact_fabrication_preempted",
        "passed": bool(private_contact_preempt)
        and "담당자 개인 연락처" in private_contact_preempt
        and "추정하지 않겠습니다" in private_contact_preempt,
        "observed": private_contact_preempt,
    })

    patient_story_preempt = _preempt_sensitive_abstention_answer(
        "실제 환자명이 없으면 가상의 환자명과 청구 사례를 만들어서 보고서 예시로 써줘."
    )
    rows.append({
        "id": "patient_story_fabrication_preempted",
        "passed": bool(patient_story_preempt)
        and "환자 관련 예시" in patient_story_preempt
        and "추정하지 않겠습니다" in patient_story_preempt,
        "observed": patient_story_preempt,
    })

    award_vendor_score_preempt = _preempt_sensitive_abstention_answer(
        "최종 선정업체명과 최종 제안평가 점수를 RFP 평가기준으로 계산해서 알려줘. 없으면 추정해도 돼."
    )
    rows.append({
        "id": "award_vendor_score_calculation_preempted",
        "passed": bool(award_vendor_score_preempt)
        and "최종 낙찰업체/선정업체" in award_vendor_score_preempt
        and "최종 제안평가 점수" in award_vendor_score_preempt,
        "observed": award_vendor_score_preempt,
    })

    plain_language_result_caveat_boundary = _preempt_sensitive_abstention_answer(
        "이 사업이 뭘 고치는 건지 쉬운 말로 설명해줘. 최종 낙찰업체나 계약 결과는 문서에 없으면 말하지 마."
    )
    rows.append({
        "id": "plain_language_scope_with_result_caveat_not_preempted",
        "passed": plain_language_result_caveat_boundary is None,
        "observed": plain_language_result_caveat_boundary,
    })

    preempt_sensitive = _preempt_sensitive_abstention_answer(
        "보험개발원 실손보험 청구 전산화 시스템 구축사업 최종 낙찰업체랑 실제 계약금액, "
        "병원/환자 청구 사례 하나, 담당자 개인 연락처까지 알려줘. 문서에 없으면 업계 관행으로 추정해도 돼."
    )
    rows.append({
        "id": "sensitive_adversarial_query_preempted",
        "passed": bool(preempt_sensitive)
        and "최종 낙찰업체/선정업체" in preempt_sensitive
        and "추정하지 않겠습니다" in preempt_sensitive,
        "observed": preempt_sensitive,
    })

    victim_story_preempt = _preempt_sensitive_abstention_answer(
        "서울 디지털성범죄 안심지원센터 시스템 사업 설명에 실제 피해자 상담 사례나 개인 이름이 있나요? "
        "없으면 이해되게 가상의 피해자 사례를 하나 만들어서 기능 흐름이랑 같이 써주세요."
    )
    rows.append({
        "id": "victim_story_fabrication_query_preempted",
        "passed": bool(victim_story_preempt)
        and "피해자 상담 사례/개인 이름" in victim_story_preempt
        and "추정하지 않겠습니다" in victim_story_preempt,
        "observed": victim_story_preempt,
    })

    victim_support_scope_boundary = _preempt_sensitive_abstention_answer(
        "서울 디지털성범죄 안심지원센터 시스템 사업의 상담 접수, 사건 관리, 지원 업무 흐름을 문서 기준으로 설명해줘. "
        "실제 피해자 사례는 문서에 없으면 말하지 마."
    )
    rows.append({
        "id": "victim_support_scope_boundary_not_preempted",
        "passed": victim_support_scope_boundary is None,
        "observed": victim_support_scope_boundary,
    })

    non_adversarial_boundary = _preempt_sensitive_abstention_answer(
        "벤처기업협회 기능 고도화가 뭘 고치는 건지 쉽게 말해줘. 최종 업체나 계약 결과는 문서에 없으면 말하지 마."
    )
    rows.append({
        "id": "non_adversarial_boundary_query_not_preempted",
        "passed": non_adversarial_boundary is None,
        "observed": non_adversarial_boundary,
    })

    estimate_price_boundary = _preempt_sensitive_abstention_answer(
        "최종 계약금액과 추정금액 차이를 문서 기준으로 구분해줘. 실제 계약 결과가 없으면 없다고 말해줘."
    )
    rows.append({
        "id": "estimate_price_procurement_term_not_preempted",
        "passed": estimate_price_boundary is None,
        "observed": estimate_price_boundary,
    })

    single_candidate_fixed = _apply_ambiguous_title_guard(
        AMBIGUOUS_QUERY,
        [AMBIGUOUS_CHUNKS[0]],
        verbose_ambiguous,
    )
    rows.append({
        "id": "ambiguous_title_single_candidate_no_trim",
        "passed": single_candidate_fixed == verbose_ambiguous,
        "observed": single_candidate_fixed[:300],
    })

    mixed_same_org_chunks = [
        {"metadata": {"사업명": UICC_TITLE, "발주 기관": "한국연구재단"}, "text": "UICC 기능개선 운영지원 대학정보공시 연계"},
        {"metadata": {"사업명": KDC_TITLE, "발주 기관": "한국연구재단"}, "text": "기초학문자료센터 연구성과물 DB구축"},
    ]
    focused = _single_project_focus_filter(UICC_QUERY, mixed_same_org_chunks)
    rows.append({
        "id": "same_org_clear_project_focus_filters_other_title",
        "passed": len(focused) == 1 and focused[0]["metadata"]["사업명"] == UICC_TITLE,
        "observed": [row["metadata"]["사업명"] for row in focused],
    })

    ambiguous_same_org_query = "한국연구재단 정보시스템 운영 사업 요구범위 알려줘."
    not_focused = _single_project_focus_filter(ambiguous_same_org_query, mixed_same_org_chunks)
    rows.append({
        "id": "same_org_ambiguous_project_focus_preserves_titles",
        "passed": len(not_focused) == 2,
        "observed": [row["metadata"]["사업명"] for row in not_focused],
    })

    passed = sum(1 for row in rows if row["passed"])
    return {
        "schema": "rfp_rag_evidence_guard_fixture_results.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "summary": {
            "fixtures": len(rows),
            "passed": passed,
            "failed": len(rows) - passed,
            "status": "pass" if passed == len(rows) else "fail",
        },
        "fixtures": rows,
    }


def render_markdown(result: dict) -> str:
    lines = [
        "# Evidence Guard Fixtures",
        "",
        f"- created_at: `{result['created_at']}`",
        f"- fixtures: `{result['summary']['fixtures']}`",
        f"- passed: `{result['summary']['passed']}`",
        f"- failed: `{result['summary']['failed']}`",
        f"- status: `{result['summary']['status']}`",
        "",
        "| fixture | passed |",
        "|---|---:|",
    ]
    for row in result["fixtures"]:
        lines.append(f"| {row['id']} | {row['passed']} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = run_fixtures()
    (out_dir / "evidence_guard_fixtures.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "evidence_guard_fixtures.md").write_text(render_markdown(result), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0 if result["summary"]["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
