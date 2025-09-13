# app.py
import time
import random
import textwrap
import streamlit as st

# -------------------- 기본 설정 --------------------
st.set_page_config(
    page_title="MBTI 공부법 추천기",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -------------------- 스타일(CSS) --------------------
st.markdown("""
<style>
/* 제목 그라데이션 */
.grad {
  font-weight: 800;
  font-size: 2.1rem;
  line-height: 1.15;
  background: linear-gradient(90deg, #7c3aed, #06b6d4, #22c55e, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 살짝 흔들리는 이모지 */
.wiggle {
  display: inline-block;
  animation: wiggle 1.2s ease-in-out infinite;
}
@keyframes wiggle {
  0%, 100% { transform: rotate(0deg) translateY(0px); }
  25% { transform: rotate(4deg) translateY(-1px); }
  75% { transform: rotate(-4deg) translateY(1px); }
}

/* 카드 느낌 */
.tip-card {
  border-radius: 16px;
  padding: 1rem 1.1rem;
  border: 1px solid rgba(120,119,198,0.25);
  background: rgba(124,58,237,0.06);
  margin-bottom: 0.6rem;
}
.small {
  opacity: 0.9; font-size: 0.95rem;
}
.badge {
  display: inline-block;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  background: #111827;
  color: #fff;
  font-size: 0.75rem;
  margin-right: 6px;
}
hr.grad { 
  border: 0; height: 1px;
  background: linear-gradient(90deg, #0000, #7c3aed55, #0000);
  margin: 0.8rem 0 1rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------- 데이터 --------------------
MBTI_TIPS = {
    # 각 유형별 핵심 성향 요약 + 추천 공부법 (짧고 실전적)
    "INTJ": {
        "tag": "전략가 🧠",
        "summary": "장기 전략과 구조화에 강함. 목표-역전 설계형.",
        "tips": [
            "🎯 **역방향 계획**: 최종 점수 ➝ 단원 ➝ 하루 할당량 거꾸로 쪼개기.",
            "📊 **메트릭 보드**: 정답률·시간·오답유형 대시보드로 점검.",
            "🧩 **원리 우선**: 공식을 암기보다 ‘유도과정’으로 정리.",
            "🔁 **스파이럴 리뷰**: 2일·7일·21일 간격으로 재노출.",
            "🚫 **주의**: 과도한 완벽주의로 착수 지연 금지(80% 기준선 실행).",
        ],
        "tools": "Notion/Obsidian로 지식 그래프 만들기 🔗",
    },
    "INTP": {
        "tag": "분석가 🧪",
        "summary": "개념 해체·재조립의 달인. 깊게 파고듦.",
        "tips": [
            "🧱 **개념 블록화**: 핵심정의→반례→경계조건 순서로 정리.",
            "📝 **왜? 노트**: 각 공식 옆에 ‘성립 이유’를 한 줄로.",
            "🔄 **메타-오답**: 틀린 이유를 분류표(개념/주의력/계산/전략).",
            "⏱️ **포모도로 딥워크**: 45분 집중 + 10분 산책.",
            "🚫 **주의**: 토픽 점프 방지—‘오늘의 질문 3개’만 해결.",
        ],
        "tools": "Jupyter/Desmos로 실험처럼 개념 검증 🧫",
    },
    "ENTJ": {
        "tag": "지휘관 🧭",
        "summary": "목표지향·실행력 최강. 시스템 구축형.",
        "tips": [
            "🏁 **성과 백로그**: 주간 KPI(문항 수/범위/오답감소율) 설정.",
            "📈 **모의고사 스프린트**: 주 1회 전범위 모사 + 회고.",
            "🤝 **스터디 리드**: 역할분담(문항출제·채점·피드백) 운영.",
            "🧠 **전략 전환 규칙**: 2주 무효 전략은 폐기/수정.",
            "🚫 **주의**: 과속 금지—개념 사각지대 체킹.",
        ],
        "tools": "Trello/Asana 로드맵 🗺️",
    },
    "ENTP": {
        "tag": "발명가 💡",
        "summary": "아이디어 폭발. 변형·응용 문제에 강함.",
        "tips": [
            "🎲 **문제 리믹스**: 기출을 조건 바꿔 재출제해보기.",
            "🧠 **Feynman 설명**: 10살에게도 설명 가능할 때까지.",
            "⏳ **타임 어택**: 제한시간 내 풀이 전략 실험.",
            "🔁 **랜덤 큐**: 다른 과목 섞기—지루함 차단.",
            "🚫 **주의**: 수렴 페이즈 필수—정답률 분석으로 고정.",
        ],
        "tools": "Miro로 개념 맵+아이디어 브레인스토밍 🌀",
    },
    "INFJ": {
        "tag": "옹호자 🌱",
        "summary": "의미 중심·깊은 몰입. 스토리텔링에 강함.",
        "tips": [
            "📚 **의미 연결**: 개념을 사례·비유로 엮어 기억.",
            "🗂️ **테마별 노트**: 단원 대신 ‘핵심질문’ 기준 분류.",
            "🎧 **프리라이팅**: 공부 전 5분 목표·감정 기록.",
            "🧘 **리추얼**: 동일한 시간·장소·음악으로 몰입 스위치.",
            "🚫 **주의**: 과한 공감 피로—학습경계(시간/알림) 세우기.",
        ],
        "tools": "Notion 템플릿 + 힐링 BGM 🎵",
    },
    "INFP": {
        "tag": "중재자 🎨",
        "summary": "가치·감성 동기. 창의적 기록에 강함.",
        "tips": [
            "🖍️ **비주얼 노트**: 색·아이콘으로 감정-개념 연결.",
            "🎯 **미니 목표**: ‘오늘 3칸 채우기’ 식의 작게-확실한 성취.",
            "💬 **셀프-코칭**: 틀린 문제에 ‘다음엔 어떻게?’ 대화문 작성.",
            "🌿 **리듬 관리**: 낮엔 암기, 밤엔 개념정리 루틴.",
            "🚫 **주의**: 기분 의존 최소화—알람 기반 시작 의식.",
        ],
        "tools": "GoodNotes/캘리그라피로 기억 고정 ✍️",
    },
    "ENFJ": {
        "tag": "선도자 🤝",
        "summary": "협업·가르치기 강점. 피드백 순환 선호.",
        "tips": [
            "🧑‍🏫 **티치백**: 배운 내용 5분 미니 강의로 설명.",
            "📅 **피드백 위클리**: 목·금에 오답 리뷰 세션.",
            "👥 **파트너 러닝**: 상호 퀴즈/사례 토론.",
            "🪜 **난이도 사다리**: 쉬움→중간→어려움 단계적 상승.",
            "🚫 **주의**: 타인 챙기다 본인 진도 놓치지 않기.",
        ],
        "tools": "Google Forms 퀴즈로 즉시 피드백 ✅",
    },
    "ENFP": {
        "tag": "활동가 🚀",
        "summary": "열정·아이디어 폭발. 다양한 자극에 강함.",
        "tips": [
            "🎮 **게이미피케이션**: 문제풀이 콤보/랭크 시스템.",
            "🪄 **5분 스타트**: ‘딱 5분’ 규칙으로 진입 장벽 다운.",
            "🔀 **포맷 스위치**: 문제→카드→말로 설명 번갈아.",
            "📣 **공개 선언**: 오늘 목표를 친구/커뮤니티에 공유.",
            "🚫 **주의**: 과다 확장 금지—주요 과목 2개 집중.",
        ],
        "tools": "Anki/Quizlet 스택 만들기 🧱",
    },
    "ISTJ": {
        "tag": "현실주의자 🧾",
        "summary": "체계·성실. 체크리스트형 학습에 강함.",
        "tips": [
            "🗃️ **표준절차(SOP)**: 풀이 단계 체크리스트 고정.",
            "📆 **루틴 타임블록**: 과목별 고정 시간 배치.",
            "🧮 **오답 레퍼토리**: 유형-원인-해결 표준화.",
            "🔁 **같은 자리**: 동일 장소·시간으로 변동성 최소화.",
            "🚫 **주의**: 지나친 보수성—신유형 주1회 노출.",
        ],
        "tools": "Excel/Sheets 진도표 & 조건부서식 ✅",
    },
    "ISFJ": {
        "tag": "수호자 🧺",
        "summary": "성실·배려. 기록·축적형 학습 강점.",
        "tips": [
            "📚 **누적 요약**: 단원 끝에 10줄 요약 카드.",
            "⏲️ **타이머 학습**: 30-5-30-10 리듬으로 피로 분산.",
            "🧩 **연결 고리**: 이전 단원과 오늘 내용 1:1 매칭.",
            "🤗 **보상 루틴**: 소소한 보상(티/산책) 예약.",
            "🚫 **주의**: 질문 미루지 말고 ‘당일 질문 박스’ 처리.",
        ],
        "tools": "종이 바인더+색 인덱스 📎",
    },
    "ESTJ": {
        "tag": "경영자 📊",
        "summary": "규율·실행. 성과 관리에 강함.",
        "tips": [
            "🏷️ **OKR**: 목표-핵심결과(정답률/범위)로 주간 운영.",
            "🧩 **표준풀이**: ‘문제 유형→절차’ 매핑표.",
            "🧑‍⚖️ **자기감사**: 매 토요일 성과 리뷰 & 조정.",
            "🏁 **마감 효과**: 모의 마감시간으로 집중 촉발.",
            "🚫 **주의**: 유연성 확보—예외 케이스 사례 수집.",
        ],
        "tools": "Toggl/Clockify로 시간 로그 ⏱️",
    },
    "ESFJ": {
        "tag": "영사관 🤗",
        "summary": "협력·조화. 그룹 스터디 운영에 강함.",
        "tips": [
            "👥 **역할 스터디**: 진행/정리/질문/격려 역할 교대.",
            "📝 **공유 노트**: 회의록처럼 요약과 action item.",
            "🔄 **리마인드**: 시험 7·3·1일 전 재점검 일정.",
            "🎉 **마무리 의식**: 소소한 축하로 동기 상승.",
            "🚫 **주의**: 부탁 과다 수락 금지—‘학습 우선권’ 선언.",
        ],
        "tools": "Google Docs 공동 편집 📄",
    },
    "ISTP": {
        "tag": "장인 🔧",
        "summary": "실전·문제 해결. 실습형 학습 강함.",
        "tips": [
            "🧪 **케이스 드릴**: 유형별 핵심 케이스 반복.",
            "📉 **실수 리플레이**: 틀린 풀이 과정을 다시 녹화/복기.",
            "🧭 **의사결정 트리**: 조건→전략 선택도.",
            "⏱️ **스피드 런**: 쉬운 문제는 60% 시간으로.",
            "🚫 **주의**: 설명 생략 금지—근거 노트 작성.",
        ],
        "tools": "OneNote 스케치+수식 ✏️",
    },
    "ISFP": {
        "tag": "모험가 🫶",
        "summary": "감각·감성. 미적/감각 자극 활용.",
        "tips": [
            "🎧 **사운드트랙**: 과목별 BGM 지정으로 컨텍스트 스위치.",
            "🖼️ **갤러리 노트**: 핵심식·개념을 카드화해 전시.",
            "🌿 **미니 루틴**: 차·향·조명으로 몰입 신호.",
            "🧩 **소형 과제**: 25분 안에 끝나는 작고 명확한 태스크.",
            "🚫 **주의**: 회피성 미루기—‘2분 시작 규칙’ 적용.",
        ],
        "tools": "캘린더 위젯에 하루 3칸만 채우기 📆",
    },
    "ESTP": {
        "tag": "사업가 🏎️",
        "summary": "즉각 실행·경쟁. 실전 모드에 강함.",
        "tips": [
            "⚡ **타임 트라이얼**: 시간 제한 문제풀이로 승부.",
            "🎯 **점수 게임**: 목표 점수 달성 시 보상 즉시 지급.",
            "🔁 **현장감 복기**: 시험장 시뮬 + 잡음/시간 압박.",
            "📸 **한 페이지 요약**: 시험 전 마지막 한 장.",
            "🚫 **주의**: 검토 스킵 금지—막판 8분은 검토 고정.",
        ],
        "tools": "Kahoot/퀴즈 쇼다운 🥊",
    },
    "ESFP": {
        "tag": "연예인 🎉",
        "summary": "에너지·사회성. 체험형·상호작용 선호.",
        "tips": [
            "🎤 **설명 챌린지**: 친구 앞 1분 요약 발표.",
            "🎲 **카드 퀘스트**: 문제 뽑기 박스로 랜덤 미션.",
            "📅 **짧고 잦게**: 20분 세션을 하루 3~4회.",
            "📸 **성과 스냅**: 오늘 성취 사진으로 기록.",
            "🚫 **주의**: 산만함 방지—폰은 ‘집중 모드’.",
        ],
        "tools": "Padlet 보드에 성과 전시 🧑‍🎨",
    },
    "INF P".replace(" ",""): None,  # 안전장치(오타 방지)
    "ENFP ".strip(): None             # 안전장치(중복 키 방지)
}

ALL_TYPES = [t for t in [
    "INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"
] if t in MBTI_TIPS]

# -------------------- 사이드바 --------------------
with st.sidebar:
    st.markdown("<span class='grad'>MBTI 공부법 추천기</span>", unsafe_allow_html=True)
    st.caption("유형을 고르면, 그 유형에 딱 맞춘 공부 전략을 추천해요 ✨")
    mbti = st.selectbox("🎯 MBTI를 선택하세요", ALL_TYPES, index=0)
    show_fun = st.toggle("재미있는 효과 켜기 ✨", value=True)
    st.markdown("—")
    st.caption("💡 팁: 실제 성향과 다를 수 있어요. ‘나에게 맞는 것’만 골라 가져가세요!")

# -------------------- 헤더 --------------------
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("<div class='wiggle'>📚</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='grad'>나에게 딱 맞는 공부 전략</div>", unsafe_allow_html=True)
st.write("")

# -------------------- 본문: 추천 출력 --------------------
profile = MBTI_TIPS.get(mbti)
if profile is None:
    st.error("유형 정보를 불러오지 못했어요. 다른 유형을 선택해 주세요.")
    st.stop()

tag = profile["tag"]
st.markdown(f"<span class='badge'>{mbti}</span> <span class='badge'>{tag}</span>", unsafe_allow_html=True)
st.write(f"**요약:** {profile['summary']}")

st.markdown("<hr class='grad'/>", unsafe_allow_html=True)

# 재미있는 로딩 애니메이션(선택)
if show_fun and "shown_once" not in st.session_state:
    with st.spinner("당신의 공부 성향을 분석 중... 🔍"):
        for i in range(0, 101, 12):
            st.progress(i, text="개인화 전략 조율 중…")
            time.sleep(0.05)
    st.session_state["shown_once"] = True
    st.toast("분석 완료! 맞춤 전략이 준비됐어요 🎉", icon="🎯")
    st.balloons()

# 팁 카드 렌더링
st.subheader("✨ 맞춤 공부법")
for tip in profile["tips"]:
    st.markdown(f"<div class='tip-card small'>{tip}</div>", unsafe_allow_html=True)

st.markdown("<hr class='grad'/>", unsafe_allow_html=True)
st.write(f"**추천 도구/방식:** {profile['tools']}")

# -------------------- 추가 기능: 미니 루틴 생성기 --------------------
st.subheader("🗓️ 1일 미니 루틴 생성기")
colA, colB, colC = st.columns(3)
with colA:
    focus = st.slider("집중 세션(분)", 20, 60, 40, step=5)
with colB:
    breakm = st.slider("휴식(분)", 3, 15, 8, step=1)
with colC:
    cycles = st.slider("반복 횟수", 2, 6, 3)

if st.button("루틴 만들기 🚀"):
    total = cycles * (focus + breakm)
    st.success(f"총 {total}분 루틴이 생성되었어요! (집중 {focus}분 + 휴식 {breakm}분 × {cycles}회)")
    st.markdown("<hr class='grad'/>", unsafe_allow_html=True)
    for i in range(1, cycles + 1):
        st.markdown(f"**세션 {i}** — 🔥 집중 {focus}분 → 🌿 휴식 {breakm}분")

    if show_fun:
        st.snow()

# -------------------- 보너스: 랜덤 동기부여 & 배지 --------------------
QUOTES = [
    "작게, 하지만 매일. 🌱",
    "오늘의 1%가 내일의 100점을 만든다. 📈",
    "완벽보다 **시작**이 먼저! 🏁",
    "어제의 나와 경쟁하자. 🥇",
    "기억은 반복의 자식이다. 🔁",
]
if st.button("한 줄 동기부여 🔥"):
    st.info(random.choice(QUOTES))

# -------------------- 풋터 --------------------
st.markdown("<hr class='grad'/>", unsafe_allow_html=True)
st.caption("© MBTI 공부법 추천기 — 재미와 동기 부여를 위한 가이드. 실제 성향과 다를 수 있어요 🙂")
