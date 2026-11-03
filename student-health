
import streamlit as st
from openai import OpenAI

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="학생 건강 도우미",
    page_icon="🌿",
    layout="centered"
)

# -----------------------------------
# API 설정
# -----------------------------------
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )
except Exception:
    client = None

# -----------------------------------
# 스타일
# -----------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F6FAF8;
}
h1 {
    color: #246B55;
}
h2, h3 {
    color: #347D65;
}
div.stButton > button {
    background-color: #347D65;
    color: white;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 제목
# -----------------------------------
st.title("🌿 학생 건강 도우미")

st.write(
    "증상에 따른 건강 정보를 확인하고 "
    "식단과 생활 습관을 알아보세요."
)

st.info(
    "이 프로그램은 건강 교육용입니다. "
    "의사의 진단을 대신하지 않습니다."
)

# -----------------------------------
# 입력
# -----------------------------------
with st.form("health_form"):

    symptoms = st.text_area(
        "현재 어떤 증상이 있나요?",
        placeholder="예: 목이 아프고 기침이 나며 콧물이 있어요."
    )

    duration = st.selectbox(
        "증상이 얼마나 지속되었나요?",
        [
            "오늘부터",
            "1~3일",
            "4~7일",
            "1주일 이상"
        ]
    )

    severity = st.select_slider(
        "증상의 심한 정도",
        options=[
            "가벼움",
            "보통",
            "심함"
        ]
    )

    temperature = st.selectbox(
        "체온",
        [
            "정상 체온",
            "37.5~38℃",
            "38℃ 이상",
            "체온을 모름"
        ]
    )

    allergy = st.text_input(
        "알레르기 또는 복용 중인 약",
        placeholder="없으면 없음"
    )

    submitted = st.form_submit_button(
        "건강 정보 확인하기"
    )

# -----------------------------------
# 응급 증상 확인
# -----------------------------------
danger_words = [
    "호흡곤란",
    "숨을 못",
    "의식이 없음",
    "의식 잃",
    "가슴을 쥐어",
    "심한 흉통",
    "경련",
    "입술이 파래",
    "심한 알레르기",
    "목이 부어 숨"
]

# -----------------------------------
# AI 분석
# -----------------------------------
if submitted:

    if not symptoms.strip():
        st.warning("증상을 입력해 주세요.")

    elif any(word in symptoms for word in danger_words):

        st.error(
            "위험할 수 있는 증상이 포함되어 있습니다."
        )

        st.write(
            "즉시 주변의 보호자나 선생님에게 알리고 "
            "119 또는 응급의료기관에 도움을 요청하세요."
        )

    elif client is None:

        st.error(
            "API 설정을 확인해 주세요. "
            "Streamlit Secrets에 API 키가 필요합니다."
        )

    else:

        with st.spinner("건강 정보를 분석하고 있어요..."):

            prompt = f"""
당신은 학생을 위한 건강 교육 정보 도우미입니다.

사용자가 입력한 증상을 바탕으로 건강 정보를 설명하세요.

[입력 정보]
증상: {symptoms}
지속 기간: {duration}
심한 정도: {severity}
체온: {temperature}
알레르기 및 복용 약: {allergy}

[필수 안전 지침]

1. 질병을 확정 진단하지 마세요.
2. 가능한 원인을 최대 3개까지 설명하되,
   가능성일 뿐이라는 점을 명시하세요.
3. 학생에게 처방약을 추천하지 마세요.
4. 일반의약품도 특정 제품의 복용을 지시하지 마세요.
5. 약국에서 약사에게 상담할 수 있는
   일반의약품의 종류와 주의사항을 설명하세요.
6. 약의 용량, 복용 횟수, 복용 기간을
   임의로 만들어내지 마세요.
7. 약물 알레르기, 중복 성분, 나이 제한,
   다른 약과의 상호작용을 고려하세요.
8. 학생의 증상에 적합한 식단을 추천하세요.
9. 증상 악화 시 피하거나 줄이면 좋은 음식과
   그 이유를 설명하세요.
10. 증상이 심하거나 지속되면 보호자와
    의료진에게 도움을 요청하도록 안내하세요.
11. 위험 증상이 의심되면 응급 진료를 안내하세요.
12. 식단이나 음식이 질병을 치료한다고
    표현하지 마세요.

[답변 형식]

### 1. 증상 이해하기
증상에 대한 쉬운 설명

### 2. 가능한 원인
가능한 원인과 그 이유

### 3. 약국에서 상담할 수 있는 정보
일반의약품의 종류, 주의사항,
약사에게 확인할 내용

### 4. 추천 식단
아침, 점심, 저녁 및 수분 섭취

### 5. 피하거나 줄이면 좋은 음식
음식과 이유

### 6. 생활 관리
학생이 일상에서 할 수 있는 관리 방법

### 7. 병원에 가야 하는 경우
보호자에게 알리거나 진료가 필요한 상황

답변은 한국어로 작성하세요.
"""

            try:

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "학생 건강 교육 도우미입니다. "
                                "의학적 진단이나 처방을 하지 않습니다. "
                                "안전 지침을 반드시 준수하세요."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                result = response.choices[0].message.content

                st.markdown("---")
                st.header("📋 건강 정보 결과")

                st.markdown(result)

                st.markdown("---")

                st.caption(
                    "본 결과는 AI가 생성한 건강 교육 정보입니다. "
                    "정확한 진단과 치료는 의료진에게 문의하세요."
                )

            except Exception as e:

                st.error(
                    "분석 중 오류가 발생했습니다. "
                    "API 키와 사용량을 확인해 주세요."
                )
