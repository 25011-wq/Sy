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
        font-size: 18px;
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

// ====================
// 공
// ====================

let ball = {
    x: canvas.width / 2,
    y: canvas.height - 70,
    radius: 8,
    dx: 4,
    dy: -4
};


// ====================
// 패들
// ====================

let paddle = {
    width: 110,
    height: 14,
    x: canvas.width / 2 - 55,
    y: canvas.height - 35
};

let leftPressed = false;
let rightPressed = false;


// ====================
// 키보드 조작
// ====================

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


// ====================
// 마우스 조작
// ====================

canvas.addEventListener("mousemove", function(e) {

    const rect = canvas.getBoundingClientRect();

    const mouseX =
        (e.clientX - rect.left)
        * canvas.width / rect.width;

    movePaddleTo(mouseX);
});


// ====================
// 스마트폰 손가락 드래그
// ====================

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


// ====================
// 벽돌 설정
// ====================

const rows = 5;
const cols = 9;

const brickWidth = 65;
const brickHeight = 22;
const brickPadding = 10;

const brickStartX = 45;
const brickStartY = 55;

let bricks = [];


// 단계별 벽돌 체력
// 1단계 = 1번
// 2단계 이상 = 2번

function createBricks() {

    bricks = [];

    const hitsNeeded = level === 1 ? 1 : 2;

    for (let r = 0; r < rows; r++) {

        bricks[r] = [];

        for (let c = 0; c < cols; c++) {

            bricks[r][c] = {

                x: brickStartX +
                   c * (brickWidth + brickPadding),

                y: brickStartY +
                   r * (brickHeight + brickPadding),

                hits: hitsNeeded
            };
        }
    }
}

createBricks();


// ====================
// 벽돌 그리기
// ====================

function drawBricks() {

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            let brick = bricks[r][c];

            if (brick.hits <= 0) {
                continue;
            }

            // 체력이 2인 벽돌은 조금 다르게 표시
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

            // 2번 맞아야 하는 벽돌에는 표시
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


// ====================
// 공 그리기
// ====================

function drawBall() {

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


// ====================
// 패들 그리기
// ====================

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


// ====================
// 정보 표시
// ====================

function updateInfo() {

    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;
    document.getElementById("level").textContent = level;
}


// ====================
// 벽돌 충돌
// ====================

function collisionDetection() {

    let remaining = 0;

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            let brick = bricks[r][c];

            if (brick.hits <= 0) {
                continue;
            }

            remaining++;

            if (
                ball.x > brick.x &&
                ball.x < brick.x + brickWidth &&
                ball.y - ball.radius < brick.y + brickHeight &&
                ball.y + ball.radius > brick.y
            ) {

                ball.dy = -ball.dy;

                // 벽돌 체력 감소
                brick.hits--;

                // 맞을 때마다 점수
                score += 10;

                updateInfo();

                // 벽돌이 완전히 깨졌다면
                if (brick.hits === 0) {
                    score += 10;
                }
            }
        }
    }

    // 모든 벽돌 제거
    if (remaining === 0) {

        if (level < 5) {

            level++;

            // 단계가 올라갈수록 공 속도 증가
            let speedMultiplier =
                1 + (level - 1) * 0.12;

            ball.dx =
                (ball.dx > 0 ? 1 : -1)
                * 4
                * speedMultiplier;

            ball.dy =
                (ball.dy > 0 ? 1 : -1)
                * 4
                * speedMultiplier;

            createBricks();

            resetBall();

        } else {

            gameWon = true;
        }

        updateInfo();
    }
}


// ====================
// 공 움직이기
// ====================

function updateBall() {

    ball.x += ball.dx;
    ball.y += ball.dy;


    // 좌우 벽

    if (
        ball.x + ball.radius > canvas.width ||
        ball.x - ball.radius < 0
    ) {

        ball.dx = -ball.dx;
    }


    // 위쪽 벽

    if (ball.y - ball.radius < 0) {

        ball.dy = -ball.dy;
    }


    // 패들 충돌

    if (
        ball.y + ball.radius >= paddle.y &&
        ball.y - ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width &&
        ball.dy > 0
    ) {

        ball.dy = -Math.abs(ball.dy);

        // 패들에 맞은 위치에 따라 방향 변화
        const hitPosition =
            (ball.x - paddle.x)
            / paddle.width - 0.5;

        ball.dx = hitPosition * 10;
    }


    // 공이 바닥으로 떨어짐

    if (ball.y - ball.radius > canvas.height) {

        lives--;

        updateInfo();

        if (lives <= 0) {

            gameOver = true;

        } else {

            resetBall();
        }
    }
}


// ====================
// 공 초기화
// ====================

function resetBall() {

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 70;

    const speed =
        4 + (level - 1) * 0.5;

    ball.dx =
        speed *
        (Math.random() > 0.5 ? 1 : -1);

    ball.dy = -speed;
}


// ====================
// 키보드 패들 이동
// ====================

function movePaddle() {

    if (leftPressed) {
        paddle.x -= 8;
    }

    if (rightPressed) {
        paddle.x += 8;
    }

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > canvas.width) {
        paddle.x = canvas.width - paddle.width;
    }
}


// ====================
// 게임 다시 시작
// ====================

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
    resetBall();
    updateInfo();
}


// ====================
// 게임 화면
// ====================

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawBall();
    drawPaddle();


    if (!gameOver && !gameWon) {

        movePaddle();
        updateBall();
        collisionDetection();

    } else {

        ctx.fillStyle =
            "rgba(0,0,0,0.7)";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.textAlign = "center";

        ctx.font = "bold 42px Arial";
        ctx.fillStyle = "white";


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


        ctx.font = "20px Arial";

        ctx.fillText(
            "스페이스바를 눌러 다시 시작",
            canvas.width / 2,
            canvas.height / 2 + 45
        );
    }

    requestAnimationFrame(draw);
}


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
