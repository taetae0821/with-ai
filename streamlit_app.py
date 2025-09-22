# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import time

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

WIDTH = 10
HEIGHT = 10
BLOCK_PROB = 0.3  # 매 프레임 블록 생성 확률

# -------------------------------
# 블록 업데이트
# -------------------------------
def update_blocks():
    st.session_state.frame += 1
    # 새 블록 생성
    if np.random.rand() < BLOCK_PROB:
        st.session_state.blocks.append({"x": np.random.randint(0, WIDTH), "y": 0})
    # 블록 이동
    for b in st.session_state.blocks:
        b["y"] += 1
    # 충돌 체크
    for b in st.session_state.blocks[:]:
        if b["y"] == HEIGHT - 1 and b["x"] == st.session_state.player_x:
            st.session_state.score += 1
            st.session_state.blocks.remove(b)
        elif b["y"] >= HEIGHT:
            st.session_state.sea_level += 1
            st.session_state.blocks.remove(b)

# -------------------------------
# 키 입력 (버튼)
# -------------------------------
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("◀"):
        st.session_state.player_x = max(0, st.session_state.player_x - 1)
with col3:
    if st.button("▶"):
        st.session_state.player_x = min(WIDTH-1, st.session_state.player_x + 1)

# -------------------------------
# 게임 루프 시뮬레이션
# -------------------------------
update_blocks()

# -------------------------------
# 게임 화면 그리기
# -------------------------------
grid = np.full((HEIGHT, WIDTH), "⬜")
# 해수면 표시
for y in range(HEIGHT-1, HEIGHT-1-st.session_state.sea_level, -1):
    if y >= 0:
        grid[y,:] = "🌊"
# 블록 표시
for b in st.session_state.blocks:
    if 0 <= b["y"] < HEIGHT:
        grid[b["y"], b["x"]] = "🟦"
# 플레이어 표시
grid[HEIGHT-1, st.session_state.player_x] = "🟩"

# 화면 출력
st.text("\n".join("".join(row) for row in grid))
st.write(f"점수: {st.session_state.score}")

# 게임 종료 체크
if st.session_state.sea_level >= HEIGHT-1:
    st.error("💀 Game Over! 해수면에 잠겼습니다.")
    # 세션 초기화
    st.session_state.player_x = 5
    st.session_state.score = 0
    st.session_state.blocks = []
    st.session_state.sea_level = 0
    st.session_state.frame = 0

# 자동 새로고침
st.experimental_rerun()
