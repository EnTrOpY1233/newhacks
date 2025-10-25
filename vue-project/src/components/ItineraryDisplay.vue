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
            {{ place.duration }}
          </span>
          <span v-if="place.category" class="detail-item category">
            {{ place.category }}
          </span>
        </div>
        
        <!-- Ticket Information -->
        <div v-if="place.ticket_info" class="ticket-info">
          <div class="ticket-status" :class="{ 'requires-ticket': place.ticket_info.requires_ticket, 'free': !place.ticket_info.requires_ticket }">
            <span class="ticket-icon">
              {{ place.ticket_info.requires_ticket ? '🎫' : '🆓' }}
            </span>
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
              🎟️ Book Tickets
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
const props = defineProps({
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

