const apiFetch = (endpoint: string) => {
  const config = useRuntimeConfig();
  return $fetch(endpoint, { baseURL: config.app.apiBaseUrl });
};

export { apiFetch };
