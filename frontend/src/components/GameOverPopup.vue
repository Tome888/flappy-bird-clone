<template>
  <div class="modal-overlay" @click.self="$emit('home')">
    <div class="popup game-over-popup">
      <h2 class="popup-title">GAME OVER 💥</h2>

      <div class="score-display">
        <p class="score-label">Final Score</p>
        <p class="final-score">{{ score }}</p>
      </div>

      <div class="buttons">
        <button
          @click="$emit('playAgain')"
          class="btn primary-btn play-again-btn"
        >
          Play Again
        </button>
        <button @click="$emit('home')" class="btn secondary-btn back-home-btn">
          Back Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  score: {
    type: Number,
    required: true,
  },
});
defineEmits(["home", "playAgain"]);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup {
  background: var(--color-popup-bg);
  padding: 40px;
  border-radius: 0;
  box-shadow: 12px 12px 0 var(--pixel-shadow-color);
  width: 90%;
  max-width: 350px;
  text-align: center;
  border: 8px solid var(--color-error);
  position: relative;
}

.popup-title {
  font-size: 2.5em;
  color: var(--color-error);
  margin-top: 0;
  margin-bottom: 30px;
  font-weight: 900;
}

.score-display {
  margin-bottom: 30px;
  padding: 15px 0;
  background-color: white;
  border: 4px solid var(--pixel-border-color);
  border-radius: 0;
}

.score-label {
  margin: 0;
  font-size: 1.1em;
  color: var(--color-text-dark);
}

.final-score {
  margin: 5px 0 0;
  font-size: 3.5em;
  font-weight: bold;
  color: var(--color-text-dark);
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.primary-btn {
  background-color: var(--color-primary);
  color: white;
}

.secondary-btn {
  background-color: var(--color-secondary);
  color: white;
}
</style>
