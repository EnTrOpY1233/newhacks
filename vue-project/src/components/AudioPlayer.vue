<template>
  <div class="audio-player-overlay" @click.self="$emit('close')">
    <div class="audio-player">
      <div class="player-header">
        <h3>🎧 {{ title }}</h3>
        <button @click="$emit('close')" class="close-button">✕</button>
      </div>
      
      <div class="player-body">
        <audio 
          ref="audioElement" 
          :src="audioUrl" 
          controls 
          autoplay
          class="audio-element"
        >
          Your browser does not support audio playback
        </audio>
      </div>
      
      <div class="player-footer">
        <p class="hint">🔊 Playing attraction audio guide</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  audioUrl: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: 'Attraction Guide'
  }
})

defineEmits(['close'])

const audioElement = ref(null)

onMounted(() => {
  if (audioElement.value) {
    audioElement.value.volume = 0.7
  }
})
</script>

<style scoped>
.audio-player-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.audio-player {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  min-width: 400px;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.player-header h3 {
  color: #333;
  margin: 0;
  font-size: 1.3rem;
}

.close-button {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-button:hover {
  color: #333;
  background: #f0f0f0;
}

.player-body {
  margin-bottom: 1rem;
}

.audio-element {
  width: 100%;
  outline: none;
}

.player-footer {
  text-align: center;
}

.hint {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

@media (max-width: 600px) {
  .audio-player {
    min-width: 90%;
    margin: 0 1rem;
  }
}
</style>

