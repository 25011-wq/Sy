import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌 깨기",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 벽돌 깨기")

html_code = """
<!DOCTYPE html>
<html>
<head>

<style>

body {
    margin: 0;
    padding: 0;
    background: #111827;
    font-family: Arial, sans-serif;
    overflow: hidden;
    touch-action: none;
}

#game {
    display: block;
    margin: 0 auto;
    background: #0f172a;
    border: 3px solid #64748b;
    border-radius: 10px;
    max-width: 100%;
    touch-action: none;
}

#info {
    color: white;
    text-align: center;
    font-size: 17px;
    margin: 10px;
}

</style>

</head>

<body>

<div id="info">

단계: <span id="level">1</span>
&nbsp;&nbsp;

점수: <span id="score">0</span>
&nbsp;&nbsp;

❤️ 목숨: <span id="lives">3</span>
&nbsp;&nbsp;

⚪ 공: <span id="ballCount">1</span>

</div>

<canvas id="game" width="700" height="500"></canvas>


<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let score = 0;
let lives = 3;
let level = 1;

let gameOver = false;
let gameWon = false;


// =====================================
// 공 배열
// =====================================

let balls = [];


// =====================================
// 공 하나 생성
// =====================================

function createBall(
    x = canvas.width / 2,
    y = canvas.height - 70,
    dx = null,
    dy = null
) {

    // 기존보다 빠른 속도
    const speed = 5.5 + (level - 1) * 0.6;

    if (dx === null) {
        dx = speed * (Math.random() > 0.5 ? 1 : -1);
    }

    if (dy === null) {
        dy = -speed;
    }

    balls.push({

        x: x,
        y: y,

        radius: 7,

        dx: dx,
        dy: dy,

        // 같은 벽돌에서 여러 번 충돌하는 것을 방지
        lastBrick: null
    });

    updateBallCount();
}


// =====================================
// 처음 공 1개
// =====================================

function resetBalls() {

    balls = [];

    createBall(
        canvas.width / 2,
        canvas.height - 70
    );
}


// =====================================
// 패들
// =====================================

let paddle = {

    width: 110,
    height: 14,

    x: canvas.width / 2 - 55,

    y: canvas.height - 35

};


let leftPressed = false;
let rightPressed = false;


// =====================================
// 키보드
// =====================================

document.addEventListener("keydown", function(e) {

    if (e.key === "ArrowLeft") {
        leftPressed = true;
    }

    if (e.key === "ArrowRight") {
        rightPressed = true;
    }

    if (e.key === " " && (gameOver || gameWon)) {
        restart();
    }

});


document.addEventListener("keyup", function(e) {

    if (e.key === "ArrowLeft") {
        leftPressed = false;
    }

    if (e.key === "ArrowRight") {
        rightPressed = false;
    }

});


// =====================================
// 마우스
// =====================================

canvas.addEventListener("mousemove", function(e) {

    const rect = canvas.getBoundingClientRect();

    const mouseX =
        (e.clientX - rect.left)
        * canvas.width / rect.width;

    movePaddleTo(mouseX);

});


// =====================================
// 스마트폰 터치
// =====================================

canvas.addEventListener(
    "touchstart",
    function(e) {

        e.preventDefault();

        const rect = canvas.getBoundingClientRect();

        const touchX =
            (e.touches[0].clientX - rect.left)
            * canvas.width / rect.width;

        movePaddleTo(touchX);

    },
    { passive: false }
);


canvas.addEventListener(
    "touchmove",
    function(e) {

        e.preventDefault();

        const rect = canvas.getBoundingClientRect();

        const touchX =
            (e.touches[0].clientX - rect.left)
            * canvas.width / rect.width;

        movePaddleTo(touchX);

    },
    { passive: false }
);


function movePaddleTo(x) {

    paddle.x = x - paddle.width / 2;

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }

}


// =====================================
// 벽돌
// =====================================

const rows = 5;
const cols = 9;

const brickWidth = 65;
const brickHeight = 22;
const brickPadding = 10;

const brickStartX = 45;
const brickStartY = 55;

let bricks = [];


function createBricks() {

    bricks = [];

    // 1단계 = 1번
    // 2단계 이상 = 2번

    const hitsNeeded =
        level === 1 ? 1 : 2;


    for (let r = 0; r < rows; r++) {

        bricks[r] = [];

        for (let c = 0; c < cols; c++) {

            bricks[r][c] = {

                x:
                    brickStartX +
                    c * (brickWidth + brickPadding),

                y:
                    brickStartY +
                    r * (brickHeight + brickPadding),

                hits: hitsNeeded

            };

        }

    }

}


// =====================================
// 벽돌 그리기
// =====================================

function drawBricks() {

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            const brick = bricks[r][c];

            if (brick.hits <= 0) {
                continue;
            }


            if (brick.hits === 2) {

                ctx.fillStyle = "#f97316";

            } else {

                ctx.fillStyle = "#38bdf8";

            }


            ctx.beginPath();

            ctx.roundRect(
                brick.x,
                brick.y,
                brickWidth,
                brickHeight,
                5
            );

            ctx.fill();


            // 체력 2 표시

            if (brick.hits === 2) {

                ctx.fillStyle = "white";

                ctx.font = "bold 13px Arial";

                ctx.textAlign = "center";

                ctx.fillText(
                    "2",
                    brick.x + brickWidth / 2,
                    brick.y + 16
                );

            }

        }

    }

}


// =====================================
// 공 그리기
// =====================================

function drawBalls() {

    for (const ball of balls) {

        ctx.beginPath();

        ctx.arc(
            ball.x,
            ball.y,
            ball.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#facc15";

        ctx.fill();

        ctx.closePath();

    }

}


// =====================================
// 패들
// =====================================

function drawPaddle() {

    ctx.fillStyle = "#a78bfa";

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        7
    );

    ctx.fill();

}


// =====================================
// 정보 업데이트
// =====================================

function updateInfo() {

    document.getElementById("level").textContent =
        level;

    document.getElementById("score").textContent =
        score;

    document.getElementById("lives").textContent =
        lives;

    updateBallCount();

}


function updateBallCount() {

    document.getElementById("ballCount").textContent =
        balls.length;

}


// =====================================
// 벽돌 충돌
// =====================================

function collisionDetection(ball) {

    let remaining = 0;


    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            const brick = bricks[r][c];

            if (brick.hits <= 0) {
                continue;
            }

            remaining++;


            // 벽돌 고유 번호

            const brickID =
                r + "-" + c;


            if (
                ball.x + ball.radius > brick.x &&
                ball.x - ball.radius <
                    brick.x + brickWidth &&
                ball.y + ball.radius > brick.y &&
                ball.y - ball.radius <
                    brick.y + brickHeight
            ) {


                // 같은 프레임에서 같은 벽돌에
                // 계속 부딪히는 것을 방지

                if (ball.lastBrick === brickID) {
                    continue;
                }


                ball.lastBrick = brickID;


                // 공 방향 반전

                ball.dy = -ball.dy;


                // 벽돌 체력 감소

                brick.hits--;


                score += 10;


                // =================================
                // ⭐ 벽돌이 완전히 깨졌을 때
                // ⭐ 공을 1개 추가
                // =================================

                if (brick.hits === 0) {

                    score += 20;


                    // 현재 공의 위치에서
                    // 새로운 공 하나 생성

                    createBall(

                        ball.x,

                        ball.y,

                        -ball.dx,

                        ball.dy

                    );

                }


                updateInfo();

            }

        }

    }


    // =================================
    // 모든 벽돌 제거 확인
    // =================================

    let bricksLeft = 0;


    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            if (bricks[r][c].hits > 0) {
                bricksLeft++;
            }

        }

    }


    if (bricksLeft === 0) {

        if (level < 5) {

            level++;


            // 다음 단계

            createBricks();


            // 공은 유지하고
            // 속도만 조금 증가

            for (const b of balls) {

                const currentSpeed =
                    Math.sqrt(
                        b.dx * b.dx +
                        b.dy * b.dy
                    );

                const newSpeed =
                    currentSpeed + 0.8;


                const angle =
                    Math.atan2(b.dy, b.dx);


                b.dx =
                    Math.cos(angle) * newSpeed;

                b.dy =
                    Math.sin(angle) * newSpeed;

            }


            updateInfo();


        } else {

            gameWon = true;

        }

    }

}


// =====================================
// 공 움직이기
// =====================================

function updateBalls() {

    const remainingBalls = [];


    for (const ball of balls) {

        ball.x += ball.dx;
        ball.y += ball.dy;


        // 좌우 벽

        if (
            ball.x + ball.radius >
                canvas.width ||

            ball.x - ball.radius < 0
        ) {

            ball.dx = -ball.dx;

        }


        // 위쪽 벽

        if (ball.y - ball.radius < 0) {

            ball.dy = -ball.dy;

        }


        // 패들

        if (

            ball.y + ball.radius >= paddle.y &&

            ball.y - ball.radius <=
                paddle.y + paddle.height &&

            ball.x >= paddle.x &&

            ball.x <=
                paddle.x + paddle.width &&

            ball.dy > 0

        ) {


            ball.dy =
                -Math.abs(ball.dy);


            const hitPosition =

                (ball.x - paddle.x)
                / paddle.width
                - 0.5;


            ball.dx =
                hitPosition * 12;


            // 너무 느려지지 않도록

            const speed =
                Math.sqrt(
                    ball.dx * ball.dx +
                    ball.dy * ball.dy
                );


            if (speed < 5.5) {

                const factor =
                    5.5 / speed;

                ball.dx *= factor;
                ball.dy *= factor;

            }

        }


        // 벽돌 충돌

        collisionDetection(ball);


        // 바닥

        if (
            ball.y - ball.radius >
            canvas.height
        ) {

            // 이 공은 제거

        } else {

            remainingBalls.push(ball);

        }

    }


    balls = remainingBalls;


    // 공이 하나도 없으면 목숨 감소

    if (balls.length === 0) {

        lives--;

        updateInfo();


        if (lives <= 0) {

            gameOver = true;

        } else {

            resetBalls();

        }

    }


    updateBallCount();

}


// =====================================
// 키보드 패들
// =====================================

function movePaddle() {

    if (leftPressed) {
        paddle.x -= 9;
    }

    if (rightPressed) {
        paddle.x += 9;
    }


    if (paddle.x < 0) {
        paddle.x = 0;
    }


    if (
        paddle.x + paddle.width >
        canvas.width
    ) {

        paddle.x =
            canvas.width - paddle.width;

    }

}


// =====================================
// 다시 시작
// =====================================

function restart() {

    score = 0;

    lives = 3;

    level = 1;

    gameOver = false;

    gameWon = false;


    paddle.x =
        canvas.width / 2 -
        paddle.width / 2;


    createBricks();

    resetBalls();

    updateInfo();

}


// =====================================
// 게임 화면
// =====================================

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    drawBricks();

    drawBalls();

    drawPaddle();


    if (
        !gameOver &&
        !gameWon
    ) {

        movePaddle();

        updateBalls();


    } else {


        ctx.fillStyle =
            "rgba(0,0,0,0.7)";


        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );


        ctx.textAlign =
            "center";


        ctx.font =
            "bold 42px Arial";


        ctx.fillStyle =
            "white";


        if (gameWon) {

            ctx.fillText(
                "🎉 YOU WIN!",
                canvas.width / 2,
                canvas.height / 2
            );

        } else {

            ctx.fillText(
                "GAME OVER",
                canvas.width / 2,
                canvas.height / 2
            );

        }


        ctx.font =
            "20px Arial";


        ctx.fillText(
            "스페이스바를 눌러 다시 시작",
            canvas.width / 2,
            canvas.height / 2 + 45
        );

    }


    requestAnimationFrame(draw);

}


// =====================================
// 시작
// =====================================

createBricks();

resetBalls();

updateInfo();

draw();

</script>

</body>
</html>
"""

components.html(
    html_code,
    height=560,
    scrolling=False
)
