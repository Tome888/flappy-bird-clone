<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="popupLeader leaderboard-popup">
      <h2 class="popup-title">Global Leaderboard 🌎</h2>

      <table class="leaderboard-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>High Score</th>
          </tr>
        </thead>
      </table>

      <div class="table-scroll-container">
        <table>
          <tbody>
            <tr v-if="leaderboard.length === 0">
              <td colspan="3" class="no-data">
                Loading or no scores submitted yet...
              </td>
            </tr>

            <tr
              v-for="(item, index) in leaderboard"
              :key="item.username"
              :class="{ highlight: index < 3 }"
            >
              <td class="rank-cell">
                {{ index + 1 }}
              </td>
              <td>{{ item.username }}</td>
              <td class="score-cell">{{ item.highscore }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="$emit('close')" class="btn primary-btn close-btn-bottom">
        Close
      </button>

      <button @click="$emit('close')" class="btn close-btn">&times;</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getLeaderboard } from "../api/api";
const leaderboard = ref([]);
onMounted(async () => {
  const data = await getLeaderboard();
  if (Array.isArray(data)) {
    leaderboard.value = data;
  } else {
    leaderboard.value = [];
  }
});
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

.popupLeader {
  background: var(--color-popup-bg);
  padding: 30px;
  border-radius: 0;
  border: 6px solid var(--pixel-border-color);
  box-shadow: 8px 8px 0 var(--pixel-shadow-color);
  width: 90%;
  max-width: 450px;
  text-align: center;
  position: relative;

  display: flex;
  flex-direction: column;
  max-height: 90vh;
}
.popup-title {
  color: var(--color-text-dark);
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.8em;
  flex-shrink: 0;
}

.table-scroll-container {
  max-height: 350px;
  overflow-y: auto;
  margin-bottom: 25px;
  flex-grow: 1;
}
.table-scroll-container table {
  width: 100%;
  border-collapse: collapse;
}

.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 0;
  background-color: var(--color-popup-bg);
  border-radius: 0;
  overflow: hidden;
  flex-shrink: 0;
}
.leaderboard-table th,
.table-scroll-container table td {
  padding: 12px 10px;
  text-align: left;
  border-bottom: 1px solid var(--pixel-border-color);
}

.leaderboard-table th {
  background-color: var(--color-primary);
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.9em;
  letter-spacing: 0.5px;
}
.table-scroll-container table td {
  background-color: white;
  color: var(--color-text-dark);
}

.table-scroll-container .highlight {
  background-color: #fcfcfc;
  font-weight: bold;
}

.score-cell {
  text-align: right;
  font-weight: bold;
}

.no-data {
  color: var(--color-text-dark);
}

.primary-btn {
  background-color: var(--color-primary);
  color: white;
}
.close-btn {
  position: absolute;
  top: -15px;
  right: -15px;
  background: var(--color-secondary);
  color: white;
  font-size: 1.5em;
  padding: 0 5px;
  width: 35px;
  height: 35px;
  line-height: 30px;
  border: 4px solid var(--pixel-border-color);
}
</style>
