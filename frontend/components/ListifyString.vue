<template>
  <div v-if="arrayType === 'simple'" class="width-sizing" :style="listStyle">
    <ul style="margin-bottom: 0">
      <li v-for="cell in text" :key="cell as string" class="word-break">
        {{ cell }}
      </li>
    </ul>
  </div>
  <div
    v-else-if="arrayType === 'list-with-links'"
    class="width-sizing"
    :style="listStyle"
  >
    <ul style="margin-bottom: 0">
      <li v-for="(cell, n) in text" :key="n" class="word-break">
        {{ (cell as ListWithLinks).title }}:
        {{ (cell as ListWithLinks).link }}
      </li>
    </ul>
  </div>
  <div v-else-if="arrayType === 'list-with-links-single'" class="width-sizing">
    {{ (text[0] as ListWithLinks).title }}:
    {{ (text[0] as ListWithLinks).link }}
  </div>
  <div v-else class="width-sizing custom-html" v-html="text" />
</template>

<script setup lang="ts">
interface ListWithLinks {
  title?: string | null
  link?: string | null
}

const props = defineProps<{
  text: string | string[] | ListWithLinks[]
  listStyle?: string
}>()

const arrayType = computed(() => {
  if (Array.isArray(props.text)) {
    if (props.text[0].constructor === Object) {
      if (props.text.length > 1) {
        return 'list-with-links'
      }
      return 'list-with-links-single'
    }
    if (props.text.length > 1) {
      return 'simple'
    }
  }
  return false
})
</script>

<style lang="scss">
// adjustment for any v-html element.
.custom-html {
  padding-left: 0 !important;

  ol {
    padding-left: 2em !important;
    list-style-type: decimal;
    margin-bottom: 0.5em;
  }

  ul {
    padding-left: 2em;
    list-style-type: disc;
    margin-bottom: 0.5em;
  }

  p {
    margin-bottom: 0.5em;
  }
}

.width-sizing {
  width: 100% !important;
}
</style>
