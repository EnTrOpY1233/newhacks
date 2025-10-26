<template>
  <div v-if="weather || events.length > 0" class="weather-info-container">
    <!-- Weather Information -->
    <div v-if="weather" class="weather-card">
      <h3 class="card-title">
        <span class="title-icon">🌤️</span>
        Weather Information
      </h3>
      <div class="weather-content">
        <div class="weather-main">
          <img 
            v-if="weather.icon" 
            :src="`https://openweathermap.org/img/wn/${weather.icon}@2x.png`" 
            :alt="weather.description"
            class="weather-icon"
          />
          <div class="weather-details">
            <div class="temperature">{{ Math.round(weather.temperature) }}°C</div>
            <div class="description">{{ weather.description }}</div>
          </div>
        </div>
        <div class="weather-extra">
          <div class="weather-item">
            <span class="item-label">Feels like:</span>
            <span class="item-value">{{ Math.round(weather.feels_like) }}°C</span>
          </div>
          <div class="weather-item">
            <span class="item-label">Humidity:</span>
            <span class="item-value">{{ weather.humidity }}%</span>
          </div>
          <div class="weather-item">
            <span class="item-label">Wind:</span>
            <span class="item-value">{{ weather.wind_speed }} m/s</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Events Information -->
    <div v-if="events.length > 0" class="events-card">
      <h3 class="card-title">
        <span class="title-icon">🎉</span>
        Special Events & Festivals
      </h3>
      <div class="events-list">
        <div 
          v-for="(event, index) in events" 
          :key="index" 
          class="event-item"
          :class="`impact-${event.impact}`"
        >
          <div class="event-header">
            <span class="event-name">{{ event.name }}</span>
            <span class="event-type">{{ event.type }}</span>
          </div>
          <p class="event-description">{{ event.description }}</p>
          <div class="event-impact">
            <span class="impact-label">Impact:</span>
            <span class="impact-badge" :class="`impact-${event.impact}`">
              {{ event.impact }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  weather: {
    type: Object,
    default: null
  },
  events: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.weather-info-container {
  margin: 2rem 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.weather-card,
.events-card {
  background: white;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #202123;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #10A37F;
}

.title-icon {
  font-size: 1.5rem;
}

.weather-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.weather-main {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.weather-icon {
  width: 80px;
  height: 80px;
}

.weather-details {
  flex: 1;
}

.temperature {
  font-size: 2.5rem;
  font-weight: 700;
  color: #10A37F;
}

.description {
  font-size: 1.1rem;
  color: #6E6E80;
  text-transform: capitalize;
}

.weather-extra {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E5E5E5;
}

.weather-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-label {
  font-size: 0.85rem;
  color: #6E6E80;
}

.item-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #202123;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.event-item {
  padding: 1rem;
  border-radius: 6px;
  background: #FAFAFA;
  border-left: 4px solid #10A37F;
  transition: all 0.15s;
}

.event-item:hover {
  background: #F0FDF9;
  transform: translateX(4px);
}

.event-item.impact-high {
  border-left-color: #EF4444;
}

.event-item.impact-medium {
  border-left-color: #F59E0B;
}

.event-item.impact-low {
  border-left-color: #10B981;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.event-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #202123;
}

.event-type {
  font-size: 0.85rem;
  padding: 0.25rem 0.75rem;
  background: #E5E5E5;
  border-radius: 12px;
  color: #6E6E80;
  text-transform: capitalize;
}

.event-description {
  font-size: 0.95rem;
  color: #6E6E80;
  margin-bottom: 0.5rem;
}

.event-impact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.impact-label {
  font-size: 0.85rem;
  color: #6E6E80;
}

.impact-badge {
  font-size: 0.8rem;
  padding: 0.2rem 0.6rem;
  border-radius: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.impact-badge.impact-high {
  background: #FEE2E2;
  color: #EF4444;
}

.impact-badge.impact-medium {
  background: #FEF3C7;
  color: #F59E0B;
}

.impact-badge.impact-low {
  background: #D1FAE5;
  color: #10B981;
}

@media (max-width: 768px) {
  .weather-info-container {
    grid-template-columns: 1fr;
  }
  
  .weather-extra {
    grid-template-columns: 1fr;
  }
}
</style>
