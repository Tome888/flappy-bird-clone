<template>
  <div class="home-screen">
    <h1 v-if="userStore.username" class="welcome-text">
      Welcome, {{ userStore.username }}!
    </h1>
    <h1 v-else class="welcome-text">Welcome, Guest!</h1>

    <p v-if="userStore.username" class="score-display">
      Your High Score: {{ userStore.highscore }}
    </p>

    <div class="main-actions">
      <button @click="$emit('play')" class="btn primary-btn">Start Game</button>

      <button @click="$emit('showLeaderboard')" class="btn secondary-btn">
        View Leaderboard
      </button>
    </div>

    <div class="user-actions">
      <button
        v-if="userStore.username"
        @click="userStore.logout()"
        class="btn tertiary-btn"
      >
        Logout
      </button>
      <button v-else @click="$emit('showLogin')" class="btn tertiary-btn">
        Login / Register
      </button>
    </div>
  </div>
</template>

<script setup>
import { userStore } from "../store/userStore";
defineEmits(["play", "showLogin", "showLeaderboard"]);
</script>

<style scoped>
.home-screen {
  text-align: center;
  padding: 40px 30px;
  background-color: var(--color-popup-bg);
  color: var(--color-text-dark);
  border-radius: 0;
  border: 8px solid var(--pixel-border-color);
  box-shadow: 10px 10px 0 var(--pixel-shadow-color);
}

.welcome-text {
  color: var(--color-primary);
  font-size: 2.2em;
  margin-bottom: 5px;
}

.score-display {
  font-size: 1.2em;
  margin-bottom: 30px;
  font-weight: bold;
}

.main-actions {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.user-actions {
  margin-top: 20px;
  border-top: 2px dashed var(--pixel-border-color);
  padding-top: 20px;
}

.primary-btn {
  background-color: var(--color-primary);
  color: white;
}

.secondary-btn {
  background-color: var(--color-secondary);
  color: white;
}

.tertiary-btn {
  background-color: white;
  color: var(--color-text-dark);
}
</style>
