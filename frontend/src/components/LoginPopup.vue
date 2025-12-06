<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="popup login-popup">
      <h2 class="popup-title">Login / Register</h2>

      <div class="input-group">
        <label for="username">Username</label>
        <input
          id="username"
          v-model="username"
          placeholder="Enter username"
          :class="{ 'input-error': error }"
        />
      </div>

      <div class="input-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="Enter password"
          :class="{ 'input-error': error }"
        />
      </div>

      <p v-if="error" class="error-message">⚠️ {{ error }}</p>

      <div class="buttons">
        <button @click="handleLogin" class="btn primary-btn">Login</button>
        <button @click="handleRegister" class="btn secondary-btn">
          Register
        </button>
      </div>

      <button @click="emit('close')" class="btn close-btn">&times;</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { login, register } from "../api/api";
import { userStore } from "../store/userStore";

const emit = defineEmits(["close"]);
const username = ref("");
const password = ref("");
const error = ref("");
async function handleLogin() {
  error.value = "";
  if (!username.value || !password.value) {
    error.value = "Username and password are required.";
    return;
  }
  try {
    const res = await login(username.value, password.value);
    userStore.login(res.username, res.highscore, 1);
    emit("close");
  } catch (err) {
    const errorMessage = err?.detail || "Invalid username or password.";
    error.value = errorMessage;
  }
}
async function handleRegister() {
  error.value = "";
  if (!username.value || !password.value) {
    error.value = "Username and password are required.";
    return;
  }
  try {
    const res = await register(username.value, password.value);
    userStore.login(res.username, res.highscore, 1);
    emit("close");
  } catch (err) {
    const errorMessage =
      err?.detail || "Registration failed. Try a different username.";
    error.value = errorMessage;
  }
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
  position: relative;
  background: var(--color-popup-bg);
  padding: 30px;
  border-radius: 0;
  border: 6px solid var(--pixel-border-color);
  box-shadow: 8px 8px 0 var(--pixel-shadow-color);
  width: 320px;
  text-align: center;
}

.popup-title {
  color: var(--color-text-dark);
  margin-bottom: 25px;
  font-size: 1.8em;
}

.input-group {
  text-align: left;
  margin-bottom: 15px;
}

input {
  border: 2px solid var(--pixel-border-color);
  border-radius: 0;
  padding: 8px;
  background-color: white;
  color: var(--color-text-dark);
}

input:focus {
  border-color: var(--color-primary);
  outline: none;
}

.input-error {
  border-color: var(--color-error) !important;
}

.error-message {
  color: var(--color-error);
  font-weight: bold;
  margin-top: 10px;
}

.buttons {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-top: 25px;
}

.primary-btn {
  background-color: var(--color-primary);
  color: white;
}
.secondary-btn {
  background-color: var(--color-secondary);
  color: white;
}

.close-btn {
  position: absolute;
  top: -15px;
  right: -15px;
  background: var(--color-error);
  color: white;
  font-size: 1.5em;
  padding: 0 5px;
  width: 35px;
  height: 35px;
  line-height: 30px;
  border: 4px solid var(--pixel-border-color);
}
</style>
