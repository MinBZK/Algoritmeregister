import { apiFetch } from '@/utils/fetchApi'

const getAll = () => apiFetch('/project').then((response) => response.data)

const getOne = (id: string) =>
  apiFetch(`/project/${id}`).then((response) => response.data)

export default { getAll, getOne }
