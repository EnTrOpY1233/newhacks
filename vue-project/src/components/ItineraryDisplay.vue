<template>
  <div class="itinerary-container">
    <h2>{{ itinerary.city }} Travel Itinerary</h2>
    <p class="duration">{{ itinerary.days }} Day Trip</p>

    <!-- Day Tabs Navigation -->
    <div class="day-tabs">
      <button 
        v-for="(day, index) in itinerary.schedule" 
        :key="index"
        @click="selectDay(index)"
        :class="['day-tab', { active: selectedDay === index }]"
      >
        Day {{ index + 1 }}
      </button>
    </div>

    <!-- Selected Day Content -->
    <div v-if="currentDaySchedule" class="day-content">
      <h3 class="day-title">Day {{ selectedDay + 1 }}</h3>
      
      <div v-for="(place, placeIndex) in currentDaySchedule.places" :key="placeIndex" class="place-card">
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
            {{ place.duration }}
          </span>
          <span v-if="place.category" class="detail-item category">
            {{ place.category }}
          </span>
        </div>
        
        <!-- Ticket Information -->
        <div v-if="place.ticket_info" class="ticket-info">
          <div class="ticket-status" :class="{ 'requires-ticket': place.ticket_info.requires_ticket, 'free': !place.ticket_info.requires_ticket }">
            <span class="ticket-text">
              {{ place.ticket_info.requires_ticket ? 'Requires Ticket' : 'Free Entry' }}
            </span>
            <span v-if="place.ticket_info.ticket_price" class="ticket-price">
              {{ place.ticket_info.ticket_price }}
            </span>
          </div>
          
          <div v-if="place.ticket_info.booking_url" class="booking-section">
            <a 
              :href="place.ticket_info.booking_url" 
              target="_blank" 
              rel="noopener noreferrer"
              class="booking-link"
            >
              Book Tickets
            </a>
          </div>
          
          <div v-if="place.ticket_info.notes" class="ticket-notes">
            {{ place.ticket_info.notes }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  itinerary: {
    type: Object,
    required: true
  }
})

defineEmits(['play-audio'])

// Tab state
const selectedDay = ref(0)

/**
 * Select a specific day tab
 * @param {Number} index - Day index (0-based)
 */
const selectDay = (index) => {
  selectedDay.value = index
}

/**
 * Get current day's schedule
 */
const currentDaySchedule = computed(() => {
  if (!props.itinerary.schedule || props.itinerary.schedule.length === 0) {
    return null
  }
  return props.itinerary.schedule[selectedDay.value]
})
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
  margin-bottom: 1.5rem;
  font-size: 1.15rem;
}

/* Day Tabs Navigation */
.day-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #E5E7EB;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none; /* Firefox */
}

.day-tabs::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}

.day-tab {
  flex: 1;
  min-width: 80px;
  padding: 1rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  color: #6B7280;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  touch-action: manipulation;
  -webkit-tap-highlight-color: rgba(16, 163, 127, 0.2);
}

.day-tab:hover {
  color: #10A37F;
  background: rgba(16, 163, 127, 0.05);
}

.day-tab.active {
  color: #10A37F;
  border-bottom-color: #10A37F;
  background: rgba(16, 163, 127, 0.08);
}

/* Day Content */
.day-content {
  animation: fadeInTab 0.3s ease-out;
}

@keyframes fadeInTab {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.day-title {
  color: #10A37F;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid #E5E5E5;
}

/* Mobile-optimized tabs */
@media (max-width: 768px) {
  .day-tabs {
    gap: 0.3rem;
    margin-bottom: 1rem;
  }
  
  .day-tab {
    min-width: 70px;
    padding: 0.9rem 1rem;
    font-size: 0.95rem;
    flex: 0 0 auto; /* Don't stretch on mobile */
  }
  
  .itinerary-container h2 {
    font-size: 1.5rem;
  }
  
  .duration {
    font-size: 1rem;
  }
}

.place-card {
  background: #FAFAFA;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  border: 1px solid #E5E5E5;
  transition: all 0.15s;
  animation: fadeInCard 0.4s ease-out;
}

@keyframes fadeInCard {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.place-card:hover {
  border-color: #10A37F;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* Mobile-optimized place cards */
@media (max-width: 768px) {
  .place-card {
    padding: 1.2rem;
    margin-bottom: 1rem;
  }
}

.place-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  gap: 1rem;
}

.place-name {
  color: #202123;
  font-size: 1.35rem;
  font-weight: 600;
  flex: 1;
  line-height: 1.3;
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
  white-space: nowrap;
  touch-action: manipulation;
  -webkit-tap-highlight-color: rgba(16, 163, 127, 0.3);
}

.audio-button:hover {
  background: #0E8C6D;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(16, 163, 127, 0.2);
}

.audio-button:active {
  transform: translateY(0);
}

/* Mobile-optimized place header */
@media (max-width: 768px) {
  .place-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
  
  .place-name {
    font-size: 1.2rem;
  }
  
  .audio-button {
    width: 100%;
    padding: 0.9rem 1.2rem;
    font-size: 0.9rem;
    min-height: 44px; /* Good touch target */
  }
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

/* Ticket Information Styles */
.ticket-info {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #e9ecef;
}

.ticket-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.ticket-status.requires-ticket {
  color: #dc3545;
}

.ticket-status.free {
  color: #28a745;
}

.ticket-icon {
  font-size: 1.2rem;
}

.ticket-text {
  font-size: 0.9rem;
}

.ticket-price {
  font-size: 0.85rem;
  color: #6c757d;
  margin-left: auto;
}

.booking-section {
  margin-bottom: 0.75rem;
}

.booking-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.booking-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
  color: white;
  text-decoration: none;
}

.ticket-notes {
  font-size: 0.8rem;
  color: #6c757d;
  line-height: 1.4;
  font-style: italic;
}
</style>

