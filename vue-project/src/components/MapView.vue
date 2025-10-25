<template>
  <div class="map-container">
    <h2>🗺️ Route Map</h2>
    <div ref="mapElement" class="map" :class="{ 'map-loading': !mapLoaded }">
      <div v-if="!mapLoaded" class="loading-overlay">
        <p>Loading map...</p>
      </div>
    </div>
    
    <div v-if="error" class="map-error">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  places: {
    type: Array,
    default: () => []
  },
  city: {
    type: String,
    default: ''
  }
})

const mapElement = ref(null)
const mapLoaded = ref(false)
const error = ref(null)
let map = null
let markers = []

const loadGoogleMaps = () => {
  return new Promise((resolve, reject) => {
    if (window.google && window.google.maps) {
      resolve()
      return
    }

    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
    
    if (!apiKey) {
      error.value = 'Please configure VITE_GOOGLE_MAPS_API_KEY in .env file'
      reject(new Error('Missing API key'))
      return
    }

    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`
    script.async = true
    script.defer = true
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

const initMap = async () => {
  try {
    await loadGoogleMaps()
    
    const defaultCenter = { lat: 43.6532, lng: -79.3832 } // Toronto default
    
    map = new window.google.maps.Map(mapElement.value, {
      center: defaultCenter,
      zoom: 12,
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'on' }]
        }
      ]
    })
    
    mapLoaded.value = true
    
    if (props.places && props.places.length > 0) {
      addMarkers()
    }
  } catch (err) {
    console.error('Failed to load Google Maps:', err)
    error.value = 'Failed to load map, please check API key'
  }
}

const addMarkers = async () => {
  if (!map || !props.places.length) return

  // Clear old markers
  markers.forEach(marker => marker.setMap(null))
  markers = []

  const bounds = new window.google.maps.LatLngBounds()
  const geocoder = new window.google.maps.Geocoder()

  for (let i = 0; i < props.places.length; i++) {
    const place = props.places[i]
    
    try {
      const result = await geocoder.geocode({ 
        address: `${place.name}, ${props.city}` 
      })
      
      if (result.results[0]) {
        const position = result.results[0].geometry.location
        
        const marker = new window.google.maps.Marker({
          position: position,
          map: map,
          title: place.name,
          label: {
            text: String(i + 1),
            color: 'white',
            fontWeight: 'bold'
          },
          animation: window.google.maps.Animation.DROP
        })

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="padding: 10px;">
              <h3 style="margin: 0 0 8px 0; color: #333;">${place.name}</h3>
              <p style="margin: 0; color: #666;">${place.description || ''}</p>
            </div>
          `
        })

        marker.addListener('click', () => {
          infoWindow.open(map, marker)
        })

        markers.push(marker)
        bounds.extend(position)
      }
    } catch (err) {
      console.error(`Failed to geocode ${place.name}:`, err)
    }
  }

  if (markers.length > 0) {
    map.fitBounds(bounds)
  }
}

onMounted(() => {
  initMap()
})

watch(() => props.places, () => {
  if (map && props.places.length > 0) {
    addMarkers()
  }
}, { deep: true })
</script>

<style scoped>
.map-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.map-container h2 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.map {
  flex: 1;
  min-height: 500px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  background: #e0e0e0;
}

.map-loading {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #666;
  font-size: 1.1rem;
}

.map-error {
  margin-top: 1rem;
  padding: 1rem;
  background: #fee;
  color: #c33;
  border-radius: 6px;
  border-left: 4px solid #c33;
}
</style>

