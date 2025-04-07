from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>츄르먹기 게임</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #fdf6e3;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            h1 {
                font-size: 28px;
            }
            button {
                margin: 10px;
                padding: 10px 20px;
                font-size: 18px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            #feedButton {
                background-color: #ff9800;
                color: white;
            }
            #laserButton {
                background-color: #4caf50;
                color: white;
            }
            #showGameInfoButton {
                position: fixed;
                top: 15px;
                left: 15px;
                background-color: #2196f3;
                color: white;
                font-size: 14px;
                padding: 6px 10px;
            }
            #gameInfo {
                display: none;
                background-color: #fff;
                border: 1px solid #ccc;
                padding: 20px;
                margin-top: 20px;
                border-radius: 10px;
                max-width: 500px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .probability, #level, #maxLevel {
                font-size: 20px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <button id="showGameInfoButton" onclick="toggleGameInfo()">게임 설명 보기</button>

        <h1>🐱 고양이에게 츄르 먹이기 🐱</h1>
        <p id="level">츄르 주세요</p>
        <p id="maxLevel"></p>

        <button id="feedButton" onclick="feedCat()">츄르 주기</button>
        <button id="laserButton" onclick="playWithLaser()">레이저로 놀아주기 (3)</button>

        <div class="probability" id="probability"></div>

        <div id="gameInfo">
            <h3>게임 설명</h3>
            <p>고양이에게 츄르를 주면서 최대 몇 개를 먹일 수 있는지 도전하세요!</p>
            <ul>
                <li>성공 시 츄르 레벨이 올라가고, 실패 시 게임이 초기화됩니다.</li>
                <li>레이저는 확률을 2배로 높여주지만, 3번만 사용할 수 있어요.</li>
            </ul>
        </div>

        <script>
            let level = 1;
            let maxLevel = 20;
            let laserCount = 3;
            let maxCatLevel = 1;
            let laserBoostActive = false;

            const probabilities = [
                1.0, 0.9, 0.86, 0.77, 0.68, 0.61, 0.60, 0.58, 0.57, 0.51,
                0.45, 0.35, 0.4, 0.32, 0.30, 0.3, 0.3, 0.3, 0.9, 0.2
            ];

            function feedCat() {
                if (level <= maxLevel) {
                    let rand = Math.random();
                    let chance = laserBoostActive ? probabilities[level - 1] * 2 : probabilities[level - 1];
                    if (rand <= chance) {
                        level++;
                        maxCatLevel = Math.max(maxCatLevel, level);
                        updateLevelDisplay();
                        laserBoostActive = false;
                    } else {
                        resetGame();
                    }
                } else {
                    document.getElementById("level").innerText = "🎉 츄르 다 먹었어요! 🎉";
                }
                updateLaserButton();
                updateProbability();
            }

            function playWithLaser() {
                if (laserCount > 0) {
                    laserCount--;
                    if (Math.random() <= 0.5) {
                        laserBoostActive = true;
                        alert("레이저 효과 발동! 고양이가 더 배고파졌어요!");
                    } else {
                        alert("고양이가 관심 없어해요 😿");
                    }
                    updateLaserButton();
                } else {
                    alert("레이저는 더 이상 사용할 수 없어요.");
                }
            }

            function updateLaserButton() {
                const laserBtn = document.getElementById("laserButton");
                laserBtn.innerText = `레이저로 놀아주기 (${laserCount})`;
                if (laserCount === 0) {
                    laserBtn.disabled = true;
                    laserBtn.style.backgroundColor = '#ccc';
                }
            }

            function updateLevelDisplay() {
                document.getElementById("level").innerText = `츄르 ${level}개 냠`;
                document.getElementById("maxLevel").innerText = `최고 기록: ${maxCatLevel}개`;
            }

            function updateProbability() {
                const prob = probabilities[level - 1] * 100;
                document.getElementById("probability").innerText = `현재 츄르 성공 확률: ${prob.toFixed(1)}%`;
            }

            function toggleGameInfo() {
                const info = document.getElementById("gameInfo");
                info.style.display = info.style.display === "none" ? "block" : "none";
            }

            function resetGame() {
                alert("실패! 고양이가 츄르를 거부했어요. 😿 게임을 다시 시작합니다.");
                level = 1;
                laserCount = 3;
                laserBoostActive = false;
                updateLevelDisplay();
                updateLaserButton();
                updateProbability();
            }

            // 초기 표시
            updateLevelDisplay();
            updateLaserButton();
            updateProbability();
        </script>
    </body>
    </html>
    """

# 💡 외부 접속 허용: 0.0.0.0, 포트 5000
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
