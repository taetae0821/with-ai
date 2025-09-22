# streamlit_app.py
import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Sea Level Rising TOFU Game", layout="wide")
st.title("🌊 Sea Level Rising - TOFU Game")

# -------------------------------
# 게임 상태 초기화
# -------------------------------
if "player_x" not in st.session_state:
    st.session_state.player_x = 5
if "player_y" not in st.session_state:
    st.session_state.player_y = 5  # 해수면보다 충분히 높게 시작
if "score" not in st.session_state:
    st.session_state.score = 0
if "blocks" not in st.session_state:
    # 시작 발판 확보
    st.session_state.blocks = [{"x": 5, "y": 0}]
if "sea_level" not in st.session_state:
    st.session_state.sea_level = 0
if "speed" not in st.session_state:
    st.session_state.speed = 0.3
if "level" not in st.session_state:
    st.session_state.level = 1
if "running" not in st.session_state:
    st.session_state.running = False
if "frame" not in st.session_state:
    st.session_state.frame = 0
if "y_velocity" not in st.session_state:
    st.session_state.y_velocity = 0

WIDTH = 10
HEIGHT = 15
GRAVITY = -0.5
JUMP_POWER = 2

# -------------------------------
# 게임 루프용 placeholder
# -------------------------------
placeholder = st.empty()

# -------------------------------
# 좌우 이동 버튼
# -------------------------------
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("◀"):
        st.session_state.player_x = max(0, st.session_state.player_x - 1)
with col3:
    if st.button("▶"):
        st.session_state.player_x = min(WIDTH-1, st.session_state.player_x + 1)
with col2:
    if st.button("점프"):
        # 블록 위에 있으면 점프 가능
        for b in st.session_state.blocks:
            if b["x"] == st.session_state.player_x and st.session_state.player_y == b["y"]:
                st.session_state.y_velocity = JUMP_POWER

# -------------------------------
# 게임 루프
# -------------------------------
def game_loop():
    while True:
        st.session_state.frame += 1

        # -------------------------------
        # 블록 생성
        # -------------------------------
        BLOCK_PROB = min(0.1 + st.session_state.level*0.02, 0.5)
        if np.random.rand() < BLOCK_PROB:
            st.session_state.blocks.append({"x": np.random.randint(0, WIDTH), "y": HEIGHT-1})

        # -------------------------------
        # 블록 이동(아래로)
        # -------------------------------
        for b in st.session_state.blocks:
            b["y"] -= 1
        st.session_state.blocks = [b for b in st.session_state.blocks if b["y"] >= 0]

        # -------------------------------
        # 캐릭터 점프/중력
        # -------------------------------
        st.session_state.player_y += st.session_state.y_velocity
        st.session_state.y_velocity += GRAVITY

        # 바닥 충돌
        if st.session_state.player_y < 0:
            st.session_state.player_y = 0
            st.session_state.y_velocity = 0

        # 블록 위 충돌
        for b in st.session_state.blocks:
            if b["x"] == st.session_state.player_x and st.session_state.player_y <= b["y"] < st.session_state.player_y + 1 and st.session_state.y_velocity < 0:
                st.session_state.player_y = b["y"]
                st.session_state.y_velocity = 0
                st.session_state.score += 1  # 블록 밟으면 점수

        # -------------------------------
        # 해수면 상승
        # -------------------------------
        st.session_state.sea_level += 0.005  # 시작하자마자 끝나지 않도록 조정
        if st.session_state.player_y < st.session_state.sea_level:
            placeholder.empty()
            st.error("💀 Game Over! 해수면에 잠겼습니다.")
            # 초기화
            st.session_state.player_x = 5
            st.session_state.player_y = 5
            st.session_state.score = 0
            st.session_state.blocks = [{"x": 5, "y": 0}]
            st.session_state.sea_level = 0
            st.session_state.level = 1
            st.session_state.speed = 0.3
            st.session_state.y_velocity = 0
            break

        # -------------------------------
        # 레벨 증가
        # -------------------------------
        if st.session_state.score >= st.session_state.level * 10:
            st.session_state.level += 1
            st.session_state.speed = max(0.05, st.session_state.speed - 0.02)

        # -------------------------------
        # Plotly 화면 그리기
        # -------------------------------
        fig = go.Figure()

        # 해수면
        fig.add_trace(go.Bar(
            x=list(range(WIDTH)),
            y=[st.session_state.sea_level]*WIDTH,
            marker_color='blue',
            opacity=0.5
        ))

        # 블록
        for b in st.session_state.blocks:
            fig.add_trace(go.Bar(
                x=[b["x"]],
                y=[1],
                marker_color='lightblue',
                base=b["y"]
            ))

        # 플레이어
        fig.add_trace(go.Bar(
            x=[st.session_state.player_x],
            y=[1],
            marker_color='green',
            base=st.session_state.player_y
        ))

        fig.update_layout(
            barmode='stack',
            xaxis=dict(range=[-0.5, WIDTH-0.5]),
            yaxis=dict(range=[0, HEIGHT]),
            showlegend=False,
            height=600,
            width=500,
        )

        placeholder.plotly_chart(fig, key=f"game_frame_{st.session_state.frame}")
        st.write(f"점수: {st.session_state.score} | 레벨: {st.session_state.level} | 해수면: {st.session_state.sea_level:.2f}")

        time.sleep(st.session_state.speed)

# -------------------------------
# 게임 시작 버튼
# -------------------------------
if st.button("게임 시작") or st.session_state.running:
    st.session_state.running = True
    game_loop()
