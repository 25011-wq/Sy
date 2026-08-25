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
// 최대 공 개수
// =====================================

const MAX_BALLS = 5;


// =====================================
// 공 배열
// =====================================

let balls = [];


// =====================================
// 공 생성
// =====================================

function createBall(
    x = canvas.width / 2,
    y = canvas.height - 70,
    dx = null,
    dy = null
) {

    // 최대 5개 제한
    if (balls.length >= MAX_BALLS) {
        return;
    }

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
        lastBrick: null
    });

    updateBallCount();
}


// =====================================
// 공 초기화
// 단계가 바뀌면 항상 공 1개
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

    if (gameOver || gameWon) {
        return;
    }

    const rect = canvas.getBoundingClientRect();

    const mouseX =
        (e.clientX - rect.left)
        * canvas.width / rect.width;

    movePaddleTo(mouseX);
});


// =====================================
// 터치
// =====================================

canvas.addEventListener(
    "touchstart",
    function(e) {

        e.preventDefault();

        // 게임 오버 → 터치해서 재시작
        if (gameOver || gameWon) {
            restart();
            return;
        }

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

        if (gameOver || gameWon) {
            return;
        }

        const rect = canvas.getBoundingClientRect();

        const touchX =
            (e.touches[0].clientX - rect.left)
            * canvas.width / rect.width;

        movePaddleTo(touchX);

    },
    { passive: false }
);


function movePaddleTo(x) {

    paddle.x =
        x - paddle.width / 2;

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


// =====================================
// 벽돌 생성
// =====================================

function createBricks() {

    bricks = [];

    // 1단계 = 1번
    // 2, 3단계 = 2번

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


            // 2번 맞아야 하는 벽돌
            if (brick.hits === 2) {

                ctx.fillStyle = "white";

                ctx.font =
                    "bold 13px Arial";

                ctx.textAlign =
                    "center";

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
// 정보
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

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            const brick = bricks[r][c];

            if (brick.hits <= 0) {
                continue;
            }


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
                // 벽돌이 완전히 깨졌을 때
                // 공 +1
                // =================================

                if (brick.hits === 0) {

                    score += 20;

                    // 최대 5개까지만 생성
                    if (balls.length < MAX_BALLS) {

                        createBall(
                            ball.x,
                            ball.y,
                            -ball.dx,
                            ball.dy
                        );

                    }

                }

                updateInfo();

            }

        }

    }


    // =================================
    // 남은 벽돌 확인
    // =================================

    let bricksLeft = 0;

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            if (bricks[r][c].hits > 0) {
                bricksLeft++;
            }

        }

    }


    // =================================
    // 단계 클리어
    // =================================

    if (bricksLeft === 0) {


        // 1 → 2 → 3

        if (level < 3) {

            level++;


            // ⭐ 단계가 바뀌면 공 1개로 초기화

            resetBalls();


            // 새로운 벽돌

            createBricks();


            // 단계가 올라갈수록 속도 증가

            for (const b of balls) {

                const speed =
                    5.5 +
                    (level - 1) * 0.8;

                const angle =
                    Math.atan2(
                        b.dy,
                        b.dx
                    );

                b.dx =
                    Math.cos(angle) * speed;

                b.dy =
                    Math.sin(angle) * speed;

            }


            updateInfo();


        } else {

            // 3단계 클리어

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


        // 위쪽

        if (
            ball.y - ball.radius < 0
        ) {

            ball.dy = -ball.dy;

        }


        // 패들

        if (

            ball.y + ball.radius >=
                paddle.y &&

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


            // 최소 속도 보장

            const speed =
                Math.sqrt(
                    ball.dx * ball.dx +
                    ball.dy * ball.dy
                );


            const minSpeed =
                5.5 +
                (level - 1) * 0.6;


            if (speed < minSpeed) {

                const factor =
                    minSpeed / speed;

                ball.dx *= factor;
                ball.dy *= factor;

            }

        }


        // 벽돌

        collisionDetection(ball);


        // 바닥

        if (
            ball.y - ball.radius >
            canvas.height
        ) {

            // 공 제거

        } else {

            remainingBalls.push(ball);

        }

    }


    balls = remainingBalls;


    // 모든 공을 놓쳤을 때

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
            canvas.width -
            paddle.width;

    }

}


// =====================================
// 재시작
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


        // 어두운 화면

        ctx.fillStyle =
            "rgba(0,0,0,0.72)";

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
                canvas.height / 2 - 20
            );

            ctx.font =
                "20px Arial";

            ctx.fillText(
                "화면을 터치해서 다시 시작",
                canvas.width / 2,
                canvas.height / 2 + 30
            );

        } else {

            ctx.fillText(
                "GAME OVER",
                canvas.width / 2,
                canvas.height / 2 - 20
            );

            ctx.font =
                "20px Arial";

            ctx.fillText(
                "화면을 터치해서 다시 시작",
                canvas.width / 2,
                canvas.height / 2 + 30
            );

        }

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
