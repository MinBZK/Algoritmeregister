<template v-show="supportingTextLoaded">
  <div>
    <NuxtLoadingIndicator color="#007bc7" />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <ClientOnly><UsePiwik /></ClientOnly>
  </div>
</template>

<script setup lang="ts">
import type { SupportingText } from './types/textLoader'
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
