<template>
  <div class="game-container">
    <canvas ref="canvas" width="400" height="600"></canvas>
    <div v-if="assetsLoaded && countdown > 0" class="countdown">
      {{ countdown }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";

const canvas = ref(null);
const countdown = ref(3);
let animationFrame = null;

const gravity = 0.05;
const jump = -2.5;
const pipeSpeed = 1.3;
const pipeSpawnInterval = 130;
const gameHeight = 600;
const groundHeight = 50;

const bird = { x: 80, y: 300, width: 34, height: 24, velocity: 0, rotation: 0 };
const maxRotation = Math.PI / 2;
const minRotation = -Math.PI / 8;
const rotationSpeed = 0.05;

let pipes = [];
let pipeSpawnTimer = 0;
let score = 0;
let gameRunning = false;
let scoreToEmit = 0;

let birdImg, pipeTopImg, pipeBottomImg, groundImg;
let jumpSound, scoreSound, hitSound;
const assetsLoaded = ref(false);

const emit = defineEmits(["gameOver"]);

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () =>
      reject(new Error(`Failed to load image: ${src}. Check file path!`));
    img.src = src;
  });
}

async function loadAssets() {
  try {
    [birdImg, pipeTopImg, pipeBottomImg, groundImg] = await Promise.all([
      loadImage("/assets/bird.png"),
      loadImage("/assets/pipe_top.png"),
      loadImage("/assets/pipe_bottom.png"),
      loadImage("/assets/ground.png"),
    ]);

    jumpSound = new Audio("/assets/wing-flap.mp3");
    scoreSound = new Audio("/assets/arcade-fx.mp3");
    hitSound = new Audio("/assets/sfx_hit.mp3");

    assetsLoaded.value = true;
  } catch (error) {
    console.error("CRITICAL ERROR: Failed to load game assets.", error.message);
  }
}

onMounted(async () => {
  await loadAssets();

  nextTick(() => {
    if (assetsLoaded.value) {
      const countdownInterval = setInterval(() => {
        countdown.value--;
        if (countdown.value < 0) {
          clearInterval(countdownInterval);
          startGame();
        }
      }, 1000);
    }

    window.addEventListener("click", handleJump);
    window.addEventListener("keydown", handleKeyDown);
  });
});

onBeforeUnmount(() => {
  window.removeEventListener("click", handleJump);
  window.removeEventListener("keydown", handleKeyDown);
  cancelAnimationFrame(animationFrame);
});

function handleJump() {
  if (gameRunning) {
    bird.velocity = jump;
    jumpSound.currentTime = 0;
    jumpSound
      .play()
      .catch((e) => console.log("Jump sound prevented by browser."));
  }
}

function handleKeyDown(e) {
  if (e.code === "Space") {
    e.preventDefault();
    handleJump();
  }
}

function startGame() {
  countdown.value = 0;
  score = 0;
  scoreToEmit = 0;
  pipes = [];
  pipeSpawnTimer = 0;
  bird.y = 300;
  bird.velocity = 0;
  bird.rotation = 0;
  gameRunning = true;
  animate();
}

function animate() {
  const ctx = canvas.value.getContext("2d");
  const { width, height } = canvas.value;
  ctx.clearRect(0, 0, width, height);

  bird.velocity += gravity;
  bird.y += bird.velocity;

  let targetRotation = maxRotation * (bird.velocity / 10);
  targetRotation = Math.min(maxRotation, Math.max(minRotation, targetRotation));
  bird.rotation += (targetRotation - bird.rotation) * rotationSpeed;

  ctx.save();
  ctx.translate(bird.x + bird.width / 2, bird.y + bird.height / 2);
  ctx.rotate(bird.rotation);
  ctx.drawImage(
    birdImg,
    -bird.width / 2,
    -bird.height / 2,
    bird.width,
    bird.height
  );
  ctx.restore();

  pipeSpawnTimer++;
  if (pipeSpawnTimer >= pipeSpawnInterval) {
    const gap = 160;
    const minTop = 70;
    const maxTop = height - groundHeight - gap - minTop;
    const topHeight = Math.random() * maxTop + minTop;

    pipes.push({
      x: width,
      top: topHeight,
      bottom: height - topHeight - gap - groundHeight,
      width: 52,
      scored: false,
    });
    pipeSpawnTimer = 0;
  }

  for (let i = 0; i < pipes.length; i++) {
    const p = pipes[i];
    p.x -= pipeSpeed;

    ctx.drawImage(pipeTopImg, p.x, 0, p.width, p.top);
    ctx.drawImage(
      pipeBottomImg,
      p.x,
      height - p.bottom - groundHeight,
      p.width,
      p.bottom + groundHeight
    );

    const horizontalOverlap =
      bird.x < p.x + p.width && bird.x + bird.width > p.x;

    if (horizontalOverlap) {
      if (
        bird.y < p.top ||
        bird.y + bird.height > height - p.bottom - groundHeight
      ) {
        endGame();
        return;
      }
    }

    if (!p.scored && bird.x > p.x + p.width) {
      p.scored = true;
      score++;
      scoreSound.currentTime = 0;
      scoreSound.play().catch((e) => console.log("Score sound prevented."));
    }

    if (p.x + p.width < 0) {
      pipes.splice(i, 1);
      i--;
    }
  }

  if (bird.y + bird.height > height - groundHeight || bird.y < 0) {
    endGame();
    return;
  }

  ctx.drawImage(groundImg, 0, height - groundHeight, width, groundHeight);

  ctx.fillStyle = "white";
  ctx.strokeStyle = "black";
  ctx.lineWidth = 3;
  ctx.font = "bold 48px Arial";
  ctx.textAlign = "center";
  ctx.fillText(score, width / 2, 60);
  ctx.strokeText(score, width / 2, 60);

  animationFrame = requestAnimationFrame(animate);
}

function endGame() {
  hitSound.currentTime = 0;
  hitSound.play().catch((e) => console.log("Hit sound prevented."));

  gameRunning = false;
  cancelAnimationFrame(animationFrame);
  scoreToEmit = score;
  emit("gameOver", scoreToEmit);
}
</script>

<style scoped>
.game-container {
  text-align: center;
  position: relative;
}
canvas {
  border: 4px solid var(--pixel-border-color, black);
  box-shadow: 6px 6px 0 var(--pixel-shadow-color, rgba(0, 0, 0, 0.4));
  display: block;
  margin: 20px auto;
  background: var(--color-bg, skyblue);
  cursor: pointer;
}
.countdown {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 72px;
  color: var(--color-error, red);
  font-weight: bold;
  -webkit-text-stroke: 4px var(--color-text-dark, black);
  text-stroke: 4px var(--color-text-dark, black);
  z-index: 10;
}
</style>
