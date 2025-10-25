<template>
  <div class="city-input-container">
    <!-- Google Maps API Loader -->
    <gmpx-api-loader 
      :key="apiKey" 
      solution-channel="GMP_GE_placepicker_v2"
    ></gmpx-api-loader>

    <div class="input-wrapper">
      <!-- Regular input with Place Picker hidden for auto-complete -->
      <div class="input-group">
        <input
          ref="cityInput"
          v-model="cityName"
          type="text"
          inputmode="text"
          autocomplete="off"
          autocapitalize="words"
          placeholder="Enter city name (e.g. Toronto, Tokyo, Paris...)"
          @keyup.enter="handleSearch"
          @focus="handleInputFocus"
          @blur="handleInputBlur"
          @input="onInputChange"
          @touchstart="handleTouchStart"
          :disabled="loading || searching"
          class="city-input"
        />
        
        <!-- Hidden Place Picker for autocomplete functionality (disabled on mobile) -->
        <div v-show="showPlacePicker && cityName.length > 0 && !isMobile" class="place-picker-dropdown">
          <gmpx-place-picker 
            ref="placePicker"
            :placeholder="cityName"
            @gmpx-placechange="handlePlaceChange"
          ></gmpx-place-picker>
        </div>
      </div>
      
      <button 
        @click="handleSearch" 
        @touchend.prevent="handleSearchTouch"
        :disabled="loading || searching || !cityName.trim()"
        class="search-button"
      >
        <span v-if="!loading && !searching">Search</span>
        <span v-else-if="searching">Searching...</span>
        <span v-else>Generating...</span>
      </button>
    </div>

    <!-- Place Confirmation Modal -->
    <div v-if="showConfirmModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Confirm Location</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        
        <div v-if="searchError" class="error-box">
          {{ searchError }}
        </div>

        <div v-else-if="foundPlaces.length === 0" class="no-results">
          <p>No locations found for "{{ searchQuery }}"</p>
          <p class="hint">Please try a different search term</p>
        </div>

        <div v-else class="places-list">
          <p class="instruction">
            We found {{ foundPlaces.length }} location{{ foundPlaces.length > 1 ? 's' : '' }} matching "{{ searchQuery }}". 
            Please select the correct one:
          </p>
          
          <div 
            v-for="(place, index) in foundPlaces" 
            :key="place.place_id"
            @click="confirmPlace(place)"
            class="place-item"
          >
            <div class="place-main">
              <div class="place-name">
                {{ place.city || 'Unknown City' }}
              </div>
              <div class="place-details">
                <span v-if="place.state" class="detail-item">{{ place.state }}</span>
                <span class="detail-item">{{ place.country }}</span>
                <span class="detail-item country-code">{{ place.country_code }}</span>
              </div>
            </div>
            <div class="place-address">
              {{ place.formatted_address }}
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal" class="btn-cancel">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Popular Cities - moved closer to search -->
    <div class="quick-cities">
      <span class="label">Popular Cities:</span>
      <button 
        v-for="city in popularCities" 
        :key="city"
        @click="selectCity(city)"
        :disabled="loading"
        class="city-tag"
      >
        {{ city }}
      </button>
    </div>

    <!-- Travel Options -->
    <div class="travel-options">
      <div class="options-grid">
        <!-- Travel Duration Slider -->
        <div class="option-group">
          <label class="option-label">
            Travel Duration: <span class="value-display">{{ selectedDays }} {{ selectedDays === 1 ? 'Day' : 'Days' }}</span>
          </label>
          <div class="slider-container">
            <input 
              type="range" 
              v-model.number="selectedDays"
              @input="onDaysChange"
              min="1" 
              max="14" 
              step="1"
              :disabled="loading"
              class="duration-slider"
            />
            <div class="slider-labels">
              <span>1 Day</span>
              <span>14 Days</span>
            </div>
          </div>
        </div>

        <!-- Travel Intensity Slider -->
        <div class="option-group">
          <label class="option-label">
            Travel Intensity: <span class="value-display">{{ currentIntensityLabel }}</span>
          </label>
          <div class="slider-container">
            <input 
              type="range" 
              v-model.number="intensitySliderValue"
              @input="onIntensityChange"
              min="0" 
              max="2" 
              step="1"
              :disabled="loading"
              class="intensity-slider"
            />
            <div class="slider-labels intensity-labels">
              <span>Relaxed</span>
              <span>Moderate</span>
              <span>Intensive</span>
            </div>
          </div>
        </div>
      </div>

      <div class="option-group preferences-group">
        <label class="option-label">Travel Preferences (select multiple):</label>
        <div class="option-buttons">
          <button 
            v-for="pref in preferenceOptions" 
            :key="pref.value"
            @click="togglePreference(pref.value)"
            :class="['option-btn', 'pref-btn', { active: selectedPreferences.includes(pref.value) }]"
            :disabled="loading"
          >
            {{ pref.emoji }} {{ pref.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['search', 'confirm-place', 'options-change'])

const placePicker = ref(null)
const cityInput = ref(null)
const cityName = ref('')
const showPlacePicker = ref(false)
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
const popularCities = ['Tokyo', 'Paris', 'Toronto', 'New York', 'London', 'Barcelona', 'Dubai', 'Shanghai']

// Mobile detection
const isMobile = ref(false)
const isTouch = ref(false)

// Place confirmation states
const searching = ref(false)
const showConfirmModal = ref(false)
const foundPlaces = ref([])
const searchQuery = ref('')
const searchError = ref(null)

// Travel options
const selectedDays = ref(3)
const selectedIntensity = ref('moderate')
const selectedPreferences = ref([])

// Intensity slider mapping
const intensitySliderValue = ref(1) // 0 = relaxed, 1 = moderate, 2 = intensive

const intensityOptions = [
  { value: 'relaxed', label: 'Relaxed' },
  { value: 'moderate', label: 'Moderate' },
  { value: 'intensive', label: 'Intensive' }
]

// Computed property for current intensity label
const currentIntensityLabel = computed(() => {
  const labels = ['Relaxed', 'Moderate', 'Intensive']
  return labels[intensitySliderValue.value] || 'Moderate'
})

const preferenceOptions = [
  { value: 'food', label: 'Food', emoji: '🍽️' },
  { value: 'historical', label: 'Historical', emoji: '🏛️' },
  { value: 'natural', label: 'Natural', emoji: '🌳' },
  { value: 'culture', label: 'Culture', emoji: '🎭' },
  { value: 'shopping', label: 'Shopping', emoji: '🛍️' },
  { value: 'adventure', label: 'Adventure', emoji: '🏔️' },
  { value: 'nightlife', label: 'Nightlife', emoji: '🌃' },
  { value: 'art', label: 'Art', emoji: '🎨' }
]

/**
 * Handle days slider change
 */
const onDaysChange = () => {
  emitOptions()
}

/**
 * Handle intensity slider change
 */
const onIntensityChange = () => {
  // Map slider value (0, 1, 2) to intensity string
  const intensityMap = ['relaxed', 'moderate', 'intensive']
  selectedIntensity.value = intensityMap[intensitySliderValue.value]
  emitOptions()
}

const selectDays = (days) => {
  selectedDays.value = days
  emitOptions()
}

const selectIntensity = (intensity) => {
  selectedIntensity.value = intensity
  // Update slider position
  const intensityMap = { 'relaxed': 0, 'moderate': 1, 'intensive': 2 }
  intensitySliderValue.value = intensityMap[intensity] || 1
  emitOptions()
}

const togglePreference = (pref) => {
  const index = selectedPreferences.value.indexOf(pref)
  if (index > -1) {
    selectedPreferences.value.splice(index, 1)
  } else {
    selectedPreferences.value.push(pref)
  }
  emitOptions()
}

const emitOptions = () => {
  emit('options-change', {
    days: selectedDays.value,
    intensity: selectedIntensity.value,
    preferences: selectedPreferences.value
  })
}

/**
 * Detect if device is mobile
 */
const detectMobile = () => {
  // Check screen width
  const isMobileWidth = window.innerWidth <= 768
  
  // Check user agent
  const isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  
  // Check touch support
  const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0
  
  isMobile.value = isMobileWidth || isMobileUA
  isTouch.value = hasTouch
  
  console.log('Mobile detection:', { isMobile: isMobile.value, isTouch: isTouch.value, width: window.innerWidth })
}

/**
 * Handle input focus
 */
const handleInputFocus = () => {
  if (!isMobile.value) {
    showPlacePicker.value = true
  }
}

/**
 * Handle input blur with delay for place picker interaction
 */
const handleInputBlur = () => {
  setTimeout(() => {
    if (!isMobile.value) {
      showPlacePicker.value = false
    }
  }, 200)
}

/**
 * Handle touch start on input
 */
const handleTouchStart = () => {
  // On mobile, ensure the input is focused properly
  if (isMobile.value && cityInput.value) {
    cityInput.value.focus()
  }
}

/**
 * Handle search button touch on mobile
 */
const handleSearchTouch = (e) => {
  if (isMobile.value) {
    e.preventDefault()
    handleSearch()
  }
}

// Handle input change
const onInputChange = () => {
  if (!isMobile.value) {
    showPlacePicker.value = cityName.value.length > 0
  }
}

// Handle place selection change from Place Picker
const handlePlaceChange = (event) => {
  const place = event.detail.place
  
  if (place) {
    // Try to extract city name from place
    let city = ''
    
    // Priority: use locality (city name)
    const localityComponent = place.address_components?.find(
      component => component.types.includes('locality')
    )
    
    if (localityComponent) {
      city = localityComponent.long_name
    } else {
      // If no locality, try administrative_area_level_1 (state/province)
      const adminComponent = place.address_components?.find(
        component => component.types.includes('administrative_area_level_1')
      )
      city = adminComponent?.long_name || place.name || place.formatted_address
    }
    
    cityName.value = city
    showPlacePicker.value = false
    console.log('Selected place:', place)
    console.log('Extracted city:', city)
  }
}

/**
 * Handle search button click
 * First validates the place exists before proceeding with itinerary generation
 */
const handleSearch = async () => {
  if (!cityName.value.trim()) return
  
  showPlacePicker.value = false
  searching.value = true
  searchError.value = null
  searchQuery.value = cityName.value.trim()

  try {
    // Call backend API to search for places
    // Use environment variable or empty string for same-origin (proxied) requests
    const API_BASE_URL = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : 'http://localhost:5000'
    const response = await fetch(`${API_BASE_URL}/api/search-places`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: searchQuery.value })
    })

    if (!response.ok) {
      throw new Error('Failed to search for places')
    }

    const data = await response.json()
    foundPlaces.value = data.places || []

    // If exactly one place found, auto-confirm it
    if (foundPlaces.value.length === 1) {
      confirmPlace(foundPlaces.value[0])
    } else {
      // Show modal for user to select from multiple places or handle no results
      showConfirmModal.value = true
    }
  } catch (error) {
    console.error('Error searching places:', error)
    searchError.value = 'Failed to search for location. Please try again.'
    showConfirmModal.value = true
  } finally {
    searching.value = false
  }
}

/**
 * Confirm the selected place and proceed with itinerary generation
 * @param {Object} place - The selected place object with city, state, country info
 */
const confirmPlace = (place) => {
  showConfirmModal.value = false
  
  // Update the city name input with the confirmed place
  cityName.value = place.city || place.formatted_address
  
  // Emit the confirmed place to parent component
  emit('confirm-place', place)
}

/**
 * Close the confirmation modal
 */
const closeModal = () => {
  showConfirmModal.value = false
  searchError.value = null
}

const selectCity = (city) => {
  cityName.value = city
  showPlacePicker.value = false
  // Don't auto-search, let user click the search button
  console.log('Selected city:', city)
}

onMounted(() => {
  if (!apiKey) {
    console.warn('Google Maps API Key not configured, Place Picker may not work properly')
  }
  
  // Detect mobile device
  detectMobile()
  
  // Re-detect on window resize
  window.addEventListener('resize', detectMobile)
  
  // Emit initial options
  emitOptions()
})
</script>

<style scoped>
.city-input-container {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  border: 1px solid #E5E5E5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.input-wrapper {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  align-items: stretch;
}

.input-group {
  flex: 1;
  position: relative;
}

.city-input {
  width: 100%;
  padding: 1.2rem 1.8rem;
  font-size: 1.1rem;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  transition: all 0.2s;
  background: white;
  color: #202123;
  -webkit-appearance: none;
  appearance: none;
}

.city-input:focus {
  outline: none;
  border-color: #10A37F;
  box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1);
}

.city-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Mobile-specific input styles */
@media (max-width: 768px) {
  .city-input {
    font-size: 16px; /* Prevent zoom on iOS */
    padding: 1rem 1.2rem;
    min-height: 48px; /* Minimum touch target */
  }
}

.place-picker-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 0.5rem;
  z-index: 1000;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-height: 300px;
  overflow-y: auto;
}

/* Custom Google Place Picker styles */
.place-picker-dropdown gmpx-place-picker {
  width: 100%;
  --gmpx-color-surface: #ffffff;
  --gmpx-color-on-surface: #202123;
  --gmpx-color-primary: #10A37F;
  --gmpx-font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --gmpx-font-size-base: 1rem;
}

.search-button {
  padding: 1.2rem 2.5rem;
  font-size: 1.1rem;
  background: #10A37F;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 600;
  white-space: nowrap;
  touch-action: manipulation; /* Disable double-tap zoom */
  -webkit-tap-highlight-color: rgba(16, 163, 127, 0.3);
}

.search-button:hover:not(:disabled) {
  background: #0E8C6D;
  box-shadow: 0 2px 8px rgba(16, 163, 127, 0.2);
}

.search-button:active:not(:disabled) {
  transform: translateY(0);
  background: #0D7A5E;
}

.search-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Mobile-specific button styles */
@media (max-width: 768px) {
  .search-button {
    padding: 1rem 2rem;
    font-size: 16px; /* Prevent zoom on iOS */
    min-height: 48px; /* Minimum touch target */
    min-width: 100px;
  }
}

.quick-cities {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #E5E5E5;
}

.label {
  color: #202123;
  font-weight: 600;
  margin-right: 0.8rem;
  font-size: 1.05rem;
}

.city-tag {
  padding: 0.7rem 1.3rem;
  background: #F7F7F8;
  border: 1.5px solid #D1D5DB;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.95rem;
  color: #202123;
  font-weight: 500;
  touch-action: manipulation;
  -webkit-tap-highlight-color: rgba(16, 163, 127, 0.2);
}

.city-tag:hover:not(:disabled) {
  background: #10A37F;
  color: white;
  border-color: #10A37F;
}

.city-tag:active:not(:disabled) {
  transform: scale(0.98);
}

.city-tag:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Mobile-specific city tag styles */
@media (max-width: 768px) {
  .city-tag {
    padding: 0.8rem 1.4rem;
    font-size: 14px;
    min-height: 40px; /* Good touch target */
  }
}

/* Travel Options */
.travel-options {
  margin: 2rem 0;
  padding: 2rem;
  background: #FAFAFA;
  border-radius: 10px;
  border: 1px solid #E5E5E5;
}

.options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.option-group {
  margin-bottom: 0;
}

.preferences-group {
  margin-top: 0;
}

.option-label {
  display: block;
  font-weight: 600;
  color: #202123;
  margin-bottom: 1.2rem;
  font-size: 1.05rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.value-display {
  color: #10A37F;
  font-weight: 700;
  font-size: 1.1rem;
}

/* Slider Container */
.slider-container {
  margin-top: 0.5rem;
}

/* Range Slider Styles */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: #E5E7EB;
  outline: none;
  opacity: 0.9;
  transition: opacity 0.2s;
  cursor: pointer;
  margin: 8px 0; /* Add vertical margin for better alignment */
}

input[type="range"]:hover {
  opacity: 1;
}

input[type="range"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Webkit browsers (Chrome, Safari, Edge) */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #10A37F;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
  margin-top: -8px; /* Center the thumb on the track */
  position: relative;
}

input[type="range"]::-webkit-slider-thumb:hover {
  background: #0E8C6D;
  transform: scale(1.1);
  box-shadow: 0 3px 6px rgba(16, 163, 127, 0.3);
}

input[type="range"]:active::-webkit-slider-thumb {
  transform: scale(1.2);
}

/* Firefox */
input[type="range"]::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #10A37F;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
  position: relative;
}

input[type="range"]::-moz-range-thumb:hover {
  background: #0E8C6D;
  transform: scale(1.1);
  box-shadow: 0 3px 6px rgba(16, 163, 127, 0.3);
}

input[type="range"]:active::-moz-range-thumb {
  transform: scale(1.2);
}

/* Track styling */
input[type="range"]::-webkit-slider-runnable-track {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: linear-gradient(to right, #10A37F 0%, #10A37F var(--value), #E5E7EB var(--value), #E5E7EB 100%);
}

input[type="range"]::-moz-range-track {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: #E5E7EB;
}

/* Duration slider - gradient from green */
.duration-slider {
  background: linear-gradient(to right, #10A37F 0%, #34D399 100%);
}

/* Intensity slider - gradient from blue to red */
.intensity-slider {
  background: linear-gradient(to right, #60A5FA 0%, #FBBF24 50%, #F87171 100%);
}

/* Slider Labels */
.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #6B7280;
}

.intensity-labels {
  justify-content: space-between;
}

.intensity-labels span {
  flex: 1;
  text-align: center;
}

.intensity-labels span:first-child {
  text-align: left;
}

.intensity-labels span:last-child {
  text-align: right;
}

.option-buttons {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.option-btn {
  padding: 0.8rem 1.5rem;
  background: white;
  border: 1.5px solid #D1D5DB;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.95rem;
  font-weight: 500;
  color: #202123;
  touch-action: manipulation;
  -webkit-tap-highlight-color: rgba(16, 163, 127, 0.2);
}

.option-btn:hover:not(:disabled) {
  border-color: #10A37F;
  background: #F7F7F8;
}

.option-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.option-btn.active {
  background: #10A37F;
  color: white;
  border-color: #10A37F;
}

.option-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pref-btn {
  min-width: 140px;
}

/* Mobile-specific option button styles */
@media (max-width: 768px) {
  .option-btn {
    padding: 0.9rem 1.3rem;
    font-size: 14px;
    min-height: 44px; /* Good touch target */
  }
  
  .pref-btn {
    min-width: 120px;
    flex: 1 1 calc(50% - 0.4rem); /* Two columns on mobile */
  }
}

/* Place Confirmation Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #E5E5E5;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #202123;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #6B7280;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #F3F4F6;
  color: #202123;
}

.error-box {
  padding: 1.5rem 2rem;
  background: #FEE2E2;
  color: #DC2626;
  border-left: 4px solid #DC2626;
  margin: 1.5rem 2rem;
  border-radius: 4px;
}

.no-results {
  padding: 3rem 2rem;
  text-align: center;
  color: #6B7280;
}

.no-results p {
  margin: 0.5rem 0;
}

.no-results .hint {
  font-size: 0.9rem;
  color: #9CA3AF;
}

.places-list {
  padding: 1.5rem 2rem;
}

.instruction {
  margin: 0 0 1.5rem 0;
  color: #4B5563;
  font-size: 0.95rem;
}

.place-item {
  padding: 1.25rem;
  border: 1.5px solid #E5E7EB;
  border-radius: 8px;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
  touch-action: manipulation;
  -webkit-tap-highlight-color: rgba(16, 163, 127, 0.1);
}

.place-item:hover {
  border-color: #10A37F;
  background: #F0FDF9;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(16, 163, 127, 0.1);
}

.place-item:active {
  background: #E6F9F4;
  transform: scale(0.99);
}

/* Mobile-specific place item styles */
@media (max-width: 768px) {
  .place-item {
    padding: 1.5rem 1.2rem;
    min-height: 80px; /* Good touch target for selections */
  }
  
  .place-item:hover {
    transform: none; /* Remove horizontal shift on touch devices */
  }
}

.place-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.place-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #202123;
  margin-bottom: 0.25rem;
}

.place-details {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.detail-item {
  font-size: 0.85rem;
  padding: 0.25rem 0.6rem;
  background: #F3F4F6;
  color: #4B5563;
  border-radius: 4px;
}

.country-code {
  background: #10A37F;
  color: white;
  font-weight: 600;
}

.place-address {
  font-size: 0.9rem;
  color: #6B7280;
  margin-top: 0.5rem;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #E5E5E5;
  display: flex;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: #F3F4F6;
  color: #202123;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #E5E7EB;
}

/* Mobile-specific slider styles */
@media (max-width: 768px) {
  input[type="range"]::-webkit-slider-thumb {
    width: 28px;
    height: 28px; /* Larger thumb for easier touch */
    margin-top: -9px; /* Center the larger thumb on mobile */
  }
  
  input[type="range"]::-moz-range-thumb {
    width: 28px;
    height: 28px;
  }
  
  input[type="range"] {
    height: 10px; /* Slightly taller track on mobile */
    margin: 10px 0; /* More margin on mobile for better spacing */
  }
  
  .slider-labels {
    font-size: 0.8rem;
  }
  
  .value-display {
    font-size: 1rem;
  }
}

@media (max-width: 968px) {
  .options-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .input-wrapper {
    flex-direction: column;
  }
  
  .search-button {
    width: 100%;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    max-width: 95vw;
  }

  .place-main {
    flex-direction: column;
  }

  .place-details {
    margin-top: 0.5rem;
  }
}
</style>

