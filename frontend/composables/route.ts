import qs from 'qs'
import { fileURLToPath } from 'url'

export const useRouteQuery = () => {
  const route = reactive(useRoute())
  const query = toRef(route, 'query')
  return query
}
