<template>
  <div :class="{ 'unsaved-changes': unsavedChange }">
    <v-textarea
      v-if="type === 'name-textarea'"
      id="name-textarea"
      rounded="0"
      :model-value="content"
      :hint="fieldProperties.help_text"
      class="name-textarea"
      rows="1"
      auto-grow
      variant="outlined"
      :counter="fieldProperties.maxLength"
      :rules="fieldProperties.rules"
      @update:focused="emit('update:focus')"
      @update:model-value="(newValue: string) => emit('update:content', newValue)"
    />
    <v-text-field
      v-else-if="type === 'fixed'"
      :model-value="content"
      rounded="0"
      variant="outlined"
      class="fixed-text-field"
      disabled
    />
    <editor-field
      v-else-if="type === 'rich-textarea' || type === 'textarea'"
      :content="content as (string | undefined)"
      :allowed-html-tags="fieldProperties.allowedHtmlTags"
      :help-text="fieldProperties.help_text"
      :counter="fieldProperties.maxLength ?? 100"
      :rules="fieldProperties.rules"
      @update:content="(newValue: string) => emit('update:content', newValue)"
      @update:focused="emit('update:focus')"
      @blur="emit('blur')"
    />
    <v-select
      v-else-if="type === 'select'"
      ref="select"
      rounded="0"
      :model-value="(content as string)"
      :items="fieldProperties.allowedItems!"
      :rules="fieldProperties.rules"
      clearable
      variant="outlined"
      @update:model-value="(newValue: any) => emit('update:content', newValue)"
    />
    <v-select
      v-else-if="type === 'multi-select'"
      ref="select"
      rounded="0"
      :model-value="(content as string[])"
      :items="fieldProperties.allowedItems!"
      :rules="fieldProperties.rules"
      multiple
      clearable
      variant="outlined"
      @update:model-value="(newValue: readonly string[]) => emit('update:content', newValue)"
    />
    <v-combobox
      v-else-if="type === 'optional-select'"
      ref="combobox"
      rounded="0"
      :model-value="(content as string[])"
      :items="fieldProperties.recommendedItems!"
      :rules="fieldProperties.rules"
      multiple
      chips
      clearable
      variant="outlined"
      @update:model-value="(newValue) => emit('update:content', newValue as string[])"
    />
    <list-with-links-field
      v-else-if="type === 'list-with-links'"
      :content="(content as ListWithLinks[])"
      :rules="fieldProperties.rules"
      :help-text="fieldProperties.help_text"
      :items="fieldProperties.recommendedItems"
      @update:content="(newValue) => emit('update:content', newValue)"
      @blur="emit('blur')"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { FormFieldProperties, ListWithLinks } from '@/types/form'
import EditorField from '@/components/editor/EditorField.vue'
import ListWithLinksField from './ListWithLinksField.vue'

defineProps<{
  content?: string | string[] | null | ListWithLinks[]
  type: string | undefined
  fieldProperties: FormFieldProperties
  fieldKey: string
  unsavedChange: boolean
  editorId: string
}>()

const emit = defineEmits<{
  (e: 'update:content', value: any): void
  (e: 'update:focus'): void
  (e: 'showC3poMenu'): void
  (e: 'blur'): void
}>()

// refs to the individual components
const select = ref()
</script>

<style scoped lang="scss">
// Make the field use a big font size
.name-textarea :deep(.v-field__input) {
  font-size: 3em !important;
}

// Styling for the fixed field
.fixed-text-field {
  .v-field__field {
    background-color: #f1f1f1;
  }
}

// Make text bold on unsaved changes
.unsaved-changes {
  :deep(.v-field__input) {
    font-weight: bold !important;
  }
  :deep(.ql-editor) {
    font-weight: bold !important;
  }
}

// small counter adjustment so it doesn't hit the head of the field below it.
:deep(.v-counter) {
  margin-bottom: 0.4em !important;
  margin-top: -0.4em !important;
}
</style>
