import { Algoritme } from '~~/types/algoritme'

export const useAlgoritme = () => {
  const algoritme = useState<Algoritme | null>('algoritme', () => null)
  const setAlgoritme = (a: Algoritme) => (algoritme.value = a)
  return {
    algoritme,
    setAlgoritme,
  }
}
