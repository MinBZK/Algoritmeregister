import { apiFetch } from '@/utils/fetchApi'

const getAll = () =>
  apiFetch('/algoritme').then((response) => {
    return response.data
  })

const getOne = (id: string) =>
  apiFetch(`/algoritme/${id}/`).then((response) => response.data)

export default { getAll, getOne }
