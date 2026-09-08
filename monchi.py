import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="몬치치 키우기",
    page_icon="🐒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 파일
# =========================================================

BASE_DIR = Path(__file__).parent

BG_PATH = BASE_DIR / "assets/C3BCB046-F78D-4E61-97AE-D1A04EAD0F0F.png"
NORMAL_PATH = BASE_DIR / "assets/CE442387-F366-4FB2-A0B6-11704E0A474A.png"
EAT_PATH = BASE_DIR / "assets/837AA3CB-1CBB-4C2D-9EBA-8ED0B5A4D33D.png"
SLEEP_PATH = BASE_DIR / "assets/935DC2BF-D149-4B85-8C5C-B2BA02179A6F.png"
DEVICE_PATH = BASE_DIR / "assets/IMG_8184.jpeg"


def image64(path):
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


bg = image64(BG_PATH)
normal = image64(NORMAL_PATH)
eat = image64(EAT_PATH)
sleep = image64(SLEEP_PATH)
device = image64(DEVICE_PATH)


# =========================================================
# HTML
# =========================================================

html = f"""
<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1,
maximum-scale=1,
user-scalable=no">

<style>

/* =====================================================
   전체
===================================================== */

html,
body {{

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: #f6e7df;

}}

* {{
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}}


/* =====================================================
   게임 전체

   ★ 방 사진을 게임 화면 전체로 사용
===================================================== */

#gameWrapper {{

    width: 100vw;
    height: 100vh;

    display: flex;

    justify-content: center;
    align-items: center;

}}


/* =====================================================
   실제 게임 공간

   ★ 16:9
===================================================== */

#game {{

    position: relative;

    width: min(100vw, 177.78vh);
    height: min(100vh, 56.25vw);

    overflow: hidden;

    background-image:
        url("data:image/png;base64,{bg}");

    /*
       ★ 중요
       배경 사진 전체가 최대한 보이도록 contain
    */

    background-size: 100% 100%;

    background-position: center;

    background-repeat: no-repeat;

    touch-action: manipulation;
}}


/* =====================================================
   캐릭터
===================================================== */

#character {{

    position: absolute;

    z-index: 30;

    width: 13%;

    left: 50%;

    /*
       ★ 중앙 위치
    */

    top: 63%;

    transform:
        translate(-50%, -50%);

    transition:
        left 1.25s ease-in-out,
        top 1.25s ease-in-out;

    pointer-events: none;
}}

#character img {{

    width: 100%;
    height: auto;

    display: block;

    image-rendering: auto;

    filter:
        drop-shadow(
            0 5px 3px
            rgba(60,40,20,.25)
        );
}}


/* =====================================================
   콩콩 뛰기
===================================================== */

.hopping {{

    animation:
        hop .42s infinite ease-in-out;
}}

@keyframes hop {{

    0%,
    100% {{
        transform:
            translate(-50%, -50%);
    }}

    50% {{
        transform:
            translate(-50%, -65%);
    }}

}}


/* =====================================================
   먹는 모션
===================================================== */

.eating {{

    animation:
        eating .5s infinite ease-in-out;
}}

@keyframes eating {{

    0%,
    100% {{
        transform:
            translate(-50%, -50%)
            scale(1);
    }}

    50% {{
        transform:
            translate(-50%, -50%)
            scale(1.08);
    }}

}}


/* =====================================================
   자는 모션
===================================================== */

.sleeping {{

    animation:
        sleeping 1.2s infinite ease-in-out;
}}

@keyframes sleeping {{

    0%,
    100% {{
        transform:
            translate(-50%, -50%)
            rotate(-2deg);
    }}

    50% {{
        transform:
            translate(-50%, -47%)
            rotate(2deg);
    }}

}}


/* =====================================================
   상태창
===================================================== */

#status {{

    position: absolute;

    z-index: 100;

    top: 3%;

    left: 50%;

    transform:
        translateX(-50%);

    display: flex;

    justify-content: center;

    gap: 6px;

    flex-wrap: wrap;

    width: 90%;
}}

.stat {{

    background:
        rgba(255,255,255,.94);

    border:
        2px solid #d9a7a7;

    border-radius: 12px;

    padding:
        5px 9px;

    color: #65432e;

    font-size:
        clamp(10px, 1.3vw, 16px);

    font-weight: bold;

    box-shadow:
        0 2px 4px
        rgba(80,50,30,.18);
}}


/* =====================================================
   배경 클릭 영역

   ★ 실제 배경 속 사물로 이동
===================================================== */

.hotspot {{

    position: absolute;

    z-index: 80;

    border-radius: 20px;

    cursor: pointer;

    touch-action: manipulation;

}}


/*
=========================================================
★ 아래 숫자는 배경 사진 속 물건 위치

필요하면 여기 숫자만 조금 조절하면 됨.
=========================================================
*/


/* -----------------------------------------------------
   🍪 쿠키
----------------------------------------------------- */

#cookieHotspot {{

    left: 8%;
    top: 62%;

    width: 20%;
    height: 20%;
}}


/* -----------------------------------------------------
   🛏️ 침대
----------------------------------------------------- */

#bedHotspot {{

    left: 3%;
    top: 27%;

    width: 30%;
    height: 38%;
}}


/* -----------------------------------------------------
   🧸 장난감
----------------------------------------------------- */

#toyHotspot {{

    right: 5%;
    top: 55%;

    width: 25%;
    height: 28%;
}}


/* -----------------------------------------------------
   🫧 씻기

   별도의 물건을 누르지 않고
   버튼으로 실행
----------------------------------------------------- */


/* =====================================================
   하단 조종부

   ★ 게임기 전체를 덮지 않음
   ★ 화면 아래에 작은 조종부만 사용
===================================================== */

#controller {{

    position: absolute;

    z-index: 200;

    left: 50%;

    bottom: 1.5%;

    transform:
        translateX(-50%);

    width: 70%;

    display: flex;

    justify-content: center;

    align-items: center;

    gap: 8px;
}}


/* =====================================================
   버튼
===================================================== */

.controlButton {{

    border:
        2px solid #c68f9a;

    background:
        rgba(255,255,255,.95);

    color: #65432e;

    border-radius: 14px;

    padding:
        7px 13px;

    font-size:
        clamp(10px, 1.4vw, 16px);

    font-weight: bold;

    box-shadow:
        0 3px 0 #cda3a9;

    cursor: pointer;

    user-select: none;
}}

.controlButton:active {{

    transform:
        translateY(3px);

    box-shadow:
        none;
}}


/* =====================================================
   메시지
===================================================== */

#message {{

    position: absolute;

    z-index: 150;

    top: 18%;

    left: 50%;

    transform:
        translateX(-50%);

    background:
        rgba(255,255,255,.96);

    color: #65432e;

    border:
        2px solid #d9a7a7;

    border-radius: 14px;

    padding:
        7px 13px;

    font-size:
        clamp(11px, 1.5vw, 17px);

    font-weight: bold;

    white-space: nowrap;

    opacity: 0;
}}


/* =====================================================
   메시지 등장
===================================================== */

.messageShow {{

    animation:
        showMessage 2s forwards;
}}

@keyframes showMessage {{

    0% {{
        opacity: 0;

        transform:
            translate(-50%, 10px);
    }}

    15%,
    75% {{
        opacity: 1;

        transform:
            translate(-50%, 0);
    }}

    100% {{
        opacity: 0;
    }}

}}


/* =====================================================
   하트 / 별 / 거품
===================================================== */

.effect {{

    position: absolute;

    z-index: 160;

    pointer-events: none;

    font-size:
        clamp(18px, 3vw, 35px);

    animation:
        effectMove 1.5s
        ease-out
        forwards;
}}

@keyframes effectMove {{

    0% {{
        opacity: 0;

        transform:
            translateY(15px)
            scale(.5);
    }}

    20% {{
        opacity: 1;
    }}

    100% {{
        opacity: 0;

        transform:
            translateY(-70px)
            scale(1.1);
    }}

}}


/* =====================================================
   ZZZ
===================================================== */

#zzz {{

    position: absolute;

    z-index: 160;

    left: 56%;

    top: 42%;

    color: #65432e;

    font-size:
        clamp(15px, 2.5vw, 28px);

    font-weight: bold;

    display: none;
}}

.zzzShow {{

    display: block !important;

    animation:
        zzzAnimation 1.5s
        infinite ease-in-out;
}}

@keyframes zzzAnimation {{

    0% {{
        opacity: 0;

        transform:
            translate(0,10px);
    }}

    50% {{
        opacity: 1;
    }}

    100% {{
        opacity: 0;

        transform:
            translate(30px,-30px);
    }}

}}


/* =====================================================
   작은 안내
===================================================== */

#hint {{

    position: absolute;

    z-index: 50;

    left: 50%;

    bottom: 13%;

    transform:
        translateX(-50%);

    color: #704d37;

    background:
        rgba(255,255,255,.72);

    padding:
        4px 10px;

    border-radius: 10px;

    font-size:
        clamp(9px, 1.2vw, 13px);

    pointer-events: none;
}}


/* =====================================================
   작은 화면 대응
===================================================== */

@media (max-width: 600px) {{

    #status {{
        top: 2%;
        gap: 3px;
    }}

    .stat {{
        padding: 4px 6px;
        border-radius: 9px;
    }}

    #character {{
        width: 15%;
    }}

    #controller {{
        width: 94%;
        gap: 3px;
    }}

    .controlButton {{
        padding:
            5px 7px;

        border-radius: 10px;
    }}

}}

</style>

</head>


<body>


<div id="gameWrapper">


    <!-- =================================================
         ★ 방 전체가 게임 화면
    ================================================== -->

    <div id="game">


        <!-- =============================================
             상태
        ============================================== -->

        <div id="status">

            <div class="stat">
                🍪 배고픔
                <span id="hunger">80</span>%
            </div>

            <div class="stat">
                💗 행복
                <span id="happy">80</span>%
            </div>

            <div class="stat">
                ⚡ 에너지
                <span id="energy">80</span>%
            </div>

            <div class="stat">
                🫧 청결
                <span id="clean">80</span>%
            </div>

            <div class="stat">
                ❤️ 건강
                <span id="health">100</span>%
            </div>

            <div class="stat">
                ⭐
                <span id="xp">0</span>
            </div>

        </div>


        <!-- =============================================
             몬치치
        ============================================== -->

        <div id="character">

            <img
                id="characterImage"
                src="data:image/png;base64,{normal}"
            >

        </div>


        <!-- =============================================
             ZZZ
        ============================================== -->

        <div id="zzz">
            Zzz...
        </div>


        <!-- =============================================
             메시지
        ============================================== -->

        <div id="message"></div>


        <!-- =============================================
             ★ 배경 속 실제 물건 클릭 영역

             사진 자체는 그대로 보임.
             투명한 클릭 영역만 위에 올라감.
        ============================================== -->

        <div
            id="cookieHotspot"
            class="hotspot"
            onclick="feed()">
        </div>


        <div
            id="bedHotspot"
            class="hotspot"
            onclick="sleepPet()">
        </div>


        <div
            id="toyHotspot"
            class="hotspot"
            onclick="play()">
        </div>


        <!-- =============================================
             하단 조종부
        ============================================== -->

        <div id="controller">

            <button
                class="controlButton"
                onclick="feed()">
                🍪 먹기
            </button>

            <button
                class="controlButton"
                onclick="sleepPet()">
                🛏️ 자기
            </button>

            <button
                class="controlButton"
                onclick="play()">
                🧸 놀기
            </button>

            <button
                class="controlButton"
                onclick="wash()">
                🫧 씻기
            </button>

        </div>


        <div id="hint">
            방에 있는 물건을 눌러보세요!
        </div>


    </div>

</div>


<script>

/* =====================================================
   상태
===================================================== */

let hunger = 80;
let happy = 80;
let energy = 80;
let clean = 80;
let health = 100;
let xp = 0;

let busy = false;


/* =====================================================
   요소
===================================================== */

const character =
    document.getElementById("character");

const characterImage =
    document.getElementById(
        "characterImage"
    );

const game =
    document.getElementById("game");

const messageBox =
    document.getElementById("message");

const zzz =
    document.getElementById("zzz");


/* =====================================================
   숫자 제한
===================================================== */

function limit(value) {{

    return Math.max(
        0,
        Math.min(
            100,
            value
        )
    );

}}


/* =====================================================
   상태 표시
===================================================== */

function updateStats() {{

    document.getElementById(
        "hunger"
    ).innerText =
        Math.round(hunger);

    document.getElementById(
        "happy"
    ).innerText =
        Math.round(happy);

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

    messageBox.innerText = text;

    messageBox.classList.remove(
        "messageShow"
    );

    void messageBox.offsetWidth;

    messageBox.classList.add(
        "messageShow"
    );

}}


/* =====================================================
   캐릭터 이동
===================================================== */

function moveTo(left, top) {{

    character.style.left =
        left + "%";

    character.style.top =
        top + "%";

}}


/* =====================================================
   중앙
===================================================== */

function goCenter() {{

    moveTo(
        50,
        63
    );

}}


/* =====================================================
   뛰기 시작
===================================================== */

function startHop() {{

    character.classList.add(
        "hopping"
    );

}}


/* =====================================================
   뛰기 종료
===================================================== */

function stopHop() {{

    character.classList.remove(
        "hopping"
    );

}}


/* =====================================================
   효과
===================================================== */

function effect(symbol) {{

    const e =
        document.createElement("div");

    e.className =
        "effect";

    e.innerText =
        symbol;

    e.style.left =
        (42 + Math.random()*16)
        + "%";

    e.style.top =
        (45 + Math.random()*15)
        + "%";

    game.appendChild(e);

    setTimeout(
        () => e.remove(),
        1500
    );

}}


/* =====================================================
   여러 효과
===================================================== */

function effects(symbol, count) {{

    for(
        let i = 0;
        i < count;
        i++
    ) {{

        setTimeout(
            () => effect(symbol),
            i * 150
        );

    }}

}}


/* =====================================================
   🍪 먹기
===================================================== */

function feed() {{

    if(busy)
        return;

    busy = true;

    showMessage(
        "🍪 쿠키 먹으러 가는 중!"
    );

    startHop();


    /*
    ★★★

    쿠키가 있는 곳으로 이동

    배경에서 쿠키 위치가
    왼쪽 아래라면 이 위치 사용

    */

    moveTo(
        17,
        68
    );


    /*
       도착
    */

    setTimeout(
        () => {{

            stopHop();

            characterImage.src =
                "data:image/png;base64,{eat}";

            character.classList.add(
                "eating"
            );

            hunger =
                limit(
                    hunger + 25
                );

            happy =
                limit(
                    happy + 8
                );

            xp += 3;

            showMessage(
                "😋 냠냠! 맛있다!"
            );

            effects(
                "💗",
                5
            );

            updateStats();

        }},
        1300
    );


    /*
       3초 행동
    */

    setTimeout(
        () => {{

            character.classList.remove(
                "eating"
            );

            characterImage.src =
                "data:image/png;base64,{normal}";

            startHop();

            goCenter();

        }},
        3000
    );


    /*
       중앙 도착
    */

    setTimeout(
        () => {{

            stopHop();

            busy = false;

        }},
        4300
    );

}}


/* =====================================================
   🛏️ 자기
===================================================== */

function sleepPet() {{

    if(busy)
        return;

    busy = true;

    showMessage(
        "🛏️ 침대로 가는 중..."
    );

    startHop();


    /*
       침대 위치
    */

    moveTo(
        18,
        47
    );


    /*
       침대 도착
    */

    setTimeout(
        () => {{

            stopHop();

            characterImage.src =
                "data:image/png;base64,{sleep}";

            character.classList.add(
                "sleeping"
            );

            zzz.classList.add(
                "zzzShow"
            );

            energy =
                limit(
                    energy + 30
                );

            happy =
                limit(
                    happy + 5
                );

            xp += 2;

            showMessage(
                "💤 Zzz... 잘 자요..."
            );

            updateStats();

        }},
        1300
    );


    /*
       3초 자기
    */

    setTimeout(
        () => {{

            character.classList.remove(
                "sleeping"
            );

            zzz.classList.remove(
                "zzzShow"
            );

            characterImage.src =
                "data:image/png;base64,{normal}";

            startHop();

            goCenter();

        }},
        3000
    );


    setTimeout(
        () => {{

            stopHop();

            busy = false;

        }},
        4300
    );

}}


/* =====================================================
   🧸 놀기
===================================================== */

function play() {{

    if(busy)
        return;

    if(energy < 15) {{

        showMessage(
            "😴 너무 피곤해요!"
        );

        return;

    }}

    busy = true;

    showMessage(
        "🧸 장난감 가지고 놀자!"
    );

    startHop();


    /*
       장난감 위치
    */

    moveTo(
        82,
        68
    );


    /*
       도착
    */

    setTimeout(
        () => {{

            stopHop();

            happy =
                limit(
                    happy + 25
                );

            energy =
                limit(
                    energy - 15
                );

            hunger =
                limit(
                    hunger - 5
                );

            xp += 5;

            showMessage(
                "🎉 우와! 재밌다!"
            );

            effects(
                "⭐",
                6
            );

            effects(
                "💗",
                3
            );

            updateStats();

        }},
        1300
    );


    /*
       3초 놀이
    */

    setTimeout(
        () => {{

            startHop();

            goCenter();

        }},
        3000
    );


    setTimeout(
        () => {{

            stopHop();

            busy = false;

        }},
        4300
    );

}}


/* =====================================================
   🫧 씻기
===================================================== */

function wash() {{

    if(busy)
        return;

    busy = true;

    showMessage(
        "🫧 뽀득뽀득 씻는 중!"
    );


    /*
       거품 생성
    */

    for(
        let i = 0;
        i < 14;
        i++
    ) {{

        setTimeout(
            () => {{

                effect(
                    Math.random() > .4
                    ? "🫧"
                    : "○"
                );

            }},
            i * 130
        );

    }}


    clean =
        limit(
            clean + 35
        );

    happy =
        limit(
            happy + 8
        );

    xp += 4;

    updateStats();


    /*
       3초 후
    */

    setTimeout(
        () => {{

            showMessage(
                "✨ 깨끗해졌어요!"
            );

            effects(
                "💗",
                4
            );

            busy = false;

        }},
        3000
    );

}}


/* =====================================================
   시간이 지나면 상태 감소
===================================================== */

setInterval(
    () => {{

        if(!busy) {{

            hunger =
                limit(
                    hunger - 0.7
                );

            happy =
                limit(
                    happy - 0.35
                );

            energy =
                limit(
                    energy - 0.3
                );

            clean =
                limit(
                    clean - 0.4
                );

        }}


        /*
           상태가 너무 낮으면 건강 감소
        */

        let bad = 0;

        if(hunger < 15)
            bad++;

        if(happy < 15)
            bad++;

        if(energy < 10)
            bad++;

        if(clean < 10)
            bad++;


        if(bad > 0) {{

            health =
                limit(
                    health -
                    bad * 0.15
                );

        }}


        updateStats();

    }},
    10000
);


/* =====================================================
   시작
===================================================== */

updateStats();

goCenter();

</script>

</body>

</html>
"""


components.html(
    html,
    height=900,
    scrolling=False
)
