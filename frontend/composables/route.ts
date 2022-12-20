import { parse } from 'qs'

export const useRouteQuery = () => {
  const query = useRoute().query.q
  const queryString = (Array.isArray(query) ? query[0] : query) || ''
  const parsed = reactive(parse(queryString.toString()))
  return parsed
}
