<template>
  <div id="app">
    <header class="app-header">
      <h1>TripTeller - AI Travel Guide</h1>
      <p class="subtitle">Smart Travel Recommendations · Voice Narration · Route Planning</p>
    </header>

    <main class="app-main">
      <CityInput 
        @confirm-place="handlePlaceConfirmed" 
        :loading="loading" 
        @options-change="handleOptionsChange" 
      />
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Show confirmed location info -->
      <div v-if="confirmedPlace" class="location-confirmed">
        <p class="confirmed-text">
          <span class="check-icon">✓</span>
          Location confirmed: <strong>{{ confirmedPlace.city }}</strong>
          <span v-if="confirmedPlace.state">, {{ confirmedPlace.state }}</span>
          <span>, {{ confirmedPlace.country }}</span>
        </p>
      </div>

      <div v-if="itinerary" class="content-grid">
        <div class="left-panel">
          <ItineraryDisplay :itinerary="itinerary" @play-audio="handlePlayAudio" />
        </div>
        
        <div class="right-panel">
          <MapView :places="itinerary.places" :city="currentCity" />
        </div>
      </div>

      <!-- Hidden audio player for direct playback -->
      <audio 
        ref="audioPlayer"
        @ended="isPlayingAudio = false"
        @pause="isPlayingAudio = false"
        @play="isPlayingAudio = true"
        style="display: none;"
      >
        Your browser does not support audio playback
      </audio>

      <!-- Audio notification toast -->
      <transition name="toast-fade">
        <div v-if="audioNotification" class="audio-toast">
          <div class="toast-icon">🔊</div>
          <div class="toast-content">
            <div class="toast-title">{{ audioNotification.title }}</div>
            <div class="toast-status">{{ audioNotification.status }}</div>
          </div>
          <button @click="stopAudio" class="toast-close">✕</button>
        </div>
      </transition>

      <div v-if="posterImage" class="poster-section">
        <h3>Destination Poster</h3>
        <img :src="posterImage" alt="Destination Poster" class="poster-image" />
      </div>

      <!-- Travel Tips at bottom -->
      <TravelTips v-if="itinerary && itinerary.tips" :tips="itinerary.tips" />
    </main>

    <footer class="app-footer">
      <p>Powered by Cerebras AI · Google Maps · ElevenLabs</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import CityInput from './components/CityInput.vue'
import ItineraryDisplay from './components/ItineraryDisplay.vue'
import MapView from './components/MapView.vue'
import AudioPlayer from './components/AudioPlayer.vue'
import TravelTips from './components/TravelTips.vue'

const loading = ref(false)
const error = ref(null)
const currentCity = ref('')
const confirmedPlace = ref(null)
const itinerary = ref(null)
const posterImage = ref(null)
const travelOptions = ref({
  days: 3,
  intensity: 'moderate',
  preferences: []
})

// Audio player refs and state
const audioPlayer = ref(null)
const isPlayingAudio = ref(false)
const audioNotification = ref(null)
let audioNotificationTimer = null

// Use environment variable or empty string for same-origin (proxied) requests
// Empty string = relative URLs (e.g., "/api/...") which will be proxied by Vite dev server
const API_BASE_URL = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : 'http://localhost:5000'

const handleOptionsChange = (options) => {
  travelOptions.value = options
  console.log('Travel options updated:', options)
}

/**
 * Handle place confirmation from CityInput component
 * This is called after the user selects a specific location from the search results
 * @param {Object} place - The confirmed place object with city, state, country, location data
 */
const handlePlaceConfirmed = async (place) => {
  console.log('Place confirmed:', place)
  confirmedPlace.value = place
  
  // Generate itinerary for the confirmed place
  await generateItinerary(place)
}

/**
 * Generate itinerary for the confirmed place
 * @param {Object} place - The place object containing location details
 */
const generateItinerary = async (place) => {
  loading.value = true
  error.value = null
  
  // Use city name from confirmed place, or fall back to formatted address
  const cityName = place.city || place.formatted_address
  currentCity.value = cityName
  itinerary.value = null
  posterImage.value = null

  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-itinerary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        city: cityName,
        days: travelOptions.value.days,
        intensity: travelOptions.value.intensity,
        preferences: travelOptions.value.preferences,
        // Include additional location context for better AI results
        location_context: {
          state: place.state,
          country: place.country,
          country_code: place.country_code,
          formatted_address: place.formatted_address,
          coordinates: place.location
        }
      })
    })
    

    if (!response.ok) {
      throw new Error('Failed to generate itinerary')
    }

    const data = await response.json()
    itinerary.value = data.itinerary

    // Optional: Generate poster
    if (data.poster_url) {
      posterImage.value = data.poster_url
    }
  } catch (err) {
    error.value = err.message || 'An error occurred, please try again'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

/**
 * Handle play audio button click
 * Directly plays audio without modal popup
 * @param {Object} place - Place object with name and description
 */
const handlePlayAudio = async (place) => {
  try {
    // Show loading notification
    showAudioNotification(place.name, 'Generating audio...')
    
    const response = await fetch(`${API_BASE_URL}/api/generate-audio`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        place_name: place.name,
        description: place.description 
      })
    })

    if (!response.ok) {
      throw new Error('Failed to generate audio')
    }

    const data = await response.json()
    
    // Update notification
    showAudioNotification(place.name, 'Playing...')
    
    // Set audio source and play
    if (audioPlayer.value) {
      const audioUrl = data.audio_url
      // If relative URL, prepend API_BASE_URL
      const fullAudioUrl = audioUrl.startsWith('http') ? audioUrl : `${API_BASE_URL}${audioUrl}`
      
      audioPlayer.value.src = fullAudioUrl
      audioPlayer.value.volume = 0.7
      
      // Play audio
      await audioPlayer.value.play()
      
      console.log('✅ Audio playing:', place.name)
    }
  } catch (err) {
    showAudioNotification(place.name, 'Failed to play audio', true)
    console.error('Audio error:', err)
    
    // Auto-hide error notification after 3 seconds
    setTimeout(() => {
      audioNotification.value = null
    }, 3000)
  }
}

/**
 * Show audio notification toast
 * @param {String} title - Place name
 * @param {String} status - Status message
 * @param {Boolean} isError - Whether this is an error notification
 */
const showAudioNotification = (title, status, isError = false) => {
  // Clear existing timer
  if (audioNotificationTimer) {
    clearTimeout(audioNotificationTimer)
  }
  
  audioNotification.value = {
    title,
    status,
    isError
  }
  
  // Auto-hide notification after 5 seconds (unless it's generating or playing)
  if (status !== 'Playing...' && status !== 'Generating audio...') {
    audioNotificationTimer = setTimeout(() => {
      audioNotification.value = null
    }, 5000)
  }
}

/**
 * Stop currently playing audio
 */
const stopAudio = () => {
  if (audioPlayer.value) {
    audioPlayer.value.pause()
    audioPlayer.value.currentTime = 0
  }
  audioNotification.value = null
  isPlayingAudio.value = false
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
  background: #F7F7F8;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: transparent;
  padding: 2rem;
  padding-bottom: 0;
  text-align: center;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.app-header h1 {
  background: white;
  padding: 2.5rem 3rem;
  border-radius: 12px;
  border: 1px solid #E5E5E5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  font-size: 3rem;
  color: #202123;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.subtitle {
  background: white;
  padding: 1.5rem 3rem;
  border-radius: 12px;
  border: 1px solid #E5E5E5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  color: #6E6E80;
  font-size: 1.3rem;
  margin-top: 1rem;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.error-message {
  background: #FEF2F2;
  color: #991B1B;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
  border: 1px solid #FECACA;
}

.location-confirmed {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin: 1rem 0;
}

.confirmed-text {
  color: #065F46;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.check-icon {
  background: #10B981;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.left-panel, .right-panel {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  border: 1px solid #E5E5E5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.poster-section {
  margin-top: 2rem;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.poster-section h3 {
  margin-bottom: 1rem;
  color: #333;
}

.poster-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.app-footer {
  background: transparent;
  color: #6E6E80;
  text-align: center;
  padding: 1.5rem;
  margin-top: 2rem;
  font-size: 0.9rem;
}

/* Audio Toast Notification */
.audio-toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: white;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 3000;
  min-width: 300px;
  border: 2px solid #10A37F;
}

.toast-icon {
  font-size: 1.8rem;
  flex-shrink: 0;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-weight: 600;
  color: #202123;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.toast-status {
  color: #10A37F;
  font-size: 0.9rem;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.3rem;
  color: #9CA3AF;
  cursor: pointer;
  padding: 0.25rem;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background: #F3F4F6;
  color: #202123;
}

/* Toast animation */
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: all 0.3s ease;
}

.toast-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Mobile positioning */
@media (max-width: 768px) {
  .audio-toast {
    bottom: 1rem;
    right: 1rem;
    left: 1rem;
    min-width: auto;
  }
}

@media (max-width: 968px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .app-header h1 {
    font-size: 1.8rem;
  }
}
</style>
