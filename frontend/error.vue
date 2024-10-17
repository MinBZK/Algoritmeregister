<template v-show="supportingTextLoad">
  <NuxtLayout>
    <div>
      <h1>{{ t('error.pageNotFound') }}</h1>
      <FormOverheidButton
        :label="t('error.goToHome')"
        @click="router.push(localePath({ path: '/' }))"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { getAllContent } from './services/textLoader'
import type { SupportingText } from '@/types/textLoader'

const router = useRouter()

const supportingTextLoaded = ref<boolean>(true)

const supportingText = useState<SupportingText | null>(
  'supportingText',
  () => null
)
const { data } = await getAllContent()
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
