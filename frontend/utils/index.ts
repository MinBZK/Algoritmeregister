import { Language } from '@/types/algoritme'

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
  labelType: 'locale-index' | 'page-title'
}
const pageTitleInfo = ref<pageTitleInfo>({
  title: '',
  labelType: 'page-title',
})
const providePageTitle = (
  input: pageTitleInfo = { title: '', labelType: 'page-title' }
) => {
  pageTitleInfo.value = input
}

const objectMap = (obj: Object, fn: Function) =>
  Object.fromEntries(Object.entries(obj).map(([k, v], i) => [k, fn(v, k, i)]))

const mapLocaleName = (language: 'nl' | 'en'): Language => {
  if (language === 'nl') return Language.NLD
  if (language === 'en') return Language.ENG
  else return Language.NLD
}

export { objectMap, changeHash, providePageTitle, pageTitleInfo, mapLocaleName }
