<template>
  <div class="date-picker-container">
    <div class="date-icon-button"
         :class="{ 'has-date': selectedDate }"
         :title="selectedDate ? formatDate(selectedDate) : 'Select travel date (Optional)'">
      <span class="date-icon">📅</span>
      <input 
        type="date" 
        ref="dateInput"
        v-model="selectedDate"
        @change="handleDateChange"
        :min="minDate"
        class="date-input-overlay"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: null
  },
  minDate: {
    type: Date,
    default: () => new Date()
  }
})

const emit = defineEmits(['update:modelValue', 'date-selected'])

const selectedDate = ref(props.modelValue)
const dateInput = ref(null)

const minDate = computed(() => {
  const date = props.minDate
  return date.toISOString().split('T')[0]
})

const handleDateChange = () => {
  emit('update:modelValue', selectedDate.value)
  emit('date-selected', selectedDate.value)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}
</script>

<style scoped>
.date-picker-container {
  margin: 0;
}

.date-icon-button {
  background: white;
  border: 2px solid #4CAF50;
  border-radius: 50%;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 48px;
  min-height: 48px;
  width: 48px;
  height: 48px;
  position: relative;
}

.date-icon-button:hover {
  background: #4CAF50;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.date-icon-button.has-date {
  background: #4CAF50;
  border-color: #4CAF50;
  color: white;
}

.date-icon-button.has-date:hover {
  background: #45a049;
  border-color: #45a049;
}

.date-icon {
  font-size: 1.5rem;
  display: block;
  pointer-events: none;
}

.date-icon-button.has-date .date-icon {
  filter: brightness(0) invert(1);
}

.date-input-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 10;
  padding: 0;
  border: none;
}
</style>
