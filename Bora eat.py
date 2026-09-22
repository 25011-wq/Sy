import streamlit as st
from datetime import date

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="보라고등학교 급식",
    page_icon="🍱",
    layout="centered"
)

# -----------------------------
# 급식 데이터
# 날짜를 추가해서 사용할 수 있음
# -----------------------------
MEALS = {
    "2026-09-21": {
        "meal": "중식",
        "calorie": "928.8 Kcal",
        "menu": [
            "귀리밥/칼슘강화",
            "김치어묵국",
            "쫄면무침",
            "매쉬드포테이토",
            "바싹불고기",
            "[자율] 석박지",
            "파주장단콩초콜릿"
        ]
    },

    "2026-09-22": {
        "meal": "중식",
        "calorie": "1024.7 Kcal",
        "menu": [
            "찰보리밥/칼슘강화",
            "오색냉채",
            "떡잡채",
            "리치골드닭갈비",
            "애호박고추장찌개",
            "[자율] 총각김치"
        ]
    },

    "2026-09-23": {
        "meal": "중식",
        "calorie": "",
        "menu": [
            # 여기에 9월 23일 메뉴 입력
        ]
    }
}


# -----------------------------
# 제목
# -----------------------------
st.title("🍱 보라고등학교 급식")
st.caption("보라고등학교 오늘의 급식을 확인하세요.")


# -----------------------------
# 날짜 선택
# -----------------------------
selected_date = st.date_input(
    "📅 날짜를 선택하세요",
    value=date.today()
)

date_key = selected_date.strftime("%Y-%m-%d")


# -----------------------------
# 급식 표시
# -----------------------------
if date_key in MEALS:

    meal = MEALS[date_key]

    st.success(
        f"{selected_date.strftime('%Y년 %m월 %d일')} 급식"
    )

    st.subheader(f"🍚 {meal['meal']}")

    if meal["calorie"]:
        st.info(f"🔥 {meal['calorie']}")

    st.markdown("### 🍽️ 오늘의 메뉴")

    for food in meal["menu"]:
        st.write(f"• {food}")

else:

    st.warning(
        "해당 날짜의 급식 정보가 아직 등록되지 않았습니다."
    )

    st.write(
        "다른 날짜를 선택하거나 급식 데이터를 추가해주세요."
    )


# -----------------------------
# 학교 정보
# -----------------------------
st.divider()

st.caption("보라고등학교")
st.caption("경기도 용인시 기흥구 한보라1로43번길 7")
