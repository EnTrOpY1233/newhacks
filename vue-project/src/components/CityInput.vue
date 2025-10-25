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
          v-model="cityName"
          type="text"
          placeholder="Enter city name (e.g. Toronto, Tokyo, Paris...)"
          @keyup.enter="handleSearch"
          @focus="showPlacePicker = true"
          @input="onInputChange"
          :disabled="loading"
          class="city-input"
        />
        
        <!-- Hidden Place Picker for autocomplete functionality -->
        <div v-show="showPlacePicker && cityName.length > 0" class="place-picker-dropdown">
          <gmpx-place-picker 
            ref="placePicker"
            :placeholder="cityName"
            @gmpx-placechange="handlePlaceChange"
          ></gmpx-place-picker>
        </div>
      </div>
      
      <button 
        @click="handleSearch" 
        :disabled="loading || !cityName.trim()"
        class="search-button"
      >
        <span v-if="!loading">Search</span>
        <span v-else>Generating...</span>
      </button>
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
        <div class="option-group">
          <label class="option-label">Travel Duration:</label>
          <div class="option-buttons">
            <button 
              v-for="day in [1, 3, 5, 7]" 
              :key="day"
              @click="selectDays(day)"
              :class="['option-btn', { active: selectedDays === day }]"
              :disabled="loading"
            >
              {{ day }} {{ day === 1 ? 'Day' : 'Days' }}
            </button>
          </div>
        </div>

        <div class="option-group">
          <label class="option-label">Travel Intensity:</label>
          <div class="option-buttons">
            <button 
              v-for="intensity in intensityOptions" 
              :key="intensity.value"
              @click="selectIntensity(intensity.value)"
              :class="['option-btn', { active: selectedIntensity === intensity.value }]"
              :disabled="loading"
            >
              {{ intensity.label }}
            </button>
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
import { ref, onMounted } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['search', 'options-change'])

const placePicker = ref(null)
const cityName = ref('')
const showPlacePicker = ref(false)
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
const popularCities = ['Tokyo', 'Paris', 'Toronto', 'New York', 'London', 'Barcelona', 'Dubai', 'Singapore']

// Travel options
const selectedDays = ref(3)
const selectedIntensity = ref('moderate')
const selectedPreferences = ref([])

const intensityOptions = [
  { value: 'relaxed', label: 'Relaxed' },
  { value: 'moderate', label: 'Moderate' },
  { value: 'intensive', label: 'Intensive' }
]

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

const selectDays = (days) => {
  selectedDays.value = days
  emitOptions()
}

const selectIntensity = (intensity) => {
  selectedIntensity.value = intensity
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

// Handle input change
const onInputChange = () => {
  showPlacePicker.value = cityName.value.length > 0
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

const handleSearch = () => {
  if (cityName.value.trim()) {
    showPlacePicker.value = false
    emit('search', cityName.value.trim())
  }
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
}

.search-button:hover:not(:disabled) {
  background: #0E8C6D;
  box-shadow: 0 2px 8px rgba(16, 163, 127, 0.2);
}

.search-button:active:not(:disabled) {
  transform: translateY(0);
}

.search-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
}

.city-tag:hover:not(:disabled) {
  background: #10A37F;
  color: white;
  border-color: #10A37F;
}

.city-tag:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
  margin-bottom: 0.8rem;
  font-size: 1.05rem;
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
}

.option-btn:hover:not(:disabled) {
  border-color: #10A37F;
  background: #F7F7F8;
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
}
</style>

