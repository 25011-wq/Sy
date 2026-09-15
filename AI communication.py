import streamlit as st
from openai import OpenAI


# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="학업 고민상담기",
    page_icon="📚",
    layout="centered"
)


# ==========================================
# OpenAI 설정
# ==========================================

try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error(
        "OpenAI API Key가 설정되지 않았습니다.\n\n"
        "Streamlit Cloud → Settings → Secrets에서 "
        "OPENAI_API_KEY를 설정해주세요."
    )
    st.stop()


MODEL = "gpt-5.4-nano"


# ==========================================
# 스타일
# ==========================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8f9fc;
    }

    .title {
        text-align: center;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .info-box {
        padding: 15px;
        border-radius: 12px;
        background-color: #f0f4ff;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 제목
# ==========================================

st.markdown(
    '<div class="title">📚 학업 고민상담기</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">공부, 성적, 진로, 학교생활에 대한 고민을 편하게 이야기해보세요.</div>',
    unsafe_allow_html=True
)


# ==========================================
# 세션 상태
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# 안내
# ==========================================

with st.expander("💡 이런 고민을 상담할 수 있어요"):
    st.write(
        """
        - 공부 방법이 고민될 때
        - 시험이나 수행평가가 걱정될 때
        - 성적 때문에 스트레스를 받을 때
        - 진로와 학업을 어떻게 연결할지 고민될 때
        - 시간 관리가 어려울 때
        - 학교생활에서 학업 때문에 고민될 때
        """
    )


# ==========================================
# 이전 대화 출력
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# 사용자 입력
# ==========================================

user_input = st.chat_input(
    "학업 고민을 자유롭게 적어주세요..."
)


if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 화면 출력
    with st.chat_message("user"):
        st.markdown(user_input)


    # ======================================
    # AI 상담
    # ======================================

    with st.chat_message("assistant"):

        with st.spinner("고민을 생각해보고 있어요..."):

            try:

                # 대화 내용을 OpenAI 형식으로 변환
                conversation = []

                for message in st.session_state.messages:
                    conversation.append(
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                    )


                response = client.responses.create(

                    model=MODEL,

                    instructions="""
너는 친절하고 현실적인 '학업 고민 상담 AI'이다.

상담 대상은 중·고등학생이다.

주로 다음과 같은 고민을 상담한다.
- 공부 방법
- 시험 및 성적
- 수행평가
- 시간 관리
- 학습 습관
- 진로와 학업
- 학교생활
- 학업으로 인한 걱정

답변 원칙:

1. 학생의 고민을 먼저 공감하고 이해한다.

2. 단순히 "힘내"라고 말하는 것보다
   실제로 실행할 수 있는 방법을 제시한다.

3. 학생의 상황을 고려하여
   너무 많은 방법을 한꺼번에 제시하지 않는다.

4. 가능하면
   '지금 할 수 있는 것 → 이번 주에 할 것'
   순서로 구체적으로 설명한다.

5. 성적이나 등수를 다른 학생과 비교하도록
   부추기지 않는다.

6. 완벽주의나 과도한 공부를 권장하지 않는다.

7. 학생이 실패했다고 느끼더라도
   그것을 능력 부족으로 단정하지 않는다.

8. 답변은 한국어로 한다.

9. 고등학생이 이해하기 쉬운 표현을 사용한다.

10. 필요한 경우 상담을 이어갈 수 있도록
    마지막에 짧은 질문 하나를 덧붙인다.

답변은 너무 길지 않게 작성한다.
""",

                    input=conversation
                )

                answer = response.output_text


                # AI 답변 출력
                st.markdown(answer)


                # AI 답변 저장
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "AI 상담 중 오류가 발생했습니다.\n\n"
                    f"오류 내용: {str(e)}"
                )


# ==========================================
# 사이드바
# ==========================================

with st.sidebar:

    st.header("📚 학업 고민상담기")

    st.write(
        """
        공부와 학교생활에 관한 고민을
        AI와 대화하면서 정리해보세요.
        """
    )

    st.divider()

    if st.button("🗑️ 상담 내용 초기화", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "※ AI의 답변은 참고용이며, 중요한 결정은 "
        "선생님이나 보호자 등 신뢰할 수 있는 어른과 함께 결정하세요."
    )
