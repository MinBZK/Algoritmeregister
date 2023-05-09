<template v-show="supportingTextLoad">
  <ClientOnly>
    <NuxtLayout>
      <div>
        <h1>{{ t('error.pageNotFound') }}</h1>
        <FormOverheidButton
          :label="t('error.goToHome')"
          @click="$router.push(localePath({ path: '/' }))"
        />
      </div>
    </NuxtLayout>
  </ClientOnly>
</template>

<script setup lang="ts">
import { SupportingText } from './types/textLoader'
import { getAllContent } from './services/textLoader'

const supportingTextLoaded = ref<boolean>(true)

const supportingText = useState<SupportingText | null>(
  'supportingText',
  () => null
)
const { data } = getAllContent()
supportingText.value = data.value
if (supportingText.value) {
  supportingTextLoaded.value = true
}

const { t } = useI18n()
const localePath = useLocalePath()

defineProps<{ error: Error }>()

const pageTitle = computed(() => t('error.pageNotFound'))

useHead({ title: pageTitle })
</script>
