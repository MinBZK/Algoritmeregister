import type { LanguageCode } from '@/types/textLoader'
import type { Algoritme } from '@/types/algoritme'
import algoritmeService from '@/services/algoritme'

export const useAlgoritme = () => {
  const algoritme = useState<Algoritme | null>('algoritme', () => null)
  const setAlgoritme = (a: Algoritme | null) => (algoritme.value = a)

  const getAndSetAlgoritme = async (lars: string, locale: LanguageCode) => {
    const { data } = await algoritmeService.getOne(lars, mapLocaleName(locale))
    algoritme.value = data.value as Algoritme
  }

  const route = useRoute()
  watch(
    () => route.name,
    () => {
      if (!route.name?.toString().includes('algoritme-params'))
        setAlgoritme(null)
    }
  )

  return {
    algoritme,
    setAlgoritme,
    getAndSetAlgoritme,
  }
}
