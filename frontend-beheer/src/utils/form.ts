import { FormFieldProperties } from '@/types/form'
import { countWithoutHTMLTags } from '@/utils/editor'

export function buildRulesFromProperties(
  field: FormFieldProperties
): ((v: any) => boolean | string)[] {
  const rules = []
  if (
    field.type == 'textarea' ||
    field.type == 'rich-textarea' ||
    field.type == 'name-textarea'
  ) {
    if (field.maxLength) {
      // Rule: Only maximum amount of characters allowed
      rules.push((v: string | null) => {
        return (
          countWithoutHTMLTags(v) <= field.maxLength! ||
          `Maximaal ${field.maxLength} karakters`
        )
      })
    }
  }
  if (field.type == 'select') {
    // Rule: Only allowed items allowed.
    if (field.allowedItems) {
      rules.push(
        (v: string | null) =>
          (v ? Object.values(field.allowedItems!).includes(v) : true) ||
          'Selecteer 1 van de toegestane waardes.'
      )
    }
  }

  if (field.type == 'multi-select' || field.type == 'optional-select') {
    // Rule: Only max items allowed
    rules.push((v: string[] | null) => {
      if (!v) return true
      if (!field.maxItems) return true
      const errorMsg = `Selecteer maximaal ${field.maxItems} waardes.`
      return v.length > field.maxItems ? errorMsg : true
    })
  }

  if (field.type == 'multi-select') {
    // Rule: only values present in *allowedItems* can be used.
    rules.push((v: string[] | string | null) => {
      if (!v) return true
      if (!field.allowedItems) return true
      const errorMsg = 'Selecteer alleen toegestane waardes.'

      if (Array.isArray(v)) {
        const firstBadEntry = v.find(
          (value) =>
            // Finds value *outside* of allowedItems.
            !Object.values(field.allowedItems!).includes(value)
        )
        return !!firstBadEntry ? errorMsg : true
      } else {
        return Object.values(field.allowedItems!).includes(v) ? true : errorMsg
      }
    })
  }

  if (field.required) {
    rules.push((v: string | null) => !!v || 'Dit veld moet ingevuld zijn.')
  }
  return rules
}
