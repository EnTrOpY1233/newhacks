<template>
  <div v-if="tips && tips.length > 0" class="tips-container">
    <h3>Travel Tips</h3>
    <ul class="tips-list">
      <li v-for="(tip, index) in tips" :key="index">{{ tip }}</li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  tips: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.tips-container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #E5E5E5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-top: 2rem;
}

.tips-container h3 {
  color: #202123;
  margin-bottom: 1.2rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.tips-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.tips-list li {
  padding: 1rem;
  padding-left: 2.5rem;
  position: relative;
  color: #374151;
  font-size: 1rem;
  line-height: 1.6;
  background: #F7F7F8;
  border-radius: 8px;
  border: 1px solid #E5E5E5;
}

.tips-list li::before {
  content: "•";
  position: absolute;
  left: 1rem;
  color: #10A37F;
  font-weight: bold;
  font-size: 1.2rem;
}
</style>





