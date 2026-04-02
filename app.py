import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Turbo Track Legends",
    page_icon="🏎️",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.sub-title {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 1.2rem;
}
.info-box {
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏎️ Turbo Track Legends</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Use arrow keys to control your car. Race against AI cars, avoid traffic, and survive the laps.</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="info-box">
        <b>Controls</b><br>
        ⬆️ Accelerate<br>
        ⬇️ Brake<br>
        ⬅️ Move Left<br>
        ➡️ Move Right
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-box">
        <b>Game Goal</b><br>
        Complete 3 laps before AI cars.<br>
        Avoid collisions and stay on track.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="info-box">
        <b>Tip</b><br>
        Click inside the game area first,<br>
        then use your keyboard arrows.
    </div>
    """, unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>Turbo Track Legends</title>
<style>
    body {
        margin: 0;
        background: #0b1020;
        color: white;
        font-family: Arial, sans-serif;
        overflow: hidden;
    }
    .wrap {
        display: flex;
        justify-content: center;
        padding: 10px 0;
    }
    canvas {
        background: linear-gradient(#0f172a, #111827);
        border: 2px solid #334155;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    }
</style>
</head>
<body>
<div class="wrap">
    <canvas id="gameCanvas" width="1000" height="650"></canvas>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

const road = {
    x: 220,
    width: 560,
    laneCount: 4,
    laneWidth: 560 / 4
};

let gameOver = false;
let gameWon = false;
let lapsToFinish = 3;
let finishDistance = 7000;

const keys = {
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false
};

const player = {
    x: road.x + road.laneWidth * 1.5 - 22,
    y: H - 140,
    w: 44,
    h: 80,
    speed: 0,
    maxSpeed: 8.5,
    accel: 0.18,
    brake: 0.22,
    friction: 0.06,
    color: "#22c55e",
    distance: 0,
    lap: 1,
    finished: false,
    rank: 1
};

const aiCars = [
    {
        name: "Blaze AI",
        x: road.x + road.laneWidth * 0.5 - 22,
        y: H - 260,
        w: 44,
        h: 80,
        speed: 5.3,
        color: "#ef4444",
        distance: 0,
        lap: 1,
        finished: false
    },
    {
        name: "Vortex AI",
        x: road.x + road.laneWidth * 2.5 - 22,
        y: H - 360,
        w: 44,
        h: 80,
        speed: 5.6,
        color: "#3b82f6",
        distance: 0,
        lap: 1,
        finished: false
    },
    {
        name: "Titan AI",
        x: road.x + road.laneWidth * 3.5 - 22,
        y: H - 460,
        w: 44,
        h: 80,
        speed: 5.1,
        color: "#f59e0b",
        distance: 0,
        lap: 1,
        finished: false
    }
];

const traffic = [];

function makeTrafficCar() {
    const lane = Math.floor(Math.random() * road.laneCount);
    return {
        x: road.x + lane * road.laneWidth + road.laneWidth / 2 - 20,
        y: -120 - Math.random() * 600,
        w: 40,
        h: 72,
        speed: 3 + Math.random() * 2.5,
        color: ["#a855f7", "#06b6d4", "#e11d48", "#84cc16"][Math.floor(Math.random() * 4)]
    };
}

for (let i = 0; i < 8; i++) {
    traffic.push(makeTrafficCar());
}

let roadScroll = 0;

document.addEventListener("keydown", (e) => {
    if (keys.hasOwnProperty(e.key)) {
        keys[e.key] = true;
        e.preventDefault();
    }
});

document.addEventListener("keyup", (e) => {
    if (keys.hasOwnProperty(e.key)) {
        keys[e.key] = false;
        e.preventDefault();
    }
});

function rectsCollide(a, b) {
    return (
        a.x < b.x + b.w &&
        a.x + a.w > b.x &&
        a.y < b.y + b.h &&
        a.y + a.h > b.y
    );
}

function drawRoad() {
    ctx.fillStyle = "#1f2937";
    ctx.fillRect(road.x, 0, road.width, H);

    ctx.strokeStyle = "#94a3b8";
    ctx.lineWidth = 6;
    ctx.strokeRect(road.x, 0, road.width, H);

    ctx.lineWidth = 4;
    ctx.strokeStyle = "#f8fafc";
    for (let i = 1; i < road.laneCount; i++) {
        const lx = road.x + i * road.laneWidth;
        for (let y = -40; y < H + 40; y += 60) {
            ctx.beginPath();
            ctx.moveTo(lx, y + (roadScroll % 60));
            ctx.lineTo(lx, y + 30 + (roadScroll % 60));
            ctx.stroke();
        }
    }

    ctx.fillStyle = "#14532d";
    ctx.fillRect(0, 0, road.x, H);
    ctx.fillRect(road.x + road.width, 0, W - (road.x + road.width), H);
}

function drawCar(car, label=null) {
    ctx.fillStyle = car.color;
    ctx.fillRect(car.x, car.y, car.w, car.h);

    ctx.fillStyle = "#0f172a";
    ctx.fillRect(car.x + 6, car.y + 10, car.w - 12, 16);
    ctx.fillRect(car.x + 6, car.y + 38, car.w - 12, 18);

    ctx.fillStyle = "#111827";
    ctx.fillRect(car.x - 3, car.y + 12, 6, 18);
    ctx.fillRect(car.x + car.w - 3, car.y + 12, 6, 18);
    ctx.fillRect(car.x - 3, car.y + 50, 6, 18);
    ctx.fillRect(car.x + car.w - 3, car.y + 50, 6, 18);

    if (label) {
        ctx.fillStyle = "white";
        ctx.font = "bold 14px Arial";
        ctx.fillText(label, car.x - 5, car.y - 8);
    }
}

function drawHUD() {
    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(18, 18, 280, 120);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(18, 18, 280, 120);

    ctx.fillStyle = "white";
    ctx.font = "bold 22px Arial";
    ctx.fillText("PLAYER HUD", 32, 46);

    ctx.font = "18px Arial";
    ctx.fillText("Speed: " + player.speed.toFixed(1), 32, 76);
    ctx.fillText("Lap: " + player.lap + " / " + lapsToFinish, 32, 102);
    ctx.fillText("Progress: " + Math.min(100, (player.distance / finishDistance) * 100).toFixed(0) + "%", 32, 128);

    const standings = [
        {name: "You", dist: player.distance},
        ...aiCars.map(c => ({name: c.name, dist: c.distance}))
    ].sort((a, b) => b.dist - a.dist);

    player.rank = standings.findIndex(s => s.name === "You") + 1;

    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(W - 260, 18, 230, 150);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(W - 260, 18, 230, 150);

    ctx.fillStyle = "white";
    ctx.font = "bold 22px Arial";
    ctx.fillText("STANDINGS", W - 242, 46);

    ctx.font = "17px Arial";
    standings.forEach((s, i) => {
        ctx.fillText((i + 1) + ". " + s.name, W - 242, 76 + i * 24);
    });
}

function updatePlayer() {
    if (keys.ArrowUp) player.speed += player.accel;
    if (keys.ArrowDown) player.speed -= player.brake;

    if (!keys.ArrowUp && !keys.ArrowDown) {
        if (player.speed > 0) player.speed -= player.friction;
        if (player.speed < 0) player.speed = 0;
    }

    if (player.speed > player.maxSpeed) player.speed = player.maxSpeed;
    if (player.speed < 0) player.speed = 0;

    if (keys.ArrowLeft) player.x -= 5.5;
    if (keys.ArrowRight) player.x += 5.5;

    if (player.x < road.x + 8) player.x = road.x + 8;
    if (player.x + player.w > road.x + road.width - 8) {
        player.x = road.x + road.width - player.w - 8;
    }

    player.distance += player.speed;
    player.lap = Math.min(lapsToFinish, Math.floor(player.distance / (finishDistance / lapsToFinish)) + 1);

    if (player.distance >= finishDistance) {
        player.finished = true;
        gameWon = player.rank === 1;
        gameOver = true;
    }
}

function updateAI() {
    aiCars.forEach((car) => {
        if (!car.finished) {
            const wobble = (Math.random() - 0.5) * 1.4;
            car.x += wobble;

            const minX = road.x + 8;
            const maxX = road.x + road.width - car.w - 8;
            if (car.x < minX) car.x = minX;
            if (car.x > maxX) car.x = maxX;

            car.distance += car.speed + (Math.random() - 0.5) * 0.15;
            car.lap = Math.min(lapsToFinish, Math.floor(car.distance / (finishDistance / lapsToFinish)) + 1);

            if (car.distance >= finishDistance) {
                car.finished = true;
            }
        }
    });
}

function updateTraffic() {
    roadScroll += player.speed * 1.7;

    traffic.forEach((car) => {
        car.y += car.speed + player.speed * 0.45;

        if (car.y > H + 120) {
            Object.assign(car, makeTrafficCar());
        }

        if (rectsCollide(player, car)) {
            player.speed *= 0.45;
        }
    });
}

function drawTraffic() {
    traffic.forEach((car) => drawCar(car));
}

function drawFinishStatus() {
    if (!gameOver) return;

    ctx.fillStyle = "rgba(0,0,0,0.65)";
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.font = "bold 44px Arial";
    ctx.fillText(gameWon ? "🏆 YOU WIN!" : "🏁 RACE FINISHED", W / 2, H / 2 - 30);

    ctx.font = "24px Arial";
    ctx.fillText("Your Rank: #" + player.rank, W / 2, H / 2 + 20);
    ctx.fillText("Refresh the page to play again", W / 2, H / 2 + 65);
    ctx.textAlign = "left";
}

function gameLoop() {
    ctx.clearRect(0, 0, W, H);

    drawRoad();

    if (!gameOver) {
        updatePlayer();
        updateAI();
        updateTraffic();

        aiCars.forEach((car) => {
            if (rectsCollide(player, car)) {
                player.speed *= 0.55;
            }
        });
    }

    drawTraffic();
    aiCars.forEach((car) => drawCar(car, car.name));
    drawCar(player, "YOU");
    drawHUD();
    drawFinishStatus();

    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
"""

components.html(game_html, height=690)

st.caption("Deploy this on GitHub and connect the repo to Streamlit Community Cloud.")
