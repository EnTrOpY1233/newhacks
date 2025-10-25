<template>
  <div class="map-container">
    <h2>Route Map</h2>
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
let currentInfoWindow = null  // Track currently open InfoWindow

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
  if (!map || !props.places.length) {
    console.log('No map or places:', { map: !!map, placesLength: props.places.length })
    return
  }

  console.log(`Adding ${props.places.length} markers for ${props.city}`)

  // Clear old markers
  markers.forEach(marker => marker.setMap(null))
  markers = []
  
  // Close any open InfoWindow
  if (currentInfoWindow) {
    currentInfoWindow.close()
    currentInfoWindow = null
  }

  const bounds = new window.google.maps.LatLngBounds()
  const geocoder = new window.google.maps.Geocoder()

  for (let i = 0; i < props.places.length; i++) {
    const place = props.places[i]
    
    try {
      const searchAddress = `${place.name}, ${props.city}`
      console.log(`Geocoding: ${searchAddress}`)
      
      const result = await geocoder.geocode({ 
        address: searchAddress
      })
      
      if (result.results[0]) {
        const position = result.results[0].geometry.location
        console.log(`✅ Found: ${place.name} at`, position.toJSON())
        
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

        // Create compact description (first 120 characters)
        const shortDesc = place.description 
          ? (place.description.length > 120 
              ? place.description.substring(0, 120) + '...' 
              : place.description)
          : '';

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="padding: 8px 12px; max-width: 280px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
              <h3 style="margin: 0 0 6px 0; color: #202123; font-size: 16px; font-weight: 600; line-height: 1.3;">${place.name}</h3>
              <p style="margin: 0; color: #565869; font-size: 14px; line-height: 1.5;">${shortDesc}</p>
              ${place.duration ? `<p style="margin: 6px 0 0 0; color: #6E6E80; font-size: 12px;">Duration: ${place.duration}</p>` : ''}
            </div>
          `,
          maxWidth: 280
        })

        marker.addListener('click', () => {
          // Close previously opened InfoWindow
          if (currentInfoWindow) {
            currentInfoWindow.close()
          }
          // Open new InfoWindow and track it
          infoWindow.open(map, marker)
          currentInfoWindow = infoWindow
        })

        markers.push(marker)
        bounds.extend(position)
      }
    } catch (err) {
      console.error(`❌ Failed to geocode ${place.name}:`, err)
    }
  }

  if (markers.length > 0) {
    console.log(`Fitting bounds for ${markers.length} markers`)
    map.fitBounds(bounds)
    // Add a small delay and zoom out a bit for better view
    setTimeout(() => {
      const currentZoom = map.getZoom()
      if (currentZoom > 15) {
        map.setZoom(13)
      }
    }, 500)
  } else {
    console.warn('No markers were added to the map')
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
  color: #202123;
  margin-bottom: 1.2rem;
  font-size: 2rem;
  font-weight: 700;
}

.map {
  flex: 1;
  min-height: 500px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  background: #E5E5E5;
  border: 1px solid #D1D5DB;
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
  color: #6E6E80;
  font-size: 1rem;
}

.map-error {
  margin-top: 1rem;
  padding: 1rem 1.5rem;
  background: #FEF2F2;
  color: #991B1B;
  border-radius: 6px;
  border: 1px solid #FECACA;
}
</style>

