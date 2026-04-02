import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Turbo Track Legends",
    page_icon="🏎️",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_instance" not in st.session_state:
    st.session_state.game_instance = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

if "selected_car" not in st.session_state:
    st.session_state.selected_car = "Thunder GT"

# -----------------------------
# Car Data
# -----------------------------
car_options = {
    "Thunder GT": {
        "color": "#22c55e",
        "max_speed": 9.2,
        "accel": 0.21,
        "brake": 0.26,
        "handling": 5.8,
        "label": "Balanced performance"
    },
    "Blaze X": {
        "color": "#ef4444",
        "max_speed": 9.6,
        "accel": 0.23,
        "brake": 0.25,
        "handling": 5.4,
        "label": "Fast top speed"
    },
    "Vortex R": {
        "color": "#3b82f6",
        "max_speed": 8.9,
        "accel": 0.20,
        "brake": 0.28,
        "handling": 6.2,
        "label": "Best handling"
    },
    "Titan ZX": {
        "color": "#f59e0b",
        "max_speed": 8.6,
        "accel": 0.18,
        "brake": 0.30,
        "handling": 6.0,
        "label": "Strong control"
    }
}

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
    min-height: 150px;
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
    '<div class="sub-title">Choose your car, select a level, avoid traffic, and complete all laps.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Top Controls
# -----------------------------
top1, top2, top3 = st.columns([2, 1, 1])

with top1:
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

with top2:
    difficulty = st.selectbox(
        "Select Level",
        ["Easy", "Medium", "Hard"],
        index=["Easy", "Medium", "Hard"].index(st.session_state.difficulty)
    )
    st.session_state.difficulty = difficulty

with top3:
    selected_car = st.selectbox(
        "Choose Car",
        list(car_options.keys()),
        index=list(car_options.keys()).index(st.session_state.selected_car)
    )
    st.session_state.selected_car = selected_car

selected_car_data = car_options[selected_car]

# -----------------------------
# Info Cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

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
    st.markdown(f"""
    <div class="info-box">
        <div class="info-title">🚦 Level</div>
        <div class="info-text">
            Selected level: <b>{difficulty}</b><br>
            Easy = fewer cars<br>
            Medium = balanced traffic<br>
            Hard = fast crowded traffic
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="info-box">
        <div class="info-title">🚘 Selected Car</div>
        <div class="info-text">
            <b>{selected_car}</b><br>
            Style: {selected_car_data["label"]}<br>
            Max Speed: {selected_car_data["max_speed"]}<br>
            Handling: {selected_car_data["handling"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    status_text = "Running" if st.session_state.game_started else "Stopped"
    st.markdown(f"""
    <div class="info-box">
        <div class="info-title">📡 Game Status</div>
        <div class="info-text">
            Current state: <b>{status_text}</b><br>
            Traffic hit = <b>Game Over</b><br>
            Finish all laps to win
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div class="control-note">Click inside the game canvas first, then use your keyboard arrows.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Game HTML
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
const DIFFICULTY = "{difficulty}";
const SELECTED_CAR = {selected_car_data};

const levelSettings = {{
    Easy: {{
        trafficCount: 6,
        trafficMinSpeed: 2.2,
        trafficMaxSpeed: 3.5,
        lapsToFinish: 2
    }},
    Medium: {{
        trafficCount: 9,
        trafficMinSpeed: 3.0,
        trafficMaxSpeed: 4.5,
        lapsToFinish: 3
    }},
    Hard: {{
        trafficCount: 13,
        trafficMinSpeed: 3.8,
        trafficMaxSpeed: 5.8,
        lapsToFinish: 4
    }}
}};

const settings = levelSettings[DIFFICULTY];

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

const lapsToFinish = settings.lapsToFinish;
const finishDistance = lapsToFinish * 2600;

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
    maxSpeed: SELECTED_CAR.max_speed,
    accel: SELECTED_CAR.accel,
    brake: SELECTED_CAR.brake,
    friction: 0.06,
    handling: SELECTED_CAR.handling,
    color: SELECTED_CAR.color,
    distance: 0,
    lap: 1
}};

const traffic = [];

function createTrafficCar() {{
    const lane = Math.floor(Math.random() * road.laneCount);
    return {{
        x: road.x + lane * road.laneWidth + road.laneWidth / 2 - 20,
        y: -120 - Math.random() * 1800,
        w: 40,
        h: 74,
        speed: settings.trafficMinSpeed + Math.random() * (settings.trafficMaxSpeed - settings.trafficMinSpeed),
        color: ["#a855f7", "#06b6d4", "#e11d48", "#84cc16", "#f97316", "#f43f5e"][Math.floor(Math.random() * 6)]
    }};
}}

for (let i = 0; i < settings.trafficCount; i++) {{
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

function drawBackground() {{
    ctx.fillStyle = "#14532d";
    ctx.fillRect(0, 0, road.x, H);
    ctx.fillRect(road.x + road.width, 0, W - (road.x + road.width), H);

    for (let i = 0; i < 10; i++) {{
        ctx.fillStyle = "#166534";
        ctx.beginPath();
        ctx.arc(60 + i * 14, 70 + i * 55, 12, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(W - 60 - i * 14, 95 + i * 52, 12, 0, Math.PI * 2);
        ctx.fill();
    }}
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
    ctx.fillRect(18, 18, 330, 190);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(18, 18, 330, 190);

    ctx.fillStyle = "white";
    ctx.font = "bold 23px Arial";
    ctx.fillText("PLAYER HUD", 32, 46);

    ctx.font = "18px Arial";
    ctx.fillText("Car: " + "{selected_car}", 32, 78);
    ctx.fillText("Speed: " + player.speed.toFixed(1), 32, 106);
    ctx.fillText("Lap: " + player.lap + " / " + lapsToFinish, 32, 134);
    ctx.fillText("Level: " + DIFFICULTY, 32, 162);
    ctx.fillText("Traffic Cars: " + settings.trafficCount, 32, 190);

    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(W - 280, 18, 250, 125);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(W - 280, 18, 250, 125);

    ctx.fillStyle = "white";
    ctx.font = "bold 21px Arial";
    ctx.fillText("RACE STATUS", W - 260, 46);

    ctx.font = "17px Arial";
    const progress = Math.min(100, (player.distance / finishDistance) * 100).toFixed(0);
    ctx.fillText("Progress: " + progress + "%", W - 260, 78);
    ctx.fillText("Goal: Complete all laps", W - 260, 106);
    ctx.fillText("Crash with traffic = Lose", W - 260, 134);

    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(18, H - 72, 440, 48);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.strokeRect(18, H - 72, 440, 48);

    ctx.fillStyle = "white";
    ctx.font = "17px Arial";
    ctx.fillText("Use arrow keys to survive traffic and finish the track.", 34, H - 41);
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

    if (keys.ArrowLeft) player.x -= player.handling;
    if (keys.ArrowRight) player.x += player.handling;

    if (player.x < road.x + 8) player.x = road.x + 8;
    if (player.x + player.w > road.x + road.width - 8) {{
        player.x = road.x + road.width - player.w - 8;
    }}

    player.distance += player.speed;
    player.lap = Math.min(lapsToFinish, Math.floor(player.distance / (finishDistance / lapsToFinish)) + 1);

    if (player.distance >= finishDistance) {{
        gameFinished = true;
        gameOver = true;
        stopped = true;
        playerWon = true;
    }}
}}

function updateTraffic() {{
    roadScroll += player.speed * 1.8;

    traffic.forEach((car) => {{
        car.y += car.speed + player.speed * 0.52;

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

    const boxW = 540;
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
    ctx.font = "bold 42px Arial";
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
    drawCar(player, "YOU");
    drawHUD();
    drawCenteredMessage("READY TO DRIVE", "Click Start Game to begin", "#1d4ed8", "#0f172a");
}}

function drawPausedScreen() {{
    drawRoad();
    drawTraffic();
    drawCar(player, "YOU");
    drawHUD();
    drawCenteredMessage("GAME STOPPED", "Click Start Game to play again", "#7c2d12", "#111827");
}}

function drawGameOverScreen() {{
    drawRoad();
    drawTraffic();
    drawCar(player, "YOU");
    drawHUD();
    drawCenteredMessage("GAME OVER", "Your car crashed into traffic", "#991b1b", "#111827");
}}

function drawWinScreen() {{
    drawRoad();
    drawTraffic();
    drawCar(player, "YOU");
    drawHUD();
    drawCenteredMessage("YOU WIN", "You completed all laps successfully", "#166534", "#0f172a");
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
        updateTraffic();
        checkCollisions();
    }}

    drawRoad();
    drawTraffic();
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
    <b>Note:</b> This version includes <b>car selection</b>, <b>3 difficulty levels</b>, 
    and only <b>your car + traffic cars</b>. Different cars have different handling and speed.
</div>
""", unsafe_allow_html=True)
