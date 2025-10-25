<template>
  <div class="city-input-container">
    <!-- Google Maps API Loader -->
    <gmpx-api-loader 
      :key="apiKey" 
      solution-channel="GMP_GE_placepicker_v2"
    ></gmpx-api-loader>

    <div class="input-wrapper">
      <!-- Google Place Picker Component -->
      <div class="place-picker-wrapper">
        <gmpx-place-picker 
          ref="placePicker"
          placeholder="输入城市名称或地址（如：Toronto, Tokyo, Paris...）"
          @gmpx-placechange="handlePlaceChange"
        ></gmpx-place-picker>
      </div>
      
      <button 
        @click="handleSearch" 
        :disabled="loading || !cityName.trim()"
        class="search-button"
      >
        <span v-if="!loading">🔍 搜索</span>
        <span v-else>⏳ 生成中...</span>
      </button>
    </div>
    
    <div class="quick-cities">
      <span class="label">热门城市：</span>
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

const emit = defineEmits(['search'])

const placePicker = ref(null)
const cityName = ref('')
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
const popularCities = ['Tokyo', 'Paris', 'Toronto', 'New York', 'London', 'Barcelona', 'Dubai', 'Singapore']

// 处理地点选择变化
const handlePlaceChange = (event) => {
  const place = event.detail.place
  
  if (place) {
    // 尝试从地点中提取城市名
    let city = ''
    
    // 优先使用 locality (城市名)
    const localityComponent = place.address_components?.find(
      component => component.types.includes('locality')
    )
    
    if (localityComponent) {
      city = localityComponent.long_name
    } else {
      // 如果没有 locality，尝试使用 administrative_area_level_1 (州/省)
      const adminComponent = place.address_components?.find(
        component => component.types.includes('administrative_area_level_1')
      )
      city = adminComponent?.long_name || place.name || place.formatted_address
    }
    
    cityName.value = city
    console.log('Selected place:', place)
    console.log('Extracted city:', city)
  }
}

const handleSearch = () => {
  if (cityName.value.trim()) {
    emit('search', cityName.value.trim())
  }
}

const selectCity = (city) => {
  cityName.value = city
  // 更新 place picker 的值
  if (placePicker.value) {
    placePicker.value.value = city
  }
  handleSearch()
}

onMounted(() => {
  if (!apiKey) {
    console.warn('Google Maps API Key 未配置，Place Picker 可能无法正常工作')
  }
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

.place-picker-wrapper {
  flex: 1;
  display: flex;
}

/* 自定义 Google Place Picker 样式 */
.place-picker-wrapper gmpx-place-picker {
  width: 100%;
  --gmpx-color-surface: #ffffff;
  --gmpx-color-on-surface: #333333;
  --gmpx-color-primary: #667eea;
  --gmpx-font-family-base: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  --gmpx-font-size-base: 1.1rem;
}

.place-picker-wrapper gmpx-place-picker::part(input) {
  padding: 1rem 1.5rem;
  font-size: 1.1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s;
}

.place-picker-wrapper gmpx-place-picker::part(input):focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-button {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-weight: 600;
  white-space: nowrap;
}

.search-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
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
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.city-tag:disabled {
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

