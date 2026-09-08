import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64


# =========================================================
# STREAMLIT 설정
# =========================================================

st.set_page_config(
    page_title="몬치치 키우기",
    page_icon="🐒",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# 파일 경로
# =========================================================

BASE_DIR = Path(__file__).parent

BACKGROUND = (
    BASE_DIR
    / "assets"
    / "C3BCB046-F78D-4E61-97AE-D1A04EAD0F0F.png"
)

NORMAL = (
    BASE_DIR
    / "assets"
    / "CE442387-F366-4FB2-A0B6-11704E0A474A.png"
)

EATING = (
    BASE_DIR
    / "assets"
    / "837AA3CB-1CBB-4C2D-9EBA-8ED0B5A4D33D.png"
)

SLEEPING = (
    BASE_DIR
    / "assets"
    / "935DC2BF-D149-4B85-8C5C-B2BA02179A6F.png"
)

GAME_DEVICE = (
    BASE_DIR
    / "assets"
    / "IMG_8184.jpeg"
)


# =========================================================
# 이미지 → BASE64
# =========================================================

def get_base64(path):

    if not path.exists():
        return ""

    return base64.b64encode(
        path.read_bytes()
    ).decode("utf-8")


background_b64 = get_base64(BACKGROUND)
normal_b64 = get_base64(NORMAL)
eating_b64 = get_base64(EATING)
sleeping_b64 = get_base64(SLEEPING)
device_b64 = get_base64(GAME_DEVICE)


# =========================================================
# 파일 확인
# =========================================================

missing = []

if not background_b64:
    missing.append(
        "C3BCB046-F78D-4E61-97AE-D1A04EAD0F0F.png"
    )

if not normal_b64:
    missing.append(
        "CE442387-F366-4FB2-A0B6-11704E0A474A.png"
    )

if not eating_b64:
    missing.append(
        "837AA3CB-1CBB-4C2D-9EBA-8ED0B5A4D33D.png"
    )

if not sleeping_b64:
    missing.append(
        "935DC2BF-D149-4B85-8C5C-B2BA02179A6F.png"
    )

if not device_b64:
    missing.append(
        "IMG_8184.jpeg"
    )


if missing:

    st.error("다음 파일을 찾을 수 없습니다.")

    for f in missing:
        st.write(f)

    st.stop()


# =========================================================
# 게임 HTML
# =========================================================

html = f"""
<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width,
initial-scale=1.0,
maximum-scale=1.0,
user-scalable=no"
>

<style>

/* =====================================================
   전체
===================================================== */

* {{
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}}

body {{
    margin: 0;
    padding: 0;

    background: transparent;

    font-family:
        Arial,
        "Noto Sans KR",
        sans-serif;

    overflow: hidden;
}}


/* =====================================================
   게임기
===================================================== */

.device {{
    position: relative;

    width: 100%;

    max-width: 850px;

    margin: auto;
}}


.device-image {{
    display: block;

    width: 100%;

    height: auto;

    user-select: none;

    pointer-events: none;
}}


/* =====================================================
   ★ 게임기 흰색 화면 영역
===================================================== */

/*
   IMG_8184.jpeg의 흰색 화면 부분에 맞춘 영역.

   화면 위치가 사진마다 다르면
   아래 4개 숫자만 조절하면 됨.

   left   = 왼쪽 위치
   top    = 위쪽 위치
   width  = 화면 너비
   height = 화면 높이
*/

.screen {{
    position: absolute;

    left: 19%;

    top: 16%;

    width: 62%;

    height: 57%;

    overflow: hidden;

    border-radius: 8px;

    background: #fff1f4;

    box-shadow:
        inset 0 0 0 3px #f0c7d1,
        inset 0 0 15px rgba(100,60,60,.12);

    touch-action: manipulation;
}}


/* =====================================================
   실제 게임 화면
===================================================== */

.game {{
    position: absolute;

    inset: 0;

    width: 100%;

    height: 100%;

    overflow: hidden;

    background-image:
        url("data:image/png;base64,{background_b64}");

    background-size: cover;

    background-position: center;
}}


/* =====================================================
   상태 HUD
===================================================== */

.hud {{
    position: absolute;

    top: 2%;

    left: 2%;

    right: 2%;

    z-index: 100;

    display: flex;

    gap: 3px;

    flex-wrap: wrap;

    justify-content: center;
}}

.stat {{
    background: rgba(255,255,255,.94);

    border: 1.5px solid #dba7b5;

    border-radius: 7px;

    padding: 3px 5px;

    min-width: 17%;

    color: #65432e;

    font-size: clamp(7px, 1.25vw, 13px);

    text-align: center;

    box-shadow:
        0 2px 0 rgba(150,90,100,.15);
}}

.stat strong {{
    font-size: 1.15em;
}}


/* =====================================================
   캐릭터
===================================================== */

.character {{
    position: absolute;

    z-index: 30;

    width: 21%;

    left: 50%;

    bottom: 15%;

    transform:
        translateX(-50%);

    transition:
        left 1.15s cubic-bezier(.45,.05,.55,.95),
        bottom .35s ease;

    pointer-events: none;
}}

.character img {{
    width: 100%;

    height: auto;

    display: block;

    filter:
        drop-shadow(
            0 3px 2px
            rgba(60,40,20,.22)
        );
}}


/* =====================================================
   콩콩 뛰기
===================================================== */

.hop {{
    animation:
        hopping .42s ease-in-out
        infinite;
}}

@keyframes hopping {{

    0%,100% {{
        margin-bottom: 0;
    }}

    50% {{
        margin-bottom: 11px;
    }}
}}


/* =====================================================
   먹는 모션
===================================================== */

.eating {{
    animation:
        eatingMove .45s ease-in-out
        infinite;
}}

@keyframes eatingMove {{

    0%,100% {{
        transform:
            translateX(-50%)
            scale(1);
    }}

    50% {{
        transform:
            translateX(-50%)
            scale(1.06);
    }}
}}


/* =====================================================
   자는 모션
===================================================== */

.sleep {{
    animation:
        sleepMove 1.4s
        ease-in-out
        infinite;
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
            translateY(3px)
            rotate(2deg);
    }}
}}


/* =====================================================
   투명 터치 영역
===================================================== */

.hotspot {{
    position: absolute;

    z-index: 80;

    cursor: pointer;

    border-radius: 15px;

    touch-action: manipulation;
}}

.hotspot:active {{
    background:
        rgba(255,255,255,.18);
}}


/* =====================================================
   ★ 배경 아이템 위치
===================================================== */

/*
   아래 위치는 16:9 방 배경 기준.

   쿠키 / 침대 / 장난감 위치가 다르면
   이 숫자를 조절하면 됨.
*/


/* 🍪 쿠키 */

.cookie {{
    left: 13%;

    bottom: 13%;

    width: 18%;

    height: 17%;
}}


/* 🛏️ 침대 */

.bed {{
    left: 3%;

    bottom: 23%;

    width: 28%;

    height: 36%;
}}


/* 🧸 장난감 */

.toy {{
    right: 13%;

    bottom: 12%;

    width: 20%;

    height: 22%;
}}


/* 🛁 씻기 */

.wash {{
    left: 72%;

    top: 30%;

    width: 18%;

    height: 25%;
}}


/* =====================================================
   효과
===================================================== */

.effect {{
    position: absolute;

    z-index: 200;

    pointer-events: none;

    font-weight: bold;

    white-space: nowrap;

    animation:
        effectUp 1.3s
        ease-out
        forwards;
}}

@keyframes effectUp {{

    0% {{
        opacity: 0;

        transform:
            translateY(15px)
            scale(.5);
    }}

    20% {{
        opacity: 1;

        transform:
            translateY(0)
            scale(1.15);
    }}

    100% {{
        opacity: 0;

        transform:
            translateY(-45px)
            scale(1);
    }}
}}


/* =====================================================
   하트
===================================================== */

.heart {{
    position: absolute;

    z-index: 150;

    font-size: 20px;

    pointer-events: none;

    animation:
        heartFloat 1.4s
        ease-out
        forwards;
}}

@keyframes heartFloat {{

    0% {{
        opacity: 0;

        transform:
            translateY(10px)
            scale(.4);
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
            translateY(-55px)
            scale(.8);
    }}
}}


/* =====================================================
   비눗방울
===================================================== */

.bubble {{
    position: absolute;

    z-index: 150;

    pointer-events: none;

    font-size: 17px;

    animation:
        bubbleFloat 1.6s
        ease-out
        forwards;
}}

@keyframes bubbleFloat {{

    0% {{
        opacity: 0;

        transform:
            translateY(10px)
            scale(.3);
    }}

    30% {{
        opacity: 1;
    }}

    100% {{
        opacity: 0;

        transform:
            translateY(-65px)
            scale(1.2);
    }}
}}


/* =====================================================
   ZZZ
===================================================== */

.zzz {{
    position: absolute;

    z-index: 160;

    left: 57%;

    bottom: 43%;

    color: #69462f;

    font-weight: bold;

    font-size: 18px;

    animation:
        zzz 1.8s
        ease-in-out
        infinite;
}}

@keyframes zzz {{

    0% {{
        opacity: 0;

        transform:
            translate(0,10px);
    }}

    45% {{
        opacity: 1;
    }}

    100% {{
        opacity: 0;

        transform:
            translate(25px,-25px);
    }}
}}


/* =====================================================
   행동 말풍선
===================================================== */

.message {{
    position: absolute;

    z-index: 180;

    left: 50%;

    top: 18%;

    transform:
        translateX(-50%);

    background: white;

    color: #65432e;

    border: 2px solid #dfaab8;

    border-radius: 12px;

    padding: 4px 9px;

    font-size: clamp(8px, 1.4vw, 14px);

    white-space: nowrap;

    box-shadow:
        0 2px 0 rgba(130,70,80,.15);

    animation:
        message 2s
        ease forwards;
}}

@keyframes message {{

    0% {{
        opacity: 0;

        transform:
            translateX(-50%)
            translateY(7px);
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
   게임 버튼
===================================================== */

.buttons {{
    position: absolute;

    z-index: 120;

    left: 3%;

    right: 3%;

    bottom: 2%;

    display: flex;

    justify-content: center;

    gap: 3px;
}}

.game-button {{
    border: 1.5px solid #dca8b5;

    background:
        rgba(255,255,255,.96);

    color: #65432e;

    border-radius: 8px;

    padding: 4px 5px;

    font-size: clamp(7px, 1.2vw, 12px);

    font-weight: bold;

    box-shadow:
        0 2px 0 #dfbdc5;

    cursor: pointer;

    min-width: 18%;
}}

.game-button:active {{
    transform:
        translateY(2px);

    box-shadow: none;
}}


/* =====================================================
   모바일
===================================================== */

@media(max-width:600px) {{

    .screen {{
        border-radius: 5px;
    }}

    .character {{
        width: 23%;
    }}

    .game-button {{
        padding: 3px 2px;
    }}

}}

</style>

</head>


<body>


<!-- =====================================================
     게임기
===================================================== -->

<div class="device">


<img
    class="device-image"
    src="data:image/jpeg;base64,{device_b64}"
>


<!-- ===================================================
     게임 화면
=================================================== -->

<div class="screen">

<div class="game" id="game">


<!-- =================================================
     상태
================================================= -->

<div class="hud">

    <div class="stat">
        🍪
        <strong id="hunger">80</strong>
        %
    </div>

    <div class="stat">
        💗
        <strong id="happy">80</strong>
        %
    </div>

    <div class="stat">
        ⚡
        <strong id="energy">80</strong>
        %
    </div>

    <div class="stat">
        🫧
        <strong id="clean">80</strong>
        %
    </div>

    <div class="stat">
        ❤️
        <strong id="health">100</strong>
        %
    </div>

    <div class="stat">
        ⭐
        <strong id="xp">0</strong>
    </div>

</div>


<!-- =================================================
     캐릭터
================================================= -->

<div
    class="character"
    id="character"
>

<img
    id="characterImage"
    src="data:image/png;base64,{normal_b64}"
>

</div>


<!-- =================================================
     터치 영역
================================================= -->


<!-- 🍪 쿠키 -->

<div
    class="hotspot cookie"
    onclick="feed()"
    title="쿠키 먹이기"
></div>


<!-- 🛏️ 침대 -->

<div
    class="hotspot bed"
    onclick="sleepPet()"
    title="재우기"
></div>


<!-- 🧸 장난감 -->

<div
    class="hotspot toy"
    onclick="play()"
    title="놀아주기"
></div>


<!-- 🫧 씻기 -->

<div
    class="hotspot wash"
    onclick="wash()"
    title="씻기기"
></div>


<!-- =================================================
     효과
================================================= -->

<div id="effects"></div>


<!-- =================================================
     메시지
================================================= -->

<div id="messages"></div>


<!-- =================================================
     버튼
================================================= -->

<div class="buttons">

<button
    class="game-button"
    onclick="feed()"
>
🍪 먹기
</button>

<button
    class="game-button"
    onclick="sleepPet()"
>
🛏️ 자기
</button>

<button
    class="game-button"
    onclick="play()"
>
🧸 놀기
</button>

<button
    class="game-button"
    onclick="wash()"
>
🫧 씻기
</button>

</div>


</div>

</div>

</div>


<script>

/* =====================================================
   게임 변수
===================================================== */

let hunger = 80;

let happiness = 80;

let energy = 80;

let clean = 80;

let health = 100;

let xp = 0;

let sleeping = false;

let busy = false;


/* =====================================================
   요소
===================================================== */

const game =
    document.getElementById("game");

const character =
    document.getElementById("character");

const characterImage =
    document.getElementById(
        "characterImage"
    );


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
        "hunger"
    ).innerText =
        Math.round(hunger);


    document.getElementById(
        "happy"
    ).innerText =
        Math.round(happiness);


    document.getElementById(
        "energy"
    ).innerText =
        Math.round(energy);


    document.getElementById(
        "clean"
    ).innerText =
        Math.round(clean);


    document.getElementById(
        "health"
    ).innerText =
        Math.round(health);


    document.getElementById(
        "xp"
    ).innerText =
        xp;

}}


/* =====================================================
   메시지
===================================================== */

function showMessage(text) {{

    const msg =
        document.createElement("div");

    msg.className =
        "message";

    msg.innerText =
        text;

    document
        .getElementById("messages")
        .appendChild(msg);

    setTimeout(
        () => msg.remove(),
        2100
    );

}}


/* =====================================================
   캐릭터 이미지 변경
===================================================== */

function setCharacter(src) {{

    characterImage.src =
        src;

}}


/* =====================================================
   캐릭터 중앙
===================================================== */

function goCenter() {{

    character.style.left =
        "50%";

    character.style.bottom =
        "15%";

}}


/* =====================================================
   캐릭터 콩콩 이동
===================================================== */

function moveCharacter(
    left,
    bottom
) {{

    character.style.left =
        left;

    character.style.bottom =
        bottom;

}}


/* =====================================================
   콩콩 모션 시작
===================================================== */

function startHop() {{

    character.classList.add(
        "hop"
    );

}}


/* =====================================================
   콩콩 모션 종료
===================================================== */

function stopHop() {{

    character.classList.remove(
        "hop"
    );

}}


/* =====================================================
   하트 효과
===================================================== */

function hearts(count = 5) {{

    for(
        let i = 0;
        i < count;
        i++
    ) {{

        setTimeout(() => {{

            const h =
                document.createElement(
                    "div"
                );

            h.className =
                "heart";

            h.innerText =
                Math.random() > .5
                ? "💗"
                : "💕";


            h.style.left =
                (
                    42 +
                    Math.random() * 18
                ) + "%";


            h.style.bottom =
                (
                    35 +
                    Math.random() * 20
                ) + "%";


            game.appendChild(h);


            setTimeout(
                () => h.remove(),
                1400
            );

        }}, i * 130);

    }}

}}


/* =====================================================
   비눗방울
===================================================== */

function bubbles() {{

    for(
        let i = 0;
        i < 10;
        i++
    ) {{

        setTimeout(() => {{

            const b =
                document.createElement(
                    "div"
                );

            b.className =
                "bubble";

            b.innerText =
                Math.random() > .5
                ? "🫧"
                : "○";


            b.style.left =
                (
                    42 +
                    Math.random() * 20
                ) + "%";


            b.style.bottom =
                (
                    28 +
                    Math.random() * 18
                ) + "%";


            game.appendChild(b);


            setTimeout(
                () => b.remove(),
                1700
            );

        }}, i * 100);

    }}

}}


/* =====================================================
   🍪 먹이기
===================================================== */

function feed() {{

    if(busy) {{
        return;
    }}


    busy = true;


    showMessage(
        "🍪 몬치치가 쿠키를 발견했어요!"
    );


    /*
       1단계
       중앙 → 쿠키 위치
    */

    startHop();


    moveCharacter(
        "22%",
        "16%"
    );


    /*
       약 1.2초 이동
    */

    setTimeout(() => {{

        stopHop();


        /*
           먹는 캐릭터로 변경
        */

        setCharacter(
            "data:image/png;base64,{eating_b64}"
        );


        character.classList.add(
            "eating"
        );


        hunger =
            limit(hunger + 25);


        happiness =
            limit(happiness + 8);


        xp += 3;


        showMessage(
            "🍪 냠냠! 맛있어요!"
        );


        hearts(3);


        updateStats();


    }}, 1200);


    /*
       행동 약 3초
    */

    setTimeout(() => {{

        character.classList.remove(
            "eating"
        );


        /*
           다시 정면 몬치치
        */

        setCharacter(
            "data:image/png;base64,{normal_b64}"
        );


        /*
           중앙으로 복귀
        */

        startHop();


        moveCharacter(
            "50%",
            "15%"
        );


    }}, 3000);


    /*
       완전히 도착 후 종료
    */

    setTimeout(() => {{

        stopHop();

        goCenter();

        busy = false;

    }}, 4200);

}}


/* =====================================================
   🛏️ 자기
===================================================== */

function sleepPet() {{

    if(busy) {{
        return;
    }}


    busy = true;


    showMessage(
        "🛏️ 침대로 갈게요..."
    );


    /*
       중앙 → 침대
    */

    startHop();


    moveCharacter(
        "17%",
        "28%"
    );


    /*
       침대 도착
    */

    setTimeout(() => {{

        stopHop();


        /*
           자는 캐릭터로 변경
        */

        setCharacter(
            "data:image/png;base64,{sleeping_b64}"
        );


        character.classList.add(
            "sleep"
        );


        sleeping = true;


        showMessage(
            "💤 Zzz... 잘 자요..."
        );


        createZZZ();


        /*
           에너지 회복
        */

        energy =
            limit(energy + 25);


        happiness =
            limit(happiness + 5);


        xp += 2;


        updateStats();


    }}, 1200);


    /*
       3초 정도 잠자는 행동
    */

    setTimeout(() => {{

        character.classList.remove(
            "sleep"
        );


        removeZZZ();


        /*
           다시 정면
        */

        setCharacter(
            "data:image/png;base64,{normal_b64}"
        );


        sleeping = false;


        /*
           중앙으로 이동
        */

        startHop();


        moveCharacter(
            "50%",
            "15%"
        );


    }}, 3000);


    setTimeout(() => {{

        stopHop();

        goCenter();

        busy = false;

    }}, 4200);

}}


/* =====================================================
   ZZZ 효과
===================================================== */

function createZZZ() {{

    removeZZZ();


    const z =
        document.createElement(
            "div"
        );

    z.className =
        "zzz";

    z.id =
        "sleepZZZ";

    z.innerText =
        "Zzz...";


    game.appendChild(z);

}}


function removeZZZ() {{

    const z =
        document.getElementById(
            "sleepZZZ"
        );

    if(z) {{
        z.remove();
    }}

}}


/* =====================================================
   🧸 놀아주기
===================================================== */

function play() {{

    if(busy) {{
        return;
    }}


    if(energy < 15) {{

        showMessage(
            "😴 너무 피곤해서 놀 수 없어요!"
        );

        return;
    }}


    busy = true;


    showMessage(
        "🧸 장난감을 발견했어요!"
    );


    /*
       중앙 → 장난감
    */

    startHop();


    moveCharacter(
        "78%",
        "16%"
    );


    setTimeout(() => {{

        stopHop();


        happiness =
            limit(
                happiness + 25
            );


        energy =
            limit(
                energy - 15
            );


        hunger =
            limit(
                hunger - 5
            );


        xp += 7;


        showMessage(
            "🧸 신나게 놀았어요!"
        );


        hearts(3);

        stars();


        updateStats();

    }}, 1200);


    /*
       3초 후 중앙으로
    */

    setTimeout(() => {{

        startHop();


        moveCharacter(
            "50%",
            "15%"
        );

    }}, 3000);


    setTimeout(() => {{

        stopHop();

        goCenter();

        busy = false;

    }}, 4200);

}}


/* =====================================================
   ⭐ 별 효과
===================================================== */

function stars() {{

    for(
        let i = 0;
        i < 6;
        i++
    ) {{

        setTimeout(() => {{

            const s =
                document.createElement(
                    "div"
                );

            s.className =
                "heart";

            s.innerText =
                "⭐";


            s.style.left =
                (
                    40 +
                    Math.random() * 25
                ) + "%";


            s.style.bottom =
                (
                    30 +
                    Math.random() * 25
                ) + "%";


            game.appendChild(s);


            setTimeout(
                () => s.remove(),
                1400
            );

        }}, i * 100);

    }}

}}


/* =====================================================
   🫧 씻기
===================================================== */

function wash() {{

    if(busy) {{
        return;
    }}


    busy = true;


    showMessage(
        "🫧 뽀득뽀득 씻어볼까요?"
    );


    /*
       몬치치에게 거품 발생
    */

    bubbles();


    happiness =
        limit(
            happiness + 10
        );


    clean =
        limit(
            clean + 35
        );


    xp += 4;


    updateStats();


    /*
       3초 후 종료
    */

    setTimeout(() => {{

        showMessage(
            "✨ 깨끗해졌어요!"
        );


        hearts(2);


        updateStats();


        busy = false;

    }}, 3000);

}}


/* =====================================================
   시간에 따른 상태 감소
===================================================== */

setInterval(() => {{

    if(busy && sleeping) {{

        energy =
            limit(
                energy + 3
            );

        hunger =
            limit(
                hunger - 1
            );

    }}

    else if(!busy) {{

        hunger =
            limit(
                hunger - .8
            );

        happiness =
            limit(
                happiness - .4
            );

        energy =
            limit(
                energy - .4
            );

        clean =
            limit(
                clean - .4
            );

    }}


    /*
       건강

       여러 상태가 너무 낮으면
       건강도 조금씩 감소
    */

    let bad = 0;


    if(hunger < 15) {{
        bad++;
    }}

    if(happiness < 15) {{
        bad++;
    }}

    if(energy < 10) {{
        bad++;
    }}

    if(clean < 10) {{
        bad++;
    }}


    if(bad > 0) {{

        health =
            limit(
                health - bad * .2
            );

    }}


    updateStats();

}}, 10000);


/* =====================================================
   초기 상태
===================================================== */

updateStats();


</script>


</body>

</html>
"""


# =========================================================
# 게임 표시
# =========================================================

components.html(
    html,
    height=720,
    scrolling=False
)
