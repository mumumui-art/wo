import streamlit as st
import random

# 초기 세션 상태 설정
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.max_level = 1
    st.session_state.laser_count = 3
    st.session_state.laser_boost = False

probabilities = [
    1.0, 0.9, 0.86, 0.77, 0.68, 0.61, 0.60, 0.58, 0.57, 0.51,
    0.45, 0.35, 0.4, 0.32, 0.30, 0.3, 0.3, 0.3, 0.9, 0.2
]

st.title("🐱 고양이에게 츄르 먹이기 게임")

with st.expander("🎮 게임 설명 보기"):
    st.markdown("""
    ### 게임 목표:
    - 귀여운 고양이에게 츄르를 최대한 많이 먹이는 것이 목표예요!

    ### 게임 규칙:
    - **츄르 주기**: 확률에 따라 츄르를 먹어요. 성공하면 레벨이 올라가요.
    - **레이저로 놀아주기**: 확률을 올릴 수 있어요. 총 3번 사용 가능!
    - **게임 종료**: 츄르 못 먹으면 다시 시작이에요.

    ### 게임 팁:
    - 레벨이 올라갈수록 확률이 낮아져요.
    - 레이저는 전략적으로 써요!

    **제작자 : 조연우**
    """)

st.subheader(f"츄르 {st.session_state.level}개 냠")
st.caption(f"✨ 최대 츄르 개수: {st.session_state.max_level}")

# 츄르 먹을 확률 표시
if st.session_state.level <= len(probabilities):
    prob = probabilities[st.session_state.level - 1]
    st.write(f"츄르 먹을 확률: **{prob * 100:.2f}%**")
else:
    st.success("🎉 츄르 다 먹었어요! 🎉")

col1, col2 = st.columns(2)

with col1:
    if st.button("츄르 주기"):
        rand = random.random()
        boost = 2 if st.session_state.laser_boost else 1

        if st.session_state.level <= len(probabilities) and rand <= probabilities[st.session_state.level - 1] * boost:
            st.session_state.level += 1
            st.session_state.max_level = max(st.session_state.max_level, st.session_state.level)
            st.success("츄르 냠냠 성공!")
        else:
            st.error("츄르 실패! 게임 다시 시작합니다.")
            st.session_state.level = 1
            st.session_state.max_level = 1
            st.session_state.laser_count = 3
        st.session_state.laser_boost = False

with col2:
    if st.session_state.laser_count > 0:
        if st.button(f"레이저로 놀아주기 ({st.session_state.laser_count})"):
            st.session_state.laser_count -= 1
            if random.random() <= 0.5:
                st.session_state.laser_boost = True
                st.info("🎯 고양이 배고파요! 확률 2배!")
            else:
                st.warning("😽 고양이 배불러서 반응 없어요...")
    else:
        st.button("레이저 더 이상 없음", disabled=True)
