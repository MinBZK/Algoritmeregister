<template>
  <span ref="target">
    <slot> </slot>
  </span>
</template>

<script setup lang="ts">
const linkify = (inputText: string) => {
  const patterns: { [key: string]: any } = {
    url: {
      regex:
        // eslint-disable-next-line
        /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim,
      template: '<a href="$1" target="_blank">$1</a>',
    },
    mail: {
      // eslint-disable-next-line
      regex: /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim,
      template: '<a href="mailto:$1">$1</a>',
    },
  }

  let replacedText: string = inputText
  Object.keys(patterns).map(
    (patternKey: string) =>
      (replacedText = replacedText.replace(
        patterns[patternKey].regex,
        patterns[patternKey].template
      ))
  )
  return replacedText
}

const target = ref<HTMLDivElement | null>(null)
watch(target, () => {
  if (target.value) {
    target.value.innerHTML = linkify(target.value.innerHTML)
  }
})
</script>
