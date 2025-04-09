import streamlit as st
import random

st.set_page_config(page_title="돼지같은 햄스터", page_icon="🐹")

# 🟡 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.turns = 0
    st.session_state.fever_time = 0

# 🟡 피버타임 시각 효과
if st.session_state.fever_time > 0:
    st.markdown("""
    <div style='
        background: linear-gradient(90deg, #f9d423, #ff4e50, #ff6f91, #ffc107);
        padding: 1em;
        text-align: center;
        border-radius: 10px;
        color: white;
        font-size: 24px;
        font-weight: bold;
        animation: blink 1s infinite;
    '> 
    🎡 피버타임 발동! 확률 4배!! 🎉  
    </div>

    <style>
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# 🐹 게임 제목과 설명
st.title("🐹 먹는 햄스터")
with st.expander("📘 게임 설명 보기"):
    st.markdown("""
    ### 게임 목표:
    햄스터에게 먹이를 최대한 많이 먹이자! 🍎🌰🍉

    ### 규칙:
    - 20번의 먹이 기회 중 가능한 한 많은 점수를 얻으세요!
    - 크기가 클수록 먹을 확률은 낮지만, 점수는 높아요.
    - 5% 확률로 🎡피버타임이 발동돼서 2번 동안 확률이 4배가 돼요!
    - 실패해도 턴은 차감됩니다. 신중하게 선택하세요!  
    """)

st.subheader(f"🎯 점수: {st.session_state.score}점 / 🍽️ {st.session_state.turns}/20 회 먹음")

# 🍎 먹이 종류
foods = [
    {"name": "해바라기씨 🌻", "prob": 0.9, "score": 1},
    {"name": "잣 🌰", "prob": 0.8, "score": 2},
    {"name": "호두 🥜", "prob": 0.7, "score": 3},
    {"name": "사과 🍎", "prob": 0.5, "score": 5},
    {"name": "복숭아 🍑", "prob": 0.4, "score": 6},
    {"name": "수박 🍉", "prob": 0.3, "score": 8},
    {"name": "바나나 🍌", "prob": 0.6, "score": 4},
    {"name": "블루베리 🫐", "prob": 0.45, "score": 5},
    {"name": "체리 🍒", "prob": 0.35, "score": 6},
    {"name": "아보카도 🥑", "prob": 0.25, "score": 9}
]

# 🎲 랜덤으로 3개 음식 선택
options = random.sample(foods, 3)
st.markdown("**🍴 어떤 먹이를 줄까요?**")

# 🧡 피버타임 처리
multiplier = 4 if st.session_state.fever_time > 0 else 1

# 🍽️ 음식 선택 버튼들
cols = st.columns(3)
for i, food in enumerate(options):
    with cols[i]:
        if st.button(food["name"]):
            if st.session_state.turns >= 20:
                st.warning("게임이 종료되었습니다. 새로고침으로 다시 시작해보세요!")
            else:
                st.session_state.turns += 1

                if random.random() < food["prob"] * multiplier:
                    st.session_state.score += food["score"]
                    st.success(f"{food['name']} 먹기 성공! (+{food['score']}점)")
                else:
                    st.error(f"{food['name']} 먹기 실패 😥")

                # 피버타임 카운트 감소
                if st.session_state.fever_time > 0:
                    st.session_state.fever_time -= 1

                # 5% 확률로 피버타임 발동
                if st.session_state.fever_time == 0 and random.random() < 0.05:
                    st.session_state.fever_time = 2
                    st.balloons()
                    st.toast("🎡 피버타임 발동! 확률 4배!", icon="🎉")

# 🛑 게임 종료 메시지
if st.session_state.turns >= 20:
    st.markdown("---")
    st.header("🏁 게임 종료!")
    st.markdown(f"🥇 최종 점수: **{st.session_state.score}점**")
    st.markdown("🔁 페이지를 새로고침하면 다시 시작할 수 있어요!")

