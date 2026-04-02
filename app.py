import streamlit as st
import random
import time

st.set_page_config(
    page_title="Velocity Race Arena",
    page_icon="🏎️",
    layout="wide"
)

# -----------------------------
# Custom Professional Styling
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.2rem;
}

.sub-title {
    text-align: center;
    font-size: 1.1rem;
    color: #bdbdbd;
    margin-bottom: 2rem;
}

.glass-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    margin-bottom: 15px;
}

.stat-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.03));
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.car-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
}

.small-text {
    color: #cfcfcf;
    font-size: 0.95rem;
}

.event-log {
    background: #111827;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #2d3748;
    height: 320px;
    overflow-y: auto;
    font-size: 0.95rem;
}

.winner-box {
    background: linear-gradient(135deg, #16a34a, #15803d);
    padding: 24px;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-size: 1.3rem;
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(22,163,74,0.35);
}

.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Game Data
# -----------------------------
cars = {
    "Thunder GT": {
        "emoji": "🏎️",
        "speed": 88,
        "handling": 80,
        "durability": 76,
        "nitro": 2
    },
    "Blaze X": {
        "emoji": "🚗",
        "speed": 82,
        "handling": 90,
        "durability": 78,
        "nitro": 3
    },
    "Vortex R": {
        "emoji": "🏁",
        "speed": 91,
        "handling": 72,
        "durability": 74,
        "nitro": 2
    },
    "Titan Muscle": {
        "emoji": "🚘",
        "speed": 79,
        "handling": 68,
        "durability": 92,
        "nitro": 1
    }
}

difficulty_settings = {
    "Easy": {"ai_min": 68, "ai_max": 82, "event_risk": 0.18},
    "Medium": {"ai_min": 74, "ai_max": 90, "event_risk": 0.28},
    "Hard": {"ai_min": 82, "ai_max": 96, "event_risk": 0.38}
}

# -----------------------------
# Session State
# -----------------------------
if "race_started" not in st.session_state:
    st.session_state.race_started = False

if "race_finished" not in st.session_state:
    st.session_state.race_finished = False

if "results" not in st.session_state:
    st.session_state.results = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "player_summary" not in st.session_state:
    st.session_state.player_summary = {}

if "player_name" not in st.session_state:
    st.session_state.player_name = "Player"

# -----------------------------
# Helper Functions
# -----------------------------
def calculate_lap_time(car_stats, difficulty, use_nitro, pit_stop=False):
    base_time = random.uniform(24.5, 33.5)

    speed_bonus = (car_stats["speed"] - 75) * 0.08
    handling_bonus = (car_stats["handling"] - 75) * 0.05
    durability_penalty = max(0, (80 - car_stats["durability"])) * 0.03

    ai_pressure = random.uniform(
        difficulty_settings[difficulty]["ai_min"],
        difficulty_settings[difficulty]["ai_max"]
    ) * 0.01

    lap_time = base_time - speed_bonus - handling_bonus + durability_penalty - ai_pressure

    if use_nitro:
        lap_time -= random.uniform(1.0, 2.0)

    if pit_stop:
        lap_time += random.uniform(3.0, 5.5)

    lap_time += random.uniform(-0.6, 0.8)

    return round(max(lap_time, 19.5), 2)


def random_event(car_stats, difficulty):
    risk = difficulty_settings[difficulty]["event_risk"]

    if random.random() > risk:
        return None, 0

    events = [
        ("Tight corner slowed you down.", round(random.uniform(0.8, 1.8), 2)),
        ("Minor tire slip on the track.", round(random.uniform(0.7, 1.7), 2)),
        ("Brilliant racing line! Time gained.", round(random.uniform(-1.5, -0.5), 2)),
        ("Late braking move worked perfectly.", round(random.uniform(-1.2, -0.4), 2)),
        ("Engine heat warning reduced pace.", round(random.uniform(0.9, 2.0), 2)),
        ("Great traction out of the turn.", round(random.uniform(-1.0, -0.3), 2)),
    ]
    return random.choice(events)


def generate_ai_opponents(difficulty):
    names = [
        "Falcon AI", "Neo Drift", "Shadow Racer",
        "Apex Hunter", "Crimson Jet", "Storm Byte"
    ]
    selected = random.sample(names, 3)
    opponents = []

    for name in selected:
        opponents.append({
            "name": name,
            "total_time": 0,
            "best_lap": None
        })

    return opponents


def reset_game():
    st.session_state.race_started = False
    st.session_state.race_finished = False
    st.session_state.results = []
    st.session_state.logs = []
    st.session_state.player_summary = {}


# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🏎️ Velocity Race Arena</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Build with Python + Streamlit • Professional racing simulator with laps, nitro, pit stops, and leaderboard</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Controls
# -----------------------------
with st.sidebar:
    st.header("⚙️ Race Setup")

    player_name = st.text_input("Driver Name", value="Player")
    st.session_state.player_name = player_name

    selected_car = st.selectbox("Choose Your Car", list(cars.keys()))
    difficulty = st.selectbox("Difficulty", list(difficulty_settings.keys()), index=1)
    total_laps = st.slider("Number of Laps", min_value=3, max_value=10, value=5)
    weather = st.selectbox("Weather Mode", ["Clear", "Cloudy", "Rainy"])

    st.markdown("---")
    st.subheader("Car Stats")
    car = cars[selected_car]

    st.markdown(f"""
    <div class="glass-card">
        <div class="car-name">{car['emoji']} {selected_car}</div>
        <div class="small-text">Speed: {car['speed']}</div>
        <div class="small-text">Handling: {car['handling']}</div>
        <div class="small-text">Durability: {car['durability']}</div>
        <div class="small-text">Nitro Charges: {car['nitro']}</div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        start_btn = st.button("Start Race", use_container_width=True)

    with col_b:
        reset_btn = st.button("Reset", use_container_width=True)

    if reset_btn:
        reset_game()
        st.rerun()

# -----------------------------
# Main Layout
# -----------------------------
left, right = st.columns([1.3, 1])

with left:
    st.markdown('<div class="section-title">Race Dashboard</div>', unsafe_allow_html=True)

    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.markdown(f'<div class="stat-box"><div class="small-text">Driver</div><div class="car-name">{player_name}</div></div>', unsafe_allow_html=True)
    with stats_col2:
        st.markdown(f'<div class="stat-box"><div class="small-text">Car</div><div class="car-name">{selected_car}</div></div>', unsafe_allow_html=True)
    with stats_col3:
        st.markdown(f'<div class="stat-box"><div class="small-text">Difficulty</div><div class="car-name">{difficulty}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.race_started and not st.session_state.race_finished:
        st.info("Set up your race from the sidebar and click **Start Race**.")

with right:
    st.markdown('<div class="section-title">Track Conditions</div>', unsafe_allow_html=True)

    weather_effect = 0
    if weather == "Rainy":
        weather_effect = 1.4
    elif weather == "Cloudy":
        weather_effect = 0.4

    st.markdown(f"""
    <div class="glass-card">
        <div class="small-text">Weather</div>
        <div class="car-name">{weather}</div>
        <br>
        <div class="small-text">Laps</div>
        <div class="car-name">{total_laps}</div>
        <br>
        <div class="small-text">Track Effect</div>
        <div class="car-name">+{weather_effect:.1f}s pressure</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Race Logic
# -----------------------------
if start_btn:
    st.session_state.race_started = True
    st.session_state.race_finished = False
    st.session_state.logs = []
    st.session_state.results = []
    st.session_state.player_summary = {}

    opponents = generate_ai_opponents(difficulty)
    player_car = cars[selected_car].copy()

    progress_area = st.container()
    live_log_area = st.container()

    player_total = 0
    best_lap = None
    remaining_nitro = player_car["nitro"]
    car_condition = 100

    with progress_area:
        st.markdown('<div class="section-title">Live Race Progress</div>', unsafe_allow_html=True)
        race_progress = st.progress(0, text="Preparing the track...")

    with live_log_area:
        log_placeholder = st.empty()

    for lap in range(1, total_laps + 1):
        use_nitro = False
        pit_stop = False

        if remaining_nitro > 0 and lap in [2, total_laps]:
            use_nitro = True
            remaining_nitro -= 1

        if car_condition < 55 and lap != total_laps:
            pit_stop = True
            car_condition += random.randint(18, 28)
            car_condition = min(car_condition, 100)

        lap_time = calculate_lap_time(player_car, difficulty, use_nitro, pit_stop)
        event, delta = random_event(player_car, difficulty)

        lap_time += weather_effect
        lap_time += delta
        lap_time = round(max(19.5, lap_time), 2)

        damage = random.randint(4, 10)
        if weather == "Rainy":
            damage += 2
        car_condition -= damage
        car_condition = max(car_condition, 35)

        player_total += lap_time
        if best_lap is None or lap_time < best_lap:
            best_lap = lap_time

        log_line = f"Lap {lap}: {lap_time}s"
        if use_nitro:
            log_line += " | Nitro used"
        if pit_stop:
            log_line += " | Pit stop"
        if event:
            if delta < 0:
                log_line += f" | {event} ({delta}s)"
            else:
                log_line += f" | {event} (+{delta}s)"
        log_line += f" | Car condition: {car_condition}%"

        st.session_state.logs.append(log_line)

        # AI opponents
        for ai in opponents:
            ai_lap = random.uniform(24.0, 33.0)
            ai_lap -= random.uniform(0.2, 1.8)
            ai_lap += weather_effect
            ai_lap += random.uniform(-0.8, 1.3)
            ai_lap = round(ai_lap, 2)

            ai["total_time"] += ai_lap
            if ai["best_lap"] is None or ai_lap < ai["best_lap"]:
                ai["best_lap"] = ai_lap

        progress_percent = lap / total_laps
        race_progress.progress(progress_percent, text=f"Lap {lap}/{total_laps} completed")

        log_html = "<div class='event-log'>" + "<br>".join(st.session_state.logs[::-1]) + "</div>"
        log_placeholder.markdown(log_html, unsafe_allow_html=True)

        time.sleep(0.6)

    # Final results
    final_results = [{
        "name": player_name,
        "car": selected_car,
        "total_time": round(player_total, 2),
        "best_lap": best_lap,
        "condition": car_condition
    }]

    for ai in opponents:
        final_results.append({
            "name": ai["name"],
            "car": "AI Prototype",
            "total_time": round(ai["total_time"], 2),
            "best_lap": ai["best_lap"],
            "condition": random.randint(60, 95)
        })

    final_results = sorted(final_results, key=lambda x: x["total_time"])

    st.session_state.results = final_results
    st.session_state.player_summary = {
        "total_time": round(player_total, 2),
        "best_lap": best_lap,
        "remaining_nitro": remaining_nitro,
        "condition": car_condition
    }
    st.session_state.race_finished = True
    st.session_state.race_started = False

# -----------------------------
# Final Results
# -----------------------------
if st.session_state.race_finished:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏁 Final Leaderboard</div>', unsafe_allow_html=True)

    leaderboard = st.session_state.results
    winner = leaderboard[0]

    if winner["name"] == st.session_state.player_name:
        st.markdown(
            f'<div class="winner-box">🏆 Congratulations {winner["name"]}! You won the race in {winner["total_time"]} seconds.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="winner-box">🔥 {winner["name"]} wins the race with a total time of {winner["total_time"]} seconds.</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    table_data = []
    for idx, racer in enumerate(leaderboard, start=1):
        table_data.append({
            "Position": idx,
            "Driver": racer["name"],
            "Car": racer["car"],
            "Total Time (s)": racer["total_time"],
            "Best Lap (s)": racer["best_lap"],
            "Car Condition (%)": racer["condition"]
        })

    st.dataframe(table_data, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your Race Summary</div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Total Time", f"{st.session_state.player_summary['total_time']} s")
    with s2:
        st.metric("Best Lap", f"{st.session_state.player_summary['best_lap']} s")
    with s3:
        st.metric("Nitro Left", st.session_state.player_summary["remaining_nitro"])
    with s4:
        st.metric("Final Condition", f"{st.session_state.player_summary['condition']}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Race Log</div>', unsafe_allow_html=True)

    race_log_html = "<div class='event-log'>" + "<br>".join(st.session_state.logs[::-1]) + "</div>"
    st.markdown(race_log_html, unsafe_allow_html=True)
