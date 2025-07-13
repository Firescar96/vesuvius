<template>
  <Input class="bg-transparent text-white" :value="value" @input="e => $emit('update:modelValue', e.target.value)" />
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { Input } from 'ant-design-vue'

defineProps({
  value: String,
})
</script>

<style lang="scss" scoped>
  input::placeholder {
    @apply text-stone-400;
  }
</style>