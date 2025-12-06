<template>
  <HomeScreen
    v-if="screen === 'home'"
    @play="startGame"
    @showLogin="showLogin = true"
    @showLeaderboard="showLeaderboard = true"
  />

  <GameCanvas v-if="screen === 'game'" @gameOver="handleGameOver" />

  <GameOverPopup
    v-if="screen === 'gameover'"
    :score="lastScore"
    @home="screen = 'home'"
    @playAgain="startGame"
  />

  <LoginPopup v-if="showLogin" @close="showLogin = false" />
  <LeaderboardPopup v-if="showLeaderboard" @close="showLeaderboard = false" />

  <WelcomePopup v-if="showWelcome" @close="showWelcome = false" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import HomeScreen from "./components/HomeScreen.vue";
import GameCanvas from "./components/GameCanvas.vue";
import LoginPopup from "./components/LoginPopup.vue";
import LeaderboardPopup from "./components/LeaderboardPopup.vue";
import GameOverPopup from "./components/GameOverPopup.vue";
import WelcomePopup from "./components/WelcomePopup.vue";

import { submitScore } from "./api/api";
import { userStore } from "./store/userStore";

const screen = ref("home");
const showLogin = ref(false);
const showLeaderboard = ref(false);
const lastScore = ref(0);

const showWelcome = ref(false);

onMounted(() => {
  const WELCOME_FLAG = "hasSeenWelcomePopup";
  if (!localStorage.getItem(WELCOME_FLAG)) {
    showWelcome.value = true;
  }
});

function startGame() {
  screen.value = "game";
}

async function handleGameOver(score) {
  lastScore.value = score;
  screen.value = "gameover";

  if (userStore.username) {
    try {
      const result = await submitScore(userStore.username, score);

      userStore.updateHighscore(score);

      if (result.newRank) {
        userStore.leaderboardRank = result.newRank;
        userStore.saveState();
      }
    } catch (error) {
      console.error("Failed to submit score:", error);
    }
  }
}
</script>

<style>
:root {
  --color-bg: #3498db;
  --color-popup-bg: #f9e79f;
  --color-primary: #27ae60;
  --color-secondary: #f39c12;
  --color-text-dark: #2c3e50;
  --color-error: #e74c3c;
  --pixel-border-color: #2c3e50;
  --pixel-shadow-color: rgba(0, 0, 0, 0.4);
}

#app {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Arial", sans-serif;
  background-color: var(--color-bg);
  color: var(--color-text-dark);
}

.btn {
  border: 4px solid var(--pixel-border-color);
  box-shadow: 4px 4px 0 var(--pixel-shadow-color);
  padding: 10px 20px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.05s ease;
}
.btn:active {
  box-shadow: 0 0 0 var(--pixel-shadow-color);
  transform: translate(4px, 4px);
}
</style>
