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

    <!-- Travel Options -->
    <div class="travel-options">
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
const intensityOptions = [
  { value: 'relaxed', label: 'Relaxed' },
  { value: 'moderate', label: 'Moderate' },
  { value: 'intensive', label: 'Intensive' }
]

const selectDays = (days) => {
  selectedDays.value = days
  emitOptions()
}

const selectIntensity = (intensity) => {
  selectedIntensity.value = intensity
  emitOptions()
}

const emitOptions = () => {
  emit('options-change', {
    days: selectedDays.value,
    intensity: selectedIntensity.value
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
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.input-wrapper {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: stretch;
}

.input-group {
  flex: 1;
  position: relative;
}

.city-input {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s;
}

.city-input:focus {
  outline: none;
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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
  --gmpx-color-on-surface: #333333;
  --gmpx-color-primary: #3B82F6;
  --gmpx-font-family-base: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  --gmpx-font-size-base: 1rem;
}

.search-button {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 600;
  white-space: nowrap;
}

.search-button:hover:not(:disabled) {
  background: #2563EB;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
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
  gap: 0.5rem;
  align-items: center;
}

.label {
  color: #666;
  font-weight: 600;
  margin-right: 0.5rem;
}

.city-tag {
  padding: 0.5rem 1rem;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.city-tag:hover:not(:disabled) {
  background: #3B82F6;
  color: white;
  border-color: #3B82F6;
}

.city-tag:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Travel Options */
.travel-options {
  margin: 1.5rem 0;
  padding: 1.5rem;
  background: #F8FAFC;
  border-radius: 8px;
  border: 1px solid #E2E8F0;
}

.option-group {
  margin-bottom: 1rem;
}

.option-group:last-child {
  margin-bottom: 0;
}

.option-label {
  display: block;
  font-weight: 600;
  color: #334155;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.option-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.option-btn {
  padding: 0.6rem 1.2rem;
  background: white;
  border: 2px solid #E2E8F0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  font-weight: 500;
  color: #64748B;
}

.option-btn:hover:not(:disabled) {
  border-color: #3B82F6;
  color: #3B82F6;
  background: #EFF6FF;
}

.option-btn.active {
  background: #3B82F6;
  color: white;
  border-color: #3B82F6;
}

.option-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .input-wrapper {
    flex-direction: column;
  }
  
  .search-button {
    width: 100%;
  }
}
</style>

