
import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
import os
import re

st.set_page_config(
    page_title="국어 모의고사 분석실",
    page_icon="📚",
    layout="wide"
)

st.title("📚 국어 모의고사 AI 분석실")
st.write("고2·고3 모의고사 지문을 읽고 분석하며 공부하는 공간")

# API 설정
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.warning("GitHub에 배포한 뒤 Streamlit Secrets에 API 키를 등록해 주세요.")

# PDF 자료 폴더
DATA_FOLDER = "자료"
os.makedirs(DATA_FOLDER, exist_ok=True)

# PDF 파일 목록
pdf_files = [
    f for f in os.listdir(DATA_FOLDER)
    if f.lower().endswith(".pdf")
]

# PDF 업로드
st.sidebar.header("📂 모의고사 자료")

uploaded_file = st.sidebar.file_uploader(
    "모의고사 PDF 추가",
    type=["pdf"]
)

if uploaded_file:
    save_path = os.path.join(DATA_FOLDER, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("PDF 업로드 완료!")
    st.rerun()

if not pdf_files:
    st.info("GitHub 저장소의 자료 폴더에 모의고사 PDF를 올려 주세요.")
    st.stop()

selected_pdf = st.sidebar.selectbox(
    "모의고사 선택",
    pdf_files
)

# PDF 텍스트 추출
reader = PdfReader(os.path.join(DATA_FOLDER, selected_pdf))

page_texts = []
for page in reader.pages:
    page_texts.append(page.extract_text() or "")

st.subheader("📖 지문 선택")

page_number = st.selectbox(
    "분석할 페이지",
    range(1, len(page_texts) + 1)
)

passage = page_texts[page_number - 1]

st.text_area(
    "PDF 원문",
    passage,
    height=250
)

# 직접 지문 입력
with st.expander("지문 직접 입력하기"):
    custom_passage = st.text_area(
        "분석할 지문을 입력하세요",
        height=200
    )

if custom_passage.strip():
    passage = custom_passage

# AI 분석 함수
def analyze(prompt):
    if not api_key:
        st.error("Streamlit Secrets에 OPENAI_API_KEY를 등록해 주세요.")
        return

    client = OpenAI(api_key=api_key)

    with st.spinner("AI가 지문을 분석하고 있어요..."):
        try:
            response = client.responses.create(
                model="gpt-5.4-nano",
                instructions="""
                너는 고등학교 2~3학년 국어 모의고사 전문 강사야.
                학생이 지문을 정확하게 이해하도록 쉽게 설명해 줘.
                반드시 제공된 지문을 근거로 분석하고,
                지문에 없는 내용을 임의로 만들어 내지 마.
                어려운 개념은 구체적인 예시를 들어 설명해 줘.
                """,
                input=f"{prompt}\n\n[지문]\n{passage}"
            )
            st.markdown(response.output_text)

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 분석 메뉴
st.divider()
st.header("1. 지문 전체 분석")

if st.button("🔍 지문 전체 분석하기", use_container_width=True):
    analyze("""
    다음 항목에 따라 지문을 분석해 줘.

    1. 지문의 주제와 중심 내용
    2. 핵심 주장 또는 설명
    3. 전체 내용 3줄 요약
    4. 문단별 핵심 내용
    5. 문단 사이의 연결 관계
    6. 글의 전개 방식과 근거
    7. 핵심 개념 정리
    8. 시험에 출제될 만한 내용
    """)

st.divider()
st.header("2. 핵심 어휘 분석")

if st.button("📚 어려운 단어와 개념 정리", use_container_width=True):
    analyze("""
    지문에서 중요한 어휘 10개를 선정해 줘.

    각 어휘마다 다음을 정리해 줘.
    1. 단어
    2. 사전적 의미
    3. 지문에서 사용된 문맥상 의미
    4. 쉬운 예시
    5. 헷갈리기 쉬운 유사 표현

    지문에 실제 등장하는 어휘를 우선적으로 선정해 줘.
    """)

st.divider()
st.header("3. 어려운 문장 분석")

sentence = st.text_area(
    "이해하기 어려운 문장을 입력하세요",
    placeholder="분석하고 싶은 문장을 붙여 넣으세요."
)

if st.button("✏️ 문장 쉽게 풀이하기", use_container_width=True):
    if sentence.strip():
        analyze(f"""
        다음 문장을 자세하게 분석해 줘.

        문장: {sentence}

        1. 쉬운 말로 바꾸기
        2. 문장 구조 분석
        3. 핵심 어휘 설명
        4. 문장의 의미와 역할
        5. 학생들이 오해하기 쉬운 부분
        """)
    else:
        st.warning("분석할 문장을 입력해 주세요.")

st.divider()
st.header("4. 시험 대비 핵심 정리")

if st.button("🎯 출제 포인트 분석", use_container_width=True):
    analyze("""
    이 지문을 고등학교 국어 모의고사에 출제한다고 가정하고 분석해 줘.

    1. 출제 가능성이 높은 핵심 내용
    2. 내용 일치·불일치 문제의 함정
    3. 선지에서 바꾸어 표현할 수 있는 부분
    4. 반드시 기억해야 하는 개념
    5. 학생들이 헷갈릴 만한 부분
    """)

st.divider()
st.header("5. 지문 확인 문제")

if st.button("📝 객관식 문제 5개 만들기", use_container_width=True):
    analyze("""
    이 지문을 바탕으로 고2~고3 모의고사 수준의
    5지선다형 문제 5개를 만들어 줘.

    주제, 세부 내용, 문단 관계, 어휘의 문맥상 의미,
    글의 전개 방식 등을 골고루 출제해 줘.

    정답과 해설은 마지막에 따로 정리해 줘.
    모든 문제는 반드시 지문을 근거로 만들어 줘.
    """)

st.divider()
st.header("6. 나만의 질문")

question = st.text_input(
    "지문을 공부하다 궁금한 점을 질문하세요"
)

if st.button("💬 질문하기"):
    if question.strip():
        analyze(question)
    else:
        st.warning("질문을 입력해 주세요.")

st.caption("※ PDF가 이미지로 스캔된 경우 글자 추출이 되지 않을 수 있습니다.")

