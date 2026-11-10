
import os
import streamlit as st
from openai import OpenAI, AuthenticationError, RateLimitError
from openai import APIConnectionError, APIStatusError

# =====================================
# 1. 기본 설정
# =====================================

st.set_page_config(
    page_title="학생 건강 도우미",
    page_icon="🌿",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #F5FAF7;
}
h1 {
    color: #247451;
}
h2, h3 {
    color: #327D5A;
}
.stButton button {
    background-color: #32815D;
    color: white;
    border-radius: 10px;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 2. API 키 불러오기
# =====================================

def get_api_key():
    # Streamlit Secrets 우선 확인
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
        if key:
            return str(key).strip()
    except Exception:
        pass

    # 환경변수 확인
    return os.getenv("OPENAI_API_KEY", "").strip()


def get_client():
    key = get_api_key()

    if not key:
        return None

    return OpenAI(
        api_key=key,
        timeout=60.0,
        max_retries=2
    )


# =====================================
# 3. 제목
# =====================================

st.title("🌿 학생 건강 도우미")

st.write("""
나의 증상을 입력하고 건강 상태에 관한 정보,
식단 및 생활 관리 방법을 확인해 보세요.
""")

st.info(
    "본 서비스는 건강 교육을 위한 AI 프로그램이며 "
    "의사의 진단이나 약사의 복약 지도를 대신하지 않습니다."
)

st.divider()

# =====================================
# 4. 사용자 입력
# =====================================

st.subheader("🩺 건강 상태 입력")

with st.form("health_form"):

    symptoms = st.text_area(
        "현재 어떤 증상이 있나요?",
        placeholder="예: 목이 아프고 기침이 나며 콧물이 나요.",
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:
        duration = st.selectbox(
            "증상 지속 기간",
            ["오늘부터", "1~3일", "4~7일", "1주일 이상"]
        )

    with col2:
        severity = st.selectbox(
            "증상 정도",
            ["가벼움", "보통", "심함"]
        )

    temperature = st.selectbox(
        "현재 체온",
        ["정상", "37.5~38℃", "38℃ 이상", "모름"]
    )

    allergy = st.text_input(
        "알레르기 및 복용 중인 약",
        placeholder="예: 없음 / 특정 약물 알레르기"
    )

    submitted = st.form_submit_button(
        "건강 정보 분석하기",
        use_container_width=True
    )

# =====================================
# 5. 위험 증상 확인
# =====================================

danger_words = [
    "호흡곤란",
    "숨쉬기 힘들",
    "숨을 못 쉬",
    "의식 잃",
    "의식이 없",
    "심한 흉통",
    "가슴 통증이 심",
    "경련",
    "입술이 파래",
    "목이 부어 숨",
    "심한 알레르기 반응"
]

# =====================================
# 6. AI 건강 정보 분석
# =====================================

if submitted:

    if not symptoms.strip():
        st.warning("증상을 먼저 입력해 주세요.")

    elif any(word in symptoms for word in danger_words):

        st.error("응급 평가가 필요한 증상일 수 있습니다.")

        st.write("""
        즉시 주변의 보호자나 선생님에게 알리세요.
        호흡곤란, 심한 흉통, 의식 변화 등 응급 증상이 있다면
        119에 연락하거나 응급의료기관의 도움을 받으세요.
        """)

    else:

        client = None

        try:
            client = get_client()
        except Exception:
            st.error(
                "API 클라이언트를 생성하지 못했습니다. "
                "API 설정을 확인해 주세요."
            )

        if client is None and not get_api_key():
            st.error("""
            API 키를 찾을 수 없습니다.

            Streamlit Cloud의 Settings → Secrets에서
            OPENAI_API_KEY를 설정해 주세요.
            """)
        
        elif client is not None:

            prompt = f"""
너는 고등학생을 위한 건강 교육 정보 도우미야.

다음 정보를 바탕으로 건강 관련 교육 정보를 제공해.

[사용자 정보]
증상: {symptoms}
지속 기간: {duration}
증상 정도: {severity}
체온: {temperature}
알레르기 및 복용 약: {allergy}

[안전 원칙]
- 질병을 확정 진단하지 않는다.
- 가능한 원인은 최대 3개까지 설명하고 불확실성을 밝힌다.
- 처방약이나 특정 약의 복용을 지시하지 않는다.
- 일반의약품은 약국에서 약사에게 상담할 수 있는 성분 또는 종류에 관한 일반 정보만 제공한다.
- 복용량과 복용 횟수를 임의로 제시하지 않는다.
- 알레르기, 중복 성분, 연령 제한 및 약물 상호작용에 주의한다.
- 음식이 질병을 치료한다고 표현하지 않는다.
- 위험 증상이나 악화 시 보호자와 의료진에게 도움을 요청하도록 한다.

[답변 형식]

### 1. 증상 분석
입력한 증상에 대한 설명과 가능한 원인

### 2. 건강 관리 정보
증상 완화에 도움이 될 수 있는 일반적인 생활 관리

### 3. 약국 상담 정보
약사에게 문의할 수 있는 일반의약품의 종류와 주의사항

### 4. 추천 식단
아침, 점심, 저녁 식단 및 수분 섭취 방법

### 5. 피하거나 줄이면 좋은 음식
증상에 따라 불편함을 악화시킬 수 있는 음식과 이유

### 6. 생활 습관
수면, 휴식, 위생 등 관리 방법

### 7. 병원 진료가 필요한 상황
증상 악화 및 지속 시 대처 방법

학생이 이해하기 쉬운 한국어로 답변해.
"""

            st.divider()
            st.subheader("📋 건강 분석 결과")

            with st.spinner("AI가 건강 정보를 분석하고 있습니다..."):

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "학생 건강 교육 정보 제공 AI. "
                                    "확정 진단과 처방은 하지 않는다."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    answer = response.choices[0].message.content

                    if answer:
                        st.markdown(answer)
                    else:
                        st.warning("AI가 답변을 생성하지 못했습니다.")

                    st.success("건강 정보 분석이 완료되었습니다.")

                except AuthenticationError:
                    st.error("""
                    [인증 오류]

                    API 키가 잘못되었거나 유효하지 않습니다.
                    OpenAI API 키를 다시 확인해 주세요.
                    """)

                except RateLimitError:
                    st.error("""
                    [사용량 또는 한도 오류]

                    API 사용량 한도 또는 요청 제한을 확인해 주세요.
                    OpenAI API 결제 및 사용량 설정을 확인하세요.
                    """)

                except APIConnectionError:
                    st.error("""
                    [연결 오류]

                    인터넷 연결 또는 API 서버 연결을 확인해 주세요.
                    잠시 후 다시 시도해 주세요.
                    """)

                except APIStatusError as e:
                    st.error(
                        f"API 서버 오류가 발생했습니다. "
                        f"상태 코드: {e.status_code}"
                    )

                except Exception as e:
                    st.error(
                        f"예상하지 못한 오류가 발생했습니다: {str(e)}"
                    )

# =====================================
# 7. 하단 안내
# =====================================

st.divider()

st.caption("""
🌿 학생 건강 도우미

이 프로그램은 건강 교육 및 정보 제공 목적으로 제작되었습니다.
실제 진단과 치료, 약물 선택은 의료진 및 약사와 상담하세요.
""")

