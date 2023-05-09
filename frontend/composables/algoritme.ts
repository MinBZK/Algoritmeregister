import { Algoritme } from '~~/types/algoritme'

export const useAlgoritme = () => {
  const algoritme = useState<Algoritme | null>('algoritme', () => null)
  const setAlgoritme = (a: Algoritme | null) => (algoritme.value = a)

  const route = useRoute()
  watch(route, () => {
    if (!route.name?.toString().includes('algoritme-lars')) setAlgoritme(null)
  })

  return {
    algoritme,
    setAlgoritme,
  }
}
