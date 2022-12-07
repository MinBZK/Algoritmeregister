const summaryTiles: Array<string> = [
  'organization',
  'department',
  'category',
  'type',
  'status',
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

const navigationItems = [
  {
    label: 'navigation.home',
    routeName: 'index',
  },
  {
    label: 'navigation.algorithmRegister',
    routeName: 'algoritme',
  },
  {
    label: 'navigation.footer',
    routeName: 'footer',
  },
  {
    label: 'navigation.over',
    routeName: 'over',
  },
  {
    label: 'navigation.contact',
    routeName: 'contact',
  },
  {
    label: 'navigation.vragen',
    routeName: 'vragen',
  },
  {
    label: 'navigation.privacyverklaring',
    routeName: 'privacyverklaring',
  },
  {
    label: 'navigation.toegankelijkheid',
    routeName: 'toegankelijkheid',
  },
]

export { summaryTiles, keys, navigationItems }
