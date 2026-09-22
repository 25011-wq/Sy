import streamlit as st
import requests
from datetime import date, timedelta

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="보라고등학교 급식",
    page_icon="🍱",
    layout="centered"
)

# NEIS 학교 정보
ATPT_OFCDC_SC_CODE = "J10"   # 경기도교육청
SD_SCHUL_CODE = "7530882"    # 보라고등학교

API_URL = "https://open.neis.go.kr/hub/mealServiceDietInfo"


# -----------------------------
# 급식 데이터 가져오기
# -----------------------------
@st.cache_data(ttl=600)
def get_meal(api_key, target_date):
    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
        "SD_SCHUL_CODE": SD_SCHUL_CODE,
        "MLSV_YMD": target_date.strftime("%Y%m%d")
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        if "mealServiceDietInfo" not in data:
            return None, "급식 정보가 없습니다."

        rows = data["mealServiceDietInfo"][1]["row"]

        if not rows:
            return None, "해당 날짜의 급식 정보가 없습니다."

        return rows, None

    except requests.exceptions.RequestException:
        return None, "NEIS API 연결에 실패했습니다."

    except Exception:
        return None, "급식 정보를 불러오는 중 오류가 발생했습니다."


# -----------------------------
# 화면
# -----------------------------
st.title("🍱 보라고등학교 급식")
st.caption("NEIS 학교급식 식단정보를 이용합니다.")

# Secrets에서 API KEY 가져오기
if "NEIS_API_KEY" not in st.secrets:
    st.error(
        "NEIS_API_KEY가 설정되지 않았습니다.\n\n"
        "Streamlit Cloud의 Settings → Secrets에 "
        "NEIS_API_KEY를 등록해주세요."
    )
    st.stop()

API_KEY = st.secrets["NEIS_API_KEY"]

# 날짜 선택
selected_date = st.date_input(
    "📅 급식 날짜를 선택하세요",
    value=date.today(),
    format="YYYY-MM-DD"
)

# 조회 버튼
if st.button("🍚 급식 조회", use_container_width=True):

    meals, error = get_meal(API_KEY, selected_date)

    if error:
        st.warning(error)

    else:
        st.success(
            f"{selected_date.strftime('%Y년 %m월 %d일')} 급식입니다!"
        )

        for meal in meals:

            meal_type = meal.get("MMEAL_SC_NM", "급식")
            menu = meal.get("DDISH_NM", "")
            calories = meal.get("CAL_INFO", "")
            nutrition = meal.get("NTR_INFO", "")
            origin = meal.get("ORPLC_INFO", "")

            # HTML 태그 제거
            menu = menu.replace("<br/>", "\n")
            menu = menu.replace("<br>", "\n")

            st.subheader(f"🍽️ {meal_type}")

            # 메뉴
            st.markdown("### 메뉴")

            menu_items = [
                item.strip()
                for item in menu.split("\n")
                if item.strip()
            ]

            for item in menu_items:
                st.write(f"• {item}")

            # 칼로리
            if calories:
                st.info(f"🔥 칼로리: {calories}")

            # 영양정보
            if nutrition:
                with st.expander("🥗 영양정보"):
                    st.write(nutrition)

            # 원산지
            if origin:
                with st.expander("🌾 원산지 정보"):
                    st.write(origin)

            st.divider()


# -----------------------------
# 빠른 날짜 이동
# -----------------------------
st.markdown("### 📆 빠른 날짜")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("어제", use_container_width=True):
        st.session_state["selected_date"] = (
            selected_date - timedelta(days=1)
        )

with col2:
    if st.button("오늘", use_container_width=True):
        st.session_state["selected_date"] = date.today()

with col3:
    if st.button("내일", use_container_width=True):
        st.session_state["selected_date"] = (
            selected_date + timedelta(days=1)
        )

st.caption(
    "※ 급식 정보는 NEIS 교육정보 개방 포털에서 제공하는 데이터를 사용합니다."
)
