<template>
  <v-card style="width: 750px; height: 300px; overflow: hidden">
    <div style="display: flex; height: 100%">
      <div style="width: 30%">
        <v-btn
          style="height: 14%"
          class="text-lowercase btn-title"
          block
          flat
          rounded="0"
          :color="getAllRuleButtonColor()"
          @click="c3poRequest"
        >
          <template v-if="!loading">
            Toets op alle regels
          </template>
          <template v-else>
            <v-progress-circular
              indeterminate
              color="yellow-darken-3"
              :width="6"
            />
          </template>
        </v-btn>
        <v-list style="overflow-y: scroll; height: 86%">
          <v-list-item
            v-for="rule in rules"
            :key="rule.rule_code"
            density="comfortable"
            style="font-size: 0.8em"
            @click="setSelectedRule(rule)"
          >
            <template #prepend>
              <v-icon
                :icon="getIcon(rule.result)"
                :color="getIconColor(rule.result)"
              />
            </template>
            {{ rule.rule_code }}
          </v-list-item>
        </v-list>
      </div>
      <div style="width: 70%">
        <v-card
          class="d-flex flex-column pa-2"
          height="100%"
          rounded="0"
        >
          <template v-if="selectedRule">
            <v-card-title>
              <template #default>
                <div style="display: flex; flex-direction: row">
                  {{ selectedRule?.rule_code }}
                  <v-spacer />
                  <v-icon
                    :icon="getIcon(selectedRule.result)"
                    :color="getIconColor(selectedRule.result)"
                  />
                </div>
              </template>
            </v-card-title>

            <v-card-text style="flex: 0 1 auto">
              {{ selectedRule.description }}
            </v-card-text>
            <v-card-subtitle> Feedback:</v-card-subtitle>
            <v-card-text>
              {{ selectedRule?.feedback_message }}
            </v-card-text>
            <!-- <v-card-subtitle>
            <template #default>
              <div style="display: flex; flex-direction: row">
                Verbeteringssuggestie:
                <v-btn
                  size="20"
                  icon="mdi-content-copy"
                  class="ml-2"
                />
              </div>
            </template>
          </v-card-subtitle>

          <v-card-text>
            Deze tekst is een stuk simpeler. In plaats van lange zinnen gebruik
            ik korte zinnen. Lalala Korte zin. Je kan deze tekst kopiëren als je
            wil.
          </v-card-text> -->
          </template>
          <template v-else>
            <v-card-title style="color: grey">
              Selecteer een regel om meer informatie te zien...
            </v-card-title>
          </template>
          <v-spacer />
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="emit('closeMenu')">
              sluiten
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { postC3poRequest } from '@/services/c3po'
import { RuleResults } from '@/types/c3po'
import { useSchemaStore } from '@/store/schema'

const schemaStore = useSchemaStore()

const props = defineProps<{
  ruleSet: string
  text: string
}>()

const emit = defineEmits<{
  (e: 'closeMenu'): void
}>()

const rules = ref<RuleResults[]>()
const setInitialRules = () => {
  const ruleSet = schemaStore.ruleSets.find(
    (ruleSet) => ruleSet.code == props.ruleSet
  )

  const parsedRules = ruleSet?.rules.map((rule) => {
    return {
      rule_code: rule.rule_code,
      description: rule.description,
      feedback_message: '',
      result: null,
    }
  })
  rules.value = parsedRules
}
setInitialRules()

const selectedRule = ref<RuleResults | null>()
const setSelectedRule = (rule: RuleResults) => {
  selectedRule.value = rule
}

const loading = ref(false)
const c3poRequest = () => {
  const body = { text: props.text, ruleSet: props.ruleSet }
  loading.value = true
  postC3poRequest(body)
    .then((response) => {
      rules.value = response.data.rules
      loading.value = false

      const updatedRule = rules.value.find(
        (rule) => selectedRule.value?.rule_code == rule.rule_code
      )
      if (updatedRule) {
        setSelectedRule(updatedRule)
      }
    })
    .catch(() => (loading.value = false))
}

const getIcon = (result: boolean | null) => {
  if (typeof result !== 'boolean') return 'mdi-help'
  return result ? 'mdi-check' : 'mdi-alert'
}

const getIconColor = (result: boolean | null) => {
  if (typeof result !== 'boolean') return 'grey'
  return result ? 'green' : 'red'
}

const getAllRuleButtonColor = () => {
  const neutral = !rules.value?.find((rule) => typeof rule.result === 'boolean')
  if (neutral) return 'grey-lighten-3'

  const badRuleFound = rules.value?.find((rule) => !rule.result)
  return badRuleFound ? 'red-lighten-1' : 'green-lighten-1'
}
</script>

<style lang="scss">
.btn-title:first-letter {
  text-transform: capitalize;
}
</style>
