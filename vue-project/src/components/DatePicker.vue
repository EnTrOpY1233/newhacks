<template>
  <div class="date-picker-container">
    <label class="date-label">
      <span class="label-icon">📅</span>
      <span class="label-text">Travel Start Date (Optional)</span>
    </label>
    <input 
      type="date" 
      v-model="selectedDate"
      @change="handleDateChange"
      :min="minDate"
      class="date-input"
      placeholder="Select start date"
    />
    <p v-if="selectedDate" class="date-info">
      Selected: {{ formatDate(selectedDate) }}
    </p>
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
  margin: 1rem 0;
}

.date-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: #202123;
  margin-bottom: 0.5rem;
}

.label-icon {
  font-size: 1.2rem;
}

.label-text {
  color: #6E6E80;
}

.date-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #E5E5E5;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.15s;
  background: white;
}

.date-input:hover {
  border-color: #10A37F;
}

.date-input:focus {
  outline: none;
  border-color: #10A37F;
  box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1);
}

.date-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #10A37F;
  font-weight: 500;
}
</style>
