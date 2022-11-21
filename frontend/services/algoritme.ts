// const apiFetch = (endpoint: string) => {
//   const config = useRuntimeConfig();
//   return $fetch(endpoint, { baseURL: config.app.apiBaseUrl });
// };
import { apiFetch } from "@/utils/fetchApi";

const getAll = async () => apiFetch("/project");

const getOne = async (id: string) => apiFetch(`/project/${id}`);

export default { getAll, getOne };
