import streamlit as st
import random

st.set_page_config(page_title="먹는 햄스터", page_icon="🐹")
st.title("🐹 먹는 햄스터")

# 햄스터 메인 이미지
st.image("https://i.imgur.com/n6bR1sD.png", width=200)

# 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.count = 0
    st.session_state.max_count = 20
    st.session_state.fever = False
    st.session_state.fever_turn = 0
    st.session_state.name = ""

# 먹이 리스트
foods = [
    {"name": "해바라기씨", "prob": 0.95, "point": 1, "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Sunflower_seeds.jpg"},
    {"name": "잣", "prob": 0.85, "point": 2, "img": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Pine_nuts_closeup.jpg"},
    {"name": "호두", "prob": 0.7, "point": 3, "img": "https://upload.wikimedia.org/wikipedia/commons/8/85/Walnuts.jpg"},
    {"name": "사과", "prob": 0.5, "point": 5, "img": "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg"},
    {"name": "복숭아", "prob": 0.35, "point": 7, "img": "https://upload.wikimedia.org/wikipedia/commons/4/45/Peach_and_cross_section.jpg"},
    {"name": "수박", "prob": 0.2, "point": 10, "img": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Watermelon_cross_BNC.jpg"}
]

# 이름 입력
if st.session_state.name == "":
    st.session_state.name = st.text_input("🐹 햄스터 이름을 입력하세요:", "")
    st.stop()

# 남은 기회 표시
st.markdown(f"**🍽️ 남은 먹이 기회: {st.session_state.max_count - st.session_state.count} / {st.session_state.max_count}**")
st.markdown(f"**⭐ 현재 점수: {st.session_state.score}점**")

# 피버타임 설명
if st.session_state.fever_turn > 0:
    st.success("🔥 피버타임 발동! 확률 4배 적용중!")
    st.image("https://i.imgur.com/EphdQXq.jpg", width=150)

# 먹이 선택
food_names = [f["name"] for f in foods]
selected = st.selectbox("🍎 어떤 먹이를 줄까요?", food_names)

if st.button("햄스터에게 먹이 주기"):
    if st.session_state.count >= st.session_state.max_count:
        st.warning("모든 먹이를 다 줬어요! 게임이 끝났습니다.")
    else:
        st.session_state.count += 1
        food = next(f for f in foods if f["name"] == selected)
        prob = food["prob"]
        
        # 피버타임 보정
        if st.session_state.fever_turn > 0:
            prob *= 4
            st.session_state.fever_turn -= 1
        elif random.random() < 0.05:
            st.session_state.fever_turn = 2
            st.balloons()
            st.success("🎡 챗바퀴 피버타임 시작!")

        success = random.random() <= prob
        st.image(food["img"], width=150)

        if success:
            st.session_state.score += food["point"]
            st.success(f"냠냠! {selected} 먹었어요! (+{food['point']}점)")
        else:
            st.error(f"앗! {selected} 실패했어요 ㅠㅠ")

# 게임 종료 후 결과
if st.session_state.count >= st.session_state.max_count:
    st.markdown("---")
    st.subheader("📋 결과 요약")
    st.markdown(f"""
    - 이름: **{st.session_state.name}**
    - 총 점수: **{st.session_state.score}점**
    """)
    st.image("https://i.imgur.com/xQT5K5y.jpg", caption="수고했어요!", width=200)

    # 랭킹 기록 파일 저장
    with open("ranking.txt", "a") as f:
        f.write(f"{st.session_state.name}: {st.session_state.score}\n")

    st.button("🔁 다시 시작", on_click=lambda: st.session_state.clear())
