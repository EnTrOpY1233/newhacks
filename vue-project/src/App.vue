<template>
  <div id="app">
    <header class="app-header">
      <h1>TripTeller - AI Travel Guide</h1>
      <p class="subtitle">Smart Travel Recommendations · Voice Narration · Route Planning</p>
    </header>

    <main class="app-main">
      <CityInput @search="handleCitySearch" :loading="loading" @options-change="handleOptionsChange" />
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="itinerary" class="content-grid">
        <div class="left-panel">
          <ItineraryDisplay :itinerary="itinerary" @play-audio="handlePlayAudio" />
        </div>
        
        <div class="right-panel">
          <MapView :places="itinerary.places" :city="currentCity" />
        </div>
      </div>

      <AudioPlayer 
        v-if="currentAudio" 
        :audio-url="currentAudio.url" 
        :title="currentAudio.title" 
        @close="currentAudio = null"
      />

      <div v-if="posterImage" class="poster-section">
        <h3>Destination Poster</h3>
        <img :src="posterImage" alt="Destination Poster" class="poster-image" />
      </div>
    </main>

    <footer class="app-footer">
      <p>Powered by Gemini AI · Google Maps · ElevenLabs</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CityInput from './components/CityInput.vue'
import ItineraryDisplay from './components/ItineraryDisplay.vue'
import MapView from './components/MapView.vue'
import AudioPlayer from './components/AudioPlayer.vue'

const loading = ref(false)
const error = ref(null)
const currentCity = ref('')
const itinerary = ref(null)
const currentAudio = ref(null)
const posterImage = ref(null)
const travelOptions = ref({
  days: 3,
  intensity: 'moderate'
})

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const handleOptionsChange = (options) => {
  travelOptions.value = options
}

const handleCitySearch = async (city) => {
  loading.value = true
  error.value = null
  currentCity.value = city
  itinerary.value = null
  posterImage.value = null

  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-itinerary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        city, 
        days: travelOptions.value.days,
        intensity: travelOptions.value.intensity
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

const handlePlayAudio = async (place) => {
  try {
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
    currentAudio.value = {
      url: data.audio_url,
      title: place.name
    }
  } catch (err) {
    error.value = err.message || 'Audio generation failed'
    console.error('Audio error:', err)
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  border-left: 4px solid #c33;
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
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
  background: rgba(0, 0, 0, 0.2);
  color: white;
  text-align: center;
  padding: 1.5rem;
  margin-top: 2rem;
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
