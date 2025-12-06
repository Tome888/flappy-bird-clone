<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="popup welcome-popup">
      <h2 class="popup-title">Welcome to Cluster Bird! 🐦</h2>

      <div class="content">
        <h3>How to Play</h3>
        <p>The goal is simple: **don't hit the pipes or the ground!**</p>

        <div class="controls-section">
          <p>Tap/Click or press the Spacebar to make the bird jump.</p>
          <div class="control-key-group">
            <span class="control-key">SPACEBAR</span>
            <span class="control-or">OR</span>
            <span class="control-key">MOUSE CLICK</span>
          </div>
        </div>

        <div class="login-section">
          <h3>Saving Your Score</h3>
          <p>
            To **save your high score** and compete on the global leaderboard,
            you must be logged in.
          </p>
          <p>
            If you don't login, you can still play, but your score will not be
            saved (Guest Mode).
          </p>
        </div>
      </div>

      <button @click="handleClose" class="btn primary-btn close-btn-bottom">
        Got It! Let's Play
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from "vue";

const emit = defineEmits(["close"]);
const WELCOME_FLAG = "hasSeenWelcomePopup";

function handleClose() {
  localStorage.setItem(WELCOME_FLAG, "true");
  emit("close");
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup {
  background: var(--color-popup-bg);
  padding: 30px;
  border-radius: 0;
  border: 6px solid var(--pixel-border-color);
  box-shadow: 8px 8px 0 var(--pixel-shadow-color);
  width: 90%;
  max-width: 400px;
  text-align: center;
  color: var(--color-text-dark);
}

.popup-title {
  color: var(--color-primary);
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 2em;
}

h3 {
  margin-top: 15px;
  color: var(--color-text-dark);
  border-bottom: 2px dashed var(--pixel-border-color);
  padding-bottom: 5px;
}

p {
  margin: 10px 0;
  font-size: 1.1em;
}

.controls-section {
  padding: 15px;
  border: 3px solid var(--color-secondary);
  background-color: white;
  margin: 15px 0;
}

.control-key-group {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.control-key {
  background-color: var(--color-text-dark);
  color: white;
  padding: 5px 10px;
  border: 2px solid var(--pixel-border-color);
  box-shadow: 2px 2px 0 var(--pixel-shadow-color);
  font-weight: bold;
  font-size: 0.9em;
}

.control-or {
  font-weight: bold;
  color: var(--color-secondary);
}

.login-section {
  margin-top: 25px;
  padding: 10px;
  background-color: #ffeaa7;
}

.primary-btn {
  background-color: var(--color-primary);
  color: white;
  width: 100%;
  margin-top: 20px;
}
</style>
