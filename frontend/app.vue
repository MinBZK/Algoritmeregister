<template v-show="supportingTextLoaded">
  <ClientOnly>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </ClientOnly>
</template>

<script setup lang="ts">
import { SupportingText } from './types/textLoader'
import { getAllContent } from './services/textLoader'

const supportingTextLoaded = ref<boolean>(false)

const supportingText = useState<SupportingText | null>(
  'supportingText',
  () => null
)
const { data } = getAllContent()
supportingText.value = data.value
if (supportingText.value) {
  supportingTextLoaded.value = true
}
</script>
