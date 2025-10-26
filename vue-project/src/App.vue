<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <div class="logo-section">
          <h1 class="main-title">
            <span class="title-trip">Trip</span><span class="title-teller">Teller</span>
          </h1>
          <div class="ai-badge">AI-Powered Travel Guide</div>
        </div>
        <div class="feature-tags">
          <span class="feature-tag">Smart Recommendations</span>
          <span class="feature-tag">Voice Narration</span>
          <span class="feature-tag">Route Planning</span>
        </div>
      </div>
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
          <span class="check-icon"></span>
          Location confirmed: <strong>{{ confirmedPlace.city }}</strong>
          <span v-if="confirmedPlace.state">, {{ confirmedPlace.state }}</span>
          <span>, {{ confirmedPlace.country }}</span>
        </p>
      </div>

      <!-- Weather and Events Information -->
      <WeatherInfo 
        v-if="weatherInfo || eventsInfo.length > 0"
        :weather="weatherInfo"
        :events="eventsInfo"
      />

      <div v-if="itinerary" class="content-grid">
        <div class="left-panel">
          <ItineraryDisplay :itinerary="itinerary" :weather-forecast="weatherForecast" @play-audio="handlePlayAudio" />
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
          <div class="toast-icon">♪</div>
          <div class="toast-content">
            <div class="toast-title">{{ audioNotification.title }}</div>
            <div class="toast-status">{{ audioNotification.status }}</div>
          </div>
          <button @click="stopAudio" class="toast-close">×</button>
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
import WeatherInfo from './components/WeatherInfo.vue'

const loading = ref(false)
const error = ref(null)
const currentCity = ref('')
const confirmedPlace = ref(null)
const itinerary = ref(null)
const posterImage = ref(null)
const weatherInfo = ref(null)
const weatherForecast = ref(null)
const eventsInfo = ref([])
const travelOptions = ref({
  days: 3,
  intensity: 'moderate',
  preferences: [],
  start_date: null
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
  weatherInfo.value = null
  weatherForecast.value = null
  eventsInfo.value = []

  try {
    // Fetch weather and events if date is selected
    if (travelOptions.value.start_date) {
      await fetchWeatherAndEvents(cityName, place, travelOptions.value.start_date)
    }

    // Fetch weather forecast for the itinerary days
    await fetchWeatherForecast(cityName, place, travelOptions.value.days)

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
        start_date: travelOptions.value.start_date,
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
 * Fetch weather forecast for multiple days
 */
const fetchWeatherForecast = async (city, place, days) => {
  try {
    const forecastResponse = await fetch(`${API_BASE_URL}/api/weather-forecast`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        city: city,
        lat: place.location?.lat,
        lon: place.location?.lng,
        days: days
      })
    })
    
    if (forecastResponse.ok) {
      const forecastData = await forecastResponse.json()
      weatherForecast.value = forecastData.forecast
    }
  } catch (err) {
    console.warn('Failed to fetch weather forecast:', err)
    // Don't fail the whole process if forecast fails
  }
}

/**
 * Fetch weather and events information for the travel date
 */
const fetchWeatherAndEvents = async (city, place, startDate) => {
  try {
    // Fetch weather information
    const weatherResponse = await fetch(`${API_BASE_URL}/api/weather`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        city: city,
        lat: place.location?.lat,
        lon: place.location?.lng,
        date: startDate
      })
    })
    
    if (weatherResponse.ok) {
      const weatherData = await weatherResponse.json()
      weatherInfo.value = weatherData.weather
    }
    
    // Fetch events information
    const eventsResponse = await fetch(`${API_BASE_URL}/api/events`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        city: city,
        country: place.country,
        date: startDate
      })
    })
    
    if (eventsResponse.ok) {
      const eventsData = await eventsResponse.json()
      eventsInfo.value = eventsData.events
    }
    
  } catch (err) {
    console.warn('Failed to fetch weather/events:', err)
    // Don't fail the whole process if weather/events fail
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
  background: linear-gradient(135deg, #06b6d4 0%, #10b981 100%);
  padding: 3rem 0;
  text-align: center;
  width: 100%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 0;
  position: relative;
  overflow: hidden;
}

/* Animated background effect */
.app-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: rotateGradient 20s linear infinite;
}

@keyframes rotateGradient {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

.logo-section {
  margin-bottom: 1.5rem;
  animation: fadeInDown 0.8s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.main-title {
  font-size: 4rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -2px;
  line-height: 1;
}

.title-trip {
  color: white;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  display: inline-block;
  animation: slideInLeft 0.6s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.title-teller {
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none;
  display: inline-block;
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.ai-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-top: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  letter-spacing: 0.5px;
  text-transform: uppercase;
  animation: fadeIn 1s ease-out 0.3s both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.feature-tags {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  animation: fadeInUp 0.8s ease-out 0.5s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-tag {
  background: rgba(255, 255, 255, 0.95);
  color: #0891b2;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.feature-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: white;
  color: #0e7490;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  animation: fadeInContent 0.6s ease-out 0.8s both;
}

@keyframes fadeInContent {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  animation: slideInNotification 0.4s ease-out;
}

@keyframes slideInNotification {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
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
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 0.5rem;
  flex-shrink: 0;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.7;
  }
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
  animation: fadeInPanel 0.5s ease-out;
}

@keyframes fadeInPanel {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.left-panel {
  animation-delay: 0.1s;
}

.right-panel {
  animation-delay: 0.2s;
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

  .main-title {
    font-size: 2.5rem;
  }
  
  .app-header {
    padding: 2rem 0;
  }
  
  .header-content {
    padding: 0 1.5rem;
  }
  
  .app-main {
    padding: 1.5rem;
  }
  
  .feature-tags {
    gap: 0.6rem;
  }
  
  .feature-tag {
    font-size: 0.85rem;
    padding: 0.5rem 1rem;
  }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
    letter-spacing: -1px;
  }
  
  .ai-badge {
    font-size: 0.75rem;
    padding: 0.4rem 1.2rem;
  }
  
  .feature-tag {
    font-size: 0.8rem;
    padding: 0.5rem 0.9rem;
  }
  
  .header-content {
    padding: 0 1rem;
  }
  
  .app-main {
    padding: 1rem;
  }
}
</style>
