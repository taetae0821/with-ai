# streamlit_app.py
import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Sea Level Rising TOFU Game", layout="wide")
st.title("🌊 Sea Level Rising - TOFU Game (Streamlit)")

# -------------------------------
# 게임 상태 초기화
# -------------------------------
if "player_x" not in st.session_state:
    st.session_state.player_x = 5
if "score" not in st.session_state:
    st.session_state.score = 0
if "blocks" not in st.session_state:
    st.session_state.blocks = []
if "sea_level" not in st.session_state:
    st.session_state.sea_level = 0
if "frame" not in st.session_state:
    st.session_state.frame = 0
if "speed" not in st.session_state:
    st.session_state.speed = 0.3  # 프레임 딜레이, 게임 속도
if "level" not in st.session_state:
    st.session_state.level = 1

WIDTH = 10
HEIGHT = 10

# -------------------------------
# 블록 업데이트
# -------------------------------
def update_blocks():
    st.session_state.frame += 1
    # 새 블록 생성 확률 증가
    BLOCK_PROB = min(0.1 + st.session_state.level*0.02, 0.5)
    if np.random.rand() < BLOCK_PROB:
        st.session_state.blocks.append({"x": np.random.randint(0, WIDTH), "y": 0})
    # 블록 이동
    for b in st.session_state.blocks:
        b["y"] += 1
    # 충돌 체크
    for b in st.session_state.blocks[:]:
        if b["y"] == HEIGHT-1 and b["x"] == st.session_state.player_x:
            st.session_state.score += 1
            st.session_state.blocks.remove(b)
        elif b["y"] >= HEIGHT:
            st.session_state.sea_level += 1
            st.session_state.blocks.remove(b)

# -------------------------------
# 플레이어 이동 버튼
# -------------------------------
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("◀"):
        st.session_state.player_x = max(0, st.session_state.player_x - 1)
with col3:
    if st.button("▶"):
        st.session_state.player_x = min(WIDTH-1, st.session_state.player_x + 1)

# -------------------------------
# 게임 루프
# -------------------------------
update_blocks()

# -------------------------------
# Plotly로 게임 화면 그리기
# -------------------------------
fig = go.Figure()

# 해수면
fig.add_trace(go.Bar(
    x=list(range(WIDTH)),
    y=[st.session_state.sea_level]*WIDTH,
    marker_color='blue',
    name='Sea Level',
    base=0,
    opacity=0.5
))

# 블록(TOFU)
for b in st.session_state.blocks:
    fig.add_trace(go.Bar(
        x=[b["x"]],
        y=[1],
        marker_color='lightblue',
        name='TOFU',
        base=b["y"]
    ))

# 플레이어
fig.add_trace(go.Bar(
    x=[st.session_state.player_x],
    y=[1],
    marker_color='green',
    name='Player',
    base=HEIGHT-1
))

fig.update_layout(
    barmode='stack',
    xaxis=dict(range=[-0.5, WIDTH-0.5], title="X 좌표"),
    yaxis=dict(range=[0, HEIGHT], title="Y 좌표"),
    showlegend=False,
    height=500,
    width=500,
)
st.plotly_chart(fig)

st.write(f"점수: {st.session_state.score} | 난이도 레벨: {st.session_state.level}")

# -------------------------------
# 레벨 증가: 점수 기준
# -------------------------------
if st.session_state.score >= st.session_state.level * 5:
    st.session_state.level += 1
    st.session_state.speed = max(0.05, st.session_state.speed - 0.02)  # 점점 빨라짐

# -------------------------------
# 게임 종료 체크
# -------------------------------
if st.session_state.sea_level >= HEIGHT-1:
    st.error("💀 Game Over! 해수면에 잠겼습니다.")
    st.session_state.player_x = 5
    st.session_state.score = 0
    st.session_state.blocks = []
    st.session_state.sea_level = 0
    st.session_state.frame = 0
    st.session_state.level = 1
    st.session_state.speed = 0.3

# -------------------------------
# 자동 새로고침
# -------------------------------
time.sleep(st.session_state.speed)
st.experimental_rerun()
