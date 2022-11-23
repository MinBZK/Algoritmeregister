import { SummaryTile } from '@/types'

const summaryTiles: SummaryTile[] = [
  {
    label: 'Organisatie',
    key: 'organization',
  },
  {
    label: 'Afdeling',
    key: 'department',
  },
  {
    label: 'Thema',
    key: 'category',
  },
  {
    label: 'Type',
    key: 'type',
  },
  {
    label: 'Status',
    key: 'status',
  },
]

const keys = {
  id: 'id',
  name: 'name',
  description: 'description_short',
  organisation: 'organization',
  department: 'department',
  type: 'type',
  theme: 'category',
  status: 'status',
}

export { summaryTiles, keys }
