import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Turbo Track Legends",
    page_icon="🏎️",
    layout="wide"
)

# -----------------------------
# Streamlit Session State
# -----------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_instance" not in st.session_state:
    st.session_state.game_instance = 0

# -----------------------------
# Actions
# -----------------------------
def start_game():
    st.session_state.game_started = True
    st.session_state.game_instance += 1

def stop_game():
    st.session_state.game_started = False

def restart_game():
    st.session_state.game_started = True
    st.session_state.game_instance += 1

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
    color: white;
}

.sub-title {
    text-align: center;
    font-size: 1.05rem;
    color: #94a3b8;
    margin-bottom: 1.2rem;
}

.info-box {
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    margin-bottom: 14px;
}

.info-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: white;
}

.info-text {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.6;
}

.status-box {
    background: linear-gradient(135deg, #111827, #0f172a);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    color: white;
    margin-top: 8px;
}

.control-note {
    text-align: center;
    color: #cbd5e1;
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🏎️ Turbo Track Legends</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Drive with arrow keys, race against AI cars, and avoid every collision.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Controls
# -----------------------------
btn1, btn2, btn3 = st.columns(3)

with btn1:
    if st.button("▶️ Start Game", use_container_width=True):
        start_game()

with btn2:
    if st.button("⏹️ Stop Game", use_container_width=True):
        stop_game()

with btn3:
    if st.button("🔄 Restart Game", use_container_width=True):
        restart_game()

# -----------------------------
# Info cards
# -----------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="info-box">
        <div class="info-title">🎮 Controls</div>
        <div class="info-text">
            ⬆️ Arrow Up = Accelerate<br>
            ⬇️ Arrow Down = Brake<br>
            ⬅️ Arrow Left = Move Left<br>
            ➡️ Arrow Right = Move Right
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-box">
        <div class="info-title">🏁 Rules</div>
        <div class="info-text">
            Touching any AI car = Game Over<br>
            Touching traffic car = Game Over<br>
            Complete all laps to finish race
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    status_text = "Running" if st.session_state.game_started else "Stopped"
    st.markdown(f"""
    <div class="info-box">
        <div class="info-title">📡 Game Status</div>
        <div class="info-text">
            Current state: <b>{status_text}</b><br>
            Click inside game area before using keyboard
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div class="control-note">Click inside the game canvas first, then use your keyboard arrows.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Game HTML / JS
# -----------------------------
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Turbo Track Legends</title>
<style>
    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        background: #08111f;
        color: white;
        font-family: Arial, sans-serif;
        overflow: hidden;
    }}

    .game-shell {{
        width: 100%;
        display: flex;
        justify-content: center;
        padding: 10px 0 0 0;
    }}

    .game-wrap {{
        position: relative;
        width: 1000px;
        height: 680px;
    }}

    canvas {{
        display: block;
        background: linear-gradient(#0f172a, #111827);
        border: 2px solid #334155;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.45);
    }}
</style>
</head>
<body>
    <div class="game-shell">
        <div class="game-wrap">
            <canvas id="gameCanvas" width="1000" height="680"></canvas>
        </div>
    </div>

<script>
const GAME_STARTED = {str(st.session_state.game_started).lower()};
const GAME_INSTANCE = {st.session_state.game_instance};

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

const road = {{
    x: 220,
    width: 560,
    laneCount: 4,
    laneWidth: 560 / 4
}};

const lapsToFinish = 3;
const finishDistance = 7500;

let gameOver = false;
let gameFinished = false;
let stopped = !GAME_STARTED;
let playerWon = false;
let roadScroll = 0;

const keys = {{
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false
}};

const player = {{
    x: road.x + road.laneWidth * 1.5 - 22,
    y: H - 130,
    w: 44,
    h: 84,
    speed: 0,
    maxSpeed: 9.0,
    accel: 0.20,
    brake: 0.25,
    friction: 0.06,
    color: "#22c55e",
    distance: 0,
    lap: 1,
    finished: false,
    rank: 1
}};

const aiCars = [
    {{
        name: "Blaze AI",
        x: road.x + road.laneWidth * 0.5 - 22,
        y: H - 250,
        w: 44,
        h: 84,
        speed: 5.4,
        color: "#ef4444",
        distance: 0,
        lap: 1,
        finished: false
    }},
    {{
        name: "Vortex AI",
        x: road.x + road.laneWidth * 2.5 - 22,
        y: H - 360,
        w: 44,
        h: 84,
        speed: 5.7,
        color: "#3b82f6",
        distance: 0,
        lap: 1,
        finished: false
    }},
    {{
        name: "Titan AI",
        x: road.x + road.laneWidth * 3.5 - 22,
        y: H - 470,
        w: 44,
        h: 84,
        speed: 5.2,
        color: "#f59e0b",
        distance: 0,
        lap: 1,
        finished: false
    }}
];

const traffic = [];

function createTrafficCar() {{
    const lane = Math.floor(Math.random() * road.laneCount);
    return {{
        x: road.x + lane * road.laneWidth + road.laneWidth / 2 - 20,
        y: -120 - Math.random() * 1400,
        w: 40,
        h: 74,
        speed: 3 + Math.random() * 2.2,
        color: ["#a855f7", "#06b6d4", "#e11d48", "#84cc16", "#f97316"][Math.floor(Math.random() * 5)]
    }};
}}

for (let i = 0; i < 9; i++) {{
    traffic.push(createTrafficCar());
}}

document.addEventListener("keydown", (e) => {{
    if (keys.hasOwnProperty(e.key)) {{
        keys[e.key] = true;
        e.preventDefault();
    }}
}});

document.addEventListener("keyup", (e) => {{
    if (keys.hasOwnProperty(e.key)) {{
        keys[e.key] = false;
        e.preventDefault();
    }}
}});

function rectsCollide(a, b) {{
    return (
        a.x < b.x + b.w &&
        a.x + a.w > b.x &&
        a.y < b.y + b.h &&
        a.y + a.h > b.y
    );
}}

function getStandings() {{
    return [
        {{name: "You", dist: player.distance}},
        ...aiCars.map(c => ({{name: c.name, dist: c.distance}}))
    ].sort((a, b) => b.dist - a.dist);
}}

function updatePlayerRank() {{
    const standings = getStandings();
    player.rank = standings.findIndex(s => s.name === "You") + 1;
}}

function drawBackground() {{
    ctx.fillStyle = "#14532d";
    ctx.fillRect(0, 0, road.x, H);
    ctx.fillRect(road.x + road.width, 0, W - (road.x + road.width), H);
}}

function drawRoad() {{
    drawBackground();

    ctx.fillStyle = "#1f2937";
    ctx.fillRect(road.x, 0, road.width, H);

    ctx.strokeStyle = "#94a3b8";
    ctx.lineWidth = 6;
    ctx.strokeRect(road.x, 0, road.width, H);

    ctx.lineWidth = 4;
    ctx.strokeStyle = "#f8fafc";

    for (let i = 1; i < road.laneCount; i++) {{
        const lx = road.x + i * road.laneWidth;
        for (let y = -50; y < H + 50; y += 70) {{
            ctx.beginPath();
            ctx.moveTo(lx, y + (roadScroll % 70));
            ctx.lineTo(lx, y + 38 + (roadScroll % 70));
            ctx.stroke();
        }}
    }}
}}

function drawCar(car, label = null) {{
    ctx.fillStyle = car.color;
    ctx.fillRect(car.x, car.y, car.w, car.h);

    ctx.fillStyle = "#0f172a";
    ctx.fillRect(car.x + 6, car.y + 10, car.w - 12, 16);
    ctx.fillRect(car.x + 6, car.y + 40, car.w - 12, 20);

    ctx.fillStyle = "#111827";
    ctx.fillRect(car.x - 3, car.y + 12, 6, 18);
    ctx.fillRect(car.x + car.w - 3, car.y + 12, 6, 18);
    ctx.fillRect(car.x - 3, car.y + 54, 6, 18);
    ctx.fillRect(car.x + car.w - 3, car.y + 54, 6, 18);

    if (label) {{
        ctx.fillStyle = "white";
        ctx.font = "bold 14px Arial";
        ctx.fillText(label, car.x - 2, car.y - 10);
    }}
}}

function drawTraffic() {{
    traffic.forEach(car => drawCar(car));
}}

function drawHUD() {{
    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(18, 18, 300, 140);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(18, 18, 300, 140);

    ctx.fillStyle = "white";
    ctx.font = "bold 23px Arial";
    ctx.fillText("PLAYER HUD", 32, 46);

    ctx.font = "18px Arial";
    ctx.fillText("Speed: " + player.speed.toFixed(1), 32, 78);
    ctx.fillText("Lap: " + player.lap + " / " + lapsToFinish, 32, 106);
    ctx.fillText("Rank: #" + player.rank, 32, 134);

    const standings = getStandings();

    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(W - 260, 18, 230, 150);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(W - 260, 18, 230, 150);

    ctx.fillStyle = "white";
    ctx.font = "bold 22px Arial";
    ctx.fillText("STANDINGS", W - 243, 46);

    ctx.font = "17px Arial";
    standings.forEach((s, i) => {{
        ctx.fillText((i + 1) + ". " + s.name, W - 243, 76 + i * 25);
    }});

    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(18, H - 72, 380, 48);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(18, H - 72, 380, 48);

    ctx.fillStyle = "white";
    ctx.font = "17px Arial";
    const progress = Math.min(100, (player.distance / finishDistance) * 100).toFixed(0);
    ctx.fillText("Race Progress: " + progress + "%", 34, H - 41);
}}

function updatePlayer() {{
    if (keys.ArrowUp) player.speed += player.accel;
    if (keys.ArrowDown) player.speed -= player.brake;

    if (!keys.ArrowUp && !keys.ArrowDown) {{
        if (player.speed > 0) {{
            player.speed -= player.friction;
        }}
    }}

    if (player.speed < 0) player.speed = 0;
    if (player.speed > player.maxSpeed) player.speed = player.maxSpeed;

    if (keys.ArrowLeft) player.x -= 5.5;
    if (keys.ArrowRight) player.x += 5.5;

    if (player.x < road.x + 8) player.x = road.x + 8;
    if (player.x + player.w > road.x + road.width - 8) {{
        player.x = road.x + road.width - player.w - 8;
    }}

    player.distance += player.speed;
    player.lap = Math.min(lapsToFinish, Math.floor(player.distance / (finishDistance / lapsToFinish)) + 1);

    if (player.distance >= finishDistance) {{
        player.finished = true;
        gameFinished = true;
        gameOver = true;
        updatePlayerRank();
        playerWon = player.rank === 1;
    }}
}}

function updateAI() {{
    aiCars.forEach((car) => {{
        if (!car.finished) {{
            const wobble = (Math.random() - 0.5) * 1.0;
            car.x += wobble;

            const minX = road.x + 8;
            const maxX = road.x + road.width - car.w - 8;

            if (car.x < minX) car.x = minX;
            if (car.x > maxX) car.x = maxX;

            car.distance += car.speed + (Math.random() - 0.5) * 0.16;
            car.lap = Math.min(lapsToFinish, Math.floor(car.distance / (finishDistance / lapsToFinish)) + 1);

            if (car.distance >= finishDistance) {{
                car.finished = true;
            }}
        }}
    }});
}}

function updateTraffic() {{
    roadScroll += player.speed * 1.8;

    traffic.forEach((car) => {{
        car.y += car.speed + player.speed * 0.48;

        if (car.y > H + 120) {{
            const newCar = createTrafficCar();
            car.x = newCar.x;
            car.y = newCar.y;
            car.w = newCar.w;
            car.h = newCar.h;
            car.speed = newCar.speed;
            car.color = newCar.color;
        }}
    }});
}}

function checkCollisions() {{
    for (let i = 0; i < aiCars.length; i++) {{
        if (rectsCollide(player, aiCars[i])) {{
            gameOver = true;
            gameFinished = false;
            playerWon = false;
            stopped = true;
            return;
        }}
    }}

    for (let i = 0; i < traffic.length; i++) {{
        if (rectsCollide(player, traffic[i])) {{
            gameOver = true;
            gameFinished = false;
            playerWon = false;
            stopped = true;
            return;
        }}
    }}
}}

function drawCenteredMessage(title, subtitle, color1, color2) {{
    ctx.fillStyle = "rgba(0,0,0,0.70)";
    ctx.fillRect(0, 0, W, H);

    const boxW = 520;
    const boxH = 220;
    const boxX = (W - boxW) / 2;
    const boxY = (H - boxH) / 2;

    const grad = ctx.createLinearGradient(boxX, boxY, boxX + boxW, boxY + boxH);
    grad.addColorStop(0, color1);
    grad.addColorStop(1, color2);

    ctx.fillStyle = grad;
    ctx.fillRect(boxX, boxY, boxW, boxH);

    ctx.strokeStyle = "rgba(255,255,255,0.18)";
    ctx.lineWidth = 2;
    ctx.strokeRect(boxX, boxY, boxW, boxH);

    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.font = "bold 44px Arial";
    ctx.fillText(title, W / 2, boxY + 82);

    ctx.font = "24px Arial";
    ctx.fillText(subtitle, W / 2, boxY + 132);

    ctx.font = "18px Arial";
    ctx.fillText("Use Streamlit buttons above to start, stop, or restart.", W / 2, boxY + 175);
    ctx.textAlign = "left";
}}

function drawStartScreen() {{
    drawRoad();
    drawTraffic();
    aiCars.forEach((car) => drawCar(car, car.name));
    drawCar(player, "YOU");
    drawHUD();
    drawCenteredMessage("READY TO RACE", "Click Start Game to begin", "#1d4ed8", "#0f172a");
}}

function drawPausedScreen() {{
    drawRoad();
    drawTraffic();
    aiCars.forEach((car) => drawCar(car, car.name));
    drawCar(player, "YOU");
    drawHUD();
    drawCenteredMessage("GAME STOPPED", "Click Start Game to play again", "#7c2d12", "#111827");
}}

function drawGameOverScreen() {{
    drawRoad();
    drawTraffic();
    aiCars.forEach((car) => drawCar(car, car.name));
    drawCar(player, "YOU");
    drawHUD();
    drawCenteredMessage("GAME OVER", "Your car crashed into another car", "#991b1b", "#111827");
}}

function drawWinScreen() {{
    drawRoad();
    drawTraffic();
    aiCars.forEach((car) => drawCar(car, car.name));
    drawCar(player, "YOU");
    drawHUD();

    if (playerWon) {{
        drawCenteredMessage("YOU WIN", "You finished the race in 1st place", "#166534", "#0f172a");
    }} else {{
        drawCenteredMessage("RACE FINISHED", "You completed the race", "#1e40af", "#111827");
    }}
}}

function gameLoop() {{
    ctx.clearRect(0, 0, W, H);

    if (!GAME_STARTED && !gameOver) {{
        drawStartScreen();
        requestAnimationFrame(gameLoop);
        return;
    }}

    if (stopped && !gameOver) {{
        drawPausedScreen();
        requestAnimationFrame(gameLoop);
        return;
    }}

    if (!gameOver) {{
        updatePlayer();
        updateAI();
        updateTraffic();
        checkCollisions();
        updatePlayerRank();
    }}

    drawRoad();
    drawTraffic();
    aiCars.forEach((car) => drawCar(car, car.name));
    drawCar(player, "YOU");
    drawHUD();

    if (gameOver) {{
        if (gameFinished) {{
            drawWinScreen();
        }} else {{
            drawGameOverScreen();
        }}
    }}

    requestAnimationFrame(gameLoop);
}}

gameLoop();
</script>
</body>
</html>
"""

components.html(game_html, height=710)

st.markdown("""
<div class="status-box">
    <b>Note:</b> If you press <b>Stop Game</b>, the current race stops. 
    Press <b>Start Game</b> again to launch a fresh run, or use <b>Restart Game</b> to reload the race instantly.
</div>
""", unsafe_allow_html=True)
