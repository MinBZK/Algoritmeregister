const apiFetch = (endpoint: string) => {
  const config = useRuntimeConfig()
  console.log(endpoint, { baseURL: config.app.apiBaseUrl })
  return useFetch(endpoint, { baseURL: config.app.apiBaseUrl })
}

export { apiFetch }
