<template>
  <div class="tab">
    <div id="toggle" :class="{ clicked: modelValue }" @click="handleClick()">
      <div class="width-78">
        <img :src="icon" alt="Lijngrafiek icoon" class="prepend-icon" />
        <h2 class="font-20px margin-bottom-none">{{ title }}</h2>
      </div>
      <slot name="append">
        <div>
          <span class="count">{{ count }}</span>
          {{ modelValue ? '▲' : '▼' }}
        </div>
      </slot>
    </div>
    <template v-if="modelValue">
      <div class="content">
        {{ description }}
        <br />
        <b v-if="clickOn">{{ clickOn }}</b>
        <slot name="default" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: boolean
    title?: string
    count?: number | string
    description: string
    clickOn?: string
    icon: string
  }>(),
  {
    title: '',
    count: '',
    clickOn: '',
    description: '',
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', modelValue: boolean): void
}>()

const handleClick = () => {
  emit('update:modelValue', !props.modelValue)
}
</script>

<style scoped lang="scss">
.tab {
  background-color: #e5f1f9;
  margin: 10px 0;
  border: 2px solid transparent;
  border-radius: 8px;
}

.content {
  padding: 20px;
}

#toggle {
  cursor: pointer;
  transition: background-color 0.5s ease;
  padding: 10px;
  display: inline-flex;
  justify-content: space-between;
  width: 100%;
  border: 2px solid transparent;
  border-radius: 8px;
  background-color: #e5f1f9;

  &:hover {
    border: dotted 2px #154273;
  }

  &.clicked {
    border-radius: 8px 8px 0 0;
    border-bottom: solid 1px rgba(21, 66, 115, 0.5);
  }
}
.count {
  margin-right: 10px;
  font-weight: bold;
}

.margin-bottom-none {
  margin-bottom: 0;
}

.prepend-icon {
  float: left;
  width: 24px;
  height: 24px;
  margin-right: 5px;
  vertical-align: middle;
}

.font-20px {
  font-size: 20px;
}

.width-78 {
  width: 78%;
  display: flex;
}
</style>
