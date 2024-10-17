<template>
  <div class="pb-6">
    <v-card
      rounded="0"
      flat
      border
      class="wrapper"
    >
      <v-row v-for="(row, n) in content" :key="n">
        <v-col cols="4">
          <v-combobox
            :value="row.title"
            density="compact"
            hide-details
            rounded="0"
            clearable
            variant="outlined"
            :items="items"
            @focus="showFeedback = true"
            @update:model-value="(e: string | null) => handleUpdate(n, 'title', e)"
          />
        </v-col>
        <v-col>
          <v-text-field
            :value="row.link"
            hide-details
            density="compact"
            variant="outlined"
            @update:model-value="(e: string) => handleUpdate(n, 'link', e)"
            @focus="showFeedback = true"
            @blur="handleBlur"
          />
        </v-col>
        <v-col cols="1">
          <v-btn
            block
            flat
            border
            rounded="0"
            class="remove-button"
            @click="removeField(n)"
          >
            <v-icon>mdi-minus</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-btn
          rounded="0"
          variant="outlined"
          border
          class="add-button"
          color="blue-lighten-1"
          @click="addField"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-row>
    </v-card>
    <editor-feedback
      v-show="showFeedback"
      :help-text="helpText"
      :active="showFeedback"
    />
  </div>
</template>

<script setup lang="ts">
import { ListWithLinks } from '@/types/form'
import EditorFeedback from '@/components/editor/EditorFeedback.vue'
import { ref } from 'vue'

const showFeedback = ref<boolean>(false)

const props = defineProps<{
  content?: ListWithLinks[]
  helpText?: string
  rules?: ((v: any) => boolean | string)[]
  items?: string[]
}>()

const emit = defineEmits<{
  (e: 'update:content', value: ListWithLinks[]): void
  (e: 'blur'): void
}>()

const addField = () => {
  const withExtraField = (props.content || []).concat({
    title: null,
    link: null,
  })
  emit('update:content', withExtraField)
}

const handleBlur = () => {
  showFeedback.value = false
  emit('blur')
}

const removeField = (entry: number) => {
  let newContent = [...props.content!]
  if (entry === 0) {
    newContent.shift()
  }
  newContent.splice(entry, entry)
  emit('update:content', newContent)
}

const handleUpdate = (
  entry: number,
  key: 'title' | 'link',
  value: string | null
) => {
  let newContent = [...props.content!]
  if (value?.length === 0) {
    value = null
  }
  newContent[entry]![key] = value
  emit('update:content', newContent)
}
</script>

<style scoped lang="scss">
.wrapper {
  padding: 1em;
  border-color: rgb(172, 172, 172);
  :deep(input) {
    font-size: 0.9em;
  }
}

.add-button {
  margin: 12px;
}

.remove-button {
  border-color: rgb(172, 172, 172);
}

:deep(.v-row + .v-row) {
  margin-top: 0;
}
</style>
