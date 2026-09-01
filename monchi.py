import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="몬치치 키우기",
    page_icon="🐒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 이미지 불러오기
# =========================================================

BASE_DIR = Path(__file__).parent

BACKGROUND = (
    BASE_DIR
    / "assets"
    / "735A6F89-95B8-4CEA-80A2-E41C041B582E.png"
)

CHARACTER = (
    BASE_DIR
    / "assets"
    / "CE442387-F366-4FB2-A0B6-11704E0A474A.png"
)


def image_to_base64(path):

    if not path.exists():
        return ""

    data = path.read_bytes()

    return base64.b64encode(data).decode("utf-8")


background_data = image_to_base64(BACKGROUND)
character_data = image_to_base64(CHARACTER)


# =========================================================
# 이미지 오류 확인
# =========================================================

if not background_data:

    st.error(
        "방 배경 이미지를 찾을 수 없습니다.\n\n"
        "assets/735A6F89-95B8-4CEA-80A2-E41C041B582E.png"
    )

    st.stop()


if not character_data:

    st.error(
        "몬치치 캐릭터 이미지를 찾을 수 없습니다.\n\n"
        "assets/CE442387-F366-4FB2-A0B6-11704E0A474A.png"
    )

    st.stop()


# =========================================================
# 게임 HTML
# =========================================================

html = f"""
<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1.0,
maximum-scale=1.0,
user-scalable=no">

<style>

/* =====================================================
   기본
===================================================== */

* {{
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}}

body {{
    margin: 0;
    padding: 0;

    background: #fff0f5;

    font-family:
        Arial,
        sans-serif;

    overflow-x: hidden;
}}


/* =====================================================
   게임 전체
===================================================== */

.game {{
    width: 100%;
    max-width: 1000px;

    margin: auto;

    position: relative;
}}


/* =====================================================
   제목
===================================================== */

.title {{
    text-align: center;

    font-size: clamp(25px, 5vw, 42px);

    font-weight: 900;

    color: #69462f;

    padding: 12px 0 5px;
}}

.subtitle {{
    text-align: center;

    color: #a36f77;

    font-size: 14px;

    margin-bottom: 10px;
}}


/* =====================================================
   상단 상태
===================================================== */

.top {{
    display: flex;

    justify-content: space-between;

    gap: 7px;

    margin: 0 8px 10px;
}}

.info {{
    background: white;

    border: 2px solid #efc4cf;

    border-radius: 15px;

    padding: 7px 10px;

    text-align: center;

    flex: 1;

    color: #69462f;

    font-size: 13px;

    box-shadow: 0 3px 0 #e8bbc6;
}}

.info strong {{
    display: block;

    font-size: 17px;
}}


/* =====================================================
   방
===================================================== */

.room {{
    position: relative;

    width: 100%;

    aspect-ratio: 16 / 9;

    overflow: hidden;

    border-radius: 22px;

    border: 4px solid #e5b3c0;

    box-shadow:
        0 7px 0 #dcaab7,
        0 12px 25px rgba(120,70,80,0.15);

    background-image:
        url("data:image/png;base64,{background_data}");

    background-size: cover;

    background-position: center;
}}


/* =====================================================
   캐릭터
===================================================== */

.character {{
    position: absolute;

    width: 25%;

    left: 50%;

    bottom: 5%;

    transform:
        translateX(-50%);

    z-index: 10;

    pointer-events: none;

    transition:
        transform .3s ease;
}}

.character img {{
    width: 100%;

    height: auto;

    display: block;

    filter:
        drop-shadow(0 5px 3px rgba(70,40,20,.2));
}}


/* =====================================================
   캐릭터 기본 움직임
===================================================== */

.bounce {{
    animation:
        bounce .55s ease;
}}

@keyframes bounce {{

    0% {{
        transform:
            translateX(-50%)
            translateY(0);
    }}

    30% {{
        transform:
            translateX(-50%)
            translateY(-18px);
    }}

    60% {{
        transform:
            translateX(-50%)
            translateY(0);
    }}

    80% {{
        transform:
            translateX(-50%)
            translateY(-7px);
    }}

    100% {{
        transform:
            translateX(-50%)
            translateY(0);
    }}

}}


/* =====================================================
   잠자기
===================================================== */

.sleeping {{
    animation:
        sleepMove 2s ease-in-out infinite;
}}

@keyframes sleepMove {{

    0%,100% {{
        transform:
            translateX(-50%)
            translateY(0)
            rotate(-2deg);
    }}

    50% {{
        transform:
            translateX(-50%)
            translateY(5px)
            rotate(2deg);
    }}

}}


/* =====================================================
   터치 가능한 아이템
===================================================== */

.item {{
    position: absolute;

    z-index: 20;

    cursor: pointer;

    border-radius: 20px;

    transition:
        transform .15s ease;
}}

.item:active {{
    transform: scale(.85);
}}


/* =====================================================
   아이템 터치 안내
===================================================== */

.item::after {{

    content: "";

    position: absolute;

    inset: -5px;

    border-radius: 20px;

    border: 2px dashed rgba(255,120,150,.0);

    transition: .2s;

}}

.item:hover::after {{

    border-color:
        rgba(255,120,150,.7);

}}


/* =====================================================
   아이템 위치
===================================================== */

/*
   배경 이미지에 맞춰 터치 영역을 배치
*/

/* 🍌 바나나 */

.banana {{
    width: 13%;

    height: 18%;

    right: 12%;

    bottom: 7%;
}}


/* 🛏️ 침대 */

.bed {{
    width: 28%;

    height: 35%;

    left: 2%;

    bottom: 24%;
}}


/* 💗 쿠션 */

.cushion {{
    width: 17%;

    height: 20%;

    right: 3%;

    bottom: 4%;
}}


/* 🛁 목욕 */

.bath {{
    width: 17%;

    height: 25%;

    left: 29%;

    bottom: 15%;
}}


/* 📚 책장 */

.books {{
    width: 20%;

    height: 40%;

    right: 2%;

    top: 25%;
}}


/* =====================================================
   효과
===================================================== */

.effect {{
    position: absolute;

    pointer-events: none;

    z-index: 50;

    font-weight: bold;

    animation:
        effectUp 1s ease forwards;
}}

@keyframes effectUp {{

    0% {{
        opacity: 0;

        transform:
            translateY(15px)
            scale(.5);
    }}

    25% {{
        opacity: 1;

        transform:
            translateY(0)
            scale(1.2);
    }}

    100% {{
        opacity: 0;

        transform:
            translateY(-65px)
            scale(1);
    }}

}}


/* =====================================================
   바나나 날아가기
===================================================== */

.flying-banana {{
    position: absolute;

    z-index: 60;

    font-size: 30px;

    animation:
        bananaFly 1s ease forwards;
}}

@keyframes bananaFly {{

    0% {{
        right: 13%;
        bottom: 12%;
        opacity: 1;
    }}

    100% {{
        right: 48%;
        bottom: 45%;
        opacity: 0;
        transform: rotate(-360deg) scale(.6);
    }}

}}


/* =====================================================
   하트
===================================================== */

.heart {{
    position: absolute;

    font-size: 25px;

    z-index: 55;

    animation:
        heartUp 1.2s ease forwards;
}}

@keyframes heartUp {{

    0% {{
        opacity: 0;

        transform:
            translateY(10px)
            scale(.5);
    }}

    30% {{
        opacity: 1;

        transform:
            translateY(0)
            scale(1.2);
    }}

    100% {{
        opacity: 0;

        transform:
            translateY(-80px)
            scale(.8);
    }}

}}


/* =====================================================
   비눗방울
===================================================== */

.bubble {{
    position: absolute;

    z-index: 55;

    font-size: 22px;

    animation:
        bubbleUp 1.5s ease forwards;
}}

@keyframes bubbleUp {{

    0% {{
        opacity: 0;

        transform:
            translateY(20px)
            scale(.4);
    }}

    30% {{
        opacity: 1;
    }}

    100% {{
        opacity: 0;

        transform:
            translateY(-100px)
            scale(1.4);
    }}

}}


/* =====================================================
   별
===================================================== */

.star {{
    position: absolute;

    z-index: 55;

    font-size: 25px;

    animation:
        starPop 1s ease forwards;
}}

@keyframes starPop {{

    0% {{
        opacity: 0;

        transform: scale(.2);
    }}

    40% {{
        opacity: 1;

        transform: scale(1.4)
        rotate(15deg);
    }}

    100% {{
        opacity: 0;

        transform:
            translateY(-60px)
            scale(.7)
            rotate(45deg);
    }}

}}


/* =====================================================
   ZZZ
===================================================== */

.zzz {{
    position: absolute;

    left: 54%;

    bottom: 55%;

    z-index: 70;

    font-size: 25px;

    color: #68452f;

    font-weight: bold;

    animation:
        zzzMove 2s ease-in-out infinite;
}}

@keyframes zzzMove {{

    0% {{
        opacity: 0;

        transform:
            translate(0,10px);
    }}

    50% {{
        opacity: 1;

        transform:
            translate(20px,-15px);
    }}

    100% {{
        opacity: 0;

        transform:
            translate(40px,-35px);
    }}

}}


/* =====================================================
   행동 메시지
===================================================== */

.message {{

    position: absolute;

    left: 50%;

    top: 5%;

    transform:
        translateX(-50%);

    z-index: 80;

    background: white;

    border: 3px solid #efc2ce;

    border-radius: 20px;

    padding: 9px 15px;

    color: #68452f;

    font-size: 15px;

    white-space: nowrap;

    box-shadow:
        0 4px 0 #e4b5c0;

    animation:
        messageShow 2s ease forwards;

}}

@keyframes messageShow {{

    0% {{
        opacity: 0;

        transform:
            translateX(-50%)
            translateY(10px);
    }}

    15%,75% {{
        opacity: 1;

        transform:
            translateX(-50%)
            translateY(0);
    }}

    100% {{
        opacity: 0;
    }}

}}


/* =====================================================
   상태창
===================================================== */

.status {{
    background: white;

    border: 3px solid #efc5d0;

    border-radius: 22px;

    margin-top: 12px;

    padding: 15px;

    box-shadow:
        0 5px 0 #e5b8c3;
}}

.stat {{
    margin-bottom: 10px;
}}

.stat:last-child {{
    margin-bottom: 0;
}}

.stat-title {{
    display: flex;

    justify-content:
        space-between;

    color: #68452f;

    font-size: 14px;

    margin-bottom: 4px;
}}

.bar {{
    height: 15px;

    background: #f4e4e8;

    border-radius: 20px;

    overflow: hidden;
}}

.fill {{
    height: 100%;

    width: 80%;

    border-radius: 20px;

    transition:
        width .4s ease;
}}

.hunger {{
    background: #f2bd65;
}}

.happy {{
    background: #ef8eaf;
}}

.energy {{
    background: #91bfe9;
}}

.clean {{
    background: #8ed4c0;
}}


/* =====================================================
   안내
===================================================== */

.tip {{
    text-align: center;

    color: #a47777;

    font-size: 13px;

    padding: 12px 5px 20px;
}}


/* 모바일
===================================================== */

@media(max-width:600px) {{

    .room {{
        border-radius: 15px;

        border-width: 3px;
    }}

    .title {{
        font-size: 30px;
    }}

    .subtitle {{
        font-size: 13px;
    }}

    .info {{
        font-size: 11px;

        padding: 5px;
    }}

    .info strong {{
        font-size: 14px;
    }}

    .character {{
        width: 27%;
    }}

    .message {{
        font-size: 12px;

        padding: 7px 11px;
    }}

}}


</style>

</head>


<body>


<div class="game">


<div class="title">
🐒 몬치치 키우기
</div>


<div class="subtitle">
방 안의 아이템을 직접 터치해서 몬치치를 돌봐주세요! 💗
</div>


<!-- ===================================================
     상단 정보
=================================================== -->

<div class="top">

    <div class="info">
        🎂
        <strong id="age">1일</strong>
        나이
    </div>

    <div class="info">
        🪙
        <strong id="coin">20</strong>
        코인
    </div>

    <div class="info">
        ⭐
        <strong id="xp">0</strong>
        XP
    </div>

</div>


<!-- ===================================================
     방
=================================================== -->

<div class="room" id="room">


<!-- 행동 메시지 -->

<div id="messageContainer"></div>


<!-- 몬치치 -->

<div
    class="character"
    id="character"
>

<img
    src="data:image/png;base64,{character_data}"
>

</div>


<!-- =================================================
     터치 아이템
================================================= -->


<!-- 🍌 바나나 -->

<div
    class="item banana"
    onclick="feed()"
    title="먹이기"
></div>


<!-- 🛏️ 침대 -->

<div
    class="item bed"
    onclick="sleepPet()"
    title="재우기"
></div>


<!-- 💗 쿠션 -->

<div
    class="item cushion"
    onclick="pet()"
    title="쓰다듬기"
></div>


<!-- 🫧 목욕 -->

<div
    class="item bath"
    onclick="bath()"
    title="씻기기"
></div>


<!-- 📚 책장 -->

<div
    class="item books"
    onclick="play()"
    title="놀아주기"
></div>


</div>


<!-- ===================================================
     상태
=================================================== -->

<div class="status">


<div class="stat">

    <div class="stat-title">

        <span>🍌 배고픔</span>

        <span id="hungerText">
            80%
        </span>

    </div>

    <div class="bar">

        <div
            class="fill hunger"
            id="hungerBar"
            style="width:80%"
        ></div>

    </div>

</div>


<div class="stat">

    <div class="stat-title">

        <span>💗 행복</span>

        <span id="happyText">
            80%
        </span>

    </div>

    <div class="bar">

        <div
            class="fill happy"
            id="happyBar"
            style="width:80%"
        ></div>

    </div>

</div>


<div class="stat">

    <div class="stat-title">

        <span>⚡ 에너지</span>

        <span id="energyText">
            80%
        </span>

    </div>

    <div class="bar">

        <div
            class="fill energy"
            id="energyBar"
            style="width:80%"
        ></div>

    </div>

</div>


<div class="stat">

    <div class="stat-title">

        <span>🫧 청결</span>

        <span id="cleanText">
            80%
        </span>

    </div>

    <div class="bar">

        <div
            class="fill clean"
            id="cleanBar"
            style="width:80%"
        ></div>

    </div>

</div>


</div>


<div class="tip">

💡 방 안의 물건을 눌러보세요!
<br>
🍌 바나나 = 먹이기　🛏️ 침대 = 재우기　🫧 목욕 = 씻기기　💗 쿠션 = 쓰다듬기　📚 책장 = 놀아주기

</div>


</div>


<script>

/* =====================================================
   게임 데이터
===================================================== */

let hunger = 80;

let happiness = 80;

let energy = 80;

let clean = 80;

let coin = 20;

let xp = 0;

let age = 1;

let sleeping = false;


/* =====================================================
   HTML 요소
===================================================== */

const character =
    document.getElementById("character");

const room =
    document.getElementById("room");


/* =====================================================
   숫자 제한
===================================================== */

function limit(value) {{

    return Math.max(
        0,
        Math.min(100, value)
    );

}}


/* =====================================================
   상태 업데이트
===================================================== */

function updateStats() {{

    document.getElementById(
        "hungerText"
    ).innerText =
        Math.round(hunger) + "%";


    document.getElementById(
        "happyText"
    ).innerText =
        Math.round(happiness) + "%";


    document.getElementById(
        "energyText"
    ).innerText =
        Math.round(energy) + "%";


    document.getElementById(
        "cleanText"
    ).innerText =
        Math.round(clean) + "%";


    document.getElementById(
        "hungerBar"
    ).style.width =
        hunger + "%";


    document.getElementById(
        "happyBar"
    ).style.width =
        happiness + "%";


    document.getElementById(
        "energyBar"
    ).style.width =
        energy + "%";


    document.getElementById(
        "cleanBar"
    ).style.width =
        clean + "%";


    document.getElementById(
        "coin"
    ).innerText =
        coin;


    document.getElementById(
        "xp"
    ).innerText =
        xp;


    document.getElementById(
        "age"
    ).innerText =
        age + "일";

}}


/* =====================================================
   메시지
===================================================== */

function message(text) {{

    const box =
        document.createElement("div");

    box.className =
        "message";

    box.innerText =
        text;

    document
        .getElementById(
            "messageContainer"
        )
        .appendChild(box);


    setTimeout(
        () => box.remove(),
        2100
    );

}}


/* =====================================================
   캐릭터 튕기기
===================================================== */

function bounce() {{

    character.classList.remove(
        "bounce"
    );

    void character.offsetWidth;

    character.classList.add(
        "bounce"
    );

}}


/* =====================================================
   하트 효과
===================================================== */

function heartEffect(count = 4) {{

    for(
        let i = 0;
        i < count;
        i++
    ) {{

        setTimeout(() => {{

            const heart =
                document.createElement(
                    "div"
                );

            heart.className =
                "heart";

            heart.innerText =
                Math.random() > .5
                ? "💗"
                : "💕";


            heart.style.left =
                (45 + Math.random() * 15)
                + "%";


            heart.style.bottom =
                (30 + Math.random() * 20)
                + "%";


            room.appendChild(
                heart
            );


            setTimeout(
                () => heart.remove(),
                1300
            );

        }}, i * 150);

    }}

}}


/* =====================================================
   별 효과
===================================================== */

function starEffect() {{

    for(
        let i = 0;
        i < 5;
        i++
    ) {{

        setTimeout(() => {{

            const star =
                document.createElement(
                    "div"
                );

            star.className =
                "star";

            star.innerText =
                "⭐";


            star.style.left =
                (42 + Math.random() * 20)
                + "%";


            star.style.bottom =
                (35 + Math.random() * 20)
                + "%";


            room.appendChild(
                star
            );


            setTimeout(
                () => star.remove(),
                1100
            );

        }}, i * 100);

    }}

}}


/* =====================================================
   비눗방울
===================================================== */

function bubbles() {{

    for(
        let i = 0;
        i < 8;
        i++
    ) {{

        setTimeout(() => {{

            const bubble =
                document.createElement(
                    "div"
                );

            bubble.className =
                "bubble";

            bubble.innerText =
                Math.random() > .5
                ? "🫧"
                : "○";


            bubble.style.left =
                (35 + Math.random() * 30)
                + "%";


            bubble.style.bottom =
                (30 + Math.random() * 15)
                + "%";


            room.appendChild(
                bubble
            );


            setTimeout(
                () => bubble.remove(),
                1600
            );

        }}, i * 120);

    }}

}}


/* =====================================================
   🍌 먹이기
===================================================== */

function feed() {{

    if(coin < 2) {{

        message(
            "🪙 코인이 부족해요!"
        );

        return;
    }}


    coin -= 2;

    hunger =
        limit(hunger + 20);

    happiness =
        limit(happiness + 5);

    xp += 2;


    /* 바나나 날아가기 */

    const banana =
        document.createElement(
            "div"
        );

    banana.className =
        "flying-banana";

    banana.innerText =
        "🍌";


    room.appendChild(
        banana
    );


    setTimeout(
        () => banana.remove(),
        1100
    );


    setTimeout(
        () => bounce(),
        650
    );


    message(
        "🍌 냠냠! 맛있다!"
    );


    heartEffect(2);


    updateStats();

}}


/* =====================================================
   🫧 씻기기
===================================================== */

function bath() {{

    clean =
        limit(clean + 30);

    happiness =
        limit(happiness + 5);

    xp += 3;


    bubbles();

    bounce();


    message(
        "🫧 뽀득뽀득 깨끗해졌어요!"
    );


    updateStats();

}}


/* =====================================================
   💗 쓰다듬기
===================================================== */

function pet() {{

    happiness =
        limit(happiness + 10);

    xp += 1;


    bounce();

    heartEffect(6);


    message(
        "💗 쓰담쓰담~ 기분이 좋아요!"
    );


    updateStats();

}}


/* =====================================================
   📚 놀아주기
===================================================== */

function play() {{

    if(energy < 15) {{

        message(
            "😴 너무 피곤해요..."
        );

        return;
    }}


    energy =
        limit(energy - 15);


    happiness =
        limit(happiness + 20);


    hunger =
        limit(hunger - 5);


    coin += 3;

    xp += 7;


    bounce();

    starEffect();

    heartEffect(3);


    message(
        "🎮 신나게 놀았어요! 🪙 +3"
    );


    updateStats();

}}


/* =====================================================
   💤 재우기
===================================================== */

function sleepPet() {{

    sleeping =
        !sleeping;


    if(sleeping) {{

        character.classList.add(
            "sleeping"
        );


        const zzz =
            document.createElement(
                "div"
            );

        zzz.className =
            "zzz";

        zzz.id =
            "zzz";

        zzz.innerText =
            "Zzz...";


        room.appendChild(
            zzz
        );


        message(
            "💤 몬치치가 잠들었어요..."
        );

    }}

    else {{

        character.classList.remove(
            "sleeping"
        );


        const zzz =
            document.getElementById(
                "zzz"
            );

        if(zzz) {{
            zzz.remove();
        }}


        message(
            "☀️ 몬치치가 일어났어요!"
        );

    }}

}}


/* =====================================================
   시간 흐름
===================================================== */

setInterval(() => {{

    if(sleeping) {{

        energy =
            limit(energy + 4);

        hunger =
            limit(hunger - 1);

    }}

    else {{

        hunger =
            limit(hunger - 1);

        happiness =
            limit(happiness - 0.5);

        energy =
            limit(energy - 0.5);

        clean =
            limit(clean - 0.5);

    }}


    updateStats();

}}, 10000);


/* =====================================================
   성장
===================================================== */

setInterval(() => {{

    if(xp >= 30 && age === 1) {{

        age = 2;

        message(
            "🌱 몬치치가 조금 자랐어요!"
        );

    }}


    if(xp >= 80 && age === 2) {{

        age = 3;

        message(
            "⭐ 몬치치가 더 성장했어요!"
        );

    }}


    if(xp >= 160 && age === 3) {{

        age = 4;

        message(
            "👑 몬치치가 완전히 성장했어요!"
        );

    }}


    updateStats();

}}, 1000);


/* =====================================================
   시작
===================================================== */

updateStats();

</script>

</body>

</html>
"""


# =========================================================
# Streamlit에 게임 표시
# =========================================================

components.html(
    html,
    height=850,
    scrolling=False
)
