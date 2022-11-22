const apiFetch = (endpoint: string) => {
  const config = useRuntimeConfig()
  return useFetch(endpoint, { baseURL: config.app.apiBaseUrl })
}

export { apiFetch }
