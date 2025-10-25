<template>
  <div class="itinerary-container">
    <h2>📅 {{ itinerary.city }} Travel Itinerary</h2>
    <p class="duration">{{ itinerary.days }} Day Trip</p>

    <div v-for="(day, index) in itinerary.schedule" :key="index" class="day-section">
      <h3 class="day-title">Day {{ index + 1 }}</h3>
      
      <div v-for="(place, placeIndex) in day.places" :key="placeIndex" class="place-card">
        <div class="place-header">
          <h4 class="place-name">{{ place.name }}</h4>
          <button 
            @click="$emit('play-audio', place)" 
            class="audio-button"
            :title="`Listen to ${place.name} introduction`"
          >
            🔊 Play Audio
          </button>
        </div>
        
        <p class="place-description">{{ place.description }}</p>
        
        <div class="place-details">
          <span v-if="place.duration" class="detail-item">
            ⏱️ {{ place.duration }}
          </span>
          <span v-if="place.category" class="detail-item category">
            🏷️ {{ place.category }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="itinerary.tips" class="tips-section">
      <h3>💡 Travel Tips</h3>
      <ul>
        <li v-for="(tip, index) in itinerary.tips" :key="index">{{ tip }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  itinerary: {
    type: Object,
    required: true
  }
})

defineEmits(['play-audio'])
</script>

<style scoped>
.itinerary-container {
  max-height: 800px;
  overflow-y: auto;
}

.itinerary-container h2 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
}

.duration {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 1rem;
}

.day-section {
  margin-bottom: 2rem;
}

.day-title {
  color: #667eea;
  font-size: 1.3rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.place-card {
  background: #f9f9f9;
  padding: 1.2rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border-left: 4px solid #667eea;
  transition: transform 0.2s, box-shadow 0.2s;
}

.place-card:hover {
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.place-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.place-name {
  color: #333;
  font-size: 1.2rem;
  flex: 1;
}

.audio-button {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.audio-button:hover {
  background: #5568d3;
  transform: scale(1.05);
}

.place-description {
  color: #555;
  line-height: 1.6;
  margin-bottom: 0.8rem;
}

.place-details {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.detail-item {
  color: #777;
  font-size: 0.9rem;
  background: white;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
}

.category {
  background: #fff3cd;
  color: #856404;
}

.tips-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #e8f4f8;
  border-radius: 8px;
}

.tips-section h3 {
  color: #0277bd;
  margin-bottom: 1rem;
}

.tips-section ul {
  list-style: none;
  padding: 0;
}

.tips-section li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
  color: #333;
}

.tips-section li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #0277bd;
  font-weight: bold;
}
</style>

