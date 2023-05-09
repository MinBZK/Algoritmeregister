<template>
  <span ref="target" class="word-break" ca> <slot> </slot> </span>
</template>

<script setup lang="ts">
const { t } = useI18n()

const linkify = (inputText: string) => {
  const externalLinkLabel = t('externalLink')
  const mailLinkLabel = t('mailLink')
  const patterns: { [key: string]: any } = {
    url_remove_www_with_https: {
      regex: /(?<!(http(s)?:\/\/))www\./gm,
      template: 'https://',
    },
    url_remove_www_without_https: {
      regex: /(?<=http(s)?:\/\/)www\./gm,
      template: '',
    },
    url: {
      regex:
        // eslint-disable-next-line
        /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim,
      template: `<a href="$1" target="_blank">$1 <img class="is-external-icon" alt="${externalLinkLabel}" src="/icon-link-external-v2.svg"/></a>`,
    },
    mail: {
      // eslint-disable-next-line
      regex: /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim,
      template: `<a href="mailto:$1" class="is-mail" alt="${mailLinkLabel}">$1</a>`,
      // template: `<a href="mailto:$1" target="_blank">$1 <img class="is-external-icon" alt="${mailLinkLabel}" src="/icon-mail.svg"/></a>`,
    },
  }

  let replacedText: string = inputText
  Object.keys(patterns).map(
    (patternKey: string) =>
      (replacedText = replacedText.replaceAll(
        patterns[patternKey].regex,
        patterns[patternKey].template
      ))
  )
  return replacedText
}

const target = ref<HTMLDivElement | null>(null)
const { currentLocale } = useLocale()

const originalContent = ref('')

onMounted(() => {
  if (target.value) {
    originalContent.value = target.value?.innerHTML
  }
})

const parseTarget = () => {
  if (target.value) {
    target.value.innerHTML = linkify(originalContent.value)
  }
}

watch(target, () => parseTarget())
watch(currentLocale, () => {
  parseTarget()
})
</script>

<style lang="scss">
.word-break {
  word-break: break-word;
}
</style>
