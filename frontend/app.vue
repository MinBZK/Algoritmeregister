<template v-show="supportingTextLoaded">
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import { SupportingText } from './types/textLoader'
import { getAllContent } from './services/textLoader'

const supportingTextLoaded = ref<boolean>(false)

const supportingText = useState<SupportingText | null>(
  'supportingText',
  () => null
)

const { data } = await getAllContent()
supportingText.value = data.value
if (supportingText.value) {
  supportingTextLoaded.value = true
}
</script>
