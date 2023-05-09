import { FormFieldProperties, SchemaProperties } from '@/types/form'

export function buildRulesFromProperties(
  field: FormFieldProperties
): ((v: any) => boolean | string)[] {
  const rules = []
  if (field.type == 'string') {
    if (field.maxLength) {
      rules.push(
        (v: string | null) =>
          (v?.length || 0) <= field.maxLength! ||
          `Maximaal ${field.maxLength} karakters`
      )
    }
  }
  if (field.type == 'enum') {
    if (field.allowedValues) {
      rules.push(
        (v: string | null) =>
          (v ? Object.values(field.allowedValues!).includes(v) : true) ||
          'Selecteer 1 van de toegestane waardes.'
      )
    }
  }

  if (field.required) {
    rules.push((v: string | null) => !!v || 'Dit veld moet ingevuld zijn.')
  }
  return rules
}

export function buildPlaceholderFromSchema(field: SchemaProperties): string {
  if (field.show_always) {
    return 'Dit veld is niet ingevuld'
  }
  return ''
}
