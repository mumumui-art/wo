import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="먹는 햄스터", page_icon="🐹")

# 초기 세션 상태 설정
if "tries" not in st.session_state:
    st.session_state.tries = 20
    st.session_state.score = 0
    st.session_state.food_index = 0
    st.session_state.fever = 0
    st.session_state.name = ""
    st.session_state.ranking = []

foods = [
    {"name": "🌻 해바라기씨", "prob": 1.0, "score": 1},
    {"name": "🌰 잣", "prob": 0.85, "score": 2},
    {"name": "🥜 호두", "prob": 0.7, "score": 3},
    {"name": "🍎 사과", "prob": 0.55, "score": 4},
    {"name": "🍑 복숭아", "prob": 0.4, "score": 5},
    {"name": "🍉 수박", "prob": 0.25, "score": 6},
]

# 타이틀 및 설명
st.title("🥜🐹 먹는 햄스터 게임")

with st.expander("📖 게임 설명 보기"):
    st.markdown("""
    ### 🎯 게임 목표:
    - 햄스터에게 다양한 먹이를 먹여 최대 점수를 노려보세요!

    ### 🍽️ 먹이 종류:
    - 🌻 해바라기씨  
    - 🌰 잣  
    - 🥜 호두  
    - 🍎 사과  
    - 🍑 복숭아  
    - 🍉 수박 (어려움 최고!)

    ### 📉 규칙:
    - 먹이가 클수록 먹기 어려워요! (확률 낮아짐)
    - 성공 시 점수는 더 올라가요!
    - 실패해도 먹을 수 있는 기회는 줄어들어요 (최대 20번)

    ### ⚡ 특별 이벤트:
    - 5% 확률로 챗바퀴 피버타임!  
    - 🎉 다음 두 번 먹을 때 확률이 4배 증가해요!

    ### 🏆 랭킹도 기록돼요!
    - 이름을 입력하면 결과가 기록돼요!

    **개발자: 조연우**
    """)

# 이름 입력
if not st.session_state.name:
    st.session_state.name = st.text_input("🎮 이름을 입력하세요", key="name_input")

# 현재 상태
st.subheader(f"🍽️ 남은 먹이 기회: {st.session_state.tries}")
st.subheader(f"🏅 현재 점수: {st.session_state.score}")
st.subheader(f"🍖 현재 먹이: {foods[st.session_state.food_index]['name']}")

# 먹이 주기 버튼
if st.button("🍽️ 먹이 주기"):
    if st.session_state.tries <= 0:
        st.warning("😵 햄스터가 배불러요! 게임이 끝났어요.")
    else:
        st.session_state.tries -= 1

        # 피버타임 여부
        fever_multiplier = 4 if st.session_state.fever > 0 else 1

        prob = foods[st.session_state.food_index]['prob'] * fever_multiplier
        rand = random.random()

        if rand <= prob:
            gained = foods[st.session_state.food_index]['score']
            st.session_state.score += gained
            st.success(f"🎉 성공! 햄스터가 {foods[st.session_state.food_index]['name']} 먹었어요! (+{gained}점)")

            # 다음 먹이로
            if st.session_state.food_index < len(foods) - 1:
                st.session_state.food_index += 1
        else:
            st.error(f"💔 실패! 햄스터가 {foods[st.session_state.food_index]['name']} 안 먹었어요...")

        # 피버타임 횟수 줄이기
        if st.session_state.fever > 0:
            st.session_state.fever -= 1

        # 피버타임 발동 여부
        if random.random() <= 0.05:
            st.session_state.fever = 2
            st.balloons()
            st.info("🔥 챗바퀴 피버타임 발동! 다음 두 번 확률 4배!")

# 게임 종료 및 결과 저장
if st.session_state.tries == 0:
    if st.session_state.name:
        st.success(f"🎉 게임 종료! {st.session_state.name}님의 최종 점수: {st.session_state.score}")
        st.session_state.ranking.append((st.session_state.name, st.session_state.score))

    # 랭킹 출력
    if st.session_state.ranking:
        st.subheader("🏆 랭킹")
        df = pd.DataFrame(st.session_state.ranking, columns=["이름", "점수"]).sort_values(by="점수", ascending=False)
        st.table(df)

    # 다시 시작 버튼
    if st.button("🔄 다시 시작"):
        st.session_state.tries = 20
        st.session_state.score = 0
        st.session_state.food_index = 0
        st.session_state.fever = 0
        st.session_state.name = ""

