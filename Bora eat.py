import streamlit as st
import requests
from datetime import date, timedelta

# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="보라고등학교 급식 메뉴",
    page_icon="🍚",
    layout="centered"
)

# NEIS 학교 정보
ATPT_OFCDC_SC_CODE = "J10"   # 경기도교육청
SD_SCHUL_CODE = "7530882"    # 보라고등학교

# Streamlit Secrets에서 API KEY 가져오기
API_KEY = st.secrets["OPEN_API_KEY"]

BASE_URL = "https://open.neis.go.kr/hub/mealServiceDietInfo"


# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f7f8fa;
}

.title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 25px;
}

.meal-card {
    background-color: white;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.meal-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 12px;
}

.menu-item {
    padding: 5px 0;
    font-size: 17px;
}

.info-box {
    background-color: #f1f3f5;
    border-radius: 12px;
    padding: 12px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# API 요청 함수
# ==========================================

@st.cache_data(ttl=300)
def get_meal_data(start_date, end_date):

    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
        "SD_SCHUL_CODE": SD_SCHUL_CODE,
        "MLSV_FROM_YMD": start_date,
        "MLSV_TO_YMD": end_date
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if "mealServiceDietInfo" not in data:
            return []

        rows = data["mealServiceDietInfo"][1]["row"]

        return rows

    except requests.exceptions.RequestException:
        return None

    except (KeyError, IndexError, TypeError):
        return []


# ==========================================
# 메뉴 정리
# ==========================================

def clean_menu(menu):

    if not menu:
        return []

    # <br/>를 줄바꿈으로 변환
    menu = menu.replace("<br/>", "\n")
    menu = menu.replace("<br>", "\n")

    result = []

    for item in menu.split("\n"):

        item = item.strip()

        if item:
            result.append(item)

    return result


# ==========================================
# 날짜 표시
# ==========================================

def format_date(date_string):

    d = date(
        int(date_string[:4]),
        int(date_string[4:6]),
        int(date_string[6:8])
    )

    weekdays = [
        "월요일",
        "화요일",
        "수요일",
        "목요일",
        "금요일",
        "토요일",
        "일요일"
    ]

    return f"{d.month}월 {d.day}일 ({weekdays[d.weekday()]})"


# ==========================================
# 급식 표시
# ==========================================

def display_meal(meal):

    meal_name = meal.get("MMEAL_SC_NM", "급식")
    menu = clean_menu(meal.get("DDISH_NM", ""))

    calories = meal.get("CAL_INFO", "")
    nutrition = meal.get("NTR_INFO", "")
    origin = meal.get("ORPLC_INFO", "")

    st.markdown(
        f"""
        <div class="meal-card">

        <div class="meal-title">
        🍱 {meal_name}
        </div>

        """,
        unsafe_allow_html=True
    )

    if menu:

        for item in menu:

            st.markdown(
                f"""
                <div class="menu-item">
                • {item}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info("등록된 급식 메뉴가 없습니다.")

    if calories:

        st.markdown(
            f"""
            <div class="info-box">
            🔥 <b>열량</b> : {calories}
            </div>
            """,
            unsafe_allow_html=True
        )

    if nutrition:

        with st.expander("영양정보 보기"):

            nutrition_items = nutrition.split("<br/>")

            for item in nutrition_items:

                if item.strip():
                    st.write(item)

    if origin:

        with st.expander("원산지 정보 보기"):

            origin_items = origin.split("<br/>")

            for item in origin_items:

                if item.strip():
                    st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 제목
# ==========================================

st.markdown(
    '<div class="title">🍚 보라고등학교 급식 메뉴</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">NEIS 학교급식정보를 이용한 급식 조회 서비스</div>',
    unsafe_allow_html=True
)


# ==========================================
# 탭
# ==========================================

tab1, tab2 = st.tabs(
    ["📅 날짜별 급식", "🗓️ 주간 급식표"]
)


# ==========================================
# 날짜별 급식
# ==========================================

with tab1:

    selected_date = st.date_input(
        "급식 날짜를 선택하세요",
        value=date.today(),
        format="YYYY-MM-DD"
    )

    date_string = selected_date.strftime("%Y%m%d")

    if st.button(
        "🍚 급식 조회",
        use_container_width=True
    ):

        meals = get_meal_data(
            date_string,
            date_string
        )

        if meals is None:

            st.error(
                "NEIS API에 연결하지 못했습니다. "
                "잠시 후 다시 시도해주세요."
            )

        elif len(meals) == 0:

            st.warning(
                f"{selected_date.strftime('%Y년 %m월 %d일')}에는 "
                "등록된 급식 정보가 없습니다."
            )

        else:

            st.subheader(
                f"📅 {selected_date.strftime('%Y년 %m월 %d일')}"
            )

            for meal in meals:

                display_meal(meal)


# ==========================================
# 주간 급식표
# ==========================================

with tab2:

    today = date.today()

    monday = today - timedelta(
        days=today.weekday()
    )

    week_start = st.date_input(
        "주간 급식 시작일",
        value=monday,
        format="YYYY-MM-DD"
    )

    week_end = week_start + timedelta(days=6)

    if st.button(
        "🗓️ 주간 급식 조회",
        use_container_width=True
    ):

        start_string = week_start.strftime("%Y%m%d")
        end_string = week_end.strftime("%Y%m%d")

        meals = get_meal_data(
            start_string,
            end_string
        )

        if meals is None:

            st.error(
                "NEIS API에 연결하지 못했습니다."
            )

        elif len(meals) == 0:

            st.warning(
                "해당 기간에 등록된 급식 정보가 없습니다."
            )

        else:

            # 날짜별로 묶기
            meals_by_date = {}

            for meal in meals:

                meal_date = meal.get(
                    "MLSV_YMD",
                    ""
                )

                if meal_date not in meals_by_date:

                    meals_by_date[meal_date] = []

                meals_by_date[meal_date].append(meal)

            current_date = week_start

            while current_date <= week_end:

                date_string = current_date.strftime("%Y%m%d")

                st.markdown(
                    f"### 📅 {format_date(date_string)}"
                )

                if date_string in meals_by_date:

                    for meal in meals_by_date[date_string]:

                        display_meal(meal)

                else:

                    st.info("등록된 급식 정보가 없습니다.")

                current_date += timedelta(days=1)


# ==========================================
# 하단
# ==========================================

st.divider()

st.caption(
    "본 서비스는 NEIS 교육정보 개방 포털의 "
    "학교급식정보 Open API를 이용합니다."
)
