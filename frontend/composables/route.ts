import qs from 'qs'

export const useRouteQuery = () => {
  const query = useRoute().query.q
  const queryString = (Array.isArray(query) ? query[0] : query) || ''
  const parsed = reactive(qs.parse(queryString.toString()))
  return parsed
}
