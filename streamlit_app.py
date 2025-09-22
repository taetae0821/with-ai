import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(page_title="Sea Level Rising Game", layout="wide")

# -------------------------------
# 초기 상태
# -------------------------------
if "player_x" not in st.session_state:
    st.session_state.player_x = 50
if "player_y" not in st.session_state:
    st.session_state.player_y = 10
if "blocks" not in st.session_state:
    st.session_state.blocks = [{"x": 40, "y": 10}]
if "sea_level" not in st.session_state:
    st.session_state.sea_level = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1

WIDTH = 100
HEIGHT = 100
BLOCK_WIDTH = 20
BLOCK_HEIGHT = 5

st.title("🌊 Sea Level Rising Game")
placeholder = st.empty()

# -------------------------------
# 게임 상태 업데이트 함수
# -------------------------------
def update_state(move=None):
    # 좌/우 이동
    if move == "left":
        st.session_state.player_x = max(0, st.session_state.player_x - 5)
    if move == "right":
        st.session_state.player_x = min(WIDTH, st.session_state.player_x + 5)

    # 블록 생성
    if st.session_state.blocks[-1]["y"] < HEIGHT - 20:
        new_x = np.random.randint(0, WIDTH-BLOCK_WIDTH)
        st.session_state.blocks.append({"x": new_x, "y": 0})

    # 블록 상승
    for block in st.session_state.blocks:
        block["y"] += 1 + 0.1*st.session_state.level

    # 점수 체크
    on_block = False
    for block in st.session_state.blocks:
        if abs(block["x"] - st.session_state.player_x) < 10 and abs(block["y"] - st.session_state.player_y) < 5:
            st.session_state.score += 1
            st.session_state.player_y = block["y"] + BLOCK_HEIGHT
            on_block = True
            break
    if not on_block:
        st.session_state.player_y -= 0.5  # 중력처럼 조금씩 내려가기

    # 해수면 상승
    st.session_state.sea_level += 0.2 + 0.05*st.session_state.level

    # 게임 종료 체크
    if st.session_state.player_y < st.session_state.sea_level:
        st.warning("💧 Game Over! 바닷물에 잠겼습니다.")
        # 상태 초기화
        st.session_state.player_x = 50
        st.session_state.player_y = 10
        st.session_state.blocks = [{"x": 40, "y": 10}]
        st.session_state.sea_level = 0
        st.session_state.score = 0
        st.session_state.level = 1

    # 레벨 증가
    if st.session_state.score >= st.session_state.level * 10:
        st.session_state.level += 1

# -------------------------------
# 화면 그리기
# -------------------------------
def draw():
    df_blocks = pd.DataFrame(st.session_state.blocks)
    fig = px.scatter(df_blocks, x="x", y="y", size_max=20, title="해수면 피하기",
                     range_x=[0, WIDTH], range_y=[0, HEIGHT])
    # 캐릭터
    fig.add_scatter(x=[st.session_state.player_x], y=[st.session_state.player_y],
                    mode="markers", marker=dict(size=15, color="green"), name="캐릭터")
    # 해수면
    fig.add_scatter(x=[0, WIDTH], y=[st.session_state.sea_level, st.session_state.sea_level],
                    mode="lines", line=dict(color="blue", width=5), name="해수면")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    placeholder.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 조작 버튼
# -------------------------------
col1, col2 = st.columns([2,1])
with col2:
    st.subheader("조작")
    if st.button("⬅️ 좌"):
        update_state("left")
    elif st.button("➡️ 우"):
        update_state("right")
    else:
        update_state()  # 버튼 클릭 없으면 블록/해수면만 상승

    st.write(f"점수: {st.session_state.score}  레벨: {st.session_state.level}")

draw()
