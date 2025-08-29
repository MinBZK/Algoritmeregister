import { Language } from '@/types/algoritme'
import type { LanguageCode } from '@/types/textLoader'

const changeHash = (hash: string | undefined) => {
  const router = useRouter()
  if (typeof hash === 'string') {
    router.replace({
      hash: '#' + hash,
    })
  } else {
    router.replace({
      hash: '',
    })
  }
}

interface pageTitleInfo {
  title: string
  labelType: 'locale-index' | 'preditor-index' | 'plain-text'
}
const pageTitleInfo = ref<pageTitleInfo>({
  title: '',
  labelType: 'plain-text',
})
const providePageTitle = (
  input: pageTitleInfo = { title: '', labelType: 'plain-text' }
) => {
  pageTitleInfo.value = input
}

const objectMap = (obj: Object, fn: Function) => // eslint-disable-line
  Object.fromEntries(Object.entries(obj).map(([k, v], i) => [k, fn(v, k, i)]))

const mapLocaleName = (language: LanguageCode): Language => {
  if (language === 'nl') return Language.NLD
  if (language === 'en') return Language.ENG
  if (language === 'fy') return Language.FRY
  if (language === 'pap') return Language.PAP
  else return Language.NLD
}

export { objectMap, changeHash, providePageTitle, pageTitleInfo, mapLocaleName }
