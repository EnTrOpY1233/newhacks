<template>
  <div class="itinerary-container">
    <h2>{{ itinerary.city }} Travel Itinerary</h2>
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
            Play Audio
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
      <h3>Travel Tips</h3>
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
  color: #202123;
  margin-bottom: 0.8rem;
  font-size: 2rem;
  font-weight: 700;
}

.duration {
  color: #6E6E80;
  margin-bottom: 2rem;
  font-size: 1.15rem;
}

.day-section {
  margin-bottom: 2.5rem;
}

.day-title {
  color: #10A37F;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid #E5E5E5;
}

.place-card {
  background: #FAFAFA;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  border: 1px solid #E5E5E5;
  transition: all 0.15s;
}

.place-card:hover {
  border-color: #10A37F;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.place-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.place-name {
  color: #202123;
  font-size: 1.35rem;
  font-weight: 600;
  flex: 1;
}

.audio-button {
  padding: 0.7rem 1.3rem;
  background: #10A37F;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.95rem;
  font-weight: 500;
}

.audio-button:hover {
  background: #0E8C6D;
}

.place-description {
  color: #565869;
  line-height: 1.7;
  margin-bottom: 1rem;
  font-size: 1rem;
}

.place-details {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.detail-item {
  color: #6E6E80;
  font-size: 0.9rem;
  background: white;
  padding: 0.4rem 0.9rem;
  border-radius: 4px;
  border: 1px solid #E5E5E5;
}

.category {
  background: #FEF3C7;
  color: #92400E;
  border-color: #FDE68A;
}

.tips-section {
  margin-top: 2.5rem;
  padding: 2rem;
  background: #F0FDF4;
  border-radius: 8px;
  border: 1px solid #D1FAE5;
}

.tips-section h3 {
  color: #065F46;
  margin-bottom: 1.2rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.tips-section ul {
  list-style: none;
  padding: 0;
}

.tips-section li {
  padding: 0.6rem 0;
  padding-left: 2rem;
  position: relative;
  color: #374151;
  font-size: 1rem;
  line-height: 1.6;
}

.tips-section li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10A37F;
  font-weight: bold;
  font-size: 1.1rem;
}
</style>

