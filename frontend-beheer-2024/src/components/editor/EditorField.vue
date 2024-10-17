<template>
  <div class="pb-6">
    <p-editor
      ref="editor"
      :model-value="content"
      :editor-style="editorStyle"
      :modules="{ keyboard: { bindings } }"
      :class="enabledClasses"
      @click="editorFocused = true"
      @update:model-value="(newValue: string) => emit('update:content', newValue)"
    >
      <template #toolbar>
        <editor-toolbar :formats="formats" />
      </template>
    </p-editor>
    <editor-feedback
      v-show="editorFocused"
      :error-messages="errorMessages"
      :help-text="helpText"
      :max-char-count="counter"
      :char-count="countWithoutHTMLTags(content || '')"
      :active="editorFocused"
      :editor-foucsed="editorFocused"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'
import { onClickOutside } from '@vueuse/core'
import {
  countWithoutHTMLTags,
  toRichTextFormat,
  initSpellchecker,
} from '@/utils/editor'
import EditorFeedback from '@/components/editor/EditorFeedback.vue'
import EditorToolbar from '@/components/editor/EditorToolbar.vue'
import keyBindings from 'quill/modules/keyboard'
import Quill from 'quill'
import { useAuthStore } from '@/store/auth'

const props = defineProps<{
  content?: string
  helpText?: string
  rules?: ((v: any) => boolean | string)[]
  counter?: number
  allowedHtmlTags?: string[]
}>()

const emit = defineEmits<{
  (e: 'update:content', modelValue: string): void
  (e: 'update:focused'): void
  (e: 'blur'): void
}>()

const authStore = useAuthStore()

// Set up editor with allowed formats
const editor = ref<Quill>(null)
onMounted(() => {
  if (editor.value) {
    initSpellchecker(
      editor.value.$el,
      authStore.APIurl,
      authStore.keycloak.idToken || ''
    )
  }
})
const editorStyle = { fontSize: '.95rem' }
const formats = computed(() =>
  props.allowedHtmlTags ? toRichTextFormat(props.allowedHtmlTags) : []
)

// Remove keyboard shortcuts based on allowed formats
const bindings = computed(() => {
  const relevantKeyBindingsFormat = ['bold', 'italic', 'underline']
  const bindingsToRemove = relevantKeyBindingsFormat.filter(
    (format) => !formats.value.includes(format)
  )
  const allBindings = keyBindings.DEFAULTS.bindings
  Object.keys(allBindings).forEach((key) => {
    if (bindingsToRemove.includes(key)) {
      allBindings[key].handler = () => false
    }
  })
  const hasListFormat =
    formats.value.filter((format) => format.class === 'list').length !== 0
  if (hasListFormat) {
    return { ...allBindings }
  }
  Object.keys(allBindings).forEach((key) => {
    if (allBindings[key].format) {
      allBindings[key].format = []
    }
  })
  return { ...allBindings }
})

// Add focus functionality
const editorFocused = ref(false)
onClickOutside(editor, () => {
  editorFocused.value = errorMessages.value.length > 0
})
watch(
  () => editorFocused.value,
  (newValue) => (newValue ? emit('update:focused') : emit('blur'))
)

// Dynamically add classes to editor based on current state
const enabledClasses = computed(() => {
  return {
    'hide-toolbar': formats.value.length === 0,
    focused: editorFocused.value,
    error: errorMessages.value.length > 0,
  }
})

// Get error messages from rules
const errorMessages = computed(() => {
  const errorMessages = [] as string[]
  const noRules = !props.rules?.length
  const isValid = props.rules?.every((rule) => rule(props.content) === true)
  if (noRules || isValid) {
    return errorMessages
  }
  return props.rules?.map((rule) => rule(props.content)) as string[]
})
</script>

<style scoped lang="scss">
.hide-toolbar {
  :deep(.ql-toolbar) {
    display: none;
  }
  :deep(.ql-editor) {
    border-top: 1px solid #ccc;
  }
}

.focused {
  :deep(.ql-editor) {
    border: 2px solid;
    padding: 10.43px 13px;
  }
}

.error {
  :deep(.ql-editor) {
    border-color: rgba(229, 57, 53, 0.8);
  }
}
</style>
