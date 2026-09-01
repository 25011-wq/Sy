import streamlit as st
import time
import random
from pathlib import Path

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="몬치치 돌보기",
    page_icon="🐒",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

html, body, [class*="css"] {
    font-family: 'Jua', sans-serif;
}

.stApp {
    background: #fff1f5;
}

.block-container {
    max-width: 700px;
    padding-top: 25px;
}

/* 제목 */

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #68452f;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #a47777;
    margin-bottom: 25px;
}

/* 캐릭터 영역 */

.character-box {
    background: #ffe1e9;
    border: 4px solid #efbdca;
    border-radius: 30px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 7px 0 #e5b2bf;
    margin-bottom: 25px;
}

/* 상태 */

.status-box {
    background: white;
    border: 3px solid #f0cbd4;
    border-radius: 25px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 5px 0 #e8c3ca;
}

/* 버튼 */

.stButton > button {
    width: 100%;
    height: 58px;

    border-radius: 18px;

    border: 2px solid #e7b8c5;

    background-color: white;

    color: #68452f;

    font-size: 18px;

    margin-bottom: 8px;
}

.stButton > button:hover {
    background-color: #ffe1e9;
}

/* 기록 */

.log {
    background: #fff7f9;

    border: 1px solid #f1d5dc;

    border-radius: 15px;

    padding: 10px;

    margin-top: 6px;

    color: #705858;
}

/* 단계 */

.badge {
    display: inline-block;

    background: #ffd5e1;

    color: #68452f;

    border-radius: 20px;

    padding: 7px 16px;

    font-size: 17px;

    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 게임 초기값
# =========================================================

if "hunger" not in st.session_state:
    st.session_state.hunger = 80

if "happiness" not in st.session_state:
    st.session_state.happiness = 80

if "energy" not in st.session_state:
    st.session_state.energy = 80

if "clean" not in st.session_state:
    st.session_state.clean = 80

if "health" not in st.session_state:
    st.session_state.health = 100

if "coin" not in st.session_state:
    st.session_state.coin = 20

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "age" not in st.session_state:
    st.session_state.age = 1

if "sleeping" not in st.session_state:
    st.session_state.sleeping = False

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

if "logs" not in st.session_state:
    st.session_state.logs = [
        "🌸 몬치치가 태어났어요!",
        "💗 몬치치를 잘 돌봐주세요!"
    ]


# =========================================================
# 공통 함수
# =========================================================

def limit(value):
    return max(0, min(100, int(value)))


def add_log(text):

    st.session_state.logs.insert(0, text)

    st.session_state.logs = st.session_state.logs[:6]


def get_stage():

    xp = st.session_state.xp

    if xp < 30:
        return "아기 몬치치", "🐣"

    elif xp < 80:
        return "어린이 몬치치", "🌱"

    elif xp < 160:
        return "청소년 몬치치", "⭐"

    else:
        return "어른 몬치치", "👑"


# =========================================================
# 시간 경과
# =========================================================

def update_time():

    now = time.time()

    elapsed = now - st.session_state.last_update

    if elapsed < 10:
        return

    count = int(elapsed // 10)

    st.session_state.last_update += count * 10

    # 자고 있는 경우
    if st.session_state.sleeping:

        st.session_state.energy = limit(
            st.session_state.energy + 4 * count
        )

        st.session_state.hunger = limit(
            st.session_state.hunger - 1 * count
        )

    # 깨어 있는 경우
    else:

        st.session_state.hunger = limit(
            st.session_state.hunger - 2 * count
        )

        st.session_state.happiness = limit(
            st.session_state.happiness - 1 * count
        )

        st.session_state.energy = limit(
            st.session_state.energy - 1 * count
        )

        st.session_state.clean = limit(
            st.session_state.clean - 1 * count
        )

    # 상태가 너무 낮으면 건강 감소

    bad = 0

    if st.session_state.hunger <= 10:
        bad += 1

    if st.session_state.happiness <= 10:
        bad += 1

    if st.session_state.clean <= 10:
        bad += 1

    if bad > 0:

        st.session_state.health = limit(
            st.session_state.health - bad
        )


# =========================================================
# 먹이기
# =========================================================

def feed():

    if st.session_state.coin < 2:

        add_log("🪙 코인이 부족해요!")

        return

    st.session_state.coin -= 2

    st.session_state.hunger = limit(
        st.session_state.hunger + 20
    )

    st.session_state.happiness = limit(
        st.session_state.happiness + 5
    )

    st.session_state.xp += 2

    add_log(
        "🍌 몬치치가 바나나를 맛있게 먹었어요!"
    )


# =========================================================
# 놀아주기
# =========================================================

def play():

    if st.session_state.energy < 15:

        add_log(
            "😴 몬치치가 너무 피곤해요!"
        )

        return

    st.session_state.energy = limit(
        st.session_state.energy - 15
    )

    st.session_state.happiness = limit(
        st.session_state.happiness + 20
    )

    st.session_state.hunger = limit(
        st.session_state.hunger - 5
    )

    st.session_state.coin += 3

    st.session_state.xp += 7

    add_log(
        "🎮 몬치치와 신나게 놀았어요! 🪙 +3"
    )


# =========================================================
# 목욕
# =========================================================

def bath():

    st.session_state.clean = limit(
        st.session_state.clean + 30
    )

    st.session_state.happiness = limit(
        st.session_state.happiness + 5
    )

    st.session_state.xp += 3

    add_log(
        "🛁 몬치치를 깨끗하게 씻겨줬어요!"
    )


# =========================================================
# 쓰다듬기
# =========================================================

def pet():

    st.session_state.happiness = limit(
        st.session_state.happiness + 10
    )

    st.session_state.xp += 1

    add_log(
        "💗 몬치치를 쓰담쓰담했어요!"
    )


# =========================================================
# 잠자기
# =========================================================

def sleep():

    if st.session_state.sleeping:

        st.session_state.sleeping = False

        add_log(
            "☀️ 몬치치가 일어났어요!"
        )

    else:

        st.session_state.sleeping = True

        add_log(
            "💤 몬치치가 잠들었어요..."
        )


# =========================================================
# 랜덤 이벤트
# =========================================================

def random_event():

    if random.random() < 0.05:

        event = random.choice([
            "🌸 몬치치가 예쁜 꽃을 발견했어요!",
            "🍀 행운이 찾아왔어요! 🪙 +5",
            "💗 몬치치가 갑자기 행복해졌어요!",
            "🐒 몬치치가 혼자 신나게 놀았어요!"
        ])

        if "🪙" in event:

            st.session_state.coin += 5

        if "행복" in event:

            st.session_state.happiness = limit(
                st.session_state.happiness + 10
            )

        add_log(event)


# =========================================================
# 시간 업데이트
# =========================================================

update_time()

random_event()


# =========================================================
# 현재 성장 단계
# =========================================================

stage_name, stage_icon = get_stage()


# =========================================================
# 제목
# =========================================================

st.markdown(
    '<div class="title">🐒 몬치치 돌보기</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '나만의 몬치치를 정성껏 키워보세요 💗'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 캐릭터
# =========================================================

st.markdown(
    '<div class="character-box">',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="badge">'
    f'{stage_icon} {stage_name}'
    f'</div>',
    unsafe_allow_html=True
)


# =========================================================
# ★★★★★ 중요 ★★★★★
# 네가 알려준 이미지 경로
# =========================================================

image_path = (
    Path(__file__).parent
    / "assets"
    / "CE442387-F366-4FB2-A0B6-11704E0A474A.png"
)


if image_path.exists():

    st.image(
        str(image_path),
        width=350
    )

else:

    st.error(
        "캐릭터 이미지를 찾을 수 없습니다."
    )

    st.code(
        "assets/CE442387-F366-4FB2-A0B6-11704E0A474A.png"
    )


# =========================================================
# 상태 메시지
# =========================================================

if st.session_state.sleeping:

    st.markdown(
        "💤 **Zzz... 몬치치가 곤히 자고 있어요!**"
    )

elif st.session_state.hunger <= 20:

    st.markdown(
        "🥺 **몬치치가 배고파하고 있어요...**"
    )

elif st.session_state.energy <= 20:

    st.markdown(
        "😴 **몬치치가 피곤해하고 있어요...**"
    )

elif st.session_state.happiness >= 80:

    st.markdown(
        "💗 **몬치치가 정말 행복해 보여요!**"
    )

else:

    st.markdown(
        "🐒 **몬치치가 당신을 바라보고 있어요!**"
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 정보
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🎂 나이",
        f"{st.session_state.age}일"
    )

with col2:

    st.metric(
        "🪙 코인",
        st.session_state.coin
    )

with col3:

    st.metric(
        "⭐ XP",
        st.session_state.xp
    )


# =========================================================
# 상태창
# =========================================================

st.markdown(
    '<div class="status-box">',
    unsafe_allow_html=True
)

st.subheader("📊 몬치치 상태")


st.write(
    f"🍌 배고픔   {st.session_state.hunger}%"
)

st.progress(
    st.session_state.hunger / 100
)


st.write(
    f"💗 행복   {st.session_state.happiness}%"
)

st.progress(
    st.session_state.happiness / 100
)


st.write(
    f"⚡ 에너지   {st.session_state.energy}%"
)

st.progress(
    st.session_state.energy / 100
)


st.write(
    f"🫧 청결   {st.session_state.clean}%"
)

st.progress(
    st.session_state.clean / 100
)


st.write(
    f"❤️ 건강   {st.session_state.health}%"
)

st.progress(
    st.session_state.health / 100
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 돌보기
# =========================================================

st.markdown(
    '<div class="status-box">',
    unsafe_allow_html=True
)

st.subheader("💗 몬치치 돌보기")


col1, col2 = st.columns(2)


with col1:

    if st.button(
        "🍌 먹이기",
        use_container_width=True
    ):

        feed()

        st.rerun()


    if st.button(
        "🎮 놀아주기",
        use_container_width=True
    ):

        play()

        st.rerun()


    if st.button(
        "🛁 목욕시키기",
        use_container_width=True
    ):

        bath()

        st.rerun()


with col2:

    if st.button(
        "💗 쓰다듬기",
        use_container_width=True
    ):

        pet()

        st.rerun()


    if st.button(
        "💤 재우기 / 깨우기",
        use_container_width=True
    ):

        sleep()

        st.rerun()


    if st.button(
        "🎁 선물 상자",
        use_container_width=True
    ):

        if st.session_state.coin >= 5:

            st.session_state.coin -= 5

            reward = random.choice([
                "🌸 예쁜 꽃을 얻었어요!",
                "🍌 맛있는 바나나를 얻었어요!",
                "💗 몬치치의 행복도가 올랐어요!",
                "🪙 코인 10개를 찾았어요!"
            ])

            if "행복" in reward:

                st.session_state.happiness = limit(
                    st.session_state.happiness + 15
                )

            elif "🪙" in reward:

                st.session_state.coin += 10

            add_log(
                "🎁 " + reward
            )

        else:

            add_log(
                "🪙 선물 상자를 열려면 "
                "코인 5개가 필요해요!"
            )

        st.rerun()


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 성장 시스템
# =========================================================

st.markdown(
    '<div class="status-box">',
    unsafe_allow_html=True
)

st.subheader("🌱 성장")


if st.session_state.xp < 30:

    remaining = 30 - st.session_state.xp

    st.write(
        f"🐣 어린이 몬치치까지 "
        f"**{remaining} XP** 남았어요!"
    )

    st.progress(
        st.session_state.xp / 30
    )


elif st.session_state.xp < 80:

    remaining = 80 - st.session_state.xp

    st.write(
        f"🌱 청소년 몬치치까지 "
        f"**{remaining} XP** 남았어요!"
    )

    st.progress(
        (st.session_state.xp - 30) / 50
    )


elif st.session_state.xp < 160:

    remaining = 160 - st.session_state.xp

    st.write(
        f"⭐ 어른 몬치치까지 "
        f"**{remaining} XP** 남았어요!"
    )

    st.progress(
        (st.session_state.xp - 80) / 80
    )


else:

    st.success(
        "👑 몬치치가 최종 성장 단계에 도달했어요!"
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 최근 기록
# =========================================================

st.markdown(
    '<div class="status-box">',
    unsafe_allow_html=True
)

st.subheader("📖 최근 기록")


for log in st.session_state.logs:

    st.markdown(
        f'<div class="log">{log}</div>',
        unsafe_allow_html=True
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 게임 설명
# =========================================================

with st.expander("📚 게임 방법"):

    st.write("""
### 🐒 몬치치 돌보기 게임

🍌 **먹이기**
- 배고픔 증가
- 행복 증가
- 코인 2개 사용

🎮 **놀아주기**
- 행복 증가
- XP 증가
- 코인 획득
- 에너지 감소

🛁 **목욕시키기**
- 청결 증가
- 행복 증가

💗 **쓰다듬기**
- 행복 증가
- XP 증가

💤 **재우기**
- 시간이 지나면 에너지 회복

🎁 **선물 상자**
- 코인 5개 사용
- 랜덤 보상

⭐ **성장**
- XP를 모으면 몬치치가 성장해요!

⏰ **시간**
- 시간이 지나면 배고픔, 행복, 에너지, 청결이 조금씩 감소해요.
""")


# =========================================================
# 자동 업데이트
# =========================================================

st.markdown("""
<script>

setTimeout(
    function() {
        window.parent.location.reload();
    },
    10000
);

</script>
""", unsafe_allow_html=True)
