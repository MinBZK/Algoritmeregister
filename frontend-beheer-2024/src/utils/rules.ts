export const emailRule = (value: string) => {
  if (/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(value)) return true
  return 'Gebruik een geldig e-mailadres, zoals naam@domein.nl'
}

export const requiredRule = (value: string) => {
  if (value) return true
  return 'Dit veld is verplicht'
}

export const nameNewNotAllowedRule = (value: string) => {
  if (value !== 'new') return true
  return 'new kan niet als technische naam gebruikt worden.'
}

export const minRequiredRule = (values: any[], minRequired: number) => {
  if (values.length >= minRequired) return true
  return `Er moet op z'n minst ${minRequired} zijn geselecteerd.`
}
