<template>
  <div
    class="version-selection-box my-4 pa-4"
    :data-selected="focus"
    @click="$emit('click')"
  >
    <div class="version-selection-box-structure">
      <v-icon color="grey" size="24">
        mdi-history
      </v-icon>
      <div>
        <strong v-if="data.create_dt">
          Versie van
          {{ formatDateTime(data.create_dt) }}
        </strong>
        <p class="text-grey-darken-1">
          Door {{ data.user_id }}
        </p>
        <v-chip v-if="data.state == 'ARCHIVED'" class="mt-3">
          Gearchiveerd
        </v-chip>
      </div>
      <v-tooltip
        :text="data.state === 'ARCHIVED' ? 'Dearchiveer' : 'Archiveer'"
        location="bottom"
      >
        <template #activator="{ props }">
          <v-btn
            v-if="!data.published"
            v-bind="props"
            :icon="
              data.state === 'ARCHIVED'
                ? 'mdi-package-up'
                : 'mdi-archive-arrow-down-outline'
            "
            class="mr-0 ml-auto rounded-lg p-0"
            color="primary"
            variant="tonal"
            size="38"
            rounded="0"
            @click="performArchiveAction"
          />
        </template>
      </v-tooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AlgorithmWithUser } from '@/types/algorithm'
import { useArchiveStore } from '@/store/archive'
import { formatDateTime } from '@/utils/datetime'

const archiveStore = useArchiveStore()

const comProps = defineProps<{
  data: AlgorithmWithUser
  focus: boolean
  lars: string
}>()

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'change'): void
}>()

const performArchiveAction = async () => {
  if (comProps.data.state === 'ARCHIVED') {
    await archiveStore.unarchiveVersion(comProps.lars, comProps.data.id)
  }
  else {
    await archiveStore.archiveVersion(comProps.lars, comProps.data.id)
  }
  emit('change')
  archiveStore.selectedVersion = null
}
</script>

<style scoped lang="scss">
.version-selection-box {
  border: 0;
  background-color: white;
  border-radius: 8px;
  width: 100%;
  font-size: 0.75em;

  margin-bottom: 3px;
  &[data-selected='true'] {
    border: 3px solid $primary-dark;
    margin-bottom: 0px;
  }
  &:hover {
    background-color: $secondary;
  }
}

.version-selection-box-structure {
  display: inline-flex;
  width: 100%;
  gap: 1em;
}
</style>
