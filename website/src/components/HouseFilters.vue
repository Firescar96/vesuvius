<template>
  <form @submit.prevent="$emit('submit')" class="flex gap-2 items-center">

    <span>Address</span>
    <Input class="w-auto" v-model="address" placeholder="2603 N. Richards Street" />

    <span>Bedrooms</span>
    <InputNumber v-model="bedrooms" placeholder="bedrooms"/>

    <Button htmlType="submit" class="bg-blue-400">Search</Button>
  </form>
</template>


<script setup lang="ts">
import {ref, defineEmits, watch} from 'vue'
import {Input, InputNumber, Button} from '@/components'

const {modelValue} = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])
const address = ref(modelValue.address)
const bedrooms = ref(modelValue.bedrooms)


watch([address, bedrooms], () => {
  emit('update:modelValue', {address: address.value, bedrooms: bedrooms.value})
}, {deep: true})
</script>