import streamlit as st
import random

st.set_page_config(
    page_title="사칙연산 게임",
    page_icon="🧮",
    layout="centered"
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "question" not in st.session_state:
    st.session_state.question = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# -----------------------------
# 문제 생성 함수
# -----------------------------
def make_question(difficulty):
    if difficulty == "쉬움":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        operators = ["+", "-"]

    elif difficulty == "보통":
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        operators = ["+", "-", "×"]

    else:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        operators = ["+", "-", "×", "÷"]

    op = random.choice(operators)

    # 뺄셈은 음수가 나오지 않도록
    if op == "-":
        if a < b:
            a, b = b, a
        answer = a - b

    elif op == "+":
        answer = a + b

    elif op == "×":
        answer = a * b

    elif op == "÷":
        # 나누어떨어지는 문제 생성
        b = random.randint(1, 20)
        answer = random.randint(1, 20)
        a = b * answer

    return f"{a} {op} {b} = ?", answer


def new_question(difficulty):
    question, answer = make_question(difficulty)
    st.session_state.question = question
    st.session_state.answer = answer
    st.session_state.feedback = ""


# -----------------------------
# 제목
# -----------------------------
st.title("🧮 사칙연산 게임")
st.write("빠르게 계산하고 높은 점수에 도전해보세요!")

# -----------------------------
# 난이도
# -----------------------------
difficulty = st.selectbox(
    "난이도를 선택하세요",
    ["쉬움", "보통", "어려움"]
)

# 난이도가 바뀌었을 때 문제 새로 생성
if st.session_state.question is None:
    new_question(difficulty)

# -----------------------------
# 점수판
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("점수", st.session_state.score)

with col2:
    st.metric("연속 정답", st.session_state.streak)

with col3:
    st.metric("푼 문제", st.session_state.total)

st.divider()

# -----------------------------
# 문제
# -----------------------------
st.subheader("문제")

st.markdown(
    f"<h1 style='text-align:center;'>{st.session_state.question}</h1>",
    unsafe_allow_html=True
)

user_answer = st.number_input(
    "답을 입력하세요",
    step=1,
    value=0
)

# -----------------------------
# 정답 확인
# -----------------------------
if st.button("정답 확인", use_container_width=True):

    st.session_state.total += 1

    if user_answer == st.session_state.answer:

        st.session_state.streak += 1

        # 연속 정답에 따라 추가 점수
        gained = 10 + (st.session_state.streak - 1) * 2
        st.session_state.score += gained

        st.session_state.feedback = (
            f"🎉 정답입니다! +{gained}점"
        )

    else:

        st.session_state.streak = 0

        st.session_state.feedback = (
            f"❌ 틀렸어요! 정답은 {st.session_state.answer}입니다."
        )

    st.rerun()

# -----------------------------
# 결과 표시
# -----------------------------
if st.session_state.feedback:

    if "정답입니다" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

# -----------------------------
# 다음 문제
# -----------------------------
if st.button("➡️ 다음 문제", use_container_width=True):
    new_question(difficulty)
    st.rerun()

# -----------------------------
# 게임 초기화
# -----------------------------
st.divider()

if st.button("🔄 게임 다시 시작"):
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.total = 0
    new_question(difficulty)
    st.rerun()
