import type { SupportingText } from '@/types/textLoader'

const replaceWithMapping = (
  text: string,
  map: Record<string, string>
): string => {
  // If there are {...} entries in the text, this function
  // will replace it with the value in the mapping if the key matches.

  // try to find mapping {...} in the string
  const matches = [...text.matchAll(/(?:{[^{}]+})/g)]

  let replacedText = text
  // replace if the match {...} has a key from the mapping
  matches.forEach((match) => {
    const key = match[0].slice(1, -1)
    if (!map[key]) return
    replacedText = replacedText.replaceAll(match[0], map[key])
  })
  return replacedText
}

export const useTextLoader = () => {
  /**
   * Summary. This composable attempts to mirror a part of the i18n module.
   *
   * The i18n module uses a function named 't('path.here')' to do local translation using
   * the locale JSONs. This can be replaced with the 'p('path.here')' function for textLoader,
   * Which will look up the indicated path in the supporting text from textLoader instead.
   *
   * Description. To migrate to textLoader from i18n do the following:
   * const { t } = usei18n() -> const { p } = useTextLoader()
   * t('someKeyHere') -> p('someKeyHere')
   */
  const { currentLocale } = useLocale()
  const locale = computed(() => currentLocale.value)

  const supportingText = useState<SupportingText | null>(
    'supportingText',
    () => null
  )

  const localPrefix = `/${currentLocale.value}`
  // Looks up key in the supporting text. language is based on currentLocale
  const p = (key: string, map?: Record<string, string>) => {
    if (!supportingText.value) return key

    try {
      const localisedSupportText = supportingText.value[currentLocale.value]
      const value = key
        .split('.')
        .reduce(
          (obj, subKey) => obj[subKey as keyof SupportingText],
          localisedSupportText
        ) as string

      const localisedText = value.replace('{localised_url}', localPrefix)
      if (!map) return localisedText
      return replaceWithMapping(localisedText, map)
    } catch (error) {
      return key
    }
  }

  return {
    p,
    locale,
  }
}
