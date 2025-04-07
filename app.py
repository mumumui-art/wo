import streamlit as st
import random

st.set_page_config(page_title="츄르먹기 게임", layout="centered")

# 초기 세션 상태 설정
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.laser = 3
    st.session_state.max_level = 1
    st.session_state.boost = False

probabilities = [
    1.0, 0.9, 0.86, 0.77, 0.68, 0.61, 0.60, 0.58, 0.57, 0.51,
    0.45, 0.35, 0.4, 0.32, 0.30, 0.3, 0.3, 0.3, 0.9, 0.2
]

st.title("🐱 고양이 츄르먹기 게임 🐱")

# 설명 토글
with st.expander("게임 설명 보기"):
    st.write("""
    - 츄르를 먹일수록 레벨이 올라갑니다.
    - 레벨이 올라갈수록 성공 확률이 낮아져요.
    - 레이저로 놀아주면 확률이 2배가 되지만, 3번만 사용 가능해요!
    """)

st.markdown(f"### 🍡 츄르 레벨: {st.session_state.level}")
st.markdown(f"🏆 최고 레벨: {st.session_state.max_level}")
st.markdown(f"📊 성공 확률: {probabilities[st.session_state.level - 1] * (2 if st.session_state.boost else 1) * 100:.1f}%")
st.markdown(f"🎮 남은 레이저: {st.session_state.laser}")

col1, col2 = st.columns(2)

with col1:
    if st.button("츄르 주기 🍡"):
        chance = probabilities[st.session_state.level - 1]
        if st.session_state.boost:
            chance *= 2
            st.session_state.boost = False

        if random.random() <= chance:
            st.session_state.level += 1
            st.session_state.max_level = max(st.session_state.max_level, st.session_state.level)
            st.success("츄르 성공! 🐱")
        else:
            st.error("츄르 실패! 게임 리셋 😿")
            st.session_state.level = 1
            st.session_state.laser = 3
            st.session_state.boost = False

with col2:
    if st.session_state.laser > 0:
        if st.button("레이저로 놀아주기 🔦"):
            st.session_state.laser -= 1
            if random.random() <= 0.5:
                st.session_state.boost = True
                st.info("고양이가 신났어요! 다음 츄르 확률 2배!")
            else:
                st.warning("고양이가 무관심해요...")

# 리셋 버튼
if st.button("🔄 게임 초기화"):
    st.session_state.level = 1
    st.session_state.laser = 3
    st.session_state.max_level = 1
    st.session_state.boost = False
    st.success("게임이 초기화되었습니다!")

