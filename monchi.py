import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="몬치치 키우기",
    page_icon="🐒",
    layout="centered"
)

BASE_DIR = Path(__file__).parent

BACKGROUND = BASE_DIR / "assets/C3BCB046-F78D-4E61-97AE-D1A04EAD0F0F.png"
NORMAL = BASE_DIR / "assets/CE442387-F366-4FB2-A0B6-11704E0A474A.png"
EATING = BASE_DIR / "assets/837AA3CB-1CBB-4C2D-9EBA-8ED0B5A4D33D.png"
SLEEPING = BASE_DIR / "assets/935DC2BF-D149-4B85-8C5C-B2BA02179A6F.png"
GAME_DEVICE = BASE_DIR / "assets/IMG_8184.jpeg"


def b64(path):
    return base64.b64encode(path.read_bytes()).decode()


bg = b64(BACKGROUND)
normal = b64(NORMAL)
eating = b64(EATING)
sleeping = b64(SLEEPING)
device = b64(GAME_DEVICE)


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

/* ==============================
   기본
============================== */

* {{
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
}}

body {{
    font-family: Arial, "Noto Sans KR", sans-serif;
}}


/* ==============================
   게임기 전체
============================== */

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


/* ==================================================
   ★★★ 핵심 ★★★

   게임기 붉은 테두리 안의
   흰색 화면에 정확하게 배치

   기존에는

   left: 19%
   width: 62%
   height: 57%

   였기 때문에 너무 작고 아래까지 내려갔음.

   현재 사진 기준으로
   흰색 화면 전체를 사용하도록 수정.
================================================== */

.screen {{

    position: absolute;

    /*
       흰색 화면의 왼쪽
    */
    left: 10.8%;

    /*
       흰색 화면의 위쪽
    */
    top: 15.7%;

    /*
       흰색 화면의 가로 크기
    */
    width: 82.4%;

    /*
       흰색 화면의 세로 크기
    */
    height: 44.1%;

    overflow: hidden;

    /*
       게임기 흰색 화면의
       둥근 모서리
    */
    border-radius: 28px;

    background: #fdf7f8;

    /*
       화면이 둥근 테두리 밖으로
       절대 나오지 않도록
    */
    clip-path: inset(
        0 round 28px
    );

    box-shadow:
        inset 0 0 0 2px
        rgba(120,80,80,.04);
}}


/* ==============================
   실제 게임
============================== */

.game {{

    position: absolute;

    inset: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    /*
       가로형 방 배경
    */
    background-image:
        url("data:image/png;base64,{bg}");

    /*
       화면을 가득 채우되
       비율은 유지
    */
    background-size: cover;

    background-position: center center;

    background-repeat: no-repeat;

    touch-action: manipulation;
}}


/* ==============================
   상태창
============================== */

.hud {{

    position: absolute;

    z-index: 100;

    top: 3%;
    left: 5%;
    right: 5%;

    display: flex;

    justify-content: center;

    gap: 5px;

    flex-wrap: wrap;
}}

.stat {{

    background:
        rgba(255,255,255,.94);

    border:
        1.5px solid #dba7b5;

    border-radius: 9px;

    padding:
        4px 7px;

    min-width: 15%;

    text-align: center;

    color: #65432e;

    font-size:
        clamp(8px, 1.25vw, 13px);

    box-shadow:
        0 2px 3px
        rgba(80,50,30,.12);
}}

.stat strong {{
    font-size: 1.1em;
}}


/* ==============================
   몬치치
============================== */

.character {{

    position: absolute;

    z-index: 30;

    width: 19%;

    left: 50%;

    bottom: 13%;

    transform:
        translateX(-50%);

    transition:
        left 1.2s
        cubic-bezier(.45,.05,.55,.95),

        bottom 1.2s
        cubic-bezier(.45,.05,.55,.95);

    pointer-events: none;
}}

.character img {{

    display: block;

    width: 100%;
    height: auto;

    filter:
        drop-shadow(
            0 3px 2px
            rgba(60,40,20,.25)
        );
}}


/* ==============================
   콩콩 뛰기
============================== */

.hop {{
    animation:
        hop .42s
        ease-in-out
        infinite;
}}

@keyframes hop {{

    0%,100% {{
        margin-bottom: 0;
    }}

    50% {{
        margin-bottom: 9px;
    }}
}}


/* ==============================
   먹기
============================== */

.eating {{
    animation:
        eat .45s
        ease-in-out
        infinite;
}}

@keyframes eat {{

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


/* ==============================
   자기
============================== */

.sleep {{
    animation:
        sleeping 1.4s
        ease-in-out
        infinite;
}}

@keyframes sleeping {{

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


/* ==============================
   터치 영역
============================== */

.hotspot {{

    position: absolute;

    z-index: 80;

    cursor: pointer;

    border-radius: 20px;

    touch-action: manipulation;
}}

.hotspot:active {{
    background:
        rgba(255,255,255,.15);
}}


/* ==============================
   배경 사물 위치
============================== */

/*
   실제 방 배경에 맞춰서
   터치 영역을 설정
*/


/* 쿠키 */

.cookie {{
    left: 12%;
    bottom: 12%;

    width: 20%;
    height: 18%;
}}


/* 침대 */

.bed {{
    left: 3%;
    bottom: 20%;

    width: 28%;
    height: 38%;
}}


/* 장난감 */

.toy {{
    right: 10%;
    bottom: 10%;

    width: 23%;
    height: 25%;
}}


/* 씻기 */

.wash {{
    right: 5%;
    top: 35%;

    width: 18%;
    height: 25%;
}}


/* ==============================
   효과
============================== */

.effect {{
    position: absolute;
    z-index: 200;
    pointer-events: none;
}}


/* 하트 */

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
            translateY(-50px)
            scale(.8);
    }}
}}


/* 비눗방울 */

.bubble {{

    position: absolute;

    z-index: 150;

    pointer-events: none;

    font-size: 18px;

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
            translateY(-60px)
            scale(1.2);
    }}
}}


/* ==============================
   ZZZ
============================== */

.zzz {{

    position: absolute;

    z-index: 160;

    left: 58%;
    bottom: 38%;

    color: #65432e;

    font-weight: bold;

    font-size: 18px;

    animation:
        zzzMove 1.7s
        ease-in-out
        infinite;
}}

@keyframes zzzMove {{

    0% {{
        opacity: 0;
        transform:
            translate(0,10px);
    }}

    40% {{
        opacity: 1;
    }}

    100% {{
        opacity: 0;
        transform:
            translate(25px,-25px);
    }}
}}


/* ==============================
   말풍선
============================== */

.message {{

    position: absolute;

    z-index: 180;

    left: 50%;
    top: 18%;

    transform:
        translateX(-50%);

    background: white;

    color: #65432e;

    border:
        2px solid #dfaab8;

    border-radius: 12px;

    padding: 5px 9px;

    font-size:
        clamp(8px, 1.4vw, 14px);

    white-space: nowrap;

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


/* ==============================
   버튼
============================== */

.buttons {{

    position: absolute;

    z-index: 120;

    left: 5%;
    right: 5%;

    bottom: 2.5%;

    display: flex;

    justify-content: center;

    gap: 4px;
}}

.game-button {{

    border:
        1.5px solid #dca8b5;

    background:
        rgba(255,255,255,.96);

    color: #65432e;

    border-radius: 9px;

    padding:
        4px 7px;

    font-size:
        clamp(8px, 1.2vw, 12px);

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


</style>
</head>


<body>


<!-- ==================================================
     게임기
================================================== -->

<div class="device">

    <img
        class="device-image"
        src="data:image/jpeg;base64,{device}"
    >


    <!-- ==============================================
         ★ 흰색 화면 안에 들어가는 게임
    =============================================== -->

    <div class="screen">

        <div class="game" id="game">


            <!-- 상태 -->

            <div class="hud">

                <div class="stat">
                    🍪 <strong id="hunger">80</strong>%
                </div>

                <div class="stat">
                    💗 <strong id="happy">80</strong>%
                </div>

                <div class="stat">
                    ⚡ <strong id="energy">80</strong>%
                </div>

                <div class="stat">
                    🫧 <strong id="clean">80</strong>%
                </div>

                <div class="stat">
                    ❤️ <strong id="health">100</strong>%
                </div>

                <div class="stat">
                    ⭐ <strong id="xp">0</strong>
                </div>

            </div>


            <!-- 몬치치 -->

            <div
                class="character"
                id="character"
            >

                <img
                    id="characterImage"
                    src="data:image/png;base64,{normal}"
                >

            </div>


            <!-- 배경 터치 영역 -->

            <div
                class="hotspot cookie"
                onclick="feed()"
            ></div>

            <div
                class="hotspot bed"
                onclick="sleepPet()"
            ></div>

            <div
                class="hotspot toy"
                onclick="play()"
            ></div>

            <div
                class="hotspot wash"
                onclick="wash()"
            ></div>


            <div id="effects"></div>

            <div id="messages"></div>


            <!-- 버튼 -->

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

/* ==========================================
   상태
========================================== */

let hunger = 80;
let happiness = 80;
let energy = 80;
let clean = 80;
let health = 100;
let xp = 0;

let busy = false;
let sleeping = false;


/* ==========================================
   요소
========================================== */

const game =
    document.getElementById("game");

const character =
    document.getElementById("character");

const characterImage =
    document.getElementById(
        "characterImage"
    );


/* ==========================================
   제한
========================================== */

function limit(v) {{

    return Math.max(
        0,
        Math.min(100, v)
    );

}}


/* ==========================================
   상태 업데이트
========================================== */

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


/* ==========================================
   메시지
========================================== */

function message(text) {{

    const m =
        document.createElement("div");

    m.className =
        "message";

    m.innerText =
        text;

    document
        .getElementById("messages")
        .appendChild(m);

    setTimeout(
        () => m.remove(),
        2100
    );
}}


/* ==========================================
   이동
========================================== */

function move(left, bottom) {{

    character.style.left = left;
    character.style.bottom = bottom;

}}

function center() {{

    move("50%", "13%");

}}

function hopStart() {{

    character.classList.add("hop");

}}

function hopStop() {{

    character.classList.remove("hop");

}}


/* ==========================================
   하트
========================================== */

function hearts() {{

    for(let i=0;i<5;i++) {{

        setTimeout(() => {{

            const h =
                document.createElement("div");

            h.className = "heart";

            h.innerText =
                Math.random() > .5
                ? "💗"
                : "💕";

            h.style.left =
                (42 + Math.random()*18) + "%";

            h.style.bottom =
                (30 + Math.random()*20) + "%";

            game.appendChild(h);

            setTimeout(
                () => h.remove(),
                1400
            );

        }}, i*120);

    }}
}}


/* ==========================================
   별
========================================== */

function stars() {{

    for(let i=0;i<5;i++) {{

        setTimeout(() => {{

            const s =
                document.createElement("div");

            s.className = "heart";

            s.innerText = "⭐";

            s.style.left =
                (40 + Math.random()*25) + "%";

            s.style.bottom =
                (30 + Math.random()*20) + "%";

            game.appendChild(s);

            setTimeout(
                () => s.remove(),
                1400
            );

        }}, i*120);

    }}
}}


/* ==========================================
   🍪 먹기
========================================== */

function feed() {{

    if(busy) return;

    busy = true;

    message(
        "🍪 쿠키 먹으러 갈게요!"
    );

    hopStart();


    /*
       중앙 → 쿠키
    */

    move(
        "22%",
        "13%"
    );


    /*
       쿠키 도착
    */

    setTimeout(() => {{

        hopStop();

        characterImage.src =
            "data:image/png;base64,{eating}";

        character.classList.add(
            "eating"
        );

        hunger =
            limit(hunger + 25);

        happiness =
            limit(happiness + 8);

        xp += 3;

        message(
            "🍪 냠냠! 맛있어요!"
        );

        hearts();

        updateStats();

    }}, 1200);


    /*
       3초 행동
    */

    setTimeout(() => {{

        character.classList.remove(
            "eating"
        );

        characterImage.src =
            "data:image/png;base64,{normal}";

        hopStart();

        center();

    }}, 3000);


    setTimeout(() => {{

        hopStop();

        center();

        busy = false;

    }}, 4200);

}}


/* ==========================================
   🛏️ 자기
========================================== */

function sleepPet() {{

    if(busy) return;

    busy = true;

    message(
        "🛏️ 침대로 갈게요..."
    );

    hopStart();


    /*
       중앙 → 침대
    */

    move(
        "17%",
        "27%"
    );


    setTimeout(() => {{

        hopStop();

        characterImage.src =
            "data:image/png;base64,{sleeping}";

        character.classList.add(
            "sleep"
        );

        sleeping = true;

        energy =
            limit(energy + 25);

        happiness =
            limit(happiness + 5);

        xp += 2;

        message(
            "💤 Zzz... 잘 자요..."
        );

        createZzz();

        updateStats();

    }}, 1200);


    /*
       3초 잠자기
    */

    setTimeout(() => {{

        character.classList.remove(
            "sleep"
        );

        removeZzz();

        characterImage.src =
            "data:image/png;base64,{normal}";

        sleeping = false;

        hopStart();

        center();

    }}, 3000);


    setTimeout(() => {{

        hopStop();

        center();

        busy = false;

    }}, 4200);

}}


/* ==========================================
   ZZZ
========================================== */

function createZzz() {{

    removeZzz();

    const z =
        document.createElement("div");

    z.className = "zzz";

    z.id = "sleepZZZ";

    z.innerText = "Zzz...";

    game.appendChild(z);

}}

function removeZzz() {{

    const z =
        document.getElementById(
            "sleepZZZ"
        );

    if(z) z.remove();

}}


/* ==========================================
   🧸 놀기
========================================== */

function play() {{

    if(busy) return;

    if(energy < 15) {{

        message(
            "😴 너무 피곤해요!"
        );

        return;
    }}

    busy = true;

    message(
        "🧸 장난감 가지고 놀자!"
    );

    hopStart();


    /*
       중앙 → 장난감
    */

    move(
        "78%",
        "13%"
    );


    setTimeout(() => {{

        hopStop();

        happiness =
            limit(happiness + 25);

        energy =
            limit(energy - 15);

        hunger =
            limit(hunger - 5);

        xp += 7;

        message(
            "🧸 우와! 재밌다!"
        );

        hearts();
        stars();

        updateStats();

    }}, 1200);


    setTimeout(() => {{

        hopStart();

        center();

    }}, 3000);


    setTimeout(() => {{

        hopStop();

        center();

        busy = false;

    }}, 4200);

}}


/* ==========================================
   🫧 씻기
========================================== */

function wash() {{

    if(busy) return;

    busy = true;

    message(
        "🫧 뽀득뽀득 씻는 중!"
    );

    bubbles();

    clean =
        limit(clean + 35);

    happiness =
        limit(happiness + 10);

    xp += 4;

    updateStats();


    setTimeout(() => {{

        message(
            "✨ 깨끗해졌어요!"
        );

        hearts();

        busy = false;

    }}, 3000);

}}


/* ==========================================
   거품
========================================== */

function bubbles() {{

    for(let i=0;i<12;i++) {{

        setTimeout(() => {{

            const b =
                document.createElement("div");

            b.className = "bubble";

            b.innerText =
                Math.random() > .4
                ? "🫧"
                : "○";

            b.style.left =
                (40 + Math.random()*22) + "%";

            b.style.bottom =
                (25 + Math.random()*25) + "%";

            game.appendChild(b);

            setTimeout(
                () => b.remove(),
                1700
            );

        }}, i*100);

    }}
}}


/* ==========================================
   시간에 따른 상태 감소
========================================== */

setInterval(() => {{

    if(!busy) {{

        hunger =
            limit(hunger - .8);

        happiness =
            limit(happiness - .4);

        energy =
            limit(energy - .4);

        clean =
            limit(clean - .4);

    }}


    let bad = 0;

    if(hunger < 15) bad++;
    if(happiness < 15) bad++;
    if(energy < 10) bad++;
    if(clean < 10) bad++;


    if(bad > 0) {{

        health =
            limit(
                health - bad * .2
            );

    }}

    updateStats();

}}, 10000);


/* ==========================================
   시작
========================================== */

updateStats();
center();

</script>

</body>
</html>
"""


components.html(
    html,
    height=700,
    scrolling=False
)
