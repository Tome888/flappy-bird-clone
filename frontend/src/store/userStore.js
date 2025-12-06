import { reactive } from "vue";

const storedState = localStorage.getItem("userStore");
const initialState = storedState
  ? JSON.parse(storedState)
  : {
      username: null,
      highscore: 0,
      leaderboardRank: null,
    };

export const userStore = reactive({
  username: initialState.username,
  highscore: initialState.highscore,
  leaderboardRank: initialState.leaderboardRank,

  saveState() {
    localStorage.setItem(
      "userStore",
      JSON.stringify({
        username: this.username,
        highscore: this.highscore,
        leaderboardRank: this.leaderboardRank,
      })
    );
  },

  login(username, highscore, rank) {
    this.username = username;
    this.highscore = highscore;
    this.leaderboardRank = rank;
    this.saveState();
  },

  logout() {
    this.username = null;
    this.highscore = 0;
    this.leaderboardRank = null;
    localStorage.removeItem("userStore");
  },

  updateHighscore(newScore) {
    if (newScore > this.highscore) {
      this.highscore = newScore;
      this.saveState();
    }
  },
});
