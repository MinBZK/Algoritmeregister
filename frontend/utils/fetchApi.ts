const apiFetch = (endpoint: string) => {
  const config = useRuntimeConfig()
  return useFetch(endpoint, { baseURL: config.public.apiBaseUrl })
}

export { apiFetch }
