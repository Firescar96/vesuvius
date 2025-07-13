<template>
  <InputNumber class="vesuvius-input-number bg-transparent text-white" :value="value" @input="value => $emit('update:modelValue', value)" />
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { InputNumber } from 'ant-design-vue'

defineProps({
  value: String,
})
</script>

<style lang="scss">
.vesuvius-input-number {
  .ant-input-number-input {
    color: white;

    &::placeholder {
      @apply text-stone-400;
    }
  }
}
</style>