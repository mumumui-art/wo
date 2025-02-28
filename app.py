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
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
                text-align: center;
                position: relative;
            }
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                flex-direction: column;
            }
            #level, #maxLevel {
                font-size: 24px;
                margin-top: 10px;
            }
            button {
                margin-top: 20px;
                padding: 10px 20px;
                font-size: 18px;
                cursor: pointer;
                border: none;
                border-radius: 5px;
                width: 250px;
            }
            #laserButton {
                background-color: #ff8c00;
                color: white;
            }
            #feedButton {
                background-color: #66cc66;
                color: white;
            }
            .probability {
                font-size: 20px;
                margin-top: 10px;
            }
            #gameInfo {
                margin-top: 10px;
                font-size: 18px;
                display: none;
                text-align: left;
                width: 400px;
                margin-top: 20px;
                position: absolute;
                top: 20px;
                left: 20px;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            }
            #showGameInfoButton {
                position: absolute;
                top: 20px;
                left: 20px;
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <button id="showGameInfoButton" onclick="toggleGameInfo()">게임 설명 보기</button>

        <div class="container">
            <div>
                <h1>🐱 고양이에게 츄르 먹이기 🐱</h1>
                <p id="level">츄르 주세요</p>
                <p id="maxLevel" style="font-size: 20px;"></p>
                <button id="feedButton" onclick="feedCat()">츄르 주기</button>
                <button id="laserButton" onclick="playWithLaser()">레이저로 놀아주기 (3)</button>
            </div>
            <div>
                <p class="probability" id="probability"></p>
            </div>
        </div>

        <div id="gameInfo">
            <h3>게임 목표:</h3>
            <p>이 게임의 목표는 귀여운 고양이에게 츄르를 먹여 최대 츄르 개수를 기록하는 것입니다. 고양이는 배가 고플 때만 츄르를 먹습니다. 당신의 역할은 고양이를 배고프게 하여 츄르를 먹게 만드는 것입니다.</p>

            <h3>게임 규칙:</h3>
            <ul>
                <li><strong>츄르 주기:</strong> 버튼을 클릭하면 고양이가 츄르를 먹을 확률이 나타납니다. 성공적으로 츄르를 먹으면 레벨이 올라갑니다.</li>
                <li><strong>레이저로 놀아주기:</strong> 게임 중에 레이저를 사용하면 고양이가 더 쉽게 츄르를 먹을 수 있습니다. 하지만 레이저는 제한된 횟수만 사용 가능합니다.</li>
                <li><strong>확률:</strong> 고양이가 츄르를 먹을 확률은 점점 변동되며, 레벨이 올라갈수록 고양이가 배불러서 츄르를 잘 먹지 않게 됩니다.</li>
                <li><strong>게임 종료:</strong> 고양이가 츄르를 다 먹으면 게임이 종료되며, 당신의 기록을 확인할 수 있습니다.</li>
            </ul>

            <h3>게임 팁:</h3>
            <ul>
                <li>레이저를 사용할 때는 확률을 두 배로 높일 수 있어요. 하지만 레이저는 한정되어 있으니 잘 사용하세요!</li>
                <li>고양이의 레벨이 높아질수록 츄르를 먹을 확률이 낮아지니, 조금 더 전략적으로 플레이해보세요.</li>
            </ul>

            <p><strong>제작자 : 조연우</strong></p>
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
                    if (laserBoostActive) {
                        if (rand <= probabilities[level - 1] * 2) {
                            level++;
                            maxCatLevel = Math.max(maxCatLevel, level);
                            updateLevelDisplay();
                            laserBoostActive = false;
                        } else {
                            resetGame();
                        }
                    } else {
                        if (rand <= probabilities[level - 1]) {
                            level++;
                            maxCatLevel = Math.max(maxCatLevel, level);
                            updateLevelDisplay();
                        } else {
                            resetGame();
                        }
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
                    let rand = Math.random();
                    if (rand <= 0.5) {
                        laserBoostActive = true;
                        alert("레이저 놀이!! 고양이가 배고파서 츄르를 무조건 먹을거 같아요");
                    } else {
                        alert("레이저로 놀아주었지만, 배불러서 움직이지를 않네요");
                    }
                    updateLaserButton();
                } else {
                    alert("레이저를 더 이상 사용할 수 없습니다!");
                }
            }

            function updateLaserButton() {
                const laserButton = document.getElementById("laserButton");
                if (laserCount > 0) {
                    laserButton.innerText = "레이저로 놀아주기 (" + laserCount + ")";
                } else {
                    laserButton.disabled = true;
                    laserButton.innerText = "레이저로 놀아주기 종료";
                }
            }

            function updateLevelDisplay() {
                document.getElementById("level").innerText = "츄르 " + level + "개 냠";
                document.getElementById("maxLevel").innerText = "최대 츄르 개수: " + maxCatLevel;
            }

            function updateProbability() {
                const probabilityText = probabilities[level - 1] * 100;
                document.getElementById("probability").innerText = `츄르 먹을 확률: ${probabilityText.toFixed(2)}%`;
            }

            function toggleGameInfo() {
                const gameInfo = document.getElementById("gameInfo");
                gameInfo.style.display = gameInfo.style.display === "none" ? "block" : "none";
            }

            function resetGame() {
                level = 1;
                maxCatLevel = 1;
                updateLevelDisplay();
                alert("게임 종료! 다시 시작합니다.");
            }

            updateLaserButton();
            updateProbability();
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=False)
