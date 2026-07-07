# RFP RAG Report Evidence Pack

- created_at: 2026-07-06T14:47:11
- source_run_dir: `I:\0706\rfp-rag-project\eval\parallel_runs\20260706_134254_RFP-RAG-parallel-EDD-full-run-after-abstention-fix`
- questions_path: `I:\0706\rfp-rag-project\eval\questions.json`

## Top Experiments

| rank | suite | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | mmr_lambda_sweep | lambda05_top8_filter_rewrite_control | 96.57 | 1.0 | 1.0 | 4.667 | 5.0 | 0.0 | 0.0 | 17.251 |
| 2 | topk_sweep | topk5_filter_rewrite | 96.53 | 1.0 | 1.0 | 5.0 | 5.0 | 0.0 | 0.0 | 23.269 |
| 3 | fetchk_sweep | fetch20_top8_filter_rewrite_control | 95.62 | 1.0 | 1.0 | 4.8 | 5.0 | 0.0 | 0.0 | 23.739 |
| 4 | topk_sweep | topk12_filter_rewrite | 93.52 | 1.0 | 1.0 | 4.333 | 5.0 | 0.0 | 0.0 | 24.79 |
| 5 | fetchk_sweep | fetch40_top8_filter_rewrite | 93.13 | 1.0 | 1.0 | 4.0 | 5.0 | 0.0 | 0.0 | 20.617 |
| 6 | mmr_lambda_sweep | lambda03_top8_filter_rewrite | 93.08 | 1.0 | 1.0 | 4.5 | 5.0 | 0.0 | 0.0 | 29.628 |
| 7 | filter_rewrite_ablation | filter_on_rewrite_on_control | 91.21 | 1.0 | 1.0 | 3.75 | 4.75 | 0.0 | 0.0 | 20.287 |
| 8 | topk_sweep | topk8_filter_rewrite_control | 91.03 | 0.875 | 0.875 | 4.75 | 5.0 | 0.0 | 0.0 | 18.297 |
| 9 | filter_rewrite_ablation | filter_on_rewrite_off | 88.93 | 0.875 | 0.812 | 4.667 | 5.0 | 0.0 | 0.0 | 21.961 |
| 10 | filter_rewrite_ablation | filter_off_rewrite_on | 82.85 | 0.75 | 0.604 | 5.0 | 5.0 | 0.111 | 0.0 | 16.998 |

## Reading Rule

- A high EDD score is not accepted as final proof by itself.
- Each sample keeps the question, answer excerpt, retrieval trace, automatic metrics, flags, and interpretation together.
- Full answers are stored in `report_evidence.json`; this Markdown file keeps excerpts readable.

## Evidence Cases

### lambda05_top8_filter_rewrite_control

#### q1_single_extract - top_experiment_full_question_set

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "2024년 이러닝시스템 운영 용역", 발주기관 국민연금공단(제공된 문서 기준)

요구사항 요약(핵심만)

1) 요구사항 체계(제안요청서 상 항목)
- 교육운영(FUR): FUR-001 ~ FUR-005(예: 역량모델 기반 TRM 제시, 교육운영 방법·예상인원, 외부콘텐츠 기준 등).  
- 품질(QUR): QUR-001(교육콘텐츠 평가·품질관리 방안 제시).  
- 이러닝시스템 운영(SFR): SFR-001~SFR-008(예: 시스템 구축·관리 기본방향, 사이버·모바일 연수원, 학습 이벤트, 큐레이션, 소셜러닝, 나의 학습노트, 직무지식진단, 역량진단).  
- 학사관리(LMR): LMR-001~LMR-002(LMS 제공, 학습참여 유인체계).  
- 콘텐츠개발(DER): DER-001~DER-003(개발 범위·요건·검사·검수).  
- 유지관리(MAR): MAR-001(관리 범위) 등.

2) 개인정보·정보보안 및 인수인계
- 정보보안·개인정보보호 규정 준수 및 보안관리 방안 제시 요구(문서6).  
- 인수인계 시 공단 보유 프로그램 및 데이터 이전 방안 제시 요구(문서6).  
- 인계·인수 절차: 인수자·인계자 간 서면 인수·인계 계획·완료확인서 제출, 인수·인계 30일 이내 완료(미흡 시 연장 가능). 퇴사(이전) 업체는 공단 관련 자료 전수파기 및 공단 직원의 폐기 완료 확인 필요(문서8).

3) 산출물·보고 및 제출시기(문서4)
- 정기보고: 착수보고서(1회), 월간업무현황보고서(월1회), 분기별 중간보고서, 최종보고서(1회).  
- 비정기(검수 완료 시 등) 산출물: 차시별 원고·스토리보드(2부), 검토결과 조치내역서, 사업완료보고서, 운영자 지침서, 유지보수 계획서, 산출물 일체(소스·스토리보드 등) 외장HDD 등.  
- 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출(심의 필요).

4) 대금지급(문서4, PMR-004)
- 콘텐츠 개발: 검수완료 후 지급.  
- 콘텐츠 및 P/G 유지보수·관리: 상·하반기 각 반기말에 지급(연2회).  
- 교육운영: 월별 또는 분기별 지급.

5) 입찰참가자격·계약방법(문서8 및 문서3 요약)
- 참가자격: 관련 법령(국가계약법령) 요건 충족, 평생교육법상 원격평생교육시설 인가 및 이러닝사업자 신고(이러닝콘텐츠업/이러닝서비스업), 나라장터 입찰참가자격 등록(업종코드 6527 또는 6529) 등.  
- 입찰방법: 일반경쟁입찰, 계약방법: 협상에 의한 계약.

6) 기타 요구사항(문서6)
- 정보보안·개인정보보호 규정 준수 방안 제시.  
- 인수인계 완료 시 공단 보유 프로그램·데이터 이전 및 보안대책 제시.

참고: 세부기능(예: SFR-002 사이버·모바일 연수원, SFR-003 학습 이벤트 등) 및 각 요구사항의 고유번호 목록은 제안요청서(문서6)에 상세 기재되어 있습
...(truncated; full text is in report_evidence.json)
```

#### q2_followup - top_experiment_full_question_set

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단 (문서2, 문서4, 문서6, 문서8, 문서3, 문서5)

콘텐츠 개발·관리 요구사항(핵심)

- 범위 및 유형 (문서6, 문서3, 문서2)
  - 직무교육, 법정의무교육, 공단 소유 콘텐츠 및 외부콘텐츠(동영상 포함), 마이크로러닝·AR/VR 등 4차산업융합 콘텐츠, 북러닝·자기개발 등 다양한 분야 포함. (문서3, 문서2, 문서6)
  - 직무교육 대상 규모 예시: 11,000명(사업범위). (문서5)

- 개발·제작 요건 (문서6, 문서2, 문서8)
  - 차시당 분량은 대체로 30~40분 내외 기준으로 콘텐츠별 상이. (문서2)
  - 콘텐츠는 PC·모바일(태블릿 포함)에서 동일 계정으로 수강 가능하도록 설계되어야 함(시스템 연계 요건). (문서8, 문서6)
  - 공단이 교육용으로 활용할 수 있도록 콘텐츠 내용을 PPT 등으로 다운로드 가능하게 구현하고, 원본·완성본을 공단(인재개발부 1부, 해당부서 1부)에 제공. (문서2, 문서4)

- 유지보수·업데이트(관리) 요구사항 (문서2, 문서6)
  - 최신 법령·지침 등 변경사항을 반영하여 상시 업데이트 가능한 관리 프로세스 운영. (문서2 MAR-002)
  - 차시별 관리, 텍스트 수정, 차시 재구성 등 수정‧보완 용이성 확보(스토리보드 활용 등). (문서2)

- 검사·검수 및 산출물 제출 (문서4, 문서6)
  - 콘텐츠 검사·검수 절차 준수(검수 완료 시 최종본 제출). (문서6, 문서4)
  - 제출 산출물: 차시별 원고·스토리보드(2부, 바인더·CD), 검토결과 조치내역서(필요 시), 사업완료보고서(2부), 운영자 지침서(2부), 유지보수 계획서(2부), 산출물 일체(소스·스토리보드 등)을 외장HDD로 제출. (문서4)
  - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출 후 심의. (문서4)

- 결제·대금 관련 (문서4 PMR-004)
  - 콘텐츠 개발비는 검수완료 후 지급. (문서4)

- 기술·구현 관련(명시된 항목) (문서2)
  - 일부 프로그램 예시 기술스택: 나의 학습노트·역량진단 등에 MS-SQL 2005, JAVA, JSP, XML, ActiveX 일부 사용 명시(세부 구현 항목). (문서2)

- 개인정보·보안·저작권 관련 (문서6, 문서4)
  - 정보보호·개인정보보호 규정 준수 및 보안관리 방안 제시 필요. (문서6, 문서4)
  - 저작권·지적재산권 보호 요구사항 표기(COR-001). 다만 구체적 권리 귀속·이전·사용범위 등 상세 조치는 제공된 문서에서 확인할 수 없습니다. (문서6)

- 품질관리·학습효과 측정 (문서8, 문서6)
  - 학습불편 및 문제제기 시 즉시 원인분석·보고 및 수정·교체 방안 제시.
  - 월별‧과정별 교육만족도·현업적용도 점검 등 성과측정 및 통계관리 방안
...(truncated; full text is in report_evidence.json)
```

#### q3_multi_topic - top_experiment_full_question_set

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 96.57; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
예. 제공된 문서에서 확인되는 교육·학습 관련 발주사업은 다음과 같습니다.

- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 — 발주기관: 인천광역시 (교육지원 요구사항 및 교육계획서 제출 의무 포함) [문서1 근거]  
- 차세대 포털·학사 정보시스템 구축사업 — 발주기관: 고려대학교 (학교현장실습 관리·이수요건 등 교직·학생 교육 관련 기능 포함) [문서3 근거]  
- 2024년 이러닝시스템 운영 용역 — 발주기관: 국민연금공단 (이러닝 콘텐츠·운영, 교육인원·평가·교재 등 상세 요구사항 포함) [문서4, 문서7, 문서8 근거]  
- 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 — 발주기관: 전북특별자치도 정읍시 (트레이닝센터 관련 운영·교육담당자·교육대상자 등 기재) [문서5 근거]  
- JST 공유대학(원) xAPI기반 LRS시스템 구축 — 발주기관: 전북대학교 (xAPI/LRS 기반 학습기록 관리 시스템 구축) [문서6 근거]

위 목록 외에 다른 기관의 교육·학습 관련 발주사업은 제공된 문서에서 확인할 수 없습니다.
```

#### q4_single_check - top_experiment_full_question_set

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나?
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 발주기관: 기초과학연구원

제공된 문서들(문서1–8)에서 AI(인공지능), 머신러닝 또는 AI 기반 예측(예: 예측모델, 예측진단 등)에 대한 명시적 요구사항은 확인할 수 없습니다. 문서에는 "주요 수치들에 대한 분석을 수행" 및 "분석 대상·방법·결과물 형태는 연구원이 정하는 바"라는 일반적 분석 요구는 있으나, 분석 방법으로서 AI 기반 예측을 명시하지는 않습니다.
```

Judge reason excerpt:

```text
검색된 근거 텍스트에서 '주요 수치들에 대한 분석을 수행' 및 '연구원이 정하는 바' 등 일반적 분석 요구는 명시되어 있으나, AI·머신러닝·예측모델 등 AI 기반 예측을 지칭하는 용어나 명시적 요구사항은 전혀 나타나지 않습니다. 답변은 근거 문서의 내용(분석 요구 존재 vs. AI 명시 부재)을 정확히 반영하고 있어 근거 기반성·질문 응답성 모두 높습니다.
```

#### q5_followup - top_experiment_full_question_set

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명/발주기관: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 기초과학연구원

요약(모니터링 업무 관련 요청사항)
- 가동기간 모니터링: 24시간 모니터링 수행(2인 1조 기본), 주간에는 감독자 1인 이상 상주(문서8).
- 모니터링 방법: 연구원에 구축된 제어시스템 또는 현장 장치를 활용하여 지속 관찰(문서8, 문서2).
- 주요 점검항목: 알람 메시지 확인, 주요 센서 트렌드(온도·압력·유량·속도 등) 확인, 정상 운전 지시값 파악, 비정상 상황 감지, 제어로직 정상 작동 여부 확인, 현장 상황 일시적/지속적 관찰 및 주기적 순찰(문서2, 문서5).
- 기록 및 분석: 주요 수치의 전자파일 기록(항목·기록 간격은 연구원이 정함, 변동 가능). 연구원 요청 시 계약자가 주요 수치에 대한 분석 수행(분석 대상·방법·결과물 형태는 연구원이 결정). 계약자는 기록·분석용 노트북·키보드·마우스 등 제공(문서2).
- 장비·교육 지원: 제어시스템 사용을 위한 컴퓨터·모니터·입력장치·책상·의자 및 기본 사용 교육은 연구원이 제공하고, 계약자는 관련 배경지식 보유 필요(문서8, 문서2).
- 통신·보고: 연구원이 지정하는 값 관찰·확인 및 상황 전달, 무전 통신 활용(무전기 연구원 제공)(문서2).
- 책임 및 응답 절차: 긴급 상황 발생 시 즉시 연구원 통보 및 연구원 지시 이행하면 계약자 책임 면제(단, 통보·지시 미준수 시 계약자 책임)(문서3).
- 기타: 제어시스템(알람 포함) 개선·보완 협조는 연구원 요청 시 한정(문서6).

근거: 상기 내용은 모두 “2025년도 중이온가속기용 극저온시스템 운전 용역 / 기초과학연구원” 과업지시서(문서2, 문서3, 문서5, 문서6, 문서8 등 제공 문서)에 근거합니다.
```

#### q6_purpose - top_experiment_full_question_set

- question: 한국 원자력 연구원에서 선량 평가 시스템 고도화 사업을 발주했는데, 이 사업이 왜 추진되는지 목적을 알려 줘.
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=4, relevance=5
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명/발주기관: 한국원자력연구원 선량평가시스템 고도화 / 한국원자력연구원 (근거: 제공문서)

목적(핵심)
- 규제요건 준수: 제한구역 경계의 연간선량 준수 여부 확인 등 원자력안전위원회 고시 대응 체계 구축(근거: 문서1).  
- 평가기법 개선: ICRP60 기반 평가장기(Organ) 및 평가장기 모듈 개선을 통한 평가정확성 향상(문서1).  
- 액체유출물 대응 기능 추가: 액체유출물에 의한 주민 피폭선량 평가 기능 추가(문서1).  
- 업무생산성 및 의사결정 지원: UI 개선 및 출력 기능 고도화를 통한 업무효율·신속한 의사결정 환경 구축(문서1).  
- 정상운전 시 규제수요 대응을 위한 K-RADAC(주민선량평가시스템) 고도화(문서3, 문서1).

문서에 없는 추가 목적은 제공된 문서에서 확인할 수 없습니다.
```

Judge reason excerpt:

```text
답변에 제시된 주요 목적(규제요건 준수, ICRP60 기반 평가장기 개선, 액체유출물에 의한 주민피폭 평가 추가, UI·출력 기능 등 업무생산성 향상, 정상운전 시 규제수요 대응)은 제공된 ‘추진배경 및 필요성’ 및 기대효과 항목과 직접 일치하여 근거에 의해 뒷받침됩니다. 다만 답변에 포함된 'K-RADAC' 표기와 '문서3' 언급은 제공된 근거문서에서 확인되지 않아 근거 밖의 추가정보로 판단되어 만점에서 감점했습니다.
```

#### q7_compare - top_experiment_full_question_set

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
요청하신 비교를 제공된 문서 내용만 근거하여 간결하게 정리합니다.

1) 사업 목적
- 고려대학교 차세대 포털·학사 정보시스템 구축사업 (발주기관: 고려대학교)
  - 노후 시스템을 차세대로 전환해 정보서비스 품질 강화 및 대학 교육시스템 경쟁력 확보 (문서1, 문서5).
- 학사시스템 기능개선 사업 (발주기관: 광주과학기술원)
  - 학사조직 개편 및 학위 연계과정 신설·과정구분 변경에 따른 시스템 개선으로 업무 편리성·효율성 제고 및 사용자 편의성 증대 (문서7).

2) 사업 범위·주요 기능
- 고려대학교 (차세대 포털·학사)
  - 포털(통합로그인, 통합·지능형 검색, 마이페이지, 공지/알림, 일정관리, 커뮤니티, 게시판, 개인화 위젯, 연계서비스(웹메일, 챗봇, 전자결재, 학사/행정) 등), 모바일 포털(기존 앱 '호잇' 하이브리드 재구축), 사용자 통합관리·SSO·간편인증·2차인증 등 전면 재구축 및 기존 기능 유지·연계 변경관리 요구(문서1, 문서6, 문서8).
- 광주과학기술원 (학사 기능개선)
  - 학사 조직개편에 따른 시스템 개선, 학위연계과정(학석연계·학석박·석→석박통합 등) 관련 메뉴·프로세스 변경 개발(학번 발급 등), 관리자·사용자 메뉴 연동 등(FUR-005, FUR-006 등 상세 요구사항 포함)(문서4, 문서7).

3) 예산·비용
- 고려대학교: 총 사업예산 11,270,000,000원(VAT 포함), 3년 분할지급(2024학년도 약 30%, 2025 약 40%, 2026 약 30%)(문서3).
- 광주과학기술원: 총 사업비 157,300,000원(VAT 포함). 세부: 설계·분석 53,000,000(설계 11M/M 표기), 개발·테스트 90,000,000 등(문서7).

4) 기간·일정
- 고려대학교: 계약일로부터 24개월 이내; 무상유지보수 12개월(문서3, 문서8).
- 광주과학기술원: 문서에 사업 착수일·총기간 명시 없음(제공된 문서에서 확인할 수 없습니다) (문서2, 문서7).

5) 계약·입찰 방식·지급조건
- 고려대학교: 제한경쟁 입찰(협상에 의한 계약), 주사업자가 일괄 제안해야 함(문서3, 문서6).
- 광주과학기술원: 공개경쟁입찰(협상에 의한 계약체결), 공동수급불가, 선금 50% 지급·잔금은 최종검수 완료시 지급(문서7).

6) 준수·품질 요구사항 및 기타 제약
- 고려대학교: 행정안전부 고시(정보시스템 구축·운영 지침), 전자정부 웹사이트 품질관리 지침 등 웹 표준·웹 접근성·시큐어코딩 준수, 개발프레임워크·표준화 요구, 기존 기능 전부 구현 및 연계 변경관리 요구(문서6).
- 광주과학기술원: 상세 요구사항·평가기준·제안서 작성 지침 등 제안요청서에 기술적 평가 및 요구사항(문서2, 문서4) — 구체적 표준 준수 항목은 문서에서 명시된 범위 외에는 확인 불가(제공된 문서에서 확인할 수 없습니다).

7)
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - top_experiment_full_question_set

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 고려대학교 (사업명: 차세대 포털·학사 정보시스템 구축사업): 있음. 문서[문서4] PER-002, PER-003에 근거하여 "모든 질의는 사용자가 요청한 시점부터 3초 이내에 결과 처리" 및 "웹페이지는 요청부터 3초 이내에 완전 출력"을 요구하고 있으며, 대량데이터(기준 5,000건 이상)·대형이미지·영상 포함 페이지 및 동시사용자 용량의 90% 초과 시 예외 규정이 명시되어 있음. (근거: 문서4)

- 광주과학기술원 (사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업 / 학사시스템 기능개선 사업): 응답시간 요구사항은 제공된 문서들에서 확인할 수 없습니다. (근거: 문서1, 문서5, 문서7)
```

#### q9_imprecise_org - top_experiment_full_question_set

- question: 원자력연구소에서 방사선량 평가하는 시스템 사업 요구사항 알려줘
- EDD: 96.57; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명: 한국원자력연구원 선량평가시스템 고도화 / 발주기관: 한국원자력연구원

요구사항(제공된 문서 기준 핵심 요약):

1. 사업 범위·기능 요구사항
- 평가장기(Organ) 개선: 포트란 모듈 및 웹시스템의 평가장기 개선(문서1).  
- 액체(유출물)에 의한 선량평가 기능 추가: 포트란 모듈 및 웹시스템에 액체선량평가 기능 추가(문서1, 문서5).  
  - 피폭경로별 평가: 외부피폭(예: 해변활동, 수상활동), 내부피폭(수산물 섭취, 음용수 섭취, 관개작물 섭취 등)(문서5 SFR-003).  
  - 평가대상: 개인선량 및 집단선량(문서5 SFR-003).  
  - 웹 UI 입력요소: 핵종, 방출량, 재농축인자; 부지특성·사회환경인자(희석수량·희석인자·섭취량·생산량·활동시간·수송기간 등)(문서5 SFR-004).  
  - 출력: 피폭경로별 선량결과 및 기준치 비교(문서5 SFR-004).  
  - DB: 생체축적인자, 선량환산인자, 부지특성인자 및 사회환경인자 구축(문서5 SFR-004).

2. 성능 요구사항
- 조회 및 계산 질의응답 시간: 사용자의 건별 질의 처리결과를 3초 이내에 화면에 보여주어야 함(문서5 PER-001).

3. 테스트 요구사항
- 단위테스트: 단위 테스트 계획서 제출(항목·방법 포함), 연구원 승인 후 시행, 연관 메뉴는 묶음으로 테스트(문서2 TER-001).  
- 통합테스트: 업무 시나리오별 통합 테스트 계획서 제출·승인 후 시행(문서2 TER-002).  
- 인수테스트: 인수 테스트 수행방법·절차·점검 후 조치방안 포함 계획 수립, 개발완료 후 최종산출물 및 테스트 결과물을 첨부해 발주자 승인검사 요청, 하자 발생 시 보완·재시험 반복(문서2 TER-003).

4. 보안·원격개발 관련 요구
- 제안요청서 명시한 비밀준수의무를 준수한 작업장 제시 가능, 발주기관이 비밀준수 불충분시 거부 가능(문서4).  
- 원격지 개발 시 보안사고 등 위험요인 식별 및 대응방안 제시 필요; 원격지 보안관리대책 구체적으로 제시해야 함(문서4).  
- SW 산출물 반출 관련: 발주기관 정보보안규정(제36조 등)에 해당하지 않는 누출금지정보(예: 기관 정보시스템의 IP 현황, 세부 시스템 구성도 등)는 제공 불가(문서4).  
- 문서2의 보안 요구사항 SER-001은 항목 존재하나 상세 내용은 제공된 문서에서 확인할 수 없습니다.

5. 프로젝트 지원·기술이전·교육·하자보수
- 교육·기술이전: 원자력연구원 자체 유지관리 가능하도록 교육계획 수립·관리자 교육 실시, 교육교재 사전 제출(문서3).  
- 기술이전 계획서: 기술이전 대상·내용(운영·경미한 장애조치·응급조치 등), 방법·기간·인원 포함하여 한국원자력연구원과 협의 후 수행(문서3 PSR-003).  
- 하자보수: 준공검사 완료일로부터 하자담보책임 12개월, 장애 접수
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
답변이 검색된 근거(문서 내 항목들: 사업명/사업범위, SFR-003·SFR-004의 기능요구, PER-001 성능요구, TER-001~003의 테스트요구, PSR-002·PSR-003의 하자보수·기술이전, 보안·원격개발·SW산출물 관련 조항 등)를 충실히 요약하고 있으며 근거에 없는 내용을 새로 창작하지 않았음. 질문(원자력연구소의 선량평가시스템 사업 요구사항 안내)에 대해 문서에 명시된 기능·성능·테스트·보안·교육·하자보수·산출물 등 핵심 요구사항을 직접적으로 정리하여 실제로 답하고 있으므로 관련성도 높음.
```

#### q10_abstention - top_experiment_full_question_set

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 96.57; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서들(문서1~문서8)에는 우주 로켓 발사 시스템 구축 사업이 없습니다. 제공된 문서 근거:

- 문서1: 사업명: 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / 발주기관: (사)부산국제영화제  
- 문서2: 사업명: [재공고] 차세대 통합정보시스템(ERP) 구축 / 발주기관: 한국가스공사  
- 문서3: 사업명: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교  
- 문서4: 사업명: 도시계획위원회 통합관리시스템 구축용역 / 발주기관: 인천광역시  
- 문서5: 사업명: 예약발매시스템 개량 ISMP 용역 / 발주기관: 한국철도공사  
- 문서6: 사업명: 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 발주기관: 인천광역시  
- 문서7: 사업명: 수협중앙회 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 / 발주기관: 수협중앙회  
- 문서8: 사업명: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교

따라서 "우주 로켓 발사 시스템 구축 사업"은 제공된 문서에서 확인할 수 없습니다.
```

### topk5_filter_rewrite

#### q1_single_extract - top_experiment_full_question_set

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "2024년 이러닝시스템 운영 용역", 발주기관 국민연금공단 (참고문서: 문서1·문서3·문서4)

확인된 요구사항(핵심만 요약)
- 보고 및 산출물 제출
  - 사업완료보고서 초안은 콘텐츠 개발 완료 최소 14일 전에 공단에 제출하여 심의(국민연금공단). (문서4)
  - 정기보고서: 착수보고서 1부(초기), 월간 업무현황보고서 월1회, 중간보고서 분기별 1회, 최종보고서 1부(국민연금공단). (문서4)
  - 비정기(산출물) 제출: 
    - 차시별 원고 및 스토리보드 2부(바인더, CD) — 검토분 및 최종본(국민연금공단). 
    - 검토결과 조치내역서 1부(바인더) — 조치사항 있을 시. 
    - 사업완료보고서 2부(바인더, CD). 
    - 운영자 지침서 2부(바인더, CD). 
    - 유지보수 계획서 2부(바인더, CD). 
    - 산출물 일체(소스, 스토리보드 등) 1부(외장HDD). (문서4)
  - 제출 방법·시기 등은 공단과 협의 후 결정 가능(국민연금공단). (문서4)

- 대금결제(프로젝트 관리 요구사항 PMR-004)
  - 콘텐츠 개발: 검수완료 후 지급(국민연금공단). 
  - 콘텐츠 및 P/G 유지보수·관리: 상/하반기 2차에 걸쳐 지급(각 반기 말). 
  - 교육운영: 월별 또는 분기별 지급(국민연금공단). (문서4)

- 기타(입찰·계약 관련 양식)
  - 입찰참가신청서·공통서류 등 제출 양식 예시 포함(문서3). (국민연금공단)

문서에 명시되어 있으나 상세 내용이 제공되지 않은 항목
- 교육과정 운영, 이러닝시스템 운영, 콘텐츠 개발·관리, 개인정보보호 및 정보보안 등 구체적 요구사항(요구기능·성능·보안요건·서비스 수준 등)은 제공된 문서들에서 상세 내용이 확인되지 않습니다. (문서1 목차 존재하나 본문 미제공)
```

#### q2_followup - top_experiment_full_question_set

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
근거: 사업명 "2024년 이러닝시스템 운영 용역", 발주기관: 국민연금공단 (문서2·문서3·문서4·문서5)

요약(문서에 명시된 콘텐츠 개발·관리 요구사항만)

- 개발 범위 및 주제(콘텐츠 유형)  
  - 직무교육 중심의 콘텐츠 개발·운영(직무 콘텐츠, 자기개발 위탁콘텐츠 포함). (근거: 문서5)  
  - AI, 빅데이터, IoT, AR/VR 등 4차 산업혁명 관련 콘텐츠, OA(최신버전)·기획·보고서 작성 등 실무형, 소통리더십·인문학·심리 등 교양형, 전화외국어·자격증 등 선택형, 북러닝(e-book 포함) 및 공공기관 연계콘텐츠 활용 등 다양화. (근거: 문서4)

- 학습형태·기술요구  
  - 마이크로러닝 기반 콘텐츠 및 온·오프 병행(블렌디드 러닝) 연계. (근거: 문서4)  
  - 모바일 포함(PC·스마트기기 동일계정 접속·수강, 실시간 교육실적 집계) 지원. (근거: 문서2 SFR-002)  
  - 학습자 맞춤형 추천(큐레이션) 및 소셜러닝(Q&A·커뮤니티) 고도화 요구. (근거: 문서2 SFR-001)

- 품질관리·운영관리  
  - 학습 불편·문제제기 발생 시 원인파악 후 즉시 보고하고 수정·보완·교체 방안 제시. (근거: 문서2)  
  - 학습만족도·현업적용도 등 월별·과정별 점검 및 교육성과 측정·통계관리 방안 제시. (근거: 문서2)  
  - 학습 필요성이 높은 콘텐츠는 유지, 세부 정비방법 및 품질관리 위원회 운영 등은 공단과 협의. (근거: 문서2)

- 변경·유지보수·하자보수  
  - 시스템 변경에 따른 콘텐츠 변환·연동 수행. (근거: 문서3)  
  - 콘텐츠 일부 수정·오탈자 정정, 자료 연계 등 관리 요구. (근거: 문서3)  
  - 하자보수: 최종검수 후 콘텐츠의 20% 범위 내에서 최소 1년 이내 지원; 계약기간 종료 후 하자보수 범위·추진체계 제시 필요. (근거: 문서3)  
  - 선정업체는 이러닝 관련 기술정보 제공 및 기술자문을 공단에 무상 지원. (근거: 문서3)

- 보고·제출 의무(개발 일정 연계)  
  - 모든 산출물·개발콘텐츠·보고서를 개발일정에 따라 제출·보고. (근거: 문서3 PMR-003)  
  - 매월 과업수행 실적 및 익월 추진계획을 익월 초까지 서면 제출 및 공단 요구 시 수시보고·회의 대응. (근거: 문서3 PMR-003)  
  - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 공단 제출 및 심의. (근거: 문서3 PMR-003)

- 준수사항  
  - 운영에는 정보보호·개인정보보호 방안 및 법령준수 포함(구체 기준·절차는 문서에 명시 없음). (근거: 문서5, 문서1 목차)

명확히 문서에서 확인되지 않는 항목(제공된 문서에서 확인할 수 없습니다)  
- 개별 콘텐츠의 분량(차시·시간), 산출물 포맷·편수·검수 기준·절차의 상세 기준, 성능(동시접속자 수·가
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
답변은 제시된 제안요청서(문서의 목차와 SFR-001·SFR-002·PMR-003 등 항목) 내용에 직접 근거하여 요약·정리하였고, 문서에 명확히 기술되지 않은 항목(차시·시간·동시접속자 수 등)은 별도로 표시하여 추정·추가정보를 생성하지 않았음. 따라서 근거에 의해 충분히 뒷받침되며 질문(콘텐츠 개발·관리 요구사항)에 적절히 답하고 있음.
```

#### q3_multi_topic - top_experiment_full_question_set

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 96.53; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서 기준으로 답변드립니다.

교육·학습 관련 발주사업(문서에서 명시된 근거와 함께)
- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 발주기관: 인천광역시  
  근거: PSR-001(교육지원) 항목(교육계획서 작성·교육실시 등) 확인됨.
- 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교  
  근거: 학교현장실습, 교직 이수요건, 성인지교육 연동 등 교육·학사 기능 명시.
- 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단  
  근거: 이러닝 콘텐츠(어학, 전화외국어, 전문자격증 등) 운영 요구사항 명시.

기타 문서 관련 사항
- 대학재정정보시스템(기본재산 및 기채 사후관리) 고도화 / 발주기관: 한국사학진흥재단  
  제공된 문서에서는 교육·학습 관련 내용 확인할 수 없습니다.
- 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 / 발주기관: 전북특별자치도 정읍시  
  문서에 '교육담당자' 서명란 등은 있으나, 교육·학습 프로그램 관련 구체적 내용은 제공된 문서에서 확인할 수 없습니다.
```

#### q4_single_check - top_experiment_full_question_set

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나?
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명/발주기관: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 기초과학연구원.

결론: 제공된 문서들(문서1–문서5)에서는 AI 기반 예측(예: 머신러닝, 예측정비, 예측모델 도입 등)에 대한 요구사항이나 명시가 없습니다. 문서에는 "주요 수치들에 대한 기록·분석(문서3·문서4)"이나 연구원 요청 시 분석 수행 등이 기재되어 있으나, AI 또는 예측 알고리즘 도입에 대한 언급은 없습니다. 따라서 AI 기반 예측 요구는 제공된 문서에서 확인할 수 없습니다.
```

Judge reason excerpt:

```text
제공된 근거에는 '주요 수치들에 대한 기록 및 분석'과 '연구원 요청 시 분석 수행' 등의 문구는 있으나 AI, 머신러닝, 예측정비, 예측모델 도입 등에 대한 명시적 언급은 없음. 답변은 이러한 근거를 바탕으로 AI 기반 예측 요구사항이 문서들에서 확인되지 않는다고 결론내고 있어 근거에 충실하게 작성됨. 단, 평가는 제공된 발췌문에 한정되며 전체 문서(또는 다른 관련 문서)에 해당 내용이 있을 경우 결과가 달라질 수 있음.
```

#### q5_followup - top_experiment_full_question_set

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명/발주기관: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 기초과학연구원

결론: 예. 제공된 과업지시서(문서들)에서 모니터링 관련 구체적 요청사항이 명시되어 있습니다.

주요 요청사항(문서4·문서1·문서5 근거):
- 주요 수치 전자기록: 주요 수치 항목 및 기록 간격은 연구원이 정함(전자파일로 기록).(문서4)
- 분석 수행: 연구원 요청 시 계약자는 주요 수치들에 대한 분석을 수행해야 하며, 분석 대상·방법·결과물 형태는 연구원이 정함.(문서4)
- 장비 제공: 기록·분석을 위해 필요한 노트북·키보드·마우스 등 컴퓨터 악세서리는 계약자가 준비.(문서4)
- 모니터링 업무 목록(표4): 알람 메시지 확인, 주요 센서 트렌드(온도·압력·유량·속도 등) 확인, 정상 지시값 숙지, 비정상 상황 감지, 연구원이 지정하는 값 관찰·상황 전달(무전 통신 활용, 무전기는 연구원 제공), 제어로직 정상 작동 여부 확인, 현장 상황 일시적·지속적 관찰(연구원 요청 시 비방사선구역 한정), 주기적 현장 순찰 등.(문서4)
- 제어시스템 개선 협조: 극저온시스템용 제어시스템(알람 포함) 개선·보완을 위한 협조는 연구원 요청 시 한정.(문서1)

문서에 없는 항목은 별도로 확인할 수 없습니다.
```

Judge reason excerpt:

```text
답변에 적힌 모든 주요 항목(주요 수치 전자기록 및 기록간격, 연구원 요청 시 분석 수행, 계약자의 노트북·키보드·마우스 준비, 표4에 제시된 모니터링 업무 목록(알람 확인, 센서 트렌드 확인, 비정상 감지, 연구원 지정값 관찰·전달(무전기 제공 포함), 제어로직 확인, 현장 관찰·주기적 순찰 등), 제어시스템 개선 협조(연구원 요청 시 한정))이 제공된 '검색된 근거' 문서 내용에 명시되어 있어 근거에 의해 잘 뒷받침됩니다. 답변은 사용자의 질문("모니터링 업무에 대한 요청사항이 있는지")에 직접적으로 응답하고 있어 관련성도 높습니다. (단, 근거의 세부 문서 번호 표기는 답변과 원문 표기에 일부 차이가 있을 수 있으나 내용적 일치는 명확합니다.)
```

#### q6_purpose - top_experiment_full_question_set

- question: 한국 원자력 연구원에서 선량 평가 시스템 고도화 사업을 발주했는데, 이 사업이 왜 추진되는지 목적을 알려 줘.
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명/발주기관: 한국원자력연구원 선량평가시스템 고도화 / 발주기관: 한국원자력연구원
근거: 문서1(1.2 추진배경·필요성, 1.4 기대효과)

목적(요약)
- 규제요건 준수: 제한구역 경계 연간선량 준수 여부 확인 체계 구축(원안위 고시 대응) 및 ICRP60 기반 평가장기 개선 필요.  
- 액체유출물 영향평가 추가: 액체유출물에 의한 주민피폭 선량평가 기능 추가 필요.  
- 업무생산성·의사결정 향상: UI 개선 및 출력 기능 고도화를 통한 업무 효율 및 신속한 의사결정 환경 구축.  
- 기대효과: 정상운전 시 선량평가 관련 규제 수요에 대응.
```

Judge reason excerpt:

```text
답변은 제공된 문서의 '1.2 추진배경 및 필요성'과 '1.4 기대효과'에 명시된 항목들을 요약한 것으로, 규제요건 준수(제한구역 경계 연간선량 확인, ICRP60 기반 개선), 액체유출물에 의한 주민피폭 선량평가 기능 추가, 업무생산성·의사결정 향상(UI·출력 기능 개선) 및 기대효과(정상운전 시 규제 수요 대응)를 그대로 반영하고 있어 근거에 기반함. 추가적인 비근거 정보는 포함되지 않음.
```

#### q7_compare - top_experiment_full_question_set

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
요청하신 비교는 제공된 문서 내용만 근거하여 작성합니다.

1) 사업명·발주기관
- (사업명: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교)  
- (사업명: 학사시스템 기능개선 사업 / 발주기관: 광주과학기술원)

2) 사업목적
- (고려대학교) 노후화된 시스템의 차세대 구축을 통해 정보서비스 품질 강화 및 대학 교육 시스템 경쟁력 확보(혁신·국제화 제고 기대). (문서1·5)
- (광주과학기술원) 학사시스템의 기능 개선—특히 학위연계과정 및 대학원 과정변경 관련 시스템 개발·프로세스 변경을 위한 개선. (문서4)
  - 기타 광범위한 목적 기술은 제공된 문서에서 확인할 수 없습니다. (광주과학기술원)

3) 사업범위·주요기능(요약)
- (고려대학교) 포털시스템 전면 구축 및 학사정보시스템 연계: 통합로그인·통합·지능형 검색·마이페이지·공지·일정·커뮤니티·게시판·위젯·연계서비스(웹메일·챗봇·전자결재·학사/행정)·개인화·SSO·간편·2차인증 등. 모바일은 기존 앱(호잇)을 하이브리드 방식으로 재구축·모바일웹·푸시 포함. (문서1)
- (광주과학기술원) 기능 단위 개선 요구사항 중심: FUR-005(학위연계과정 시스템 개발—학사 이수 후 석사·학박 통합 학번 발급 메뉴, 관리자/사용자 메뉴 연동, 프로세스 변경 등), FUR-006(대학원 과정변경 시스템 개발—석사→석박통합 등 프로세스·메뉴 연동). 성능요구(PER-001) 존재하나 상세는 문서에 제한적 기재. (문서4)

4) 대상 사용자·규모
- (고려대학교) 내부 구성원(학생·졸업생 포함, 교직원, 연구원 등). 문서에 학생·교직원 수(서울·세종 캠퍼스 합계 등)가 기재되어 있어 대규모 사용자 기반임을 확인 가능. (문서1·5)
- (광주과학기술원) 요구사항은 관리자·사용자 메뉴 연동을 명시하나, 구체적 사용자 수·규모는 제공된 문서에서 확인할 수 없습니다. (광주과학기술원)

5) 기간·유지보수·예산
- (고려대학교) 사업기간: 계약일로부터 24개월. 무상유지보수: 사업종료 후 12개월. 사업예산: 11,270,000,000원(VAT 포함, 3년 분할지급) 및 연도별 지급비율 기재. (문서3)
- (광주과학기술원) 사업기간·무상유지보수·예산 등 구체 수치는 제공된 문서에서 확인할 수 없습니다. (광주과학기술원)

6) 입찰·계약 방식
- (고려대학교) 제한 경쟁 입찰(협상에 의한 계약). (문서3)
- (광주과학기술원) 입찰방식 관련 항목이 목차에 있으나, 구체 방식(예: 제한·공개 등)은 제공된 문서에서 확인할 수 없습니다. (광주과학기술원)

7) 기술·플랫폼 관련(기재된 내용)
- (고려대학교) 기존 학사정보시스템 일부는 PowerBuilder·Java/Servlets/JSP/Ajax 등으로 운영 중이며, 포털은 기존 앱(호잇) 활용한 하이브리드 모바일 재구축 등 명시. (문서1·5
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
답변은 제공된 검색 근거 문서의 항목(사업명, 발주기관, 사업목적, 주요기능·요구사항, 사용자·규모(고려대에 대한 인원 수 기재), 기간·무상유지·예산, 입찰방식, 기술 스택 예시, 광주과학기술원의 FUR-005/FUR-006 및 담당자 등)을 근거로 요약·비교하고 있으며, 문서에 없는 세부사항은 명시적으로 '확인 불가'로 표기함. 근거에 없는 내용을 임의로 생성하지 않았고, 질문에 대한 비교(범위·목적·규모·기간·예산·기술·입찰 등)를 충실히 제공하였으므로 근거성·관련성 모두 높게 평가됩니다.
```

#### q8_compare_precise - top_experiment_full_question_set

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 고려대학교 (사업명: 차세대 포털·학사 정보시스템 구축사업): 있음. 문서(요구사항 PER-002, PER-003)에 모든 질의 및 웹페이지 출력은 사용자가 요청한 시점부터 3초 이내 처리·표시되어야 한다고 명시됨. 단, 예외로 대량데이터(기준 5,000건 이상), 대형이미지(기준 500KB 이상)·영상 포함 페이지, 동시사용자 용량의 90% 초과 시에는 미적용 또는 별도 기준을 제시해야 함(근거: 문서4).

- 광주과학기술원 (사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업·학사시스템 기능개선 사업): 제공된 문서들(문서1, 문서5)에서는 응답시간(업무응답시간/웹페이지 디스플레이 시간)에 대한 요구사항을 확인할 수 없습니다.
```

#### q9_imprecise_org - top_experiment_full_question_set

- question: 원자력연구소에서 방사선량 평가하는 시스템 사업 요구사항 알려줘
- EDD: 96.53; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
근거: 사업명 "한국원자력연구원 선량평가시스템 고도화", 발주기관: 한국원자력연구원. 아래 내용은 제공된 문서에 근거한 요구사항 요약입니다.

1) 사업개요 및 계약조건
- 기간: 계약일로부터 6개월. (한국원자력연구원)
- 사업비: 46,600천원(부가가치세 포함). (한국원자력연구원)
- 입찰: 중소기업간 제한경쟁입찰(협상에 의한 계약, 기술평가90%/가격10%). (한국원자력연구원)

2) 추진배경·필요성
- 규제 준수: 원자력안전위원회 고시(방사선방호 등) 상의 연간선량 확인 체계 필요, ICRP60 기반 평가장기 개선 필요, 액체유출물에 의한 주민피폭선량평가 필요. (한국원자력연구원)
- 업무생산성: UI 개선, 출력 기능 고도화로 업무생산성·의사결정 신속화 필요. (한국원자력연구원)

3) 사업범위(주요 기능)
- 평가장기(Organ) 개선: 포트란 모듈 및 웹시스템의 평가장기 개선. (한국원자력연구원)
- 액체유출물 선량평가 기능 추가: 포트란 모듈 및 웹시스템에 액체 선량평가 추가. (한국원자력연구원)
- 추가 요구(문서 일부): 집단선량 평가장기 추가(문서에 일부 표기). (한국원자력연구원)

4) 기능 요구사항(세부)
- 포트란 모듈 액체 선량평가(SFR-003):
  - 피폭경로별(외부: 해변·수상활동 등, 내부: 수산물·음용수·관개작물 섭취 등) 선량평가.
  - 평가대상: 개인선량 및 집단선량. (한국원자력연구원)
- 웹시스템 액체 선량평가(SFR-004):
  - UI 입력: 핵종, 방출량, 재농축인자; 희석수량·희석인자·섭취량·생산량·활동시간·수송기간 등 부지특성·사회환경인자.
  - 출력: 피폭경로별 선량결과 및 기준치 비교.
  - DB: 생체축적인자, 선량환산인자, 부지특성인자 및 사회환경인자. (한국원자력연구원)

5) 성능요구사항
- 질의응답 시간(PER-001): 데이터 조회 및 선량평가 질의 처리 결과를 3초 이내에 화면에 보여주어야 함. (한국원자력연구원)

6) 테스트요구사항
- 단위테스트(TER-001): 메뉴별 단위테스트 계획서 제출(연구원 승인 후 시행), 관련 메뉴군 구성 시 함께 테스트. (한국원자력연구원)
- 통합테스트(TER-002): 업무 시나리오별 통합테스트 계획서 제출·승인 후 시행. (한국원자력연구원)
- 인수테스트(TER-003): 인수시험 방법·절차·점검 후 조치방안 포함한 계획 수립, 개발완료 후 최종산출물 및 테스트결과 첨부해 승인검사 요청, 하자 발견 시 보완·재시험 반복. (한국원자력연구원)

7) 프로젝트 지원·유지관리·기술이전
- 교육훈련: 연구원 자체 유지관리 가능하도록 교육훈련 계획 수립·관리자 교육 실시, 교육교재는 상세히 작성해 교육 이전 제출. (한국원자력연구원)
- 하자보수(PSR-002): 하자담보 책임기간은 준공검사 완료일로부터 12개월. 장애 접수 후 24시간 이내 보수
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
groundedness: 답변은 제공된 검색 근거 문서의 항목들을 그대로 요약·정리하고 있으며(사업개요, 추진배경, 사업범위, 기능요구사항 SFR-003/SFR-004, 성능 PER-001, 테스트 TER-001~TER-003, PSR-002/PSR-003 등) 문서에 없는 정보를 새로 창작하지 않았음. relevance: 질문(원자력연구소의 방사선량 평가 시스템 사업 요구사항)에 대해 기능요구, 성능, 테스트, 유지관리·기술이전·보안·사업조건 등 주요 요구사항을 포괄적으로 답변하여 요구에 적절히 응답함(문서에 누락된 상세 인터페이스·DB 스키마 등은 언급하지 않았음을 명시함).
```

#### q10_abstention - top_experiment_full_question_set

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 96.53; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역)
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서들(사업명·발주기관 근거: 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / (사)부산국제영화제; [재공고]차세대 통합정보시스템(ERP) 구축 / 한국가스공사; 차세대 포털·학사 정보시스템 구축사업 / 고려대학교; 도시계획위원회 통합관리시스템 구축용역 / 인천광역시; 예약발매시스템 개량 ISMP 용역 / 한국철도공사)에서는 우주 로켓 발사 시스템 구축 사업을 확인할 수 없습니다.
```

### fetch20_top8_filter_rewrite_control

#### q1_single_extract - top_experiment_full_question_set

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단

요구사항 요약(핵심만, 근거 문서 명시)

1) 요구사항 분류·주요 기능(문서6)
 - 교육운영 관련(FUR-001 ~ FUR-005): 국민연금 역량모델 기반 TRM 제시, 교육운영 방법·예상인원, 외부콘텐츠 제시 기준 및 기타 요청사항 제시. (근거: 문서6)
 - 품질요구(QUR-001): 교육콘텐츠 평가 및 품질관리 방안 제시. (문서6)
 - 이러닝시스템 기능(SFR-001 ~ SFR-008): 시스템 구축·관리 기본방향, 사이버(모바일)연수원, 학습 이벤트, 큐레이션 서비스, 소셜러닝, 나의 학습노트, 직무지식진단, 역량진단 등 운영. (문서6)
 - 학사관리(LMR-001~LMR-002): LMS 제공, 학습참여 유인체계 제시. (문서6)
 - 콘텐츠개발(DER-001~DER-003): 개발 범위·요건·검사·검수 관련 요구. (문서6)
 - 유지관리(MAR-001): 유지관리 수행 범위 요구. (문서6)

2) 개인정보보호·정보보안 및 인수인계(문서6, 문서8)
 - 정보보안·개인정보보호 규정 준수 및 보안관리 방안 제시 요구. (문서6)
 - 인수인계 시 공단 보유 프로그램 및 데이터 이전 방안 제시. (문서6)
 - 계약 종료 후 이전 업체는 공단 관련 자료 전수 파기하고 공단 직원의 폐기 확인을 받아야 함. (문서8)
 - 인수·인계는 인수자·인계자 간 서면 완료확인서 제출, 원칙 30일 이내 완료(미흡 시 연장 가능). (문서8)

3) 산출물·보고서·제출형태(문서4)
 - 사업완료보고서 초안: 콘텐츠 개발 완료 최소 14일 전 제출·심의. (문서4)
 - 정기보고서: 착수(1회), 월간업무(월1회), 분기중간(분기1회), 최종(1회). (문서4)
 - 비정기 산출물 예: 차시별 원고·스토리보드(2부, 바인더·CD), 검토결과 조치내역서(1부), 사업완료보고서·운영자지침서·유지보수계획서(각 2부), 산출물 일체(외장HDD) 등. (문서4)
 - 제출방법·시기·형태는 공단과 협의 가능. (문서4)

4) 대금결제 및 일정(문서4)
 - 콘텐츠 개발: 검수완료 후 지급. (문서4)
 - 콘텐츠·P/G 유지보수·관리: 상/하반기 2회 지급(각 반기 말). (문서4)
 - 교육운영: 월별 또는 분기별 지급. (문서4)
 - 기타 세부 추진일정은 공단 일정표에 따름(문서4·문서5에 일정 개요). (문서4, 문서5)

5) 입찰·참가자격(문서3)
 - 참가자격: 관련 법령상 자격 보유, 원격평생교육시설 인가 및 이러닝사업자 신고, 나라장터에 관련 업종 코드 등록 등. (문서3)
 - 입찰방법: 일반경쟁입찰, 계약방법: 협상에 의한 계약. (문서3)

제공된 문서에서 확인할 수 없는 사항
 - 각 기능 요구별(예: SFR-002 등)의 상세 기술사양(구체적 화면·API·성능 수치 등)
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
답변은 제시된 '2024년 이러닝시스템 운영 용역 제안요청서'의 목차 및 본문 발췌(교육운영·이러닝시스템 기능, 콘텐츠개발·검수, 개인정보보호·정보보안, 산출물·보고서 제출, 대금결제 및 일정, 입찰·참가자격 등)를 요약하여 핵심 요구사항으로 정리하고 있음. 문서에 없는 세부 기술치·API 등은 답변에서 명확히 ‘확인 불가’로 언급하여 근거 범위를 벗어나지 않았음. 다만 답변 내 일부 문서번호 표기(예: 문서6 등)는 원문 스니펫에 직접 일치하지 않는 표기 방식이며, 매우 상세한 기술사양은 원문에서 제공되지 않아 누락됨.
```

#### q2_followup - top_experiment_full_question_set

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단

요약(콘텐츠 개발·관리 요구사항 — 문서에 명시된 내용만)

- 개발범위 및 목적
  - 직무 콘텐츠 개발·운영 및 위탁교육(자기개발) 콘텐츠 운영(문서6)
  - AI·빅데이터·IoT·AR/VR 등 4차산업융합 콘텐츠, 마이크로러닝, 전자책(e-book) 등 다양한 형식 지원(문서4)

- 개발·제작 역량 제출 요구
  - 보유기술 및 개발방법론 제시(문서5)
  - 콘텐츠 관리를 위한 장비·개발도구 보유현황 및 확보방안 제시(문서5)
  - 동영상 촬영 및 전자책 제작 등 지원방안 제시(문서5)

- 요청분석 및 변경·연동 대응
  - 공단의 콘텐츠 개발요청사항에 대한 분석내용 기술(문서5)
  - 시스템 변경에 따른 콘텐츠 변환 및 외부 연동 대응(문서3)
  - 콘텐츠 수록 내용 일부 수정·오탈자 정정 등 수정·보완 또는 교체 방안 제시(문서2, 문서3)

- 품질·검수·하자보수
  - 개발물 하자보수: 최종 검수 후 콘텐츠의 20% 범위 내에서 최소 1년 이내 지원(문서3)
  - 학습자 불편·문제제기 발생 시 원인 파악 후 즉시 보고 및 수정·보완·교체 방안 제시(문서2)
  - 월별·과정별 교육만족도·현업적용도 점검 및 통계관리·성과측정 방안 제시(문서2)

- 산출물 제출·보고
  - 사업수행 중 산출물·개발콘텐츠 및 보고서를 개발일정에 따라 제출(문서3)
  - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출하여 심의(문서3)

- 인수인계·지원
  - 각종 데이터 및 소스코드(게시자료 포함) 인수인계 방안 제시(문서5)
  - 선정업체는 관련 정보기술에 대한 지속적 정보제공 및 기술자문을 공단에 무상 지원(문서3)

- 예산·기간 관련
  - 콘텐츠 개발·관리는 전체 사업예산 중 해당 부문(금 153,000천원) 내에서 제안(문서6)
  - 사업기간: 계약체결일로부터 2025년 2월까지(문서6)

제공된 문서에서 확인할 수 없는 항목(문서 근거 명시)
- 개별 콘텐츠 분량(시간/분), 납품 파일 형식·코덱·해상도 등 기술적 세부요건은 제공된 문서에서 확인할 수 없습니다. (근거: 2024년 이러닝시스템 운영 용역 / 국민연금공단)
- 검수의 상세 기준(평가기준 항목별 수치), 산출물 일람 및 제출 포맷·부수(예: 차시별 원고·스토리보드 수량 등)는 제공된 문서에서 확인할 수 없습니다. (근거: 위 사업 제안요청서)
```

#### q3_multi_topic - top_experiment_full_question_set

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 95.62; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서 기준으로 교육·학습 관련 발주사업은 다음과 같습니다.

- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 발주기관: 인천광역시 (문서1: 교육지원 PSR 포함)  
- 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교 (문서3: 교직·현장실습 등 학사·교육 기능 포함)  
- 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단 (문서4, 문서7, 문서8: 이러닝·콘텐츠·운영 요구사항 포함)  
- JST 공유대학(원) xAPI기반 LRS시스템 구축 / 발주기관: 전북대학교 (문서6: xAPI 기반 LRS 관련)  
- 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 / 발주기관: 전북특별자치도 정읍시 (문서5: 트레이닝센터 관련)
```

#### q4_single_check - top_experiment_full_question_set

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나?
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
사업명/발주기관: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 기초과학연구원.

제공된 문서들에는 AI 기반 예측(예: 머신러닝)을 명시한 요구사항은 없습니다. 문서에는 주요 수치의 기록 및 연구원 요청 시 분석 수행 요구가 있으나, "분석 대상, 분석 방법 및 분석 결과물의 형태 등은 연구원이 정하는 바"라고만 명시되어 있어 AI 사용 여부나 AI 예측 기술 도입에 대한 명시는 제공된 문서에서 확인할 수 없습니다.
```

Judge reason excerpt:

```text
검색된 문서에는 AI·머신러닝 기반 예측을 명시한 요구사항은 등장하지 않습니다. 문서에는 ‘주요 수치 기록 및 연구원 요청 시 분석 수행’ 및 ‘기록 항목·간격은 연구원이 정하는 바’와 같은 조항이 있어 기록·분석 의무는 있으나 AI 사용 또는 예측기술 도입을 요구하거나 명시적으로 지정한 근거는 없습니다. 따라서 답변의 핵심(명시적 AI 요구사항 없음)은 근거에 잘 부합합니다.
```

#### q5_followup - top_experiment_full_question_set

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 발주기관: 기초과학연구원

요약(문서 근거):
- 모니터링 항목 및 업무: 알람 메시지 확인, 주요 센서 트렌드 확인(온도·압력·유량·속도 등), 정상 운전 지시값 파악·숙지, 비정상 운전 상황 감지, 제어로직 정상 작동 여부 확인, 현장 상황의 일시적·지속적 관찰(연구원 요청 시 비방사선구역 한정), 기타 운전 상황 확인(주기적 현장 순찰 포함). (문서2, 문서6)
- 상황 발생 시 조치 및 통보: 연구원에 지체없이 상황 전파 및 연구원 지시 긴급조치 이행 의무, 미이행 시 계약자 책임 발생 가능. (문서4)
- 기록·제출 요구: 주요 수치 기록(연구원 양식), 일일근무일지·월간보고서 등 전자파일로 저장·제출(계약자가 준비한 PC에 상시 저장), 주요 수치 기록 간격 및 항목은 연구원이 정함. (문서2, 문서3)
- 추가 협조: 연구원 요청 시 제어시스템(알람시스템 포함) 개선·보완에 협조. (문서8)

참고 문서: 문서2, 문서3, 문서4, 문서6, 문서8 (상기 사업명/발주기관 기준).
```

#### q6_purpose - top_experiment_full_question_set

- question: 한국 원자력 연구원에서 선량 평가 시스템 고도화 사업을 발주했는데, 이 사업이 왜 추진되는지 목적을 알려 줘.
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=4, relevance=5
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
근거: 사업명 "한국원자력연구원 선량평가시스템 고도화" / 발주기관: 한국원자력연구원

목적(문서 근거)
- 규제요건 준수: 제한구역 경계의 연간선량 준수 여부 확인 체계 구축(원자력안전위원회고시), ICRP60 기반 평가장기 개선, 액체유출물에 의한 주민피폭선량평가 기능 추가(문서1).  
- 업무생산성 향상: UI 개선 및 출력 기능 고도화를 통해 업무 효율성·신속한 의사결정 환경 구축(문서1).  
- 시스템 고도화 목표: 정상운전 시 주민선량평가시스템(K-RADAC) 고도화(문서6, 문서1의 기대효과).
```

Judge reason excerpt:

```text
답변의 핵심 목적들(규제요건 준수: 제한구역 경계 연간선량 확인체계 구축, ICRP60 기반 평가장기 개선, 액체유출물에 의한 주민피폭선량평가 기능 추가; 업무생산성 향상: UI 개선 및 출력 기능 고도화; 정상운전 시 규제수요 대응 등)은 제시된 근거(사업 안내의 1.2, 1.3, 1.4 등)에 명시되어 있어 대부분 근거에 의해 뒷받침됨. 다만 답변에 등장하는 '주민선량평가시스템(K-RADAC)'라는 특정 명칭 및 일부 문서 번호(문서6 등)는 제공된 근거문서에 명시되어 있지 않으므로(근거 부족) 1점 감점함.
```

#### q7_compare - top_experiment_full_question_set

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
아래 비교는 제공된 문서 내용만을 근거로 작성하였습니다.

1) 사업 목적
- 고려대학교 차세대 포털·학사 정보시스템 구축사업(발주: 고려대학교): 노후 시스템을 차세대로 구축해 정보서비스 품질 강화 및 대학 교육시스템 경쟁력 확보.  
- 학사시스템 기능개선 사업(발주: 광주과학기술원, GIST): 학사조직 개편 및 학위 연계과정 신설·과정구분 변경에 따른 시스템 개선으로 업무 편의성 및 효율성 제고.

2) 사업 범위·주요기능
- 고려대학교: 포털(통합로그인, 통합/지능형 검색, 마이페이지, 공지/알림, 일정, 커뮤니티, 게시판, 위젯, 연계서비스(웹메일·챗봇·전자결재·학사/행정) 등) 및 개인화·SSO·간편·2차인증, 모바일(기존 앱 ‘호잇’ 하이브리드 재구축·모바일웹·푸시) 포함. (사업명: 고려대학교 차세대 포털·학사 정보시스템 구축사업)  
- GIST: 학사 조직개편에 따른 시스템 개선 및 학위연계과정(학석연계, 학석박연계, 과정변경 등) 관련 기능 개발(예: 이수 후 석사·석박 통합 학번 발급 메뉴 등), 요구사항(FUR-005, FUR-006) 상세 명시. (사업명: 학사시스템 기능개선 사업 / 발주: 광주과학기술원)

3) 대상 사용자 범위
- 고려대학교: 학생(졸업생 포함), 교직원, 연구원 등 내부 구성원 대상 포털 기능 제공. (고려대학교)  
- GIST: 문서상 명시된 것은 학사·대학원 관련 관리자 및 사용자 메뉴 연동 등 (광주과학기술원). 추가 대상 세부는 제공문서에서 확인 불가.

4) 기간 및 일정
- 고려대학교: 계약일로부터 24개월 이내. (고려대학교)  
- GIST: 명시된 전체 사업 기간(개월 수)은 제공된 문서에서 확인할 수 없습니다. (광주과학기술원)

5) 예산·가격
- 고려대학교: 총사업예산 11,270,000,000원(VAT 포함, 3년 분할지급). (고려대학교)  
- GIST: 사업비 157,300,000원(VAT 포함). (광주과학기술원)

6) 유지보수·지급 등 조건
- 고려대학교: 무상유지보수기간 사업종료일로부터 12개월. (고려대학교)  
- GIST: 선금 50% 지급, 잔금은 최종검수 완료 시 지급; 공동수급 불가(공동수급불가). 유지보수 기간 등은 제공문서에서 확인할 수 없습니다. (광주과학기술원)

7) 계약·입찰 방식 및 제약
- 고려대학교: 제한경쟁입찰(협상에 의한 계약). 주사업자가 일괄 제안해야 함; 행정안전부 지침·웹표준·시큐어코딩 준수 등 요구됨. (고려대학교)  
- GIST: 공개경쟁입찰(협상에 의한 계약체결). 공동수급 불가 명시. (광주과학기술원)

8) 기술·품질요구(표준·보안 등)
- 고려대학교: 행정안전부 고시 기준 준수, 웹표준·웹호환성·웹접근성·시큐어코딩 적용 및 프레임워크 활용 등 명시. (고려대학교)  
- GIST: 상세 기능요구 및 성능요구(PER-001) 항
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - top_experiment_full_question_set

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
고려대학교(사업명: 차세대 포털·학사 정보시스템 구축사업): 있음. 문서([문서4])의 성능요구 PER-002(온라인성 업무응답시간)과 PER-003(웹페이지 디스플레이시간)에서 모든 질의·웹페이지는 사용자가 요청한 시점부터 3초 이내에 처리·표시되어야 함을 요구하며, 대량데이터(기준 5,000건 이상)·대형이미지(기준 500KB 이상)·동시사용자 용량의 90% 초과 등의 예외를 명시함.

광주과학기술원(사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업): 제공된 문서([문서1], [문서7], [문서5])에서는 응답시간(처리속도/화면표시시간)에 대한 명시적 요구사항을 확인할 수 없습니다.
```

Judge reason excerpt:

```text
답변은 제공된 문서 내용에 직접 근거함: 고려대학교 문서에서 PER-002(온라인성 업무응답시간)·PER-003(웹페이지 디스플레이시간)으로 모든 질의/웹페이지는 요청 시점부터 3초 이내 처리/표시해야 하며 예외사항도 명시되어 있어 해당 주장이 문서로 뒷받침됨. 광주과학기술원 관련으로 제공된 문서들(사업기간 산정서, 개인정보·기대효과 등)에는 응답시간(처리속도/화면표시시간)에 대한 명시적 요구사항이 포함되어 있지 않아 '없음'으로 답한 것도 제공된 근거와 일치함. (다른 문서가 있으면 결과가 달라질 수 있음.)
```

#### q9_imprecise_org - top_experiment_full_question_set

- question: 원자력연구소에서 방사선량 평가하는 시스템 사업 요구사항 알려줘
- EDD: 95.62; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: clean_high_score_sample
- interpretation: Automatic metrics and judge scores agree; keep as a positive report sample.

Answer excerpt:

```text
근거: 사업명 "한국원자력연구원 선량평가시스템 고도화" / 발주기관: 한국원자력연구원

요약(핵심 요구사항)
- 사업개요·계약: 계약기간 6개월, 사업비 46,600천원(부가세 포함), 제한경쟁입찰(중소기업 대상), 협상에 의한 계약(기술평가90%, 가격평가10%). (문서1)

기능 요구사항
- 평가장기 개선: 포트란 모듈 및 웹시스템의 평가장기(Organ) 개선. (문서1)
- 액체 유출물 선량평가 추가
  - 포트란 모듈 및 웹시스템에 액체 선량평가 기능 추가. (문서1, 문서5)
  - 피폭경로별 평가: 외부피폭(예: 해변활동, 수상활동), 내부피폭(예: 수산물·음용수·관개작물 섭취). (문서5 SFR-003)
  - 평가대상: 개인선량 및 집단선량(집단선량 항목 추가 요구 있음). (문서5 SFR-003, 문서5 상단)
  - 웹 UI 입력항목: 핵종, 방출량, 재농축인자; 부지·사회환경인자(희석수량·희석인자, 섭취량·생산량·활동시간·수송기간 등). 출력: 피폭경로별 선량결과 및 기준치 비교. (문서5 SFR-004)
  - DB구성: 생체축적인자, 선량환산인자, 부지특성인자 및 사회환경인자. (문서5 SFR-004)

성능 요구사항
- 질의응답 시간: 데이터 조회 및 선량평가 처리속도 최적화, 사용자의 건별 질의에 대해 3초 이내 화면 표시. (문서5 PER-001)

테스트 요구사항
- 단위테스트: 구현시 단위 테스트 항목·방법 명시한 단위테스트계획서 제출, 메뉴별 계획 수립·연구원 승인 후 시행, 관련 메뉴군 구성해 테스트. (문서2 TER-001)
- 통합테스트: 업무 시나리오별 통합테스트 계획서 제출·승인 후 시행. (문서2 TER-002)
- 인수테스트: 인수시험 방법·절차·점검후 조치방안 포함 계획 수립, 개발완료 후 최종산출물·테스트결과물 첨부해 승인검사 요청, 하자 발견 시 만족할 때까지 보완·반복. (문서2 TER-003)

보안·원격개발 요구사항
- 원격지 개발 시 비밀준수의무를 만족하는 작업장 제시 가능(발주처 우선검토). 원격지 개발에 따른 위험요인 식별 및 대응방안, 구체적 원격지 보안관리대책 제시 요구. (문서4)
- SW 산출물 반출 관련 보안(누출금지정보 예시: 내부·외부 IP, 세부시스템 구성 등) 적용. (문서4)
- 보안 요구사항 SER-001은 식별되어 있으나 세부 내용은 제공된 문서에서 확인할 수 없습니다. (문서2 SER-001)

프로젝트 지원·유지관리·기술이전
- 교육·기술이전: 한국원자력연구원이 자체 유지관리 가능하도록 교육계획 수립·관리자 교육 실시, 교육교재는 세부 기술 포함해 교육 이전 제출. (문서3)
- 하자보수: 준공검사 완료일로부터 하자담보기간 12개월, 장애 접수 후 24시간 이내 보수 가능하도록 신속 대응, 기술지원부서 및 전문인력 확보. (문서3 PSR-002)
- 기술이전 계획: 기술이전
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
답변은 제출된 '검색된 근거' 문서의 항목들을 충실히 요약·정리하고 있음. 사업개요(기간·예산·입찰방식·계약방법), 기능요구(SFR-003, SFR-004의 평가장기 개선·액체 선량평가 항목 및 UI·DB 요구), 성능요구(PER-001의 3초 응답 요구), 테스트요구(TER-001~TER-003), 보안·원격개발 요구, 기술이전·교육·하자보수(PSR-002, PSR-003) 및 산출물·보고·일정관리 등 주요 요구사항을 근거 문서에 기반해 제시하고 있어 근거에 기반한 응답이며 질문(사업 요구사항 요청)에 적절히 답하고 있음. 허위·추가 생성된 사실은 발견되지 않음; 단 일부 레이블(예: 문서번호 표기)은 응답 편의를 위해 사용된 것으로, 내용 자체는 제공된 근거에서 직접 확인 가능함.
```

#### q10_abstention - top_experiment_full_question_set

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 95.62; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서에서 확인할 수 없습니다.

근거: 문서에 수록된 사업들은 예컨대
- 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / 발주기관: (사)부산국제영화제
- [재공고] 차세대 통합정보시스템(ERP) 구축 / 발주기관: 한국가스공사
- 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교
- 도시계획위원회 통합관리시스템 구축용역 / 발주기관: 인천광역시
- 예약발매시스템 개량 ISMP 용역 / 발주기관: 한국철도공사
- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 발주기관: 인천광역시
- 수협중앙회 수산물사이버직매장 시스템 재구축 ISMP 수립 / 발주기관: 수협중앙회

위 문서들에는 우주 로켓 발사 시스템 구축 관련 내용이 포함되어 있지 않습니다.
```

### fetch40_top8_filter_rewrite

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 93.13; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=2, relevance=5
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: low_groundedness
- interpretation: LLM judge found a quality issue; inspect answer-evidence alignment, not only retrieval metrics.

Answer excerpt:

```text
요청하신 내용은 아래와 같이 정리합니다. 근거 문서: 사업명 "2024년 이러닝시스템 운영 용역" / 발주기관: 국민연금공단(참고문서[문서1],[문서3],[문서6],[문서8],[문서4]).

요약(핵심 요구사항)
1. 교육과정 운영
 - 국민연금공단 역량모델(리더십·직무·공통)에 기반한 TRM(Training Road Map) 제시 및 전 직원 대상 카테고리별 콘텐츠 제공(근거: 문서3 FUR-001).  
 - 학습참여 유인체계 제시 요구(근거: 문서3).

2. 콘텐츠 개발·관리
 - 콘텐츠 개발 범위·요건·검사·검수 등 요구(문서3 DER-001~DER-003 표기).  
 - 저작권·지적재산권 보호 준수(문서3 COR-001).

3. 시스템(이러닝) 운영·유지관리
 - 콘텐츠 및 플랫폼 유지관리·관리범위 요구(문서3 MAR-001·MAR-002).  
 - 운영 중 산출물·검수 체계 및 사업보고 등 프로젝트 관리 요구(PMR-001~PMR-006)(문서3).

4. 동영상 촬영 및 실시간(화상)강의 지원
 - 촬영지원 10회(1회 기준 1일 8시간), 촬영·편집기사 및 장비·설비 제공(문서8).  
 - 촬영 관련 업체 직원 숙식비는 공단 부담(문서8).  
 - 실시간 송출(쌍방향 기능 포함: 채팅, Q&A 등) 요구, 송출 운영은 정산 기준 적용(문서8, 문서3 PSR-001).

5. 개인정보보호 및 정보보안
 - 「개인정보 보호법」 준용, 개인정보처리 위탁 시 준수사항 숙지(문서8 SER-001).  
 - 위탁계약서(서식9) 작성, 종사자 보안서약서(서식10) 및 개인정보보호교육·실태점검 필수(문서8).  
 - 공단은 최소한의 개인정보만 제공, 수집된 개인정보는 목적 달성 시 지체 없이 파기(문서8).

6. 산출물·보고서 및 제출요건
 - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출 후 심의(문서6).  
 - 정기보고: 착수보고(1회), 월간 업무현황(월1회), 분기 중간보고(분기1회), 최종보고(1회)(문서6).  
 - 산출물(차시별 원고·스토리보드, 사업완료보고서, 운영자 지침서, 유지보수계획서, 소스 등) 제출 형식(바인더, CD, 외장HDD 등) 및 수량 명시(문서6).

7. 대금결제
 - 콘텐츠 개발: 검수완료 후 지급.  
 - 유지보수·관리: 상·하반기 2회로 분할 지급(각 반기 말).  
 - 교육운영: 월별 또는 분기별 지급(문서6 PMR-004).

8. 사업수행 관련 행정·입찰사항
 - 입찰참가신청·보증 등 일반 입찰서류 및 공동수급 표준 협정서 등 제출(문서4).  
 - 청렴·부조리 신고 안내(문서1).

문서에서 확인되지 않는 항목(제공된 문서에서 확인할 수 없습니다)
 - 구체적인 과업기간(시작·종료일), 예산·가격 산출 기준의 상세 수치, SLA(가용성·응답시간 등) 및 사용자 수·과정 수 등
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
답변은 전반적으로 제공된 제안요청서 발췌에 등장하는 주요 항목들(교육과정 운영(TRM), 콘텐츠 개발·검수, 운영·유지관리, 개인정보보호·보안, 산출물 및 보고서 체계, 사업관리 요구 등)을 적절히 정리하여 질문에 잘 답하고 있음(따라서 relevance 높음). 다만 근거문서에서 직접 확인되지 않는 구체적 수치·조항(예: 촬영지원 '10회', '1일 8시간', 촬영업체 숙식비 공단 부담 등), 지급 방식·분할지급의 세부 표현, 그리고 응답에 사용된 '문서3/문서6/문서8'와 같은 참조 표기는 제공된 근거 텍스트에 명확히 대응하지 않음. 일부 항목은 원문에 있는 항목명만을 요약한 반면, 몇몇 세부사항은 근거에 없거나 과장되어 보이므로 전체적으로 근거대응성은 낮음(2/5).
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 93.13; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거 문서: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단

요약 — 콘텐츠 개발·관리 핵심 요구사항

- 범위 및 목적  
  - 직무 콘텐츠 개발·운영 및 위탁(자기개발) 콘텐츠 운영 포함. 운영에는 정보보안·개인정보보호 및 법령준수가 포함되어야 함. (근거: 문서6)

- 콘텐츠 유형 및 기능 요구사항  
  - 4차 산업혁명(인공지능·빅데이터·AR·VR 등), 마이크로러닝, 모바일·e-book, 북러닝, OA·직무·소통·리더십 등 직무·교양 콘텐츠 및 외부 공공콘텐츠 연계 운영. (근거: 문서6)  
  - 어학(다국어, 회화·문법 등), 전화외국어, 전문자격증 과정(전문자격증 최소 15개 이상 제시 등) 등 세부 과목 요구. (근거: 문서5)

- 개발·수정·연동 요구  
  - 시스템 변경에 따른 콘텐츠 변환·연동 지원 필요. 콘텐츠 수록 내용 일부 수정·오탈자 정정, 관련 자료 연결 등 반영 요구. (근거: 문서2)

- 하자보수·유지관리  
  - 최종 검수 후 콘텐츠의 20% 범위 내에서 최소 1년 이내 하자보수 지원. 계약종료 후 하자보수 범위 및 추진체계 제시해야 함. (근거: 문서2)  
  - 선정업체는 관련 정보기술에 대한 지속적 정보제공 및 기술자문을 공단에 무상 지원해야 함. (근거: 문서2)

- 품질관리 및 문제처리  
  - 학습자 불편사항·문제제기 발생 시 원인파악 즉시 보고 및 수정·보완 또는 교체 방안 제시. 품질관리 위원회 운영 방식 등은 공단과 협의. (근거: 문서3)  
  - 월별·과정별 교육만족도·현업적용도 점검 실시와 체계적 교육성과측정 및 통계관리 방안 제시 요구. (근거: 문서3)

- 보고·산출물 제출  
  - 과업수행 중 생산된 모든 산출물·개발콘텐츠·보고서를 일정에 따라 제출. 콘텐츠 개발 완료 최소 14일 전에 사업완료보고서 초안 제출 및 심의 필요. (근거: 문서2, PMR-003)

- 보안·개인정보 준수  
  - 콘텐츠 운영·관리 시 정보보안·개인정보보호 및 관련 법령 준수 필요(운영범위에 포함). (근거: 문서6)

- 예산·기간 제약  
  - 사업기간: 계약체결일~2025.2월. 콘텐츠 개발·관리 관련 예산(총 사업예산 중 해당 항목)은 명시된 한도를 초과할 수 없음(문서에 제시된 예산 범위 준수). (근거: 문서7)

제공된 문서에서 확인할 수 없는 항목(명시): 상세한 개발절차·검수기준(세부 체크리스트), 산출물 형식 및 제출 상세 목록, 과업별 산정 단가·평가배점 등은 제공된 문서에서 확인할 수 없습니다. (근거: 사업명: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단)
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 93.13; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 재단법인스포츠윤리센터, 전북특별자치도 정읍시, 전북대학교, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
예. 제공된 문서들 중 교육·학습 관련 발주 사업(문서 기준)은 다음과 같습니다.

- 문서1: 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 발주기관: 인천광역시 (교육지원·교육계획 요구사항 포함)  
- 문서3: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교 (교직·실습·이수관리 기능 기술)  
- 문서4, 문서8: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단 (다양한 이러닝·평가 요구사항)  
- 문서5: 스포츠윤리센터 LMS(학습지원시스템) 기능개선 / 발주기관: 재단법인스포츠윤리센터 (LMS 기능 및 통계·연계 고도화)  
- 문서7: JST 공유대학(원) xAPI기반 LRS시스템 구축 / 발주기관: 전북대학교 (xAPI/LRS 기반 학습기록 시스템)  
- 문서6: 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 / 발주기관: 전북특별자치도 정읍시 (사업명·문서 내 교육담당자·교육대상자 표기)

참고: 한국사학진흥재단 문서(문서2)는 청렴각서·계약 관련 내용으로, 교육·학습 관련 발주사업으로 확인되지는 않습니다.
```

#### q5_followup - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 93.13; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 발주기관: 기초과학연구원

요약(문서 근거 표시):
- 전자파일로 주요 수치 기록을 요구함(기록 항목·간격은 연구원이 정함, 증감 가능). 연구원 요청 시 해당 수치에 대한 분석 수행(분석 대상·방법·결과물 형태는 연구원이 정함). 계약자가 기록용 노트북·키보드·마우스 등 준비. (문서2)
- 모니터링 업무 리스트(필수 항목): 알람 메시지 확인, 온도·압력·유량·속도 등 주요 센서 트렌드 확인, 정상운전 지시값 파악, 비정상 상황 감지, 연구원 지정 값 관찰·상황 전달(무전 통신 사용, 무전기 연구원 제공), 제어로직 정상 작동 여부 확인, 현장 일시적/지속 관찰(연구원 요청 시 비방사선구역 한정), 주기적 현장 순찰 등. (문서2, 문서6)
- 가동·휴지기간 모두 모니터링 수행 요구: 휴지기간에도 주간 운전인력 제공 및 일부 인원은 모니터링·제어 수행. (문서4)
- 위험(긴급) 상황 발생 시 즉시 연구원에 전파하고 연구원이 지시한 긴급조치 사항을 수행해야 함(이를 이행하지 않으면 계약자 책임). (문서4)
- 운전 중 수리 필요 사항 별도 기록(연구원 양식 제공) 및 연구원 요청 시 제어시스템(알람 포함) 개선·보완 협조 등 모니터링 관련 추가 협조 의무. (문서7)

결론: 기초과학연구원 발주 과업지시서에는 극저온시스템의 모니터링 업무에 대한 구체적 요청사항이 명시되어 있습니다(상기 근거 문서: 문서2, 문서4, 문서6, 문서7).
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 93.13; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 광주과학기술원, 광주과학기술원, 광주과학기술원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
요청하신 비교는 아래 제공된 문서 내용만 근거해 요약했습니다.

1) 사업명·발주기관
- 고려대학교 차세대 포털·학사 정보시스템 구축 사업 (고려대학교) — 문서1, 문서3, 문서4.
- 학사시스템 기능개선 사업 (광주과학기술원) — 문서2, 문서6, 문서8.

2) 사업목표·범위(주요 내용)
- 고려대학교: 포털시스템 중심의 전면 구축(통합로그인, 통합/지능형 검색, 마이페이지, 공지/알림, 일정관리, 커뮤니티/게시판, 개인화 위젯, 연계서비스(웹메일·챗봇·전자결재·학사/행정 서비스), SSO·간편·2차인증, 모바일(기존 앱 '호잇' 하이브리드 재구축) 등 포털·학사 정보시스템 전반 재구축. (고려대학교, 문서1)
- 광주과기원: 특정 학사 기능 개선(학사 조직개편 반영, 학위연계·학석·학석박·대학원 과정변경 관련 메뉴 및 프로세스 개발·연동 등)— 대상은 학사 프로세스와 관련된 기능 개선 중심. (광주과기원, 문서6, 문서8)

3) 사업기간·유지보수
- 고려대학교: 계약일로부터 24개월 이내, 무상유지보수 12개월. (고려대학교, 문서3)
- 광주과기원: 적정 사업기간 산정치는 5개월(종합의견), 문서상 산정 결과는 5개월로 제시됨. (광주과기원, 문서2)

4) 예산·대금지급
- 고려대학교: 사업예산 11,270,000,000원(VAT 포함), 3년 분할지급(2024 약30% / 2025 약40% / 2026 약30%). (고려대학교, 문서3)
- 광주과기원: 사업비 157,300,000원(VAT 포함). 선금 50% 지급, 잔금은 최종검수 완료 시 지급. 공동수급 불가. (광주과기원, 문서8)

5) 입찰·계약 방식 및 제한사항
- 고려대학교: 제한경쟁입찰(협상에 의한 계약). (고려대학교, 문서3)
- 광주과기원: 공개경쟁입찰(협상에 의한 계약체결), 공동수급불가 명시. 개인정보 동의서 관련 보유기간(원 입찰참가 서류 관리 목적 5년) 및 동의 거부 시 계약체결 대상 제외 규정도 존재(입찰참가자 관련). (광주과기원, 문서8; 문서2)

6) 평가·검토·요구사항 차이
- 고려대학교: 기술·기능(30점)·성능·품질(10점) 등 상세 평가항목 존재(시스템장비, 기능요구사항, 보안, 데이터 전환 등). 개발방법론·설계·보안·데이터 전환 계획의 구체성 요구. (고려대학교, 문서4)
- 광주과기원: 사업목표·추진체계·업무분장 등 실무 중심 요구사항과 학사 프로세스 연계·재설계 강조. 시스템 통합 시 기존 시스템 영향 최소화, 한 시스템 장애가 다른 시스템에 영향 없어야 함, 신규 도입 제품은 기존 제품과 유기적 연계 및 커스터마이징 가능해야 함(제안서 일반요건). (광주과기원, 문서5; 문서7; 문서8)

7) 기대효과·성격(규모 비교)
- 고려대학교: 포털·학사정보시스템 전면 차세대 구축으로 정보서비스 품질 제고 및 대학 교육 시스템 경쟁력 확보(대규모 통합
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 93.13; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
고려대학교(차세대 포털·학사 정보시스템 구축사업): 예. 문서4에 근거하여 PER-002(온라인성 업무응답시간)에서 모든 질의는 사용자 요청 시점부터 3초 내 처리(단, 대량데이터·대형이미지·동시사용자 90% 초과 등 예외 규정 있음), PER-003(웹페이지 디스플레이시간)에서 웹페이지는 요청 후 3초 내 출력하도록 요구하고 있습니다.

광주과학기술원(실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업): 응답시간 요구사항은 제공된 문서(문서1, 문서8 등)에서 확인할 수 없습니다.
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 93.13; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 전북특별자치도 정읍시, 고려대학교, 인천광역시, 한국철도공사 (용역), 수협중앙회, 인천광역시
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서에서 우주 로켓 발사 시스템 구축 사업은 확인할 수 없습니다.

근거 문서(사업명/발주기관):
- 문서1: 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / (사)부산국제영화제  
- 문서2: [재공고] 차세대 통합정보시스템(ERP) 구축 / 한국가스공사  
- 문서3: 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 / 전북특별자치도 정읍시  
- 문서4: 차세대 포털·학사 정보시스템 구축사업 / 고려대학교  
- 문서5: 도시계획위원회 통합관리시스템 구축용역 / 인천광역시  
- 문서6: 예약발매시스템 개량 ISMP 용역 / 한국철도공사  
- 문서7: 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 / 수협중앙회  
- 문서8: 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 인천광역시
```

### filter_off_rewrite_off

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 65.3; coverage: 0.0; first_hit_rank: None; abstention: True; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 수협중앙회, 서민금융진흥원, KOICA 전자조달, 재단법인스포츠윤리센터, 한국연구재단, 한국농수산식품유통공사, 인천광역시 동구, 한국철도공사 (용역)
- flags: coverage_below_target, false_abstention
- interpretation: The system refused despite a non-abstention case; inspect abstention prompt and evidence confidence.

Answer excerpt:

```text
제공된 문서에서 확인할 수 없습니다.

근거 문서(검토 대상):
- 문서1: 사업명: 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 / 발주기관: 수협중앙회  
- 문서2: 사업명: 서민금융 채팅 상담시스템 구축 / 발주기관: 서민금융진흥원  
- 문서3: 사업명: 우즈베키스탄 국회 방송시스템 구축 PMC 용역 / 발주기관: KOICA 전자조달  
- 문서4: 사업명: 스포츠윤리센터 LMS 기능개선 / 발주기관: 재단법인스포츠윤리센터  
- 문서5: 사업명: 2024년 기초학문자료센터 시스템 운영 및 DB구축 / 발주기관: 한국연구재단  
- 문서6: 사업명: 농산물가격안정기금 정부예산회계연계시스템 고도화 / 발주기관: 한국농수산식품유통공사  
- 문서7: 사업명: 수도국산달동네박물관 전시해설 시스템 구축 / 발주기관: 인천광역시 동구  
- 문서8: 사업명: 예약발매시스템 개량 ISMP 용역 / 발주기관: 한국철도공사

국민연금공단이 발주한 이러닝시스템 관련 요구사항 분석을 원하시면 해당 기관의 RFP 또는 관련 문서를 제공해 주세요.
```

Judge reason excerpt:

```text
제공된 '검색된 근거' 문서들(CSR-011 등)은 수협, 서민금융진흥원, KOICA 등 여러 발주기관의 요구사항을 포함하고 있으나 국민연금공단(및 국민연금공단이 발주한 이러닝)에 관한 언급은 없음. 따라서 질문에 대해 해당 근거 내에서 국민연금공단 이러닝 요구사항을 정리할 수 없다는 답변은 근거에 부합하며, 추가 문서(RFP 등)를 요청한 것도 질문에 직접적으로 대응하는 적절한 응답임.
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 65.3; coverage: 1.0; first_hit_rank: 2; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: KOICA 전자조달, 국민연금공단, 재단법인 한국장애인문화예술원, 국민연금공단, 재단법인 한국장애인문화예술원, (사)부산국제영화제, 국민연금공단, 조선대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "2024년 이러닝시스템 운영 용역" / 발주기관: 국민연금공단

요약(핵심 요구사항)

1) 개발 프로세스·지원
- 개발 요청 시 즉시 수행, 개발 컨설팅 및 개발계획서 제출 의무.  
- 개발 안내 워크숍 개최.  
- 설계서·스토리보드 기반으로 공단 담당자 및 내용전문가 검토·수정·보완, 프로토 차시 검토 후 전체 개발 시행.  
- 하도급은 공단 사전승인 필요, 하도급 비율 50% 초과 불가, 재하도급 원칙 금지.

2) 콘텐츠 설계·형식
- 유지보수·호환성·확정성 고려하여 개발; 완료 후 수정·추가·삭제가 용이하도록 개발.  
- 동영상 타입으로 차시별 30~40분 내외로 제작.  
- 웹 학습·모바일 학습 연동(스마트러닝) 가능하도록 설계.  
- 주제별 세분화된 모듈로 1개 차시 구성 및 모듈별 게시 가능.  
- 과정 특성에 맞는 멀티미디어 및 엔터테인먼트 요소 적용(학습흥미 유발, 학습자 중심).  
- 콘텐츠와 “나의 학습노트” 연동 가능하도록 개발.  
- 디자인·이미지 등은 3안 이상 제안.  
- 공단 업무망 분리 등 네트워크 환경을 고려하여 네트워크 부하 적은 기술 적용.  
- 공단이 제작한 교안(PPT) 및 음성녹음 파일을 합본(싱크 조절 포함)하여 콘텐츠에 포함; 스크립트(자막)도 포함.

3) 품질관리·운영
- 콘텐츠 품질관리 평가 기준 제시 및 이에 따른 업그레이드·퇴출 방안 제시.  
- 불량 판단 시 변경 또는 추가 제공(빈번한 민원 콘텐츠는 공단과 협의 후 교체).  
- 연 2회 이상 정기적·지속적 콘텐츠 관리(최신성, 인기도, 만족도 기준으로 교체/정비).  
- 학습자 불편·문제 발생 시 원인 파악 후 즉시 보고 및 수정·보완·교체 방안 제시.

4) 산출물·보고
- 최종 사업완료보고서 초안은 사업완료 14일 전 공단에 제출하여 심의.  
- 정기보고: 착수보고서(1회), 월간업무현황보고서(월1회), 중간보고서(분기별), 최종보고서(1회).  
- 비정기 산출물: 차시별 원고·스토리보드(2부, 바인더·CD), 검토결과 조치내역서(1부), 사업완료보고서(2부 바인더·CD), 운영자 지침서 및 유지보수 계획서(각 2부), 산출물 일체(소스·스토리보드 등) 1부(외장HDD) — 제출 시기는 공단과 협의 가능.

5) 결제·지급
- 콘텐츠 개발 대금은 검수완료 후 지급.  
- 콘텐츠·P/G 유지보수·관리는 상·하반기 각 반기 말에 지급(2차례).  
- 교육운영은 월별 또는 분기별 지급.

6) 외부콘텐츠·추가요청
- 본부 부서 요청 시 제공 가능한 외부콘텐츠 우선 제공.  
- 교재 제공 협조, 미비 시 교안 등 학습자료 제공.  
- 신입 직원용 단계별 적응 콘텐츠 제시, 모바일 연동 과정 학습방법 안내, HRD 담당자 역량강화용 콘텐츠 제시.

(문서에 없는 추가 세부기능·정량적 성능치 등은 제공된 문서
...(truncated; full text is in report_evidence.json)
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 65.3; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: false_abstention, missing_llm_judge_score
- interpretation: The system refused despite a non-abstention case; inspect abstention prompt and evidence confidence.

Answer excerpt:

```text
제공된 문서 기준으로 교육·학습 관련 발주 사업(다른 기관 포함)은 다음과 같습니다.

- 인천광역시: 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 — 교육지원(교육계획 수립·교육실시 등) 명시 (참고 문서1).  
- 고려대학교: 차세대 포털·학사 정보시스템 구축사업 — 교직·실습·이수관리 등 교육/학사 기능 명시 (참고 문서3).  
- 국민연금공단: 2024년 이러닝시스템 운영 용역 — 이러닝 콘텐츠·운영, 교육평가, 수강인원 등 상세 요구사항 명시 (참고 문서4, 문서7, 문서8).  
- 전북대학교: JST 공유대학(원) xAPI기반 LRS시스템 구축 — 학습기록(LRS) 관련 사업 (참고 문서6).  
- 전북특별자치도 정읍시: 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 — 사업명에 ‘트레이닝센터’ 포함(참고 문서5).

다른 교육·학습 관련 발주가 더 있는지는 제공된 문서 외에는 확인할 수 없습니다.
```

#### q4_single_check - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나?
- EDD: 65.3; coverage: 0.0; first_hit_rank: None; abstention: True; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 서울특별시교육청, 고려대학교, 한국원자력연구원, KOICA 전자조달, 서울특별시 여성가족재단, 고려대학교, 한국농어촌공사, 한영대학
- flags: coverage_below_target, false_abstention
- interpretation: The system refused despite a non-abstention case; inspect abstention prompt and evidence confidence.

Answer excerpt:

```text
제공된 문서들(서울특별시교육청: 지능정보화전략계획(ISP) 수립(2차), 고려대학교: 차세대 포털·학사 정보시스템 구축사업, 한국원자력연구원: 선량평가시스템 고도화, KOICA 전자조달: 우즈베키스탄 국회 방송시스템 구축 PMC, 서울특별시 여성가족재단: 디지털성범죄 안심지원센터 통합사업, 한국농어촌공사: AFSIS 사업, 한영대학교: 특성화 학사정보시스템 고도화)에는 '기초과학연구원 극저온시스템' 사업 관련 내용이 포함되어 있지 않습니다.  
따라서 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있는지는 제공된 문서에서 확인할 수 없습니다.
```

Judge reason excerpt:

```text
제공된 검색 근거에는 나열된 다른 사업들(서울특별시교육청 ISP, 고려대 포털, 원자력연구원 선량평가 고도화 등)만 포함되어 있으며 '기초과학연구원 극저온시스템' 관련 내용이나 AI 기반 예측 요구사항은 언급되어 있지 않습니다. 따라서 답변('제공된 문서들에서 해당 요구사항을 확인할 수 없음')은 검색된 근거에 직접 근거하고 있으며, 질문에 대해 해당 근거 범위 내에서 정확히 응답하고 있습니다.
```

#### q5_followup - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 65.3; coverage: 0.0; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=1, relevance=3
- retrieved_orgs: 재단법인 광주광역시 광주문화재단, 한국가스공사, 한국건강가정진흥원, 파주도시관광공사, 수협중앙회, 을지대학교, (사）한국대학스포츠협의회, (사)부산국제영화제
- flags: coverage_below_target, low_groundedness, low_relevance
- interpretation: Retrieval did not cover all target organizations; inspect filtering, rewrite, and MMR diversity.

Answer excerpt:

```text
다음 참고 문서들에서 모니터링 관련 요청사항이 명시적으로 확인됩니다.

- 2024년 BIFF & ACFM 온라인서비스 재개발 (발주기관: (사)부산국제영화제): "상시 모니터링 및 장애예방, 장애처리 활동" 명시(정기 예방점검 월 1회, 장애접수 후 4시간 이내 보수 대응 등). (문서8)

- 2025년 아이돌봄인력 인적성 검사 정보시스템 운영 (발주기관: 한국건강가정진흥원): 예방점검·정기·수시점검 수행 및 점검결과 보고서 제출 의무, 장애 발생 시 대응시간 기준 등 명시(MAR-005 등). (문서3)

- 종량제봉투 판매관리 전산시스템 개선사업 (발주기관: 파주도시관광공사): 관련 항목에 "시스템 모니터링"이 명시되어 있으며 성능·오류 응답시간 요구사항 등 포함. (문서4)

- KUSF 체육특기자 경기기록 관리시스템 개발 (발주기관: (사)한국대학스포츠협의회): 시스템 관리자 매뉴얼에 "로그 및 백업 관리 등 모두 포함 필요" 등 운영·관리(모니터링 관련) 항목 명시. (문서7)

제공된 문서 범위 내에서는 위 문서들에서만 모니터링 요구사항이 확인되며, 문서1, 문서2, 문서5, 문서6 등에는 명시적 모니터링 요구사항이 확인되지 않습니다.
```

Judge reason excerpt:

```text
제공된 '검색된 근거' 자체에 이미 명시된 여러 모니터링 관련 요구사항(정기·수시 예방점검 및 점검결과 보고서 제출, 장애대응·백업·복구·로그수집, 신고접수 후 착수시간 기준, 오류응답시간·느린작업 안내, 동시접속 성능 기준 등)이 존재함. 그러나 답변은 근거 문서의 내용이 아닌 다른 문서(문서8, 문서3 등)를 인용하며 근거와 일치하지 않는 진술을 하고 있고, 제공된 근거의 구체적 항목들을 인용·요약하지 않았음. 따라서 답변 내용은 질문에 어느 정도 응답하였으나(모니터링 요구가 있다고 응답함) 실제 '검색된 근거'로 뒷받침되지 않아 groundedness는 매우 낮고(rev=1), 질문에 대한 응답 자체는 부분적으로 이루어졌으므로 relevance는 중간 수준(3)으로 평가함.
```

#### q6_purpose - issue_or_audit_queue

- question: 한국 원자력 연구원에서 선량 평가 시스템 고도화 사업을 발주했는데, 이 사업이 왜 추진되는지 목적을 알려 줘.
- EDD: 65.3; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 한국원자력연구원, 경기도 평택시, 대한상공회의소, 한국보건산업진흥원, 한국연구재단, 서울시립대학교, 한국원자력연구원, 한국생산기술연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "한국원자력연구원 선량평가시스템 고도화" / 발주기관: 한국원자력연구원(참조: 문서1, 문서7)

주요 추진 목적(간략)
- 규제요건 준수: 제한구역경계 연간선량 준수 여부 확인 체계 구축(원자력안전위원회 고시 대응), ICRP60 기반 평가장기 개선, 액체유출물에 의한 주민피폭 선량평가 수행 필요.
- 업무생산성 향상: UI 개선으로 신속한 의사결정 환경 조성 및 출력 기능 고도화를 통한 생산성 향상.
- 기대효과: 정상운전 시 선량평가 관련 규제 수요에 대응.
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 65.3; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=3, relevance=5
- retrieved_orgs: 고려대학교, 광주과학기술원, 서울시립대학교, 고려대학교, 대전대학교, 서영대학교 산학협력단, 조선대학교, 고려대학교
- flags: low_groundedness
- interpretation: LLM judge found a quality issue; inspect answer-evidence alignment, not only retrieval metrics.

Answer excerpt:

```text
요청하신 비교는 아래 제공된 문서만을 근거로 합니다. 각 항목에 근거된 사업명(발주기관)을 함께 표기합니다.

1) 사업 목적·목표
- 고려대학교 차세대 포털·학사 정보시스템 구축사업(고려대학교): 노후화된 시스템을 차세대로 구축하여 정보서비스 품질 강화 및 대학 교육 시스템 경쟁력 확보 (문서1).
- 학사시스템 기능개선 사업(광주과학기술원): 기존 학사시스템의 기능 개선(문서2의 목차에 '사업목적'·'사업목표' 명시). 구체 목표 내용은 문서에 상세히 제시되어 있으나 제공된 excerpt에서 세부 내용은 확인 불가(제공된 문서에서 확인할 수 없습니다). 근거: 문서2.

2) 사업 범위·주요 기능
- 고려대학교(문서1·문서8): 포털 전면 구축(통합로그인·통합/지능형 검색·마이페이지·공지·일정·커뮤니티·게시판·위젯·개인화·SSO·간편·2차인증 등), 모바일(기존 앱 '호잇' 하이브리드 재구축), 학사/행정/연구 시스템 연계 등 매우 광범위한 기능 포함(문서1, 문서8).
- 광주과학기술원(문서2): RFP에 '요구사항 총괄표'·'요구사항 상세'가 포함되어 기능개선 범위를 정의하도록 되어 있으나, 제공된 문서 발췌에서는 구체적 기능 항목이 제시되어 있지 않음(제공된 문서에서 확인할 수 없습니다). 근거: 문서2.

3) 기간·예산·계약방식
- 고려대학교(문서4): 사업기간은 계약일로부터 24개월, 무상유지보수 12개월, 사업예산 11,270,000,000원(VAT 포함, 3년 분할지급), 입찰·계약방법은 제한경쟁(협상에 의한 계약)이라고 명시됨(문서4).
- 광주과학기술원(문서2): 제공된 발췌에서는 사업기간·예산·계약방식 정보가 보이지 않음(제공된 문서에서 확인할 수 없습니다). 근거: 문서2.

4) 기술스택·연계시스템 현황
- 고려대학교(문서8): 기존 시스템·기술스택 일부 명시(Java/Spring, Spring boot, Kotlin, Swift, node.js, flutter, vue.js 등) 및 통합검색(Search Formula-1), SSO(SafeIdentity) 등 여러 내부 시스템 연계 현황 표기(문서8).
- 광주과학기술원(문서2): 기술스택이나 구체 연계시스템 정보는 제공된 발췌에 없음(제공된 문서에서 확인할 수 없습니다). 근거: 문서2.

5) 제안·평가·관리 문서화 수준
- 고려대학교(문서4·문서1): 제안서 작성 유의사항·목차·별첨 등 상세한 제안서 지침 및 대규모 문서(별첨 포함)가 존재(문서4).
- 광주과학기술원(문서2): 제안서 평가방법, 기술성 평가기준, 제안서 제출 등 평가·제출 관련 항목이 목차에 상세히 구성되어 있음(문서2). 다만 세부 평가기준 내용은 발췌에서 확인 불가(제공된 문서에서 확인할 수 없습니다).

6) 종합 비교 요약(핵심)
- 고려대학교 사업: 전체 대학 구성원을 대상으로 하는 대규모 차세대 포
...(truncated; full text is in report_evidence.json)
```

Judge reason excerpt:

```text
답변은 대부분 제공된 근거 문서를 참조해 고려대 사업(포털·학사 전면구축, 예산·기간·유지보수 등) 내용을 정확히 요약하였음. 다만 광주과학기술원 문서에 대해 '구체적 기능 항목이 제시되어 있지 않다'고 한 부분은 부정확함(제공된 발췌에는 데이터 연계·클라우드·비식별화·데이터 시각화·AI 파일럿 등 구체적 과업이 포함되어 있음). 또한 일부 기술스택/세부사항은 근거 문서에서 명확하지 않은 점을 올바르게 지적한 부분도 있음. 따라서 근거에 기반한 내용도 다수 포함되나, 광주과학기술원 측의 일부 구체사항을 누락하거나 잘못평가한 점 때문에 완전한 근거성은 떨어짐.
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 65.3; coverage: 1.0; first_hit_rank: 2; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 서영대학교 산학협력단, 광주과학기술원, (사)부산국제영화제, 고려대학교, 대전대학교, 한국원자력연구원, (사）한국대학스포츠협의회, 인천광역시
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 고려대학교: 제공된 문서(사업명: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교)에서는 응답시간(응답속도) 요구사항이 명시되어 있지 않습니다. 근거: 문서의 PMR-006(산출물 및 보고서 제출) 등 프로젝트관리 요구사항만 기재됨.

- 광주과학기술원: 제공된 문서(사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업 / 발주기관: 광주과학기술원)에서는 응답시간에 관한 요구사항이 명시되어 있지 않습니다. 근거: 개인정보 동의 및 소프트웨어 사업 기간 산정서 등만 포함되어 있음.

문서에 없는 내용은 추측할 수 없습니다.
```

#### q9_imprecise_org - issue_or_audit_queue

- question: 원자력연구소에서 방사선량 평가하는 시스템 사업 요구사항 알려줘
- EDD: 65.3; coverage: 1.0; first_hit_rank: 3; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 한국연구재단, 한국생산기술연구원, 한국원자력연구원, 한국철도공사 (용역), 재단법인 광주광역시 광주문화재단, 국방과학연구소, 울산광역시, 국가과학기술지식정보서비스
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 한국원자력연구원 선량평가시스템 고도화 / 발주기관: 한국원자력연구원

문서(문서3)에 근거한 확인된 요구사항 요약:
- 기술이전 계획은 한국원자력연구원과 협의하여 작성해야 함.
  - 포함사항: 기술이전 대상 및 내용(운영시 필요하거나 경미한 장애조치·응급조치 기술 등 포함), 기술이전 방법, 기간, 인원.
- 기술지원 조직 구성 및 절차 수립: 체계적 기술지원 조직을 구성하고 사업종결 시점까지 실질적 기술지원 수행.
- 지속적 정보제공 및 기술자문: 사업으로 습득된 노하우 및 관련 IT 정보를 지속 제공하고 기술자문 수행.
- 향후 기능보완·시스템확장·타 기종 연계·S/W 업그레이드 등에 필요한 제반 기술사항 적극 지원.
- 추가제안(PSR-004): 사업수행자가 필요하다고 판단하는 추가 제안 가능하나, 사업과 연관성이 적은 제안은 지양.
- 입찰방식: 「국가를 당사자로 하는 계약에 관한 법률시행령」에 의거 협상에 의한 계약체결 적용(세부는 기획재정부 계약예규 등 준용).

제공된 문서에서 확인할 수 없습니다:
- 구체적 기능 요구사항(세부 기능 목록), 성능 수치(처리속도·가용성 등), 데이터 요구·변환 계획, 보안 요구사항 세부, 시험·인수 기준, 상세 산출물 목록 등은 제공된 문서에서 확인할 수 없습니다.
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 65.3; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서에서 확인할 수 없습니다.

근거 문서(사업명 / 발주기관):
- 문서1: 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / (사)부산국제영화제
- 문서2: [재공고]차세대 통합정보시스템(ERP) 구축 / 한국가스공사
- 문서3: 차세대 포털·학사 정보시스템 구축사업 / 고려대학교
- 문서4: 도시계획위원회 통합관리시스템 구축용역 / 인천광역시
- 문서5: 예약발매시스템 개량 ISMP 용역 / 한국철도공사
- 문서6: 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 인천광역시
- 문서7: 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 / 수협중앙회
- 문서8: 차세대 포털·학사 정보시스템 구축사업(부분) / 고려대학교
```

### filter_on_rewrite_off

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 88.93; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단

요약(근거: 제공된 문서들: 문서6, 문서4, 문서8, 문서3 등)

1) 요구사항 분류(주요 항목 및 고유번호)
- 교육운영(FUR)
  - FUR-001 국민연금공단 역량모델 기반 TRM 제시
  - FUR-002 교육운영 방법 제시
  - FUR-003 교육 예상인원 제시
  - FUR-004 외부콘텐츠 제시 기준
  - FUR-005 외부콘텐츠 기타 요청사항
- 이러닝 시스템 운영(SFR)
  - SFR-001 이러닝시스템 구축 및 관리 기본방향
  - SFR-002 사이버(모바일)연수원 구축
  - SFR-003 “학습 이벤트” 운영
  - SFR-004 “큐레이션 서비스” 운영
  - SFR-005 “소셜러닝” 운영
  - SFR-006 “나의 학습노트” 운영
  - SFR-007 “직무지식진단” 운영
  - SFR-008 “역량진단” 운영
- 학사관리(LMR)
  - LMR-001 학습관리시스템(LMS) 제공
  - LMR-002 학습참여 유인체계 제시
- 콘텐츠 개발/관리(DER)
  - DER-001 콘텐츠 개발 범위
  - DER-002 콘텐츠 개발 요건
  - DER-003 콘텐츠 검사 및 검수
- 품질(QUR)
  - QUR-001 교육콘텐츠 평가 및 품질관리 방안 제시
- 유지관리(MAR)
  - MAR-001 유지관리(관리 범위) 제시

2) 프로젝트 관리·대금·보고(근거: 문서4)
- 대금결제(PMR-004)
  - 콘텐츠 개발: 검수완료 후 지급
  - 콘텐츠 및 P/G 유지보수·관리: 상/하반기 2회 지급(각 반기 말)
  - 교육운영: 월별 또는 분기별 지급
- 보고서·산출물 제출
  - 정기보고: 착수보고(1회), 월간 업무현황(월1회), 중간보고(분기1회), 최종보고(1회)
  - 비정기 산출물: 차시별 원고·스토리보드(2부), 검토결과 조치내역서, 사업완료보고서(2부), 운영자 지침서(2부), 유지보수 계획서(2부), 산출물 일체(소스 등) 외장HDD 1부 등
  - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출

3) 보안·개인정보·인수인계(근거: 문서6, 문서8)
- 정보보안·개인정보보호 규정 준수 및 보안관리 방안 제시 요구
- 인수인계 시 공단 보유 프로그램 및 데이터 이전 방안 제시
- 이전(퇴직) 업체는 공단 관련 자료를 지체 없이 전수 파기하고 공단 직원의 폐기 확인을 받아야 함
- 인수자·인계자 간 인수·인계 계획 및 완료확인서 서면 제출(30일 이내 인수·인계 완료, 공단이 미흡 판단 시 기간 연장 가능)

4) 입찰·참가자격(근거: 문서3, 문서8 일부)
- 원격평생교육시설 인가 및 이러닝사업자(이러닝콘텐츠업 또는 이러닝서비스업) 신고 등 참가자격 명시
- 전자입찰(나라장터) 관련 업종코드 등록 요구

제공된 문서에서 확인할
...(truncated; full text is in report_evidence.json)
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 88.93; coverage: 1.0; first_hit_rank: 2; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: KOICA 전자조달, 국민연금공단, 재단법인 한국장애인문화예술원, 국민연금공단, 재단법인 한국장애인문화예술원, (사)부산국제영화제, 국민연금공단, 조선대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단

콘텐츠 개발·관리 요구사항(문서 기준, 핵심만)

1. 개발 전반
 - 요청 즉시 개발 수행 및 개발 컨설팅·개발계획서 제출(문서4).  
 - 개발 완료 후 유지보수·호환성·확정성 고려, 수정·추가·삭제가 용이하도록 개발(문서4).  
 - 하도급은 공단 사전승인 필요, 하도급율 50% 초과 불가, 재하도급 원칙 금지(문서4).

2. 콘텐츠 형식·설계
 - 차시별 동영상 타입으로 30~40분 내외로 개발(문서4).  
 - 웹(PC)과 모바일 연동되는 스마트러닝 설계(문서4).  
 - 주제별 세분화된 모듈로 1차시 구성 및 모듈별 게시 가능하도록 개발(문서4).  
 - 멀티미디어·엔터테인먼트 요소 등 학습자 중심 설계(문서4).  
 - 콘텐츠와 “나의 학습노트” 연동 가능하도록 개발(문서4).  
 - 공단 네트워크 환경(업무망 분리 등)을 고려해 네트워크 부하가 적은 기술 적용(문서4).  
 - 디자인·이미지 등은 3종 이상 제안(문서4).  
 - 공단이 제공한 교안(PPT 등)과 음성녹음 파일을 합본(싱크 조절 포함), 스크립트(자막) 포함하여 개발(문서4).

3. 산출물 및 제출·검수
 - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출(문서2).  
 - 차시별 원고·스토리보드(각 2부, 바인더·CD), 검토결과 조치내역서(조치시 1부), 사업완료보고서·운영자 지침서·유지보수 계획서(각 2부, 바인더·CD), 소스 일체(외장HDD 1부) 등 제출(문서2).  
 - 산출물 제출 방법·시기 등은 공단과 협의 가능(문서2).

4. 유지관리·검수·대금
 - 콘텐츠 개발은 검수완료 후 대금 지급(문서2 PMR-004).  
 - 콘텐츠 및 P/G 유지보수는 연 2회(상·하반기) 지급(문서2 PMR-004).

5. 외부콘텐츠 연계
 - 공단 본부 요청 시 제공 가능한 외부콘텐츠 우선 제공(문서7).  
 - 교재 제공 협조, 부족 시 교안 등 학습자료 제공(문서7).  
 - 신입직원 조직적응을 위한 단계별 콘텐츠 제시(문서7).  
 - 모바일연동 과정에 대한 학습방법 안내 등 학습자별 적합 서비스 제공(문서7).  
 - HRD 담당자 역량 강화를 위한 콘텐츠 제시(문서7).

6. 품질관리·평가
 - 콘텐츠 품질 관리 평가기준 및 관리방안 제시(교체·업그레이드·퇴출 방안 포함)(문서7 QUR-001).  
 - 불량·기준미달 콘텐츠는 변경 또는 추가 제공, 민원 빈발 시 공단과 협의해 교체(문서7 QUR-001).  
 - 연 2회 이상 정기적 콘텐츠 관리(최신성·인기도·만족도 등으로 교체·정비)(문서7 QUR-001).  
 - 학습자 불편·문제 제기 발생 시 원인파악 후 즉시 보고하고 수정·보완 또는 교체 방안 제시(문서7 QUR-001).

주의:
...(truncated; full text is in report_evidence.json)
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 88.93; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
예. 제공된 문서에서 확인되는 교육·학습 관련 발주 사업은 다음과 같습니다(사업명 / 발주기관):

- 2024년 이러닝시스템 운영 용역 / 국민연금공단 (문서4·7·8)
- 차세대 포털·학사 정보시스템 구축사업 / 고려대학교 (문서3)
- JST 공유대학(원) xAPI기반 LRS시스템 구축 / 전북대학교 (문서6)
- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 — 교육지원 요구사항 포함 / 인천광역시 (문서1)
- 정읍체육트레이닝센터 통합운영관리시스템 구축 용역(협상에의한계약,긴급) / 전북특별자치도 정읍시 (문서5)

이 외에 추가로 교육·학습 관련 다른 기관의 발주 여부는 제공된 문서에서 확인할 수 없습니다.
```

#### q5_followup - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 88.93; coverage: 0.0; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 재단법인 광주광역시 광주문화재단, 한국가스공사, 한국건강가정진흥원, 파주도시관광공사, 수협중앙회, 을지대학교, (사）한국대학스포츠협의회, (사)부산국제영화제
- flags: coverage_below_target, missing_llm_judge_score
- interpretation: Retrieval did not cover all target organizations; inspect filtering, rewrite, and MMR diversity.

Answer excerpt:

```text
요청하신 모니터링 관련 요구사항은 아래 사업문서들에서 확인됩니다. (근거: 각 문서 명/발주기관 표기)

- 사업명: 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / 발주기관: (사)부산국제영화제  
  - 상시 모니터링 및 장애예방·장애처리 활동 요구.  
  - 정기 예방점검(月 1회) 실시 요구.  
  - 장애 발생 시 즉시 조치, 장애접수 후 4시간 이내 보수 가능하도록 대응 요구.  
  - “인적자원 활용한 모니터링” 명시. (문서8, MAR-003·MAR-004)

- 사업명: 2025년 아이돌봄인력 인적성 검사 정보시스템 운영 / 발주기관: 한국건강가정진흥원  
  - 예방점검 계획 수립 및 정기점검 수행 요구(점검결과 보고서 제출).  
  - 진흥원 요청 시 정기외 수시점검 실시 요구.  
  - 장애 발생 시 로그 수집 및 장애처리 이력 관리·보고 요구.  
  - 장애 신고 시 신고접수 시각으로부터 2시간 이내 착수(업무시간 내 내부업무 서비스 중단 시 장애처리시간: 8시간 이내). (문서3, MAR 관련)

- 사업명: 종량제봉투 판매관리 전산시스템 개선사업 / 발주기관: 파주도시관광공사  
  - 시스템 모니터링 관련 성능요구(오류응답시간·느린작업 응답표시 등) 명시.  
  - 동시 사용자 기준(시스템당 동시 사용자 100명 이상 지원) 등 성능 모니터링 근거 존재. (문서4, PER-003 등)

- 사업명: KUSF 체육특기자 경기기록 관리시스템 개발 / 발주기관: (사)한국대학스포츠협의회  
  - 시스템 관리자 매뉴얼에 로그 및 백업 관리 등 운영·관리(모니터링 관련 항목) 포함 요구. (문서7)

제공된 문서에서 위 네 건에서 명시적 모니터링·점검·장애대응 관련 요구사항을 확인할 수 있습니다. 다른 제공 문서들에서는 명확한 모니터링 요구사항이 명시되어 있지 않습니다. (근거: 각 문서 내용)
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 88.93; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
요청하신 비교는 아래 내용으로 정리합니다. 근거가 된 사업명/발주기관을 각 항목에 명시합니다.

1) 사업 목적
- 고려대학교(차세대 포털·학사 정보시스템 구축사업): 노후 시스템의 차세대 구축을 통해 정보서비스 품질 강화 및 대학 교육시스템 경쟁력 확보(문서1, 문서3).  
- 광주과학기술원(학사시스템 기능개선 사업): 학사조직 개편 및 학위 연계과정 신설·구분 변경에 따른 시스템 기능 개선으로 업무 편의성·효율성 제고(문서7).

2) 사업 범위·주요 기능
- 고려대학교: 통합로그인·통합·지능형 검색, 마이페이지, 공지/알림, 일정관리, 커뮤니티/게시판, 개인화(위젯), 연계서비스(웹메일, 챗봇, 전자결재, 학사/행정), SSO·간편·2차인증, 사용자 통합관리, 역할기반 검색 우선노출, 모바일(기존 호잇 앱 하이브리드 재구축 + 모바일웹, 푸쉬) 등 포털·학사 통합 응용SW 전반 개발(문서1, 문서8).  
- 광주과학기술원: 학사 조직개편에 따른 시스템 개선 및 학위연계과정(학석연계, 학석박통합연계 등)·대학원 과정변경 관련 메뉴·프로세스 개발(FUR-005, FUR-006 등), 구체적 기능·성능 요구 명시(문서4, 문서7).

3) 대상범위·규모
- 고려대학교: 학생(졸업생 포함), 교직원, 연구원 대상, 기관 인원(예: 서울캠퍼스 학부 20,373명 등) 제시 — 대규모 사용자 대상(문서1, 문서5).  
- 광주과학기술원: 대상 사용자 수치 등 규모 정보는 제공된 문서에서 확인할 수 없습니다(문서2, 문서7).

4) 예산 및 기간
- 고려대학교: 사업예산 11,270,000,000원(VAT 포함), 계약일로부터 24개월 이내, 무상유지보수 12개월(문서3).  
- 광주과학기술원: 사업비 157,300,000원(VAT 포함), 기간(사업완료 기한)은 제공된 문서에서 확인할 수 없습니다(문서7).

5) 계약·지급·수급 관련
- 고려대학교: 제한경쟁입찰(협상에 의한 계약), 사업비 연도별 분할지급(2024·2025·2026 학년도 비율 기재)(문서3).  
- 광주과학기술원: 공개경쟁입찰(협상에 의한 계약), 선금 50% 지급·잔금은 최종검수 완료 시 지급, 공동수급불가(문서7).

6) 기술·품질·준수요건
- 고려대학교: 행정안전부 고시 등 관련 지침(전자정부 웹사이트 품질관리 등) 준수, 시큐어코딩 적용, 프레임워크·UI·코드 표준화, 기존 기능 모두 구현·연계 변경 관리 등 엄격한 준수 요구(문서6).  
- 광주과학기술원: 기능·성능 요구사항(FUR·PER 등) 및 제안·평가 기준(목차에 포함) 제시 — 다만 광주과기원 문서에서 행정안전부 고시 준수 등 구체적 표준 준수 의무는 제공된 문서에서 확인할 수 없습니다(문서2, 문서4).

7) 기타 특징
- 고려대학교: 대규모 전면 재구축(포털+학사 통합), 모바일 앱 하이브리드 재구축, 주사업
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 88.93; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 고려대학교(사업명: 차세대 포털·학사 정보시스템 구축사업): 있음. 문서(요구사항 PER-002, PER-003)에 업무응답시간·웹페이지 디스플레이시간 모두 "사용자 요청으로부터 3초 이내" 처리 요구(대량데이터·대형이미지·동시사용자(90% 초과) 등 예외 규정 포함). (근거: 제공문서 중 문서4)

- 광주과학기술원(사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업 및 학사시스템 기능개선 사업): 제공된 문서들에서는 응답시간(초 단위) 요구사항이 명시되어 있지 않습니다. 제공된 문서에서 확인할 수 없습니다. (근거: 제공문서 중 문서1, 문서7, 문서5)
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 88.93; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서들에서는 우주 로켓 발사 시스템 구축 사업을 확인할 수 없습니다.

근거 문서(사업명 / 발주기관):
- 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / (사)부산국제영화제  
- [재공고]차세대 통합정보시스템(ERP) 구축 / 한국가스공사  
- 차세대 포털·학사 정보시스템 구축사업 / 고려대학교 (문서3, 문서8)  
- 도시계획위원회 통합관리시스템 구축용역 / 인천광역시  
- 예약발매시스템 개량 ISMP 용역 / 한국철도공사  
- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 인천광역시  
- 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 / 수협중앙회
```

### filter_off_rewrite_on

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 82.85; coverage: 0.0; first_hit_rank: None; abstention: True; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 수협중앙회, 서민금융진흥원, KOICA 전자조달, 재단법인스포츠윤리센터, 한국연구재단, 한국농수산식품유통공사, 인천광역시 동구, 한국철도공사 (용역)
- flags: coverage_below_target, false_abstention, missing_llm_judge_score
- interpretation: The system refused despite a non-abstention case; inspect abstention prompt and evidence confidence.

Answer excerpt:

```text
제공된 문서들(근거: 문서1 수협중앙회 수산물사이버직매장 / 문서2 서민금융진흥원 채팅상담시스템 / 문서3 KOICA 우즈베키스탄 국회방송 PMC / 문서4 스포츠윤리센터 LMS 개선 / 문서5 한국연구재단 기초학문자료센터 / 문서6 한국농수산식품유통공사 농산물가격안정기금시스템 / 문서7 인천 동구 박물관 전시해설시스템 / 문서8 한국철도공사 예약발매시스템)를 검토한 결과,

요청하신 "국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항"은 제공된 문서에서 확인할 수 없습니다.

국민연금공단 관련 또는 해당 이러닝사업의 RFP/요구사항 문서를 제공해 주시면, 그 문서에 근거해 요구사항을 정리해 드리겠습니다.
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 82.85; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 재단법인 한국장애인문화예술원, 국민연금공단, 국민연금공단, (사)부산국제영화제, 국민연금공단, 고려대학교, KOICA 전자조달
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단 (제안요청서, 참고문서)

요약(콘텐츠 개발·관리 주요 요구사항)
- 요구사항 분류: DER-001~DER-003(콘텐츠 개발 범위·요건·검사·검수), MAR-001(유지관리) 등으로 구성됨. (근거: 제안요청서 요구사항 구성)

개발·제작 프로세스 및 산출물
- 개발요청 즉시 수행, 개발컨설팅 지원 및 개발계획서 제출, 개발안내 워크숍 개최(근거: 문서6).  
- 설계서·스토리보드 작성 후 공단 담당자·내용전문가 검토·수정·보완, 프로토(시범) 차시 검토·공단 승인 후 전체 차시 개발(근거: 문서6).  
- 콘텐츠 검사·검수 절차 요구(검수 일정·방식은 제안요청서 기준에 따름). (근거: DER-003 항목 명시 및 문서6)

콘텐츠 제작 기준
- 차시별 동영상 타입 길이: 30~40분 내외(근거: 문서6).  
- 웹 학습과 모바일 학습 연동(스마트러닝) 설계(근거: 문서6).  
- 주제별 세분화된 모듈로 1개 차시 구성, 모듈별 게시 가능하도록 개발(근거: 문서6).  
- 멀티미디어·엔터테인먼트 요소 적용 등 학습자 중심 설계(근거: 문서6).  
- “나의 학습노트”와 연동 가능하도록 개발(근거: 문서6).  
- 공단 네트워크(업무망 분리 등)를 고려해 네트워크 부하가 적은 기술 적용(근거: 문서6).  
- 교안(PPT) 및 음성녹음 파일 합본(싱크 조절 포함), 스크립트(자막) 작업 포함(근거: 문서6).  
- 디자인·이미지 등은 3종 이상 제안(근거: 문서6).

유지보수·하자보수·연동
- 시스템 변경 시 콘텐츠 변환·연동 수행(문서3).  
- 콘텐츠 일부 수정·오탈자 정정 및 관련 자료 연결 등 지원(문서3).  
- 하자보수: 최종 검수 후 콘텐츠의 20% 범위 내에서 최소 1년 이내 지원(문서3).  
- 사업기간 종료 후 하자보수 범위 및 추진체계 제시 요구(문서3).  
- 선정업체는 이러닝 관련 기술정보·기술자문을 공단에 무상 제공(문서3).

하도급·지적재산권·보안·인수인계
- 하도급: 사전승인 필요, 하도급 비율 50% 초과 금지, 재하도급 원칙 금지(문서6).  
- 정보보안·개인정보보호 규정 준수 및 보안관리 방안 제시 요구(문서1·문서4).  
- 인수인계 시 공단 보유 프로그램·데이터 이전 방안 제시 요구(문서1).

보고·제출
- 개발된 모든 산출물·콘텐츠·보고서를 개발일정에 따라 제출(문서3 PMR-003).  
- 콘텐츠 개발 완료 최소 14일 전에 사업완료보고서 초안 제출(문서3 PMR-003).

제공된 문서에서 확인되는 내용은 위와 같습니다. 다른 세부 항목(예: 검수 세부기준, 보상·평가 세부절차 등)은 제공된 문서에서 확인할 수 없습니다.
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 82.85; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
예. 제공된 문서 내 교육·학습 관련 발주사업(사업명/발주기관)은 다음과 같습니다.

- 사업명: 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 발주기관: 인천광역시 — 교육지원(발주기관 직원 대상 교육계획·교육실시 의무) 명시 (문서1).  
- 사업명: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교 — 학교현장실습 관리·교직 이수요건 등 교육 관련 기능 포함 (문서3).  
- 사업명: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단 — 이러닝 콘텐츠·평가·수강인원 등 교육 운영 전반 명시(문서4, 문서7, 문서8).  
- 사업명: JST 공유대학(원) xAPI기반 LRS시스템 구축 / 발주기관: 전북대학교 — 학습기록(LRS) 관련 시스템 구축 사업 (문서6).

이 외에 제공된 문서에서 추가적인 교육/학습 관련 발주사업은 확인할 수 없습니다.
```

#### q4_single_check - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나?
- EDD: 82.85; coverage: 0.0; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=5, relevance=5
- retrieved_orgs: 서울특별시교육청, 고려대학교, 한국원자력연구원, KOICA 전자조달, 서울특별시 여성가족재단, 고려대학교, 한국농어촌공사, 한영대학
- flags: coverage_below_target
- interpretation: Retrieval did not cover all target organizations; inspect filtering, rewrite, and MMR diversity.

Answer excerpt:

```text
제공된 참고문서들(문서1~문서8: 서울특별시교육청 ISP, 고려대학교 차세대 포털·학사시스템, 한국원자력연구원 선량평가시스템, KOICA 우즈베키스탄 국회방송 PMC, 서울특별시 여성가족재단 디지털성범죄 삭제지원, 고려대학교 등)에는 "기초과학연구원 극저온시스템" 사업 관련 내용이 포함되어 있지 않습니다.  
따라서 제공된 문서에서 기초과학연구원 극저온시스템 사업의 AI 기반 예측 요구사항은 확인할 수 없습니다.
```

Judge reason excerpt:

```text
검색된 근거들은 서울시교육청, 고려대학교, 한국원자력연구원 등 다른 사업들의 요구사항을 포함하고 있으며 '기초과학연구원 극저온시스템' 또는 해당 사업의 AI 기반 예측 요구사항에 대한 언급이 전혀 없습니다. 답변은 이 근거들에 근거하여 제공된 문서에서는 해당 요구사항을 확인할 수 없다고 직접적으로 결론내리고 있어 근거 기반이며 질문에 적절히 응답하고 있습니다.
```

#### q5_followup - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 82.85; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 기초과학연구원, 한국가스공사, 중앙선거관리위원회, 한국농어촌공사, 경희대학교, 전북대학교, 기초과학연구원, 중앙선거관리위원회
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
있습니다.

- 2025년도 중이온가속기용 극저온시스템 운전 용역 / 기초과학연구원:
  - 주요 수치 항목을 전자파일로 기록(기록 항목·간격은 연구원이 정함). 연구원 요청 시 주요 수치들에 대한 분석 수행(분석 대상·방법·결과물 형태는 연구원이 결정). 노트북 등 컴퓨터 악세서리 계약자 준비 필요. (근거: 문서1)
  - 모니터링 업무 목록(표 4): 알람 메시지 확인, 주요 센서 트렌드 확인(온도·압력·유량·속도 등), 정상 운전 시 지시값 파악·숙지, 비정상 운전 상황 감지, 연구원 요청 시 지정 값 관찰·확인·상황 전달(무전 통신 사용·무전기 제공), 제어로직 정상 작동 여부 확인, 현장 상황 일시적·지속적 관찰(요청 시, 비방사선구역 한정), 기타(주기적 현장 순찰 포함). (근거: 문서1, 문서7)
  - 운전 중 수리가 필요한 사항 별도 기록 및 연구원 요청에 따른 제어시스템(알람 포함) 개선 협조 등 요구사항 존재. (근거: 문서7)

- 중앙선거관리위원회 행정정보시스템 위탁운영사업 / 중앙선거관리위원회:
  - “상시 시스템 모니터링을 통한 시스템 성능 유지 및 고도화” 및 장애 사전예방·신속대응 체계 구축 요구. (근거: 문서3)

- JST 공유대학(원) xAPI기반 LRS시스템 구축 / 전북대학교:
  - 24시간×365일 무중단 인프라 관제, 주기적 S/W 업데이트, 웹방화벽 설치·모니터링, 장애 시 신속 조치·데이터 백업 등 상시 모니터링·장애대응 요구. (근거: 문서6)

- 산학협력단 정보시스템 운영(경희대학교):
  - 정보시스템 최적화 유지를 위한 선제적 예방 조치 및 상시 모니터링 요구(장애·응답 대응 포함). (근거: 문서5)

참고: 위 내용은 제공된 문서들에 명시된 모니터링 관련 요구사항만을 정리한 것입니다.
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 82.85; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 서울시립대학교, 고려대학교, 대전대학교, 서영대학교 산학협력단, 조선대학교, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
다음 비교는 오직 제공된 문서 내용만을 근거로 합니다. (근거 문서: 고려대학교 차세대 포털·학사 정보시스템 구축사업 — 문서1, 문서4, 문서8 / 광주과학기술원 학사시스템 기능개선 사업 — 문서2)

1) 사업 목적
- 고려대학교(차세대 포털·학사 정보시스템): 노후화된 시스템을 차세대로 구축하여 정보서비스 품질 강화 및 대학 교육 시스템 경쟁력 확보(문서1).  
- 광주과학기술원(학사시스템 기능개선): 제공된 문서에서 확인할 수 없습니다(문서2).

2) 사업 범위·주요기능
- 고려대학교: 포털(통합로그인, 통합·지능형 검색, 마이페이지, 공지/알림, 일정관리, 커뮤니티, 게시판, 개인화 위젯, 연계서비스(웹메일, 챗봇, 전자결재, 학사/행정 등) 등), 사용자별 정보 제공·검색 우선노출·SSO·간편/2차인증, 모바일 포털(기존 앱 '호잇' 하이브리드 재구축 포함) 등 응용SW 개발(문서1, 문서8).  
- 광주과학기술원: 요구사항·범위 관련 항목(요구사항 총괄표, 상세 요구사항 등)이 목차에 있으나 구체 내용은 제공된 문서에서 확인할 수 없습니다(문서2).

3) 목표 대상 사용자
- 고려대학교: 학생(졸업생 포함), 교직원, 연구원 등 내부 구성원 대상 포털(문서1).  
- 광주과학기술원: 제공된 문서에서 확인할 수 없습니다(문서2).

4) 사업기간·유지보수
- 고려대학교: 계약일로부터 24개월 이내 수행, 무상유지보수 기간 사업종료일로부터 12개월(문서4).  
- 광주과학기술원: 제공된 문서에서 확인할 수 없습니다(문서2).

5) 예산·지급
- 고려대학교: 사업예산 11,270,000,000원(VAT 포함), 3년 분할 지급(2024≈30%, 2025≈40%, 2026≈30%)(문서4).  
- 광주과학기술원: 제공된 문서에서 확인할 수 없습니다(문서2).

6) 계약·입찰 방식
- 고려대학교: 제한 경쟁 입찰(협상에 의한 계약)(문서4).  
- 광주과학기술원: 목차에 입찰방식/평가 관련 항목 존재하나 구체 방식은 제공된 문서에서 확인할 수 없습니다(문서2).

7) 기술·플랫폼 정보
- 고려대학교: 주요 구성에 Java/Spring 기반 포털(KUPID), 통합인증 SafeIdentity, 통합검색 Search Formula-1, 모바일(호잇)에는 Spring Boot/Java/Kotlin/Swift 등 기술 언급(문서8).  
- 광주과학기술원: 제공된 문서에서 확인할 수 없습니다(문서2).

8) 평가·선정 관련
- 고려대학교: 제안서 작성·효력 등 상세 지침 포함(문서4 일부).  
- 광주과학기술원: 제안서 평가방법·기술성 평가기준 등 목차 존재(문서2)나 세부 기준은 제공된 문서에서 확인할 수 없습니다.

요약: 고려대학교 사업은 목적·범위(포털/모바일/검색 등), 기간(24개월), 예산(약 112.7억 원), 유지보수(12개월
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 82.85; coverage: 1.0; first_hit_rank: 2; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 서영대학교 산학협력단, 광주과학기술원, (사)부산국제영화제, 고려대학교, 대전대학교, 한국원자력연구원, (사）한국대학스포츠협의회, 인천광역시
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교  
  → 제공된 문서(문서4)에서 응답 시간(응답속도)에 대한 요구사항은 확인할 수 없습니다. (제공된 문서에서 확인할 수 없습니다)

- 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업 / 발주기관: 광주과학기술원  
  → 제공된 문서(문서2)에서 응답 시간(응답속도)에 대한 요구사항은 확인할 수 없습니다. (제공된 문서에서 확인할 수 없습니다)
```

#### q9_imprecise_org - issue_or_audit_queue

- question: 원자력연구소에서 방사선량 평가하는 시스템 사업 요구사항 알려줘
- EDD: 82.85; coverage: 1.0; first_hit_rank: 3; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 한국연구재단, 한국생산기술연구원, 한국원자력연구원, 한국철도공사 (용역), 재단법인 광주광역시 광주문화재단, 국방과학연구소, 울산광역시, 국가과학기술지식정보서비스
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거 문서: 사업명 "한국원자력연구원 선량평가시스템 고도화" / 발주기관: 한국원자력연구원

요구사항(문서에 명시된 내용만):

- 기술이전 계획 수립 및 이행: 한국원자력연구원과 협의하여 기술이전 대상 및 내용(시스템 운영에 필요한 경미한 장애조치·응급조치 기술 등 포함), 기술이전 방법, 기간, 인원 등을 계획에 포함하고 수행할 것.  
- 기술지원 조직 및 절차 구성: 기술지원을 위한 조직을 구성하고 체계적인 기술지원 절차를 수립하여 사업 종료 시점까지 실질적 기술지원을 수행할 것.  
- 지속적 정보제공 및 기술자문: 사업 수행으로 획득한 노하우 및 관련 정보기술을 지속적으로 제공하고 기술자문을 제공할 것.  
- 향후 보완·확장 지원: 발주기관이 기능 보완, 시스템 확장, 타 기종 연계, S/W 업그레이드 등을 하고자 할 경우 필요한 제반 기술사항을 적극 지원할 것.  
- 추가제안 허용(제한): 사업수행자의 창의적 판단에 따른 추가제안 사항 제출 가능하되, 본 사업과 연관성이 적은 제안은 지양할 것(요구사항 고유번호 PSR-004).

제공된 문서에서 확인할 수 없는 사항: 인력·인원 수치, 세부 산출물 목록, 성능·기능 요구사항 등 구체적 기술요구 및 일정·평가기준 등은 제공된 문서에서 확인할 수 없습니다.
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 82.85; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서에서 확인할 수 없습니다.

근거 문서(사업명 / 발주기관):
- 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 입찰 공고 / (사)부산국제영화제
- [재공고]차세대 통합정보시스템(ERP) 구축 / 한국가스공사
- 차세대 포털·학사 정보시스템 구축사업 / 고려대학교
- 도시계획위원회 통합관리시스템 구축용역 / 인천광역시
- 예약발매시스템 개량 ISMP 용역 / 한국철도공사
- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 인천광역시
- 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 / 수협중앙회
```

### filter_on_rewrite_on_control

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 91.21; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "2024년 이러닝시스템 운영 용역", 발주기관 국민연금공단 (제공문서 기준)

요구사항 요약 — 핵심 항목만 정리합니다.

1) 요구사항 구성(분류·식별)
- 교육운영 관련: FUR-001 ~ FUR-005 (역량모델 기반 TRM, 교육운영방법, 교육예상인원, 외부콘텐츠 제시 기준 등). (국민연금공단 2024년 이러닝시스템 운영 용역)
- 이러닝시스템 운영 관련: SFR-001 ~ SFR-008 (시스템 기본방향, 사이버/모바일 연수원, 학습 이벤트, 큐레이션, 소셜러닝, 나의 학습노트, 직무지식진단, 역량진단). (동문서)
- 학사관리: LMR-001 ~ LMR-002 (LMS 제공, 학습참여 유인체계). (동문서)
- 콘텐츠 개발·관리: DER-001 ~ DER-003 (개발범위, 개발요건, 검사·검수). (동문서)
- 유지관리: MAR-001 (관리 범위). (동문서)
- 품질: QUR-001 (콘텐츠 평가 및 품질관리 방안 제시). (동문서)

2) 개인정보보호·정보보안 및 인수인계
- 정보보안·개인정보보호 규정 준수 및 보안관리 방안 제시 요구. (국민연금공단 이러닝시스템 운영 용역)
- 인수인계 시 공단 보유 프로그램 및 데이터 이전 방안 제출 요구. (동문서)
- 인수인계 절차: 인수자·인계자 간 인수·인계 계획·결과 및 완료확인서 서면 제출, 인수·인계는 원칙 30일 이내 완료(공단이 미흡하다고 판단 시 연장 가능). 이전 업체는 공단 관련 자료 전수 파기하고 공단 직원의 폐기 완료 확인 받아야 함. (동문서)

3) 산출물·보고 및 제출 형식
- 사업완료보고서 초안은 콘텐츠 개발 완료 최소 14일 전에 제출해 심의 받아야 함. (국민연금공단)
- 정기보고: 착수보고서(1회), 월간업무현황보고서(월1회), 분기 중간보고서(분기1회), 최종보고서(1회). (동문서)
- 비정기 산출물 및 제출형태: 차시별 원고·스토리보드(2부, 바인더·CD), 검토결과 조치내역서(1부, 바인더), 사업완료보고서(2부, 바인더·CD), 운영자 지침서(2부), 유지보수 계획서(2부), 산출물 일체(소스·스토리보드 등)(1부, 외장HDD). (동문서)
- 제출 방법·시기는 공단과 협의 후 결정될 수 있음. (동문서)

4) 대금결제 및 유지보수 지급 조건
- 콘텐츠 개발: 검수완료 후 지급. (국민연금공단)
- 콘텐츠 및 P/G 유지보수·관리: 상/하반기 2회 지급(각 반기 말). (동문서)
- 교육운영 관련 비용: 월별 또는 분기별 지급. (동문서)

5) 입찰·계약 관련(참가자격·방법)
- 참가자격: 국계법 시행령 등 법적 자격요건 충족 업체, 평생교육법에 따른 원격평생교육시설 인가 및 이러닝사업자 신고, 나라장터에 이러닝콘텐츠업(6527) 또는 이러닝서비스업(6529) 등록 등. (국민연금공단 입찰 관련 서류)
- 입찰방법: 일반경쟁입찰, 계약방법:
...(truncated; full text is in report_evidence.json)
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 91.21; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "2024년 이러닝시스템 운영 용역", 발주기관 "국민연금공단" (제공된 문서들)

콘텐츠 개발·관리 요구사항(문서에 명시된 항목만)

1. 개발 범위 및 목적
 - 직무 콘텐츠 개발·운영 및 위탁(자기개발) 콘텐츠 운영(직무교육 대상 예: 11,000명) (문서6).  
 - AI, 빅데이터, AR/VR 등 4차산업 융합콘텐츠, 마이크로러닝, 블렌디드 러닝, 법정의무교육 패키지화 등 대상 콘텐츠 유형 제시 (문서3).

2. 산출물·제출물·형태
 - 콘텐츠 원본 및 완성본을 인재개발부 1부·해당부서 1부 제공. 교재 활용을 위해 PPT 등으로 다운로드 가능하도록 구현 (문서2).  
 - 제출 산출물: 차시별 원고·스토리보드(2부, 바인더·CD), 검토결과 조치내역서(1부), 사업완료보고서(2부, 바인더·CD), 운영자 지침서(2부), 유지보수 계획서(2부), 산출물 일체(소스·스토리보드 등) 1부(외장HDD) 등 규정(문서4).  
 - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출(문서4).

3. 품질·검수·지급
 - 교육콘텐츠 평가 및 품질관리 방안 제시 요구(QUR-001) (문서7).  
 - 콘텐츠 개발 대금은 검수완료 후 지급(문서4, PMR-004).  
 - 검수 절차의 세부 항목·기준은 제공된 문서에서 상세 내용 확인 불가함(문서7·문서4에 명시된 검수 완료·제출 항목은 위에 기재).

4. 유지관리(개편·업데이트) 요구사항
 - 최신 법령·지침 등 상시 업데이트 가능한 관리프로세스 운영(문서2 MAR-002).  
 - 콘텐츠 유지보수: 차시별 관리, 텍스트 수정, 차시 재구성 등, 스토리보드를 활용해 수정·보완 용이성 확보 요구(문서2 MAR-002).

5. 기술·보안·규격 관련
 - 콘텐츠 및 관련 프로그램·소스 포함 전달(외장HDD) 요구(문서4).  
 - 일부 프로그램(예: 나의 학습노트, 역량진단 등)에 사용된 기술스택 예시(MS‑SQL2005, JAVA, JSP, XML, ActiveX 등) 표기(문서2 MAR-001).  
 - 정보보안·개인정보보호 규정 준수 및 인수인계 시 공단 보유 프로그램·데이터 이전 방안 제시 요구(문서7, 문서6).  
 - 정보시스템 설계·구축 관련 각종 정부 지침(정보화 표준·접근성·클라우드 등) 준수 요구(문서8).

6. 기타 절차·제출 주기
 - 정기보고서 제출: 착수 1회, 월간업무현황 월1회, 중간(분기)·최종보고 등 규정(문서4).  
 - 산출물 제출 시기·형태는 공단과 협의 후 결정될 수 있음(문서4).

제공된 문서에서 확인할 수 없는 사항
 - DER-001(구체적 개발범위의 세부 목록), DER-002(구체적 개발요건의 세부 기술 사양), DER-003(검수·검사 절차의 상세 기준 및 체크리스트)은 문서에 제목 및 일부 일반요건만 명시되어 있으나
...(truncated; full text is in report_evidence.json)
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 91.21; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=1, relevance=4
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: low_groundedness
- interpretation: LLM judge found a quality issue; inspect answer-evidence alignment, not only retrieval metrics.

Answer excerpt:

```text
다음 발주사업들이 교육·학습 관련 내용으로 확인됩니다 (근거: 각 참고문서):

- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 발주기관: 인천광역시 — 문서에 "교육지원", "교육계획서" 명시 (문서1).  
- 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교 — 학교현장실습·교직 이수요건 등 교육관리 기능 설명 포함 (문서3).  
- 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단 — 이러닝 운영, 교육콘텐츠·평가·예상인원 등 상세 기재 (문서4, 문서7, 문서8).  
- JST 공유대학(원) xAPI기반 LRS시스템 구축 / 발주기관: 전북대학교 — xAPI 기반 LRS(학습기록) 시스템 사업 명시 (문서6).  
- 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 / 발주기관: 전북특별자치도 정읍시 — 사업명에 '트레이닝센터' 포함(문서5).

제공된 문서 내에서는 위 항목들 외에 추가로 교육·학습 관련 발주사업은 확인할 수 없습니다.
```

Judge reason excerpt:

```text
답변은 여러 특정 발주사업(기관과 사업명)을 열거하고 있으나 제공된 '검색된 근거'는 조각난 문서 내용들과 일반적 ‘교육’ 관련 항목들(예: 교육지원, 교직 이수요건, 이러닝/어학 콘텐츠, xAPI 기반 시스템 등)을 포함할 뿐, 답변이 제시한 각 사업명과 발주기관을 명확히 뒷받침하지 않습니다. 일부 항목(xAPI, 교직 이수요건, 이러닝 관련 문구)은 근거에 존재하므로 전반적으로 교육 관련 사업이 있다는 응답 자체는 질문에 부합하나, 답변의 구체적 매칭과 ‘위 목록 외에는 없다’는 단정은 근거로 충분히 입증되지 않습니다.
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 91.21; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
요청하신 비교는 제공된 문서 내용만으로 정리합니다.

요약: 두 사업은 목적·범위·규모에서 차이가 큽니다. 아래 항목별로 각각의 근거 사업명(발주기관)을 함께 제시합니다.

- 사업명 / 발주기관
  - 고려대학교: 차세대 포털·학사 정보시스템 구축사업 (발주: 고려대학교)  
  - 광주과학기술원: 학사시스템 기능개선 사업 (발주: 광주과학기술원)

- 사업목적/목표
  - 고려대학교: 노후 시스템을 차세대화해 정보서비스 품질 강화 및 대학 교육시스템 경쟁력 확보 (고려대학교).  
  - 광주과학기술원: 학사조직 개편·학위 연계과정 도입에 따른 시스템 개선으로 업무 편리성·효율성 및 사용자 편의성 증대 (광주과학기술원).

- 사업범위 / 주요기능
  - 고려대학교: 통합로그인·통합/지능형 검색·마이페이지·공지/알림·일정관리·커뮤니티·게시판·사용자별 정보서비스·위젯·연계서비스(웹메일, 챗봇, 전자결재, 학사/행정 서비스) 등 포털 전반과 모바일(기존 앱 ‘호잇’ 하이브리드 재구축 포함) 및 학사·행정·연구시스템 연계 (고려대학교).  
  - 광주과학기술원: 학사조직 개편에 따른 시스템 개선, 학위연계과정(학석연계, 학석박통합 등) 관련 메뉴·학번 발급·프로세스 변경 및 관리자/사용자 메뉴 연동 등 기능 개선·구축 (광주과학기술원, FUR-005·FUR-006).

- 규모·예산
  - 고려대학교: 사업예산 11,270,000,000원(VAT 포함), 사업기간 계약일로부터 24개월, 무상유지보수 12개월 (고려대학교).  
  - 광주과학기술원: 사업비 157,300,000원(VAT 포함), 세부 견적: 설계·분석 53,000,000원(11M/M), 개발·테스트 90,000,000원 (광주과학기술원).

- 계약·입찰 방식 및 지급조건
  - 고려대학교: 제한경쟁입찰(협상에 의한 계약) (고려대학교).  
  - 광주과학기술원: 공개경쟁입찰(협상에 의한 계약체결), 선금 50% 지급·잔금은 최종검수 시 지급, 공동수급불가 (광주과학기술원).

- 추진일정·개발기간
  - 고려대학교: 계약일로부터 24개월 내 완료, 추진일정(분석·설계·개발·통합테스트·시범운영·오픈 등) 제시 (고려대학교).  
  - 광주과학기술원: 문서에 상세 총괄 일정 표시는 제공되지 않음 — 제공된 문서에서 확인할 수 없습니다 (광주과학기술원).

- 개발·기술요구 및 준수사항
  - 고려대학교: 모든 기존 기능 구현, 연계 변경 관리, 개발방법론·프로세스 제시 요구, 행정안전부 고시 지침 준수, 웹표준·웹접근성·시큐어코딩 적용 등 (고려대학교).  
  - 광주과학기술원: 요구사항(기능·성능) 상세화 및 제안·평가 관련 지침 포함(문서 색인 상), 그러나 세부한 개발프레임워크·보안·웹표준 준수 요구사항은 제공된 문서에서 확인할 수 없습니다 (광주과학기술원).

- 기대효과 / 목적 달
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 91.21; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 고려대학교 (사업명: 차세대 포털·학사 정보시스템 구축사업)  
  근거: 문서4. 응답시간 요구사항이 있음.  
  - 업무응답시간(PER-002): 모든 질의는 사용자가 요청한 시점부터 3초 이내에 결과 처리(포탈/학사 및 연계 레거시 시스템 포함). 단, 대량데이터(5,000건 이상), 대형이미지(≥500KB)·영상 포함 페이지와 동시사용자 용량의 90% 초과 시 예외 규정 있음.  
  - 웹페이지 디스플레이시간(PER-003): 웹페이지는 요청 후 3초 이내에 완전 출력(동일 예외사항 존재).

- 광주과학기술원 (사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업)  
  근거: 문서1, 문서7, 문서5 등.  
  - 제공된 문서들에서는 응답시간(업무응답시간·페이지 디스플레이시간 등)에 대한 요구사항을 명시하고 있지 않습니다. 즉, "제공된 문서에서 확인할 수 없습니다."
```

#### q9_imprecise_org - issue_or_audit_queue

- question: 원자력연구소에서 방사선량 평가하는 시스템 사업 요구사항 알려줘
- EDD: 91.21; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "한국원자력연구원 선량평가시스템 고도화" / 발주기관: 한국원자력연구원 (제공된 문서들)

핵심 요구사항 요약(문서별 근거 표기)

- 사업 개요: 계약기간 계약일로부터 6개월, 사업비 46,600천원, 제한경쟁·협상에 의한 계약 방식 (문서1).  
- 범위: 평가장기(Organ) 개선(포트란 모듈 및 웹시스템) 및 액체(유출물) 선량평가 기능 추가(포트란 모듈·웹시스템) (문서1, 문서5 SFR-003~004).  
- 액체 선량평가(기능 세부):  
  - 피폭경로: 외부피폭(예: 해변/수상활동), 내부피폭(수산물·음용수·관개작물 섭취 등) (문서5 SFR-003).  
  - UI 입력항목(웹): 핵종, 방출량, 재농축인자, 부지특성·사회환경인자(희석수량·희석인자, 섭취량·생산량·활동시간·수송기간 등) (문서5 SFR-004).  
  - DB: 생체축적인자, 선량환산인자, 부지특성·사회환경인자 (문서5 SFR-004).  
  - 출력: 피폭경로별 선량결과·기준치 비교, 개인선량 및 집단선량 산출 (문서5 SFR-003~004).  
- 평가성능: 사용자 건별 조회·선량평가 처리 응답을 화면에 3초 이내로 표시해야 함 (문서5 PER-001).  
- 테스트 요구사항:  
  - 단위/통합/인수 테스트 계획서 제출 및 연구원 승인 후 수행, 연관 메뉴군 단위 테스트, 인수시험 시 결함 보완·재검증 반복 요구(세부 절차·계획 포함) (문서2 TER-001~003).  
- 보안·원격개발: 원격지 개발에 따른 위험 식별 및 구체적 보안관리대책 제시, 제시 작업장이 비밀준수 요건 미충족 시 거부 가능(문서4).  
  - SER-001(보안 요구사항)의 상세 내용은 제공된 문서에서 확인할 수 없습니다 (문서2 SER-001).  
- 기술이전 및 교육: 자체 유지관리 가능토록 기술이전 계획 제출·이행, 관리자 교육 실시(교재 사전제출·자가학습 가능 구성) (문서3).  
- 하자보수·지원: 준공검사 완료일로부터 하자담보 기간 12개월, 장애 접수 후 24시간 이내 보수 가능하도록 유지관리 인력 확보 및 즉각 기술지원(문서3 PSR-002).  
- 산출물·보고: 소스(주석·문서 포함)·실행파일, 매뉴얼(사용자/운영자), 교육자료, 기술이전계획서, 하자보수계획서 등 제출; 착수/중간/완료 보고회 및 주간/월간 보고서 등(문서6 PMR-005 및 제출 목록).  
- 일정관리: 사업수행계획서에 WBS로 상세 일정·진도 수치화, 계획 대비 10% 이상 지연 시 비상조치 및 보고(문서6 PMR-005).  
- SW사업정보 및 지식재산: SW사업정보(SW사업 수행·실적) 데이터 제출 의무(spir.kr 준수), 일부 보안민감 산출물(예: 내부·외부 IP 현황, 상세 시스템 구성도 등)은 제공 제한(문서4 7.4~7.5).  

추가 세부사항 또는 미기
...(truncated; full text is in report_evidence.json)
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 91.21; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서들(근거: 문서1 2024년 BIFF & ACFM 온라인서비스 재개발 … 발주기관: (사)부산국제영화제; 문서2 [재공고]차세대 통합정보시스템(ERP) 구축 – 한국가스공사; 문서3·8 차세대 포털·학사 정보시스템 구축사업 – 고려대학교; 문서4 도시계획위원회 통합관리시스템 구축용역 – 인천광역시; 문서5 예약발매시스템 개량 ISMP 용역 – 한국철도공사; 문서6 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 – 인천광역시; 문서7 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 – 수협중앙회)에서는 우주 로켓 발사 시스템 구축 사업이 확인되지 않습니다. 제공된 문서에서 확인할 수 없습니다.
```

### lambda03_top8_filter_rewrite

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 93.08; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 2024년 이러닝시스템 운영 용역 (발주기관: 국민연금공단)

요구사항 요약(문서에 명시된 항목 기준)

- 교육운영(코드: FUR)
  - FUR-001: 국민연금공단 역량모델 기반의 TRM 제시
  - FUR-002: 교육운영 방법 제시
  - FUR-003: 교육 예상인원 제시
  - FUR-004~FUR-005: 외부콘텐츠 제시 기준 및 기타 요청사항

- 이러닝시스템 기능(코드: SFR)
  - SFR-001: 이러닝시스템 구축·관리 기본방향
  - SFR-002: 사이버(모바일) 연수원 구축
  - SFR-003: 학습 이벤트 운영
  - SFR-004: 큐레이션 서비스 운영
  - SFR-005: 소셜러닝 운영
  - SFR-006: 나의 학습노트 운영
  - SFR-007: 직무지식진단 운영
  - SFR-008: 역량진단 운영
  - 정보보안·개인정보보호: 관련 규정 준수 및 보안관리 방안 제시 (문서 명시)
  - 인수인계 시 공단 보유 프로그램 및 데이터 이전 방안 제시 (문서 명시)

- 콘텐츠 개발·관리(코드: DER)
  - DER-001~DER-003: 콘텐츠 개발 범위·요건·검사·검수 요구
  - 계약업체는 콘텐츠 개발 완료 최소 14일 전에 사업완료보고서 초안 공단에 제출(심의)할 것
  - 제출 산출물(예시): 차시별 원고·스토리보드(2부), 검토결과 조치내역서, 사업완료보고서, 운영자 지침서, 유지보수 계획서, 산출물 일체(소스 포함)를 외장HDD 제출 등(문서에 명시된 수량·형태 포함)

- 품질 요구사항(코드: QUR)
  - QUR-001: 교육콘텐츠 평가 및 품질관리 방안 제시

- 학사관리(코드: LMR)
  - LMR-001: 학습관리시스템(LMS) 제공
  - LMR-002: 학습참여 유인체계 제시

- 유지관리(코드: MAR)
  - MAR-001: 유지관리 범위 제시(문서에 코드만 명시)

- 프로젝트관리·대금결제(코드: PMR)
  - PMR-004(대금결제): 
    - 콘텐츠 개발: 검수완료 후 지급
    - 콘텐츠 및 P/G 유지보수·관리: 상·하반기 각 반기 말에 2차 지급
    - 교육운영: 월별 또는 분기별 지급
  - 보고서 제출주기: 착수보고(1회), 월간업무현황(월1회), 중간보고(분기별), 최종보고(1회)
  - 산출물 제출시기·수량은 문서에 명시된 대로 제출(검수 완료 시 바인더·CD·외장HDD 등)

- 인수·인계 및 자료파기(문서 명시)
  - 이전 업체는 공단 관련 자료를 지체없이 전수 파기하고 공단직원의 폐기 확인을 받아야 함
  - 인수·인계 완료는 원칙 30일 이내, 공단이 미흡하다고 판단하면 연장 가능
  - 인수·인계 계획 및 완료확인서를 서면 제출(양 당사자 확인 포함)

- 입찰·자격·계약방법(문서 명시)
  - 원격평생교육시설 인가 및 이러닝사업자(이러닝콘텐츠
...(truncated; full text is in report_evidence.json)
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 93.08; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=3, relevance=5
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: low_groundedness
- interpretation: LLM judge found a quality issue; inspect answer-evidence alignment, not only retrieval metrics.

Answer excerpt:

```text
근거: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단

핵심 요구사항(콘텐츠 개발·관리)
- 산출물 및 제공형식
  - 콘텐츠 원본 및 완성본을 인재개발부(1부)·해당부서(1부)에 제공. 콘텐츠를 교재로 활용할 수 있도록 PPT 등으로 다운로드 가능하게 구현. (문서2)

- 개발범위·수량·형태
  - 개발 차시 예시: 일반 콘텐츠 60차시, 부서별 필수교육 10차시 등(문서8).  
  - 동영상 콘텐츠는 차시당 30~40분 내외 기준(문서2).  
  - 실물 교재가 지급되는 항목(외부콘텐츠·전문자격증·북러닝·전화외국어 등)은 실물 제공 및 배송료 포함 가격 제시 요구(문서8).

- 콘텐츠 주제·유형
  - 직무교육, 가치체계 이해, 사회적 가치, 개인정보보호, 정보보안 등 공단 소유 콘텐츠 및 외부콘텐츠 연계(문서2, 문서3).

- 기술·플랫폼 관련 요구
  - 제공될 기능 예: 나의 학습노트, 역량진단 등(문서2).  
  - 기존 일부 구성요소 기술스택 표기: MS-SQL 2005, JAVA, JSP, ActiveX control, XML 등(문서2).

- 유지보수·업데이트 프로세스
  - 최신 법령·지침 등 반영을 위한 상시 업데이트 관리프로세스 운영.  
  - 주요 작업: 콘텐츠 유지보수(차시별 관리), 텍스트 수정, 차시 재구성 등, 스토리보드 활용으로 수정·보완 용이성 확보(문서2 MAR-002).

- 개발역량·장비·제작지원
  - 제안서에 보유기술·개발방법론, 장비·개발도구 보유현황 및 확보방안 제시 요구.  
  - 동영상 촬영·전자책 제작 등 제작 지원 방안 제시 요구(문서6).

- 운영연계·서비스 요구사항
  - 큐레이션·소셜러닝 운영방안, 나의 학습노트·직무지식·역량진단 운영방안, 관리자용 통계·보고서 추출 및 지원 방안, 학습자 독려·진도관리·수료율 제고 방안, 배너 디자인 지원 등 제시(문서6).

- 인수인계·저작권·보안
  - 각종 데이터 및 소스코드(게시자료 포함) 인수인계 방안 제시 요구(문서6).  
  - 제작된 콘텐츠·산출물의 지적재산권은 공단과 선정업체 공동소유. 제3자 권리침해 발생 시 사업자가 법규에 따르고 손해배상 비율은 상호협의(문서4).  
  - 개인정보보호·정보보안·기밀보안·재해복구 방안 제시 요구(문서6).

- 즉시시정·보고
  - 즉각 반영하여 시정하고 결과보고서를 서면으로 제출(문서2 상단 언급).

제공된 문서에서 확인할 수 없는 항목
- 콘텐츠 개발에 대한 세부 검수기준(검수절차·평가세부사항), 세부 납품 일정(마일스톤) 및 지급조건의 상세 항목 등은 제공된 문서에서 확인할 수 없습니다.
```

Judge reason excerpt:

```text
대부분의 항목(원본·완성본 제공, PPT 다운로드 가능, 동영상 차시 길이, 콘텐츠 유형, 기술스택 일부, 유지보수·업데이트 프로세스, 인수인계·저작권·보안 요구 등)은 제공된 제안요청서 문서 내용과 직접 일치하거나 명시적으로 뒷받침됩니다. 다만 답변에 포함된 일부 세부 수치(예: '일반 콘텐츠 60차시, 부서별 필수교육 10차시')와 문서 번호 표기(문서2/문서3/문서8 등)는 근거 텍스트에 명확히 보이지 않거나 출처 표기가 사실과 다를 수 있어 부분적 과대해석·추정이 섞여 있습니다.
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 93.08; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
예. 제공된 문서들 중 교육·학습 관련 내용이 확인되는 다른 발주사업은 다음과 같습니다(근거 표기).

- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 인천광역시  
  근거: [문서1] — PSR-001 교육지원(교육계획 수립·교육실시·교재·소요경비 등) 명시.

- 차세대 포털·학사 정보시스템 구축사업 / 고려대학교  
  근거: [문서3] — 학교현장실습 관리, 적/인성검사·응급처치·성인지교육 이수관리 등 교직·학생 교육 관련 기능 명시.

- 2024년 이러닝시스템 운영 용역 / 국민연금공단  
  근거: [문서4], [문서7], [문서8] — 이러닝 콘텐츠·전화외국어·전문자격증 과정·교육평가·예상교육인원 등 학습운영 상세 명시.

- JST 공유대학(원) xAPI기반 LRS시스템 구축 / 전북대학교  
  근거: [문서6] — xAPI 기반 LRS(학습기록 관리) 구축 사업명 명시.

참고: 정읍체육트레이닝센터 통합운영관리시스템 구축 용역(정읍시)의 문서에는 비밀유지계약서 양식에 '교육담당자/교육대상자' 표기가 있으나, 교육·학습 관련 구체적 내용은 제공된 문서에서 확인할 수 없습니다.
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 93.08; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
요구사항에 따라 제공된 문서 내용만으로 핵심 비교 요약합니다. 각 항목에 근거가 된 사업명(또는 발주기관)을 함께 표기합니다.

1) 사업 성격·범위  
- (고려대학교) 차세대 포털·학사 정보시스템 구축사업: 포털(통합로그인, 통합/지능형 검색, 마이페이지, 위젯, 통합·개인화 서비스 등), 모바일 앱(기존 호잇 하이브리드 재구축), 학사·행정·연구 시스템 연계, DW/BI 포함 등 포괄적 차세대 구축(문서1·3·6·7·8 근거).  
- (광주과학기술원) 학사시스템 기능개선 사업: 기존 학사시스템의 기능 개선 및 특정 기능(학석통합·학위연계과정, 대학원 과정변경 등) 개발에 초점(FUR-005, FUR-006 등, 문서4 근거).

2) 목표 사용자·대상범위  
- (고려대학교) 학생(졸업생 포함), 교직원, 연구원 등 대학 내부 구성원 전반 대상(문서1·5 근거).  
- (광주과학기술원) 관리자 및 사용자 메뉴 연동 등 기능 대상 언급은 있으나 전체 대상 범위 명시사항은 제공된 문서에서 확인할 수 없습니다 (문서4 근거).

3) 주요 기능·기술 요구 차이  
- (고려대학교) 통합로그인·SSO, 통합/지능형 검색(신분별 우선노출, 유사도/추천), 개인화 위젯, 연계서비스(웹메일·챗봇·전자결재 등), 모바일 하이브리드 앱, DW/ETL·BI포털·BI솔루션, 웹표준·웹접근성·시큐어코딩 및 행정안전부 지침 준수 요구(문서1·6·8 근거).  
- (광주과학기술원) 학위연계·과정변경 관련 구체적 기능요구(FUR-005·FUR-006) 및 성능요구 항목(PER-001 등) 존재하나 세부 기술·성능 명세는 제공된 문서에서 확인할 수 없습니다 (문서4·2 근거).

4) 기간·예산·계약방식  
- (고려대학교) 사업기간: 계약일로부터 24개월, 무상유지보수 12개월, 사업예산 11,270,000,000원(VAT 포함), 입찰·계약: 제한경쟁입찰(협상에 의한 계약)(문서3 근거).  
- (광주과학기술원) 제안서 문서(문서2)에 추진일정·입찰평가 항목이 있으나 전체 사업기간·예산·입찰방식 등의 구체값은 제공된 문서에서 확인할 수 없습니다.

5) 규모·복잡성 전망(문서에 근거한 비교)  
- (고려대학교) 포털·학사·DW·BI·모바일을 포함한 전반적 차세대 시스템 구축으로 범위·통합·연계 요구가 광범위하여 대규모 사업(문서1·6·8 근거).  
- (광주과학기술원) 특정 학사 기능 개선 및 과정 관련 모듈 개발 중심으로 범위가 상대적으로 제한적임(문서4 근거).

6) 기타(관리·준수사항)  
- (고려대학교) 기존 기능 유지 의무, 연계 변경관리, 개발방법론·프로세스 제시 요구, 행정안전부 고시 준수 등 명시(문서6 근거).  
- (광주과학기술원) 제안서 평가·입찰절차·지식재산권·원격개발 등 운영·계약 관련 항목들이 제안요청서에 포함되어 있음(문서2 목차·문서4
...(truncated; full text is in report_evidence.json)
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 93.08; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 인천광역시, 한국철도공사 (용역), 고려대학교, 수협중앙회
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서에서 확인할 수 없습니다.

근거: 문서1(2024년 BIFF & ACFM 온라인서비스 재개발… 발주기관: (사)부산국제영화제), 문서2([재공고]차세대 통합정보시스템(ERP) 구축 발주기관: 한국가스공사), 문서3/7(차세대 포털·학사 정보시스템 구축사업 발주기관: 고려대학교), 문서4(인천일자리플랫폼 정보시스템 구축 ISP 수립용역 발주기관: 인천광역시), 문서6(예약발매시스템 개량 ISMP 용역 발주기관: 한국철도공사), 문서8(수협중앙회 수산물사이버직매장 시스템 재구축 ISMP 발주기관: 수협중앙회) 등에서 우주 로켓 발사 시스템 구축 사업은 언급되어 있지 않습니다.
```

### lambda07_top8_filter_rewrite

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 80.0; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 2024년 이러닝시스템 운영 용역 제안요청서(사업명: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단)

요구사항(핵심 정리)
- 교육 운영 관련
  - FUR-001: 국민연금공단 역량 모델 기반의 TRM 제시
  - FUR-002: 교육운영 방법 제시
  - FUR-003: 교육 예상인원 제시
  - FUR-004~FUR-005: 외부콘텐츠 제시 기준 및 기타 요청사항

- 이러닝 시스템 운영 관련
  - SFR-001: 이러닝시스템 구축 및 관리 기본방향 제시
  - SFR-002: 사이버(모바일)연수원 구축
  - SFR-003: “학습 이벤트” 운영
  - SFR-004: “큐레이션 서비스” 운영
  - SFR-005: “소셜러닝” 운영
  - SFR-006: “나의 학습노트” 운영
  - SFR-007: “직무지식진단” 운영
  - SFR-008: “역량진단” 운영
  - LMR-001: 학습관리시스템(LMS) 제공
  - LMR-002: 학습참여 유인체계 제시

- 콘텐츠 개발·관리
  - DER-001: 콘텐츠 개발 범위
  - DER-002: 콘텐츠 개발 요건
  - DER-003: 콘텐츠 검사 및 검수
  - QUR-001: 교육콘텐츠 평가 및 품질관리 방안 제시
  - MAR-001 등: 유지관리(관리 범위) 제시

- 개인정보보호 및 정보보안
  - 정보보안·개인정보보호 규정 준수 및 보안 관리 방안 제출 요구(제안서에 제시)

- 인수·인계 및 자료관리
  - 인수·인계 계획·결과 및 완료확인서 서면 제출
  - 인수·인계 기간: 30일 이내 완료(발주기관 사유로 연장 가능)
  - 계약 종료 후 이전 업체는 공단 관련 자료 전수 파기 및 공단 직원의 폐기 완료 확인 필요
  - 인수인계 시 공단 보유 프로그램 및 데이터 이전 방안 제시

- 기타 운영·관리 요구
  - 시스템 현황(구성도·인프라)은 보안서약서 제출 후 담당자 입회하에 열람 가능
  - 정보보안·개인정보조치 포함한 종합 보안관리 방안 제시 요구

- 입찰 참가자격(관련 요구사항)
  - “원격평생교육시설” 인가 및 이러닝사업자(이러닝서비스업 또는 이러닝콘텐츠업) 신고 업체
  - 전자입찰서 제출 전까지 나라장터에 이러닝콘텐츠업(6527) 또는 이러닝서비스업(6529)으로 등록

참고: 상기 항목은 국민연금공단의 2024년 이러닝시스템 운영 용역 제안요청서에 명시된 요구사항을 요약한 것입니다.
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 80.0; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 국민연금공단, 사업명 "2024년 이러닝시스템 운영 용역" 제안요청서(제공 문서)

요약 — 콘텐츠 개발·관리 요구사항(핵심)
1. 개발 범위(근거: DER-001, 문서6)
 - 신규 차시 개발: 60차시(협의 후 진행)  
 - 부서별 필수교육 콘텐츠: 10차시(협의 후 진행)  
 - 공단 소유 콘텐츠 관리: 146개 과정(계약 후 즉시 서비스)  
 - 영상 스크립트 기능 추가 등 기능적 개선 포함  
 - 시스템 변경에 따른 콘텐츠 변환·연동 및 오탈자·내용 수정 대응 요구

2. 개발 요건 및 방법론(근거: DER-002, 문서7, 문서8)
 - 제안서에 보유기술 및 개발방법론 기술 제시 요구  
 - 콘텐츠 개발을 위한 장비/개발도구 보유현황 및 확보방안 제시  
 - 동영상 촬영·전자책(e-book) 제작 등 지원 방안 제시  
 - 공단의 콘텐츠 개발요청사항에 대한 분석 내용 기술  
 - 선정업체는 과업별 책임자 지정 및 인력변경 시 사전보고

3. 검사·검수(근거: DER-003, 문서3)
 - 최종 검수 이후 하자보수 적용(세부 검수절차·기준은 제안서에 제시되어야 함)  
 - 사업완료 보고서 초안은 콘텐츠 개발 완료 최소 14일 전에 제출하여 심의

4. 유지관리·하자보수(근거: MAR-001, 문서3, 문서6)
 - 개발물에 대한 무상하자보수: “개발범위의 20% 범위 내”에서 최소 1년 지원  
 - 계약기간 종료 후 하자보수 범위 및 추진체계 제시 필요  
 - 이러닝시스템 관련 기술정보 제공 및 기술자문을 공단에 무상 지원해야 함

5. 인수·인계 및 소유권·보안 관련(근거: 문서6, 문서7, 문서8)
 - 공단 기존 보유 콘텐츠·프로그램·데이터 이전 방안 제출(계약 후 즉시 서비스)  
 - 각종 데이터 및 소스코드(게시자료 포함) 인수인계 방안 제시  
 - 저작권 보호방안, 기밀보안 체계, 개인정보보호·정보보안 준수 방안 제시 의무  
 - 소유권자 동의 없이 제3자 자료 제공 금지; 권리의무 양도 금지(하도급은 공단 승인 후 가능)

6. 품질관리·보고(근거: QUR-001, PMR-003, 문서3, 문서7)
 - 교육콘텐츠 평가 및 품질관리 방안 제시 필요  
 - 매월 과업수행 실적 및 익월 추진계획 보고(서면), 수시보고·회의 응해야 함  
 - 교육결과·통계·수료설문 등 보고 지원 방안 제시

참고·한계
 - 제안요청서에서 확인된 항목들을 정리했으며, 세부 검수기준(정량적 수치), 상세 개발 산출물 템플릿, 구체적 마일스톤 일정·SLA 및 비용 분류 등의 상세 항목은 제공된 문서에서 확인할 수 없습니다.
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 80.0; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=1, relevance=3
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 전북특별자치도 정읍시, 국민연금공단, 국민연금공단, 전북대학교, 울산광역시
- flags: low_groundedness, low_relevance
- interpretation: LLM judge found a quality issue; inspect answer-evidence alignment, not only retrieval metrics.

Answer excerpt:

```text
예 있습니다. 제공된 문서에 근거한 교육/학습 관련 사업(사업명 / 발주기관):

- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 인천광역시 (교육자료·교육지원 PSR-001, 교육계획서 요구)  
- 차세대 포털·학사 정보시스템 구축사업 / 고려대학교 (교직·학교현장실습 및 이수요건 관리 기능 명시)  
- 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 / 전북특별자치도 정읍시 (체육트레이닝센터, 교육담당자·교육대상자 등 기재)  
- 2024년 이러닝시스템 운영 용역 / 국민연금공단 (이러닝 콘텐츠·평가·교육예상인원 등 상세 요구)  
- JST 공유대학(원) xAPI기반 LRS시스템 구축 / 전북대학교 (LRS 구축 사업명 명시)  
- 2024년 버스정보시스템 확대 구축 및 기능개선 용역 / 울산광역시 (PSR-003 교육 계획 요구)

참고 문서 외에 다른 기관의 교육·학습 관련 발주 여부는 제공된 문서에서 확인할 수 없습니다.
```

Judge reason excerpt:

```text
제공된 근거 문서에는 ‘교육지원(PSR-001)’, ‘교육계획서’, ‘교직 이수요건 관리’, ‘정읍시청’ 등 교육 관련 조항과 요구사항이 명시되어 있어 일반적인 교육·학습 사업의 존재는 뒷받침됩니다. 그러나 답변에 열거된 개별 사업명(예: 인천일자리플랫폼 ISP, 차세대 포털·학사 정보시스템(고려대), 국민연금공단 이러닝, JST LRS 등)과 발주기관별 명시는 검색된 근거에서 직접 확인되지 않으며 상당수는 근거 없이 특정 사업명을 부여한 것으로 보입니다. 따라서 답변의 핵심 주장(교육 관련 사업 존재)은 어느 정도 관련성이 있으나 대부분의 상세 항목은 근거 부족(제작·추가 정보의 조작)으로 평가됩니다.
```

#### q5_followup - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 80.0; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 발주기관: 기초과학연구원

문서 근거로 확인되는 모니터링 업무 요청사항(핵심):
- 가동기간 동안 24시간 모니터링 수행(2인1조 기본, 주간엔 감독자 1인 이상 상주) — 문서8(3.3, 3.3.1).  
- 모니터링은 연구원에 구축된 제어시스템 또는 현장 장치를 활용하여 수행 — 문서8(3.3.1).  
- 모니터링 업무 항목(표4): 알람 메시지 확인, 주요 센서 트렌드 확인(온도·압력·유량·속도 등), 정상 운전 지시값 파악, 비정상 상황 감지, 제어로직 정상 작동 여부 확인, 현장 상황 일시/지속 관찰(주기적 순찰 포함) 등 — 문서2(표4), 문서7.  
- 주요 수치의 기록은 전자파일로 하며, 기록 대상 항목 및 기록 간격은 연구원이 정함(운영 상황에 따라 증감 가능) — 문서2.  
- 연구원 요청 시 계약자는 주요 수치에 대한 분석을 수행해야 하며(분석 대상·방법·결과물 형태는 연구원이 정함) — 문서2.  
- 기록·분석을 위해 필요한 노트북 및 일부 컴퓨터 악세서리는 계약자가 준비해야 함(다만 제어시스템 사용을 위한 컴퓨터·모니터·키보드·마우스·책상·의자는 연구원이 제공함) — 문서2, 문서8.  
- 연구원이 현장 확인을 요청하는 경우 지정된 값 관찰·확인 및 상황 전달(무전 통신 활용, 무전기는 연구원 제공) — 문서2(표4).  
- 계약자는 제어시스템 기본 사용 교육을 받으며, 이를 이해할 배경지식을 보유해야 함 — 문서8(3.3.1).

문서에 명시되지 않은 사항(예: 모니터링에 AI·머신러닝 예측 적용 요구 등)은 제공된 문서에서 확인할 수 없습니다.
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 80.0; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
요청하신 비교는 제공된 문서 내용만을 근거로 작성합니다.

1) 사업 목적·목표
- 고려대학교 차세대 포털·학사 정보시스템 구축사업(고려대): 노후화된 시스템을 차세대로 구축해 정보서비스 품질 강화 및 대학 교육시스템 경쟁력 확보. (문서1/문서6)
- 광주과학기술원 학사시스템 기능개선 사업(GIST): 학사조직 개편·학위 연계과정 신설에 따른 시스템 기능 개선으로 업무 편의성·효율성 및 사용자 편의성 증대. (문서5)

2) 사업 범위·주요 기능
- 고려대: 포털(통합로그인·통합/지능형 검색·마이페이지·위젯·공지·커뮤니티 등), 개인화·SSO·간편인증·2차인증, 모바일 포털 앱(기존 '호잇' 하이브리드 재구축), 학사/행정/연구 시스템 연계, 통합데이터 저장소(DW)·BI 포털·BI 솔루션 등 광범위한 응용SW 및 데이터/분석 기능 포함. (문서1/문서7/문서8)
- GIST: 학사 조직개편에 따른 시스템 개선 및 학위연계과정 시스템 구축 등 학사기능 개선에 초점. 상세 요구사항·기능은 제안요청서에 있음(세부항목 존재). (문서5/문서2 목차)

3) 예산·규모
- 고려대: 사업예산 11,270,000,000원(VAT 포함), 계약일로부터 24개월 내 수행, 무상유지보수 12개월. (문서3)
- GIST: 사업비 157,300,000원(VAT 포함). (문서5)
(비교 근거: 문서3, 문서5)

4) 계약·지급 방식
- 고려대: 제한경쟁입찰(협상에 의한 계약). 지급은 3년 분할(2024~2026학년도 비율 명시). (문서3)
- GIST: 공개경쟁입찰(협상에 의한 계약체결), 선금 50% 지급, 잔금은 최종검수 후 지급, 공동수급 불가. (문서5)

5) 기술·운영 요구사항 및 조건
- 고려대: 역할기반 권한관리(RBAC), 통합아이디 체계(개인별 복수신분 통합) 운영 방안 및 재생성 처리, 우회인증 방지, 대학 정보화 인력과의 협업·기술이전 제시, 다양한 IT환경에서 구동 가능성, 저작권 문제 책임 등 상세한 아키텍처·보안·연계·기술이전 요구. (문서4)
- GIST: 사업목표·범위·산출(업무분석자·개발자 인건비 명시)·제안요청 및 평가절차 등 제반 입찰 문서 구성(세부 요구사항·평가기준 포함). 구체 기술요구(예: 인증, DW 등)는 제공문서에서 요약만 확인됨. (문서2/문서5)

6) 기대효과·성과
- 고려대: 정보서비스 품질 향상, 대학 교육시스템 경쟁력 확보, DW·BI를 통한 통계·분석 제공 등. (문서1/문서8)
- GIST: 업무 편리성 제고, 업무효율성 극대화, 사용자 편의성 증대, 안정적 시스템 운영. (문서5)

7) 공개된 세부기술 스택(참고)
- 고려대: 기존 시스템들에 Java/Spring 계열, 통합검색(Search Formula-1), 통합인증(SafeIdentity), 모바일(Spring boot, Kotlin, Swift) 등
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 80.0; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 광주과학기술원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 고려대학교(사업명: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교)  
  근거: 문서5  
  응답시간 요구사항 있음 — 온라인 업무응답시간(PER-002) 및 웹페이지 디스플레이시간(PER-003)을 사용자 요청 시 3초 이내로 처리하도록 규정함. 단, 대량데이터(기준 5,000건 이상)·대형이미지(기준 500KB 이상) 포함 페이지 또는 동시사용자 용량의 90% 초과 시 예외로 함.

- 광주과학기술원(사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업 / 발주기관: 광주과학기술원)  
  근거: 문서1, 문서7, 문서8(및 첨부 서식)  
  응답시간 요구사항에 관한 규정은 제공된 문서에서 확인할 수 없습니다.
```

#### q9_imprecise_org - issue_or_audit_queue

- question: 원자력연구소에서 방사선량 평가하는 시스템 사업 요구사항 알려줘
- EDD: 80.0; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원, 한국원자력연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 한국원자력연구원 선량평가시스템 고도화
발주기관: 한국원자력연구원

요구사항(핵심만 요약, 제공된 문서 근거)

1) 기능 요구사항
- 평가장기(Organ) 개선: 포트란 모듈 및 웹시스템 평가장기 개선(문서1, 문서2).
- 액체(방출수) 선량평가 추가:
  - 포트란 모듈 액체 선량평가 추가(개인·집단선량 포함) — 외부피폭(해변·수상활동 등), 내부피폭(수산물·음용수·관개작물 섭취 등)(SFR-003, 문서6).
  - 웹시스템 액체 선량평가 UI 및 DB 구축: 선원항(핵종, 방출량, 재농축인자), 부지특성·사회환경인자(희석수량·희석인자, 섭취량·생산량·활동시간·수송기간 등), 피폭경로별 선량결과 및 기준치 비교 출력, DB 항목(생체축적인자, 선량환산인자, 부지·사회환경인자)(SFR-004, 문서6).

2) 성능 요구사항
- 조회 및 선량평가 질의응답 시간: 사용자 건별 질의 처리 결과를 3초 이내 화면에 표시(PER-001, 문서6).

3) 인터페이스·데이터 요구사항
- 웹 접근성 및 UI 구현 요구(문서2).
- 초기자료 구축·데이터 변환 및 보안 요구: DB 구축 대상·방법·보안사항 포함(문서2, SFR-004).

4) 테스트·품질·보안 요구사항
- 테스트: 단위테스트, 통합테스트 및 인수시험 등(문서3, 문서2).
- 품질: 변경사항 관리, 정기점검 및 장애지원(문서2).
- 보안: 국가 정보보안 지침(용역사업 보안관리), 개인정보보호법 준수 및 외주 용역사업 보안특약 적용(문서7, 문서2).

5) 프로젝트 관리·제약사항·인수·인계
- 사업기간: 계약일로부터 6개월(문서1, 문서3, 문서7).
- 사업비: 46,600천원(부가세 포함)(문서1).
- 계약·입찰: 제한경쟁입찰(중소기업간), 협상에 의한 계약, 기술평가 90%·가격평가 10%(문서1, 문서5).
- 개발원칙: 모듈화하여 기능성·신뢰성·효율성·재사용성·유지보수성 보장(문서2, 문서3).
- 제안서에 포함해야 할 항목: 설계/구현방안, 추진전략·계획, 문제점·위험요인 및 대응방안, 필요 시 기존시스템 이전·환경설정·최적화·DB구축·필수 SW 제안(문서4, 문서2, 문서3).
- 일정관리·보고: WBS 기반 세부 일정, 계획 대비 10% 이상 지연 시 비상조치·진도보고, 착수·중간·완료 보고회(문서4).
- 인도물·기술이전: 소스(주석·문서 포함) 및 실행파일, 매뉴얼(사용자/운영자), 교육계획·결과, 기술이전계획서, 하자보수계획서, 보안확약서 등 제출(문서4, 문서5).
- 기술지원: 기술이전 및 사업종료 시까지 조직 구성해 기술지원 수행, 개발 후 습득 노하우 지속 제공, 필요시 시스템 보완·확장 지원(문서5).
- 유지보수: 개발 후 무상 유지보수 1년 언급(문서7).

6) 추가/제안 요구
- 제안자가 필요하다고 판단되는 추가 제안(단, 연관성 적은 제안 지양)(PS
...(truncated; full text is in report_evidence.json)
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 80.0; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 한국철도공사 (용역), 인천광역시, 인천광역시, 수협중앙회, 고려대학교
- flags: missed_abstention, missing_llm_judge_score
- interpretation: The system answered a question expected to abstain; inspect retrieval distractors and no-evidence policy.

Answer excerpt:

```text
아닙니다. 제공된 문서들(문서1: "2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역" / 발주기관: (사)부산국제영화제, 문서2: "[재공고]차세대 통합정보시스템(ERP) 구축" / 발주기관: 한국가스공사, 문서3: "차세대 포털·학사 정보시스템 구축사업" / 발주기관: 고려대학교, 문서4: "예약발매시스템 개량 ISMP 용역" / 발주기관: 한국철도공사, 문서5: "인천일자리플랫폼 정보시스템 구축 ISP 수립용역" / 발주기관: 인천광역시, 문서6: "도시계획위원회 통합관리시스템 구축용역" / 발주기관: 인천광역시, 문서7: "수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고" / 발주기관: 수협중앙회, 문서8: "차세대 포털·학사 정보시스템 구축사업" / 발주기관: 고려대학교)에는 우주 로켓 발사 시스템 구축 사업이 없습니다. 제공된 문서에서 확인할 수 없습니다.
```

### topk8_filter_rewrite_control

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 91.03; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 사업명 "2024년 이러닝시스템 운영 용역" / 발주기관: 국민연금공단

요구사항 요약(핵심만)

1) 교육운영 관련 (문서6)
- 국민연금공단 역량모델 기반 TRM 제시(FUR-001)
- 교육운영 방법 제시(FUR-002)
- 교육 예상인원 제시(FUR-003)
- 외부콘텐츠 제시 기준 및 기타 요청사항(FUR-004, FUR-005)
- 교육콘텐츠 평가·품질관리 방안(QUR-001)

2) 이러닝시스템(운영) 기능 요구사항 (문서6)
- 이러닝시스템 구축·관리 기본방향(SFR-001)
- 사이버(모바일) 연수원 구축(SFR-002)
- 학습 이벤트 운영(SFR-003)
- 큐레이션 서비스 운영(SFR-004)
- 소셜러닝 운영(SFR-005)
- 나의 학습노트 운영(SFR-006)
- 직무지식진단 운영(SFR-007)
- 역량진단 운영(SFR-008)
- 학습관리시스템 제공 및 학사관리(학습참여 유인체계)(LMR-001, LMR-002)

3) 콘텐츠 개발·관리 (문서6, 문서4)
- 콘텐츠 개발 범위·요건 및 검수(DER-001~DER-003)
- 차시별 원고·스토리보드 제출 및 검토(비고: 공단 요구시 검토분, 검수 완료 시 최종본 제출) (문서4)
- 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출(문서4)
- 산출물(원본·소스·스토리보드 등) 제출 및 형식(바인더·CD·외장HDD 등) 명시(문서4)

4) 유지·관리 및 운영 범위 (문서6, 문서4)
- 콘텐츠 및 P/G 유지보수·관리: 지급 및 관리 방식(대금결제 관련) (PMR-004, 문서4)
- 유지보수 계획서 등 산출물 제출(문서4)

5) 개인정보보호·정보보안·인수인계 (문서6, 문서8)
- 정보보안·개인정보보호 규정 준수 및 보안 관리 방안 제시 요구(문서6)
- 인수인계 시 공단 보유 프로그램·데이터 이전 방안 제시(문서6)
- 계약 종료 후 이전 업체는 공단 관련 자료 전수 파기 및 공단 직원의 폐기 확인 필요(문서8)
- 인수·인계 계획·결과 및 완료확인서 서면 제출, 인수·인계는 원칙 30일 이내 완료(문서8). 공단이 미흡 판단 시 기간 연장 가능(문서8)

6) 프로젝트관리·보고·대금결제 (문서4)
- 보고서 제출 주기: 착수(1회), 월간업무현황(월1회), 중간(분기1회), 최종(1회) 등(문서4)
- 비정기 산출물 목록 및 제출 수량/형식(문서4)
- 대금결제: 콘텐츠 개발은 검수완료 후 지급, 콘텐츠·P/G 유지보수는 상/하반기 지급, 교육운영은 월별 또는 분기별 지급(문서4, PMR-004)

7) 입찰참가자격·계약방법(문서8)
- 원격평생교육시설 인가 및 이러닝사업자(이러닝서비스업 또는 이러닝콘텐츠업) 신고 필요
- 나라장터에 입찰참가자격 등록(이러닝콘텐츠업 6527 또는 이러닝서비스업 6529) 필수
- 입찰방법: 일반경쟁입찰, 계약방법: 협상에 의
...(truncated; full text is in report_evidence.json)
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 91.03; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서에서 확인되는 교육/학습 관련 타 발주 사업은 다음과 같습니다(근거: 각 사업명/발주기관 표기).

- 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 / 인천광역시 — 교육지원(교육계획서, 교육훈련계획 등) 요구사항 포함.  
- 차세대 포털·학사 정보시스템 구축사업 / 고려대학교 — 교직·학생 실습관리, 이수요건 등 교육·학사 관련 기능 포함.  
- 2024년 이러닝시스템 운영 용역 / 국민연금공단 — 이러닝 운영, 과정·교재·평가·예상인원 등 교육 운영 요구사항 포함.  
- JST 공유대학(원) xAPI기반 LRS시스템 구축 / 전북대학교 — xAPI 기반 LRS(학습기록 저장·관리) 구축 사업임.  
- 정읍체육트레이닝센터 통합운영관리시스템 구축 용역 / 전북특별자치도 정읍시 — 문서에 교육담당자·교육대상자 서명란 및 비밀유지계약서 등 교육 관련 항목 확인.

문서에 근거한 항목만 명시하였으며, 추가 사업은 제공된 문서들에서는 확인할 수 없습니다.
```

#### q5_followup - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 91.03; coverage: 0.0; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 재단법인 광주광역시 광주문화재단, 한국가스공사, 한국건강가정진흥원, 파주도시관광공사, 수협중앙회, 을지대학교, (사）한국대학스포츠협의회, (사)부산국제영화제
- flags: coverage_below_target, missing_llm_judge_score
- interpretation: Retrieval did not cover all target organizations; inspect filtering, rewrite, and MMR diversity.

Answer excerpt:

```text
요청하신 모니터링 업무 관련 요구사항 검색 결과(근거 문서·발주기관 표기):

모니터링 요구사항이 명시된 문서
- 사업명: 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 / 발주기관: (사)부산국제영화제 (문서8)
  - 내용: “인적자원 활용한 모니터링”, “상시 모니터링 및 장애예방, 장애처리 활동”, “정기 예방점검(월 1회) 실시”, “장애접수 후 4시간 이내 보수 가능하도록 대응 조치” 등 명시(MAR-003, MAR-004).
- 사업명: 2025년 아이돌봄인력 인적성 검사 정보시스템 운영 / 발주기관: 한국건강가정진흥원 (문서3)
  - 내용: “정기점검 및 수시점검 실시”, “정기 점검 후 점검결과 보고서 제출”, “장애 발생 시 로그 수집 및 이력 관리”, “장애 신고 접수 시각으로부터 2시간 이내 착수(업무시간 외 장애처리시간 등 세부시간 규정)” 등 명시(MAR-005 등).
- 사업명: 종량제봉투 판매관리 전산시스템 개선사업 / 발주기관: 파주도시관광공사 (문서4)
  - 내용: “시스템 모니터링” 명시 및 성능·응답시간 요구사항(오류응답·느린작업 처리, 동시 접속수 기준) 포함(PER-003, SIR-001 관련).
- 사업명: KUSF 체육특기자 경기기록 관리시스템 개발 / 발주기관: (사)한국대학스포츠협의회 (문서7)
  - 내용: 시스템 관리자 매뉴얼에 “로그 및 백업 관리 등 모두 포함 필요” 등 운영·관리(로그 관리) 항목 명시 — 모니터링·운영 관련 산출물 요구.

모니터링 요구사항이 문서에서 확인되지 않는(또는 명시적 표현 없음) 문서
- 사업명: 2024년 광주문화예술통합플랫폼 시스템 유지 및 보수 / 발주기관: 재단법인 광주광역시 광주문화재단 (문서1)
  - 제공된 문서에서 “모니터링”이라는 명시적 요구사항은 확인할 수 없습니다.
- 사업명: [재공고]차세대 통합정보시스템(ERP) 구축 / 발주기관: 한국가스공사 (문서2)
  - 제공된 문서에서 “모니터링”이라는 명시적 요구사항은 확인할 수 없습니다.
- 사업명: 수산물사이버직매장 시스템 재구축 ISMP 수립 입찰 공고 / 발주기관: 수협중앙회 (문서5)
  - 제공된 문서에서 “모니터링”이라는 명시적 요구사항은 확인할 수 없습니다.
- 사업명: 을지대학교 비교과시스템 개발 / 발주기관: 을지대학교 (문서6)
  - 제공된 문서에서 “모니터링”이라는 명시적 요구사항은 확인할 수 없습니다.

필요하면 각 문서의 관련 문구(원문 발췌)까지 제공해드리겠습니다.
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 91.03; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
아래 비교는 제공된 문서 내용만을 근거로 작성했습니다.

1) 사업 목적/범위
- 고려대학교(차세대 포털·학사 정보시스템 구축사업): 노후 시스템을 차세대로 재구축하여 정보서비스 품질 강화 및 대학 교육시스템 경쟁력 확보. 포털(통합로그인·지능형검색·마이페이지·커뮤니티·위젯·연계서비스 등)과 학사행정 통합 개발, 모바일 앱(기존 호잇 하이브리드 재구축) 포함. (문서1, 문서5, 문서8)
- 광주과학기술원(학사시스템 기능개선 사업): GIST 학사조직 개편·학위 연계과정(학석연계·학석박·석사→석박통합 등) 도입에 따른 학사 시스템의 기능 개선 및 프로세스 변경·구축에 집중. (문서4, 문서7)

2) 개발 범위·구체기능
- 고려대학교: 포털 전반(검색 개인화, SSO, 간편·2차인증, 위젯 개인화), 학사·행정·연구시스템 연계, 모바일 포털(앱·웹·푸시) 등 광범위한 응용SW 개발. (문서1)
- 광주과학기술원: 학위연계과정·대학원 과정변경 관련 메뉴(학번 신규발급 등), 관리자·사용자 메뉴 연동 및 관련 프로세스 변경 등 특정 기능 개선. (문서4)

3) 사업비·규모
- 고려대학교: 총 예산 11,270,000,000원(VAT 포함), 3년 분할지급(2024 약30%, 2025 약40%, 2026 약30%). (문서3)
- 광주과학기술원: 총 사업비 157,300,000원(VAT 포함). 설계·분석 53,000,000원(총 11 M/M), 개발·테스트 90,000,000원 등 상세 견적 포함. (문서7)

4) 기간·유지보수
- 고려대학교: 계약일로부터 24개월 이내, 무상유지보수 12개월. (문서3)
- 광주과학기술원: 사업 기간(총 기간)은 제공된 문서에서 확인할 수 없습니다. (문서2/문서7)

5) 계약·입찰 방식 및 참여 제한
- 고려대학교: 제한 경쟁 입찰(협상에 의한 계약), 주사업자 일괄제안 요구. (문서3, 문서6)
- 광주과학기술원: 공개경쟁입찰(협상에 의한 계약체결), 공동수급불가(공동수급 제한). (문서7)

6) 결제·지급 조건
- 고려대학교: 연도별 분할지급 비율만 제시(위 3년 분할). (문서3)
- 광주과학기술원: 선금 50% 지급, 잔금은 최종검수 완료 시 지급. (문서7)

7) 품질·준수 기준 등
- 고려대학교: 행정안전부 고시(정보시스템 구축·운영 지침), 전자정부 웹사이트 품질관리 지침 준수, 시큐어코딩·웹표준·접근성 적용 등 요구. (문서6)
- 광주과학기술원: 구체적 외부 규격 준수 항목은 제공된 문서에서 확인할 수 없습니다. (문서2/문서4/문서7)

8) 대상 규모 및 환경
- 고려대학교: 서울·세종 캠퍼스 인력·학생 수 등 대규모 사용자 환경(예: 서울캠퍼스 학부 20,373명·대학원 9,947명 등) 명시. (문서5)
- 광주과학기술원: 대상 인원 규모(사용자 수 등)는 제공된 문서에서 확인할 수 없습니다. (
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 91.03; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
고려대학교(차세대 포털·학사 정보시스템 구축사업): 있음 — 성능요구 PER-002에 따라 모든 질의의 업무응답시간을 사용자가 요청한 시점부터 3초 이내로 처리해야 하며(PER-003: 웹페이지 디스플레이시간도 3초 이내), 단 대량데이터(기준 5,000건 이상), 대형이미지(≥500KB) 또는 동시사용자 용량의 90% 초과 시 예외가 적용됨. (근거: 사업명: 차세대 포털·학사 정보시스템 구축사업 / 발주기관: 고려대학교, 문서4)

광주과학기술원(실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업): 제공된 문서들에서는 응답시간(업무응답시간/웹페이지 표시시간)에 대한 요구사항을 확인할 수 없습니다. (근거: 사업명: RCMS 연계 모듈 변경 사업 / 발주기관: 광주과학기술원, 문서7 등)
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 91.03; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서들(예: 문서1 사업명: "2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역" / 발주기관: (사)부산국제영화제; 문서2: "[재공고]차세대 통합정보시스템(ERP) 구축" / 발주기관: 한국가스공사; 문서3·8: "차세대 포털·학사 정보시스템 구축사업" / 발주기관: 고려대학교; 문서4: "도시계획위원회 통합관리시스템 구축용역" / 발주기관: 인천광역시; 문서5: "예약발매시스템 개량 ISMP 용역" / 발주기관: 한국철도공사; 문서6: "인천일자리플랫폼 정보시스템 구축 ISP 수립용역" / 발주기관: 인천광역시; 문서7: "수산물사이버직매장 시스템 재구축 ISMP" / 발주기관: 수협중앙회)에서는 우주 로켓 발사 시스템 구축 사업이 없습니다. 제공된 문서에서 확인할 수 없습니다.
```

### topk12_filter_rewrite

#### q1_single_extract - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘.
- EDD: 93.52; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
근거: 2024년 이러닝시스템 운영 용역 / 국민연금공단

요약(핵심 요구사항)
1. 사업기간·예산
 - 계약체결일~2025.2월, 총예산 773,801천원(교육운영 부문 620,801천원, 콘텐츠개발·시스템·서버 등 153,000천원). 가격제안 시 각 부문별 예산 초과 불가. (근거: 사업개요)

2. 사업목적
 - 온택트 교육수요 충족, 직급별 역량진단 및 맞춤교육, 직무·부서별 콘텐츠 개발, 상시 학습 활성화. (근거: 사업개요)

3. 사업범위
 - 직무 콘텐츠 개발·운영, 외부(위탁)콘텐츠 운영, 사이버(모바일)연수원 구축·운영 및 LMS·서버 임대, 공단 콘텐츠·프로그램 수정·보완, 정보보안·개인정보보호 및 법령 준수 포함. (근거: 사업범위)

4. 주요 기능(요구사항 코드)
 - 역량모델 기반 TRM 제시(FUR-001). (근거)
 - 교육운영 방법, 교육예상인원, 외부콘텐츠 제시 기준·기타(FUR-002~FUR-005). (근거)
 - 교육콘텐츠 품질관리 방안 제시(QUR-001). (근거)
 - 이러닝시스템 기본방향 및 사이버(모바일)연수원 구축(SFR-001~SFR-002). (근거)
 - 학습 이벤트, 큐레이션, 소셜러닝, 나의 학습노트, 직무지식진단, 역량진단 등 서비스 운영(SFR-003~SFR-008). (근거)
 - LMS 제공 및 학사관리(학습유인체계 포함)(LMR-001~LMR-002). (근거)
 - 콘텐츠 개발 범위·요건·검사·검수(개발 요구사항 DER-001~DER-003). (근거)
 - 유지관리 범위(MAR-001). (근거)
(모두 근거: 요구사항 구성 표)

5. 산출물·보고서 제출 및 형식
 - 콘텐츠 개발 완료 최소 14일 전 사업완료보고서 초안 제출하여 심의. (근거)
 - 정기보고서: 착수보고서(1회), 월간업무현황(월1), 분기중간보고(분기1), 최종보고서(1회). (근거)
 - 비정기 산출물: 차시별 원고·스토리보드(2부, 바인더·CD), 검토결과 조치내역서(바인더), 사업완료보고서·운영자지침서·유지보수계획서(각 2부, 바인더·CD), 산출물 일체(소스·스토리보드 등) 1부 외장HDD 제출. (근거)

6. 대금결제
 - 콘텐츠 개발: 검수완료 후 지급. 유지보수·관리: 상·하반기 2회(각 반기 말) 지급. 교육운영: 월별 또는 분기별 지급. (근거: PMR-004)

7. 인수·인계 및 자료파기
 - 인수·인계는 인수자·인계자 간 계획·결과·완료확인서 작성·제출. 인수·인계 완료기한 30일 이내(공단이 미흡 판단 시 연장 가능). 이전 업체는 보유한 공단 관련 자료를 지체없이 전수 파기하고 공단 직원의 폐기 완료 확인을 받아야 함. (근거)

8. 정보보안·개인정보보호
 - 정보보안, 개인정보보호 규정 준수 및 보안 관리 방안 제시 요구. 인수인계 시 공단 보유 프로그램 및 데이터 이전 방안 제시. (
...(truncated; full text is in report_evidence.json)
```

#### q2_followup - issue_or_audit_queue

- question: 국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘. / 콘텐츠 개발 관리 요구 사항에 대해서 더 자세히 알려 줘.
- EDD: 93.52; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단, 국민연금공단
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 2024년 이러닝시스템 운영 용역 / 발주기관: 국민연금공단

요약 — 콘텐츠 개발·관리 관련 요구사항(근거 문서 표기)

1. 개발 범위 및 산출물
- 직무교육·부서별 필수교육 등 공단 교육과정 개발(직무교육 대상 연간 인원 표기 등) — 근거: 문서4, 문서12  
- 개발 산출물 예시(차시 수 등): 차시 60, 부서별 필수교육 차시 10, 직무교육 대상 11,000명 등 표기 — 근거: 문서12  
- 공단에 원본(소스)·완성본 및 교재(PPT 등) 제공, 다운로드 기능 구현 요구(인재개발부 1부·해당부서 1부 제공) — 근거: 문서11

2. 개발 요건(콘텐츠 특성 및 기술)
- 모바일·PC 동시수강 가능, 마이크로러닝·e-book, AI·빅데이터·AR/VR 등 4차산업융합 콘텐츠 포함 권장 · 최신 OA버전 반영 등 실무 중심 콘텐츠 요구 — 근거: 문서2, 문서4  
- 외부 공공콘텐츠(K-MOOC 등) 연계, 북러닝·전화외국어·전문자격 과정 등 다양한 형식 지원 — 근거: 문서4, 문서12  
- 접근성 및 정보화 표준 준수(행정안전부·과기정통부 지침, 웹접근성 등) 요구 — 근거: 문서6

3. 개발 방법·자원·검증
- 콘텐츠 개발 방법론·보유기술·개발도구·장비 보유현황 및 확보방안 제시 요구(동영상 촬영·전자책 제작 지원 포함) — 근거: 문서8  
- 촬영지원: 공단 요청 시 현장·스튜디오 촬영 및 실시간 송출 지원(예: 10회 촬영지원, 1회 기준 1일 8시간) 및 장비·인력 지원 — 근거: 문서9(PSR-001), 문서8

4. 검수·품질관리·보고
- 교육콘텐츠 평가 및 품질관리 방안 제시 요구(QUR-001) — 근거: 문서10  
- 콘텐츠 개발 완료 최소 14일 이전에 사업완료보고서 초안 제출(검수·심의 절차) 및 매월·수시 보고 의무 — 근거: 문서3(PMR-003)  
- 개정사항(법령·업무처리 변경·오탈자 등) 발생 시 즉시 수정·보고 및 수정 범위에 따른 처리 절차(단순수정·대폭변경 등) 제시 — 근거: 문서9

5. 유지관리·하자보수·기술지원
- 콘텐츠 유지보수(차시별 관리·텍스트 수정·재구성 등) 및 최신 법령·지침 반영 관리프로세스 운영 요구 — 근거: 문서11(MAR-002), 문서9  
- 하자보수: 최종 검수 후 콘텐츠의 20% 범위 내에서 최소 1년 이내 지원 요구(사업기간 종료 후 하자보수 범위·체계 제시) — 근거: 문서3  
- 선정업체는 이러닝 관련 기술정보·기술자문을 공단에 무상 제공해야 함 — 근거: 문서3

6. 인수인계·저작권·보안
- 소스·게시자료 포함 각종 데이터 및 소스코드 인수인계 방안 제시, 인수인계 후 이전업체의 자료 폐기 등 요구 — 근거: 문서8, 문서10  
- 개인정보보호·정보보안 준수 및 보안관리 방안 제시 요구(인수인계 포함) — 근거: 문서10, 문서8

7. 참고(요
...(truncated; full text is in report_evidence.json)
```

#### q3_multi_topic - issue_or_audit_queue

- question: 교육이나 학습 관련해서 다른 기관이 발주한 사업은 없나?
- EDD: 93.52; coverage: None; first_hit_rank: None; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 인천광역시, 한국사학진흥재단, 고려대학교, 국민연금공단, 전북특별자치도 정읍시, 전북대학교, 국민연금공단, 국민연금공단, 울산광역시, 한국철도공사 (용역), 대한장애인체육회, 축산물품질평가원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
있음. 제공된 문서 내에서 교육·학습 관련 요구사항이나 이러닝/LMS/LRS 등 교육사업으로 확인되는 타 기관 발주 사업은 다음과 같습니다(근거: 해당 문서).

- 인천광역시 — 인천일자리플랫폼 정보시스템 구축 ISP 수립용역 (문서1, PSR-001 교육지원)  
- 고려대학교 — 차세대 포털·학사 정보시스템 구축사업 (문서3, 교직·실습·이수관리 등 교육 관련 기능 기술)  
- 국민연금공단 — 2024년 이러닝시스템 운영 용역 (문서4·7·8, 이러닝 콘텐츠·교육평가·교육인원 등 상세 요구)  
- 전북대학교 — JST 공유대학(원) xAPI기반 LRS시스템 구축 (문서6, LRS 구축으로 학습기록 관련 사업)  
- 울산광역시 — 2024년 버스정보시스템 확대 구축 및 기능개선 용역 (문서9, PSR-003 교육 계획 요구)  
- 한국철도공사 — 운행정보기록 자동분석시스템 개량 (문서10, PSR-001 교육지원)  
- 축산물품질평가원 — 꿀 품질평가 전산시스템 기능개선 사업 (문서12, PSR-02·PSR-03 교육지원·교육자료 제작)

참고: 정읍시 발주 정읍체육트레이닝센터 통합운영관리시스템(문서5)에는 '교육담당자/교육대상자' 서명란 등 교육 관련 항목이 있으나 교육요구사항의 구체성은 문서에 제한적입니다.
```

#### q5_followup - issue_or_audit_queue

- question: 기초과학연구원 극저온시스템 사업 요구에서 AI 기반 예측에 대한 요구사항이 있나? / 그럼 모니터링 업무에 대한 요청사항이 있는지 찾아보고 알려 줘.
- EDD: 93.52; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원, 기초과학연구원
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
사업명: 2025년도 중이온가속기용 극저온시스템 운전 용역 / 발주기관: 기초과학연구원

결론: 예, 제공된 문서에서 모니터링 업무에 대한 구체적 요청사항이 확인됩니다.

근거(주요 요청사항 요약, 관련 문서·항목):
- 가동기간 24시간 모니터링 운영(기본 2인 1조, 주간 감독자 상주) — 문서10 3.3.1.
- 모니터링 대상 및 세부 업무(알람 메시지 확인, 주요 센서 트렌드 확인(온도·압력·유량·속도 등), 비정상 상황 감지, 제어로직 정상성 확인, 현장 관찰·순찰 등) — 문서2·문서11 표 4.
- 모니터링은 연구원 구축 제어시스템(WinCC, CS‑studio 등) 또는 현장 장치를 활용하여 수행 — 문서11 표 5, 문서10 3.3.1.
- 주요 수치의 전자적 기록(기록 항목·간격은 연구원이 정함) 및 필요 시 연구원 요청에 따른 분석 수행(분석 대상·방법·결과물 형태는 연구원이 정함) — 문서2·문서12 3.3.2.
- 기록·제출 의무(극저온시스템 주요 수치 기록문서·일일근무일지·월간보고서 등, 일부는 매월 기성 제출) — 문서6 제출문서 표(표 13).
- 장비·교육 관련: 연구원은 제어시스템용 컴퓨터·모니터·키보드·마우스·책상·의자 및 기본 사용 교육 제공, 계약자는 기록용 노트북·키보드·마우스 등 준비해야 함 — 문서2·문서10.

문서에 없는 내용은 추측하지 않았습니다.
```

#### q7_compare - issue_or_audit_queue

- question: 고려대학교 차세대 포털 시스템 사업이랑 광주과학기술원의 학사 시스템 기능개선 사업을 비교해 줄래?
- EDD: 93.52; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 고려대학교, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
아래 비교는 제공된 문서 내용만을 근거로 작성했으며, 근거가 된 사업명·발주기관을 각 항목에 명시합니다.

1) 사업 목적
- 고려대학교(차세대 포털·학사 정보시스템 구축사업): 노후 시스템을 차세대로 구축해 정보서비스 품질 강화 및 대학 교육 시스템 경쟁력 확보(고려대학교 문서).  
- 광주과학기술원(학사시스템 기능개선 사업): 학사조직 개편 및 학위 연계과정 신설/변경에 따른 시스템 개선으로 업무 편리성·효율성 및 사용자 편의성 증대(광주과학기술원 문서).

2) 사업 범위·주요 기능
- 고려대학교: 포털(통합로그인/SSO, 통합·지능형 검색, 마이페이지, 공지/알림, 일정, 커뮤니티, 위젯, 연계서비스(웹메일·챗봇·전자결재·학사/행정 등)·개인화·모바일(기존 호잇 앱 하이브리드 재구축) 등 포털·학사 전반의 응용SW 개발 및 DW/BI 연계 포함(고려대학교 문서들).  
- 광주과학기술원: 학사 조직개편 관련 설계·개발 및 학위연계(학사→석사, 학석사·학석박 통합연계, 대학원 과정변경 등) 관련 기능 추가 및 프로세스 변경·연동(요구사항 FUR-005·FUR-006 등)(광주과학기술원 문서·별표).

3) 대상 사용자 범위
- 고려대학교: 학생(졸업생 포함), 교직원, 연구원 등 교내 구성원 대상 포털 서비스(고려대학교 문서).  
- 광주과학기술원: 학사 운영 관련 관리자 및 학생 등(광주과학기술원 문서).  

4) 예산
- 고려대학교: 총사업비 11,270,000,000원(VAT 포함), 3년 분할지급(고려대학교 문서).  
- 광주과학기술원: 총사업비 157,300,000원(VAT 포함), 세부 내역(설계 53,000,000원, 개발·테스트 90,000,000원)(광주과학기술원 문서).

5) 사업기간·일정
- 고려대학교: 계약일로부터 24개월 이내, 무상유지보수 12개월(고려대학교 문서).  
- 광주과학기술원: 문서에 사업 시작·종료 기간의 총괄 기간 명시가 제공된 문서에서 확인할 수 없습니다(광주과학기술원 문서).

6) 계약/입찰 방식·지급 조건
- 고려대학교: 제한경쟁 입찰(협상에 의한 계약)(고려대학교 문서).  
- 광주과학기술원: 공개경쟁 입찰(협상에 의한 계약), 선금 50% 지급·잔금은 최종검수 후 지급, 공동수급 불가(광주과학기술원 문서).

7) 기술환경·연계 요구
- 고려대학교: 기존 포털(KUPID Java/Spring), 통합인증(SSO SafeIdentity), 통합검색(Search Formula-1), 모바일(호잇 Spring boot/Java/Kotlin/Swift) 등 다수 시스템과 연계·통합, DW/BI·ETL 요구 등 대내외 연계·표준·시큐어코딩 준수 요구(고려대학교 문서).  
- 광주과학기술원: 구체적 기존 기술스택은 제공된 문서에서 확인할 수 없습니다; 요구사항은 학사·학위연계 기능 중심(광주과학기술원 문
...(truncated; full text is in report_evidence.json)
```

#### q8_compare_precise - issue_or_audit_queue

- question: 고려대학교랑 광주과학기술원 각각 응답 시간에 대한 요구사항이 있나? 문서를 기반으로 정확하게 답변해 줘.
- EDD: 93.52; coverage: 1.0; first_hit_rank: 1; abstention: False; expected_abstention: False
- judge: groundedness=None, relevance=None
- retrieved_orgs: 광주과학기술원, 고려대학교, 고려대학교, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교, 광주과학기술원, 고려대학교
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
- 고려대학교(사업명: 차세대 포털·학사 정보시스템 구축사업) — 있음. 근거: 문서4(요구사항 PER-002, PER-003).
  - 요구사항: 모든 질의의 업무응답시간 및 웹페이지 디스플레이 시간은 사용자가 요청한 시점으로부터 3초 이내 처리/표시.
  - 예외: 대량데이터(기준 5,000건 이상)나 대형이미지(기준 500KB 이상)·영상 포함 페이지, 또는 동시사용자 용량의 90% 초과 시에는 적용 제외(단 대량데이터 처리시간 기준 제시 요구).

- 광주과학기술원(사업명: 실시간통합연구비관리시스템(RCMS) 연계 모듈 변경 사업) — 제공된 문서에서 응답시간 관련 요구사항을 확인할 수 없습니다. 근거: 문서1, 문서7, 문서9, 문서11 등.
```

#### q10_abstention - issue_or_audit_queue

- question: 이 문서들 중에 우주 로켓 발사 시스템 구축 사업이 있나요?
- EDD: 93.52; coverage: None; first_hit_rank: None; abstention: True; expected_abstention: True
- judge: groundedness=None, relevance=None
- retrieved_orgs: (사)부산국제영화제, 한국가스공사, 고려대학교, 인천광역시, 한국철도공사 (용역), 인천광역시, 수협중앙회, 고려대학교, 그랜드코리아레저(주), 그랜드코리아레저(주), 파주도시관광공사, (사)부산국제영화제
- flags: missing_llm_judge_score
- interpretation: Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue.

Answer excerpt:

```text
제공된 문서들(예: 문서1: 2024년 BIFF & ACFM 온라인서비스 재개발… 발주기관: (사)부산국제영화제, 문서2: [재공고]차세대 통합정보시스템(ERP) 구축… 발주기관: 한국가스공사, 문서5: 예약발매시스템 개량 ISMP 용역… 발주기관: 한국철도공사, 문서6: 인천일자리플랫폼 ISP… 발주기관: 인천광역시, 문서7: 수협중앙회 수산물사이버직매장 재구축… 발주기관: 수협중앙회 등)에서는 우주 로켓 발사 시스템 구축 사업이 없습니다. 제공된 문서에서 확인할 수 없습니다.
```
