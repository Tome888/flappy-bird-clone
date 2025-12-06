const API_URL = "http://127.0.0.1:8000";

export async function register(username, password) {
  return fetch(`${API_URL}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  }).then((res) => res.json());
}

export async function login(username, password) {
  return fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  }).then((res) => res.json());
}

export async function submitScore(username, score) {
  return fetch(`${API_URL}/score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, score }),
  }).then((res) => res.json());
}

export async function getLeaderboard() {
  return fetch(`${API_URL}/leaderboard`).then((res) => res.json());
}
